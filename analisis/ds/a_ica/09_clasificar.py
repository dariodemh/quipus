# -*- coding: utf-8 -*-
"""Clasificar pares con tramo distintivo >=4 en publicados (Urton 2005) vs nuevos."""
import pandas as pd, numpy as np, os
from collections import defaultdict
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos'); HERE = os.path.dirname(__file__)
sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv')); sel['kfg'] = sel['kfg'].astype(str)
OBJ = dict(zip(sel['kfg'], sel['objeto'])); pr = dict(zip(sel['objeto'], sel['procedencia']))
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv')); c['kfg'] = c['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy(); cc['objeto'] = cc['kfg'].map(OBJ)
def ncl(s): return 0 if pd.isna(s) or str(s).strip() in ('', 'nan') else len([x for x in str(s).split(';') if x.strip()])
cc['ncl'] = cc['nudos'].map(ncl); cc = cc.sort_values(['kfg', 'orden'])
def series_of(ob):
    kfg = sel[sel['objeto'] == ob]['kfg'].iloc[0]
    sub = cc[(cc['objeto'] == ob) & (cc['kfg'] == kfg)]
    return sub[(sub['nivel'] == 0) & (sub['ncl'] > 0)]['valor'].astype(int).tolist()
OBJS = list(sel['objeto'].unique()); series = {ob: series_of(ob) for ob in OBJS}
def seqset(v, L): return set(tuple(v[i:i+L]) for i in range(len(v)-L+1))
uron = {frozenset(p) for p in [('KH0212', 'KH0213'), ('KH0175', 'KH0190'), ('KH0128', 'KH0137'), ('KH0130', 'KH0166')]}
maxrun = defaultdict(int); barg = {}
for L in range(16, 3, -1):
    d = defaultdict(list)
    for ob in OBJS:
        for g in seqset(series[ob], L):
            if max(g) > 2: d[g].append(ob)
    for g, obs in d.items():
        for i in range(len(obs)):
            for j in range(i+1, len(obs)):
                key = frozenset((obs[i], obs[j]))
                if L > maxrun[key]:
                    maxrun[key] = L; barg[key] = g
print('=== Pares con tramo distintivo >=4 (clasificados) ===')
rows = []
for key, L in sorted(maxrun.items(), key=lambda x: -x[1]):
    if L >= 4:
        a, b = sorted(key)
        rows.append((L, a, b, 'PUBLICADO-Urton' if key in uron else 'nuevo', list(barg[key])))
for L, a, b, cl, g in rows:
    print('%2d  %s~%s  %-16s [%s] [%s]' % (L, a, b, cl, pr.get(a, '')[:14], pr.get(b, '')[:14]))
    print('      run=%s' % g)
print('\nTotal pares >=4:', len(rows), '| publicados:', sum(1 for r in rows if r[3].startswith('PUB')), '| nuevos:', sum(1 for r in rows if r[3] == 'nuevo'))
