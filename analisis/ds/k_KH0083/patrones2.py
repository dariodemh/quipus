# -*- coding: utf-8 -*-
"""KH0083: controles adicionales. Escaneo honesto de periodicidad, runs de color,
estructura vs valor. Semilla 0, 1000 perm."""
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
NPERM = 1000
C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy().sort_values('orden').reset_index(drop=True)
pend = K[K.nivel == 0].sort_values('orden').reset_index(drop=True)
pos = np.arange(1, len(pend) + 1)

# SR en cualquier parte del color
isSR = pend['color'].astype(str).str.contains('SR').to_numpy()
print('SR en cualquier parte:', int(isSR.sum()), 'posiciones', list(pos[isSR]))

# --- escaneo honesto de periodo: max sobre m del max count en residuo ---
def best_period(flags, maxm=44):
    best = (0, 0)
    for m in range(2, maxm + 1):
        r = pos % m
        c = max(sum(flags[r == k]) for k in range(m))
        if c > best[0]:
            best = (c, m)
    return best

obs_best = best_period(isSR)
print('\n[scan] mejor (maxcount, periodo) observado =', obs_best)
null = np.array([best_period(rng.permutation(isSR)) [0] for _ in range(NPERM)])
p = (1 + (null >= obs_best[0]).sum()) / (1 + NPERM)
print('       nulo media=%.3f p=%.5f' % (null.mean(), p))

# --- runs de color (menos cambios = mas homogeneo) ---
def prim(s): return str(s).split(':')[0].split('/')[0].split('-')[0].strip()
seq = pend['color'].map(prim).to_numpy()
def n_ch(s): return int(sum(s[i] != s[i-1] for i in range(1, len(s))))
obs = n_ch(seq)
nullc = np.array([n_ch(rng.permutation(seq)) for _ in range(NPERM)])
p_low = (1 + (nullc <= obs).sum()) / (1 + NPERM)
p_high = (1 + (nullc >= obs).sum()) / (1 + NPERM)
print('\n[runs] cambios color colgantes obs=%d nulo=%.1f p_menos=%.4f p_mas=%.4f' % (obs, nullc.mean(), p_low, p_high))

# --- color dominante W vs AB por bloque de 11 ---
for k in range(8):
    blk = seq[11*k:11*k+11]
    print('  bloque %d [%d-%d] colores:' % (k+1, 11*k+1, 11*k+11), list(blk))

# --- estructura vs valor: val vs n_descendientes ---
ch = {}
for _, r in K.iterrows():
    if pd.notna(r['padre']):
        ch.setdefault(r['padre'], []).append(r['cuerda'])
def ndesc(name):
    n = 0
    stack = list(ch.get(name, []))
    while stack:
        x = stack.pop(); n += 1; stack += ch.get(x, [])
    return n
K['ndesc'] = K['cuerda'].map(ndesc)
pend2 = K[K.nivel == 0].copy()
corr = np.corrcoef(pend2['ndesc'], pend2['valor'])[0, 1]
print('\n[struct] corr(n_descendientes, valor) colgantes = %.3f' % corr)
corr2 = np.corrcoef(K['ndesc'], K['valor'])[0, 1]
print('          corr(n_descendientes, valor) todas = %.3f' % corr2)
# valor real vs tiene descendientes
print('     colgantes con hijos y valor>0:', int(((pend2['ndesc'] > 0) & (pend2['valor'] > 0)).sum()),
      '| con hijos y valor 0:', int(((pend2['ndesc'] > 0) & (pend2['valor'] == 0)).sum()))
