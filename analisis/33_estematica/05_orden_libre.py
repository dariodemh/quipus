"""33 · POST HOC (no estaba en el diseño congelado). Prueba sin orden para «versiones» que comparten
cabeceras con desglose distinto (UR256/UR267B, UR266/UR275), que la medida multibloque no ve porque
cada tramo compartido tiene 2 cuerdas (< τ).
Estadístico K(A,B) = n.º de valores distintos ≥ 100 presentes en A y en B (exactos).
Nulo de reemplazo: K(A,X) para quipus X de otra procedencia conocida (o, si A no la tiene, de otro
museo), de tamaño entre 0,5 y 2 veces el de B; p_A = rango. Igual cambiando los papeles; p = máx.
Si K(A,B) supera a todos los comparadores, la cola se extrapola con una binomial negativa (o Poisson)
ajustada por momentos a los K de los comparadores.
Orden (independiente de K): posiciones (primera aparición) de los K valores compartidos en A y en B;
L = máx(subsecuencia creciente, decreciente) más larga; p_orden = P(L' ≥ L) bajo permutación al azar
(20 000 simulaciones por K). Detecta «resumen/índice»: los valores de A reaparecen EN ORDEN en B,
espaciados (cabeceras de secciones), que el alineamiento con huecos no ve.
Familia: todos los pares con K ≥ 3; BH sobre esa familia. Salida: orden_libre.csv, salida_05.txt"""
import os

import numpy as np
import pandas as pd
from scipy import sparse, stats

from comun import OUT, RAIZ, bh, preparar

def lis(x):
    import bisect
    t = []
    for v in x:
        i = bisect.bisect_left(t, v)
        t[i:i + 1] = [v]
    return len(t)


_CACHE = {}


def p_orden(k, L, rng):
    if k not in _CACHE:
        sims = np.array([max(lis(p), lis(-p)) for p in (rng.permutation(k) for _ in range(20000))])
        _CACHE[k] = sims
    return (np.sum(_CACHE[k] >= L) + 1) / (len(_CACHE[k]) + 1)


DESC = {'Unknown', 'unknown', 'Peru', 'South Peru', 'Aankoop', ''}


def main():
    D = preparar()
    ids = np.array(D['ids'])
    q = pd.read_csv(os.path.join(RAIZ, 'analisis/datos/quipus.csv')).set_index('kfg')
    proc = q.procedencia.reindex(ids).fillna('Unknown').values
    mus = q.museo.reindex(ids).fillna('').values
    n = np.array([len(D['seqs'][k]) for k in ids])
    vals = [set(D['seqs'][k].v[D['seqs'][k].v >= 100].tolist()) for k in ids]
    vocab = {v: x for x, v in enumerate(sorted(set().union(*vals)))}
    r, c = zip(*[(i, vocab[v]) for i, s in enumerate(vals) for v in s])
    X = sparse.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(ids), len(vocab)))
    K = (X @ X.T).toarray().astype(int)
    np.fill_diagonal(K, 0)
    pi, pj = np.where(np.triu(K >= 3, 1))

    def p_lado(a, b):
        conoc = ~np.isin(proc, list(DESC))
        ok = conoc & (proc != proc[a]) & (proc != proc[b]) if proc[a] not in DESC else conoc & (mus != mus[a])
        ok &= (n >= .5 * n[b]) & (n <= 2 * n[b])
        ok[[a, b]] = False
        comp = K[a, ok]
        k = K[a, b]
        pe = (np.sum(comp >= k) + 1) / (len(comp) + 1)
        m, v = comp.mean() + .5 / len(comp), comp.var(ddof=1) + .5 / len(comp)   # suavizado: nunca 0
        if v > m:                                   # binomial negativa por momentos (sobredispersión)
            r_ = m * m / (v - m)
            pp = stats.nbinom.sf(k - 1, r_, r_ / (r_ + m))
        else:
            pp = stats.poisson.sf(k - 1, m)
        return max(min(pe, pp), 1e-300) if pe <= 2 / (len(comp) + 1) else pe, len(comp)
    rng = np.random.default_rng(20261033)
    pos = [{v: i for i, v in reversed(list(enumerate(D['seqs'][k].v.tolist())))} for k in ids]
    filas = []
    for a, b in zip(pi, pj):
        comunes = sorted(vals[a] & vals[b], key=lambda v: pos[a][v])
        orden_b = np.array([pos[b][v] for v in comunes])
        L = max(lis(orden_b), lis(-orden_b))
        pa, na = p_lado(a, b)
        pb, nb = p_lado(b, a)
        filas.append(dict(A=ids[a], B=ids[b], K=K[a, b], nA=n[a], nB=n[b], p=max(pa, pb), n_comp=min(na, nb), L_orden=L,
                          p_orden=p_orden(len(comunes), L, rng),
                          procA=proc[a], procB=proc[b]))
    f = pd.DataFrame(filas)
    f['q'] = bh(f.p.values)
    f['q_orden'] = bh(f.p_orden.values)
    f['p_comb'] = [stats.combine_pvalues([x, y], method='fisher')[1] for x, y in zip(f.p, f.p_orden)]
    f['q_comb'] = bh(f.p_comb.values)
    f = f.sort_values('p_comb')
    f.to_csv(os.path.join(OUT, 'orden_libre.csv'), index=False, float_format='%.3g')
    txt = f'pares con K>=3: {len(f)}; q<0,05: {(f.q < .05).sum()}\n' + f.head(40).to_string()
    open(os.path.join(OUT, 'salida_05.txt'), 'w', encoding='utf-8').write(txt)
    print(txt)


if __name__ == '__main__':
    main()
