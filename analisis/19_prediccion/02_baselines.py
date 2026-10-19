"""Tarea 3. Lineas base sin entender el sistema, sobre las mismas cuerdas ocultas (una por vez) que el LOO.
Base 1 mediana de la columna (misma posicion en el registro, resto del quipu) y 1b media; Base 2 valor del registro anterior en
esa posicion; Base 3 valor mas frecuente del quipu; Base 4 magnitud de fila: en UR278 modelo log aditivo fila+columna,
en el resto razon mediana valor/cabecera x cabecera (cabecera: razon cabecera/suma del resto). Salida: baselines_resultados.csv
y tabla comparativa por regla."""
import numpy as np
import pandas as pd
from collections import Counter
import comun19 as M

cons = pd.read_csv(M.AQUI / "loo_consenso.csv")
L = pd.read_csv(M.AQUI / "loo_resultados.csv")


def clave(t):
    k, i = M.REC_DE[t]
    r = M.REC[k][i]
    lv = M.INFO[t]["nivel"]
    same = [x for x in r["cords"] if M.INFO[x]["nivel"] == lv]
    return k, i, (lv, same.index(t))


def valor_en(k, i, key):
    r = M.REC[k][i]
    same = [x for x in r["cords"] if M.INFO[x]["nivel"] == key[0]]
    return M.VAL[same[key[1]]] if key[1] < len(same) else None


def base_ur278(t):
    rows = {r["g"]: r["l0"] for r in M.REC["UR278"]}
    g = M.REC["UR278"][M.REC_DE[t][1]]["g"]
    if t not in rows[g]:
        return None
    j = rows[g].index(t)
    data = [(gg, jj, np.log(M.VAL[x])) for gg, l0 in rows.items() for jj, x in enumerate(l0)
            if M.VAL[x] and x != t]
    D = pd.DataFrame(data, columns=["g", "j", "lv"])
    a = pd.Series(0.0, index=D.g.unique())
    b = pd.Series(0.0, index=D.j.unique())
    for _ in range(10):
        a = (D.lv - D.j.map(b)).groupby(D.g).mean()
        b = (D.lv - D.g.map(a)).groupby(D.j).mean()
    if g not in a.index or j not in b.index:
        return None
    return int(round(np.exp(a[g] + b[j])))


def bases(t):
    k, i, key = clave(t)
    otros = [(ii, valor_en(k, ii, key)) for ii in range(len(M.REC[k])) if ii != i]
    vs = [v for _, v in otros if v]
    out = {}
    if vs:
        out["mediana_col"] = int(round(np.median(vs)))
        out["media_col"] = int(round(np.mean(vs)))
    prev = [v for ii, v in otros if ii < i and v]
    if prev:
        out["registro_previo"] = prev[-1]
    todos = [M.VAL[x] for x in M.ORD[k] if x != t and M.VAL[x]]
    out["moda_quipu"] = Counter(todos).most_common(1)[0][0]
    if k == "UR278":
        b4 = base_ur278(t)
        if b4:
            out["magnitud_fila"] = b4
    else:
        r = M.REC[k][i]
        if r["header"] is not None:
            hdr = r["header"]
            if t == hdr:
                suma = sum(M.VAL[x] or 0 for x in r["cords"] if x != t)
                rat = []
                for ii, rr in enumerate(M.REC[k]):
                    if ii != i and rr["header"] and M.VAL[rr["header"]]:
                        s2 = sum(M.VAL[x] or 0 for x in rr["cords"] if x != rr["header"])
                        if s2:
                            rat.append(M.VAL[rr["header"]] / s2)
                if rat and suma:
                    out["magnitud_fila"] = int(round(np.median(rat) * suma))
            elif M.VAL[hdr]:
                rat = [v / M.VAL[M.REC[k][ii]["header"]] for ii, v in otros
                       if v and M.REC[k][ii]["header"] and M.VAL[M.REC[k][ii]["header"]]]
                if rat:
                    out["magnitud_fila"] = int(round(np.median(rat) * M.VAL[hdr]))
    return out


filas = []
for r in cons.itertuples():
    t = (r.quipu, r.cuerda)
    for nombre, p in bases(t).items():
        filas.append(dict(quipu=r.quipu, cuerda=r.cuerda, real=r.real, metodo=nombre, pred=p, **M.metricas(p, r.real)))
B = pd.DataFrame(filas)
B.to_csv(M.AQUI / "baselines_resultados.csv", index=False)

pd.set_option("display.width", 200)
CB = [c for c in ["mediana_col", "media_col", "registro_previo", "moda_quipu", "magnitud_fila"]]


def fila_tabla(nombre, sub_cons, regla=None):
    res = {"n": len(sub_cons)}
    m = sub_cons
    res["modelo_exacta"], res["modelo_tol"], res["modelo_r5"] = m.exacta.mean(), m.tol.mean(), m.r5.mean()
    keys = set(zip(m.quipu, m.cuerda))
    ex_union = np.zeros(len(m), bool)
    for c in CB:
        b = B[(B.metodo == c)]
        b = b[[(q, cu) in keys for q, cu in zip(b.quipu, b.cuerda)]].set_index(["quipu", "cuerda"])
        idx = pd.MultiIndex.from_frame(m[["quipu", "cuerda"]])
        bb = b.reindex(idx)
        # sin prediccion de la base = fallo
        res[f"{c}_exacta"] = bb.exacta.fillna(False).astype(float).mean()
        res[f"{c}_tol"] = bb.tol.fillna(False).astype(float).mean()
        ex_union |= bb.exacta.fillna(False).to_numpy(bool)
    res["union_bases_exacta"] = ex_union.mean()
    return pd.Series(res, name=nombre)


tabla = [fila_tabla("TODAS (consenso por cuerda)", cons)]
for regla in ["celda270", "cierre", "copia", "cuota", "fila278", "suma_AB"]:
    ks = set(zip(L[L.regla == regla].quipu, L[L.regla == regla].cuerda))
    sub = cons[[(q, c) in ks for q, c in zip(cons.quipu, cons.cuerda)]].copy()
    # el modelo se evalua con la prediccion de ESA regla (primera via de la regla)
    pr = L[L.regla == regla].drop_duplicates(["quipu", "cuerda"]).set_index(["quipu", "cuerda"])
    idx = pd.MultiIndex.from_frame(sub[["quipu", "cuerda"]])
    for col in ["exacta", "tol", "r5"]:
        sub[col] = pr.reindex(idx)[col].to_numpy()
    tabla.append(fila_tabla(f"regla {regla}", sub))
for flag, nom in [(False, "cuerdas NO usadas en descubrimiento"), (True, "cuerdas usadas en descubrimiento")]:
    tabla.append(fila_tabla(nom, cons[cons.descubrimiento == flag]))
T = pd.DataFrame(tabla).round(3)
T.to_csv(M.AQUI / "baselines_tabla.csv")
print(T.T.to_string())
