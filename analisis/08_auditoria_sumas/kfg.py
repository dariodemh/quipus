"""Reimplementación de los detectores de sumas de Ascher del KFG (Medrano y Khosla 2024,
source/02_ascher_sum_relationships.html) + nulos por permutación + coste por relación.

Detectores (reglas copiadas del código KFG):
  PPS  colgante (valor>10) = suma de un tramo contiguo de colgantes a su izq. o der., a CUALQUIER distancia.
       Busca el primer inicio s (valor>0) cuyo cumsum alcanza v; si ese tramo tiene 1 cuerda, se rinde (quirk KFG).
       Tramo >=2 cuerdas (los huecos 0 cuentan) y v > nº de cuerdas del tramo. Bucle i in range(n-2) por lado.
  COL  colgante (valor>10) = suma de un tramo de >=3 colgantes NO NULOS del mismo color (color "más largo"),
       contiguos dentro de la lista de ese color, a izq. o der.; tramo más corto; v > longitud.
  IDX  colgante (valor>5, no múltiplo de 10 si <100 ni de 100 si 100..999) = suma de >=2 cuerdas no nulas con el
       mismo índice en grupos contiguos a izq. o der.; tramo más corto; v > longitud.
  SUB  subsidiaria de nivel 1 (valor>10, no múltiplo de 10 si <100) = suma de >=3 colgantes no nulos contiguos a la
       izq. (incluida su madre) o a la der.; tramo más corto; v > longitud.
Cada lado (izq./der.) cuenta como una relación, como en los CSV del KFG.
"""
import re
import numpy as np, pandas as pd
from pathlib import Path
from numba import njit

RAIZ = Path(__file__).resolve().parents[2]
REL = RAIZ / "data/external/data-science-khipu-article/data/ascher_sum_relations"


def color_largo(s):
    if not isinstance(s, str):
        return ""
    if "(" not in s:
        return s
    best, bl = s, -1.0
    for seg in s.split("/"):
        m = re.match(r"\s*([^()]+)\(([\d.]+)-([\d.]+)\)", seg)
        if m and float(m.group(3)) - float(m.group(2)) > bl:
            best, bl = m.group(1).strip(), float(m.group(3)) - float(m.group(2))
    return best


def kfg_name(n):
    return n.replace(" - ", "_").replace("/", "_").replace(" ", "_")


def cargar():
    c = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
    c["valor"] = c["valor"].fillna(0).round().astype("int64")
    c["pres"] = c["nudos"].notna() | (c["valor"] > 0)
    c["col"] = c["color"].map(color_largo)
    codes = {k: i for i, k in enumerate(c["col"].unique())}
    out = {}
    for k, d in c.groupby("kfg", sort=False):
        d = d.sort_values("orden").reset_index(drop=True)
        P = np.where(d["nivel"].values == 0)[0]
        pos = {n: j for j, n in enumerate(d["cuerda"].values[P])}
        S = np.where(d["nivel"].values == 1)[0]
        g = d["grupo"].values[P]
        # índice dentro del grupo
        gi = np.zeros(len(P), np.int64); gid = np.zeros(len(P), np.int64)
        u = {x: i for i, x in enumerate(pd.unique(g))}
        cnt = {}
        for j, x in enumerate(g):
            gid[j] = u[x]; gi[j] = cnt.get(x, 0); cnt[x] = gi[j] + 1
        out[k] = dict(
            kfg=k, n=len(d), v=d["valor"].values.astype(np.int64), pres=d["pres"].values, lvl=d["nivel"].values.astype(np.int64),
            P=P.astype(np.int64), S=S.astype(np.int64),
            spar=np.array([pos.get(p, -1) for p in d["padre"].values[S]], np.int64),
            col=np.array([codes[x] for x in d["col"].values[P]], np.int64),
            gid=gid, gi=gi, ng=len(u), names=d["cuerda"].values)
    return out


# ------------------------------------------------------------------ detectores
@njit(cache=True)
def _first_ge(S, lo, hi, t):
    # primer índice k en [lo,hi) con S[k] >= t (S no decreciente)
    while lo < hi:
        m = (lo + hi) // 2
        if S[m] < t:
            lo = m + 1
        else:
            hi = m
    return lo


@njit(cache=True)
def pps_side(a, rel_i, rel_s, rel_e, nrel, rev):
    """a: valores de colgantes (en orden de búsqueda). Registra (i, s, e) en coordenadas originales."""
    n = len(a)
    S = np.zeros(n + 1, np.int64)
    for i in range(n):
        S[i + 1] = S[i] + a[i]
    for i in range(n - 2):
        v = a[i]
        if v <= 10:
            continue
        for s in range(i + 1, n):
            if a[s] > 0:
                t = S[s] + v
                k = _first_ge(S, s + 1, n + 1, t)
                if k <= n and S[k] == t:
                    if k - s >= 2 and v > k - s:
                        if rev:
                            rel_i[nrel] = n - 1 - i; rel_s[nrel] = n - k; rel_e[nrel] = n - s
                        else:
                            rel_i[nrel] = i; rel_s[nrel] = s; rel_e[nrel] = k
                        nrel += 1
                    break
    return nrel


@njit(cache=True)
def pps(a):
    n = len(a)
    ri = np.empty(2 * n + 1, np.int64); rs = np.empty(2 * n + 1, np.int64); re_ = np.empty(2 * n + 1, np.int64)
    m = pps_side(a, ri, rs, re_, 0, False)
    m = pps_side(a[::-1].copy(), ri, rs, re_, m, True)
    return ri[:m], rs[:m], re_[:m]


@njit(cache=True)
def shortest(vals, v, minlen, maxlen):
    """Longitud del tramo contiguo más corto (minlen..maxlen) de vals (>0) que suma v; 0 si no hay."""
    m = len(vals)
    if m < minlen:
        return 0
    S = np.zeros(m + 1, np.int64)
    for i in range(m):
        S[i + 1] = S[i] + vals[i]
    best = 0
    for s in range(m):
        t = S[s] + v
        k = _first_ge(S, s + 1, m + 1, t)
        if k <= m and S[k] == t:
            L = k - s
            if L >= minlen and L <= maxlen and (best == 0 or L < best):
                best = L
    return best


@njit(cache=True)
def col_sum(a, col):
    n = len(a); r = 0
    buf = np.empty(n, np.int64)
    for i in range(n):
        v = a[i]
        if v <= 10:
            continue
        # izquierda
        m = 0
        for j in range(i):
            if col[j] == col[i] and a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 3, 248)
        if L > 0 and v > L: r += 1
        m = 0
        for j in range(i + 1, n):
            if col[j] == col[i] and a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 3, 248)
        if L > 0 and v > L: r += 1
    return r


@njit(cache=True)
def idx_sum(a, gid, gi, ng):
    n = len(a); r = 0
    # tabla grupo x índice -> posición
    maxi = 0
    for i in range(n):
        if gi[i] + 1 > maxi: maxi = gi[i] + 1
    T = -np.ones((ng, maxi), np.int64)
    for i in range(n):
        T[gid[i], gi[i]] = i
    buf = np.empty(ng, np.int64)
    for i in range(n):
        v = a[i]
        if v <= 5: continue
        if v < 100 and v % 10 == 0: continue
        if v >= 100 and v < 1000 and v % 100 == 0: continue
        k = gi[i]; g = gid[i]
        m = 0
        for h in range(g):
            j = T[h, k]
            if j >= 0 and a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 2, 100000)
        if L > 0 and v > L: r += 1
        m = 0
        for h in range(g + 1, ng):
            j = T[h, k]
            if j >= 0 and a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 2, 100000)
        if L > 0 and v > L: r += 1
    return r


@njit(cache=True)
def sub_sum(a, sv, spar):
    n = len(a); r = 0
    buf = np.empty(n, np.int64)
    for q in range(len(sv)):
        v = sv[q]; p = spar[q]
        if v <= 10 or p < 0: continue
        if v < 100 and v % 10 == 0: continue
        m = 0
        for j in range(p + 1):
            if a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 3, 248)
        if L > 0 and v > L: r += 1
        m = 0
        for j in range(p + 1, n):
            if a[j] > 0:
                buf[m] = a[j]; m += 1
        L = shortest(buf[:m], v, 3, 248)
        if L > 0 and v > L: r += 1
    return r


# ------------------------------------------------------------------ coste por relación (modelo de dígitos)
def digit_model(vals):
    """F[d, k, x]: prob. del dígito x en la posición k (0 = unidades) entre valores de d dígitos del quipu (+0.5 Laplace).
    El dígito inicial se restringe a 1..9."""
    D = 7
    F = np.zeros((D + 1, D, 10))
    vals = vals[vals > 0]
    for d in range(1, D + 1):
        w = vals[(vals >= 10 ** (d - 1)) & (vals < 10 ** d)]
        for k in range(d):
            dig = (w // 10 ** k) % 10
            h = np.bincount(dig, minlength=10).astype(float) + 0.5
            if k == d - 1:
                h[0] = 0.0
            F[d, k] = h / h.sum()
    return F


@njit(cache=True)
def pw(w, d, F):
    p = 1.0
    for k in range(d):
        p *= F[d, k, (w // 10 ** k) % 10]
    return p


@njit(cache=True)
def coste(a, i, F):
    """P(V ∈ W_i): V ~ modelo de dígitos con el mismo nº de dígitos que a[i]; W_i = sumas distintas de tramos
    (>=2 cuerdas, empezando en cuerda no nula, sin contener i) a la izq. o der. de i. Nº de dígitos <= 6."""
    v = a[i]
    d = 0; x = v
    while x > 0:
        d += 1; x //= 10
    if d > 6:
        return 0.0
    lo = 10 ** (d - 1); hi = 10 ** d
    seen = np.zeros(hi - lo, np.bool_)
    n = len(a); p = 0.0
    for side in range(2):
        a0 = 0 if side == 0 else i + 1
        a1 = i if side == 0 else n
        for s in range(a0, a1):
            if a[s] <= 0: continue
            t = a[s]
            for e in range(s + 1, a1):
                t += a[e]
                if t >= hi: break
                if t >= lo and not seen[t - lo]:
                    seen[t - lo] = True
                    p += pw(t, d, F)
    return min(p, 1.0)


@njit(cache=True)
def coste_local(a, i, F):
    """Como coste(), pero W_i = sumas de tramos ADYACENTES a i (saltando huecos 0): empiezan en la primera cuerda no nula
    a la derecha de i o terminan en la primera no nula a su izquierda."""
    v = a[i]
    d = 0; x = v
    while x > 0:
        d += 1; x //= 10
    if d > 6:
        return 0.0
    lo = 10 ** (d - 1); hi = 10 ** d
    seen = np.zeros(hi - lo, np.bool_)
    n = len(a); p = 0.0
    s = i + 1
    while s < n and a[s] == 0:
        s += 1
    t = 0; c = 0
    for e in range(s, n):
        t += a[e]; c += 1
        if t >= hi: break
        if c >= 2 and t >= lo and not seen[t - lo]:
            seen[t - lo] = True; p += pw(t, d, F)
    s = i - 1
    while s >= 0 and a[s] == 0:
        s -= 1
    t = 0; c = 0
    for e in range(s, -1, -1):
        t += a[e]; c += 1
        if t >= hi: break
        if c >= 2 and t >= lo and not seen[t - lo]:
            seen[t - lo] = True; p += pw(t, d, F)
    return min(p, 1.0)


@njit(cache=True)
def es_ady(a, i, s, e):
    if s > i:
        for j in range(i + 1, s):
            if a[j] != 0: return False
        return True
    for j in range(e, i):
        if a[j] != 0: return False
    return True


@njit(cache=True)
def rel_pps(a, F):
    """Relaciones PPS con atributos: (i, s, e, adyacente, cadena, coste_global, coste_local)."""
    ri, rs, re_ = pps(a)
    m = len(ri)
    issum = np.zeros(len(a), np.bool_)
    for r in range(m):
        issum[ri[r]] = True
    R = np.zeros((m, 7))
    for r in range(m):
        i = ri[r]
        ch = 0
        for j in range(rs[r], re_[r]):
            if issum[j]:
                ch = 1; break
        ad = es_ady(a, i, rs[r], re_[r])
        R[r, 0] = i; R[r, 1] = rs[r]; R[r, 2] = re_[r]; R[r, 3] = ad; R[r, 4] = ch
        R[r, 5] = coste(a, i, F)
        R[r, 6] = coste_local(a, i, F) if ad else 1.0
    return R


@njit(cache=True)
def stats(a, col, gid, gi, ng, sv, spar, F):
    """Vector de estadísticos de un quipu:
    0 PPS, 1 COL, 2 IDX, 3 SUB, 4 PPS v>=100, 5 PPS adyacente, 6 PPS en cadena (algún sumando es cuerda-suma PPS),
    7 PPS adyacente con coste local <0.01 ("cara"), 8 ídem <0.001, 9 PPS adyacente y v>=100,
    10 suma de -log10(coste local) de las PPS adyacentes, 11 PPS con coste global <0.05."""
    out = np.zeros(12)
    R = rel_pps(a, F)
    m = R.shape[0]
    out[0] = m
    out[1] = col_sum(a, col)
    out[2] = idx_sum(a, gid, gi, ng)
    out[3] = sub_sum(a, sv, spar)
    for r in range(m):
        v = a[int(R[r, 0])]; ad = R[r, 3] > 0
        if v >= 100: out[4] += 1
        if ad: out[5] += 1
        if ad and v >= 100: out[9] += 1
        out[6] += R[r, 4]
        if ad:
            if R[r, 6] < 0.01: out[7] += 1
            if R[r, 6] < 0.001: out[8] += 1
            out[10] += -np.log10(max(R[r, 6], 1e-6))
        if R[r, 5] < 0.05: out[11] += 1
    return out


NST = 12
NOMBRES = ["PPS", "COL", "IDX", "SUB", "PPS_100", "PPS_ady", "PPS_cadena", "PPS_cara01", "PPS_cara001", "PPS_ady100", "PPS_sumlog_local", "PPS_global05"]


@njit(cache=True)
def run_null(v0, P, S, spar, col, gid, gi, ng, pidx, seg, B, seed, F):
    np.random.seed(seed)
    res = np.zeros((B, NST))
    vals0 = v0[pidx]
    for b in range(B):
        vals = vals0.copy()
        for q in range(len(seg) - 1):
            x = vals[seg[q]:seg[q + 1]].copy()
            np.random.shuffle(x)
            vals[seg[q]:seg[q + 1]] = x
        v = v0.copy()
        for t in range(len(pidx)):
            v[pidx[t]] = vals[t]
        res[b] = stats(v[P], col, gid, gi, ng, v[S], spar, F)
    return res


def obs(Q, F=None):
    if F is None:
        F = digit_model(Q["v"][Q["pres"]])
    v = Q["v"]
    return stats(v[Q["P"]], Q["col"], Q["gid"], Q["gi"], Q["ng"], v[Q["S"]], Q["spar"], F)


def estratos(Q, modo):
    """modo 0: todo el quipu; 1: dentro de nivel; 2: dentro de nivel x magnitud (nº de dígitos).
    Las cuerdas ausentes (0 sin nudos) quedan fijas."""
    pres = np.where(Q["pres"])[0]
    lv = np.minimum(Q["lvl"], 3)
    v = Q["v"]
    mag = np.where(v > 0, np.floor(np.log10(np.maximum(v, 1))).astype(np.int64) + 1, 0)
    st = [np.zeros(len(v), np.int64), lv, lv * 100 + mag][modo]
    s = st[pres]
    o = np.argsort(s, kind="stable")
    pidx = pres[o].astype(np.int64)
    ss = s[o]
    seg = np.concatenate([[0], np.where(np.diff(ss) != 0)[0] + 1, [len(ss)]]).astype(np.int64)
    return pidx, seg


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    r = p[o] * n / (np.arange(n) + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    q = np.empty(n); q[o] = np.minimum(r, 1)
    return q


def autotest():
    # PPS: 20 = 5+15 (adyacente, der.) ; 12 en pos 4 = 4+8 (izq.)
    a = np.array([20, 5, 15, 4, 8, 12, 1], np.int64)
    ri, rs, re_ = pps(a)
    got = sorted(zip(ri.tolist(), rs.tolist(), re_.tolist()))
    assert (0, 1, 3) in got and (5, 3, 5) in got, got
    # quirk: valor idéntico encontrado primero corta la búsqueda
    a = np.array([30, 30, 10, 20, 1], np.int64)
    ri, _, _ = pps(a)
    assert 0 not in ri.tolist()
    # shortest y filtros
    assert shortest(np.array([1, 2, 3, 4, 5], np.int64), 9, 3, 248) == 3   # 2+3+4
    assert shortest(np.array([4, 5], np.int64), 9, 3, 248) == 0
    assert col_sum(np.array([15, 4, 5, 6, 7], np.int64), np.array([0, 0, 0, 0, 1], np.int64)) == 1
    assert idx_sum(np.array([3, 4, 7], np.int64), np.array([0, 1, 2], np.int64), np.zeros(3, np.int64), 3) == 1
    assert sub_sum(np.array([1, 5, 6, 2], np.int64), np.array([13], np.int64), np.array([3], np.int64)) == 1
    print("autotest ok")


if __name__ == "__main__":
    autotest()
