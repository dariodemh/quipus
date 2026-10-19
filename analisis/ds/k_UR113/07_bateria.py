# -*- coding: utf-8 -*-
"""UR113: bateria final de pruebas con filtros anti-triviales y nulos (500 perm., semilla 0)."""
import pandas as pd, numpy as np, os
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv')); u['valor'] = u.valor.fillna(0)
p = u[u.nivel == 0].copy(); s = u[u.nivel > 0].copy()
N = 500

# --- A. madre = suma de >=2 hijas
h = s.groupby('padre').agg(sumh=('valor', 'sum'), nh=('valor', 'size'))
m = p.merge(h, left_on='cuerda', right_index=True).fillna({'sumh': 0, 'nh': 0})
m = m[(m.nh >= 2) & (m.valor > 0)].copy()
print('A. madre=suma de >=2 hijas, valor>0: n =', len(m))
def hitsA(d, ssum):
    return int((d.valor.values == d.cuerda.map(ssum).fillna(-1).values).sum())
obs = hitsA(m, h.sumh)
null = []
for _ in range(N):
    perm = rng.permutation(s.valor.values)
    sg = pd.Series(perm, index=s.index).groupby(s.padre.values).sum()
    null.append(hitsA(m, sg))
null = np.array(null)
print('   exactas', obs, '| nulo media', round(null.mean(), 2), 'max', null.max(),
      '| p =', round((np.sum(null >= obs) + 1) / (N + 1), 4))
print('   cuerdas exactas:', list(m.cuerda[m.valor.values == m.cuerda.map(h.sumh).fillna(-1).values]))

# --- B/C. corridas contiguas no triviales (>=2 sumandos >0, objetivo >=3)
gi_arr = p.grupo.values; v = p.valor.values; col = p.color.fillna('NA').values; name = p.cuerda.values
groups = [(g, np.where(gi_arr == g)[0]) for g in pd.unique(gi_arr)]
def scan(vals, colors, gidx, mono=False, maxlen=10):
    out = []
    for g, idx in gidx:
        w = vals[idx]; c = colors[idx]
        cs = np.concatenate([[0], np.cumsum(w)])
        nz = np.concatenate([[0], np.cumsum(w > 0)])
        for i in range(2, len(w)):
            if w[i] < 3: continue
            for k in range(2, min(maxlen, i) + 1):
                if nz[i] - nz[i - k] < 2: continue
                if mono and len(set(c[i - k:i])) > 1: continue
                if abs((cs[i] - cs[i - k]) - w[i]) < 0.5:
                    out.append((g, name[idx[i]], int(w[i]), k, tuple(int(x) for x in w[i - k:i])))
                    break
    return out
obsB = scan(v, col, groups); obsC = scan(v, col, groups, True)
print('\nB. corrida contigua no trivial:', len(obsB))
for x in obsB: print('   ', x)
def nullB(mono=False, n=200):
    r = []
    for _ in range(n):
        pv = rng.permutation(v)
        r.append(len(scan(pv, col, groups, mono)))
    return np.array(r)
nb = nullB(False); nc = nullB(True)
print('   nulo B: media', round(nb.mean(), 2), 'max', nb.max(), 'p', round((np.sum(nb >= len(obsB)) + 1) / (len(nb) + 1), 4))
print('C. monocroma:', len(obsC), '| nulo media', round(nc.mean(), 2), 'max', nc.max(),
      'p', round((np.sum(nc >= len(obsC)) + 1) / (len(nc) + 1), 4))

# --- D. totales de grupo identicos
gt = p.groupby('grupo').valor.sum()
pairs = int(sum(c * (c - 1) // 2 for c in gt.value_counts()))
def nullD(n=500):
    out = []
    for _ in range(n):
        g2 = pd.Series(rng.permutation(v)).groupby(gi_arr).sum()
        out.append(sum(c * (c - 1) // 2 for c in g2.round().value_counts()))
    return np.array(out)
nd = nullD()
print('\nD. pares de grupos con total identico: obs', pairs, '| nulo media', round(nd.mean(), 2),
      'max', nd.max(), 'p', round((np.sum(nd >= pairs) + 1) / 501, 4))
print('   iguales:', {int(k): int(c) for k, c in gt.value_counts()[gt.value_counts() > 1].items()})
print('\nE. total colgantes', int(p.valor.sum()), '; total todas', int(u.valor.sum()))
