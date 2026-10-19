"""Pruebas internas T1-T7 sobre la frontera (diseno.md). Uso: python 01_internas.py [--nulo R] [--controles]"""
import sys, time
import numpy as np, pandas as pd
from comun import *
from scipy.stats import rankdata

ETAPAS = [999, 9999, 99999]
BMAX = 2
CH = 5000  # replicas por bloque


def en_bloques(fn, N, rng, *perm_args):
    out = []
    while N > 0:
        n = min(CH, N); out.append(fn(n, rng)); N -= n
    return np.concatenate(out)


def perm_filas(base, n, rng):
    return np.take_along_axis(np.broadcast_to(base, (n, len(base))), np.argsort(rng.random((n, len(base))), 1), 1)


def racha(E, W):
    """E,W (N, L): por fila, max suma de W en rachas de E con longitud >= 3."""
    E = E.astype(np.float64)
    Cw = np.cumsum(W * E, 1); Ce = np.cumsum(E, 1)
    lz_w = np.maximum.accumulate(np.where(E == 0, Cw, 0), 1)
    lz_e = np.maximum.accumulate(np.where(E == 0, Ce, 0), 1)
    rs = Cw - lz_w; rl = Ce - lz_e
    return np.where(rl >= 3, rs, 0).max(1) if E.shape[1] else np.zeros(E.shape[0])


def moda_cuenta(M):
    """M (N, L) valores; sentinelas unicos negativos no cuentan. max multiplicidad por fila."""
    S = np.sort(M, 1)
    eq = (S[:, 1:] == S[:, :-1]) & (S[:, 1:] >= 0)
    if eq.shape[1] == 0: return np.zeros(len(M))
    E = eq.astype(np.int64); c = np.cumsum(E, 1)
    lz = np.maximum.accumulate(np.where(E == 0, c, 0), 1)
    return (c - lz).max(1) + 1


# ---------- estadisticos vectorizados (X: N x n) ----------
def acf_prom(X, match=False, base=None):
    n = X.shape[1]; K = n // 3
    if K < 2: return None
    A = []
    for k in range(1, K + 2):
        if match:
            A.append((X[:, :-k] == X[:, k:]).mean(1) - base)
        else:
            A.append((X[:, :-k] * X[:, k:]).sum(1) / (X * X).sum(1) * n / (n - k))
    A = np.array(A)  # (K+1, N); A[k-1] = lag k
    best = np.full(X.shape[0], -1.0)
    for k in range(2, K + 1):
        pr = A[k - 1] - (A[k - 2] + A[k]) / 2
        best = np.maximum(best, np.where(A[k - 1] > 0, pr, -1.0))
    return best


def t1(v):
    """Enmienda 1: min-p de prominencia por rangos y por coincidencia exacta de valores no nulos."""
    if len(v) < 10 or len(set(v)) < 3: return None
    u, I = np.unique(v, return_inverse=True)
    r = pd.Series(v).rank().to_numpy(); r = r - r.mean()
    ru = np.zeros(len(u)); ru[I] = r  # rango (centrado) de cada valor distinto
    nz = v[v > 0]; base = ((np.unique(nz, return_counts=True)[1] / len(v)) ** 2).sum()
    nzu = u > 0
    def f(Ix):
        Ix = Ix.astype(int)
        a = acf_prom(ru[Ix])
        M = np.where(nzu[Ix], Ix, -1 - np.arange(Ix.shape[1])[None, :])  # ceros nunca coinciden
        b = acf_prom(M.astype(float), True, base)
        return np.vstack([a, b]).T
    return I.astype(float), f


def t2(col):
    if len(col) < 10 or len(set(col)) < 2: return None
    u, c = np.unique(col, return_inverse=True)
    base = ((np.bincount(c) / len(c)) ** 2).sum()
    return c.astype(float), lambda X: acf_prom(X, True, base)


def t3(v):
    if (v > 0).sum() < 6: return None
    u, I = np.unique(v, return_inverse=True)
    T = tol(u[:, None], u[None, :]) & (u[:, None] > 0) & (u[None, :] > 0)
    nz = v[v > 0]; vals, cnt = np.unique(nz, return_counts=True); fr = dict(zip(vals, cnt / len(nz)))
    wu = np.array([-np.log(fr[x]) if x > 0 else 0.0 for x in u])
    n = len(v)
    def f(Ix):
        Ix = Ix.astype(int); best = np.zeros(len(Ix))
        for d in range(1, n - 2):
            E = T[Ix[:, :-d], Ix[:, d:]]
            best = np.maximum(best, racha(E, wu[Ix[:, :-d]]))
        return best
    return I.astype(float), f


def t6(v, g):
    """Enmienda 1: min-p de (a) sumas a paso k = 2..12 y (b) sumas de la misma posicion en L >= 2 grupos consecutivos."""
    n = len(v)
    if n < 6 or (v >= 10).sum() == 0: return None
    gid = pd.factorize(g)[0]; ng = gid.max() + 1
    slot = np.zeros(n, int)
    for gg in range(ng):
        ix = np.where(gid == gg)[0]; slot[ix] = np.arange(len(ix))
    pos = {(gid[i], slot[i]): i for i in range(n)}
    listas = []  # (i, terminos en orden de L)
    for i in range(n):
        for d in (-1, 1):
            t = []; G = gid[i] + d
            while 0 <= G < ng and (G, slot[i]) in pos and len(t) < 12:
                t.append(pos[(G, slot[i])]); G += d
            if len(t) >= 2: listas.append((i, np.array(t)))
    def f(X):
        X = X.astype(np.int64); N = len(X)
        hit = np.zeros((N, n), bool); tgt = X >= 10
        for k in range(2, min(12, n // 2) + 1):
            for sgn in (1, -1):
                acc = np.zeros((N, n), np.int64); cnt = np.zeros((N, n), np.int64)
                for L in range(1, 13):
                    s = L * k
                    if s >= n: break
                    sh = np.zeros((N, n), np.int64)
                    if sgn == 1: sh[:, s:] = X[:, :-s]
                    else: sh[:, :-s] = X[:, s:]
                    acc += sh; cnt += sh > 0
                    if L >= 2:
                        valid = np.zeros(n, bool)
                        if sgn == 1: valid[s:] = True
                        else: valid[:n - s] = True
                        hit |= (acc == X) & tgt & (cnt >= 2) & valid
        hit2 = np.zeros((N, n), bool)
        for i, t in listas:
            T = X[:, t]; cs = np.cumsum(T, 1); cn = np.cumsum(T > 0, 1)
            hit2[:, i] |= ((cs[:, 1:] == X[:, [i]]) & (cn[:, 1:] >= 2)).any(1) & tgt[:, i]
        return np.vstack([hit.sum(1), hit2.sum(1)]).T.astype(float)
    return v.astype(float), f


def t7_esquemas(v, g):
    n = len(v); sch = {}
    sch["adyacentes0"] = (np.arange(0, n - 1, 2), np.arange(1, n, 2))
    sch["adyacentes1"] = (np.arange(1, n - 1, 2), np.arange(2, n, 2))
    a, b = [], []
    for gg in np.unique(g):
        ix = np.where(g == gg)[0]
        if len(ix) >= 4:
            h = len(ix) // 2; a += list(ix[:h]); b += list(ix[::-1][:h])
    sch["espejo_grupo"] = (np.array(a, int), np.array(b, int))
    h = n // 2; sch["espejo_total"] = (np.arange(h), np.arange(n - 1, n - 1 - h, -1))
    return {k: s for k, s in sch.items() if len(s[0]) >= 4}


def t7(v, g):
    sch = t7_esquemas(v, g)
    if not sch or (v > 0).sum() < 6: return None
    def f(X):
        X = X.astype(np.int64); out = []
        for k, (a, b) in sch.items():
            S = X[:, a] + X[:, b]
            bad = (S < 2) | ((X[:, a] == 0) & (X[:, b] == 0))
            S = np.where(bad, -1 - np.arange(len(a))[None, :], S)
            out.append(moda_cuenta(S))
        return np.array(out).T
    return v.astype(float), f, list(sch)


def t4(v, g):
    grupos = []
    for gg in np.unique(g):
        x = v[(g == gg) & (v > 0)]
        if len(x) >= 4: grupos.append(x)
    if not grupos: return None
    den = sum(len(x) * (len(x) - 1) / 2 for x in grupos)
    def kend(Xg):
        m = Xg.shape[1]; i, j = np.triu_indices(m, 1)
        return np.sign(Xg[:, j] - Xg[:, i]).sum(1)
    obs_s = [kend(x[None, :].astype(float))[0] for x in grupos]
    obs = sum(abs(s) for s in obs_s) / den
    def nulo(N, rng):
        tot = np.zeros(N)
        for x in grupos:
            tot += np.abs(kend(perm_filas(x.astype(float), N, rng)))
        return tot / den
    return obs, nulo, float(np.sign(sum(obs_s)))


def t5(pv, sv):
    m = (pv > 0) & (sv > 0); pv = pv[m]; sv = sv[m]
    if len(pv) < 5: return None
    n = len(pv); rp = pd.Series(pv).rank().to_numpy()
    def stats(S):  # S (N, n) subsidiarias
        R = np.round(S / pv[None, :], 9)
        Dm = np.where(pv[None, :] - S == 0, -1.0 - np.arange(n)[None, :], (pv[None, :] - S) + 1e12)
        rho = _corr_rows(rp, rankdata(S, axis=1))
        return np.vstack([moda_cuenta(R), moda_cuenta(Dm), np.nan_to_num(rho)]).T
    return sv.astype(float), stats


def _rank_rows(S):
    return np.apply_along_axis(lambda r: pd.Series(r).rank().to_numpy(), 1, S)


def _corr_rows(a, B):
    a = a - a.mean(); B = B - B.mean(1, keepdims=True)
    den = np.sqrt((a * a).sum() * (B * B).sum(1)); den[den == 0] = np.inf
    return (B @ a) / den


def p_minp(obs_vec, null_fn, rng_base, etapas=ETAPAS):
    """null_fn(N, rng) -> (N, S). min-p calibrado, escalada si b <= BMAX."""
    for N in etapas:
        rng = np.random.default_rng(rng_base)
        Z = np.concatenate([null_fn(min(CH, N - i), rng) for i in range(0, N, CH)])
        ps_obs = np.array([((Z[:, s] >= obs_vec[s] - 1e-12).sum() + 1) / (N + 1) for s in range(Z.shape[1])])
        # p de cada replica por rango
        Z = Z.astype(float); Pz = np.empty(Z.shape)
        for s in range(Z.shape[1]):
            srt = np.sort(Z[:, s])
            Pz[:, s] = (N - np.searchsorted(srt, Z[:, s] - 1e-12, "left") + 1) / (N + 1)
        mz = Pz.min(1); mo = ps_obs.min()
        b = int((mz <= mo + 1e-15).sum())
        if b > BMAX: break
    return (b + 1) / (N + 1), N, b, int(np.argmin(ps_obs))


def detalle_t1(v):
    r = pd.Series(v).rank().to_numpy(); r = r - r.mean(); n = len(v); K = n // 3
    A = [(r[:-k] * r[k:]).sum() / (r * r).sum() * n / (n - k) for k in range(1, K + 2)]
    pr = [(A[k - 1] - (A[k - 2] + A[k]) / 2) if A[k - 1] > 0 else -1 for k in range(2, K + 1)]
    li = 0
    nzv = np.where(v > 0, v, -1 - np.arange(n)); base = ((np.unique(v[v > 0], return_counts=True)[1] / n) ** 2).sum()
    B = [(nzv[:-k] == nzv[k:]).mean() - base for k in range(1, K + 2)]
    pb = [(B[k - 1] - (B[k - 2] + B[k]) / 2) if B[k - 1] > 0 else -1 for k in range(2, K + 1)]
    return f"{int(np.argmax(pr) + 2)}/{int(np.argmax(pb) + 2)}"


def correr(k, v, g, col, sp, sv, rng_semilla=SEMILLA):
    filas = []
    def simple(nombre, prep, extra=""):
        if prep is None:
            filas.append(dict(kfg=k, prueba=nombre, estadistico=np.nan, p=np.nan, N=0, detalle="NA")); return
        base, f = prep[0], prep[1]
        obs = float(f(base[None, :])[0])
        p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([f(perm_filas(base, min(CH, n - i), rng)) for i in range(0, n, CH)]), ETAPAS, BMAX)
        filas.append(dict(kfg=k, prueba=nombre, estadistico=obs, p=p, N=N, detalle=extra))
    def multi(nombre, prep, nombres, extra=""):
        if prep is None:
            filas.append(dict(kfg=k, prueba=nombre, estadistico=np.nan, p=np.nan, N=0, detalle="NA")); return
        base, st = prep[0], prep[1]; obs = st(base[None, :])[0]
        p, N, b, w = p_minp(obs, lambda n, rng: st(perm_filas(base, n, rng)), SEMILLA)
        filas.append(dict(kfg=k, prueba=nombre, estadistico=float(obs[w]), p=p, N=N, detalle=f"{nombres[w]};{extra}"))
    multi("T1_periodo_valor", t1(v), ["rangos", "iguales"], f"lag_rangos/iguales={detalle_t1(v)}" if t1(v) else "")
    pc = t2(col)
    if pc:
        u, c = np.unique(col, return_inverse=True); n = len(c); K = n // 3; base = ((np.bincount(c) / n) ** 2).sum()
        A = [(c[:-kk] == c[kk:]).mean() - base for kk in range(1, K + 2)] if K >= 2 else []
        lag = int(np.argmax([(A[kk - 1] - (A[kk - 2] + A[kk]) / 2) if A[kk - 1] > 0 else -1 for kk in range(2, K + 1)]) + 2) if K >= 2 else 0
        simple("T2_periodo_color", pc, f"lag={lag};colores={len(u)}")
    else:
        simple("T2_periodo_color", None)
    simple("T3_repeticion", t3(v))
    r4 = t4(v, g)
    if r4 is None: filas.append(dict(kfg=k, prueba="T4_tendencia", estadistico=np.nan, p=np.nan, N=0, detalle="NA"))
    else:
        obs, nul, sg = r4
        p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([nul(min(CH, n - i), rng) for i in range(0, n, CH)]), ETAPAS, BMAX)
        filas.append(dict(kfg=k, prueba="T4_tendencia", estadistico=obs, p=p, N=N, detalle=f"signo={sg:+.0f}"))
    pv = v[sp] if len(sp) else np.array([], np.int64)
    r5 = t5(pv, sv) if len(sp) else None
    if r5 is None: filas.append(dict(kfg=k, prueba="T5_subsidiaria", estadistico=np.nan, p=np.nan, N=0, detalle="NA"))
    else:
        base, st = r5; obs = st(base[None, :])[0]
        p, N, b, w = p_minp(obs, lambda n, rng: st(perm_filas(base, n, rng)), SEMILLA)
        filas.append(dict(kfg=k, prueba="T5_subsidiaria", estadistico=float(obs[w]), p=p, N=N, detalle=["razon_modal", "dif_modal", "spearman"][w] + f";obs={np.round(obs,3).tolist()}"))
    multi("T6_suma_salteada", t6(v, g), ["paso_k", "misma_posicion"])
    r7 = t7(v, g)
    if r7 is None: filas.append(dict(kfg=k, prueba="T7_pares_suma", estadistico=np.nan, p=np.nan, N=0, detalle="NA"))
    else:
        base, st, nombres = r7; obs = st(base[None, :])[0]
        p, N, b, w = p_minp(obs, lambda n, rng: st(perm_filas(base, n, rng)), SEMILLA)
        filas.append(dict(kfg=k, prueba="T7_pares_suma", estadistico=float(obs[w]), p=p, N=N, detalle=nombres[w]))
    return filas


def quipu_nulo(q, r):
    """Frontera nula: permutacion de colgantes (tamanos de grupo fijos), colores y subsidiarias independientes."""
    rng = np.random.default_rng(SEMILLA + 1000 * r + FRONTERA.index(q.k))
    return rng.permutation(q.v), q.g, rng.permutation(q.col), q.sub_padre, rng.permutation(q.sub_v)


def sinteticos():
    rng = np.random.default_rng(SEMILLA)
    pool = np.concatenate([quipu(k).v for k in FRONTERA]); pool = pool[(pool > 0) & (pool < 500)]
    base = lambda n: rng.choice(pool, n)
    out = {}
    v = np.tile(base(5), 6); out["T1_periodo_valor"] = (v, np.repeat(np.arange(6), 5), np.array(["W"] * 30), np.array([], int), np.array([], np.int64))
    col = np.tile(np.array(list("ABCD")), 8); v = base(32)
    out["T2_periodo_color"] = (v, np.zeros(32, int), col, np.array([], int), np.array([], np.int64))
    v = base(30); v[20:26] = v[3:9]; out["T3_repeticion"] = (v, np.repeat(np.arange(5), 6), np.array(["W"] * 30), np.array([], int), np.array([], np.int64))
    v = np.concatenate([np.sort(base(6)) for _ in range(5)]); out["T4_tendencia"] = (v, np.repeat(np.arange(5), 6), np.array(["W"] * 30), np.array([], int), np.array([], np.int64))
    v = base(20) * 10; sp = np.arange(12); sv = v[sp] // 10
    out["T5_subsidiaria"] = (v, np.zeros(20, int), np.array(["W"] * 20), sp, sv)
    v = base(24) % 50 + 1
    for j in (0, 2, 4): v[18 + j] = v[j] + v[6 + j] + v[12 + j]
    out["T6_suma_salteada"] = (v, np.repeat(np.arange(4), 6), np.array(["W"] * 24), np.array([], int), np.array([], np.int64))
    v = base(24) % 49 + 1
    for gg in range(4):
        ix = np.arange(gg * 6, gg * 6 + 6); v[ix[3:]] = 50 - v[ix[:3]][::-1]
    out["T7_pares_suma"] = (v, np.repeat(np.arange(4), 6), np.array(["W"] * 24), np.array([], int), np.array([], np.int64))
    return out


if __name__ == "__main__":
    t0 = time.time()
    if "--controles" in sys.argv:
        filas = []
        for prueba, (v, g, col, sp, sv) in sinteticos().items():
            r = [x for x in correr("SINT_" + prueba[:2], v, g, col, sp, sv) if x["prueba"] == prueba][0]
            filas.append(r); print(prueba, r["p"], r["N"], r["detalle"], flush=True)
        pd.DataFrame(filas).to_csv(AQUI / "controles_internos.csv", index=False)
        sys.exit()
    rnulo = int(sys.argv[sys.argv.index("--nulo") + 1]) if "--nulo" in sys.argv else None
    filas = []
    for i, k in enumerate(FRONTERA):
        q = quipu(k)
        args = quipu_nulo(q, rnulo) if rnulo is not None else (q.v, q.g, q.col, q.sub_padre, q.sub_v)
        filas += correr(k, *args)
        if i % 20 == 0: print(i, k, round(time.time() - t0), flush=True)
    out = AQUI / (f"internas_nulo{rnulo}.csv" if rnulo is not None else "internas.csv")
    pd.DataFrame(filas).to_csv(out, index=False)
    print("listo", out, round(time.time() - t0), "s")
