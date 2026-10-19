# -*- coding: utf-8 -*-
"""Cuanta capacidad combinatoria tienen de hecho los 4 rasgos binarios dentro
de cada quipu, frente a independencia (permutando cada rasgo por separado)."""
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng = np.random.default_rng(SEED)
d, q = prep.load()
d0 = d[d.nivel == 0].copy()
d0["uniV"] = (d0.union2 == "V").astype(float).where(d0.union2.notna())
d0["torZ"] = (d0.torsion2 == "Z").astype(float).where(d0.torsion2.notna())
d0["kdS"] = (d0.kdir == "S").astype(float).where(d0.kdir.isin(["S", "Z"]))
d0["crom"] = d0.cromatico

qs = []
cols = ["uniV", "torZ", "kdS", "crom"]
for k, x in d0.groupby("kfg"):
    y = x.dropna(subset=cols)
    if len(y) < 8:
        continue
    M = y[cols].values.astype(int)
    obs = len(set(map(tuple, M)))
    qs.append((k, M, obs))
print("quipus:", len(qs), "| mediana combinaciones observadas:",
      np.median([o for _, _, o in qs]))


def mean_combos(shuffle=False):
    tot = 0
    for k, M, obs in qs:
        if shuffle:
            Z = np.column_stack([rng.permutation(M[:, j]) for j in range(4)])
            tot += len(set(map(tuple, Z)))
        else:
            tot += obs
    return tot / len(qs)


obs = mean_combos()
null = np.array([mean_combos(True) for _ in range(500)])
p = (1 + (null >= obs).sum()) / 501
print(f"media observada={obs:.3f} | nulo independiente={null.mean():.3f} (DE {null.std():.3f}) p={p:.4f}")
print("Si obs << nulo: los rasgos son redundantes (no exploran combinaciones).")
print("Si obs ~ nulo: se combinan como bits independientes.")
