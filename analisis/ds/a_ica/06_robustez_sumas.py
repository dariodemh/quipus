# -*- coding: utf-8 -*-
"""Robustez (filtro distintivo, corrección múltiple), sumas internas y jerarquía."""
import pandas as pd, numpy as np, os
from collections import defaultdict

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
EXT = os.path.join(RAIZ, 'data', 'external', 'data-science-khipu-article', 'data')
HERE = os.path.dirname(__file__)
sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv')); sel['kfg'] = sel['kfg'].astype(str)
OBJ = dict(zip(sel['kfg'], sel['objeto'])); pr = dict(zip(sel['objeto'], sel['procedencia']))
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv')); c['kfg'] = c['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy(); cc['objeto'] = cc['kfg'].map(OBJ)
def ncl(s): return 0 if pd.isna(s) or str(s).strip() in ('', 'nan') else len([x for x in str(s).split(';') if x.strip()])
cc['ncl'] = cc['nudos'].map(ncl); cc = cc.sort_values(['kfg', 'orden'])
def series_of(ob, col='valor'):
    kfg = sel[sel['objeto'] == ob]['kfg'].iloc[0]
    sub = cc[(cc['objeto'] == ob) & (cc['kfg'] == kfg)]
    return sub[(sub['nivel'] == 0) & (sub['ncl'] > 0)][col].tolist()
OBJS = list(sel['objeto'].unique())
series = {ob: series_of(ob) for ob in OBJS}
colser = {ob: [str(x) for x in series_of(ob, 'color')] for ob in OBJS}

def seqset(v, L): return set(tuple(v[i:i+L]) for i in range(len(v)-L+1))
def shared(ser, L, filt):
    ss = {ob: {g for g in seqset(ser[ob], L) if filt(g)} for ob in ser}
    tot = 0
    for i in range(len(OBJS)):
        for j in range(i+1, len(OBJS)):
            tot += len(ss[OBJS[i]] & ss[OBJS[j]])
    return tot

print('=== Robustez: valor L=4 con filtros ===')
for name, filt in [('sin filtro', lambda g: True),
                   ('distintivo (max>2)', lambda g: max(g) > 2),
                   ('sin repetidos', lambda g: len(set(g)) == len(g)),
                   ('distintivo y sin repetidos', lambda g: max(g) > 2 and len(set(g)) == len(g))]:
    obs = shared(series, 4, filt)
    null = []
    for t in range(500):
        perm = {}
        for k, ob in enumerate(OBJS):
            perm[ob] = list(np.random.default_rng(t*7 + k).permutation(series[ob]))
        null.append(shared(perm, 4, filt))
    null = np.array(null); p = (np.sum(null >= obs)+1)/(len(null)+1)
    print('  %-28s obs=%5d  nulo=%7.1f  p=%.4f' % (name, obs, null.mean(), p))

print('\n=== Robustez: color L=4 con filtros ===')
for name, filt in [('sin filtro', lambda g: True),
                   ('>=2 colores distintos', lambda g: len(set(g)) > 1),
                   ('>=3 colores distintos', lambda g: len(set(g)) > 2)]:
    obs = shared(colser, 4, filt)
    null = []
    for t in range(500):
        perm = {}
        for k, ob in enumerate(OBJS):
            perm[ob] = list(np.random.default_rng(t*13 + k).permutation(colser[ob]))
        null.append(shared(perm, 4, filt))
    null = np.array(null); p = (np.sum(null >= obs)+1)/(len(null)+1)
    print('  %-28s obs=%5d  nulo=%7.1f  p=%.4f' % (name, obs, null.mean(), p))

print('\n=== Sumas internas (KFG) ===')
for f, k in [('ascher_sum_relationships', 'name'), ('cluster_cluster_sum', 'name')]:
    d = pd.read_csv(os.path.join(EXT, 'ascher_sum_relations', f + '.csv'))
    if k not in d.columns: k = d.columns[1]
    # identificar columna de nombre
    nmcol = [col for col in d.columns if col.lower() in ('name', 'kfg_name')]
    nmcol = nmcol[0] if nmcol else d.columns[1]
    d['k'] = d[nmcol].astype(str).str.replace(r'.*>(AS|UR|KH|HP|JC|QU|CM)\d+<.*', r'\1', regex=True)
    sub = d[d[nmcol].astype(str).str.contains('|'.join(sel['kfg']), na=False)]
    print(' ', f, 'filas para el set:', len(sub))
    numcols = [col for col in d.columns if col.startswith('num_')]
    for col in numcols:
        vals = pd.to_numeric(sub[col], errors='coerce').fillna(0)
        if vals.sum() > 0:
            quipus = sub.loc[vals > 0, nmcol].astype(str).str.extract(r'>(\w+)<')[0].tolist()
            print('    %s: total=%d en %s' % (col, int(vals.sum()), quipus[:10]))

print('\n=== Quipus con top cord / suma (de khipu_summary) ===')
sm = pd.read_csv(os.path.join(EXT, 'khipu_summary.csv')).set_index('kfg_name')
sm = sm[sm.index.isin(sel['kfg'])]
for col in ['num_top_cords', 'num_top_cord_sum_clusters', 'num_top_cord_double_sum_clusters',
            'num_banded_clusters', 'num_decreasing_clusters', 'num_seriated_clusters']:
    nz = sm[sm[col].fillna(0) > 0]
    print(' ', col, '->', len(nz), 'quipus:', list(nz.index)[:12])
