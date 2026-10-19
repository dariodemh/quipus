# -*- coding: utf-8 -*-
"""Motor de desciframiento por tanteo controlado (estilo Knight-Yamada /
Snyder-Barzilay-Knight 2010) + controles.

Modelo: bigramas de silabas (quechua colonial). Se busca la asignacion
signo -> silaba que maximiza  sum_t log P(f(s_t) | f(s_{t-1}))
por recocido simulado con reinicios. Todo se compara con el mismo esfuerzo de
busqueda sobre secuencias barajadas (nulo) y sobre texto real cifrado
(control positivo).
"""
import re, json, os, sys, math, random
import numpy as np
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm_utils import CORP, silabas

# ------------------------------------------------------------------ LM
def load_stream_lm(name):
    """Carga el LM y devuelve (uni, bi) entrenado sobre el flujo continuo."""
    d = json.load(open(os.path.join(CORP, f"lm_{name}.json"), encoding="utf-8"))
    uni = Counter(d["uni"])
    bi = Counter({tuple(k.split("\t")): v for k, v in d["bi"].items()})
    return uni, bi

def build_L(uni, bi, K=120, k=0.1):
    """Matriz de log-probabilidades L[prev, cur] sobre las K silabas mas frecuentes.
    Fila 0 = <s>. Suavizado add-k sobre K."""
    top = [s for s, _ in uni.most_common(K)]
    idx = {s: i + 1 for i, s in enumerate(top)}
    K2 = len(top)
    N = sum(uni[s] for s in top)
    ctx = np.zeros(K2 + 1)
    cnt = np.zeros((K2 + 1, K2))
    for (a, b), c in bi.items():
        if b in idx:
            j = idx[b] - 1
            if a == "<s>":
                ctx[0] += c; cnt[0, j] += c
            elif a in idx:
                ctx[idx[a]] += c; cnt[idx[a] - 1, j] += c
    L = np.zeros((K2 + 1, K2))
    denom = (ctx[:, None] + k * K2)
    denom[denom == 0] = 1
    L = np.log((cnt + k / K2) / denom + 1e-300)
    return L, top

def logp_true(L, syls, inv):
    """logL de una asignacion dada (lista de silabas alineada con inv)."""
    m = {s: i + 1 for i, s in enumerate(inv)}
    f = np.array([m[s] for s in syls])
    return f

# ------------------------------------------------------------------ secuencias
def counts_seq(seq, verbose=False):
    signs = sorted(set(seq))
    idx = {s: i for i, s in enumerate(signs)}
    V = len(signs)
    C = np.zeros((V, V))
    st = np.zeros(V)
    for t, x in enumerate(seq):
        if t == 0:
            st[idx[x]] += 1
        else:
            C[idx[seq[t - 1]], idx[x]] += 1
    return C, st, signs

def objective(C, st, f, L):
    """f: (B,V) indices de silaba (1..K). Devuelve (B,)."""
    # L[f_prev, f_cur] -> (B,V,V)
    Lp = L[f[:, :, None] + 1, f[:, None, :]]
    val = (C * Lp).sum(axis=(1, 2))
    val = val + (st * L[0][f]).sum(axis=1)
    return val

def anneal(C, st, L, restarts=4, iters=2500, T0=3.0, T1=0.02, seed=0, f_init=None):
    """Recocido simulado batcheado sobre asignaciones INYECTIVAS signo -> silaba
    (cifrado de sustitucion). C:(B,V,V) st:(B,V). Devuelve f (B,V), val (B,)."""
    B, V, _ = C.shape
    K = L.shape[1]
    assert V <= K, (V, K)
    rng = np.random.default_rng(seed)
    best_f = np.zeros((B, V), dtype=int)
    best_v = np.full(B, -1e18)
    ar = np.arange(B)
    signos = np.arange(V)[None, :]
    for r in range(restarts):
        if f_init is not None and r == 0:
            f = f_init.copy()
        else:
            f = np.stack([rng.permutation(K)[:V] for _ in range(B)])
        pos = np.full((B, K), -1, dtype=int)
        pos[ar[:, None], f] = signos
        cur = objective(C, st, f, L)
        T = T0
        alpha = (T1 / T0) ** (1.0 / max(1, iters))
        for it in range(iters):
            f0 = f.copy(); pos0 = pos.copy()
            if rng.random() < 0.5:
                a = rng.integers(0, V, B); b = rng.integers(0, V, B)
                fa = f[ar, a].copy(); fb = f[ar, b].copy()
                f[ar, a] = fb; f[ar, b] = fa
                pos[ar, fa] = b; pos[ar, fb] = a
            else:
                a = rng.integers(0, V, B)
                c = rng.integers(0, K, B)
                b = pos[ar, c].copy()
                old = f[ar, a].copy()
                f[ar, a] = c
                cond = (b >= 0) & (b != a)
                f[ar[cond], b[cond]] = old[cond]
                pos[ar, old] = b
                pos[ar, c] = a
            new = objective(C, st, f, L)
            d = new - cur
            acc = (d >= 0) | (rng.random(B) < np.exp(np.minimum(d / T, 0)))
            bad = ~acc
            f[bad] = f0[bad]; pos[bad] = pos0[bad]
            cur = np.where(acc, new, cur)
            T *= alpha
            upd = cur > best_v
            if upd.any():
                best_v[upd] = cur[upd]; best_f[upd] = f[upd]
    return best_f, best_v

# ------------------------------------------------------------------ estadisticos
def hcond(seq, V):
    """Entropia condicional empirica H(next|prev), en bits, y normalizada."""
    if len(seq) < 3:
        return np.nan, np.nan
    c = Counter(seq); n = len(seq)
    uni = np.array([c[s] for s in sorted(c)], float) / n
    H1 = -(uni * np.log2(uni)).sum()
    bi = Counter(zip(seq[:-1], seq[1:]))
    H2 = 0.0
    for (a, b), k in bi.items():
        H2 -= (k / (n - 1)) * math.log2(k / c[a])
    # correccion de Miller-Madow con el numero de celdas observadas
    H1c = H1 + (len(c) - 1) / (2 * n * math.log(2))
    H2c = H2 + (len(bi) - 1) / (2 * (n - 1) * math.log(2))
    return H2c, H2c / max(1e-9, math.log2(max(V, 2)))

def zipf_slope(seq):
    c = np.array(sorted(Counter(seq).values(), reverse=True), float)
    if len(c) < 3:
        return np.nan
    x = np.log(np.arange(1, len(c) + 1)); y = np.log(c)
    return float(np.polyfit(x, y, 1)[0])

def rep_rate(seq):
    if len(seq) < 2:
        return np.nan
    return float(np.mean([seq[i] == seq[i - 1] for i in range(1, len(seq))]))
