# -*- coding: utf-8 -*-
"""KH0083: patron de color periodico y otras pruebas con nulo. Semilla 0, 1000 perm."""
import pandas as pd, numpy as np
from collections import Counter

rng = np.random.default_rng(0)
NPERM = 1000
C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy().sort_values('orden').reset_index(drop=True)
pend = K[K.nivel == 0].sort_values('orden').reset_index(drop=True)

def prim(s):
    return str(s).split(':')[0].split('/')[0].split('-')[0].strip()
pend['col1'] = pend['color'].map(prim)

pos = np.arange(1, len(pend) + 1)
isSR = pend['col1'].str.contains('SR').to_numpy()

print('== colgantes:', len(pend), '| con SR:', isSR.sum(), '| posiciones SR:', list(pos[isSR]))

# T1: periodicity. max count of SR en una clase de residuo mod m
def max_residue(flags, m):
    r = pos % m
    return max(sum(flags[r == c]) for c in range(m))

obs11 = max_residue(isSR, 11)
print('\n[T1] SR, max n en un residuo mod 11 =', obs11, '(de', isSR.sum(), 'SR)')
null = np.empty(NPERM)
for b in range(NPERM):
    f = rng.permutation(isSR)
    null[b] = max_residue(f, 11)
p11 = (1 + (null >= obs11).sum()) / (1 + NPERM)
print('     nulo media=%.3f  p=%.5f' % (null.mean(), p11))
# por residuo
r = pos % 11
print('     conteo SR por residuo mod11:', {c: int(sum(isSR[r == c])) for c in range(11)})

# T1b: gaps SR
srpos = list(pos[isSR])
print('     gaps entre SR consecutivos:', [srpos[i+1]-srpos[i] for i in range(len(srpos)-1)])

# T2: numero de cambios de color en la secuencia de colgantes vs nulo (solo W/AB/SR/...)
seq = pend['col1'].to_numpy()
def n_changes(s):
    return int(sum(s[i] != s[i-1] for i in range(1, len(s))))
obs_ch = n_changes(seq)
null_ch = np.array([n_changes(rng.permutation(seq)) for _ in range(NPERM)])
p_ch = (1 + (null_ch >= obs_ch).sum()) / (1 + NPERM)
print('\n[T2] cambios de color en secuencia de colgantes: obs=%d nulo=%.1f p=%.4f' % (obs_ch, null_ch.mean(), p_ch))

# T3: suma total y por bloque de 11
print('\n[T3] suma de valor de colgantes = %g' % pend['valor'].sum())
print('     suma de TODAS las cuerdas = %g' % K['valor'].sum())
blocks = [pend['valor'].iloc[11*k:11*(k+1)].sum() for k in range(8)]
print('     suma por bloque de 11:', [int(b) for b in blocks])

# T4: distribucion de valores no-cero
v = K[K['valor'] > 0]['valor'].astype(int)
print('\n[T4] n valores>0 =', len(v), '| distintos =', v.nunique())
print('     top 20 valores:', Counter(v.tolist()).most_common(20))
