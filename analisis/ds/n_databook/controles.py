#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Control nulo: permutacion de cuerdas KFG dentro de cada quipu.
Compara la concordancia observada (valor, color, largo) con la esperable
si el emparejamiento dentro del quipu fuese aleatorio. Semilla fija."""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)
rng = np.random.default_rng(42)

r = pd.read_csv(D('databook_vs_kfg.csv'))
r = r[(r.nivel_db == r.nivel_kfg) & (r.score >= 3)].copy()
r['color_eq'] = (r.color_db_n.fillna('') == r.color_kfg_n.fillna('')).astype(float)
r['largo_eq'] = ((r.largo_db - r.largo_kfg).abs() <= 0.5).astype(float)
r['valor_eq'] = (r.valor_db == r.valor_kfg).astype(float)
r = r[r.valor_db.notna() & r.valor_kfg.notna()].copy()

def match(col, db, kf):
    if col == 'valor':
        return (db == kf).astype(float)
    if col == 'color':
        return (pd.Series(db).fillna('').values == pd.Series(kf).fillna('').values).astype(float)
    return (np.abs(np.asarray(db, float) - np.asarray(kf, float)) <= 0.5).astype(float)

def obs(col, dbc, kfc):
    a = match(col, r[dbc], r[kfc])
    return float(a.mean())

def perm_test(col, dbc, kfc, nperm=1000):
    obs_val = obs(col, dbc, kfc)
    null = np.empty(nperm)
    groups = [g for _, g in r.groupby('quipu')]
    for k in range(nperm):
        vals = []
        for g in groups:
            v = g[kfc].to_numpy().copy()
            rng.shuffle(v)
            vals.append(match(col, g[dbc].values, v))
        null[k] = np.concatenate(vals).mean()
    p = (1 + np.sum(null >= obs_val)) / (nperm + 1)
    return obs_val, null.mean(), np.quantile(null, .975), p

out = []
for name, dbc, kfc in [('valor', 'valor_db', 'valor_kfg'),
                       ('color', 'color_db_n', 'color_kfg_n'),
                       ('largo', 'largo_db', 'largo_kfg')]:
    o, m, q, p = perm_test(name, dbc, kfc)
    out.append(dict(prueba=name, observado=round(o, 4), nulo_medio=round(m, 4),
                    nulo_p975=round(q, 4), p_empirico=p))
res = pd.DataFrame(out)
# Holm
res = res.sort_values('p_empirico').reset_index(drop=True)
m = len(res)
res['p_holm'] = [min(1, (m - i) * p) for i, p in enumerate(res.p_empirico)]
for i in range(1, len(res)):
    res.loc[i, 'p_holm'] = max(res.loc[i, 'p_holm'], res.loc[i-1, 'p_holm'])
res.to_csv(D('controles_nulos.csv'), index=False)
print(res.to_string(index=False))
print('\npares', len(r), 'quipus', r.quipu.nunique())
