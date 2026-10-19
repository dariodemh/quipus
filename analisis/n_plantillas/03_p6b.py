"""P6b: suma de secciones de k = ventana de colgantes de otro quipu j del mismo hallazgo.
Hallazgo = misma procedencia conocida o misma región conocida (revisión de clave, plantillas.md §3).
Nulo: permutar los valores de k (cuerdas anudadas) y recalcular el máximo sobre TODOS los j.
Salida: p6b.csv. Uso: python 03_p6b.py [kfg ...]"""
import sys, pickle, numpy as np, pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from numpy.lib.stride_tricks import sliding_window_view as sw
import plantillas as T

OUT = Path(__file__).resolve().parent
DAT = pickle.load(open(OUT / 'datos.pkl', 'rb')); K = DAT['K']; meta = DAT['meta']
MALO = {'Unknown', 'unknown', 'Peru', ''}

def socios(k):
    if k not in meta.index: return []
    p, r = meta.loc[k, 'procedencia'], meta.loc[k, 'region']
    out = []
    for j in K:
        if j == k or j not in meta.index: continue
        if (p not in MALO and meta.loc[j, 'procedencia'] == p) or (r not in MALO and meta.loc[j, 'region'] == r):
            out.append(j)
    return out

def plan(k):
    """lista de (L, matriz de índices de secciones a sumar: S = sum over blocks)."""
    G = T.groups(k); n = len(k['vals'])
    sz = [len(x) for x in G if len(x) >= 3]
    if not sz: return []
    m = max(set(sz), key=sz.count)
    starts = [x[0] for x in G]
    P = []
    for t in range(1, 7):
        L = m * t
        if not 4 <= L <= 40: continue
        for o in starts:
            nb = (n - o) // L
            if nb < 2: continue
            blocks = [np.arange(o + i * L, o + (i + 1) * L) for i in range(nb)]
            runs = set()
            for r in (2, 3):
                for i in range(nb - r + 1): runs.add((i, r))
            runs.add((0, nb))
            for i, r in runs: P.append((L, np.stack(blocks[i:i + r])))
    return P

def stat(v0, P, W):
    """v0: valores de k con ausentes = 0. W: {L: [ventanas de cada j]} -> max coincidencias."""
    best = 0
    byL = {}
    for L, idx in P: byL.setdefault(L, []).append(v0[idx].sum(0))
    for L, Ss in byL.items():
        S = np.unique(np.stack(Ss), axis=0)
        for Wj in W.get(L, []):
            hit = ((S[:, None, :] == Wj[None, :, :]) & (S[:, None, :] >= 1)).sum(-1)
            best = max(best, int(hit.max()))
    return best

def run(kfg):
    k = K[kfg]; js = socios(kfg); P = plan(k)
    if not js or not P: return None
    W = {}
    for L in {L for L, _ in P}:
        for j in js:
            vj = np.nan_to_num(K[j]['vals'])
            if len(vj) >= L: W.setdefault(L, []).append(sw(vj, L))
    v0 = np.nan_to_num(k['vals']); an = ~np.isnan(k['vals'])
    obs = stat(v0, P, W)
    rng = np.random.default_rng([20261018, sum(map(ord, kfg))])
    p, B = 1.0, 0
    for B in (199, 1999):
        ge = 0
        for _ in range(B):
            v = v0.copy(); v[an] = rng.permutation(v0[an])
            ge += stat(v, P, W) >= obs
        p = (1 + ge) / (1 + B)
        if p > 10 / B: break
    return dict(kfg=kfg, plantilla='P6b', estadistico=obs, p_perm=p, B=B, n_socios=len(js))

if __name__ == '__main__':
    ks = sys.argv[1:] or sorted(K)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = [r for r in ex.map(run, ks) if r]
    d = pd.DataFrame(rows)
    d.to_csv(OUT / ('p6b.csv' if not sys.argv[1:] else 'p6b_prueba.csv'), index=False)
    print(d.to_string())
