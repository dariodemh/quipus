"""T1. Urton (2019) sobre UR28: verificacion aritmetica de las tres sumas = 102.

Afirmacion (ficha 2019-Urton, p. 34): el cordel #1 suma 102; el grupo 2
(#2-#4 + subsidiarios) suma 102; las seis agrupaciones del grupo 3
(#5-#74) tambien suman 102, con un error de registro de 2 unidades.
Ademas: mitad AB / mitad MB.

Este script NO interpreta 102 como pachaca: solo comprueba la aritmetica
interna del quipu, que es lo unico falsable con cuerdas.csv.
"""
import os
import pandas as pd
from comun import cargar

c, q, _ = cargar()
d = c[c.kfg == "UR028"].sort_values("orden").copy()

print("UR028: filas totales", len(d), "| colgantes nivel 0", (d.nivel == 0).sum(),
      "| subsidiarias", (d.nivel == 1).sum())

# Grupos del KFG
res = []
for gr, g in d.groupby("grupo"):
    top = g[g.nivel == 0]
    res.append({
        "grupo": gr, "n_total": len(g), "n_colgantes": len(top),
        "suma": g.valor.sum(), "suma_colgantes": top.valor.sum(),
        "AB": g[g.color == "AB"].valor.sum(),
        "MB": g[g.color == "MB"].valor.sum(),
        "KB": g[g.color == "KB"].valor.sum(),
    })
r = pd.DataFrame(res)
print("\nSumas por grupo del KFG (incluye subsidiarias):")
print(r.to_string(index=False))

p1 = d[d.cuerda == "p1"].valor.iloc[0]
g1 = r[r.grupo == 1]
g3 = r[r.grupo.isin([2, 3, 5, 7])]
print("\n1) p1 =", p1)
print("2) grupo 1 (p2-p4 + subs) =", g1.suma.iloc[0],
      "  [AB", g1.AB.iloc[0], "+ MB", g1.MB.iloc[0], "]")
print("3) grupos 2,3,5,7 (p5-p76 + subs) =", g3.suma.sum(),
      "  [AB", g3.AB.sum(), "+ MB", g3.MB.sum(), "+ KB", g3.KB.sum(), "]")
print("   desvio respecto de 102:", g3.suma.sum() - 102,
      "(Urton reporta un error de 2 unidades)")

# Control: cuantos subconjuntos de grupos dan exactamente 102
from itertools import combinations
grupos = list(r.grupo)
hits = []
for k in range(1, len(grupos) + 1):
    for comb in combinations(grupos, k):
        if abs(r.set_index("grupo").loc[list(comb), "suma"].sum() - 102) < 1e-9:
            hits.append(comb)
print("\nCombinaciones de grupos del KFG que suman exactamente 102:", len(hits))
print(hits[:10])

print("\nColores de los 76 colgantes:")
print(d[d.nivel == 0].color.value_counts(dropna=False).to_string())

print("\nNOTA: el articulo dice 74 cordeles; el KFG registra 76 colgantes")
print("(p35 y p56 son cuerdas sin color ni nudos, valor 0 = ausente).")
