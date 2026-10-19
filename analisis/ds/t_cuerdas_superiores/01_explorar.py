# -*- coding: utf-8 -*-
"""Exploracion estructural: cuerdas con union T y su grupo precedente."""
import pandas as pd, numpy as np, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
g = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'grupos.csv'))

# valor: 0 sin nudos = ausente
c['sin_nudos'] = c['nudos'].isna() | (c['nudos'].astype(str).str.strip().isin(['', 'nan']))
c['val'] = c['valor'].astype(float)
c.loc[c['sin_nudos'] & (c['val'] == 0), 'val'] = np.nan

T = c[c['union'] == 'T'].copy()
rows = []
for kfg, d in T.groupby('kfg'):
    d = d.sort_values('orden')
    tops = d[(d['nivel'] == 0)]
    for _, t in tops.iterrows():
        # grupo precedente
        gg = g[g['kfg'] == kfg].sort_values('grupo')
        prev = gg[gg['grupo'] == t['grupo'] - 1]
        rec = dict(kfg=kfg, top=t['cuerda'], top_val=t['val'], top_grupo=t['grupo'],
                   top_color=t['color'], top_orden=t['orden'], nT=len(d),
                   nT_level0=len(tops), prev_grupo=np.nan, prev_desde=np.nan,
                   prev_hasta=np.nan, prev_n=np.nan, prev_sum_l0=np.nan,
                   prev_sum_all=np.nan, prev_n_l0=np.nan)
        if len(prev):
            p = prev.iloc[0]
            pd_ = c[(c['kfg'] == kfg) & (c['grupo'] == p['grupo'])]
            l0 = pd_[pd_['nivel'] == 0]
            rec.update(prev_grupo=p['grupo'], prev_desde=p['desde'],
                       prev_hasta=p['hasta'], prev_n=len(pd_),
                       prev_sum_l0=l0['val'].sum(min_count=1),
                       prev_sum_all=pd_['val'].sum(min_count=1),
                       prev_n_l0=len(l0))
        rows.append(rec)
res = pd.DataFrame(rows)
res['match_l0'] = np.isclose(res['top_val'], res['prev_sum_l0'])
res['match_all'] = np.isclose(res['top_val'], res['prev_sum_all'])
res.to_csv(os.path.join(BASE, 'tops_estructura.csv'), index=False)
print('tops level0:', len(res), 'quipus:', res.kfg.nunique())
print(res[['kfg','top','top_val','top_grupo','prev_grupo','prev_n','prev_n_l0',
           'prev_sum_l0','prev_sum_all','match_l0','match_all']].to_string())
print('\nMATCH l0:', res.match_l0.sum(), '/', res.match_l0.notna().sum())
print('MATCH all:', res.match_all.sum(), '/', res.match_all.notna().sum())
