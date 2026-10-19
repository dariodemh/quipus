"""Tarea 1 (síntesis). Grafo a nivel de CUERDA del archivo de Incahuasi.

Reúne en una sola tabla de aristas (origen -> destino) las relaciones que superaron sus nulos en 01-04 (y en
04_concordancias / 09_incahuasi), más la aritmética interna de cada registro:
  copia        valor idéntico (o ±1 dígito) alineado en orden entre quipus emparejados (LCS con retroceso, valores >=30)
  total_grupo  total de un grupo de UR278 -> cuerda de UR266/UR275/UR269 (LCS en orden con tolerancia)
  suma_AB      cabecera del registro i del componente A + la del componente B -> cuerda del libro consolidado
               (solo diferencias 0 o 1; las ±1 dígito en decenas/centenas son demasiado laxas para sumas)
  parte_P/S    total de colgantes (P) o de primeras subsidiarias (S) de un grupo de UR270 -> cabecera de UR273B (P)
               y de UR273A (S), solo cuando coinciden en la misma fila (prueba conjunta de 04); suma_PS: P+S -> libro
  cuota / neto dentro de un registro con cuota c: cabecera x -> cuerda c, y x -> cuerda n con n = x - c (- deducciones)
Solo se listan aristas; su significación está en las salidas de 01-04. Salidas: grafo_cuerdas.csv,
grafo_quipus.csv (aristas agregadas por par de quipus y tipo) y libro_consolidado.csv (una fila por cabecera >=100 de
UR275/UR266/UR269 con sus fuentes).
"""
import numpy as np
import pandas as pd
import comun13 as C

TOL = C.TOL
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
P = c[c.pres]
CUOTA = {"UR255": 15, "UR267A": 15, "UR256": 10, "UR267B": 10, "UR266": 47, "UR275": 47, "UR274A": 30,
         "UR274B": 17, "UR273B": 17, "UR268": 208, "UR269": None}
aristas = []


def lcs_back(x, y):
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), int)
    for i in range(n):
        for j in range(m):
            H[i + 1, j + 1] = H[i, j] + 1 if abs(int(x[i]) - int(y[j])) in TOL else max(H[i, j + 1], H[i + 1, j])
    i, j, out = n, m, []
    while i and j:
        if abs(int(x[i - 1]) - int(y[j - 1])) in TOL and H[i, j] == H[i - 1, j - 1] + 1:
            out.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif H[i - 1, j] >= H[i, j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def add(qa, ca, va, qb, cb, vb, tipo, nota="", exacto=None):
    aristas.append(dict(origen=qa, cuerda_o=ca, valor_o=int(va), destino=qb, cuerda_d=cb, valor_d=int(vb), tipo=tipo,
                        exacto=(int(va) == int(vb)) if exacto is None else exacto, nota=nota))


# 1. copias
for a, b in [("UR255", "UR267A"), ("UR256", "UR267B"), ("UR266", "UR275"), ("UR273A", "UR274A"),
             ("UR273B", "UR274B"), ("UR269", "UR275"), ("UR269", "UR266")]:
    sa, sb = P[(P.kfg == a) & (P.valor >= 30)], P[(P.kfg == b) & (P.valor >= 30)]
    for i, j in lcs_back(sa.valor.to_numpy(), sb.valor.to_numpy()):
        ra, rb = sa.iloc[i], sb.iloc[j]
        add(a, ra.cuerda, ra.valor, b, rb.cuerda, rb.valor, "copia")

# 2. totales de grupo de UR278
g278 = P[(P.kfg == "UR278") & (P.nivel == 0)].groupby("grupo").agg(v=("valor", "sum"), n=("valor", "size"))
g278 = g278[(g278.n >= 2) & (g278.v >= 100)]
for b in ["UR266", "UR275", "UR269"]:
    sb = P[(P.kfg == b) & (P.valor >= 100)]
    for i, j in lcs_back(g278.v.to_numpy(), sb.valor.to_numpy()):
        add("UR278", f"g{g278.index[i]}(suma de {g278.n.iloc[i]})", g278.v.iloc[i], b, sb.iloc[j].cuerda,
            sb.iloc[j].valor, "total_grupo")


# 3. sumas de componentes A+B, registro a registro (registro = grupo que no es separador rosa)
def registros(k):
    s = c[c.kfg == k]
    out = []
    for g, x in s.groupby("grupo"):
        x0 = x[x.nivel == 0]
        if x0.color.str.startswith("PK").all() and not x0.pres.any():
            continue
        p0 = x0[x0.pres]
        out.append((g, p0.cuerda.iloc[0] if len(p0) else None, int(p0.valor.iloc[0]) if len(p0) else None))
    return out


consol = P[P.kfg.isin(["UR266", "UR275", "UR269"]) & (P.valor >= 100)]
for qa, qb, cc in [("UR267A", "UR267B", 25), ("UR273A", "UR273B", 47), ("UR274A", "UR273B", 47)]:
    for (ga, ca, xa), (gb, cb, xb) in zip(registros(qa), registros(qb)):
        if xa is None or xb is None:
            continue
        for r in consol[consol.valor.sub(xa + xb).abs() <= 1].itertuples():  # sumas: solo exacto o ±1
            nota = f"{qa}:{ca}={xa} + {qb}:{cb}={xb} = {xa + xb}; cuota esperada {cc}"
            add(qa, ca, xa, r.kfg, r.cuerda, r.valor, "suma_AB(parte A)", nota, r.valor == xa + xb)
            add(qb, cb, xb, r.kfg, r.cuerda, r.valor, "suma_AB(parte B)", nota, r.valor == xa + xb)

# 4. UR270: P y S por grupo -> misma fila de UR273B / UR273A
s = c[(c.kfg == "UR270") & c.pres].copy()
s["sub"] = s.cuerda.str.extract(r"^p\d+(s\d+)$")[0]
A3 = {g: (cu, x) for g, cu, x in registros("UR273A") if x}
B3 = {g: (cu, x) for g, cu, x in registros("UR273B") if x}
for g, x in s.groupby("grupo"):
    Pg = x[x.nivel == 0].valor.sum()
    Sg = x[x["sub"] == "s1"].valor.sum()
    for k in set(A3) & set(B3):
        if B3[k][1] == Pg and abs(A3[k][1] - Sg) in TOL:
            add("UR270", f"g{g}:colgantes", Pg, "UR273B", B3[k][0], B3[k][1], "parte_P")
            add("UR270", f"g{g}:subsid_s1", Sg, "UR273A", A3[k][0], A3[k][1], "parte_S")
            for r in consol[consol.valor.sub(Pg + Sg).abs() <= 1].itertuples():
                add("UR270", f"g{g}:colgantes+subsid", Pg + Sg, r.kfg, r.cuerda, r.valor, "suma_PS")

# 5. cuota y neto dentro de cada registro
for k, cc in CUOTA.items():
    s = P[P.kfg == k]
    for g, x in s.groupby("grupo"):
        x0 = x[x.nivel == 0]
        if not len(x0) or x0.valor.iloc[0] < 100:
            continue
        cab = x0.iloc[0]
        rest = x.drop(cab.name)
        for cu in ([cc] if cc else [20, 25, 40, 44, 46, 47]):
            hit_c = rest[rest.valor == cu]
            hit_n = rest[rest.valor == cab.valor - cu]
            if len(hit_c):
                add(k, cab.cuerda, cab.valor, k, hit_c.iloc[0].cuerda, cu, "cuota")
            if len(hit_n):
                add(k, cab.cuerda, cab.valor, k, hit_n.iloc[0].cuerda, hit_n.iloc[0].valor, "neto", f"x - {cu}")
            elif len(hit_c) and len(rest) >= 3:
                otros = rest.drop(hit_c.index[0])
                if abs(int(cab.valor) - cu - int(otros.valor.sum())) in TOL:
                    add(k, cab.cuerda, cab.valor, k, otros.iloc[-1].cuerda, otros.iloc[-1].valor, "neto",
                        f"x = {cu} + " + " + ".join(map(str, otros.valor.tolist())))

E = pd.DataFrame(aristas).drop_duplicates()
E.to_csv(C.AQUI / "grafo_cuerdas.csv", index=False)
G = (E[E.origen != E.destino].groupby(["origen", "destino", "tipo"])
     .agg(aristas=("exacto", "size"), exactas=("exacto", "sum")).reset_index())
G.to_csv(C.AQUI / "grafo_quipus.csv", index=False)
I = E[E.origen == E.destino].groupby(["origen", "tipo"]).agg(aristas=("exacto", "size")).reset_index()
pd.set_option("display.width", 200)
print(f"aristas a nivel de cuerda: {len(E)} (entre quipus: {(E.origen != E.destino).sum()}; "
      f"internas: {(E.origen == E.destino).sum()})")
print(G.to_string(index=False))
print(I.to_string(index=False))

L = []
for k in ["UR275", "UR266", "UR269"]:
    for g, x in P[(P.kfg == k) & (P.nivel == 0)].groupby("grupo"):
        if x.valor.iloc[0] < 100:
            continue
        cab = x.iloc[0]
        ent = E[(E.destino == k) & (E.cuerda_d == cab.cuerda) & (E.origen != k)]
        fuentes = "; ".join(sorted({f"{r.origen}:{r.cuerda_o}={r.valor_o}({r.tipo})" for r in ent.itertuples()}))
        todo = c[(c.kfg == k) & (c.grupo == g)]
        L.append(dict(quipu=k, grupo=g, cabecera=cab.valor, color=cab.color,
                      cuerdas=" ".join(str(v) if p else "·" for v, p in zip(todo.valor, todo.pres)), fuentes=fuentes))
pd.DataFrame(L).to_csv(C.AQUI / "libro_consolidado.csv", index=False)
