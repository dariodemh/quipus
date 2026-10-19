"""P7: controles finales. Lado del par vs color dominante en el corpus; prediccion
de la regla de orientacion en las variantes; total por tipo en UR1140."""
import numpy as np, pandas as pd
from collections import Counter
from scipy.stats import fisher_exact, mannwhitneyu, binomtest
from lib import load, records, canon, prof, OUT

c = load()
print('== lado del par de marcadoras vs color dominante (grupos de 9 con 2 marcadoras) ==')
rows = []
for k, dd in c[c.nivel == 0].groupby('kfg'):
    for r in records(c, k, size=9):
        rows.append(dict(k=k, maj=r['maj'], side='L' if r['pos'] == (3, 4) else ('R' if r['pos'] == (6, 7) else 'otro')))
D = pd.DataFrame(rows)
print(pd.crosstab(D.maj, D.side).to_string())
A = D[(D.side != 'otro')]
tab = pd.crosstab(A.maj.isin(['W']), A.side)
print('\nW vs no-W x L/R:'); print(tab.to_string())
print('Fisher p=', fisher_exact(tab.values)[1])
# dentro de cada quipu: coherencia lado-color
print('\nquipus con ambos lados: color dominante por lado')
g = D[D.side != 'otro'].groupby('k').filter(lambda x: x.side.nunique() > 1)
if len(g):
    print(g.groupby(['k', 'side']).maj.agg(lambda s: dict(Counter(s))).to_string())

print('\n== UR1140: total del registro por tipo de par ==')
R = [r for r in records(c, 'UR1140')]
for p in [(3, 4), (6, 7)]:
    t = [r['tot'] for r in R if r['pos'] == p]
    print(p, 'n', len(t), 'total medio', round(np.mean(t), 1))
a = [r['tot'] for r in R if r['pos'] == (3, 4)]; b = [r['tot'] for r in R if r['pos'] == (6, 7)]
print('MWU p=', mannwhitneyu(a, b).pvalue)

print('\n== prediccion de la regla de orientacion (sin invertir vs invertir) ==')
for k, size in [('UR1131', 10), ('UR234', 8), ('UR1140', 9)]:
    RR = [r for r in records(c, k, size=size) if not np.isnan(r['vals']).any()]
    orig = np.array([r['vals'] for r in RR])
    f_orig = np.mean([np.argmax(v) == 0 for v in orig])
    can = np.array([canon(r['vals'], r['pos'], size=size) for r in RR])
    f_can = np.mean([np.argmax(v) == 0 for v in can])
    n = len(can); pbin = binomtest(int(f_can * n), n, 0.5, alternative='greater').pvalue
    print(f'{k} (size {size}, n={n}): sin invertir max_c1={f_orig:.0%} | regla max_c1={f_can:.0%} | p(regla vs azar)={pbin:.5f}')

print('\n== UR1176: grupos de 9 con 2 marcadoras y campos completos ==')
RR = records(c, 'UR1176')
print('grupos', len(RR), 'posiciones', Counter(str(r['pos']) for r in RR),
      'completos', sum(1 for r in RR if not np.isnan(r['vals']).any()))
for r in RR[:3]:
    print(' ', r['pos'], np.round(r['vals'], 0), r['mcol'])

print('\n== Santa: 6 campos, posicion del maximo (bandas de color de 6) ==')
allpos = []
for k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    cols = list(d.col); vals = d.v.to_numpy(float); i = 0
    while i <= len(cols) - 6:
        if len(set(cols[i:i + 6])) == 1 and not np.isnan(vals[i:i + 6]).any() and np.ptp(vals[i:i + 6]) > 0:
            allpos.append(int(np.argmax(vals[i:i + 6])) + 1); i += 6
        else:
            i += 1
print('n bandas', len(allpos), 'posicion del maximo:', dict(Counter(allpos)),
      'frac pos1', round(np.mean(np.array(allpos) == 1), 3))
