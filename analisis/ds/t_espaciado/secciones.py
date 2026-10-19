"""Test de secciones: ¿el gap más grande de cada quipu separa regímenes de valor distintos?

Para cada quipu con >=6 grupos y un gap >=2 cm:
  - se parte en dos por el gap más grande y se mide |media log valor antes - después|
  - nulo: partir en un límite de grupo aleatorio del mismo quipu
Se repite para nº de racimos y largo medio. Unidad = quipu.
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
g = pd.read_pickle(os.path.join(D, 'grupos.pkl')).sort_values(['kfg', 'grupo']).reset_index(drop=True)
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
SEED = 20261017
NPERM = 5000

# medias por grupo
feat = c[c.tiene_nudos].groupby(['kfg', 'grupo']).agg(
    v=('logvalor', 'mean'), ncl=('n_clusters', 'mean'), lar=('largo', 'mean')).reset_index()
g = g.merge(feat, on=['kfg', 'grupo'], how='left')

res = []
detalle = []
for k, d in g.groupby('kfg'):
    d = d.sort_values('grupo').reset_index(drop=True)
    if len(d) < 6:
        continue
    valid = d.dropna(subset=['gap'])
    if valid.empty or valid.gap.max() < 2.0:
        continue
    # posición del gap máximo (gap_after del grupo i)
    idx = int(valid.gap.idxmax())
    # el corte debe dejar >=2 grupos a cada lado
    if idx < 1 or idx > len(d) - 2:
        continue
    row = {}
    for col in ['v', 'ncl', 'lar']:
        x = d[col].values
        if np.isnan(x).any():
            row[col] = np.nan
            continue
        obs = abs(np.nanmean(x[:idx + 1]) - np.nanmean(x[idx + 1:]))
        # nulo: cortes aleatorios entre 1 y len-2
        rng = np.random.default_rng(SEED + sum(ord(ch) for ch in k))
        cuts = rng.integers(1, len(d) - 1, size=NPERM)
        null = np.array([abs(np.nanmean(x[:cc + 1]) - np.nanmean(x[cc + 1:])) for cc in cuts])
        row[col] = dict(obs=obs, null_mean=null.mean(),
                        p=(1 + np.sum(null >= obs)) / (NPERM + 1),
                        z=(obs - null.mean()) / (null.std() + 1e-9))
    if any(not isinstance(row[col], dict) for col in ['v', 'ncl', 'lar']):
        continue
    detalle.append(dict(kfg=k, gap=d.gap.iloc[idx], n_grupos=len(d), **{
        f'{col}_{kk}': vv for col in ['v', 'ncl', 'lar'] for kk, vv in row[col].items()}))
    res.append(row)

R = pd.DataFrame(detalle)
print('quipus con sección (>=6 grupos, gap>=2cm, corte interior):', len(R))
print('gap del corte: mediana', R.gap.median(), '| max', R.gap.max())
for col, name in [('v', 'log valor medio'), ('ncl', 'nº racimos medio'), ('lar', 'largo medio')]:
    print(f'\n--- {name} ---')
    print('obs medio', round(R[f'{col}_obs'].mean(), 3),
          '| nulo medio', round(R[f'{col}_null_mean'].mean(), 3),
          '| z medio', round(R[f'{col}_z'].mean(), 3),
          '| % quipus p<0.05', round((R[f'{col}_p'] < 0.05).mean(), 3),
          '| p(z medio)',
          f"{__import__('scipy').stats.norm.sf(R[f'{col}_z'].mean() * np.sqrt(len(R))):.3g}")

# Comparar con seccionar por el gap más grande vs un gap aleatorio del mismo quipu
print('\nDistribución de z (gap máximo):')
print(R[['v_z', 'ncl_z', 'lar_z']].describe(percentiles=[.5, .9]).round(2).to_string())
