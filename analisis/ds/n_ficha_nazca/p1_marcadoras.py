"""P1: las 2 marcadoras. Atributos, que distingue a la 1a de la 2a, y asociacion
de su posicion con propiedades del registro."""
import numpy as np, pandas as pd
from collections import Counter
from scipy.stats import mannwhitneyu, binomtest, spearmanr
from lib import load, records, canon, prof, corr, holm, bh, OUT, RNG

c = load()
KS = ['UR1140', 'UR1136', 'UR223', 'HP056']
rows = []
for k in KS:
    for r in records(c, k):
        rows.append(dict(khipu=k, g=r['g'], pos=str(r['pos']), maj=r['maj'], tot=r['tot'],
                         m1col=r['mcol'][0], m2col=r['mcol'][1],
                         m1v=r['mval'][0], m2v=r['mval'][1],
                         m1tor=r['mtor'][0], m2tor=r['mtor'][1],
                         m1uni=r['muni'][0], m2uni=r['muni'][1],
                         m1dir=r['mdir'][0], m2dir=r['mdir'][1],
                         m1L=float(r['mfield'][0:1].largo.iloc[0]) if False else np.nan,
                         m1f=r['mfield'][0], m2f=r['mfield'][1]))
M = pd.DataFrame(rows)
# largos de las marcadoras
for i, k in enumerate(KS):
    pass
lg = {}
for k in KS:
    d = c[(c.kfg == k) & (c.nivel == 0)]
    lg[k] = dict(zip(d.cuerda, d.largo))
M['m1L'] = [lg[r.khipu].get(r.m1f, np.nan) for r in M.itertuples()]
M['m2L'] = [lg[r.khipu].get(r.m2f, np.nan) for r in M.itertuples()]
M['mix1'] = M.m1col.str.contains(':'); M['mix2'] = M.m2col.str.contains(':')

print('== valores de las marcadoras (1a, 2a) por quipu ==')
print(M.groupby('khipu')[['m1v', 'm2v', 'm1L', 'm2L']].agg(['count', 'mean', 'median']).round(1).to_string())

print('\n== pares de color (1a | 2a) ==')
print(M.groupby(['khipu', 'm1col', 'm2col']).size().to_string())

print('\n== torsion / union / direccion (conteos 1a / 2a) ==')
for a, b in [('m1tor', 'm2tor'), ('m1uni', 'm2uni'), ('m1dir', 'm2dir')]:
    print(a, dict(M[a].value_counts()), '|', b, dict(M[b].value_counts()),
          '| iguales', int((M[a] == M[b]).sum()), '/', len(M))

def sign_p(x, y):
    d = np.asarray(x, float) - np.asarray(y, float); d = d[~np.isnan(d)]
    n = int((d != 0).sum()); k = int((d > 0).sum())
    return (binomtest(k, n, 0.5).pvalue if n else np.nan), k, n

print('\n== tests pareados 1a vs 2a ==')
out = []
for k, d in list(M.groupby('khipu')) + [('TODOS', M)]:
    for name, a, b in [('valor', 'm1v', 'm2v'), ('largo', 'm1L', 'm2L')]:
        p, kk, n = sign_p(d[a], d[b])
        out.append(dict(khipu=k, test=f'{name} 1a>2a', k=kk, n=n, p=p))
    a = int((d.mix1 & ~d.mix2).sum()); b2 = int((~d.mix1 & d.mix2).sum())
    out.append(dict(khipu=k, test='color mixta 1a!=2a', k=a, n=a + b2,
                    p=binomtest(a, a + b2, 0.5).pvalue if a + b2 else np.nan))
O = pd.DataFrame(out)
O['holm'] = holm(O.p.fillna(1))
print(O.round(4).to_string(index=False))

print('\n== posicion de las marcadoras vs total del registro ==')
for k, d in M.groupby('khipu'):
    if d.pos.nunique() < 2:
        print(f'{k}: una sola posicion {d.pos.unique()[0]}, n={len(d)}, total medio={d.tot.mean():.1f}')
        continue
    gr = [g.tot.dropna().values for _, g in d.groupby('pos')]
    u, p = mannwhitneyu(*gr) if len(gr) == 2 else (np.nan, np.nan)
    print(f'{k}: ' + ' | '.join(f'{a}: n={len(g)}, tot medio={g.tot.mean():.1f}' for a, g in d.groupby('pos')) + f'  MWU p={p:.4f}')

print('\n== posicion de las marcadoras vs color dominante ==')
print(pd.crosstab([M.khipu, M.maj], M.pos).to_string())

print('\n== posicion de las marcadoras vs indice de grupo (bloques) ==')
for k in ['UR1140', 'UR1136', 'UR223', 'HP056']:
    d = M[M.khipu == k].sort_values('g')
    seq = list(d.pos)
    runs = 1 + sum(1 for i in range(1, len(seq)) if seq[i] != seq[i - 1])
    cnt = 0; B = 9999
    arr = np.array(seq)
    for _ in range(B):
        s = RNG.permutation(arr); rr = 1 + sum(1 for i in range(1, len(s)) if s[i] != s[i - 1])
        if rr <= runs:
            cnt += 1
    print(f'{k}: secuencia {seq} runs={runs} p(<=runs)={(1+cnt)/(1+B):.4f}')

print('\n== UR1140: perfil canonico por tipo de marcadora ==')
Rs = records(c, 'UR1140')
for p in ['(3, 4)', '(6, 7)']:
    V = np.array([canon(x['vals'], x['pos']) for x in Rs if str(x['pos']) == p and not np.isnan(x['vals']).any()])
    print(p, 'n', len(V), 'media cruda', np.round(np.nanmean(V, 0), 1), 'perfil z', np.round(prof(V), 2))

print('\n== valor de las marcadoras vs total del registro (Spearman) ==')
for k, d in M.groupby('khipu'):
    if len(d) >= 5:
        r1, p1 = spearmanr(d.m1v, d.tot, nan_policy='omit')
        r2, p2 = spearmanr(d.m2v, d.tot, nan_policy='omit')
        print(f'{k}: m1 r={r1:.2f} p={p1:.3f} | m2 r={r2:.2f} p={p2:.3f}')

M.to_csv(OUT / 'marcadoras.csv', index=False)
print('\nescrito marcadoras.csv')
