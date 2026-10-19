# -*- coding: utf-8 -*-
"""
02_analisis.py — Compara las listas coloniales de 01_listas.py con la firma
de 9 partes de UR278.

Controles:
  * rho de Spearman entre tamaño y posición, con nulo de permutación
    (enumeración exacta si n<=9; Monte Carlo 200.000 si n>9).
  * distancia de perfil (L2 sobre proporciones ordenadas) de las listas de
    9 unidades a cada una de las 24 filas de UR278; el nulo es la distribución
    de distancias entre las propias filas de UR278 (276 pares).
  * distancia en el orden documental (L1 a la media de UR278), comparada con
    la distribución de las 24 filas.
  * estructura de tríadas (3x3) frente a todas las particiones en 3 tríadas.
  * corrección de Holm (primarias y todas).

Salidas: resultados.csv, controles.csv.
"""
import os
import itertools
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
NPERM = 200_000


# ------------------------------------------------------------------ datos
def load_lists():
    d = pd.read_csv(os.path.join(BASE, "listas.csv"))
    out = {}
    for lid, g in d.groupby("list_id", sort=False):
        g = g.sort_values("orden")
        out[lid] = dict(
            x=g["cifra"].tolist(),
            nombres=g["nombre"].tolist(),
            region=g["region"].iloc[0],
            nivel=g["nivel"].iloc[0],
            fuente=g["fuente"].iloc[0],
            linea=g["linea"].iloc[0],
            completa=bool((g["completa"] == "si").all()),
            estructura=g["estructura"].iloc[0],
            nota=g["nota"].iloc[0],
        )
    return out


def signature():
    d = pd.read_csv(os.path.join(BASE, "..", "..", "13_sistema_incahuasi",
                                 "ur278_tabla.csv"))
    d = d[d["n"] == 9].copy()
    C = [f"c{i}" for i in range(1, 10)]
    X = d[C].values.astype(float)
    P = X / X.sum(1, keepdims=True)
    prof = P.mean(0)
    cv = P.std(1, ddof=1) / P.mean(1)
    rho = np.array([spearmanr(row, np.arange(1, 10)).statistic for row in P])
    eff = 1.0 / (P ** 2).sum(1)
    # distancias entre filas, perfiles ordenados
    S = np.sort(P, axis=1)[:, ::-1]
    rr = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            rr.append(np.linalg.norm(S[i] - S[j]))
    rr = np.array(rr)
    # L1 de cada fila (en su orden) a la media
    asg = np.abs(P - prof).sum(1)
    # pendiente log(proporcion) ~ posicion, en el orden fisico
    slopes = np.array([np.polyfit(np.arange(1, 10), np.log(row), 1)[0]
                       for row in P])
    slopes_sorted = np.array([np.polyfit(np.arange(1, 10), np.log(row), 1)[0]
                              for row in S])
    return dict(P=P, prof=prof, cv=cv, rho=rho, eff=eff, S=S, rr=rr, asg=asg,
                slopes=slopes, slopes_sorted=slopes_sorted, n_rows=len(d))


# ------------------------------------------------------------------ tests
def cv_eff(x):
    x = np.asarray(x, float)
    p = x / x.sum()
    return (x.std(ddof=1) / x.mean(), x.max() / x.min(), 1.0 / (p ** 2).sum(),
            (1.0 / (p ** 2).sum()) / len(x))


def rho_test(x, nperm=NPERM, seed=SEED):
    """rho de Spearman y p por permutación de posiciones (rápido, con empates)."""
    from scipy.stats import rankdata
    x = np.asarray(x, float)
    n = len(x)
    rho_obs = spearmanr(x, np.arange(1, n + 1)).statistic
    rv = rankdata(x)
    rv = rv - rv.mean()
    rng = np.random.default_rng(seed)
    perm = np.empty((nperm, n), dtype=np.int16)
    for k in range(nperm):
        perm[k] = rng.permutation(n) + 1
    perm = perm.astype(float) - (n + 1) / 2.0
    num = perm @ rv
    den = np.sqrt((rv ** 2).sum() * (perm ** 2).sum(axis=1))
    vals = num / den
    p_dec = (np.sum(vals <= rho_obs) + 1) / (nperm + 1)
    p_two = 2 * min(p_dec, (np.sum(vals >= rho_obs) + 1) / (nperm + 1))
    return rho_obs, min(p_two, 1.0), p_dec, vals.std()


def exact_rho_p(x):
    """p exacto a una cola (n<=9, con empates), enumerando n! posiciones."""
    from scipy.stats import rankdata
    x = np.asarray(x, float)
    n = len(x)
    if n > 9:
        return np.nan
    rv = rankdata(x)
    rv = rv - rv.mean()
    rho_obs = spearmanr(x, np.arange(1, n + 1)).statistic
    c = (n + 1) / 2.0
    sd_rv = np.sqrt((rv ** 2).sum())
    sd_p = np.sqrt(sum((k - c) ** 2 for k in range(1, n + 1)))
    cnt = 0
    tot = 0
    for perm in itertools.permutations(range(1, n + 1)):
        num = sum(rv[i] * (perm[i] - c) for i in range(n))
        rho = num / (sd_rv * sd_p)
        tot += 1
        if rho <= rho_obs + 1e-12:
            cnt += 1
    return cnt / tot


def exact_rho_p_nonies(x):
    return exact_rho_p(x)


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * p[idx]
        running = max(running, val)
        adj[idx] = min(running, 1.0)
    return adj


def shape_test(x, sig):
    """Solo para n=9: distancia de perfil ordenado a las 24 filas de UR278."""
    x = np.asarray(x, float)
    p = x / x.sum()
    ps = np.sort(p)[::-1]
    ds = np.linalg.norm(sig["S"] - ps, axis=1)
    # percentil de la distancia media frente a los 276 pares fila-fila
    pct = 100 * np.mean(sig["rr"] <= ds.mean())
    p_emp = (np.sum(sig["rr"] <= ds.mean()) + 1) / (len(sig["rr"]) + 1)
    # orden documental: L1 a la media
    l1 = np.abs(p - sig["prof"]).sum()
    pct_asg = 100 * np.mean(sig["asg"] <= l1)
    p_asg = (np.sum(sig["asg"] <= l1) + 1) / (len(sig["asg"]) + 1)
    l2_prof = np.linalg.norm(ps - np.sort(sig["prof"])[::-1])
    return dict(l2_mean=ds.mean(), l2_min=ds.min(), l2_max=ds.max(),
                pct=pct, p_emp=p_emp, l1=l1, pct_asg=pct_asg, p_asg=p_asg,
                l2_prof=l2_prof)


def null_cv_test(x, sig, nsim=20_000, seed=SEED):
    """Nulo: listas aleatorias de la misma n y CV; L2 al perfil medio."""
    x = np.asarray(x, float)
    p = x / x.sum()
    cv = x.std(ddof=1) / x.mean()
    if cv <= 0:
        return np.nan, np.nan, np.nan
    obs = np.linalg.norm(np.sort(p)[::-1] - np.sort(sig["prof"])[::-1])
    sigma = np.sqrt(np.log(1 + cv ** 2))
    rng = np.random.default_rng(seed)
    vals = np.empty(nsim)
    for k in range(nsim):
        z = rng.lognormal(0, sigma, len(x))
        z = z / z.sum()
        vals[k] = np.linalg.norm(np.sort(z)[::-1] - np.sort(sig["prof"])[::-1])
    pval = (np.sum(vals <= obs) + 1) / (nsim + 1)
    return obs, np.median(vals), pval


def triad_test(sig):
    """Media r dentro de las tres tríadas consecutivas vs 20.000 particiones."""
    P = sig["P"]
    L = np.log(P) - np.log(P).mean(1, keepdims=True)
    R = np.corrcoef(L.T)

    def stat(tri):
        s = []
        for t in tri:
            for i, j in itertools.combinations(t, 2):
                s.append(R[i, j])
        return np.mean(s)

    obs = stat([(0, 1, 2), (3, 4, 5), (6, 7, 8)])
    rng = np.random.default_rng(SEED)
    vals = []
    for _ in range(20_000):
        perm = rng.permutation(9)
        vals.append(stat([tuple(perm[0:3]), tuple(perm[3:6]), tuple(perm[6:9])]))
    vals = np.array(vals)
    p = (np.sum(vals >= obs) + 1) / (len(vals) + 1)
    return obs, vals.mean(), p


# ------------------------------------------------------------------ main
def main():
    L = load_lists()
    S = signature()
    print("Firma UR278: %d filas de 9; perfil CV=%.3f max/min=%.2f eff=%.2f; "
          "rho(perfil,pos)=%.2f (p=%.4f)" % (
              S["n_rows"], S["prof"].std(ddof=1) / S["prof"].mean(),
              S["prof"].max() / S["prof"].min(), 1 / (S["prof"] ** 2).sum(),
              spearmanr(S["prof"], np.arange(1, 10)).statistic,
              spearmanr(S["prof"], np.arange(1, 10)).pvalue))
    print("CV dentro de fila: med=%.3f IQR=%.3f-%.3f max=%.3f; "
          "rho por fila: med=%.2f, %.0f%% <= -0.5, %.0f%% <= -0.7" % (
              np.median(S["cv"]), np.percentile(S["cv"], 25),
              np.percentile(S["cv"], 75), S["cv"].max(),
              np.median(S["rho"]), 100 * np.mean(S["rho"] <= -.5),
              100 * np.mean(S["rho"] <= -.7)))

    # listas primarias: independientes, completas, n=7..11
    primarias = ["caj_bambamarca_1567", "cusco_coco_1535", "aullaga_acho_1540"]
    secundarias = ["lupaca_sayas_1567", "lupaca_cabeceras_1567",
                   "chayanta_1540", "chayanta_1548", "yanque_collagua_1540",
                   "cavana_conde_1540"]

    res = []
    ctr = []
    for lid, d in L.items():
        x = [v for v in d["x"] if v != "" and not pd.isna(v)]
        if not d["completa"] or len(x) < 3:
            continue
        x = np.asarray(x, float)
        n = len(x)
        cv, mm, eff, even = cv_eff(x)
        if np.allclose(x, x[0]):
            rho, p2, pdec = np.nan, np.nan, np.nan
        else:
            rho, p2, pdec, sd = rho_test(x)
        pct_cv = 100 * np.mean(S["cv"] <= cv)
        p = x / x.sum()
        slope = np.polyfit(np.arange(1, n + 1), np.log(p), 1)[0]
        ps = np.sort(p)[::-1]
        slope_sorted = np.polyfit(np.arange(1, n + 1), np.log(ps), 1)[0]
        row = dict(list_id=lid, region=d["region"], nivel=d["nivel"], n=n,
                   total=x.sum(), media=x.mean(), cv=cv, max_min=mm,
                   eff_n=eff, evenness=even, rho=rho, p_rho_dec=pdec,
                   p_rho_two=p2, pct_cv_ur278=pct_cv,
                   slope_logrank=slope, slope_sorted=slope_sorted,
                   estructura=d["estructura"][:80])
        if n == 9:
            sh = shape_test(x, S)
            obs_cv, med_cv, p_cv = null_cv_test(x, S)
            row.update(l2_mean=sh["l2_mean"], l2_min=sh["l2_min"],
                       l2_max=sh["l2_max"], pct_l2=sh["pct"],
                       p_l2=sh["p_emp"], l1_asg=sh["l1"],
                       pct_l1_asg=sh["pct_asg"], p_l1_asg=sh["p_asg"],
                       l2_profile=sh["l2_prof"], null_cv_median=med_cv,
                       p_null_cv=p_cv,
                       pct_slope=100 * np.mean(S["slopes"] <= slope),
                       pct_slope_sorted=100 * np.mean(
                           S["slopes_sorted"] <= slope_sorted))
        res.append(row)
        if not np.isnan(pdec):
            ctr.append(dict(test="rho_dec", list_id=lid, stat=rho,
                            null="permutacion", p=pdec, nperm=NPERM,
                            nota="una cola: lista ordenada de mayor a menor"))

    R = pd.DataFrame(res)
    # correcciones
    prim = R[R.list_id.isin(primarias)].copy()
    R["holm_primarias"] = np.nan
    R.loc[prim.index, "holm_primarias"] = holm(prim["p_rho_dec"].values)
    R["holm_todas"] = np.nan
    valid = R["p_rho_dec"].notna()
    R.loc[valid, "holm_todas"] = holm(R.loc[valid, "p_rho_dec"].values)
    # sensibilidad: solo listas completas con n>=7 (9 listas)
    R["holm_n7"] = np.nan
    m7 = (R["n"] >= 7) & R["p_rho_dec"].notna()
    R.loc[m7, "holm_n7"] = holm(R.loc[m7, "p_rho_dec"].values)

    # tests de forma
    for lid in ["caj_bambamarca_1567", "cusco_coco_1535"]:
        r = R[R.list_id == lid].iloc[0]
        ctr.append(dict(test="perfil_ordenado", list_id=lid,
                        stat=r["l2_mean"], null="276 pares de filas UR278",
                        p=r["p_l2"], nperm=len(S["rr"]),
                        nota="L2 medio a las 24 filas; menor = mas parecido"))
        ctr.append(dict(test="orden_documental", list_id=lid,
                        stat=r["l1_asg"], null="24 filas UR278 a la media",
                        p=r["p_l1_asg"], nperm=len(S["asg"]),
                        nota="L1 a la media; menor = mas parecido"))
        ctr.append(dict(test="nulo_cv", list_id=lid,
                        stat=r["l2_profile"],
                        null="lognormal misma n y CV (20.000)",
                        p=r["p_null_cv"], nperm=20_000,
                        nota="L2 al perfil medio; p bajo = mas cerca que el azar con su CV"))

    # triadas
    obs, nullmean, p = triad_test(S)
    ctr.append(dict(test="triadas_3x3", list_id="UR278", stat=obs,
                    null="20.000 particiones en 3 triadas", p=p, nperm=20_000,
                    nota="media r dentro de (1-2-3)(4-5-6)(7-8-9)"))

    # estabilidad de la transcripcion de Chayanta
    a = np.array([40, 8, 15, 22, 10, 60, 60, 20, 49, 26, 16, 20], float)
    b = np.array([42, 8, 15, 46, 10, 60, 62, 20, 49, 27, 17, 20], float)
    rho_t = spearmanr(a, b).statistic
    ctr.append(dict(test="orden_estable_chayanta", list_id="chayanta",
                    stat=rho_t, null="—", p=np.nan, nperm=0,
                    nota="misma secuencia de 12 pueblos en 1540 y 1548; valores rho"))

    # exacto para Bambamarca (con empates)
    pex = exact_rho_p(list(L["caj_bambamarca_1567"]["x"]))
    ctr.append(dict(test="rho_exacto", list_id="caj_bambamarca_1567",
                    stat=spearmanr(L["caj_bambamarca_1567"]["x"],
                                   np.arange(1, 10)).statistic,
                    null="9! = 362.880 permutaciones", p=pex, nperm=362880,
                    nota="p exacto a una cola (con empates)"))
    # Bambamarca sin la primera pachaca (la del cacique principal)
    x8 = np.array(L["caj_bambamarca_1567"]["x"][1:], float)
    pex8 = exact_rho_p(x8)
    ctr.append(dict(test="rho_sin_primero", list_id="caj_bambamarca_1567",
                    stat=spearmanr(x8, np.arange(1, 9)).statistic,
                    null="8! = 40.320 permutaciones", p=pex8, nperm=40320,
                    nota="descenso de las 8 pachacas subordinadas"))

    C = pd.DataFrame(ctr)
    R.to_csv(os.path.join(BASE, "resultados.csv"), index=False)
    C.to_csv(os.path.join(BASE, "controles.csv"), index=False)

    # ------------------------------------------------------------ salida
    cols = ["list_id", "n", "cv", "max_min", "evenness", "rho", "p_rho_dec",
            "holm_primarias", "pct_cv_ur278", "pct_l2", "pct_l1_asg"]
    print("\nListas completas (n>=5):")
    print(R[cols].sort_values(["n", "list_id"]).to_string(index=False,
          float_format=lambda z: f"{z:.3f}"))
    print("\nControles:")
    print(C[["test", "list_id", "stat", "p", "nperm"]].to_string(index=False,
          float_format=lambda z: f"{z:.4f}"))
    print("\nBambamarca p exacto (una cola) = %.5f" % pex)
    print("Chayanta rho entre transcripciones = %.3f" % rho_t)


if __name__ == "__main__":
    main()
