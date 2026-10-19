# -*- coding: utf-8 -*-
"""Conklin: la cuerda superior (union T) suma el grupo anterior.
Dos nulos: (a) suma de un grupo al azar del mismo quipu; (b) una cuerda suelta."""
import numpy as np
import pandas as pd
import prep

rng = np.random.default_rng(20261018)
d, q = prep.load()
d0 = d[d.nivel == 0].copy()
d0["grupo"] = pd.to_numeric(d0["grupo"], errors="coerce")
d0["valor_n"] = pd.to_numeric(d0["valor_n"], errors="coerce")

obs = []
cand_grupo = {}
cand_cuerda = {}
for k, x in d0.groupby("kfg"):
    gs = {g: y.valor_n.sum() for g, y in x.groupby("grupo")}
    vals = x.valor_n.values
    for g, y in x.groupby("grupo"):
        t = y[y.union == "T"]
        if len(t) != 1 or (g - 1) not in gs:
            continue
        tv = float(t.valor_n.iloc[0])
        obs.append((k, g, tv, gs[g - 1]))
        cand_grupo[(k, g)] = [v for gg, v in gs.items() if gg != g - 1]
        cand_cuerda[(k, g)] = vals

obs_rate = np.mean([np.isclose(t, p) for _, _, t, p in obs])
print(f"cuerdas T con grupo previo: {len(obs)}; igualdades exactas: "
      f"{sum(np.isclose(t, p) for _, _, t, p in obs)} ({obs_rate:.3f})")

for nombre, cand in [("suma de grupo", cand_grupo), ("cuerda suelta", cand_cuerda)]:
    null = np.empty(5000)
    for i in range(5000):
        c = 0
        for k, g, tv, prev in obs:
            c += bool(np.isclose(tv, rng.choice(cand[(k, g)])))
        null[i] = c / len(obs)
    p = (1 + (null >= obs_rate).sum()) / 5001
    print(f"nulo ({nombre}): {null.mean():.3f} (DE {null.std():.3f}); p={p:.5f}")
