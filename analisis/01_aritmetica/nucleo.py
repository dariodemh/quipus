"""Núcleo compartido: carga de quipus y detectores aritméticos (numba) con nulos por permutación.

Convenciones
- valor 0 sin nudos = cuerda AUSENTE (no es un cero real): se queda fija en su sitio al permutar y no cuenta como sumando.
- Relaciones (todas con igualdad exacta):
  R1  colgante/subsidiaria = suma de sus subsidiarias directas (>=2 subsidiarias no nulas)
  F   colgante = suma de un tramo contiguo de colgantes inmediatamente a su izquierda o derecha (2..CAPF sumandos)
  A   igual, pero el tramo empieza/termina en frontera de grupo (suma de grupos enteros, 2..CAPA sumandos)
  TA  A restringida a cuerdas con union T (cuerda superior)
  R4  grupo C = suma cuerda a cuerda de k=2..4 grupos contiguos del mismo tamaño (izq. o der.)
  R5a grupo D de n cuerdas = (totales de los n grupos contiguos inmediatos a izq. o der.), un grupo por cuerda
  R5b total de un grupo = suma de los totales de k=2..6 grupos contiguos (izq. o der.)
"""
import numpy as np, pandas as pd
from pathlib import Path
from numba import njit

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "analisis/datos"
CAPF, CAPA = 10, 40
NS = 16  # longitud del vector de estadísticos
NOMBRES = ["R1", "R1_elig", "F", "A", "TA", "TA_elig", "R4", "R4_elig", "R5a", "R5a_elig", "R5b", "R5b_elig", "cuerdas_pos", "Fany", "Fsub", "Fsub_elig"]


def cargar():
    c = pd.read_csv(DATOS / "cuerdas.csv", low_memory=False)
    q = pd.read_csv(DATOS / "quipus.csv")
    c["valor"] = c["valor"].fillna(0).round().astype("int64")
    c["pres"] = c["nudos"].notna() | (c["valor"] > 0)
    out = {}
    for k, d in c.groupby("kfg", sort=False):
        d = d.sort_values("orden").reset_index(drop=True)
        idx = {n: i for i, n in enumerate(d["cuerda"])}
        par = np.array([idx.get(p, -1) if isinstance(p, str) else -1 for p in d["padre"]], dtype=np.int64)
        lvl = d["nivel"].values.astype(np.int64)
        L0 = np.where(lvl == 0)[0].astype(np.int64)
        g = d["grupo"].values[L0]
        gs = np.concatenate([[0], np.where(np.diff(g) != 0)[0] + 1, [len(L0)]]).astype(np.int64)
        out[k] = dict(kfg=k, v=d["valor"].values.astype(np.int64), pres=d["pres"].values, par=par, lvl=lvl, L0=L0,
                      sub=(lvl > 0), isT=(d["union"].values[L0] == "T"), gs=gs, grp=g, df=d)
    return out, q


def estratos(Q, modo):
    """Devuelve (pidx, seg): índices de cuerdas presentes ordenados por estrato y límites de segmento."""
    pres = np.where(Q["pres"])[0]
    lv = np.minimum(Q["lvl"], 3)
    if modo == 0:
        st = np.zeros(len(Q["v"]), dtype=np.int64)
    elif modo == 1:
        st = lv
    else:  # nivel x grupo (grupo de la cuerda raíz; las subsidiarias heredan el grupo)
        d = Q["df"]
        st = lv * 100000 + d["grupo"].values
    s = st[pres]
    o = np.argsort(s, kind="stable")
    pidx = pres[o].astype(np.int64)
    ss = s[o]
    seg = np.concatenate([[0], np.where(np.diff(ss) != 0)[0] + 1, [len(ss)]]).astype(np.int64)
    return pidx, seg


@njit(cache=True)
def stats_L0(a, isT, gs, out):
    m = len(a)
    G = len(gs) - 1
    S = np.zeros(m + 1, np.int64)
    N = np.zeros(m + 1, np.int64)
    for i in range(m):
        S[i + 1] = S[i] + a[i]
        N[i + 1] = N[i] + (1 if a[i] > 0 else 0)
    isgs = np.zeros(m + 1, np.bool_)
    for g in range(G + 1):
        isgs[gs[g]] = True
    F = 0; A = 0; TA = 0; nT = 0; pos = 0
    for i in range(m):
        if a[i] <= 0:
            continue
        pos += 1
        bF = 1000; bA = 1000
        # izquierda: tramo [j,i)
        tg = S[i] - a[i]
        if tg >= 0:
            j = np.searchsorted(S, tg)
            if j < i and S[j] == tg:
                nz = N[i] - N[j]
                if nz >= 2:
                    if nz < bF: bF = nz
                    jj = j
                    while jj < i and S[jj] == tg:
                        if isgs[jj]:
                            if nz < bA: bA = nz
                            break
                        jj += 1
        # derecha: tramo [i+1,k)
        tg = S[i + 1] + a[i]
        k = np.searchsorted(S, tg)
        if k < m + 1 and S[k] == tg and k > i + 1:
            nz = N[k] - N[i + 1]
            if nz >= 2:
                if nz < bF: bF = nz
                kk = k
                while kk <= m and S[kk] == tg:
                    if isgs[kk]:
                        if nz < bA: bA = nz
                        break
                    kk += 1
        if bF <= 10: F += 1
        if bA <= 40:
            A += 1
            if isT[i]: TA += 1
        if isT[i]: nT += 1
    # grupos
    tot = np.zeros(G, np.int64)
    nzg = np.zeros(G, np.int64)
    for g in range(G):
        tot[g] = S[gs[g + 1]] - S[gs[g]]
        nzg[g] = N[gs[g + 1]] - N[gs[g]]
    R4 = 0; R4e = 0; R5a = 0; R5ae = 0; R5b = 0; R5be = 0
    for g in range(G):
        n = gs[g + 1] - gs[g]
        # R4
        if n >= 2 and nzg[g] >= 2:
            fe = False; mt = False
            for k in range(2, 5):
                for lado in range(2):
                    if lado == 0:
                        g0 = g - k
                        if g0 < 0: continue
                    else:
                        g0 = g + 1
                        if g + k > G - 1: continue
                    ok = True
                    for t in range(g0, g0 + k):
                        if gs[t + 1] - gs[t] != n:
                            ok = False; break
                    if not ok: continue
                    fe = True
                    for t in range(n):
                        s = 0
                        for h in range(g0, g0 + k):
                            s += a[gs[h] + t]
                        if s != a[gs[g] + t]:
                            ok = False; break
                    if ok: mt = True
            if fe:
                R4e += 1
                if mt: R4 += 1
        # R5a
        if n >= 2 and nzg[g] >= 2:
            fe = False; mt = False
            for lado in range(2):
                if lado == 0:
                    g0 = g - n
                    if g0 < 0: continue
                else:
                    g0 = g + 1
                    if g + n > G - 1: continue
                fe = True
                ok = True; multi = False
                for t in range(n):
                    if tot[g0 + t] != a[gs[g] + t]:
                        ok = False; break
                    if nzg[g0 + t] >= 2: multi = True
                if ok and multi: mt = True
            if fe:
                R5ae += 1
                if mt: R5a += 1
        # R5b
        if tot[g] > 0 and G >= 3:
            fe = False; mt = False
            for k in range(2, 7):
                for lado in range(2):
                    if lado == 0:
                        g0 = g - k
                        if g0 < 0: continue
                    else:
                        g0 = g + 1
                        if g + k > G - 1: continue
                    fe = True
                    s = 0; nzs = 0
                    for h in range(g0, g0 + k):
                        s += tot[h]
                        if tot[h] > 0: nzs += 1
                    if s == tot[g] and nzs >= 2: mt = True
            if fe:
                R5be += 1
                if mt: R5b += 1
    out[2] = F; out[3] = A; out[4] = TA; out[5] = nT
    out[6] = R4; out[7] = R4e; out[8] = R5a; out[9] = R5ae; out[10] = R5b; out[11] = R5be; out[12] = pos


@njit(cache=True)
def stats_R1(v, par, out):
    n = len(v)
    cs = np.zeros(n, np.int64); cz = np.zeros(n, np.int64); cc = np.zeros(n, np.int64)
    for i in range(n):
        p = par[i]
        if p >= 0:
            cs[p] += v[i]
            if v[i] > 0: cz[p] += 1
            cc[p] += 1
    r = 0; e = 0
    for p in range(n):
        if cc[p] >= 2:
            e += 1
            if v[p] > 0 and cz[p] >= 2 and cs[p] == v[p]:
                r += 1
    out[0] = r; out[1] = e



@njit(cache=True)
def stats_any(v, L0, sub, out):
    """Fany: colgante = suma de CUALQUIER tramo contiguo de colgantes (2..10 sumandos no nulos), a cualquier distancia.
    Fsub: lo mismo para subsidiarias (valor = suma de un tramo de colgantes)."""
    a = v[L0]
    m = len(a)
    W = np.empty(m * 10 + 1, np.int64)
    nw = 0
    for j in range(m):
        if a[j] <= 0: continue
        s = 0; nz = 0
        for e in range(j, m):
            if a[e] <= 0: continue
            nz += 1
            if nz > 10: break
            s += a[e]
            if nz >= 2:
                W[nw] = s; nw += 1
    Ws = np.sort(W[:nw])
    fa = 0; fs = 0; fe = 0
    for i in range(m):
        if a[i] > 0 and nw > 0:
            k = np.searchsorted(Ws, a[i])
            if k < nw and Ws[k] == a[i]: fa += 1
    for i in range(len(v)):
        if sub[i] and v[i] > 0:
            fe += 1
            k = np.searchsorted(Ws, v[i])
            if k < nw and Ws[k] == v[i]: fs += 1
    out[13] = fa; out[14] = fs; out[15] = fe

@njit(cache=True)
def todo(v, par, L0, isT, gs, sub):
    out = np.zeros(16, np.int64)
    stats_R1(v, par, out)
    stats_L0(v[L0], isT, gs, out)
    stats_any(v, L0, sub, out)
    return out


@njit(cache=True)
def run_null(v0, par, L0, isT0, gs0, sub, pidx, seg, B, seed, modo):
    np.random.seed(seed)
    res = np.zeros((B, 16), np.int64)
    n = len(v0)
    vals0 = v0[pidx]
    obs_r1 = np.zeros(16, np.int64)
    if modo == 3:
        stats_R1(v0, par, obs_r1)
        stats_any(v0, L0, sub, obs_r1)
    a0 = v0[L0]
    G = len(gs0) - 1
    m = len(L0)
    for b in range(B):
        if modo < 3:
            vals = vals0.copy()
            for s in range(len(seg) - 1):
                x = vals[seg[s]:seg[s + 1]].copy()
                np.random.shuffle(x)
                vals[seg[s]:seg[s + 1]] = x
            v = v0.copy()
            for i in range(len(pidx)):
                v[pidx[i]] = vals[i]
            out = np.zeros(16, np.int64)
            stats_R1(v, par, out)
            stats_L0(v[L0], isT0, gs0, out)
            stats_any(v, L0, sub, out)
        else:
            pm = np.random.permutation(G)
            a = np.zeros(m, np.int64); tt = np.zeros(m, np.bool_)
            gs = np.zeros(G + 1, np.int64)
            p = 0
            for h in range(G):
                g = pm[h]
                for t in range(gs0[g], gs0[g + 1]):
                    a[p] = a0[t]; tt[p] = isT0[t]; p += 1
                gs[h + 1] = p
            out = np.zeros(16, np.int64)
            out[0] = obs_r1[0]; out[1] = obs_r1[1]
            stats_L0(a, tt, gs, out)
            stats_any(a, np.arange(m), np.zeros(m, np.bool_), out)
            out[14] = obs_r1[14]; out[15] = obs_r1[15]
        res[b] = out
    return res


# ---------- proporciones fijas ----------
FRAC = [(1, 10), (1, 5), (1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (1, 1), (4, 3), (3, 2), (2, 1), (3, 1), (4, 1), (5, 1), (10, 1)]
FP = np.array([f[0] for f in FRAC], np.int64)
FQ = np.array([f[1] for f in FRAC], np.int64)


@njit(cache=True)
def stats_ratio(v, par, L0, gs, fp, fq, out):
    """out[0:nf] = pares (colgante/subsidiaria, suma de hijos) con hijos*q == padre*p ; out[nf:2nf] = pares de grupos (tot_i*p == tot_j*q)."""
    nf = len(fp)
    n = len(v)
    cs = np.zeros(n, np.int64); cz = np.zeros(n, np.int64)
    for i in range(n):
        p = par[i]
        if p >= 0:
            cs[p] += v[i]
            if v[i] > 0: cz[p] += 1
    for f in range(nf):
        c = 0
        for p in range(n):
            if cz[p] >= 1 and v[p] > 0 and cs[p] * fq[f] == v[p] * fp[f]:
                c += 1
        out[f] = c
    G = len(gs) - 1
    tot = np.zeros(G, np.int64)
    for g in range(G):
        for t in range(gs[g], gs[g + 1]):
            tot[g] += v[L0[t]]
    for f in range(nf):
        c = 0
        for i in range(G):
            if tot[i] < 10: continue
            for j in range(G):
                if i != j and tot[j] >= 10 and tot[i] * fq[f] == tot[j] * fp[f]:
                    c += 1
        out[nf + f] = c


@njit(cache=True)
def run_null_ratio(v0, par, L0, gs, pidx, seg, B, seed, fp, fq):
    np.random.seed(seed)
    nf = len(fp)
    res = np.zeros((B, 2 * nf), np.int64)
    vals0 = v0[pidx]
    for b in range(B):
        vals = vals0.copy()
        for s in range(len(seg) - 1):
            x = vals[seg[s]:seg[s + 1]].copy()
            np.random.shuffle(x)
            vals[seg[s]:seg[s + 1]] = x
        v = v0.copy()
        for i in range(len(pidx)):
            v[pidx[i]] = vals[i]
        out = np.zeros(2 * nf, np.int64)
        stats_ratio(v, par, L0, gs, fp, fq, out)
        res[b] = out
    return res


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    r = p[o] * n / (np.arange(n) + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    q[o] = np.minimum(r, 1)
    return q


def autotest():
    """Comprobación mínima de los detectores con casos construidos a mano."""
    z = np.zeros(16, np.int64)
    a = np.array([1, 2, 3, 4, 4, 6], np.int64); o = z.copy(); stats_L0(a, np.zeros(6, np.bool_), np.array([0, 2, 4, 6]), o)
    assert o[6] == 1 and o[10] == 1, o          # R4 (grupo3 = g1+g2 cuerda a cuerda) y R5b (10 = 3+7)
    a = np.array([1, 2, 3, 4, 3, 7], np.int64); o = z.copy(); stats_L0(a, np.zeros(6, np.bool_), np.array([0, 2, 4, 6]), o)
    assert o[8] == 1, o                          # R5a (grupo de resumen [3,7])
    v = np.array([3, 4, 5, 12, 10, 4, 6], np.int64); par = np.array([-1, -1, -1, -1, -1, 4, 4])
    o = todo(v, par, np.array([0, 1, 2, 3, 4]), np.array([0, 0, 0, 1, 0], bool), np.array([0, 3, 5]), par >= 0)
    assert o[0] == 1 and o[4] == 1 and o[2] >= 1, o  # R1, TA (cuerda superior 12 = 3+4+5), F
    print("autotest ok")


if __name__ == "__main__":
    autotest()
