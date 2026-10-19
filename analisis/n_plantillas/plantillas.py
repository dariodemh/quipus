"""Estadísticos de las plantillas congeladas (ver plantillas.md). Cada función vectorizada
recibe una matriz B×n de valores (o colores) permutados y devuelve B estadísticos.
Convención: estadístico mayor = más parecido a la plantilla; None = la puerta no se cumple."""
import numpy as np
from collections import Counter
from numpy.lib.stride_tricks import sliding_window_view as sw
from scipy.stats import rankdata

# ---------- perfiles demográficos (P1) ----------
_AG = [0, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100]
_LX = [1, .77, .66, .63, .61, .58, .55, .51, .48, .44, .40, .36, .31, .26, .20, .14, .08, .04, .015, .004, 0]
_g = np.linspace(0, 100, 10001)
_l = np.interp(_g, _AG, _LX)
def PY(a, b):
    m = (_g >= a) & (_g <= b)
    return np.trapezoid(_l[m], _g[m]) if hasattr(np, 'trapezoid') else np.trapz(_l[m], _g[m])
E_GP = np.array([PY(25, 50), PY(50, 80), PY(80, 100), .03 * PY(0, 100), PY(18, 25), PY(12, 18),
                 PY(9, 12), PY(5, 9), PY(1, 5), PY(0, 1)])
E_AGE = np.array([PY(0, 1), PY(1, 5), PY(5, 9), PY(9, 12), PY(12, 18), PY(18, 25), PY(25, 50), PY(50, 80), PY(80, 100)])
T_CENSO = np.array([[740, 89, 601, 1846], [474, 96, 372, 973]], float)
T_TASA = np.array([[1196, 366, 500, 758], [1392, 234.5, 641, 483.5]], float)
H_BINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11]  # clases: 0,1..7,8-10,>=11
H_P = np.array([.03, .15, .19, .18, .15, .11, .08, .05, .05, .01])

def hbin(v):
    return np.digitize(v, H_BINS) - 1

def _spearman_windows(V, E):
    """V: B×n; devuelve B×nw de ρ de Spearman de cada ventana de len(E) con E."""
    w = len(E)
    W = sw(V, w, axis=1)                      # B×nw×w
    R = rankdata(W, axis=-1)
    R = R - R.mean(-1, keepdims=True)
    e = rankdata(E); e = e - e.mean()
    num = (R * e).sum(-1)
    den = np.sqrt((R ** 2).sum(-1) * (e ** 2).sum())
    with np.errstate(invalid='ignore', divide='ignore'):
        r = num / den
    return np.nan_to_num(r, nan=-1.0)

def P1a(V):
    return _spearman_windows(V, E_GP).max(1) if V.shape[1] >= 10 else None
def P1b(V):
    if V.shape[1] < 9: return None
    return np.maximum(_spearman_windows(V, E_AGE).max(1), _spearman_windows(V, E_AGE[::-1]).max(1))
def P1c(V):
    if V.shape[1] < 20: return None
    r = _spearman_windows(V, E_GP)
    return np.minimum(r[:, :-10], r[:, 10:]).max(1)
def P1d(V, onehot):
    if onehot is None: return None
    S = V @ onehot                            # B×G sumas de grupo (solo grupos con valor)
    return _spearman_windows(S, E_GP).max(1)

def _prop_windows(V, T):
    W = sw(V, 4, axis=1)
    pos = (W > 0).all(-1)
    P = W / np.where(pos, W.sum(-1), 1)[..., None]
    Tn = T / T.sum(1, keepdims=True)
    d = np.min([np.abs(P - t).sum(-1) for t in Tn], axis=0)
    d = np.where(pos, d, np.inf)
    out = -d.min(1)
    return np.where(np.isfinite(out), out, -9.0)
def P2(V):  return _prop_windows(V, T_CENSO) if V.shape[1] >= 4 else None
def P7c(V): return _prop_windows(V, T_TASA) if V.shape[1] >= 4 else None

def _count_windows(V, lo, hi, w):
    if V.shape[1] < w: return None
    x = ((V >= lo) & (V <= hi)).astype(int)
    c = np.concatenate([np.zeros((x.shape[0], 1), int), np.cumsum(x, 1)], 1)
    return (c[:, w:] - c[:, :-w]).max(1)
def P8b(V): return _count_windows(V, 28, 32, 12)
def P8c(V): return _count_windows(V, 38, 42, 9)

# ---------- composición (solo nulo de corpus) ----------
def P3(v, corpus_p):
    v = v[~np.isnan(v)]
    if len(v) < 10: return None
    b = hbin(v)
    return float(np.mean(np.log(H_P[b]) - np.log(corpus_p[b])))

def P12(vals, s1):
    m = (vals >= 8) & ~np.isnan(s1)
    if m.sum() < 8: return None
    s = s1[m]
    return float(np.mean((s >= 1) & (s <= 7)))

# ---------- estructuras de grupo ----------
def groups(k):
    """lista de arrays de índices de colgantes por grupo, en orden."""
    g = k['grp']; out = []; start = 0
    for i in range(1, len(g) + 1):
        if i == len(g) or g[i] != g[i - 1]:
            out.append(np.arange(start, i)); start = i
    return out

def modal_groups(G, lo, hi, minn):
    sz = Counter(len(x) for x in G if lo <= len(x) <= hi)
    if not sz: return None, None
    m, n = max(sz.items(), key=lambda t: (t[1], t[0]))
    if n < minn: return None, None
    return m, [x for x in G if len(x) == m]

def P4_prep(k):
    G = groups(k)
    G2 = [x for x in G if len(x) > 1]
    m, mg = modal_groups(G2, 4, 12, 6)
    if m is None: return None
    if sum(len(x) for x in mg) < .5 * sum(len(x) for x in G2): return None
    v = k['vals'][~np.isnan(k['vals'])]
    if len(v) == 0 or np.median(v) > 30: return None
    return np.array(mg)                        # R×m índices

def P4(C, idx):
    """C: B×n códigos de color; idx: R×m."""
    X = C[:, idx]                              # B×R×m
    out = np.empty(X.shape[0])
    for b in range(X.shape[0]):
        hom, mods = [], []
        for row in X[b]:
            vals, cnt = np.unique(row, return_counts=True)
            hom.append(cnt.max() / len(row)); mods.append(vals[cnt.argmax()])
        mods = np.array(mods)
        out[b] = np.mean(hom) + np.mean(mods[1:] != mods[:-1])
    return out

def P5a_prep(k):
    G = groups(k)
    m, mg = modal_groups(G, 8, 10, 4)
    if m is None: return None
    v = k['vals'][~np.isnan(k['vals'])]
    if len(v) == 0 or np.median(v) < 20: return None
    M = np.array(mg)
    comp = ~np.isnan(k['vals'][M]).any(1)
    if comp.sum() < 4: return None
    return M[comp]

def P5a(Vfull, M):
    X = Vfull[:, M]                            # B×R×m
    s = X.sum(-1, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        P = X / s
        cv = P.std(1) / P.mean(1)              # B×m
    return -np.nanmedian(np.where(np.isfinite(cv), cv, np.nan), 1)

def _grp_valued(k, minv):
    out = []
    for x in groups(k):
        y = x[~np.isnan(k['vals'][x])]
        if len(y) >= minv: out.append(y)
    return out

def P5b_prep(k):
    G = _grp_valued(k, 3)
    return G if len(G) >= 4 else None
def P5b(Vfull, G):
    first = np.array([x[0] for x in G])
    D = Vfull[:, first] - np.stack([Vfull[:, x[1:]].sum(1) for x in G], 1)
    out = np.zeros(len(D))
    for b, d in enumerate(D):
        d = d[(d >= 1) & (d <= 300)]
        if len(d): out[b] = np.unique(d, return_counts=True)[1].max()
    return out

def P5c_prep(k):
    T = []
    for x in _grp_valued(k, 3):
        for i in range(len(x) - 2): T.append(x[i:i + 3])
    return np.array(T) if len(T) >= 4 else None
def P5c(Vfull, T):
    X = Vfull[:, T]                            # B×nt×3
    hit = (X[..., 0] == X[..., 1] + X[..., 2]) & (X[..., 1] >= 2)
    out = np.zeros(len(X))
    for b in range(len(X)):
        c = X[b, hit[b], 1]
        if len(c): out[b] = np.unique(c, return_counts=True)[1].max()
    return out

def P6a_prep(k):
    G = _grp_valued(k, 2)
    return G if len(G) >= 3 else None
def P6a(Vfull, G):
    out = np.zeros(len(Vfull))
    allidx = np.concatenate(G)
    owner = np.concatenate([np.full(len(x), i) for i, x in enumerate(G)])
    for b in range(len(Vfull)):
        v = Vfull[b]; tot = [v[x].sum() for x in G]; n = 0
        for i, x in enumerate(G):
            if len(x) >= 3 and tot[i] >= 20 and 2 * v[x].max() == tot[i]: n += 1
        vals_other = v[allidx]
        for i, t in enumerate(tot):
            if t >= 10 and np.any(vals_other[owner != i] == t): n += 1
        out[b] = n
    return out

def P7a_prep(k):
    G = groups(k)
    m, mg = modal_groups(G, 3, 20, 4)
    if m is None: return None
    M = np.array(mg)
    pos = np.tile(np.arange(m), (len(M), 1))
    ok = ~np.isnan(k['vals'][M])
    if ok.sum() < 8: return None
    return M[ok], pos[ok]
def _eta(L, lab):
    """L: B×c (log valores), lab: c etiquetas -> η² por fila."""
    u, inv = np.unique(lab, return_inverse=True)
    oh = np.zeros((len(lab), len(u))); oh[np.arange(len(lab)), inv] = 1
    n = oh.sum(0); mu = (L @ oh) / n; gm = L.mean(1, keepdims=True)
    ssb = ((mu - gm) ** 2 * n).sum(1); sst = ((L - gm) ** 2).sum(1)
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.nan_to_num(ssb / sst)
def P7a(Vfull, prep):
    cells, pos = prep
    return _eta(np.log10(Vfull[:, cells] + 1), pos)

def P7b_prep(k):
    G = _grp_valued(k, 3)
    if not 11 <= len(G) <= 13: return None
    return np.concatenate(G), np.concatenate([np.full(len(x), i) for i, x in enumerate(G)])
P7b = P7a

def P8a_obs_null(k, B, rng):
    G = groups(k); sub = k['sub']
    units = []
    for x in G:
        if len(x) == 1 and units: units[-1] = np.concatenate([units[-1], x])
        else: units.append(x)
    U = len(units)
    if U < 3: return None, None
    def run(sizes):
        ok = (sizes >= 27) & (sizes <= 33); best = cur = 0
        for o in ok:
            cur = cur + 1 if o else 0; best = max(best, cur)
        return best
    obs = run(np.array([sub[x].sum() for x in units]))
    cs = np.concatenate([[0], np.cumsum(sub)]); n = len(sub)
    null = np.empty(B)
    for b in range(B):
        cuts = np.sort(rng.choice(np.arange(1, n), U - 1, replace=False))
        e = np.concatenate([[0], cuts, [n]])
        null[b] = run(cs[e[1:]] - cs[e[:-1]])
    return obs, null

def P9a(C):
    if C.shape[1] < 9: return None
    A = [np.mean(C[:, :-l] == C[:, l:], 1) for l in (1, 2, 3)]
    return A[2] - np.maximum(A[0], A[1])

def P9b(k):
    G = groups(k); n = len(k['vals']); sz = np.array([len(x) for x in G])
    iv = False
    for i in range(len(sz) - 3):
        s = np.sort(sz[i:i + 4])
        if np.all(np.abs(s - np.array([9, 9, 9, 14])) <= 1): iv = True; break
    return {'P9b_i': 40 <= n <= 42, 'P9b_ii': 326 <= k['ntot'] <= 352, 'P9b_iii': 161 <= n <= 167, 'P9b_iv': iv}

def P10(C):
    """C: B×n colores de cuerdas con valor positivo, en orden."""
    n = C.shape[1]
    if n < 11: return None
    best = np.full(C.shape[0], 0.0)
    for L in (11, 12, 13):
        if n < L: continue
        W = sw(C, L, axis=1)                   # B×nw×L
        def hom(X):
            s = np.sort(X, -1)
            # moda: longitud máxima de rachas en el arreglo ordenado
            eq = s[..., 1:] == s[..., :-1]
            run = np.zeros(X.shape[:-1]); cur = np.zeros(X.shape[:-1]); md = s[..., 0].copy()
            for j in range(eq.shape[-1]):
                cur = np.where(eq[..., j], cur + 1, 0)
                upd = cur > run; md = np.where(upd, s[..., j + 1], md); run = np.maximum(run, cur)
            return (run + 1) / X.shape[-1], md
        h1, m1 = hom(W[..., :5]); h2, m2 = hom(W[..., 5:])
        s = (h1 + h2) / 2 * (m1 != m2)
        best = np.maximum(best, s.max(1))
    return best

def P11_prep(k):
    G = [x for x in groups(k)]
    return G if sum(len(x) >= 3 for x in G) >= 3 else None
def P11(C, G, marker=False):
    out = np.zeros(len(C))
    for b in range(len(C)):
        c = C[b]; best = 0
        tup = [tuple(c[x]) for x in G]
        bysize = {}
        for i, t in enumerate(tup):
            if len(t) >= 3 and len(set(t)) > 1: bysize.setdefault(len(t), []).append(i)
        for L, ids in bysize.items():
            if len(ids) < 2: continue
            mod = np.array(Counter(tup[i] for i in ids).most_common(1)[0][0])
            n = 0
            for i in ids:
                if np.mean(np.array(tup[i]) == mod) >= .8:
                    if not marker: n += 1
                    elif i > 0:
                        pv = tup[i - 1]
                        if len(pv) == 1 or (len(pv) != L and Counter(pv).most_common(1)[0][0] not in set(mod)): n += 1
            best = max(best, n)
        out[b] = best
    return out

def P11c_prep(k):
    G = _grp_valued(k, 2)
    if len(G) < 8: return None
    heads = np.array([x[0] for x in G]); rest = np.concatenate([x[1:] for x in G])
    return heads, rest
def P11c(Vfull, prep):
    heads, rest = prep
    out = np.empty(len(Vfull))
    for b, v in enumerate(Vfull):
        allv = np.concatenate([v[heads], v[rest]])
        u, cnt = np.unique(allv, return_counts=True)
        once = set(u[cnt == 1])
        out[b] = np.mean([x in once for x in v[heads]]) - np.mean([x in once for x in v[rest]])
    return out


if __name__ == '__main__':   # comprobación mínima
    rng = np.random.default_rng(0)
    gp = E_GP[None, :] * 10
    assert abs(P1a(gp)[0] - 1) < 1e-9
    assert P2(np.array([[740, 89, 601, 1846.]]))[0] == 0
    assert P8b(np.array([[30.] * 12]))[0] == 12
    C = np.array([[0, 1, 2] * 5])
    assert P9a(C)[0] == 1
    print('ok', np.round(E_GP / E_GP.sum(), 3))


# ---------- REVISIONES (una por plantilla, documentadas en plantillas.md §3) ----------
def P4r_prep(k):
    v = k['vals'][~np.isnan(k['vals'])]
    if len(k['vals']) < 24 or len(v) == 0 or np.median(v) > 30: return None
    return True
def P4r(C):
    """registros = bandas de color (rachas de color idéntico); fracción de colgantes en bandas
    del largo modal k (4..12), exigiendo >= 6 bandas de ese largo; si no, 0."""
    out = np.zeros(len(C))
    for b, c in enumerate(C):
        cut = np.flatnonzero(c[1:] != c[:-1]) + 1
        runs = np.diff(np.concatenate([[0], cut, [len(c)]]))
        r = runs[(runs >= 4) & (runs <= 12)]
        if len(r) == 0: continue
        u, n = np.unique(r, return_counts=True)
        i = np.lexsort((u, n))[-1]
        if n[i] >= 6: out[b] = u[i] * n[i] / len(c)
    return out

def P8ar_obs_null(k, B, rng):
    """unidad = racha de grupos de 1 + el grupo siguiente (cuerda de lazo + colgantes, UR006);
    estadístico = n.º de unidades con 26..36 cuerdas (subárbol completo); nulo: cortes al azar."""
    G = groups(k); sub = k['sub']; units = []; pend = []
    for x in G:
        pend.append(x)
        if len(x) > 1: units.append(np.concatenate(pend)); pend = []
    if pend: units.append(np.concatenate(pend))
    U = len(units)
    if U < 3: return None, None
    f = lambda s: np.sum((s >= 26) & (s <= 36))
    obs = f(np.array([sub[x].sum() for x in units]))
    cs = np.concatenate([[0], np.cumsum(sub)]); n = len(sub)
    null = np.empty(B)
    for b in range(B):
        cuts = np.sort(rng.choice(np.arange(1, n), U - 1, replace=False))
        e = np.concatenate([[0], cuts, [n]])
        null[b] = f(cs[e[1:]] - cs[e[:-1]])
    return obs, null
