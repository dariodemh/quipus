"""Puntúa todos los quipus contra todas las variantes congeladas (salvo P6b, en 03_p6b.py).
Salida: obs_perm.csv (kfg, plantilla, estadistico, p_perm, B). Uso: python 02_puntuar.py [kfg ...]"""
import sys, pickle, numpy as np, pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import plantillas as T

OUT = Path(__file__).resolve().parent
DAT = pickle.load(open(OUT / 'datos.pkl', 'rb'))
K = DAT['K']
STAGES = [199, 1999, 19999, 99999]
CAP_LENTO = 19999          # tope para estadísticos con bucle en Python
CHUNK = 2000

def corpus_pmf():
    v = np.concatenate([k['vals'] for k in K.values()]); v = v[~np.isnan(v)]
    return np.bincount(T.hbin(v), minlength=10) / len(v)

def seq_p(obs, gen, f, rng, cap):
    """p secuencial de Monte Carlo: gen(rng, B) -> matriz B×n; f -> estadísticos."""
    p, B = 1.0, 0
    for B in STAGES:
        if B > cap: break
        ge = 0
        for s in range(0, B, CHUNK):
            b = min(CHUNK, B - s)
            ge += int(np.sum(f(gen(rng, b)) >= obs - 1e-12))
        p = (1 + ge) / (1 + B)
        if p > 10 / B: break
    return p, B

def perm_rows(x, rng, B):
    return rng.permuted(np.tile(x, (B, 1)), axis=1)

def score(kfg):
    k = K[kfg]; rng = np.random.default_rng(abs(hash(('20261018', kfg))) % 2**32)
    rng = np.random.default_rng([20261018, sum(map(ord, kfg)) * 7919 + len(kfg)])
    rows = []
    vals = k['vals']; anud = ~np.isnan(vals); V = vals[anud]
    ccodes = pd.factorize(k['col'])[0]
    def add(name, obs, p=np.nan, B=0):
        rows.append(dict(kfg=kfg, plantilla=name, estadistico=float(obs), p_perm=p, B=B))
    genV = lambda r, B: perm_rows(V, r, B)
    def genVfull(r, B):
        X = np.tile(vals, (B, 1)); X[:, anud] = perm_rows(V, r, B); return X
    genC = lambda r, B: perm_rows(ccodes, r, B)
    # --- ventanas sobre V ---
    for name, f in [('P1a', T.P1a), ('P1b', T.P1b), ('P1c', T.P1c), ('P2', T.P2), ('P7c', T.P7c),
                    ('P8b', T.P8b), ('P8c', T.P8c)]:
        o = f(V[None, :]) if len(V) else None
        if o is not None:
            add(name, o[0], *seq_p(o[0], genV, f, rng, STAGES[-1]))
    # P1d: sumas de grupo
    g = k['grp'][anud]
    ug = pd.unique(g)
    if len(ug) >= 10:
        oh = (g[:, None] == ug[None, :]).astype(float)
        f = lambda X: T.P1d(X, oh)
        o = f(V[None, :]); add('P1d', o[0], *seq_p(o[0], genV, f, rng, STAGES[-1]))
    # composición
    o = T.P3(vals, PMF)
    if o is not None: add('P3', o)
    o = T.P12(vals, k['s1'])
    if o is not None: add('P12', o)
    # grupos sobre valores completos
    for name, prep, f, cap in [('P5a', T.P5a_prep, T.P5a, STAGES[-1]), ('P5b', T.P5b_prep, T.P5b, CAP_LENTO),
                               ('P5c', T.P5c_prep, T.P5c, CAP_LENTO), ('P6a', T.P6a_prep, T.P6a, CAP_LENTO),
                               ('P7a', T.P7a_prep, T.P7a, STAGES[-1]), ('P7b', T.P7b_prep, T.P7b, STAGES[-1]),
                               ('P11c', T.P11c_prep, T.P11c, CAP_LENTO)]:
        pr = prep(k)
        if pr is None: continue
        ff = (lambda X, pr=pr, f=f: f(X, pr))
        o = ff(vals[None, :])[0]
        add(name, o, *seq_p(o, genVfull, ff, rng, cap))
    # colores
    if T.P4r_prep(k):
        o = T.P4r(ccodes[None, :])[0]
        add('P4r', o, *seq_p(o, genC, T.P4r, rng, CAP_LENTO))
    o = T.P9a(ccodes[None, :])
    if o is not None: add('P9a', o[0], *seq_p(o[0], genC, T.P9a, rng, STAGES[-1]))
    pos = anud & (np.nan_to_num(vals) > 0)
    cp = ccodes[pos]
    o = T.P10(cp[None, :])
    if o is not None:
        add('P10', o[0], *seq_p(o[0], lambda r, B: perm_rows(cp, r, B), T.P10, rng, CAP_LENTO))
    pr = T.P11_prep(k)
    if pr is not None:
        for name, mk in [('P11a', False), ('P11b', True)]:
            ff = (lambda C, mk=mk: T.P11(C, pr, mk)); o = ff(ccodes[None, :])[0]
            add(name, o, *seq_p(o, genC, ff, rng, CAP_LENTO))
    # P8a: cortes aleatorios
    o, null = T.P8ar_obs_null(k, 1999, rng)
    if o is not None:
        p = (1 + np.sum(null >= o)) / 2000
        if p <= 10 / 1999:
            o2, null = T.P8ar_obs_null(k, 19999, rng); p = (1 + np.sum(null >= o)) / 20000; add('P8ar', o, p, 19999)
        else:
            add('P8ar', o, p, 1999)
    # P9b: conteos
    for name, hit in T.P9b(k).items():
        add(name, float(hit))
    return rows

def _init():
    global PMF
    PMF = corpus_pmf()
PMF = corpus_pmf()

if __name__ == '__main__':
    ks = sys.argv[1:] or sorted(K)
    rows = []
    with ProcessPoolExecutor(max_workers=8, initializer=_init) as ex:
        for i, r in enumerate(ex.map(score, ks, chunksize=2)):
            rows += r
            if i % 50 == 0: print(i, ks[i], flush=True)
    out = pd.DataFrame(rows)
    fn = 'obs_perm.csv' if not sys.argv[1:] else 'obs_perm_prueba.csv'
    out.to_csv(OUT / fn, index=False)
    print(out.groupby('plantilla').size())
