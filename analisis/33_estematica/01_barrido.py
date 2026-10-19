"""33 · Barrido de todos los pares: medida multibloque, nulo por nivel con Monte Carlo secuencial
(etapa 0: 9 permutaciones a TODOS los pares; siguen solo los que superan las 9 -> 99 -> 999; cola de
Gumbel), Holm/BH sobre todos los pares. La huella de valores (diseño §3) queda como columna de
diagnóstico (adenda: perdía 7 de los 25 pares de 04).
Uso: python 01_barrido.py --mitad E     (solo pares E–E; fase de exploración)
     python 01_barrido.py               (todos los pares; fase congelada)
Salidas: barrido_<fase>.csv.gz (todos los pares), division.csv, salida_01_<fase>.txt."""
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy import sparse

from comun import (ESCALAS, GAP, KMAX, OUT, RAIZ, SEED, TAU, bh, evaluar_pares, p_valor, preparar)

N0, N1, N2 = 9, 99, 999


def division(ids):
    q = pd.read_csv(os.path.join(RAIZ, 'analisis/datos/quipus.csv')).set_index('kfg')
    proc = q.procedencia.reindex(ids).fillna('Unknown').values
    rng = np.random.default_rng(SEED)
    lado = {}
    for p in sorted(set(proc)):
        m = sorted(k for k, x in zip(ids, proc) if x == p)
        m = [m[i] for i in rng.permutation(len(m))]
        for t, k in enumerate(m):
            lado[k] = 'E' if t < len(m) // 2 or (len(m) % 2 and t == len(m) // 2 and rng.random() < .5) else 'C'
    return pd.Series(lado).reindex(ids)


def prefiltro(D, ids):
    """H_k(i,j) = sum idf(v) sobre valores distintos >=10 en i y en k*j; max sobre k."""
    vals = [set(D['seqs'][k].v.values.tolist()) for k in ids]
    vocab = sorted({v for s in vals for v in s if v >= 10})
    col = {v: x for x, v in enumerate(vocab)}
    df = np.zeros(len(vocab))
    rows, cols = [], []
    for i, s in enumerate(vals):
        for v in s:
            if v in col:
                rows.append(i); cols.append(col[v]); df[col[v]] += 1
    X = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(ids), len(vocab)))
    idf = np.log2(len(ids) / df)
    XW = X @ sparse.diags(idf)
    best = np.zeros((len(ids), len(ids)))
    for k in ESCALAS:
        r, c = [], []
        for j, s in enumerate(vals):
            for v in s:
                w = v * int(round(k)) if k >= 1 else (v // int(round(1 / k)) if v % int(round(1 / k)) == 0 else None)
                if w is not None and w in col:
                    r.append(j); c.append(col[w])
        Xk = sparse.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(ids), len(vocab)))
        best = np.maximum(best, (XW @ Xk.T).toarray())
    return best


def main():
    fase = 'E' if '--mitad' in sys.argv else 'todo'
    t0 = time.time()
    D = preparar()
    ids = np.array(D['ids'])
    nq = len(ids)
    lado = division(ids)
    lado.rename('mitad').to_frame().to_csv(os.path.join(OUT, 'division.csv'), index_label='kfg')
    pi, pj = [x.astype(np.int64) for x in np.triu_indices(nq, 1)]
    NPARES = len(pi)
    H = prefiltro(D, ids)
    h = H[pi, pj]
    log = [f'quipus {nq}; pares {NPARES}']
    if fase == 'E':
        e = lado.values == 'E'
        sel = np.where(e[pi] & e[pj])[0]
        log.append(f'FASE E: pares E–E {len(sel)}')
    else:
        sel = np.arange(NPARES)
    sel = sel[np.random.default_rng(SEED).permutation(len(sel))]  # reparte la carga entre hilos
    npares_fase = len(sel)
    a, b = pi[sel], pj[sel]
    o, kb, n0 = evaluar_pares(D['V'], D['LV'], D['off'], a, b, N0, SEED, ESCALAS, GAP, TAU, KMAX, 0)
    b0 = (n0 >= o[:, None]).sum(1)
    nul = [n0[x] for x in range(len(a))]
    log.append(f'etapa 0 ({N0} perm. a {len(a)} pares): {time.time() - t0:.0f} s; siguen {int((b0 == 0).sum())}')
    for etapa, (NN, sd) in enumerate(((N1, SEED + 1), (N2, SEED + 2))):
        bb = np.array([(nul[x] >= o[x]).sum() for x in range(len(a))])
        top = np.where(bb == 0)[0] if etapa == 0 else np.where((bb <= 1) & (np.array([len(v) for v in nul]) > N0))[0]
        if len(top) == 0:
            continue
        _, _, nn = evaluar_pares(D['V'], D['LV'], D['off'], a[top], b[top], NN, sd, ESCALAS, GAP, TAU, KMAX, 0)
        for t, x in enumerate(top):
            nul[x] = np.concatenate((nul[x], nn[t]))
        log.append(f'etapa {etapa + 1} ({NN} perm. a {len(top)} pares): {time.time() - t0:.0f} s')
    p = np.ones(len(a)); pe = np.ones(len(a)); nperm = np.zeros(len(a), int)
    for x in range(len(a)):
        p[x], pe[x] = [float(v[0]) for v in p_valor(np.array([o[x]]), nul[x][None, :])]
        nperm[x] = len(nul[x])
    # Holm y BH sobre TODOS los pares de la fase (Monte Carlo secuencial)
    pall = p
    q = bh(pall)
    orden = np.argsort(pall)
    holm = np.empty(npares_fase)
    holm[orden] = np.minimum(1, np.maximum.accumulate(pall[orden] * (npares_fase - np.arange(npares_fase))))
    r = pd.DataFrame(dict(A=ids[a], B=ids[b], nA=np.diff(D['off'])[a], nB=np.diff(D['off'])[b], huella=h[sel],
                          score=o, escala=ESCALAS[kb], null_media=[x.mean() for x in nul],
                          null_max=[x.max() for x in nul], nperm=nperm, p=p, p_emp=pe, q=q, holm=holm,
                          mitadA=lado.values[a], mitadB=lado.values[b]))
    r = r.sort_values('p')
    r.attrs = {}
    r.to_csv(os.path.join(OUT, f'barrido_{fase}.csv.gz'), index=False, float_format='%.4g')
    log.append(f'q<0,05: {(r.q < .05).sum()}  Holm<0,05: {(r.holm < .05).sum()}  q<0,20: {(r.q < .2).sum()}')
    log.append(r.head(60).to_string())
    open(os.path.join(OUT, f'salida_01_{fase}.txt'), 'w', encoding='utf-8').write('\n'.join(log))
    print('\n'.join(log[:8]))


if __name__ == '__main__':
    main()
