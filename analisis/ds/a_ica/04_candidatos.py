# -*- coding: utf-8 -*-
"""Inspección de los pares candidatos y control de explicaciones aburridas."""
import pandas as pd, numpy as np, os
from collections import Counter

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
HERE = os.path.dirname(__file__)
sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv')); sel['kfg'] = sel['kfg'].astype(str)
OBJ = dict(zip(sel['kfg'], sel['objeto']))
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv')); c['kfg'] = c['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy()
cc['objeto'] = cc['kfg'].map(OBJ)

def ncl(s):
    return 0 if pd.isna(s) or str(s).strip() in ('', 'nan') else len([x for x in str(s).split(';') if x.strip()])
cc['ncl'] = cc['nudos'].map(ncl)
cc = cc.sort_values(['kfg', 'orden'])

def series_of(ob):
    kfgs = sel[sel['objeto'] == ob]['kfg'].tolist()
    sub = cc[cc['objeto'] == ob]
    # un solo kfg por objeto (el primero)
    kfg = kfgs[0]
    sub = sub[sub['kfg'] == kfg]
    return sub[(sub['nivel'] == 0) & (sub['ncl'] > 0)]['valor'].astype(int).tolist(), kfg

print('=== KH0128 (UR1114) vs KH0137 (UR1123) ===')
sa, ka = series_of('KH0128')
sb, kb = series_of('KH0137')
print('KH0128 = %s, n pendientes=%d, total=%d' % (ka, len(sa), sum(sa)))
print('KH0137 = %s, n pendientes=%d, total=%d' % (kb, len(sb), sum(sb)))
print('secuencia KH0128:', sa[:40], '...')
print('secuencia KH0137:', sb[:40], '...')

def seqset(v, L): return set(tuple(v[i:i+L]) for i in range(len(v)-L+1))
for L in (3, 4, 5):
    inter = seqset(sa, L) & seqset(sb, L)
    print('L=%d compartidos=%d -> %s' % (L, len(inter), sorted(inter)))

# ¿los n-gramas compartidos son "distintivos"? nº de n-gramas triviales (todos <=2)
def distinctive(v, L, thr=2):
    S = seqset(v, L)
    return {g for g in S if max(g) > thr}
print('L=4 distintivos KH0128=%d KH0137=%d compartidos(>2)=%d' %
      (len(distinctive(sa,4)), len(distinctive(sb,4)), len(distinctive(sa,4)&distinctive(sb,4))))

# ¿hay coincidencia de TOTAL entre ambos?
print('total KH0128=%d  total KH0137=%d' % (sum(sa), sum(sb)))

print('\n=== KH0157 (UR1141) vs KH0164 (UR1152): estructura (2,2,2,2,2,2,2,2,2,2) ===')
for ob in ('KH0157', 'KH0164'):
    s, k = series_of(ob)
    print('%s = %s  n=%d  secuencia=%s total=%d' % (ob, k, len(s), s, sum(s)))

print('\n=== Distribución de los 148 aciertos total(A)=valor en B ===')
allvals = {ob: set(cc[(cc['objeto'] == ob) & (cc['ncl'] > 0)]['valor'].astype(int)) for ob in sel['objeto'].unique()}
tot = {ob: sum(series_of(ob)[0]) for ob in sel['objeto'].unique()}
hits = []
for a in tot:
    for b in allvals:
        if a != b and tot[a] > 0 and tot[a] in allvals[b]:
            hits.append(tot[a])
h = Counter(hits)
print('nº total de aciertos:', len(hits), 'de', len(tot), 'objetos')
print('aciertos con total<=20:', sum(v for k, v in h.items() if k <= 20),
      '| >20:', sum(v for k, v in h.items() if k > 20),
      '| >100:', sum(v for k, v in h.items() if k > 100))
print('totales más frecuentes entre los aciertos:', h.most_common(10))
