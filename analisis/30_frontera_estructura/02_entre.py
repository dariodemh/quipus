"""Pruebas entre quipus I1-I9 (diseno.md). Uso: python 02_entre.py [--nulo R] [--controles] [--desde i --hasta j]"""
import sys, time
import numpy as np, pandas as pd
from comun import *

ETAPAS = [199, 1999, 19999, 99999]
BMAX = 1
PRESUP = 300.0
LMAX = 12


def concat(partners):
    vals, own, gid = [], [], []
    for i, p in enumerate(partners):
        q = quipu(p)
        vals += list(q.v) + [-1]; own += [i] * len(q.v) + [-1]
        gid += [f"{i}_{x}" for x in q.g] + ["sep"]
    return np.array(vals, np.int64), np.array(own), np.array(gid)


def shift(X, fill=0):
    Y = np.empty_like(X); Y[:, 1:] = X[:, :-1]; Y[:, 0] = fill
    return Y


def chunks(N, size):
    i = 0
    while i < N:
        yield min(size, N - i); i += size


# ---------- rachas I1-I4: F permutado (filas de indices de valores distintos) ----------
def prep_rachas(v, B):
    u, I = np.unique(v, return_inverse=True)
    nz = v[v > 0]; vals, cnt = np.unique(nz, return_counts=True); fr = dict(zip(vals, cnt / max(len(nz), 1)))
    wu = np.array([-np.log(fr[x]) if x > 0 else 0.0 for x in u])
    TB = tol(u[:, None], B[None, :]) & (u[:, None] > 0) & (B[None, :] > 0)
    return u, I, wu, TB


def stat_racha(Ix, modo, u, wu, TB, B, own, detalle=False):
    """Enmienda 2: Ix (N, n) indices de valores de F (ya invertido si I2). Para cada companero, suma de pesos
    de las posiciones de F cubiertas por rachas (>= 3) con ese companero; max sobre companeros.
    Tolera huecos y sustituciones entre tramos."""
    N, n = Ix.shape; M = len(B); P = int(own.max()) + 1
    trip = []; W = wu[Ix]
    S = np.zeros((N, M)); Lc = np.zeros((N, M)); Eprev = np.zeros((N, M), bool)
    Bpos = B > 0; Bsh = np.concatenate([[0], B[:-1]]); Bpos_sh = np.concatenate([[False], Bpos[:-1]])
    Fprev = None
    for i in range(n):
        Fi = u[Ix[:, i]]; wi = wu[Ix[:, i]][:, None]
        if modo == "copia":
            E = TB[Ix[:, i]]
            S = np.where(E, shift(S) + wi, 0); Lc = np.where(E, shift(Lc) + 1, 0)
        else:
            if Fprev is None:
                Fprev = Fi; wprev = wi; S[:] = 0; Lc[:] = 0; Eprev[:] = False; continue
            valid = (Fi > 0)[:, None] & Bpos[None, :] & (Fprev > 0)[:, None] & Bpos_sh[None, :]
            if modo == "diferencia":
                E = valid & ((B[None, :] - Fi[:, None]) == (Bsh[None, :] - Fprev[:, None])) & (B[None, :] != Fi[:, None])
            else:  # razon
                E = valid & (B[None, :] * Fprev[:, None] == Bsh[None, :] * Fi[:, None]) & (B[None, :] != Fi[:, None])
            Ep = shift(Eprev, False)
            S = np.where(E, np.where(Ep, shift(S), wprev) + wi, 0)
            Lc = np.where(E, np.where(Ep, shift(Lc), 1) + 1, 0)
            Eprev = E; Fprev = Fi; wprev = wi
        r, j = np.nonzero(Lc >= 3)
        if len(r):
            for d in (0, 1, 2): trip.append((r * n + (i - d)) * P + own[j])
    out = np.zeros(N)
    if not trip: return (out, None) if detalle else out
    t = np.unique(np.concatenate(trip))
    rp = (t // (n * P)) * P + t % P
    w = W.ravel()[t // P]
    tot = np.bincount(rp, weights=w, minlength=N * P).reshape(N, P)
    if detalle:
        pbest = int(tot[0].argmax()); cubiertas = int(((t % P) == pbest).sum())
        return tot.max(1), (pbest, cubiertas)
    return tot.max(1)


def mejor_companero_racha(Ix, modo, u, wu, TB, B, own):
    """Para el observado: companero y posicion de la mejor racha (solo informativo)."""
    n = Ix.shape[1]; M = len(B); bestv = 0; arg = None
    S = np.zeros((1, M)); Lc = np.zeros((1, M)); Eprev = np.zeros((1, M), bool); Fprev = None
    Bpos = B > 0; Bsh = np.concatenate([[0], B[:-1]]); Bpos_sh = np.concatenate([[False], Bpos[:-1]])
    for i in range(n):
        Fi = u[Ix[:, i]]; wi = wu[Ix[:, i]][:, None]
        if modo == "copia":
            E = TB[Ix[:, i]]; S = np.where(E, shift(S) + wi, 0); Lc = np.where(E, shift(Lc) + 1, 0)
        else:
            if Fprev is None:
                Fprev = Fi; wprev = wi; continue
            valid = (Fi > 0)[:, None] & Bpos[None, :] & (Fprev > 0)[:, None] & Bpos_sh[None, :]
            if modo == "diferencia":
                E = valid & ((B[None, :] - Fi[:, None]) == (Bsh[None, :] - Fprev[:, None])) & (B[None, :] != Fi[:, None])
            else:
                E = valid & (B[None, :] * Fprev[:, None] == Bsh[None, :] * Fi[:, None]) & (B[None, :] != Fi[:, None])
            Ep = shift(Eprev, False)
            S = np.where(E, np.where(Ep, shift(S), wprev) + wi, 0); Lc = np.where(E, np.where(Ep, shift(Lc), 1) + 1, 0)
            Eprev = E; Fprev = Fi; wprev = wi
        z = np.where(Lc >= 3, S, 0)[0]
        if z.max() > bestv:
            j = int(z.argmax()); bestv = z.max(); arg = (int(own[j]), i, j, int(Lc[0, j]))
    return arg


# ---------- I5 grupos permutados ----------
def lis(a):
    import bisect
    t = []
    for x in a:
        i = bisect.bisect_left(t, x)
        if i == len(t): t.append(x)
        else: t[i] = x
    return len(t)


def prep_grupos(g, partners):
    gid = pd.factorize(g)[0]
    fgr = [np.where(gid == x)[0] for x in range(gid.max() + 1)]
    fgr = [ix for ix in fgr if len(ix) >= 2]
    bylen = {}
    for pi, p in enumerate(partners):
        q = quipu(p); pg = pd.factorize(q.g)[0]
        for x in range(pg.max() + 1 if len(pg) else 0):
            vals = q.v[pg == x]
            if len(vals) >= 2 and (vals > 0).sum() >= 2:
                bylen.setdefault(len(vals), []).append((pi, x, vals))
    bylen = {L: (np.array([a for a, _, _ in l]), np.array([b for _, b, _ in l]), np.array([c for _, _, c in l])) for L, l in bylen.items()}
    return fgr, bylen


def stat_grupos(X, fgr, bylen, devolver=False):
    N = len(X); out = np.zeros(N); info = None
    cand = []  # por grupo de F: (N, G) coincidencias
    for ix in fgr:
        L = len(ix)
        if L not in bylen: cand.append(None); continue
        own, gx, P = bylen[L]
        Fg = X[:, ix]
        ok = (Fg > 0).sum(1) >= 2
        m = tol(Fg[:, None, :], P[None, :, :]).all(2) & ok[:, None]
        cand.append((m, own, gx))
    for r in range(N):
        porp = {}
        for gi, c in enumerate(cand):
            if c is None: continue
            m, own, gx = c
            hit = np.where(m[r])[0]
            for h in hit:
                d = porp.setdefault(own[h], {})
                if gi not in d: d[gi] = gx[h]
        best = 0
        for p, d in porp.items():
            if len(d) >= 2:
                idx = [d[gi] for gi in sorted(d)]
                val = len(d) - lis(idx)
                if val > best: best = val; info = (p, len(d), val)
        out[r] = best
    return (out, info) if devolver else out


# ---------- I6/I8: derivados de F en companeros ----------
def sumas_bloque(X):
    """X (N, n) -> (N, K) sumas de bloques contiguos L=2..12 con >=2 no nulos; invalidas = -1."""
    N, n = X.shape; cs = np.concatenate([np.zeros((N, 1), np.int64), np.cumsum(X, 1)], 1)
    cz = np.concatenate([np.zeros((N, 1), np.int64), np.cumsum(X > 0, 1)], 1)
    out = []
    for L in range(2, LMAX + 1):
        if L > n: break
        s = cs[:, L:] - cs[:, :-L]; z = cz[:, L:] - cz[:, :-L]
        out.append(np.where((z >= 2) & (s >= 10), s, -1))
    return np.concatenate(out, 1) if out else np.full((N, 1), -1)


def prep_tabla_variantes(partners):
    """tabla ordenada (variante, companero, cuerda) para cuerdas >= 10 de cada companero (todos los niveles)."""
    rows = []
    for pi, p in enumerate(partners):
        for ci, x in enumerate(quipu(p).todos):
            if x >= 10:
                for w in variantes(int(x)): rows.append((w, pi, ci))
    if not rows: return None
    a = np.array(rows, np.int64); a = a[np.argsort(a[:, 0], kind="stable")]
    return a


def contar_hits(vals_por_fila, tabla, npart):
    """vals_por_fila (N, K) valores; cuenta por fila el max sobre companeros de cuerdas distintas acertadas."""
    N = len(vals_por_fila); out = np.zeros(N)
    keys = tabla[:, 0]
    for r in range(N):
        u = np.unique(vals_por_fila[r]); u = u[u >= 10]
        lo = np.searchsorted(keys, u, "left"); hi = np.searchsorted(keys, u, "right")
        if (hi - lo).sum() == 0: continue
        idx = np.concatenate([np.arange(a, b) for a, b in zip(lo, hi) if b > a])
        pc = np.unique(tabla[idx, 1] * 100000 + tabla[idx, 2])
        out[r] = np.bincount(pc // 100000).max()
    return out


def stat_totales_F(X, fgr_all, sets):
    """I8: totales de grupo de F (>=2 no nulos, >=10) presentes (exacto) en cada companero; max."""
    N = len(X); T = []
    for ix in fgr_all:
        Xi = X[:, ix]; t = Xi.sum(1); T.append(np.where(((Xi > 0).sum(1) >= 2) & (t >= 10), t, -1))
    if not T: return np.zeros(N)
    T = np.array(T).T
    best = np.zeros(N)
    for s in sets:
        best = np.maximum(best, np.isin(T, s).sum(1))
    return best


# ---------- I7/I9: derivados de companeros en F ----------
def permutar_segmentos(B, own, N, rng):
    """permuta los colgantes de cada companero (las posiciones de separador quedan fijas)."""
    key = own[None, :] * 1.0 + rng.random((N, len(B))) * 0.5
    key[:, own < 0] = np.where(own < 0)[0][None, :] * 0 - 1  # separadores
    # orden estable por companero: reordena solo dentro de cada segmento
    out = np.empty((N, len(B)), np.int64)
    segs = [np.where(own == i)[0] for i in range(own.max() + 1)]
    for ix in segs:
        if len(ix) == 0: continue
        out[:, ix] = B[ix][np.argsort(rng.random((N, len(ix))), 1)]
    out[:, own < 0] = -1
    return out


def stat_bloques_companeros(Xb, own, fvar_keys, fvar_cord):
    """I7: sumas de bloque (L 2..12) de cada companero que igualan con tol una cuerda de F; max sobre companeros de cuerdas de F distintas."""
    N, M = Xb.shape
    sep = (Xb < 0)
    Xc = np.where(sep, 0, Xb)
    cs = np.concatenate([np.zeros((N, 1), np.int64), np.cumsum(Xc, 1)], 1)
    cz = np.concatenate([np.zeros((N, 1), np.int64), np.cumsum(Xc > 0, 1)], 1)
    csep = np.concatenate([np.zeros((N, 1), np.int64), np.cumsum(sep, 1)], 1)
    rr, oo, vv = [], [], []
    for L in range(2, LMAX + 1):
        s = cs[:, L:] - cs[:, :-L]; z = cz[:, L:] - cz[:, :-L]; e = csep[:, L:] - csep[:, :-L]
        ok = (z >= 2) & (s >= 10) & (e == 0)
        ok &= np.isin(s, fvar_keys)
        r, j = np.nonzero(ok)
        rr.append(r); oo.append(own[j]); vv.append(s[r, j])
    r = np.concatenate(rr); o = np.concatenate(oo); v = np.concatenate(vv)
    out = np.zeros(N)
    if len(r) == 0: return out
    lo = np.searchsorted(fvar_keys, v, "left"); hi = np.searchsorted(fvar_keys, v, "right")
    rep = hi - lo
    R = np.repeat(r, rep); O = np.repeat(o, rep)
    idx = np.concatenate([np.arange(a, b) for a, b in zip(lo, hi)])
    Cc = fvar_cord[idx]
    key = np.unique((R * 10000 + O) * 10000 + Cc)
    ro = key // 10000
    cnt = np.bincount(ro)
    rows = np.nonzero(cnt)[0]
    np.maximum.at(out, rows // 10000, cnt[rows])
    return out


def stat_totales_companeros(Xb, gsegs, gown, fset):
    """I9: totales de grupo (>=2 no nulos, >=10) de cada companero que aparecen exactos en F; max sobre companeros."""
    N = len(Xb); out = np.zeros(N)
    if not gsegs: return out
    T = np.array([Xb[:, ix].sum(1) for ix in gsegs]).T
    Z = np.array([(Xb[:, ix] > 0).sum(1) for ix in gsegs]).T
    H = np.isin(T, fset) & (Z >= 2) & (T >= 10)
    for o in np.unique(gown):
        out = np.maximum(out, H[:, gown == o].sum(1))
    return out


def correr(k, v, g, partners, psitio, fnulo_seed=None):
    """Devuelve filas I1..I9 para un quipu con secuencia v y grupos g."""
    filas = []; t0 = time.time()
    q = quipu(k)
    todos_F = q.todos
    gid = pd.factorize(g)[0]
    fgr_all = [np.where(gid == x)[0] for x in range(gid.max() + 1)]
    def fila(nombre, obs, p, N, det=""):
        filas.append(dict(kfg=k, prueba=nombre, estadistico=obs, p=p, N=N, detalle=det))
    # I1-I4
    B, own, _ = concat(partners)
    if (v > 0).sum() >= 3 and len(B):
        u, I, wu, TB = prep_rachas(v, B)
        for nombre, modo, inv in [("I1_copia", "copia", False), ("I2_invertida", "copia", True),
                                  ("I3_diferencia", "diferencia", False), ("I4_razon", "razon", False)]:
            def st(Ix): return stat_racha(Ix[:, ::-1] if inv else Ix, modo, u, wu, TB, B, own)
            obs = float(st(I[None, :])[0])
            def nul(N, rng):
                return np.concatenate([st(np.argsort(rng.random((c, len(I))), 1).choose(I) if False else I[np.argsort(rng.random((c, len(I))), 1)]) for c in chunks(N, 400)])
            if obs > 0:
                p, N, b = p_escalada(obs, nul, ETAPAS, BMAX, PRESUP)
                _, a = stat_racha((I[::-1] if inv else I)[None, :], modo, u, wu, TB, B, own, True)
                det = f"companero={partners[a[0]]};posiciones_F_cubiertas={a[1]}"
            else:
                p, N, det = 1.0, 0, "sin racha >= 3"
            fila(nombre, obs, p, N, det)
    else:
        for nombre in ["I1_copia", "I2_invertida", "I3_diferencia", "I4_razon"]: fila(nombre, np.nan, np.nan, 0, "NA")
    # I5
    fgr, bylen = prep_grupos(g, partners)
    if len(fgr) >= 2 and bylen:
        obs_arr, info = stat_grupos(v[None, :], fgr, bylen, True); obs = float(obs_arr[0])
        if obs > 0:
            p, N, b = p_escalada(obs, lambda N, rng: np.concatenate([stat_grupos(v[np.argsort(rng.random((c, len(v))), 1)], fgr, bylen) for c in chunks(N, 2000)]), ETAPAS, BMAX, PRESUP)
            det = f"companero={partners[info[0]]};emparejados={info[1]};desplazados={info[2]}"
        else:
            p, N, det = 1.0, 0, "ningun grupo desplazado"
        fila("I5_grupos_permutados", obs, p, N, det)
    else:
        fila("I5_grupos_permutados", np.nan, np.nan, 0, "NA")
    # I6
    tabla = prep_tabla_variantes(partners)
    if tabla is not None and (v > 0).sum() >= 2:
        st6 = lambda X: contar_hits(sumas_bloque(X), tabla, len(partners))
        obs = float(st6(v[None, :])[0])
        p, N, b = p_escalada(obs, lambda N, rng: np.concatenate([st6(v[np.argsort(rng.random((c, len(v))), 1)]) for c in chunks(N, 2000)]), ETAPAS, BMAX, PRESUP) if obs > 0 else (1.0, 0, 0)
        fila("I6_suma_bloque_F_en_otro", obs, p, N)
    else:
        fila("I6_suma_bloque_F_en_otro", np.nan, np.nan, 0, "NA")
    # I7
    fv = sorted({(w, ci) for ci, x in enumerate(todos_F) if x >= 10 for w in variantes(int(x))})
    if fv and len(B):
        fk = np.array([a for a, _ in fv], np.int64); fc = np.array([b for _, b in fv], np.int64)
        obs = float(stat_bloques_companeros(B[None, :], own, fk, fc)[0])
        nul7 = lambda N, rng: np.concatenate([stat_bloques_companeros(permutar_segmentos(B, own, c, rng), own, fk, fc) for c in chunks(N, 100)])
        p, N, b = p_escalada(obs, nul7, ETAPAS, BMAX, PRESUP) if obs > 0 else (1.0, 0, 0)
        fila("I7_suma_bloque_otro_en_F", obs, p, N)
    else:
        fila("I7_suma_bloque_otro_en_F", np.nan, np.nan, 0, "NA")
    # I8 / I9 (companeros del sitio)
    if psitio:
        sets = [np.unique(quipu(p).todos) for p in psitio]
        if any(len(ix) >= 2 for ix in fgr_all):
            st8 = lambda X: stat_totales_F(X, fgr_all, sets)
            obs = float(st8(v[None, :])[0])
            if obs > 0:
                p, N, b = p_escalada(obs, lambda N, rng: np.concatenate([st8(v[np.argsort(rng.random((c, len(v))), 1)]) for c in chunks(N, 5000)]), ETAPAS, BMAX, PRESUP)
                hits = [psitio[i] for i, s in enumerate(sets) if st8_one(v, fgr_all, s) == obs]
                det = "companeros=" + "|".join(hits[:5])
            else:
                p, N, det = 1.0, 0, ""
            fila("I8_total_grupo_F_en_sitio", obs, p, N, det)
        else:
            fila("I8_total_grupo_F_en_sitio", np.nan, np.nan, 0, "NA")
        Bs, owns, gids = concat(psitio)
        gsegs, gown = [], []
        for gname in pd.unique(gids[owns >= 0]):
            ix = np.where(gids == gname)[0]
            if len(ix) >= 2: gsegs.append(ix); gown.append(owns[ix[0]])
        gown = np.array(gown)
        fset = np.unique(todos_F[todos_F >= 10])
        if gsegs and len(fset):
            st9 = lambda Xb: stat_totales_companeros(Xb, gsegs, gown, fset)
            obs = float(st9(Bs[None, :])[0])
            if obs > 0:
                p, N, b = p_escalada(obs, lambda N, rng: np.concatenate([st9(permutar_segmentos(Bs, owns, c, rng)) for c in chunks(N, 500)]), ETAPAS, BMAX, PRESUP)
                H = stat_totales_por_companero(Bs, gsegs, gown, fset)
                det = "companeros=" + "|".join(psitio[o] for o, c in H if c == obs)[:200]
            else:
                p, N, det = 1.0, 0, ""
            fila("I9_total_grupo_sitio_en_F", obs, p, N, det)
        else:
            fila("I9_total_grupo_sitio_en_F", np.nan, np.nan, 0, "NA")
    else:
        fila("I8_total_grupo_F_en_sitio", np.nan, np.nan, 0, "NA sin companeros de sitio")
        fila("I9_total_grupo_sitio_en_F", np.nan, np.nan, 0, "NA sin companeros de sitio")
    for f in filas: f["seg"] = round(time.time() - t0, 1)
    return filas


def st8_one(v, fgr_all, s):
    return stat_totales_F(v[None, :], fgr_all, [s])[0]


def stat_totales_por_companero(Bs, gsegs, gown, fset):
    T = np.array([Bs[ix].sum() for ix in gsegs]); Z = np.array([(Bs[ix] > 0).sum() for ix in gsegs])
    H = np.isin(T, fset) & (Z >= 2) & (T >= 10)
    return [(o, int(H[gown == o].sum())) for o in np.unique(gown)]


def nulo_frontera(k, r):
    """Una realizacion del nulo: F con colgantes permutados (tamanos de grupo fijos)."""
    q = quipu(k); rng = np.random.default_rng(SEMILLA + 1000 * r + FRONTERA.index(k))
    return rng.permutation(q.v), q.g


if __name__ == "__main__":
    t0 = time.time()
    if "--controles" in sys.argv:
        filas = []
        # I2: UR1107 frente a UR237 (mismo objeto, invertido)
        k = "UR1107"; P = companeros(k, "amplio") + ["UR237"]
        filas += [dict(f, control="I2 UR1107~UR237") for f in correr(k, quipu(k).v, quipu(k).g, P, []) if f["prueba"] in ("I2_invertida", "I1_copia")]
        k = "UR1084"; P = sorted(set(companeros(k, "amplio")) | {"HP055"})
        filas += [dict(f, control="I1 UR1084~HP055") for f in correr(k, quipu(k).v, quipu(k).g, P, []) if f["prueba"] == "I1_copia"]
        k = "UR278"
        filas += [dict(f, control="I8 UR278->Incahuasi") for f in correr(k, quipu(k).v, quipu(k).g, ["UR266"], companeros(k, "sitio")) if f["prueba"].startswith("I8")]
        df = pd.DataFrame(filas); print(df[["control", "prueba", "estadistico", "p", "N", "detalle"]].to_string())
        df.to_csv(AQUI / "controles_entre.csv", index=False)
        sys.exit()
    rnulo = int(sys.argv[sys.argv.index("--nulo") + 1]) if "--nulo" in sys.argv else None
    a = int(sys.argv[sys.argv.index("--desde") + 1]) if "--desde" in sys.argv else 0
    b = int(sys.argv[sys.argv.index("--hasta") + 1]) if "--hasta" in sys.argv else len(FRONTERA)
    filas = []
    for i, k in enumerate(FRONTERA[a:b], start=a):
        if rnulo is None:
            v, g = quipu(k).v, quipu(k).g
        else:
            v, g = nulo_frontera(k, rnulo)
        filas += correr(k, v, g, companeros(k, "amplio"), companeros(k, "sitio"))
        print(i, k, round(time.time() - t0), flush=True)
    suf = (f"_nulo{rnulo}" if rnulo is not None else "") + (f"_{a}_{b}" if (a, b) != (0, len(FRONTERA)) else "")
    pd.DataFrame(filas).to_csv(AQUI / f"entre{suf}.csv", index=False)
    print("listo", round(time.time() - t0), "s")
