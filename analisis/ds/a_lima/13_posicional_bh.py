# -*- coding: utf-8 -*-
"""Correccion multiple BH sobre coincidencias posicionales por par (todas las 1891
parejas) y sobre bigramas. Nulo: barajar dentro de cada quipu, 500 iter, semilla 0."""
import pandas as pd, numpy as np, itertools
from scipy.stats import false_discovery_control as fdr
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]
V = {}
for k in solo:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V[k] = list(d["valor"].fillna(0).astype(int))
pairs = list(itertools.combinations(solo, 2))

def pe(a, b):
    n = min(len(a), len(b))
    return sum(1 for i in range(n) if a[i] == b[i] and a[i] > 0)
obs = {(a, b): pe(V[a], V[b]) for a, b in pairs}
ge = {kk: 0 for kk in obs}
perm = {k: list(V[k]) for k in solo}
for it in range(NC):
    for k in solo:
        rng.shuffle(perm[k])
    for a, b in pairs:
        if pe(perm[a], perm[b]) >= obs[(a, b)]:
            ge[(a, b)] += 1
p = np.array([(ge[kk] + 1) / (NC + 1) for kk in obs])
q = fdr(p, method="bh")
print("Coincidencias posicionales (nivel0): pares con q<0.05 =", (q < 0.05).sum(), "/", len(pairs))
print("min p =", round(p.min(), 5), " min q =", round(q.min(), 4))
order = np.argsort(p)[:6]
keys = list(obs)
for i in order:
    a, b = keys[i]
    print(f"  {a:8s} x {b:8s} obs={obs[(a,b)]:2d} p={p[i]:.4f} q={q[i]:.3f}")
print("\nUR066 x UR067: obs=", obs[("UR066", "UR067")], "p=", round(p[keys.index(("UR066","UR067"))], 4),
      "q=", round(q[keys.index(("UR066","UR067"))], 3))
