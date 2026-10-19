"""UR231: aritmetica estricta sin ceros + nulos intra-grupo.
Regla del brief: 0 sin nudos = valor ausente, no cero. Por tanto una ventana de
sumandos solo es valida si TODAS las cuerdas tienen nudos y valor >0.
"""
import pandas as pd, numpy as np, json
from collections import Counter

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
RNG = np.random.default_rng(0)
NPERM = 1000

u = pd.read_csv(OUT + 'cuerdas_enriquecidas.csv')
pend = u[u.nivel == 0].sort_values(['grupo', 'idx']).reset_index(drop=True)
vals = pend.v.fillna(0).to_numpy(float)
names = pend.cuerda.to_numpy()
groups = [(gid, int(d.index[0]), int(d.index[-1])) for gid, d in pend.groupby('grupo')]

def rels(v, maxlen=5, adjacency=False, collect=False):
    out = []
    for gid, a, b in groups:
        seg = v[a:b + 1]; L = len(seg)
        for i in range(L):
            if seg[i] <= 0: continue
            s = 0.0
            for j in range(i, min(i + maxlen, L)):
                if seg[j] <= 0: break          # solo cuerdas con valor
                s += seg[j]
                if j == i: continue
                cand = ([i - 1] if i > 0 else []) + ([j + 1] if j + 1 < L else []) if adjacency \
                    else [k for k in range(L) if (k < i or k > j) and seg[k] > 0]
                for k in cand:
                    if seg[k] == s:
                        out.append((gid, names[a + k], float(s), i, j, list(map(float, seg[i:j + 1])),
                                    'ady' if adjacency else 'grupo'))
    return out if collect else len(out)

obs_a = rels(vals, 5, True, True)
obs_g = rels(vals, 5, False, True)
print('ESTRICTAS adyacentes (todas >0):', len(obs_a))
for r in obs_a: print('  g%d %s = %.0f  idx %d-%d' % r[:5], r[5])
print('MISMO GRUPO cualquier posicion (todas >0):', len(obs_g), 'cuerdas', len(set(r[1] for r in obs_g)))
print('por grupo:', dict(sorted(Counter(r[0] for r in obs_g).items())))
print('primeras 25:')
for r in obs_g[:25]: print('  g%d %s = %.0f  idx %d-%d' % r[:5], r[5])

def null_intra(v):
    vp = v.copy()
    for gid, a, b in groups:
        idx = np.arange(a, b + 1); nz = idx[vp[idx] > 0]
        vp[nz] = RNG.permutation(vp[nz])
    return vp

na, ng = [], []
for it in range(NPERM):
    vp = null_intra(vals)
    na.append(rels(vp, 5, True)); ng.append(rels(vp, 5, False))
na, ng = np.array(na), np.array(ng)
res = {}
for k, o, arr in [('adyacente', len(obs_a), na), ('mismo_grupo', len(obs_g), ng)]:
    p = (1 + (arr >= o).sum()) / (1 + NPERM)
    res[k] = dict(obs=o, null_mean=round(float(arr.mean()), 2), null_sd=round(float(arr.std()), 2),
                  p=float(p), z=round(float((o - arr.mean()) / arr.std()), 2))
print(json.dumps(res, indent=1))
json.dump(res, open(OUT + 'aritmetica_sin_ceros.json', 'w'), indent=1)

# Grupo 77 en detalle
print('\nGRUPO 77:')
print(u[u.grupo == 77][['cuerda', 'valor', 'nudos', 'color', 'union', 'largo']].to_string(index=False))
