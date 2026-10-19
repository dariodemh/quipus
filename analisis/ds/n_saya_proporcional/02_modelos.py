# -*- coding: utf-8 -*-
"""
02_modelos.py -- Prueba A: proporcionalidad de las 9 columnas de UR278.

Modelos
  M1  proporcion fija + ruido multinomial           (8 parametros)
  M2  proporcion fija + perturbacion por registro   (Dirichlet-multinomial, 9)
  M3  proporciones independientes por registro      (multinomial saturado, 192)
Comparacion por log-verosimilitud, AIC y BIC; bondad de ajuste por simulacion
parametrica. Ajuste beta-binomial por columna para ver que columnas son mas
estables. Tendencias con el orden de los registros y elasticidad al total.

Salidas: modelos_ur278.csv, gof_ur278.csv, columnas_ur278.csv,
         tendencias_ur278.csv, ajuste_ur270.csv, salida_02.txt
"""
import json
import numpy as np
import pandas as pd
from scipy import stats, special
from scipy.optimize import minimize, minimize_scalar

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)
OUT = "analisis/ds/n_saya_proporcional"
COLS = [f"c{i}" for i in range(1, 10)]
PCOLS = [f"p{i}" for i in range(1, 10)]

d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[COLS].to_numpy(float)
N = d["N"].to_numpy(float)
P = X / N[:, None]
n, k = X.shape
logN = np.log(N)
orden = np.arange(1, n + 1)


# ------------------------------------------------------------------ utilidades
def multinom_ll(x, N, p):
    """log-verosimilitud multinomial (p puede ser (k,) o (n,k))."""
    p = np.asarray(p, float)
    if p.ndim == 1:
        p = np.broadcast_to(p, x.shape)
    c = special.gammaln(N + 1) - special.gammaln(x + 1).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(x > 0, x * np.log(p), 0.0)
    return float((c + t.sum(axis=1)).sum())


def dm_ll(x, N, p, alpha):
    """Dirichlet-multinomial: p_i ~ Dirichlet(alpha*p), x_i|p_i ~ Mult(N_i,p_i)."""
    a = alpha * np.asarray(p, float)
    c = special.gammaln(N + 1) - special.gammaln(x + 1).sum(axis=1)
    t = (special.gammaln(np.asarray(alpha, float)) - special.gammaln(N + alpha)
         + (special.gammaln(x + a) - special.gammaln(a)).sum(axis=1))
    return float((c + t).sum())


def softmax(theta):
    z = np.concatenate([theta, [0.0]])
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def fit_dm(x, N, starts=(10.0, 100.0, 1000.0)):
    """Ajusta p (k-1) y alpha por maxima verosimilitud."""
    p0 = x.sum(0) / N.sum()
    th0 = np.log(p0[:-1] / p0[-1])

    def nll(par):
        p = softmax(par[:k - 1])
        alpha = np.exp(par[k - 1])
        if alpha > 1e9:
            return 1e12
        return -dm_ll(x, N, p, alpha)

    best = None
    for a0 in starts:
        par0 = np.concatenate([th0, [np.log(a0)]])
        r = minimize(nll, par0, method="L-BFGS-B",
                     options={"maxiter": 4000, "ftol": 1e-12})
        if best is None or r.fun < best.fun:
            best = r
    p = softmax(best.x[:k - 1])
    alpha = float(np.exp(best.x[k - 1]))
    return p, alpha, -best.fun


def fit_alpha_profile(x, N, p, lo=1e-3, hi=1e7):
    """Maximiza alpha con p fijo (para el test de sobredispersion)."""
    f = lambda la: -dm_ll(x, N, p, np.exp(la))
    r = minimize_scalar(f, bounds=(np.log(lo), np.log(hi)), method="bounded",
                        options={"xatol": 1e-6})
    return float(np.exp(r.x)), -r.fun


# ------------------------------------------------------------------ M1, M2, M3
p1 = X.sum(0) / N.sum()
LL1 = multinom_ll(X, N, p1)
p2, alpha2, LL2 = fit_dm(X, N)
LL3 = multinom_ll(X, N, X / N[:, None])

k1, k2, k3 = k - 1, k, n * (k - 1)
AIC = lambda ll, kk: -2 * ll + 2 * kk
BIC = lambda ll, kk, m: -2 * ll + kk * np.log(m)
modelos = pd.DataFrame([
    {"modelo": "M1 multinomial (proporcion fija)", "k": k1, "LL": LL1,
     "AIC_n24": AIC(LL1, k1), "BIC_n24": BIC(LL1, k1, n),
     "BIC_n54601": BIC(LL1, k1, N.sum())},
    {"modelo": "M2 Dirichlet-multinomial (proporcion fija + perturbacion)", "k": k2,
     "LL": LL2, "AIC_n24": AIC(LL2, k2), "BIC_n24": BIC(LL2, k2, n),
     "BIC_n54601": BIC(LL2, k2, N.sum())},
    {"modelo": "M3 proporciones libres por registro (saturado)", "k": k3, "LL": LL3,
     "AIC_n24": AIC(LL3, k3), "BIC_n24": BIC(LL3, k3, n),
     "BIC_n54601": BIC(LL3, k3, N.sum())},
])
modelos["Delta_AIC"] = modelos.AIC_n24 - modelos.AIC_n24.min()
modelos["Delta_BIC"] = modelos.BIC_n24 - modelos.BIC_n24.min()

# LRT de sobredispersion: M1 (alpha=inf) vs M2, perfil con p fijo en p1
alpha_prof, LL2_prof = fit_alpha_profile(X, N, p1)
LRT = 2 * (LL2_prof - LL1)
p_LRT_mixtura = 0.5 * stats.chi2.sf(LRT, 1)  # limite en la frontera
B_LRT = 1000
lrt_sim = np.empty(B_LRT)
for b in range(B_LRT):
    xs = rng.multinomial(N.astype(int), p1)
    _, llp = fit_alpha_profile(xs, N, p1)
    lrt_sim[b] = 2 * (llp - multinom_ll(xs, N, p1))
p_LRT_boot = (1 + np.sum(lrt_sim >= LRT)) / (B_LRT + 1)

# factor de sobredispersion implicado por M2 en el N medio
Nbar = N.mean()
overdisp_M2 = (Nbar + alpha2) / (1 + alpha2)
var_ratio = overdisp_M2

# ------------------------------------------------------------------ estadisticos
def kendall_w(P):
    m, kk = P.shape
    R = np.array([stats.rankdata(row) for row in P])
    Rj = R.sum(0)
    S = ((Rj - Rj.mean()) ** 2).sum()
    return 12 * S / (m ** 2 * (kk ** 3 - kk))


def clr(P):
    L = np.log(P)
    return L - L.mean(1, keepdims=True)


def pc1_share(P):
    Z = clr(P)
    Z = Z - Z.mean(0)
    s = np.linalg.svd(Z, compute_uv=False)
    return float(s[0] ** 2 / (s ** 2).sum())


def het_stat(P, N):
    """SD entre columnas de log(var observada / var multinomial esperada)."""
    V = P.var(0, ddof=1)
    E = P.mean(0) * (1 - P.mean(0)) * np.mean(1 / N)
    return float(np.std(np.log(V / E), ddof=1))


def trend_stat(P, orden):
    """Media de rho^2 parcial (controlando log N) entre cada columna y el orden."""
    lo = np.log(orden)
    lN = np.log(N)
    vals = []
    for j in range(P.shape[1]):
        rx, ry, rz = (stats.rankdata(P[:, j]), stats.rankdata(orden),
                      stats.rankdata(lN))
        ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
        ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
        vals.append(stats.pearsonr(ex, ey)[0] ** 2)
    return float(np.mean(vals))


def size_stat(P, N):
    lN = np.log(N)
    return float(max(abs(stats.spearmanr(P[:, j], lN)[0]) for j in range(P.shape[1])))


def serial_stat(P):
    Z = clr(P)
    adj = np.mean(np.linalg.norm(np.diff(Z, axis=0), axis=1))
    idx = rng.integers(0, len(Z), size=(4000, 2))
    idx = idx[idx[:, 0] != idx[:, 1]]
    alea = np.mean(np.linalg.norm(Z[idx[:, 0]] - Z[idx[:, 1]], axis=1))
    return float(adj / alea)


def stats_all(P, N, orden):
    return {"R_CV": float(np.mean(P.std(0, ddof=1) / P.mean(0)) /
                          np.mean(np.sqrt(P.mean(0) * (1 - P.mean(0)) / N.mean()) / P.mean(0))),
            "W": kendall_w(P), "PC1": pc1_share(P), "H": het_stat(P, N),
            "T": trend_stat(P, orden), "S": size_stat(P, N),
            "L": serial_stat(P), "CVcol": float(P.mean(0).std(ddof=1) / P.mean(0).mean())}


obs = stats_all(P, N, orden)

# ------------------------------------------------------------------ GOF M1 y M2
def sim_stats(modelo, B):
    filas = []
    for b in range(B):
        if modelo == "M1":
            xs = rng.multinomial(N.astype(int), p1)
        else:
            pi = rng.dirichlet(alpha2 * p2, size=n)
            xs = np.array([rng.multinomial(int(N[i]), pi[i]) for i in range(n)])
        Ps = xs / N[:, None]
        filas.append(stats_all(Ps, N, orden))
    return pd.DataFrame(filas)


B1, B2 = 4000, 2000
s1 = sim_stats("M1", B1)
s2 = sim_stats("M2", B2)

gof = []
for nombre, val in obs.items():
    for etiqueta, sim in (("M1", s1), ("M2", s2)):
        v = sim[nombre].to_numpy()
        p_inf = (1 + np.sum(v <= val)) / (len(v) + 1)
        p_sup = (1 + np.sum(v >= val)) / (len(v) + 1)
        gof.append({"modelo": etiqueta, "estadistico": nombre,
                    "observado": val, "sim_media": float(v.mean()),
                    "sim_p05": float(np.quantile(v, 0.05)),
                    "sim_p95": float(np.quantile(v, 0.95)),
                    "p_inf": p_inf, "p_sup": p_sup,
                    "p": min(1.0, 2 * min(p_inf, p_sup))})
gof = pd.DataFrame(gof)

# BH dentro de cada modelo
def bh(p):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    q = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        i = o[rank]
        val = min(prev, p[i] * m / (rank + 1))
        q[i] = val
        prev = val
    return q
gof["q_BH"] = np.nan
for et in ("M1", "M2"):
    m = gof.modelo == et
    gof.loc[m, "q_BH"] = bh(gof.loc[m, "p"].values)

# ------------------------------------------------------------------ por columna
def fit_bb(x, N, p0=None, rho0=0.005):
    """Beta-binomial marginal: x_i ~ BB(N_i, p, rho)."""
    if p0 is None:
        p0 = x.sum() / N.sum()

    def nll(par):
        p = 1 / (1 + np.exp(-par[0]))
        rho = 1 / (1 + np.exp(-par[1]))
        a = p * (1 / rho - 1)
        b = (1 - p) * (1 / rho - 1)
        ll = (special.gammaln(N + 1) - special.gammaln(x + 1)
              - special.gammaln(N - x + 1)
              + special.betaln(x + a, N - x + b) - special.betaln(a, b))
        return -ll.sum()

    r = minimize(nll, [np.log(p0 / (1 - p0)), np.log(rho0 / (1 - rho0))],
                 method="L-BFGS-B")
    p = 1 / (1 + np.exp(-r.x[0]))
    rho = 1 / (1 + np.exp(-r.x[1]))
    ll1 = -r.fun
    ll0 = multinom_ll(x[:, None], N, np.array([p0])) if False else None
    # binomial con p MLE
    ll0 = float(np.sum(special.gammaln(N + 1) - special.gammaln(x + 1)
                       - special.gammaln(N - x + 1)
                       + x * np.log(p0) + (N - x) * np.log(1 - p0)))
    # SE por Hessiano numerico sobre (logit p, logit rho)
    eps = 1e-4
    H = np.zeros((2, 2))
    f0 = r.fun
    for i in range(2):
        for j in range(2):
            ei = np.zeros(2); ej = np.zeros(2)
            ei[i] = eps; ej[j] = eps
            H[i, j] = (nll(r.x + ei + ej) - nll(r.x + ei - ej)
                       - nll(r.x - ei + ej) + nll(r.x - ei - ej)) / (4 * eps * eps)
    try:
        V = np.linalg.inv(H)
        se_logit = np.sqrt(np.maximum(np.diag(V), 0))
    except np.linalg.LinAlgError:
        se_logit = np.array([np.nan, np.nan])
    se_rho = rho * (1 - rho) * se_logit[1]
    stat = 2 * (ll1 - ll0)
    pval = 0.5 * stats.chi2.sf(max(stat, 0), 1)
    return dict(p=p, rho=rho, se_rho=se_rho, ll=ll1, ll0=ll0, LRT=stat, p_LRT=pval)

col = []
for j, c in enumerate(COLS):
    r = fit_bb(X[:, j], N)
    col.append({"columna": c, "media_p": P[:, j].mean(),
                "CV_obs": P[:, j].std(ddof=1) / P[:, j].mean(),
                "CV_mult": np.sqrt(P[:, j].mean() * (1 - P[:, j].mean()) / N.mean()) / P[:, j].mean(),
                "CV_ratio": (P[:, j].std(ddof=1) / P[:, j].mean()) /
                            (np.sqrt(P[:, j].mean() * (1 - P[:, j].mean()) / N.mean()) / P[:, j].mean()),
                "p_bb": r["p"], "rho_bb": r["rho"], "se_rho": r["se_rho"],
                "LRT_bb": r["LRT"], "p_LRT": r["p_LRT"],
                "min": X[:, j].min(), "max": X[:, j].max()})
col = pd.DataFrame(col)
col["q_LRT_BH"] = bh(col["p_LRT"].values)

# ------------------------------------------------------------------ tendencias
def partial_spearman(x, y, z):
    rx, ry, rz = stats.rankdata(x), stats.rankdata(y), stats.rankdata(z)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
    ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    r, p = stats.pearsonr(ex, ey)
    return r, p

tend = []
for j, c in enumerate(COLS):
    r0, p0 = stats.spearmanr(P[:, j], orden)
    r1, p1v = partial_spearman(P[:, j], orden, logN)
    b, a, rr, pp, se = stats.linregress(logN, np.log(X[:, j]))
    tend.append({"columna": c, "rho_orden": r0, "p_orden": p0,
                 "rho_orden_dado_logN": r1, "p_orden_dado_logN": p1v,
                 "elasticidad_N": b, "se_elasticidad": se,
                 "p_elasticidad_1": 2 * (1 - stats.t.cdf(abs((b - 1) / se), n - 2))})
tend = pd.DataFrame(tend)
tend["q_orden_BH"] = bh(tend["p_orden_dado_logN"].values)
tend["q_elast_BH"] = bh(tend["p_elasticidad_1"].values)

# nulo de tendencia multivariada: permutar el orden
B_T = 5000
t_obs = trend_stat(P, orden)
t_sim = np.empty(B_T)
for b in range(B_T):
    t_sim[b] = trend_stat(P, rng.permutation(orden))
p_trend = (1 + np.sum(t_sim >= t_obs)) / (B_T + 1)

# changepoint: maxima separacion entre mitades (estadistico F multivariado sobre CLR)
Z = clr(P)
Zc = Z - Z.mean(0)


def changepoint_stat(Zc):
    m = len(Zc)
    tot = (Zc ** 2).sum()
    best = -1
    for cut in range(4, m - 3):
        a = Zc[:cut].mean(0)
        b = Zc[cut:].mean(0)
        between = cut * (a ** 2).sum() + (m - cut) * (b ** 2).sum()
        best = max(best, between / tot)
    return best

cp_obs = changepoint_stat(Zc)
cp_sim = np.empty(B_T)
for b in range(B_T):
    cp_sim[b] = changepoint_stat(Zc[rng.permutation(n)])
p_cp = (1 + np.sum(cp_sim >= cp_obs)) / (B_T + 1)

# ------------------------------------------------------------------ replicacion UR270
rep270 = None
try:
    u = pd.read_csv(f"{OUT}/datos_ur270.csv")
    X270 = u[COLS].to_numpy(float)
    N270 = u["N"].to_numpy(float)
    P270 = X270 / N270[:, None]
    p1u = X270.sum(0) / N270.sum()
    LL1u = multinom_ll(X270, N270, p1u)
    p2u, a2u, LL2u = fit_dm(X270, N270)
    rep270 = {"n_filas": len(u), "unidades": int(N270.sum()),
              "alpha": a2u, "LL1": LL1u, "LL2": LL2u,
              "LRT": 2 * (LL2u - LL1u),
              "R_CV": float(np.mean(P270.std(0, ddof=1) / P270.mean(0)) /
                            np.mean(np.sqrt(P270.mean(0) * (1 - P270.mean(0)) / N270.mean()) / P270.mean(0))),
              "W": kendall_w(P270)}
except Exception as e:
    rep270 = {"error": str(e)}

# ------------------------------------------------------------------ guardar
modelos.to_csv(f"{OUT}/modelos_ur278.csv", index=False)
gof.to_csv(f"{OUT}/gof_ur278.csv", index=False)
col.to_csv(f"{OUT}/columnas_ur278.csv", index=False)
tend.to_csv(f"{OUT}/tendencias_ur278.csv", index=False)
np.save(f"{OUT}/sim_trend.npy", t_sim)
np.save(f"{OUT}/sim_cp.npy", cp_sim)

res = {"n": n, "k": k, "unidades": int(N.sum()),
       "p1": p1.tolist(), "p2": p2.tolist(), "alpha2": alpha2,
       "alpha_prof": alpha_prof, "LRT": LRT, "p_LRT_mixtura": float(p_LRT_mixtura),
       "p_LRT_boot": float(p_LRT_boot), "overdisp_M2": float(overdisp_M2),
       "tend_obs": float(t_obs), "p_trend": float(p_trend),
       "cp_obs": float(cp_obs), "p_cp": float(p_cp),
       "obs": {k2: float(v) for k2, v in obs.items()},
       "ur270": rep270}
json.dump(res, open(f"{OUT}/resultados_02.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ------------------------------------------------------------------ imprimir
L = []
L.append("=== UR278: 24 registros completos, 54 601 unidades ===")
L.append(modelos.to_string(index=False, float_format=lambda z: f"{z:.2f}"))
L.append("")
L.append(f"M2: alpha = {alpha2:.1f}; factor de sobredispersion en N medio ({Nbar:.0f}): {overdisp_M2:.1f}")
L.append(f"LRT sobredispersion (perfil) = {LRT:.1f}; p mixtura = {p_LRT_mixtura:.2e}; p bootstrap = {p_LRT_boot:.4f}")
L.append("")
L.append("=== GOF por simulacion (M1: 4000 sims; M2: 2000 sims) ===")
L.append(gof.pivot(index="estadistico", columns="modelo",
                   values=["observado", "sim_media", "p"]).to_string(float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== Columnas (beta-binomial marginal) ===")
L.append(col[["columna", "media_p", "CV_obs", "CV_mult", "CV_ratio", "rho_bb",
              "se_rho", "p_LRT", "q_LRT_BH", "min", "max"]].to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== Tendencias con el orden (parcial, controlando log N) y elasticidad ===")
L.append(tend.to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append(f"Tendencia multivariada: obs {t_obs:.4f}; p permutacion = {p_trend:.4f}")
L.append(f"Changepoint: obs {cp_obs:.4f}; p permutacion = {p_cp:.4f}")
L.append("")
L.append("=== Replicacion UR270 ===")
L.append(json.dumps(rep270, ensure_ascii=False, indent=2))

txt = "\n".join(L)
open(f"{OUT}/salida_02.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
