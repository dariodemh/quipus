# -*- coding: utf-8 -*-
"""ATAQUE 3b: controles finales del reparto W-R.
 - W>R en UR053 vs otros quipus (Fisher) y nulo barajando color dentro del quipu.
 - share1 por quipu en otros quipus con pares W-R: percentil de UR053.
 - comparacion del reparto UR053 con trios contiguos genericos.
"""
import re
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

rng = np.random.default_rng(20261018)
RAIZ = r"."
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
c["col"] = c.color.astype(str).map(lambda s: "R" if re.sub(r"\([^)]*\)", "", s).startswith("R")
                                   else re.sub(r"\([^)]*\)", "", s))
c["val"] = pd.to_numeric(c.valor, errors="coerce")
p = c[(c.nivel == 0) & c.val.notna()].sort_values(["kfg", "orden"])

pares = []
for k, g in p.groupby("kfg"):
    L = list(zip(g.col, g.val))
    for i in range(len(L) - 1):
        if L[i][0] == "W" and L[i + 1][0] == "R":
            pares.append((k, L[i][1], L[i + 1][1]))
D = pd.DataFrame(pares, columns=["kfg", "w", "r"])
D["ur"] = D.kfg.str.startswith("UR053")
a = int(((D[D.ur].w > D[D.ur].r)).sum()); n1 = int(D.ur.sum())
b = int(((D[~D.ur].w > D[~D.ur].r)).sum()); n2 = int((~D.ur).sum())
print(f"W>R: UR053 {a}/{n1} ({a/n1:.3f}) vs otros {b}/{n2} ({b/n2:.3f})")
print("Fisher bilateral p=%.2e" % fisher_exact([[a, n1 - a], [b, n2 - b]])[1])

# nulo: barajar color dentro de cada quipu UR053 (conserva valores)
ur = p[p.kfg.str.startswith("UR053")]
obs = a / n1
cnt = 0
NS = 5000
for _ in range(NS):
    aa = nn = 0
    for k, g in ur.groupby("kfg"):
        col = rng.permutation(g.col.values)
        v = g.val.values
        for i in range(len(v) - 1):
            if col[i] == "W" and col[i + 1] == "R":
                nn += 1
                aa += v[i] > v[i + 1]
    if nn and aa / nn >= obs:
        cnt += 1
print(f"nulo barajando color dentro de UR053: p={(cnt+1)/(NS+1):.4f}")

# share1 por quipu con pares W-R
sh = []
for k, g in D.groupby("kfg"):
    if str(k).startswith("UR053"):
        continue
    sh.append((k, np.mean(g.w / (g.w + g.r))))
sh = pd.DataFrame(sh, columns=["kfg", "s1"])
ur_s1 = np.mean(D[D.ur].w / (D[D.ur].w + D[D.ur].r))
print(f"share1 W-R por quipu: otros n={len(sh)} mediana={sh.s1.median():.3f} "
      f"P90={sh.s1.quantile(.9):.3f} max={sh.s1.max():.3f} | UR053={ur_s1:.3f} "
      f"percentil={100*np.mean(sh.s1<ur_s1):.1f}")

# cuantos quipus fuera de UR053 tienen >=3 pares W-R
print("quipus otros con >=3 pares W-R:", int((D[~D.ur].groupby('kfg').size() >= 3).sum()))
