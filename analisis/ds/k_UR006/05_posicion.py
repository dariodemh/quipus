# -*- coding: utf-8 -*-
"""UR006: gradiente de valores por posicion dentro de los 24 grupos grandes + nulo."""
import pandas as pd, numpy as np, os
from scipy.stats import spearmanr
BASE = r"."; OUT = os.path.join(BASE, "analisis", "ds", "k_UR006")
u = pd.read_csv(os.path.join(OUT, "cuerdas_ur006.csv"))
big = sorted(u[u.nivel == 0].groupby("grupo_g").size().pipe(lambda s: s[s >= 20]).index.tolist())
mats = []
for g in big:
    mats.append(u[(u.grupo_g == g) & (u.nivel == 0)].sort_values("orden").valor.astype(float).values)

def stat(mats):
    rs = []
    for m in mats:
        if len(m) > 2 and np.std(m) > 0:
            rs.append(spearmanr(np.arange(len(m)), m).statistic)
    return np.mean(rs)

obs = stat(mats)
rng = np.random.default_rng(0); N = 1000; null = np.zeros(N)
for i in range(N):
    null[i] = stat([rng.permutation(m) for m in mats])
p = (1 + (null >= obs).sum()) / (N + 1)
print(f"Spearman posicion~valor (media en 24 grupos): obs={obs:.3f} nulo={null.mean():.3f} sd={null.std():.3f} p={p:.4f}")

# fraccion de ceros en primera mitad vs segunda
first = np.concatenate([m[:len(m)//2] for m in mats])
second = np.concatenate([m[len(m)//2:] for m in mats])
print(f"%cero 1a mitad={100*(first==0).mean():.1f}  %cero 2a mitad={100*(second==0).mean():.1f}")
# posicion 12 siempre >0?
c12 = [m[11] for m in mats if len(m) > 11]
print("pos12 valores:", c12, " ceros:", sum(v == 0 for v in c12))
