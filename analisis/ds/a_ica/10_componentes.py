# -*- coding: utf-8 -*-
"""Filtro de información (>=3 valores distintos) + componentes conexas vs nulo."""
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

def graph_edges(ser, L=4, thr=2, mindistinct=3):
    edges = {}
    ss = {ob: {g for g in seqset(ser[ob], L) if max(g) > thr and len(set(g)) >= mindistinct} for ob in ser}
    for i in range(len(OBJS)):
        for j in range(i+1, len(OBJS)):
            n = len(ss[OBJS[i]] & ss[OBJS[j]])
            if n >= 1: edges[frozenset((OBJS[i], OBJS[j]))] = n
    return edges

def components(edges, nodes):
    par = {n: n for n in nodes}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in edges:
        a, b = tuple(e); ra, rb = f(a), f(b)
        if ra != rb: par[ra] = rb
    comp = defaultdict(list)
    for n in nodes: comp[f(n)].append(n)
    return [sorted(v) for v in comp.values() if len(v) > 1]

edges = graph_edges(series)
comps = components(edges, OBJS)
print('=== Componentes conexas (L=4, max>2, >=3 valores distintos), >=2 nodos ===')
for comp in sorted(comps, key=len, reverse=True):
    print('  tamaño %d: %s' % (len(comp), comp))
    for a in comp:
        print('      %s [%s]' % (a, pr.get(a)))

maxcomp = max((len(c) for c in comps), default=1)
n_edges = len(edges)
print('\nobs: %d componentes>1, componente mayor=%d, aristas=%d' % (len(comps), maxcomp, n_edges))
# nulo
nm, ne = [], []
for t in range(500):
    perm = {}
    for k, ob in enumerate(OBJS):
        perm[ob] = list(np.random.default_rng(t*17 + k).permutation(series[ob]))
    e = graph_edges(perm); c2 = components(e, OBJS)
    nm.append(max((len(x) for x in c2), default=1)); ne.append(len(e))
nm = np.array(nm); ne = np.array(ne)
print('nulo componente mayor: media %.2f p95=%.0f  p=%.4f' % (nm.mean(), np.percentile(nm,95), (np.sum(nm>=maxcomp)+1)/501))
print('nulo nº aristas: media %.1f  obs=%d  p=%.4f' % (ne.mean(), n_edges, (np.sum(ne>=n_edges)+1)/501))

print('\n=== Tríada Pisco/Ica [30,40,30,50]: KH0141, KH0464, KH0465 ===')
for ob in ('KH0141', 'KH0464', 'KH0465'):
    print('  %s [%s] n=%d total=%d : %s' % (ob, pr.get(ob), len(series[ob]), sum(series[ob]), series[ob]))
