"""Descriptivos del espaciado entre grupos y exploración de las relaciones aritméticas KFG."""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
R = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
REL = os.path.join(R, 'data', 'external', 'data-science-khipu-article', 'data', 'ascher_sum_relations')

g = pd.read_pickle(os.path.join(D, 'grupos.pkl'))
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
pd.set_option('display.width', 180)

print('--- espaciado entre grupos ---')
print('grupos', len(g), 'quipus', g.kfg.nunique(), '| quipus con >=2 grupos:', int((g.groupby('kfg').size() >= 2).sum()))
nz = g.dropna(subset=['gap'])
print('pares con gap:', len(nz), '| gap cm:', nz.gap.describe(percentiles=[.25, .5, .75, .9, .95, .99]).round(2).to_dict())
for t in [1, 2, 3, 5, 10]:
    print(f'gap >= {t} cm: {int((nz.gap >= t).sum())} ({100*(nz.gap>=t).mean():.1f}%) en {nz[nz.gap>=t].kfg.nunique()} quipus')
print('gap por tamaño del grupo anterior:')
print(nz.groupby(nz.n_pend.clip(upper=5)).gap.agg(['count', 'median', 'mean', 'max']).round(2).to_string())

# ¿los gaps grandes separan grupos de 1 colgante?
print('\nfracción de grupos siguientes con 1 colgante según gap:')
nz2 = nz.copy()
nz2['sig_n'] = nz2.groupby('kfg').n_pend.shift(-1)
for lo, hi in [(0, 0.75), (0.75, 2), (2, 5), (5, 1e9)]:
    m = (nz2.gap > lo) & (nz2.gap <= hi) if lo else (nz2.gap >= lo) & (nz2.gap <= hi)
    print(f'  ({lo},{hi}]: n={m.sum()}, sig_n=1: {nz2.loc[m,"sig_n"].eq(1).mean():.2f}, mediana sig_n={nz2.loc[m,"sig_n"].median():.0f}')

# ---- relaciones aritméticas KFG: recuento y mapeo a grupos ----
print('\n--- relaciones aritméticas KFG ---')
for f in ['ascher_decreasing_cluster_relation.csv', 'cluster_sum_bands_relation.csv',
          'cluster_cluster_sum_relation.csv', 'pendant_pendant_sum_relation.csv',
          'sum_top_cords_relation.csv', 'double_sum_top_cords_relation.csv']:
    d = pd.read_csv(os.path.join(REL, f))
    print(f'{f}: filas={len(d)}, quipus={d["name"].nunique()}, cols={d.columns.tolist()[:8]}')
    # comprobar que name existe en grupos
    print('  quipus en grupos:', d.name.isin(g.kfg.unique()).mean().round(3))

# cluster positions (índices de grupo) en las relaciones
for f, col in [('ascher_decreasing_cluster_relation.csv', 'cluster_position'),
               ('cluster_sum_bands_relation.csv', 'cluster_position')]:
    d = pd.read_csv(os.path.join(REL, f))
    ok = 0
    for r in d.itertuples():
        gg = g[g.kfg == r.name]
        if len(gg) and 0 <= int(getattr(r, col)) < len(gg):
            ok += 1
    print(f'{f}: cluster_position válido como índice de grupo {ok}/{len(d)}')

d = pd.read_csv(os.path.join(REL, 'cluster_cluster_sum_relation.csv'))
print('\ncluster_distance describe:', d.cluster_distance.describe(percentiles=[.5, .9]).round(2).to_dict())
print('cord_count_distance describe:', d.cord_count_distance.describe(percentiles=[.5, .9]).round(2).to_dict())
print(d[['name', 'cluster_sum', 'left_cluster_position', 'right_cluster_position', 'cluster_distance', 'cord_count_distance']].head(6).to_string())
