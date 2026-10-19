# -*- coding: utf-8 -*-
"""UR006: tests de aritmetica con nulo de permutacion (barajar valores, 1000 it, semilla 0)."""
import pandas as pd, numpy as np, os
BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "k_UR006")
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, "cuerdas_ur006.csv"))
u["nudos"] = u["nudos"].fillna("")
G = u.grupo_g.values.astype(int)
NIV = u.nivel.values.astype(int)
PAD = u.padre.fillna("").values
CUE = u.cuerda.values
VAL = u.valor.values.astype(float)
NGRP = G.max() + 1

# precompute para cada grupo: idx pendientes y subsidiarias
pend_idx = {g: np.where((G == g) & (NIV == 0))[0] for g in range(NGRP)}
sub_idx = {g: np.where((G == g) & (NIV > 0))[0] for g in range(NGRP)}
# hijos directos por padre
hijos = {}
for i in np.where(NIV > 0)[0]:
    hijos.setdefault(PAD[i], []).append(i)
padres = [k for k in hijos if (u.cuerda == k).any()]
pad_val = {k: VAL[u.cuerda == k][0] for k in padres}

def run(v):
    t1 = sum(1 for k in padres if abs(pad_val[k] - sum(v[i] for i in hijos[k])) < 1e-6)
    t2 = 0
    for g in range(NGRP):
        idx = np.where((G == g))[0]
        if len(idx) >= 3:
            vv = v[idx]
            if np.any(np.abs(vv - (vv.sum() - vv)) < 1e-6):
                t2 += 1
    t3 = 0  # marcadores: ultima subsidiaria = suma de las anteriores menos las 2 grandes
    for g in range(NGRP):
        si = sub_idx[g]
        if len(pend_idx[g]) == 1 and len(si) >= 4:
            vv = v[si]
            if abs(vv[-1] - vv[:-2].sum()) < 1e-6:
                t3 += 1
    t4 = 0  # tripla final grande (suma>=50) en marcadores
    for g in range(NGRP):
        si = sub_idx[g]
        if len(pend_idx[g]) == 1 and len(si) >= 3 and v[si][-3:].sum() >= 50:
            t4 += 1
    return np.array([t1, t2, t3, t4])

obs = run(VAL)
N = 1000
null = np.zeros((N, 4))
for i in range(N):
    null[i] = run(rng.permutation(VAL))
names = ["T1 padre=sum(hijos)", "T2 grupo: cord=sum(resto)", "T3 marcador: ult=sum(ant-2)", "T4 tripla final>=50"]
for j, nm in enumerate(names):
    p = (1 + (null[:, j] >= obs[j]).sum()) / (N + 1)
    print(f"{nm}: obs={obs[j]:.0f}  media_nulo={null[:,j].mean():.2f}  sd={null[:,j].std():.2f}  p={p:.4f}")
