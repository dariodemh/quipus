"""Tarea 4. Predicciones a ciegas verificables en el objeto.
(A) Discrepancias: cuerda con valor registrado donde el modelo (oculta la cuerda, usa las demas) predice otro valor.
(B) Reconstrucciones: cuerdas sin nudos (ausentes/rotas) del sistema para las que el modelo da un valor.
Confianza = tasa de acierto exacto en el LOO de la regla y rol (loo_resultados.csv); si >=2 vias independientes coinciden
se usa la tasa observada de las cuerdas con voto >=2 (0,80). Salida: predicciones_museo.csv."""
import numpy as np
import pandas as pd
import comun19 as M

L = pd.read_csv(M.AQUI / "loo_resultados.csv")
tasa = L.groupby(["regla", "quipu"]).exacta.mean().to_dict()  # fiabilidad de la regla en ese quipu (LOO)
cons = pd.read_csv(M.AQUI / "loo_consenso.csv")
t_voto2 = cons[cons.votos >= 2].exacta.mean()
filas = []


def etiqueta(p):
    return "alta" if p >= 0.75 else "media" if p >= 0.5 else "baja"


def agrupar(t, P, real, tipo):
    """Una fila por valor predicho distinto; vias = reglas que lo apoyan."""
    por = {}
    for p in P:
        por.setdefault(p["pred"], []).append(p)
    for v, ps in por.items():
        if v <= 0 or v == real:
            continue
        indep = len({p["rule"] for p in ps})
        rol = M.rol(t)
        c = max(tasa.get((p["rule"], t[0]), 0.0) for p in ps)
        if indep >= 2:
            c = max(c, t_voto2)
        filas.append(dict(quipu=t[0], cuerda=t[1], tipo=tipo, valor_registrado=real if real else "sin nudos",
                          valor_predicho=v, via=" + ".join(sorted({p["via"] for p in ps})), reglas_independientes=indep,
                          confianza_num=round(c, 2), confianza=etiqueta(c),
                          alternativas=";".join(str(x) for x in por if x != v)))


for t in M.presentes():
    agrupar(t, M.predecir(t), M.VAL[t], "discrepancia")
for t in M.VAL:
    if M.VAL[t] is None and M.INFO[t]["pres"] is False and not M.INFO[t]["color"].startswith("PK"):
        agrupar(t, M.predecir(t, {t}), None, "reconstruccion")
D = pd.DataFrame(filas)

# colapsar filas completas de UR278: si >=5 celdas de la misma fila discrepan en la misma cantidad, es la fila entera
if len(D):
    D["delta"] = pd.to_numeric(D.valor_predicho) - pd.to_numeric(D.valor_registrado, errors="coerce")
    rows = {r["g"]: r["l0"] for r in M.REC["UR278"]}
    cell2row = {x: g for g, l0 in rows.items() for x in l0}
    D["fila278"] = [cell2row.get((q, c)) if q == "UR278" else None for q, c in zip(D.quipu, D.cuerda)]
    grp = D[(D.quipu == "UR278") & D.via.str.startswith("UR278->UR2") & D.fila278.notna()]
    colapsar = []
    for (g, d), x in grp.groupby(["fila278", "delta"]):
        if len(x) >= 5 and d != 0:
            colapsar.append((g, d, x))
    out = D.drop(index=[i for _, _, x in colapsar for i in x.index]).copy()
    nuevas = []
    for g, d, x in colapsar:
        nuevas.append(dict(quipu="UR278", cuerda=f"fila g{int(g)} (alguna de {len(rows[g])} celdas; suma registrada {int(sum(M.VAL[c] or 0 for c in rows[g]))})",
                           tipo="discrepancia de fila", valor_registrado=int(sum(M.VAL[c] or 0 for c in rows[g])),
                           valor_predicho=int(sum(M.VAL[c] or 0 for c in rows[g])) + int(d), via=x.via.iloc[0],
                           reglas_independientes=1, confianza_num=x.confianza_num.max(), confianza=x.confianza.iloc[0],
                           alternativas=f"el libro (UR266/UR275) dice +{int(d)}; una celda de la fila debe corregirse en {int(d)}"))
    D = pd.concat([out.drop(columns=["delta", "fila278"]), pd.DataFrame(nuevas)], ignore_index=True)
    D = D.sort_values(["tipo", "confianza_num"], ascending=[True, False])
# filtro anti-ruido: un error de lectura da valores cercanos; una diferencia grande (p. ej. 124 frente a 150, 1690 frente a 47)
# indica mas bien que la regla no aplica a esa cuerda. Se conservan las reconstrucciones y las discrepancias cercanas.
def cercana(r):
    if r.tipo != "discrepancia":
        return True
    v, p = float(r.valor_registrado), float(r.valor_predicho)
    return abs(p - v) / v <= 0.10 or (abs(p - v) <= 10 and p < 100)


D = D[[cercana(r) for r in D.itertuples()]]
D.to_csv(M.AQUI / "predicciones_museo.csv", index=False)
pd.set_option("display.width", 220, "display.max_colwidth", 60)
print(len(D), D.groupby(["tipo", "confianza"]).size().to_string())
print(D[D.confianza.isin(["alta", "media"])].head(60)[["quipu", "cuerda", "tipo", "valor_registrado", "valor_predicho", "via", "confianza_num"]].to_string())
