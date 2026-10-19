# -*- coding: utf-8 -*-
"""Tramos contiguos comunes vía n-gramas (rápido) + grafo + nulo por permutación."""
import pandas as pd, numpy as np, os
from collections import defaultdict

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
HERE = os.path.dirname(__file__)
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
OBJS = list(sel['objeto'].unique())
series = {ob: series_of(ob) for ob in OBJS}

def seqset(v, L): return set(tuple(v[i:i+L]) for i in range(len(v)-L+1))

def best_runs(ser, Lmin=3, Lmax=16, thr=2):
    """Devuelve lista (L, a, b, gram) de los mejores tramos compartidos distintivos."""
    out = []
    for L in range(Lmax, Lmin-1, -1):
        d = defaultdict(list)
        for ob in ser:
            for g in seqset(ser[ob], L):
                if max(g) > thr:
                    d[g].append(ob)
        for g, obs in d.items():
            for i in range(len(obs)):
                for j in range(i+1, len(obs)):
                    out.append((L, obs[i], obs[j], g))
    return out

runs = best_runs(series)
runs.sort(key=lambda x: (-x[0], x[1]))
print('=== Tramos compartidos distintivos más largos (top) ===')
seen = set()
for L, a, b, g in runs:
    key = tuple(sorted((a, b)))
    if (key, L) in seen: continue
    seen.add((key, L))
    if len([1 for s in seen if s[0]==key]) == 1 and L >= 4:
        print('%2d  %s [%s] ~ %s [%s]  %s' % (L, a, pr.get(a), b, pr.get(b), list(g)))
    if len(seen) > 400: break

# maxrun por par
maxrun = defaultdict(int); barg = {}
for L, a, b, g in runs:
    key = tuple(sorted((a, b)))
    if L > maxrun[key]:
        maxrun[key] = L; barg[key] = g
print('\n=== Pares con tramo distintivo >=5 ===')
for (a, b), L in sorted(maxrun.items(), key=lambda x: -x[1]):
    if L >= 5:
        print('%2d  %s [%s] ~ %s [%s]  %s' % (L, a, pr.get(a), b, pr.get(b), list(barg[(a,b)])))

# ---- Nulo: maxrun global bajo permutación dentro de cada quipu ----
maxobs = max(maxrun.values()) if maxrun else 0
null = []
for t in range(500):
    perm = {}
    for k, ob in enumerate(OBJS):
        rng = np.random.default_rng(t*131 + k)
        perm[ob] = list(rng.permutation(series[ob]))
    mx = 0
    for L in range(maxobs+2, 2, -1):
        d = defaultdict(int)
        for ob in perm:
            for g in seqset(perm[ob], L):
                if max(g) > 2: d[g] += 1
        if any(v >= 2 for v in d.values()):
            mx = L; break
    null.append(mx)
null = np.array(null)
p = (np.sum(null >= maxobs)+1)/(len(null)+1)
print('\nTramo máximo obs=%d  nulo medio=%.2f  p95=%.0f  p=%.4f' % (maxobs, null.mean(), np.percentile(null,95), p))

# ---- Grafo por n-gramas L=4 distintivos ----
ss = {ob: {g for g in seqset(series[ob],4) if max(g) > 2} for ob in OBJS}
print('\n=== Aristas con >=2 n-gramas L=4 distintivos compartidos ===')
for i in range(len(OBJS)):
    for j in range(i+1, len(OBJS)):
        n = len(ss[OBJS[i]] & ss[OBJS[j]])
        if n >= 2:
            print('  %d  %s [%s] ~ %s [%s]' % (n, OBJS[i], pr.get(OBJS[i]), OBJS[j], pr.get(OBJS[j])))
