# -*- coding: utf-8 -*-
"""Jerarquía del archivo (detalle vs resumen) y alineación del par KH0128/KH0137."""
import pandas as pd, numpy as np, os
from collections import defaultdict, Counter

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
OBJS = list(sel['objeto'].unique())
series = {ob: series_of(ob) for ob in OBJS}
tot = {ob: sum(series[ob]) for ob in OBJS}
vals_by = {ob: set(series[ob]) for ob in OBJS}

# --- Alineación KH0128 / KH0137 ---
a = series['KH0128']; b = series['KH0137']
run = [40, 9, 57, 30, 56, 80, 21, 8, 22, 12]
def find(hay, needle):
    for i in range(len(hay)-len(needle)+1):
        if hay[i:i+len(needle)] == needle: return i
    return -1
ia, ib = find(a, run), find(b, run)
print('=== Alineación KH0128(UR1114) / KH0137(UR1123) ===')
print('corrida compartida:', run)
print('posición en KH0128:', ia, '/', len(a), '   posición en KH0137:', ib, '/', len(b))
w = 6
print('KH0128 %s' % a[max(0,ia-6):ia+len(run)+6])
print('KH0137 %s' % b[max(0,ib-6):ib+len(run)+6])
print('total KH0128=%d  total KH0137=%d' % (tot['KH0128'], tot['KH0137']))

# --- Grafo de contención de totales: X contiene el total de Y (resumen) ---
print('\n=== Candidatos a RESUMEN: quipus que contienen el total de otros ===')
contains = defaultdict(list)
for x in OBJS:
    for y in OBJS:
        if x != y and tot[y] > 0 and tot[y] in vals_by[x]:
            contains[x].append(y)
for x, ys in sorted(contains.items(), key=lambda kv: -len(kv[1]))[:10]:
    print('  %s [%s] contiene totales de %d quipus: %s' % (x, pr[x], len(ys), ys[:8]))

print('\n=== Candidatos a DETALLE: cuyo total aparece en muchos otros ===')
inother = Counter()
for x, ys in contains.items():
    for y in ys:
        inother[y] += 1
for y, n in inother.most_common(10):
    print('  %s [%s] total=%d aparece en %d quipus' % (y, pr[y], tot[y], n))

# Robustez del test de totales con umbral
def total_hits(thr):
    hits = 0
    for x in OBJS:
        vals = vals_by[x]
        for y in OBJS:
            if x != y and tot[y] > thr and tot[y] in vals:
                hits += 1
    return hits
print('\n=== Robustez test de totales por umbral ===')
for thr in (0, 20, 100, 500):
    obs = total_hits(thr)
    null = []
    allv = [v for ob in OBJS for v in series[ob]]
    for t in range(500):
        rng = np.random.default_rng(t*3 + 1)
        sh = allv[:]; rng.shuffle(sh); k = 0
        pt, pv = {}, {}
        for ob in OBJS:
            n = len(series[ob]); seg = sh[k:k+n]; k += n
            pt[ob] = sum(seg); pv[ob] = set(seg)
        h = 0
        for x in OBJS:
            for y in OBJS:
                if x != y and pt[y] > thr and pt[y] in pv[x]: h += 1
        null.append(h)
    null = np.array(null); p = (np.sum(null >= obs)+1)/(len(null)+1)
    print('  thr>%3d  obs=%4d  nulo=%6.1f  p=%.4f' % (thr, obs, null.mean(), p))
