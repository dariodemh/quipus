# -*- coding: utf-8 -*-
"""CM009: escaneo de periodos con nulo que preserva color + corrección de Holm."""
import pandas as pd, numpy as np
from scipy import stats

q = pd.read_csv("analisis/ds/k_CM009/cm009_cuerdas.csv").sort_values("cord_id").reset_index(drop=True)
v = q.numeric_value.to_numpy(int); col = q.color.to_numpy(); n = len(v)
rng = np.random.default_rng(0)
NDRAW = 1000

def best_off():
    """Mejor desfase d de repetición de 20 entre cuerdas 1..60 (3 bloques)."""
    a = v[:20]
    res = {}
    for d in range(0, 20):
        seg = v[d:d+20]
        if len(seg) == 20:
            res[d] = int(np.sum(a == seg))
    return res
print("acuerdos v[1..20] vs v[d+1..d+20]:", best_off())

periods = [4, 8, 12, 16, 20, 24, 40]
obs, pvals = [], []
for L in periods:
    idx = np.arange(n - L)
    o = float(np.mean(v[idx] == v[idx + L]))
    null = []
    for _ in range(NDRAW):
        s = v.copy()
        for c in np.unique(col):
            m = np.where(col == c)[0]; s[m] = rng.permutation(s[m])
        null.append(float(np.mean(s[idx] == s[idx + L])))
    p = (1 + np.sum(np.asarray(null) >= o)) / (1 + NDRAW)
    obs.append(o); pvals.append(p)
    print(f"L={L:3d} obs={o:.3f} p={p:.4f}")

# Holm
order = np.argsort(pvals)
m = len(pvals); adj = [None]*m; prev = 0
for rank, i in enumerate(order):
    val = min(1.0, (m - rank) * pvals[i])
    prev = max(prev, val); adj[i] = prev
print("\nHolm:")
for L, o, p, a in zip(periods, obs, pvals, adj):
    print(f"  L={L:3d} obs={o:.3f} p={p:.4f} p_holm={a:.4f} {'*' if a < 0.05 else ''}")
