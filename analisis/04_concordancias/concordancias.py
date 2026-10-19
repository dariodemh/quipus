"""Concordancias entre quipus: cuasi-duplicados (tarea 1) y relaciones de resumen (tarea 2).

Uso:  python analisis/04_concordancias/concordancias.py          (cálculo completo, ~5-10 min)
      python analisis/04_concordancias/concordancias.py --demo   (autocomprobación)
Salidas en analisis/04_concordancias/resultados/.

Método (detalle en informe.md):
- Secuencia de un quipu = valores de las cuerdas con nudos (todas las jerarquías) en `orden`;
  las cuerdas sin nudos (ausentes) se ignoran.
- Puntuación = alineamiento local Smith-Waterman (hueco lineal, 5 bits) con puntuaciones log-odds
  en bits: coincidencia exacta log2(0.85/f(v)), tolerante (|a-b| = 10^k: un dígito ±1)
  log2(0.05/t(v)), discordancia log2(0.10/(1-f-t)). f y t son frecuencias en la composición
  conjunta del PAR (así "1-1-1" entre dos quipus llenos de unos puntúa ~0). Ambos sentidos de B.
- Nulo: los dos quipus barajados (conserva la distribución de valores de cada uno). 50
  permutaciones para todos los pares; para p<0.01, 1000 permutaciones simples y 1000 por bloques
  de 5 cuerdas (conserva la autocorrelación local). Si la observación supera todas las
  permutaciones, la cola se extrapola con una Gumbel (Karlin-Altschul). BH-FDR sobre todos los pares.
- Tarea 2: secuencia de totales de grupo de A (grupos con >=2 colgantes anudados) contra la
  secuencia de cuerdas de B; azar = composición de B. Nulo: colgantes de A barajados entre
  posiciones conservando los tamaños de grupo (totales nulos de magnitud realista) y B barajado.
"""
import math
import os
import sys

import numpy as np
import pandas as pd
from numba import njit, prange

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'analisis', '04_concordancias', 'resultados')
SEED = 20261017
GAP = 5.0
GAP_B_SUM = 0.1  # tarea 2: los totales pueden estar dispersos en B (p. ej. 1.a cuerda de cada grupo)
N_PERM_ALL = 50
N_PERM_TOP = 1000


# ---------------------------------------------------------------- alineamiento
@njit(cache=True)
def _cuenta(sv, v):
    return np.searchsorted(sv, v, side='right') - np.searchsorted(sv, v, side='left')


@njit(cache=True)
def _es_tol(d):
    p = 1
    for _ in range(7):
        if d == p:
            return True
        p *= 10
    return False


@njit(cache=True)
def _ft(vals, pool):
    """f(v) y t(v) de cada valor de vals respecto de la composición `pool` (suavizado +0.5)."""
    sv = np.sort(pool)
    n = sv.shape[0]
    f = np.empty(vals.shape[0])
    t = np.empty(vals.shape[0])
    for i in range(vals.shape[0]):
        v = vals[i]
        f[i] = (_cuenta(sv, v) + 0.5) / (n + 1.0)
        c = 0
        p = 1
        for _ in range(7):
            c += _cuenta(sv, v + p) + _cuenta(sv, v - p)
            p *= 10
        t[i] = (c + 0.5) / (n + 1.0)
    return f, t


@njit(cache=True)
def matriz(a, b, fa, ta, fb, tb):
    """Matriz de puntuaciones log-odds (bits)."""
    S = np.empty((a.shape[0], b.shape[0]))
    for i in range(a.shape[0]):
        for j in range(b.shape[0]):
            d = abs(a[i] - b[j])
            if d == 0:
                S[i, j] = math.log2(0.85 / fa[i])
            elif _es_tol(d):
                S[i, j] = math.log2(0.05 / max(ta[i], tb[j]))
            else:
                S[i, j] = math.log2(0.10 / max(1.0 - min(fa[i] + ta[i], fb[j] + tb[j]), 1e-3))
    return S


@njit(cache=True)
def sw_mat(S, gap, rev, gap_b=-1.0):
    """Smith-Waterman local con hueco lineal sobre S (rev: columnas invertidas). Máxima puntuación.
    gap: saltar un elemento de A (filas); gap_b: saltar uno de B (columnas; <0 => igual a gap)."""
    if gap_b < 0:
        gap_b = gap
    m, n = S.shape
    prev = np.zeros(n + 1)
    cur = np.zeros(n + 1)
    best = 0.0
    for i in range(m):
        cur[0] = 0.0
        for j in range(n):
            s = S[i, n - 1 - j] if rev else S[i, j]
            h = prev[j] + s
            if prev[j + 1] - gap > h:
                h = prev[j + 1] - gap
            if cur[j] - gap_b > h:
                h = cur[j] - gap_b
            if h < 0:
                h = 0.0
            cur[j + 1] = h
            if h > best:
                best = h
        for j in range(n + 1):
            prev[j] = cur[j]
    return best


@njit(cache=True)
def matriz_dup(a, b):
    pool = np.concatenate((a, b))
    fa, ta = _ft(a, pool)
    fb, tb = _ft(b, pool)
    return matriz(a, b, fa, ta, fb, tb)


@njit(cache=True)
def matriz_sum(tot, b):
    """Totales de A (filas) contra cuerdas de B (columnas); azar = composición de B."""
    fa, ta = _ft(tot, b)
    fb, tb = _ft(b, b)
    return matriz(tot, b, fa, ta, fb, tb)


@njit(cache=True)
def score_dup(a, b, gap):
    S = matriz_dup(a, b)
    return max(sw_mat(S, gap, False), sw_mat(S, gap, True))


@njit(cache=True)
def score_sum(tot, b, gap):
    S = matriz_sum(tot, b)
    return max(sw_mat(S, gap, False, GAP_B_SUM), sw_mat(S, gap, True, GAP_B_SUM))


@njit(cache=True)
def barajar(x, block):
    """block<=1: permutación simple. block>1: bloques contiguos de `block` cuerdas con fase
    aleatoria, permutados como unidades (conserva la autocorrelación local)."""
    n = x.shape[0]
    if block <= 1 or n <= block:
        return x[np.random.permutation(n)]
    ph = np.random.randint(0, block)
    starts = [0]
    s = ph if ph > 0 else block
    while s < n:
        starts.append(s)
        s += block
    starts.append(n)
    nb = len(starts) - 1
    order = np.random.permutation(nb)
    out = np.empty_like(x)
    k = 0
    for o in order:
        for u in range(starts[o], starts[o + 1]):
            out[k] = x[u]
            k += 1
    return out


@njit(parallel=True, cache=True)
def todos_los_pares(V, off, pi, pj, nperm, seed, gap, block):
    """Tarea 1. Para cada par: puntuación observada y nperm puntuaciones nulas."""
    K = pi.shape[0]
    obs = np.zeros(K)
    null = np.zeros((K, nperm))
    for k in prange(K):
        a = V[off[pi[k]]:off[pi[k] + 1]]
        b = V[off[pj[k]]:off[pj[k] + 1]]
        obs[k] = score_dup(a, b, gap)
        np.random.seed(seed + k)
        for r in range(nperm):
            null[k, r] = score_dup(barajar(a, block), barajar(b, block), gap)
    return obs, null


@njit(cache=True)
def _totales(vv, gid, ng):
    tot = np.zeros(ng, dtype=np.int64)
    for x in range(vv.shape[0]):
        tot[gid[x]] += vv[x]
    return tot


@njit(parallel=True, cache=True)
def resumen_pares(PV, GID, NG, poff, V, off, pi, pj, nperm, seed, gap, block):
    """Tarea 2. A = pi (totales de sus grupos), B = pj (cuerdas)."""
    K = pi.shape[0]
    obs = np.zeros(K)
    null = np.zeros((K, nperm))
    for k in prange(K):
        i = pi[k]
        pv = PV[poff[i]:poff[i + 1]]
        gid = GID[poff[i]:poff[i + 1]]
        b = V[off[pj[k]]:off[pj[k] + 1]]
        obs[k] = score_sum(_totales(pv, gid, NG[i]), b, gap)
        np.random.seed(seed + k)
        for r in range(nperm):
            tot = _totales(barajar(pv, block), gid, NG[i])
            null[k, r] = score_sum(tot, barajar(b, block), gap)
    return obs, null


@njit(parallel=True, cache=True)
def resumen_orden(PV, GID, NG, poff, V, off, pi, pj, nperm, seed, gap):
    """Tarea 2, nulo de ORDEN: mismos totales de A (misma magnitud y mismas coincidencias sueltas
    posibles) en orden aleatorio; B intacto. Sólo mide si las coincidencias siguen el orden."""
    K = pi.shape[0]
    obs = np.zeros(K)
    null = np.zeros((K, nperm))
    for k in prange(K):
        i = pi[k]
        tot = _totales(PV[poff[i]:poff[i + 1]], GID[poff[i]:poff[i + 1]], NG[i])
        b = V[off[pj[k]]:off[pj[k] + 1]]
        obs[k] = score_sum(tot, b, gap)
        np.random.seed(seed + k)
        for r in range(nperm):
            null[k, r] = score_sum(tot[np.random.permutation(tot.shape[0])], b, gap)
    return obs, null


# ---------------------------------------------------------------- estadística
BETA_MIN = 1 / math.log(2)  # escala de Karlin-Altschul para log-odds en bits (lambda=1)


def p_valor(x, null):
    """p empírico si la observación cae dentro del nulo; si supera todas las permutaciones, cola de
    Gumbel ajustada por momentos (beta con suelo teórico para evitar colas degeneradas)."""
    x = np.asarray(x, float)
    nperm = null.shape[1]
    pe = ((null >= x[:, None]).sum(1) + 1) / (nperm + 1)
    beta = np.maximum(null.std(1, ddof=1) * math.sqrt(6) / math.pi, BETA_MIN)
    loc = null.mean(1) - 0.5772156649 * beta
    with np.errstate(over='ignore'):
        pg = -np.expm1(-np.exp(-(x - loc) / beta))
    p = np.where(null.max(1) < x, np.minimum(pg, pe), pe)
    return p, pe


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    r = p[o] * n / np.arange(1, n + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    out = np.empty(n)
    out[o] = np.minimum(r, 1)
    return out


# ---------------------------------------------------------------- traza (para informes)
def traza(S, gap=GAP, gap_b=None):
    """Smith-Waterman con traceback (Python; sólo pares seleccionados). Devuelve (score, sentido,
    lista de (i, j) alineados; None = hueco), j en el orden original de B."""
    best_all = None
    for rev in (False, True):
        M = S[:, ::-1] if rev else S
        n, m = M.shape
        H = np.zeros((n + 1, m + 1))
        P = np.zeros((n + 1, m + 1), dtype=np.int8)
        for i in range(n):
            for j in range(m):
                opts = (0.0, H[i, j] + M[i, j], H[i, j + 1] - gap, H[i + 1, j] - (gap if gap_b is None else gap_b))
                k = int(np.argmax(opts))
                H[i + 1, j + 1] = opts[k]
                P[i + 1, j + 1] = k
        i, j = np.unravel_index(np.argmax(H), H.shape)
        best = H[i, j]
        path = []
        while i > 0 and j > 0 and P[i, j] != 0:
            k = P[i, j]
            if k == 1:
                path.append((i - 1, j - 1)); i -= 1; j -= 1
            elif k == 2:
                path.append((i - 1, None)); i -= 1
            else:
                path.append((None, j - 1)); j -= 1
        path = path[::-1]
        if rev:
            path = [(x, None if y is None else m - 1 - y) for x, y in path]
        if best_all is None or best > best_all[0]:
            best_all = (best, 'inverso' if rev else 'directo', path)
    return best_all


# ---------------------------------------------------------------- datos
def preparar():
    c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'), low_memory=False)
    c['kn'] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != '') & c.valor.notna()
    c = c.sort_values(['kfg', 'orden'])
    ck = c[c.kn].copy()
    ck['v'] = ck.valor.round().astype(np.int64)
    seqs = {k: g for k, g in ck.groupby('kfg', sort=True) if len(g) >= 3}
    ids = sorted(seqs)
    off = np.cumsum([0] + [len(seqs[k]) for k in ids]).astype(np.int64)
    V = np.concatenate([seqs[k].v.values for k in ids]).astype(np.int64)
    # tarea 2: colgantes (nivel 0) anudados en grupos con >=2 colgantes anudados
    PV, GID, NG, GR = [], [], [], []
    for k in ids:
        p = seqs[k][seqs[k].nivel == 0]
        cnt = p.groupby('grupo').size()
        ok = sorted(cnt[cnt >= 2].index)
        p = p[p.grupo.isin(ok)]
        PV.append(p.v.values)
        GID.append(pd.Categorical(p.grupo, categories=ok).codes.astype(np.int64))
        NG.append(len(ok)); GR.append(ok)
    poff = np.cumsum([0] + [len(x) for x in PV]).astype(np.int64)
    return dict(c=c, seqs=seqs, ids=ids, V=V, off=off, PV=np.concatenate(PV).astype(np.int64),
                GID=np.concatenate(GID), NG=np.array(NG, dtype=np.int64), poff=poff, GR=GR)


def totales_grupo(D, k):
    i = D['ids'].index(k)
    sl = slice(D['poff'][i], D['poff'][i + 1])
    return _totales(D['PV'][sl], D['GID'][sl], D['NG'][i]), D['GR'][i]


def ngram_semillas(ids, seqs, n=3, vmin=10):
    """Preselección por hashing de n-gramas (n=3, todos los valores >= vmin), en ambos sentidos."""
    idx = {}
    for qi, k in enumerate(ids):
        v = seqs[k].v.values
        for s in (v, v[::-1]):
            for x in range(len(s) - n + 1):
                g = tuple(s[x:x + n])
                if min(g) >= vmin:
                    idx.setdefault(g, set()).add(qi)
    pares = set()
    for s in idx.values():
        s = sorted(s)
        for x in range(len(s)):
            for y in range(x + 1, len(s)):
                pares.add((s[x], s[y]))
    return pares


# ---------------------------------------------------------------- principal
def evaluar(fun, args, pi, pj, seed):
    """Etapa 1: 50 permutaciones simples a todos los pares; etapa 2 (p<0.01): 1000 simples +
    1000 por bloques de 5."""
    obs, null = fun(*args, pi, pj, N_PERM_ALL, seed, GAP, 1)
    p, pe = p_valor(obs, null)
    res = pd.DataFrame(dict(score=obs, null_media=null.mean(1), p=p, p_emp=pe, p_bloque=1.0,
                            refinado=False))
    top = np.where(p < 1e-2)[0]
    print('  refinando', len(top), 'pares', flush=True)
    o2, n2 = fun(*args, pi[top], pj[top], N_PERM_TOP, seed + 1, GAP, 1)
    p2, pe2 = p_valor(o2, n2)
    res.loc[top, 'p'] = p2; res.loc[top, 'p_emp'] = pe2; res.loc[top, 'null_media'] = n2.mean(1)
    o3, n3 = fun(*args, pi[top], pj[top], N_PERM_TOP, seed + 2, GAP, 5)
    res.loc[top, 'p_bloque'] = p_valor(o3, n3)[0]
    res.loc[top, 'refinado'] = True
    res['q'] = bh(res.p.values)
    res['q_bloque'] = bh(res.p_bloque.values)  # no refinados: p_bloque=1 (conservador)
    return res


def main():
    os.makedirs(OUT, exist_ok=True)
    D = preparar()
    ids = np.array(D['ids'])
    nq = len(ids)
    L = np.diff(D['off'])
    print('quipus con >=3 cuerdas anudadas:', nq)
    pi, pj = [x.astype(np.int64) for x in np.triu_indices(nq, 1)]
    print('tarea 1: pares', len(pi), flush=True)
    r1 = evaluar(todos_los_pares, (D['V'], D['off']), pi, pj, SEED)
    sem = ngram_semillas(D['ids'], D['seqs'])
    r1.insert(0, 'semilla_3grama', [(a, b) in sem for a, b in zip(pi, pj)])
    r1.insert(0, 'nB', L[pj]); r1.insert(0, 'nA', L[pi]); r1.insert(0, 'B', ids[pj]); r1.insert(0, 'A', ids[pi])
    r1.to_csv(os.path.join(OUT, 'pares_duplicados_todos.csv.gz'), index=False, float_format='%.4g')
    sig = (r1.q < .05) & (r1.q_bloque < .05)
    print('  q<0.05:', (r1.q < .05).sum(), ' robustos (también bloques):', sig.sum(),
          ' pares con semilla:', len(sem), ' con q<0.05 y semilla:', ((r1.q < .05) & r1.semilla_3grama).sum())


def tarea2():
    D = preparar()
    ids = np.array(D['ids'])
    L = np.diff(D['off'])
    pi, pj = [x.astype(np.int64) for x in np.triu_indices(len(ids), 1)]
    oi = np.concatenate([pi, pj]); oj = np.concatenate([pj, pi])
    keep = D['NG'][oi] >= 2  # al menos dos totales: correspondencia secuencial posible
    oi, oj = oi[keep], oj[keep]
    print('tarea 2: pares ordenados', len(oi), flush=True)
    r2 = evaluar(resumen_pares, (D['PV'], D['GID'], D['NG'], D['poff'], D['V'], D['off']), oi, oj, SEED + 10)
    top = np.where(r2.refinado.values)[0]
    o, n = resumen_orden(D['PV'], D['GID'], D['NG'], D['poff'], D['V'], D['off'], oi[top], oj[top],
                         N_PERM_TOP, SEED + 13, GAP)
    r2['p_orden'] = 1.0
    r2.loc[top, 'p_orden'] = p_valor(o, n)[0]
    r2['q_orden'] = bh(r2.p_orden.values)  # no refinados: 1 (conservador)
    r2.insert(0, 'nB', L[oj]); r2.insert(0, 'n_totales', D['NG'][oi])
    r2.insert(0, 'B_cuerdas', ids[oj]); r2.insert(0, 'A_totales', ids[oi])
    r2.to_csv(os.path.join(OUT, 'pares_resumen_todos.csv.gz'), index=False, float_format='%.4g')
    print('  q<0.05:', (r2.q < .05).sum(), ' y q_orden<0.05:', ((r2.q < .05) & (r2.q_orden < .05)).sum(),
          ' y q_bloque<0.05:', ((r2.q < .05) & (r2.q_bloque < .05)).sum())


def grandes(umbral=100):
    """Tarea 1b: igual que la tarea 1 pero sólo con la subsecuencia de valores >= umbral (las
    "cabeceras" de bloque). Robusta a inserciones de cuerdas pequeñas entre versiones."""
    D = preparar()
    sub = {k: s[s.v >= umbral] for k, s in D['seqs'].items()}
    ids = np.array(sorted(k for k, s in sub.items() if len(s) >= 3))
    off = np.cumsum([0] + [len(sub[k]) for k in ids]).astype(np.int64)
    V = np.concatenate([sub[k].v.values for k in ids]).astype(np.int64)
    pi, pj = [x.astype(np.int64) for x in np.triu_indices(len(ids), 1)]
    print(f'tarea 1b (valores >= {umbral}): quipus {len(ids)}, pares {len(pi)}', flush=True)
    r = evaluar(todos_los_pares, (V, off), pi, pj, SEED + 20)
    L = np.diff(off)
    r.insert(0, 'nB', L[pj]); r.insert(0, 'nA', L[pi]); r.insert(0, 'B', ids[pj]); r.insert(0, 'A', ids[pi])
    r.to_csv(os.path.join(OUT, f'pares_duplicados_valores{umbral}.csv.gz'), index=False, float_format='%.4g')
    print('  q<0.05:', (r.q < .05).sum())


def _demo():
    """Autocomprobación: copia de 20 cuerdas con un error de ±1 dígito y una cuerda omitida."""
    rng = np.random.default_rng(0)
    a = rng.integers(1, 300, 40).astype(np.int64)
    b = np.concatenate([rng.integers(1, 300, 10), a[5:25], rng.integers(1, 300, 10)]).astype(np.int64)
    b[15] += 10
    b = np.delete(b, 20)
    V = np.concatenate([a, b])
    o, n = todos_los_pares(V, np.array([0, 40, len(V)], dtype=np.int64), np.array([0]), np.array([1]),
                           200, 1, GAP, 1)
    assert p_valor(o, n)[0][0] < 1e-3, (o, n.max())
    sc, sentido, path = traza(matriz_dup(a, b))
    assert sentido == 'directo' and sum(1 for x, y in path if x is not None and y is not None) >= 17
    # nulo: dos secuencias independientes no deben salir significativas
    c = rng.integers(1, 300, 40).astype(np.int64)
    V = np.concatenate([a, c])
    o, n = todos_los_pares(V, np.array([0, 40, 80], dtype=np.int64), np.array([0]), np.array([1]),
                           200, 1, GAP, 1)
    assert p_valor(o, n)[0][0] > 0.01
    # tarea 2: los 6 totales de grupo de A aparecen en orden, dispersos entre 80 cuerdas de B
    pv = rng.integers(1, 60, 30).astype(np.int64)
    gid = np.repeat(np.arange(6), 5).astype(np.int64)
    b = rng.integers(1, 60, 80).astype(np.int64)
    b[5::12][:6] = _totales(pv, gid, 6)
    o, n = resumen_pares(pv, gid, np.array([6]), np.array([0, 30]), b, np.array([0, 80]),
                         np.array([0]), np.array([0]), 300, 1, GAP, 1)
    assert p_valor(o, n)[0][0] < 1e-3, (o, n.max())
    print('demo ok')


if __name__ == '__main__':
    if '--demo' in sys.argv:
        _demo()
    elif '--grandes' in sys.argv:
        grandes()
    elif '--resumen' in sys.argv:
        tarea2()
    else:
        main()
        tarea2()
        grandes()
