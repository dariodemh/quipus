# -*- coding: utf-8 -*-
"""E) gran total de A como valor de cuerda de B.
D) periodicidad de color y patrones de color compartidos.
C) modularidad de grupos (tamano de grupo dominante).
"""
import pandas as pd, numpy as np, os
from collections import Counter
ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')
RNG = np.random.default_rng(0); NREP = 500
c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
KFG = q.loc[q['procedencia'].isin(['Nazca', 'Atarco']), 'kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy().sort_values(['kfg', 'orden'])
real = s['nudos'].notna() & (s['nudos'].astype(str).str.strip() != '')
s = s.assign(val=np.where(real, s['valor'], np.nan))

vals = {k: set(d['val'].dropna().astype(int)) for k, d in s.groupby('kfg')}
tot = {k: int(d['val'].dropna().sum()) for k, d in s.groupby('kfg')}
print('=== E) gran total de A presente como valor de cuerda en B ===')
found = 0
for a in KFG:
    for b in KFG:
        if a != b and tot[a] > 0 and tot[a] in vals[b]:
            print(f'   total({a})={tot[a]} aparece como cuerda en {b}')
            found += 1
print('total hallazgos:', found)

# ---- D) periodicidad de color ----
print('\n=== D1) periodicidad de la secuencia de color de colgantes ===')
def colorseq(d):
    d = d[d['nivel'] == 0].sort_values('orden')
    return [str(x) if pd.notna(x) else 'NA' for x in d['color']]
def bestperiod(seq, tmax=40):
    n = len(seq)
    best = (0.0, 1)
    for T in range(2, tmax + 1):
        if n < 2 * T:
            break
        # fraccion de i con color[i]==color[i+T]
        m = sum(1 for i in range(n - T) if seq[i] == seq[i + T])
        f = m / (n - T)
        if f > best[0]:
            best = (f, T)
    return best
cs = {k: colorseq(d) for k, d in s.groupby('kfg')}
for k in KFG:
    f, T = bestperiod(cs[k])
    print(f'   {k}: periodo T={T} coincidencia={f:.2f} (n={len(cs[k])})')
print('\n--- nulo de periodicidad: media de coincidencia a mejor periodo (barajar color dentro de quipu) ---')
obs_mean = np.mean([bestperiod(cs[k])[0] for k in KFG])
null_mean = []
for r in range(200):
    vals_ = []
    for k in KFG:
        v = list(cs[k]); RNG.shuffle(v); vals_.append(bestperiod(v)[0])
    null_mean.append(np.mean(vals_))
null_mean = np.array(null_mean)
print(f'obs_media={obs_mean:.3f} nulo_media={null_mean.mean():.3f} max={null_mean.max():.3f} '
      f'p={(1+(null_mean>=obs_mean).sum())/201:.4f}')

print('\n=== D2) bigramas de color compartidos entre quipus (top) ===')
def bigrams(seq):
    return set(zip(seq[:-1], seq[1:]))
bs = {k: bigrams(cs[k]) for k in KFG}
res = []
for i in range(len(KFG)):
    for j in range(i+1, len(KFG)):
        inter = bs[KFG[i]] & bs[KFG[j]]
        if inter:
            res.append((KFG[i], KFG[j], len(inter), sorted(inter)[:3]))
for r in sorted(res, key=lambda x: -x[2])[:10]:
    print('   ', r)

print('\n=== C) modularidad de grupos (tamano dominante y homogeneidad) ===')
for k in KFG:
    counts = [int((dd['nivel'] == 0).sum()) for _, dd in s[s['kfg'] == k].groupby('grupo')]
    counts = [x for x in counts if x > 0]
    if not counts: continue
    cc = Counter(counts)
    dom, nd = cc.most_common(1)[0]
    print(f'   {k}: n_grupos={len(counts)} tamano_dominante={dom}x{nd} homog={(nd/len(counts)):.2f} counts={counts[:12]}{"..." if len(counts)>12 else ""}')
