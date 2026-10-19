"""Cuantos pares entre quipus hay que alinear y cuanto tarda el LCS."""
import time
import numpy as np
import pandas as pd
from itertools import combinations
from motor import cargar

c, q = cargar()
l0 = c[c.nivel == 0]
seq = {k: (d.orden.to_numpy(), d.vi.to_numpy()) for k, d in l0.groupby("kfg")}
proc = q.set_index("kfg").procedencia.fillna("Unknown").to_dict()
byp = {}
for k in seq:
    byp.setdefault(proc.get(k, "Unknown"), []).append(k)
pares = []
for p, L in byp.items():
    if p == "Unknown":
        continue
    for a, b in combinations(sorted(L), 2):
        na, nb = len(seq[a][0]), len(seq[b][0])
        if na < 8 or nb < 8:
            continue
        if not (0.5 <= na / nb <= 2.5):
            continue
        pares.append((a, b))
print("pares candidatos (misma procedencia, >=8 colgantes, ratio 0.5-2.5):", len(pares))
print("procedencias con pares:", len({proc[a] for a, b in pares}))
print("top procedencias:", pd.Series([proc[a] for a, b in pares]).value_counts().head(8).to_dict())

# coste de un LCS puro en python
def lcs(X, Y, tol=frozenset({0, 1})):
    n, m = len(X), len(Y)
    H = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        xi, Hi, Hn = X[i], H[i], H[i + 1]
        for j in range(m):
            yj = Y[j]
            if xi is not None and yj is not None and abs(xi - yj) in tol:
                Hn[j + 1] = Hi[j] + 1
            else:
                a, bb = Hn[j], Hi[j + 1]
                Hn[j + 1] = a if a > bb else bb
    return H[n][m]

t0 = time.time()
tot = 0
for a, b in pares[:300]:
    tot += lcs(list(seq[a][1]), list(seq[b][1]))
dt = time.time() - t0
print("300 LCS en %.2f s -> estimacion total %.0f s" % (dt, dt / 300 * len(pares)))
