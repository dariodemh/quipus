# -*- coding: utf-8 -*-
"""UR113: autocorrelacion de color (franjas cortas) frente a nulo intra-grupo."""
import pandas as pd, numpy as np, os
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv')); u['valor'] = u.valor.fillna(0)
p = u[u.nivel == 0].copy()
p['color'] = p.color.fillna('NA')

def lagstat(df, lag):
    s = n = 0
    for _, g in df.groupby('grupo'):
        c = g.color.values
        if len(c) <= lag: continue
        s += int((c[lag:] == c[:-lag]).sum()); n += len(c) - lag
    return s, n

for lag in [1, 2, 3, 4]:
    s, n = lagstat(p, lag)
    null = []
    for _ in range(300):
        d = p.copy()
        d['color'] = d.groupby('grupo').color.transform(lambda x: rng.permutation(x.values))
        null.append(lagstat(d, lag)[0])
    null = np.array(null)
    print(f'lag {lag}: obs {s}/{n} = {s/n:.2f} | nulo {null.mean():.1f} ({null.mean()/n:.2f}) '
          f'| p = {(np.sum(null >= s) + 1) / 301:.3f}')
