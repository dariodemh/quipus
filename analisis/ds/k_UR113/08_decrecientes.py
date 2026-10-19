# -*- coding: utf-8 -*-
"""UR113: orden decreciente de los colgantes dentro de cada grupo, y contexto de corpus."""
import pandas as pd, numpy as np, os
from scipy.stats import spearmanr
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
c = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'), dtype={'kfg': str})
c['valor'] = pd.to_numeric(c.valor, errors='coerce').fillna(0)
for x in ['nivel', 'grupo']:
    c[x] = pd.to_numeric(c[x], errors='coerce')
p = c[c.nivel == 0]

def rho(g):
    v = g.valor.values
    if len(v) < 5 or len(set(v)) < 3: return np.nan
    return spearmanr(np.arange(len(v)), v)[0]

rows = []
for (k, gi), g in p.groupby(['kfg', 'grupo']):
    r = rho(g)
    if not np.isnan(r):
        rows.append(dict(kfg=k, grupo=gi, n=len(g), rho=r))
R = pd.DataFrame(rows)
R['dec'] = (R.rho <= -0.6).astype(int)
per = R.groupby('kfg').agg(ngrupos=('rho', 'size'), nder=('dec', 'sum'), rho_med=('rho', 'median'))
per['frac'] = per.nder / per.ngrupos
per = per[per.ngrupos >= 3].sort_values('frac', ascending=False)
print('grupos analizables (n>=5, >=3 valores distintos):', len(R), 'en', R.kfg.nunique(), 'quipus')
print('\nUR113: grupos', int(per.loc['UR113', 'ngrupos']), 'decrecientes', int(per.loc['UR113', 'nder']),
      'frac', round(per.loc['UR113', 'frac'], 3), 'rho mediana', round(per.loc['UR113', 'rho_med'], 2))
print('percentil de UR113 en frac decreciente:', round((per.frac < per.loc['UR113', 'frac']).mean(), 3),
      '; en rho mediana (mas negativo = mas decreciente):',
      round((per.rho_med > per.loc['UR113', 'rho_med']).mean(), 3))
print('\nTop 12 quipus por fraccion de grupos decrecientes (>=3 grupos):')
print(per.head(12).round(2).to_string())
print('\nDistribucion: media frac', round(per.frac.mean(), 3), 'mediana', round(per.frac.median(), 3))
per.to_csv(os.path.join(OUT, 'decrecientes_corpus.csv'))
# KFG
d = pd.read_csv(os.path.join(BASE, 'data/external/data-science-khipu-article/data/ascher_sum_relations/ascher_decreasing_cluster.csv'))
s = d[d.name.astype(str).str.strip() == 'UR113']
print('\nKFG ascher_decreasing_cluster para UR113:', s[['has_decreasing_clusters', 'num_decreasing_clusters', 'mean']].to_dict('records'))
d['num_decreasing_clusters'] = pd.to_numeric(d.num_decreasing_clusters, errors='coerce')
print('media corpus num_decreasing_clusters', round(d.num_decreasing_clusters.mean(), 2), 'max', d.num_decreasing_clusters.max())
print('percentil UR113:', round((d.num_decreasing_clusters < s.num_decreasing_clusters.iloc[0]).mean(), 3) if len(s) else 'NA')
