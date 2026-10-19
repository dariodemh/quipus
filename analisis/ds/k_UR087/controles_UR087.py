#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controles de UR087: firma estructural de runs de 6, cuerdas superiores/marcadores,
atachment recto/verso en los seis del Santa, y control de tamano de las relaciones de suma.
Semilla 0. Salidas compactas."""
import sqlite3
import numpy as np
import pandas as pd

C = pd.read_csv('analisis/datos/cuerdas.csv')
C['valor'] = pd.to_numeric(C.valor, errors='coerce').fillna(0)
P = C[C.nivel == 0]

def color_runs(g):
    g = g.sort_values('orden')
    cols = g.color.map(lambda x: str(x).split('/')[0].split(':')[0].split('(')[0]).values
    N = len(cols); runs = []; cur = None; s = 0
    for i in range(N):
        if cols[i] != cur:
            if cur is not None: runs.append(i - s)
            cur = cols[i]; s = i
    runs.append(N - s)
    return runs

# ---- firma estructural: fraccion de colgantes en runs de exactamente 6 ----
rows = []
for k, g in P.groupby('kfg'):
    runs = color_runs(g)
    n6 = sum(r for r in runs if r == 6)
    rows.append((k, len(g), n6, n6 / len(g)))
S = pd.DataFrame(rows, columns=['kfg', 'pend', 'n6', 'frac6'])
u = S[S.kfg == 'UR087'].iloc[0]
big = S[S.pend >= 100]
print('== FIRMA "RUNS DE 6" ==')
print(f"UR087: pend={u.pend:.0f} n6={u.n6:.0f} frac6={u.frac6:.3f}")
print(f"percentil corpus={100*(S.frac6<=u.frac6).mean():.1f}%  "
      f"percentil grandes(>=100)={100*(big.frac6<=u.frac6).mean():.1f}%  "
      f"p(>=) en grandes={(big.n6>=u.n6).mean():.3f} (n={len(big)})")
print('top8 por frac6:', S.sort_values('frac6', ascending=False).head(8)[
    ['kfg', 'pend', 'n6', 'frac6']].to_dict('records'))

# ---- seis del Santa en OKR: top cords, marcadores, attach ----
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
ids = {'KH0323': 'UR087', 'KH0324': 'UR088', 'KH0325': 'UR089',
       'KH0326': 'UR090', 'KH0327': 'UR091', 'KH0328': 'UR092'}
m = pd.read_sql('select KHIPU_ID,OKR_NUM from khipu_main', con)
sub = m[m.OKR_NUM.isin(ids)]
co = pd.read_sql('select KHIPU_ID,CORD_CLASSIFICATION,ATTACHMENT_TYPE,CORD_LEVEL from cord '
                 'where KHIPU_ID in (%s)' % ','.join(map(str, sub.KHIPU_ID)), con)
print('\n== LOS SEIS DEL SANTA (OKR) ==')
for _, r in sub.iterrows():
    cc = co[co.KHIPU_ID == r.KHIPU_ID]
    print(f"  {ids[r.OKR_NUM]:6s} colgantes={(cc.CORD_LEVEL==1).sum():3d} "
          f"T={(cc.CORD_CLASSIFICATION=='T').sum()} M={(cc.CORD_CLASSIFICATION=='M').sum()} "
          f"attach={cc.ATTACHMENT_TYPE.value_counts().to_dict()}")

# ---- control de tamano de las relaciones de suma (regresion count~pend) ----
from scipy import stats
sz = P.groupby('kfg').size().rename('pend')
base = 'data/external/data-science-khipu-article/data/ascher_sum_relations/'
print('\n== RELACIONES DE SUMA vs TAMANO (z de residuo, p de dos colas) ==')
ps = {}
for f, col in [('pendant_pendant_sum.csv', 'num_sum_cords'),
               ('pendant_pendants_color_sum.csv', 'num_sum_cords'),
               ('indexed_pendant_sum.csv', 'num_sum_cords'),
               ('cluster_cluster_sum.csv', 'num_sum_clusters'),
               ('sum_top_cords.csv', 'num_sum_top_cords')]:
    df = pd.read_csv(base + f).set_index('name').join(sz).dropna(subset=['pend'])
    A = np.c_[np.ones(len(df)), df.pend.values]
    b, *_ = np.linalg.lstsq(A, df[col].values, rcond=None)
    res = df[col].values - A @ b
    up = df.loc['UR087', 'pend']; uv = df.loc['UR087', col]
    z = (uv - (b[0] + b[1] * up)) / (res.std() + 1e-9)
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    ps[f] = p
    print(f"  {f[:26]:27s} UR087={uv:3.0f} pred={b[0]+b[1]*up:5.1f} z={z:5.2f} p={p:.3f}")
# Holm
sorted_p = sorted(ps.values())
holm = [min(1, p * (len(ps) - i)) for i, p in enumerate(sorted_p)]
print('  Holm: p_ordenados=', [round(x, 3) for x in sorted_p], '-> ajustados=', [round(x, 3) for x in holm])
print('  -> ninguna relacion de suma sobrevive Holm (min p ajustado >0.05)' if min(holm) > 0.05 else '  -> alguna sobrevive')
