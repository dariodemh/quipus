# -*- coding: utf-8 -*-
"""Duplicados exactos y casi-duplicados (posible 'checks-and-balances') en UR262."""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)
NPERM = 1000
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0).astype(float)
n = len(q)
val = q.valor.values
nivel = q.nivel.values.astype(int)

# pares madre-hijo
pairs = [(i, j) for i in range(n) for j in q.index[q.padre == q.cuerda.iloc[i]]]
# pares de pendientes dentro del mismo grupo
pend = q[q.nivel == 0]
ppairs = [(i, j) for i in pend.index for j in pend.index
          if i < j and q.grupo.iloc[i] == q.grupo.iloc[j]]

print("pares madre-hijo:", len(pairs), "| pares de pendientes mismo grupo:", len(ppairs))

def count_near(v, pairs, tol):
    k = 0
    for i, j in pairs:
        a, b = v[i], v[j]
        if a > 0 and b > 0 and abs(a - b) <= tol * max(a, b):
            k += 1
    return k

for tol, name in [(0.0, "exactos"), (0.01, "<=1%"), (0.05, "<=5%")]:
    obs_mh = count_near(val, pairs, tol)
    obs_pp = count_near(val, ppairs, tol)
    nmh, npp = [], []
    for _ in range(NPERM):
        vv = RNG.permutation(val)
        nmh.append(count_near(vv, pairs, tol))
        npp.append(count_near(vv, ppairs, tol))
    nmh, npp = np.array(nmh), np.array(npp)
    print(f"\n{name}: madre-hijo obs={obs_mh} nulo={nmh.mean():.2f} p={(1+(nmh>=obs_mh).sum())/(1+NPERM):.4f}"
          f" | pendientes obs={obs_pp} nulo={npp.mean():.2f} p={(1+(npp>=obs_pp).sum())/(1+NPERM):.4f}")

# listar los casi-duplicados madre-hijo <=1%
print("\ncasos madre-hijo <=1%:")
for i, j in pairs:
    a, b = val[i], val[j]
    if a > 0 and b > 0 and abs(a - b) <= 0.01 * max(a, b):
        print(f"  {q.cuerda.iloc[i]}={a:.0f} -> {q.cuerda.iloc[j]}={b:.0f}  (G{int(q.grupo.iloc[i])})")
