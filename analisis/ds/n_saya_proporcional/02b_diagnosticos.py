# -*- coding: utf-8 -*-
"""
02b_diagnosticos.py -- diagnosticos de la prueba A.

1. Localizacion del cambio de regimen y que columnas lo producen (p ajustado
   por la seleccion del corte).
2. Heterogeneidad de la sobredispersion entre columnas: rho comun frente a
   rho libre (LRT + bootstrap).
3. Verosimilitud predictiva leave-one-out M1 vs M2.
4. Robustez de la tendencia (leave-one-out, por tramos).
5. Cargas del primer componente y su relacion con orden y tamano.

Salidas: diagnosticos_ur278.csv, salida_02b.txt
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

d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[COLS].to_numpy(float)
N = d["N"].to_numpy(float)
P = X / N[:, None]
n, k = X.shape
orden = np.arange(1, n + 1)
logN = np.log(N)


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


def clr(P):
    L = np.log(P)
    return L - L.mean(1, keepdims=True)


Z = clr(P)
Zc = Z - Z.mean(0)


# ---------------------------------------------------------------- 1. changepoint
def cp_stat(Zc, cortes):
    m = len(Zc)
    tot = (Zc ** 2).sum()
    vals = []
    for cut in cortes:
        a = Zc[:cut].mean(0)
        b = Zc[cut:].mean(0)
        vals.append((cut * (a ** 2).sum() + (m - cut) * (b ** 2).sum()) / tot)
    vals = np.array(vals)
    i = int(np.argmax(vals))
    return float(vals[i]), int(cortes[i])


cortes = np.arange(4, n - 3)
cp_obs, cut_obs = cp_stat(Zc, cortes)
B = 5000
cp_sim = np.empty(B)
for b in range(B):
    cp_sim[b] = cp_stat(Zc[rng.permutation(n)], cortes)[0]
p_cp = (1 + np.sum(cp_sim >= cp_obs)) / (B + 1)

# por columna: estadistico maximo sobre cortes, p ajustado por seleccion
def col_cp_stat(x, cortes):
    vals = []
    for cut in cortes:
        a, b = x[:cut], x[cut:]
        s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        vals.append(abs(a.mean() - b.mean()) / (s + 1e-12))
    return float(np.max(vals))

dif = P[cut_obs:].mean(0) - P[:cut_obs].mean(0)
cpcol = []
for j in range(k):
    obs = col_cp_stat(P[:, j], cortes)
    cnt = 0
    for b in range(2000):
        if col_cp_stat(P[rng.permutation(n), j], cortes) >= obs:
            cnt += 1
    # p post-hoc en el corte elegido (no corrige la seleccion del corte)
    cnt2 = 0
    Bf = 5000
    for b in range(Bf):
        idx = rng.permutation(n)
        dd = P[idx[cut_obs:], j].mean() - P[idx[:cut_obs], j].mean()
        if abs(dd) >= abs(dif[j]):
            cnt2 += 1
    cpcol.append({"columna": COLS[j], "dif_antes_despues": dif[j],
                  "t_max": obs, "p_sel": (1 + cnt) / 2001,
                  "p_cut_fijo": (1 + cnt2) / (Bf + 1)})
cpcol = pd.DataFrame(cpcol)
cpcol["q_BH_sel"] = bh(cpcol.p_sel.values)
cpcol["q_BH_fijo"] = bh(cpcol.p_cut_fijo.values)

# ---------------------------------------------------------------- 2. rho comun
def bb_ll(x, N, p, rho):
    a = p * (1 / rho - 1)
    b = (1 - p) * (1 / rho - 1)
    return float(np.sum(special.gammaln(N + 1) - special.gammaln(x + 1)
                        - special.gammaln(N - x + 1)
                        + special.betaln(x + a, N - x + b) - special.betaln(a, b)))


def fit_bb_free(x, N):
    p0 = x.sum() / N.sum()

    def nll(par):
        p = 1 / (1 + np.exp(-par[0]))
        rho = 1 / (1 + np.exp(-par[1]))
        return -bb_ll(x, N, p, rho)

    r = minimize(nll, [np.log(p0 / (1 - p0)), np.log(0.005 / 0.995)],
                 method="L-BFGS-B")
    return (-r.fun, 1 / (1 + np.exp(-r.x[0])), 1 / (1 + np.exp(-r.x[1])))


def fit_bb_common(X, N, rho=None):
    """rho comun; p_j libre por columna. Si rho es None se optimiza."""
    if rho is None:
        def nll(par):
            r = 1 / (1 + np.exp(-par[-1]))
            s = 0.0
            for j in range(X.shape[1]):
                p = 1 / (1 + np.exp(-par[j]))
                s += bb_ll(X[:, j], N, p, r)
            return -s
        p0 = X.sum(0) / N.sum()
        x0 = list(np.log(p0 / (1 - p0))) + [np.log(0.006 / 0.994)]
        r = minimize(nll, x0, method="L-BFGS-B", options={"maxiter": 4000})
        return -r.fun, 1 / (1 + np.exp(-r.x[-1])), 1 / (1 + np.exp(-r.x[:-1]))
    else:
        ll = 0.0
        ps = []
        for j in range(X.shape[1]):
            x = X[:, j]
            f = lambda z: -bb_ll(x, N, 1 / (1 + np.exp(-z)), rho)
            r = minimize_scalar(f, bounds=(-12, 12), method="bounded")
            ll += -r.fun
            ps.append(1 / (1 + np.exp(-r.x)))
        return ll, rho, np.array(ps)


free = [fit_bb_free(X[:, j], N) for j in range(k)]
LL_free = sum(f[0] for f in free)
LL_com, rho_com, ps_com = fit_bb_common(X, N)
LRT_het = 2 * (LL_free - LL_com)
p_het = stats.chi2.sf(LRT_het, k - 1)

B_het = 400
het_sim = np.empty(B_het)
for b in range(B_het):
    Xs = np.empty_like(X)
    for j in range(k):
        p = ps_com[j]
        a = p * (1 / rho_com - 1)
        bb = (1 - p) * (1 / rho_com - 1)
        pi = rng.beta(a, bb, size=n)
        Xs[:, j] = rng.binomial(N.astype(int), pi)
    llf = sum(fit_bb_free(Xs[:, j], N)[0] for j in range(k))
    llc = fit_bb_common(Xs, N, rho=rho_com)[0]
    het_sim[b] = 2 * (llf - llc)
p_het_boot = (1 + np.sum(het_sim >= LRT_het)) / (B_het + 1)

# ---------------------------------------------------------------- 3. LOO M1 vs M2
def dm_ll_rows(x, N, p, alpha):
    a = alpha * p
    c = special.gammaln(N + 1) - special.gammaln(x + 1).sum(axis=1)
    t = (special.gammaln(alpha) - special.gammaln(N + alpha)
         + (special.gammaln(x + a) - special.gammaln(a)).sum(axis=1))
    return c + t


def mult_ll_rows(x, N, p):
    c = special.gammaln(N + 1) - special.gammaln(x + 1).sum(axis=1)
    return c + (x * np.log(p)).sum(axis=1)


def fit_dm_train(x, N):
    p0 = x.sum(0) / N.sum()
    kk = x.shape[1]
    th0 = np.log(p0[:-1] / p0[-1])

    def nll(par):
        z = np.concatenate([par[:kk - 1], [0.0]])
        z = z - z.max()
        p = np.exp(z) / np.exp(z).sum()
        alpha = np.exp(par[kk - 1])
        if alpha > 1e9:
            return 1e12
        return -dm_ll_rows(x, N, p, alpha).sum()

    best = None
    for a0 in (30.0, 200.0, 2000.0):
        r = minimize(nll, np.concatenate([th0, [np.log(a0)]]),
                     method="L-BFGS-B", options={"maxiter": 3000})
        if best is None or r.fun < best.fun:
            best = r
    z = np.concatenate([best.x[:kk - 1], [0.0]])
    z = z - z.max()
    p = np.exp(z) / np.exp(z).sum()
    return p, float(np.exp(best.x[kk - 1]))


loo = []
for i in range(n):
    m = np.ones(n, bool); m[i] = False
    p1 = X[m].sum(0) / N[m].sum()
    ll1 = mult_ll_rows(X[i:i + 1], N[i:i + 1], p1)[0]
    p2, a2 = fit_dm_train(X[m], N[m])
    ll2 = dm_ll_rows(X[i:i + 1], N[i:i + 1], p2, a2)[0]
    loo.append({"fila": i + 1, "LL_M1": ll1, "LL_M2": ll2, "dif": ll2 - ll1,
                "alpha_train": a2})
loo = pd.DataFrame(loo)

# ---------------------------------------------------------------- 4. robustez
def trend_stat_local(P, N, orden):
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


t_full = trend_stat_local(P, N, orden)
loo_t = []
for i in range(n):
    m = np.ones(n, bool); m[i] = False
    loo_t.append(trend_stat_local(P[m], N[m], np.arange(1, m.sum() + 1)))
loo_t = np.array(loo_t)

# por tramos: antes y despues del corte
tramos = []
for nombre, sl in (("antes", slice(0, cut_obs)), ("despues", slice(cut_obs, n))):
    idx = np.arange(n)[sl]
    t = trend_stat_local(P[idx], N[idx], np.arange(1, len(idx) + 1))
    Bt = 2000
    sim = np.array([trend_stat_local(P[idx], N[idx], rng.permutation(np.arange(1, len(idx) + 1)))
                    for _ in range(Bt)])
    tramos.append({"tramo": nombre, "n": len(idx), "T": t,
                   "p": (1 + np.sum(sim >= t)) / (Bt + 1)})
tramos = pd.DataFrame(tramos)

# ---------------------------------------------------------------- 5. PC
U, S, Vt = np.linalg.svd(Zc, full_matrices=False)
var_sh = S ** 2 / (S ** 2).sum()
pc = pd.DataFrame({"columna": COLS, "PC1": Vt[0], "PC2": Vt[1], "PC3": Vt[2]})
pc["media_p"] = P.mean(0)
cor_pc = {"PC1_orden": stats.spearmanr(U[:, 0] * S[0], orden)[0],
          "PC1_logN": stats.spearmanr(U[:, 0] * S[0], logN)[0],
          "PC2_orden": stats.spearmanr(U[:, 1] * S[1], orden)[0],
          "PC2_logN": stats.spearmanr(U[:, 1] * S[1], logN)[0]}

# ---------------------------------------------------------------- guardar
cpcol.to_csv(f"{OUT}/changepoint_columnas.csv", index=False)
loo.to_csv(f"{OUT}/loo_ur278.csv", index=False)
pc.to_csv(f"{OUT}/pc_ur278.csv", index=False)
res = {"cp_obs": cp_obs, "cut": cut_obs, "p_cp": float(p_cp),
       "gaps_antes": d.grupo.values[:cut_obs].tolist(),
       "gaps_despues": d.grupo.values[cut_obs:].tolist(),
       "dif_antes_despues": dif.tolist(),
       "rho_comun": rho_com, "LL_free": LL_free, "LL_comun": LL_com,
       "LRT_het": LRT_het, "p_het": float(p_het), "p_het_boot": float(p_het_boot),
       "loo_M1": float(loo.LL_M1.sum()), "loo_M2": float(loo.LL_M2.sum()),
       "loo_dif": float(loo.dif.sum()), "loo_gana_M2": int((loo.dif > 0).sum()),
       "trend_full": t_full, "trend_loo_min": float(loo_t.min()),
       "trend_loo_max": float(loo_t.max()),
       "fila_mas_influyente": int(np.argmin(loo_t) + 1),
       "tramos": tramos.to_dict(orient="records"),
       "var_shares": var_sh.tolist(), "cor_pc": cor_pc}
json.dump(res, open(f"{OUT}/resultados_02b.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

L = []
L.append("=== 1. Cambio de regimen ===")
L.append(f"Mejor corte: fila {cut_obs} (grupos {d.grupo.values[cut_obs-1]} | {d.grupo.values[cut_obs]}); estadistico {cp_obs:.4f}; p permutacion {p_cp:.4f}")
L.append(cpcol.to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== 2. Heterogeneidad de rho entre columnas ===")
L.append(f"rho comun = {rho_com:.5f}; LL libre = {LL_free:.2f}; LL comun = {LL_com:.2f}")
L.append(f"LRT = {LRT_het:.2f} (8 gl); p chi2 = {p_het:.4g}; p bootstrap = {p_het_boot:.4f}")
L.append("rho por columna: " + ", ".join(f"{c}={f[2]:.5f}" for c, f in zip(COLS, free)))
L.append("")
L.append("=== 3. Verosimilitud predictiva leave-one-out ===")
L.append(f"LL M1 = {loo.LL_M1.sum():.2f}; LL M2 = {loo.LL_M2.sum():.2f}; diferencia = {loo.dif.sum():.2f}")
L.append(f"M2 gana en {int((loo.dif>0).sum())}/{n} filas; rango de alpha de entrenamiento {loo.alpha_train.min():.0f}-{loo.alpha_train.max():.0f}")
L.append("")
L.append("=== 4. Robustez de la tendencia ===")
L.append(f"T completo = {t_full:.4f}; al quitar una fila: {loo_t.min():.4f}-{loo_t.max():.4f} (fila mas influyente: {np.argmin(loo_t)+1})")
L.append(f"nulo aproximado 1/(n-2) = {1/(n-2):.4f}")
L.append(tramos.to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== 5. Componentes principales del CLR ===")
L.append(f"varianza explicada: {np.round(var_sh[:4],3).tolist()}")
L.append(pc.to_string(index=False, float_format=lambda z: f"{z:.3f}"))
L.append(f"correlaciones: {json.dumps(cor_pc, ensure_ascii=False)}")

txt = "\n".join(L)
open(f"{OUT}/salida_02b.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
