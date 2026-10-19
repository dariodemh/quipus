"""02: pruebas de Incahuasi (reglas a-d) en Pachacamac y Puruchuco.

Registro = grupo de colgantes (incluye grupos vacios entre el minimo y el maximo:
regla b). Tres definiciones de valor de registro, todas con TODAS las cuerdas
(regla a):
  X  cabecera (primer colgante anudado)          <- linea base de n_detectores
  P  suma de colgantes nivel 0 del grupo
  PS P + suma de la primera subsidiaria (regla c)
Regla (d): en OKR las marcadoras M separan bloques (solo UR073 en Puruchuco);
en KFG los grupos PK sin nudos ya son separadores.

T1 copias       : P_A(i) == P_B(i) por posicion          (nulo: barajar B)
T2 A+B -> C     : P_A(i)+P_B(i) en los valores de registro de un tercer quipu
                  (nulo: barajar el orden de B; E exacta invariante a la permutacion)
T3 filas->filas : LCS ordenada de P_A y P_B              (nulo: barajar B)
T4 cuotas       : x_i - v = c, con v otra cuerda del grupo (nulo: barajar cuerdas)
Correccion T2: se repite TODA la busqueda con B barajado (jardin de senderos).
T1/T3/T4: BH sobre toda la familia.
"""
import itertools
import json
import sys
import numpy as np
import pandas as pd
from scipy.stats import poisson
from numba import njit
import comun_np as L

rng = np.random.default_rng(L.SEED + 2)
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 100
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


@njit(cache=True)
def _tol(d):
    d = abs(d)
    return d == 0 or d == 1 or d == 10 or d == 100 or d == 1000


@njit(cache=True)
def lcs_nb(x, y):
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            if _tol(x[i] - y[j]):
                H[i + 1, j + 1] = H[i, j] + 1
            else:
                H[i + 1, j + 1] = max(H[i, j + 1], H[i + 1, j])
    return H[n, m]


def datos_archivo(c, ks):
    D = {}
    for k in ks:
        regs = L.registros_kfg(c, k)
        if not regs:
            continue
        X = np.array([r["x"] for r in regs], dtype=np.int64)
        P = np.array([r["p"] for r in regs], dtype=np.int64)
        S = np.array([r["s"] for r in regs], dtype=np.int64)
        D[k] = dict(X=X, P=P, PS=P + S, S=S, regs=regs)
    return D


# ---------------------------------------------------------------- T1
def test_copias(D, ks):
    filas = []
    for a, b in itertools.combinations(ks, 2):
        va, vb = D[a]["P"], D[b]["P"]
        n = min(len(va), len(vb))
        if n < 5:
            continue
        x, y = va[:n], vb[:n]
        M = x[:, None] == y[None, :]
        h = int(np.trace(M))
        nl = np.array([M[np.arange(n), rng.permutation(n)].sum() for _ in range(1000)])
        filas.append(dict(A=a, B=b, n=n, hit=h, nulo=nl.mean(), p=L.p_emp(h, nl),
                          exceso=h - nl.mean()))
    d = pd.DataFrame(filas)
    if len(d):
        d["q"] = L.bh(d.p)
    return d.sort_values("p")


# ---------------------------------------------------------------- T2
def construir_T2(D, ks, campo):
    """Matrices de coincidencia M[i,j] = 1[x_i+y_j esta en algun tercer quipu]."""
    dueños = {}
    for k in ks:
        for v in set(int(t) for t in D[k][campo] if t > 0):
            dueños.setdefault(v, set()).add(k)
    conf = []
    for a, b in itertools.combinations(ks, 2):
        va, vb = D[a][campo], D[b][campo]
        n = min(len(va), len(vb))
        if n < 3:
            continue
        x, y = va[:n], vb[:n]
        sa = set(int(t) for t in D[a][campo] if t > 0)
        sb = set(int(t) for t in D[b][campo] if t > 0)
        M = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(n):
                v = int(x[i] + y[j])
                M[i, j] = len(dueños.get(v, ())) > ((v in sa) + (v in sb))
        E = M.sum() / n
        h = int(np.trace(M))
        p = poisson.sf(h - 1, E) if E > 0 else (0.0 if h > 0 else 1.0)
        conf.append(dict(A=a, B=b, n=n, M=M, E=E, hit=h, p=p))
    return conf


def nulo_T2(conf, nrep):
    """Distribucion nula del minimo p sobre toda la familia."""
    out = []
    for _ in range(nrep):
        best = 1.0
        for cf in conf:
            n, M = cf["n"], cf["M"]
            h = int(M[np.arange(n), rng.permutation(n)].sum())
            p = poisson.sf(h - 1, cf["E"]) if cf["E"] > 0 else (0.0 if h > 0 else 1.0)
            if p < best:
                best = p
        out.append(best)
    return np.array(out)


# ---------------------------------------------------------------- T3
def test_lcs(D, ks, campo, nrep=200):
    filas = []
    for a, b in itertools.permutations(ks, 2):
        va, vb = D[a][campo], D[b][campo]
        n = min(len(va), len(vb))
        if n < 4:
            continue
        x, y = va[:n], vb[:n]
        h = lcs_nb(x, y)
        nl = np.array([lcs_nb(x, rng.permutation(y)) for _ in range(nrep)])
        filas.append(dict(A=a, B=b, n=n, lcs=h, nulo=nl.mean(),
                          p=L.p_emp(h, nl), exceso=h - nl.mean()))
    d = pd.DataFrame(filas)
    if len(d):
        d["q"] = L.bh(d.p)
    return d.sort_values("p")


# ---------------------------------------------------------------- T4
def test_cuotas(D, ks, nrep=2000):
    filas = []
    cands = list(range(2, 61)) + [208]
    for k in ks:
        regs = [r for r in D[k]["regs"] if not r["vacio"]]
        if len(regs) < 4:
            continue
        xs = np.array([r["x"] for r in regs])
        pools = [[v for v in r["vals"] if v != r["x"] and v > 0] for r in regs]

        def apoyo(pp):
            cnt = {c: 0 for c in cands}
            for x, po in zip(xs, pp):
                for v in set(po):
                    c = int(x - v)
                    if c in cnt:
                        cnt[c] += 1
            c = max(cnt, key=cnt.get)
            return cnt[c], c

        obs, cobs = apoyo(pools)
        pool = [v for po in pools for v in po]
        nl = []
        for _ in range(nrep):
            rng.shuffle(pool)
            i = 0
            pp = []
            for po in pools:
                pp.append(pool[i:i + len(po)])
                i += len(po)
            nl.append(apoyo(pp)[0])
        nl = np.array(nl)
        filas.append(dict(kfg=k, n=len(regs), apoyo=obs, cuota=cobs,
                          nulo=nl.mean(), max_nulo=nl.max(), p=L.p_emp(obs, nl)))
    d = pd.DataFrame(filas)
    if len(d):
        d["q"] = L.bh(d.p)
    return d.sort_values("p")


def analizar(proc):
    c, q = L.cargar_kfg()
    if proc == "Puruchuco":
        ks = sorted(q[q.region == "Puruchuco"].kfg)
    else:
        ks = sorted(q[q.procedencia == proc].kfg)
    D = datos_archivo(c, ks)
    ks = [k for k in ks if k in D]
    pr(f"\n===== {proc}: {len(ks)} quipus, "
       f"{sum(1 for k in ks if len(D[k]['P'])>=3)} con >=3 registros =====")
    r = dict(proc=proc, ks=ks, pmin={}, pcorr={})
    for campo in ["X", "P", "PS"]:
        conf = construir_T2(D, ks, campo)
        d = pd.DataFrame([{k: v for k, v in cf.items() if k != "M"} for cf in conf])
        d["q_fdr"] = L.bh(d.p) if len(d) else []
        d.to_csv(L.AQUI / f"suma_{proc}_{campo}.csv", index=False)
        pmin, fdr = float(d.p.min()), float(d.q_fdr.min())
        nl = nulo_T2(conf, NREP) if NREP else np.array([np.nan])
        pcorr = L.p_emp(pmin, nl, mayor_es_mejor=False) if NREP else np.nan
        r["pmin"][campo] = pmin
        r["pcorr"][campo] = float(pcorr)
        r["nulo_" + campo] = nl.tolist()
        pr(f"T2 {campo}: {len(d)} pares; min p={pmin:.2e}; BH min q={fdr:.2e}; "
           f"p corregido (jardin, {NREP} rep)={pcorr:.4f}")
        pr("   top: " + ", ".join(f"{t.A}+{t.B}(h={t.hit},E={t.E:.1f},p={t.p:.2e})"
                                  for t in d.nsmallest(4, "p").itertuples()))
    cop = test_copias(D, ks)
    cop.to_csv(L.AQUI / f"copias_{proc}.csv", index=False)
    if len(cop):
        r["cop_min_q"] = float(cop.q.min())
        pr(f"T1 copias: {len(cop)} pares; min q={cop.q.min():.3f}; top: " +
           ", ".join(f"{t.A}+{t.B}(h={t.hit},nulo={t.nulo:.1f},p={t.p:.4f},q={t.q:.3f})"
                     for t in cop.head(3).itertuples()))
    lc = test_lcs(D, ks, "P", nrep=200)
    lc.to_csv(L.AQUI / f"lcs_{proc}.csv", index=False)
    if len(lc):
        r["lcs_min_q"] = float(lc.q.min())
        pr(f"T3 LCS: {len(lc)} pares ordenados; min q={lc.q.min():.3f}; top: " +
           ", ".join(f"{t.A}->{t.B}(LCS={t.lcs},nulo={t.nulo:.1f},p={t.p:.4f},q={t.q:.2f})"
                     for t in lc.head(3).itertuples()))
    cu = test_cuotas(D, ks)
    cu.to_csv(L.AQUI / f"cuotas_{proc}.csv", index=False)
    if len(cu):
        r["cuotas_q005"] = cu[cu.q < .05].kfg.tolist()
        pr(f"T4 cuotas: {len(cu)} quipus; q<0.05: " +
           ", ".join(f"{t.kfg}(c={t.cuota},ap={t.apoyo},q={t.q:.3f})"
                     for t in cu[cu.q < .05].itertuples()))
    return r


if __name__ == "__main__":
    res = {}
    for proc in ["Incahuasi", "Pachacamac", "Puruchuco"]:
        res[proc] = analizar(proc)
    json.dump(res, open(L.AQUI / "general.json", "w"), indent=1)
    with open(L.AQUI / "salida_02_general.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(OUT) + "\n")
