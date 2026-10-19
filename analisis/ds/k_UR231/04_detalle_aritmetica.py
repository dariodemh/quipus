"""UR231: detalle de las sumas estrictas y nulo alternativo intra-grupo."""
import pandas as pd, numpy as np, json

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
RNG = np.random.default_rng(0)
NPERM = 1000

u = pd.read_csv(OUT + 'cuerdas_enriquecidas.csv')
pend = u[u.nivel == 0].sort_values(['grupo', 'idx']).reset_index(drop=True)
vals = pend.v.fillna(0).to_numpy(float)
names = pend.cuerda.to_numpy()
n = len(vals)
groups = [(gid, int(d.index[0]), int(d.index[-1])) for gid, d in pend.groupby('grupo')]

def strict(v, maxlen=5):
    out = []
    for gid, a, b in groups:
        seg = v[a:b + 1]; L = len(seg)
        for i in range(L):
            for j in range(i + 1, min(i + maxlen, L)):
                s = seg[i:j + 1].sum()
                if s <= 0: continue
                for k, side in ([(i - 1, 'izq')] if i > 0 else []) + ([(j + 1, 'der')] if j + 1 < L else []):
                    if seg[k] == s:
                        out.append((gid, names[a + k], float(s), side, i, j, list(map(float, seg[i:j + 1]))))
    return out

obs = strict(vals)
print('sumas estrictas (adyacentes, mismo grupo, ventana 2-5):', len(obs))
for r in obs:
    print(f'  g{r[0]:>2} {r[1]:>7} = {r[2]:.0f}  ({r[3]}, idx {r[4]}-{r[5]})  sumandos {r[6]}')

# nulo intra-grupo: permutar valores >0 dentro de cada grupo
def count_strict(v):
    return len(strict(v))

null = []
for it in range(NPERM):
    vp = vals.copy()
    for gid, a, b in groups:
        idx = np.arange(a, b + 1)
        nz = idx[vp[idx] > 0]
        vp[nz] = RNG.permutation(vp[nz])
    null.append(count_strict(vp))
null = np.array(null)
p = (1 + (null >= len(obs)).sum()) / (1 + NPERM)
print('\nNulo intra-grupo: media %.2f sd %.2f p95 %.0f  p=%.4f' % (null.mean(), null.std(), np.percentile(null, 95), p))
json.dump(dict(obs=len(obs), null_mean=float(null.mean()), null_sd=float(null.std()),
               p=float(p), sum_cords=int(len(set(r[1] for r in obs)))),
          open(OUT + 'sumas_estrictas_intragrupo.json', 'w'), indent=1)

# reparto por grupo y longitud de ventana
from collections import Counter
print('por grupo:', Counter(r[0] for r in obs))
print('por longitud:', Counter(r[5] - r[4] + 1 for r in obs))
print('cuerdas suma distintas:', sorted(set(r[1] for r in obs)))
