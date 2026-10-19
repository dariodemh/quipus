"""33 · Núcleo compartido: datos, medida multibloque (reordenamiento, inversión, escala, huecos,
tolerancia) y nulo de rachas. Reutiliza las puntuaciones log-odds de 04 (`_ft`, `matriz`).
`python comun.py --demo` autocomprueba la medida con copias sembradas."""
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from numba import njit, prange

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.dirname(os.path.abspath(__file__))
SEED = 20261033
GAP, TAU, KMAX = 5.0, 20.0, 5  # TAU 10 -> 20: adenda 2 de diseno.md
ESCALAS = np.array([1.0, 10.0, 0.1, 2.0, 0.5])
CENT = -10 ** 9  # centinela: nunca coincide (ni tolerante)

sys.path.insert(0, os.path.join(RAIZ, 'analisis', '04_concordancias'))
from concordancias import _ft, matriz, p_valor, bh, barajar  # noqa: E402  (reutilizo 04)


def color_norm(s):
    return re.sub(r'\([^)]*\)', '', str(s)) if isinstance(s, str) else ''


def preparar():
    c = pd.read_csv(os.path.join(RAIZ, 'analisis/datos/cuerdas.csv'), low_memory=False)
    c['kn'] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != '') & c.valor.notna()
    c = c.sort_values(['kfg', 'orden'])
    ck = c[c.kn].copy()
    ck['v'] = ck.valor.round().astype(np.int64)
    ck['col'] = ck.color.map(color_norm)
    seqs = {k: g.reset_index(drop=True) for k, g in ck.groupby('kfg', sort=True) if len(g) >= 3}
    ids = sorted(seqs)
    off = np.cumsum([0] + [len(seqs[k]) for k in ids]).astype(np.int64)
    V = np.concatenate([seqs[k].v.values for k in ids]).astype(np.int64)
    LV = np.concatenate([seqs[k].nivel.values for k in ids]).astype(np.int64)
    return dict(c=c, seqs=seqs, ids=ids, V=V, LV=LV, off=off)


# ------------------------------------------------------------------ medida multibloque
@njit(cache=True)
def escalar(b, k):
    out = np.empty_like(b)
    for j in range(b.shape[0]):
        if k >= 1.0:
            out[j] = b[j] * int(round(k))
        else:
            d = int(round(1.0 / k))
            out[j] = b[j] // d if b[j] % d == 0 else CENT
    return out


@njit(cache=True)
def matriz_par(a, b):
    pool = np.concatenate((a, b[b > 0]))
    fa, ta = _ft(a, pool)
    fb, tb = _ft(b, pool)
    S = matriz(a, b, fa, ta, fb, tb)
    for j in range(b.shape[0]):
        if b[j] == CENT:
            for i in range(a.shape[0]):
                S[i, j] = -3.0
    return S


@njit(cache=True)
def _sw(S, gap, rev, H, P):
    m, n = S.shape
    best, bi, bj = 0.0, 0, 0
    for i in range(m):
        for j in range(n):
            s = S[i, n - 1 - j] if rev else S[i, j]
            h, p = 0.0, 0
            x = H[i, j] + s
            if x > h:
                h, p = x, 1
            x = H[i, j + 1] - gap
            if x > h:
                h, p = x, 2
            x = H[i + 1, j] - gap
            if x > h:
                h, p = x, 3
            H[i + 1, j + 1] = h
            P[i + 1, j + 1] = p
            if h > best:
                best, bi, bj = h, i + 1, j + 1
    return best, bi, bj


@njit(cache=True)
def multibloque(S0, gap, tau, kmax, rec):
    """Suma de hasta kmax bloques locales disjuntos (filas y columnas de cada tramo se retiran).
    rec[x] = (i, j, bloque, sentido) de cada celda alineada (j en el orden original de B);
    devuelve (total, n_bloques, n_celdas)."""
    S = S0.copy()
    m, n = S.shape
    H = np.zeros((m + 1, n + 1))
    P = np.zeros((m + 1, n + 1), dtype=np.int8)
    total, nb, nc = 0.0, 0, 0
    for b in range(kmax):
        b0, i0, j0 = _sw(S, gap, False, H, P)
        b1, i1, j1 = _sw(S, gap, True, H, P)
        rev = b1 > b0
        best = b1 if rev else b0
        if (b == 0 and best <= 0) or (b > 0 and best < tau):
            break
        if not rev:  # recalcular la orientación elegida para el traceback
            best, i, j = _sw(S, gap, False, H, P)
        else:
            i, j = i1, j1
        total += best
        imin, imax, jmin, jmax = m, -1, n, -1
        while i > 0 and j > 0 and P[i, j] != 0:
            p = P[i, j]
            jj = (n - j) if rev else (j - 1)
            if p == 1:
                if nc < rec.shape[0]:
                    rec[nc, 0], rec[nc, 1], rec[nc, 2], rec[nc, 3] = i - 1, jj, b, 1 if rev else 0
                nc += 1
                i -= 1; j -= 1
            elif p == 2:
                i -= 1
            else:
                j -= 1
            imin = min(imin, i); imax = max(imax, i)
            jmin = min(jmin, jj); jmax = max(jmax, jj)
        for r in range(max(imin, 0), min(imax + 1, m)):
            for c in range(n):
                S[r, c] = -1e6
        for c in range(max(jmin, 0), min(jmax + 1, n)):
            for r in range(m):
                S[r, c] = -1e6
        nb += 1
    return total, nb, nc


@njit(cache=True)
def puntuar(a, b, escalas, gap, tau, kmax):
    rec = np.zeros((1, 4), dtype=np.int64)
    best, kbest = -1.0, 0
    for k in range(escalas.shape[0]):
        bt = escalar(b, escalas[k])
        if (bt > 0).sum() < 3:
            continue
        s, _, _ = multibloque(matriz_par(a, bt), gap, tau, kmax, rec)
        if s > best:
            best, kbest = s, k
    return best, kbest


@njit(cache=True)
def barajar_rachas(x):
    """Nulo principal (adenda 2): permuta las rachas de valores iguales como unidades; conserva
    las rachas (1-1-1-1) y la composición, destruye el orden entre valores distintos."""
    n = x.shape[0]
    st = [0]
    for i in range(1, n):
        if x[i] != x[i - 1]:
            st.append(i)
    st.append(n)
    o = np.random.permutation(len(st) - 1)
    out = np.empty_like(x)
    k = 0
    for r in o:
        for u in range(st[r], st[r + 1]):
            out[k] = x[u]
            k += 1
    return out


@njit(cache=True)
def barajar_bloques(x, block):
    return barajar(x, block)


@njit(parallel=True, cache=True)
def evaluar_pares(V, LV, off, pi, pj, nperm, seed, escalas, gap, tau, kmax, modo):
    """modo 0: nulo de rachas; modo 1: bloques de 5. Devuelve obs, k elegido, nulos."""
    K = pi.shape[0]
    obs = np.zeros(K)
    kb = np.zeros(K, dtype=np.int64)
    null = np.zeros((K, nperm))
    for q in prange(K):
        a = V[off[pi[q]]:off[pi[q] + 1]]
        b = V[off[pj[q]]:off[pj[q] + 1]]
        obs[q], kb[q] = puntuar(a, b, escalas, gap, tau, kmax)
        np.random.seed(seed + q)
        for r in range(nperm):
            if modo == 0:
                null[q, r] = puntuar(barajar_rachas(a), barajar_rachas(b), escalas, gap, tau, kmax)[0]
            else:
                null[q, r] = puntuar(barajar_bloques(a, 5), barajar_bloques(b, 5), escalas, gap, tau, kmax)[0]
    return obs, kb, null


def detalle(a, b, k):
    """Bloques del par con la escala k (índice en ESCALAS): DataFrame de celdas alineadas."""
    bt = escalar(b, ESCALAS[k])
    rec = np.zeros((len(a) + len(b) + 5, 4), dtype=np.int64)
    tot, nb, nc = multibloque(matriz_par(a, bt), GAP, TAU, KMAX, rec)
    d = pd.DataFrame(rec[:nc], columns=['i', 'j', 'bloque', 'inverso']).sort_values(['bloque', 'i'])
    return tot, nb, d.reset_index(drop=True)


def _demo():
    rng = np.random.default_rng(1)
    a = rng.choice([1, 2, 3, 5, 10, 12, 20, 33, 47, 58, 120, 133, 251, 312, 404, 1180], 60).astype(np.int64)
    a[:10] = [57, 30, 56, 143, 211, 87, 64, 402, 19, 233]
    a[30:40] = [912, 18, 73, 260, 45, 132, 77, 501, 28, 66]
    otro = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20], 60).astype(np.int64)
    # B = bloque 2 de A invertido + ruido + bloque 1 con un error ±1 nudo y una omisión
    b1 = np.delete(a[:10].copy(), 4); b1[2] += 10
    b = np.concatenate((otro[:15], a[30:40][::-1], otro[15:30], b1)).astype(np.int64)
    s, k = puntuar(a, b, ESCALAS, GAP, TAU, KMAX)
    tot, nb, d = detalle(a, b, k)
    assert nb >= 2 and ESCALAS[k] == 1.0 and set(d.inverso) == {0, 1}, (nb, k, d)
    s10, k10 = puntuar(a, (b * 10).astype(np.int64), ESCALAS, GAP, TAU, KMAX)
    assert ESCALAS[k10] == 0.1 and abs(s10 - s) < 1e-6, (s10, s, k10)
    s0, _ = puntuar(a, otro, ESCALAS, GAP, TAU, KMAX)
    assert s0 < s / 3, (s0, s)
    y = barajar_rachas(np.array([1, 1, 1, 5, 7, 7], dtype=np.int64))
    assert sorted(y) == [1, 1, 1, 5, 7, 7] and ''.join(map(str, y)).count('111') == 1
    print('demo ok', round(s, 1), nb, 'bloques; escala x10 ->', round(s10, 1), '; independiente', round(s0, 1))


if __name__ == '__main__' and '--demo' in sys.argv:
    _demo()
