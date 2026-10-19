"""UR231: aritmetica interna y controles nulos.

Nulo principal: barajar los 227 valores (no nulos) entre las 864 posiciones de
colgante del quipu, conservando estructura de grupos, colores y ceros.
1000 permutaciones, semilla 0.
"""
import pandas as pd, numpy as np, json

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
RNG = np.random.default_rng(0)
NPERM = 1000

u = pd.read_csv(OUT + 'cuerdas_enriquecidas.csv')
pend = u[u.nivel == 0].sort_values(['grupo', 'idx']).reset_index(drop=True)
vals = pend.v.fillna(0).to_numpy(float)
n = len(vals)
groups = [(gid, int(d.index[0]), int(d.index[-1])) for gid, d in pend.groupby('grupo')]
print('colgantes', n, 'valores>0', (vals > 0).sum(), 'total', vals.sum())

def within_group(v, maxlen=5, adjacency=False):
    rels, cords = 0, set()
    for gid, a, b in groups:
        seg = v[a:b + 1]; L = len(seg)
        for i in range(L):
            s = 0.0
            for j in range(i, min(i + maxlen, L)):
                if j == i:
                    continue
                s = seg[i:j + 1].sum()
                if s <= 0:
                    continue
                cand = ([i - 1] if i > 0 else []) + ([j + 1] if j + 1 < L else []) if adjacency \
                    else [k for k in range(L) if k < i or k > j]
                for k in cand:
                    if seg[k] == s:
                        rels += 1; cords.add((gid, k))
    return rels, len(cords)

def global_short(v, maxlen=6):
    """Tipo KFG pero solo ventanas de 2..6 cuerdas: toda ventana contigua y toda
    cuerda con ese valor fuera de la ventana."""
    rels, cords = 0, set()
    pos = {}
    for i, x in enumerate(v):
        if x > 0:
            pos.setdefault(x, []).append(i)
    for i in range(n):
        s = 0.0
        for j in range(i, min(i + maxlen, n)):
            s += v[j]
            if j == i or s <= 0:
                continue
            for k in pos.get(s, ()):
                if k < i or k > j:
                    rels += 1; cords.add(k)
    return rels, len(cords)

scans = {'estricta_adyacente': lambda v: within_group(v, 5, True),
         'mismo_grupo_cualquier_pos': lambda v: within_group(v, 5, False),
         'global_ventana_2a6': lambda v: global_short(v, 6)}
obs = {k: f(vals) for k, f in scans.items()}
print('observado (relaciones, cuerdas):', obs)

null = {k: [] for k in scans}
for it in range(NPERM):
    vp = vals.copy(); nz = np.flatnonzero(vp > 0)
    vp[nz] = RNG.permutation(vp[nz])
    for k, f in scans.items():
        null[k].append(f(vp)[0])
    if (it + 1) % 250 == 0: print('perm', it + 1, flush=True)

res = {}
for k in scans:
    arr = np.array(null[k]); o = obs[k][0]
    res[k] = dict(obs=o, obs_cuerdas=obs[k][1], null_mean=round(float(arr.mean()), 2),
                  null_sd=round(float(arr.std()), 2), null_p95=float(np.percentile(arr, 95)),
                  p=(1 + (arr >= o).sum()) / (1 + NPERM),
                  z=round(float((o - arr.mean()) / arr.std()), 2) if arr.std() > 0 else None)
print(json.dumps(res, indent=1, ensure_ascii=False))
json.dump(res, open(OUT + 'aritmetica_nulos.json', 'w'), indent=1, ensure_ascii=False)
np.save(OUT + 'nulo_global.npy', np.array(null['global_ventana_2a6']))
