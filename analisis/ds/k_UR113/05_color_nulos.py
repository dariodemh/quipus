# -*- coding: utf-8 -*-
"""UR113: nulos de color y de repeticion de valores (1000 permutaciones, semilla 0)."""
import pandas as pd, numpy as np, os, itertools
from collections import defaultdict
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv')); u['valor'] = u.valor.fillna(0)
p = u[u.nivel == 0].copy().reset_index(drop=True)
s = u[u.nivel > 0].copy()
p['color'] = p.color.fillna('NA'); s['color'] = s.color.fillna('NA')
N = 1000

# 1) grupos monocromos
def mono(df):
    return int(df.groupby('grupo').color.nunique().eq(1).sum())
obs1 = mono(p)
null1 = [mono(p.assign(color=rng.permutation(p.color.values))) for _ in range(N)]
p1 = (np.sum(np.array(null1) >= obs1) + 1) / (N + 1)
print(f'1. grupos monocromos: obs {obs1}/{p.grupo.nunique()}  nulo {np.mean(null1):.1f} (max {max(null1)})  p={p1:.4f}')

# 2) valor modal repetido dentro de grupo
def modal_stat(df):
    c = 0
    for gi, g in df.groupby('grupo'):
        v = g.valor[g.valor > 0]
        if len(v) >= 4:
            c += int(v.value_counts().iloc[0])
    return c
obs2 = modal_stat(p)
null2 = [modal_stat(p.assign(valor=rng.permutation(p.valor.values))) for _ in range(N)]
p2 = (np.sum(np.array(null2) >= obs2) + 1) / (N + 1)
print(f'2. suma de conteos del valor modal por grupo (grupos >=4 cuerdas): obs {obs2}  nulo {np.mean(null2):.1f} (max {max(null2)})  p={p2:.4f}')
# 2b) grupos con un unico valor dominante >=50%
dom = p[p.valor > 0].groupby('grupo').valor.agg(lambda x: x.value_counts().iloc[0] / len(x))
print('   grupos con >=50% de un mismo valor:', int((dom >= .5).sum()), ':', {int(k): round(v, 2) for k, v in dom[dom >= .5].items()})

# 3) orden de color dentro de la lista de subsidiarias
def consist(df):
    pair = defaultdict(lambda: [0, 0])
    for _, g in df.groupby('padre'):
        cl = list(g.color)
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                if cl[i] == cl[j]: continue
                pair[(cl[i], cl[j])][0] += 1; pair[(cl[j], cl[i])][1] += 1
    tot = cons = 0
    for (a, b), (ab, ba) in pair.items():
        if ab + ba < 3: continue
        tot += ab + ba; cons += max(ab, ba)
    return cons / tot if tot else 0
obs3 = consist(s)
null3 = []
for _ in range(200):
    d = s.copy()
    d['color'] = d.groupby('padre').color.transform(lambda x: rng.permutation(x.values))
    null3.append(consist(d))
p3 = (np.sum(np.array(null3) >= obs3) + 1) / (len(null3) + 1)
print(f'3. consistencia de orden de color intra-madre: obs {obs3:.3f}  nulo {np.mean(null3):.3f} (max {max(null3):.3f})  p={p3:.4f}')

# 4) unicidad de color dentro de la lista de subsidiarias
s['nsub'] = s.groupby('padre').color.transform('size')
s['ncol'] = s.groupby('padre').color.transform('nunique')
obs4 = s.groupby('padre').ncol.first().sub(s.groupby('padre').nsub.first()).mean()
# nulo: colores sorteados de la distribucion global de subsidiarias
gl = s.color.value_counts(normalize=True)
def sim():
    out = []
    for _, g in s.groupby('padre'):
        draws = rng.choice(gl.index, size=len(g), p=gl.values)
        out.append(len(set(draws)) - len(g))
    return np.mean(out)
null4 = [sim() for _ in range(200)]
p4 = (np.sum(np.array(null4) <= obs4) + 1) / (len(null4) + 1)
print(f'4. color distinto - n subsidiarias (0 = todos distintos): obs {obs4:.2f}  nulo {np.mean(null4):.2f} (min {min(null4):.2f})  p={p4:.4f}')
print('   (nulo mas negativo = mas unicidad)')

# 5) color de la madre predice color de sus subsidiarias?
ct = pd.crosstab(s.color, s.merge(p[['cuerda', 'color']], left_on='padre', right_on='cuerda', suffixes=('', '_madre')).color_madre, normalize='columns')
print('\n5. solapamiento color madre/subs: prob. de que una sub comparta color con su madre:',
      round((s.merge(p[['cuerda','color']],left_on='padre',right_on='cuerda',suffixes=('','_m')).eval('color==color_m') ).mean(), 3))
