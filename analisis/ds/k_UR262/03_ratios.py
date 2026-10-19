# -*- coding: utf-8 -*-
"""Relaciones pendant <-> hijos: igualdad, suma, razon. Inspeccion de cordones grandes."""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0)

p = q[(q.nivel == 0) & (q.n_hijos > 0)].copy()
p["ratio"] = np.where(p.suma_hijos > 0, p.valor / p.suma_hijos, np.nan)

print("== pendientes con hijos: valor vs suma de hijos ==")
print("n =", len(p))
print("iguales:", int((p.valor == p.suma_hijos).sum()),
      "| ratio mediano %.2f" % p.ratio.median())
print("\nhistograma de ratio v/(suma hijos) en bins:")
bins = [0, .05, .1, .2, .3, .5, .7, 1.01, 1.5, 2, 3, 5, 6, 7, 8, 10, 100]
print(pd.cut(p.ratio, bins=bins).value_counts().sort_index().to_string())

print("\n== pendientes ordenados por ratio (los 20 con suma_hijos>0 y ratio 5-10) ==")
sel = p[(p.ratio > 5) & (p.ratio < 10)].sort_values("ratio")
print(sel[["cuerda", "grupo", "valor", "n_hijos", "suma_hijos", "ratio", "color"]].head(20).to_string(index=False))

print("\n== igualdad exacta por numero de hijos ==")
print(p.groupby("n_hijos").apply(lambda d: pd.Series(
    {"n": len(d), "iguales": int((d.valor == d.suma_hijos).sum())})).to_string())

print("\n== cordones con valor >= 1000 ==")
big = q[q.valor >= 1000].sort_values("valor", ascending=False)
print(big[["cuerda", "nivel", "padre", "valor", "color", "n_hijos", "suma_hijos"]].head(30).to_string(index=False))
print("total cordones >=1000:", len(big), "| de ellos nivel 0:", int((big.nivel == 0).sum()))

print("\n== color vs magnitud ==")
q["grande"] = q.valor >= 1000
ct = pd.crosstab(q.color, q.grande)
ct["n"] = ct.sum(axis=1)
ct["pct_grande"] = (100 * ct.get(True, 0) / ct.n).round(1)
print(ct.sort_values("n", ascending=False).head(12).to_string())
