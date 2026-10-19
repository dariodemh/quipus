"""01. Demografia: ¿son las columnas de las tablas categorias de edad/sexo?

Prueba principal en UR278 (28 registros x 9 columnas) y cribado de todas las
tablas reconstruibles (R>=3, K>=4).

Estadisticos:
  CVcol  = coeficiente de variacion entre las medias de columna (perfil).
  CVfila = CV dentro de fila (dispersion de magnitudes de un registro).
  max/min.
  D      = distancia de Aitchison minima entre el perfil observado y un modelo
           demografico, minimizando sobre las K! asignaciones columna->banda
           (resuelto exacto como problema de asignacion lineal).

Nulos:
  (1) H0 demografico: las columnas SON bandas de un modelo de poblacion estable
      (Siler, e0~28). Bootstrap parametrico Dirichlet-multinomial con la misma
      dispersion entre filas que la observada.
  (2) Dirichlet ajustado por momentos (columnas intercambiables, control de
      dispersion).
  (3) permutacion de celdas dentro de fila (columnas intercambiables exactas).
"""
import warnings
warnings.filterwarnings("ignore", message="Mean of empty slice")
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare
from scipy.optimize import linear_sum_assignment
import comun as C

rng = np.random.default_rng(C.SEED)
B = 4000


def clr(p, eps=1e-9):
    p = np.asarray(p, float) + eps
    p = p / p.sum()
    return np.log(p) - np.log(p).mean()


def d_aitchison(obs, modelo):
    """Distancia minima de Aitchison sobre asignaciones columna->banda."""
    a, b = clr(obs), clr(modelo)
    cost = -np.outer(a, b)          # max a.P.b  <=> min distancia
    r, c = linear_sum_assignment(cost)
    perm = c[np.argsort(r)]
    return float(np.linalg.norm(a - b[perm])), perm


def cv_col(sh):
    m = np.nanmean(sh, axis=0)
    return float(m.std(ddof=1) / m.mean())


def modelo_bandas(K):
    """K bandas: 0-4, 5-9, ..., 5(K-1)+ ; la ultima abierta a 105."""
    assert 2 <= K <= 12
    b = np.array([5 * i for i in range(K)] + [105.0])
    return C.edad_estable(b), b


def modelo_gp():
    """Esquema tipo Guaman Poma (9 grados, anchos desiguales)."""
    b = np.array([0, 2, 5, 10, 15, 20, 40, 60, 70, 105.0])
    return C.edad_estable(b), b


def ajustar_s0(sh, totales):
    """Concentracion Dirichlet por momentos, descontando ruido multinomial."""
    P = sh[np.isfinite(sh).all(1)]
    T = np.asarray(totales, float)[np.isfinite(sh).all(1)]
    if len(P) < 3:
        return 50.0
    mu = P.mean(0)
    var_obs = P.var(0, ddof=1)
    var_noise = np.mean(mu * (1 - mu) / T[:, None], axis=0)
    var_true = np.maximum(var_obs - var_noise, 1e-4 * mu * (1 - mu))
    s0 = np.mean(mu * (1 - mu) / var_true) - 1
    if not np.isfinite(s0):
        return 50.0
    return float(np.clip(s0, 2, 5000))


def sim_dm(totales, modelo, s0, rng):
    """Una tabla simulada bajo H0: p ~ Dirichlet(modelo*s0); N ~ Multinomial."""
    S = []
    for t in totales:
        p = rng.dirichlet(modelo * s0)
        p = np.maximum(p, 0)
        p = p / p.sum() * (1 - 1e-8)
        p[-1] = 1.0 - p[:-1].sum()
        S.append(rng.multinomial(int(max(t, 1)), p))
    S = np.asarray(S, float)
    return S / S.sum(1, keepdims=True)


# ---------------------------------------------------------------- UR278
u = pd.read_csv(C.RAIZ / "13_sistema_incahuasi" / "ur278_tabla.csv")
V = u[[f"c{i}" for i in range(1, 10)]].to_numpy(float)
tot = np.nansum(V, axis=1)
sh = V / tot[:, None]
obs_perfil = np.nanmean(sh, axis=0)
obs_cv = cv_col(sh)
s0 = ajustar_s0(sh, tot)

boot_cv, boot_mm = [], []
for _ in range(B):
    idx = rng.integers(0, len(V), len(V))
    s = sh[idx]
    boot_cv.append(cv_col(s))
    mm = np.nanmean(s, axis=0)
    boot_mm.append(mm.max() / mm.min())
ci_cv = np.percentile(boot_cv, [2.5, 97.5])
ci_mm = np.percentile(boot_mm, [2.5, 97.5])

print("=== UR278: perfil de columnas ===")
print("perfil %% : %s" % (obs_perfil * 100).round(1).tolist())
print("CVcol observado %.3f  IC95 bootstrap [%.3f, %.3f]" % (obs_cv, ci_cv[0], ci_cv[1]))
print("max/min observado %.2f  IC95 [%.2f, %.2f]" %
      (obs_perfil.max() / obs_perfil.min(), ci_mm[0], ci_mm[1]))
cvv = C.cv_intrafila(V)
print("CV intra-fila: mediana %.2f  p5-p95 [%.2f, %.2f]" %
      (np.median(cvv), *np.percentile(cvv, [5, 95])))
print("filas con max/min >= 3.6: %d/%d" %
      ((C.razon_max_min(V) >= 3.6).sum(), len(V)))
print("concentracion Dirichlet ajustada s0 = %.0f (CV fila ~ ruido+s0)" % s0)

print("\n=== Modelos demograficos vs observado (UR278) ===")
filas = []
for nombre, (mod, b) in [("S1_5a+", modelo_bandas(9)), ("S3_GP", modelo_gp())]:
    d, perm = d_aitchison(obs_perfil, mod)
    cvs, ds = [], []
    for _ in range(B):
        s = sim_dm(tot, mod, s0, rng)
        cvs.append(cv_col(s))
        ds.append(d_aitchison(np.nanmean(s, axis=0), mod)[0])
    cvs, ds = np.array(cvs), np.array(ds)
    p_cv = float((cvs <= obs_cv).mean())
    p_d = float((ds >= d).mean())
    print("%-8s CV=%.2f max/min=%.1f  D=%.2f  mejor orden=%s" %
          (nombre, mod.std(ddof=1) / mod.mean(), mod.max() / mod.min(), d, perm.tolist()))
    print("         perfil %%: %s" % (mod * 100).round(1).tolist())
    print("         bajo H0: CV medio %.2f [%.2f,%.2f]; p(CV<=obs)=%.4f" %
          (cvs.mean(), *np.percentile(cvs, [2.5, 97.5]), p_cv))
    print("                   D medio %.2f; p(D>=obs)=%.4f" % (ds.mean(), p_d))
    filas.append(dict(modelo=nombre, cv_modelo=mod.std(ddof=1) / mod.mean(),
                      mm_modelo=mod.max() / mod.min(), D=d, p_cv=p_cv, p_D=p_d))

# ---------------------------------------------------------------- estructura
print("\n=== Control: las columnas, ¿son intercambiables? ===")
ok = ~np.isnan(V).any(1)
if ok.sum() >= 5:
    st = friedmanchisquare(*[V[ok, j] for j in range(9)])
    print("Friedman (filas completas n=%d): chi2=%.1f p=%.2e" % (ok.sum(), st.statistic, st.pvalue))

null_cv = []
for _ in range(B):
    P = np.array([rng.permutation(r) for r in V])
    null_cv.append(cv_col(P / np.nansum(P, axis=1, keepdims=True)))
null_cv = np.array(null_cv)
print("nulo permutacion-fila: CV medio %.3f [%.3f,%.3f]; p(CV>=obs)=%.4f" %
      (null_cv.mean(), *np.percentile(null_cv, [2.5, 97.5]),
       (null_cv >= obs_cv).mean()))

# Dirichlet por momentos (columnas con las mismas medias observadas)
P = sh[np.isfinite(sh).all(1)]
mu = P.mean(0)
var = P.var(0, ddof=1)
s0b = float(np.mean(mu * (1 - mu)) / np.mean(np.maximum(var, 1e-9)) - 1)
alpha = np.maximum(mu * max(s0b, 1), 1e-3)
dcv = np.array([cv_col(rng.dirichlet(alpha, size=len(P))) for _ in range(500)])
print("Dirichlet por momentos (alpha medio %.1f): CV medio %.3f; p(CV>=obs)=%.4f" %
      (alpha.mean(), dcv.mean(), (dcv >= obs_cv).mean()))

# ---------------------------------------------------------------- emparejamiento 1:1 (sexos)
print("\n=== Firma de sexos: emparejamiento 1:1 de columnas ===")
print("correlaciones entre columnas:")
print(pd.DataFrame(np.corrcoef(V.T), index=[f"c{i}" for i in range(1, 10)],
                   columns=[f"c{i}" for i in range(1, 10)]).round(2).to_string())


def coste_parejas(M):
    """Mejor emparejamiento de 8 de las 9 columnas, min sum|log(a+1)/(b+1)|."""
    def rec(lst):
        if not lst:
            yield []
            return
        a = lst[0]
        for i in range(1, len(lst)):
            for resto in rec(lst[1:i] + lst[i + 1:]):
                yield [(a, lst[i])] + resto
    best = (np.inf, None, None)
    for fuera in range(M.shape[1]):
        rest = [c for c in range(M.shape[1]) if c != fuera]
        for pares in rec(rest):
            cost = np.nansum([np.abs(np.log((M[:, a] + 1) / (M[:, b] + 1))) for a, b in pares])
            if cost < best[0]:
                best = (float(cost), pares, fuera)
    return best


cost, pares, fuera = coste_parejas(V)
null_cost = []
for _ in range(500):
    Pn = np.column_stack([rng.permutation(V[:, j]) for j in range(9)])  # columnas independientes
    null_cost.append(coste_parejas(Pn)[0])
null_cost = np.array(null_cost)
print("mejor emparejamiento: coste=%.1f (fuera c%d), pares=%s" %
      (cost, fuera + 1, [(a + 1, b + 1) for a, b in pares]))
rat = []
for a, b in pares:
    with np.errstate(invalid="ignore", divide="ignore"):
        rat += list(np.maximum(V[:, a], V[:, b]) / np.minimum(V[:, a], V[:, b]))
rat = np.array(rat)
print("razon max/min dentro de cada par: mediana %.2f  p5-p95 [%.2f, %.2f]  (1:1 exacto = 1.00)"
      % (np.nanmedian(rat), *np.nanpercentile(rat, [5, 95])))
print("nulo columnas independientes: coste medio %.1f [%.1f,%.1f]; p(coste<=obs)=%.4f" %
      (null_cost.mean(), *np.percentile(null_cost, [2.5, 97.5]),
       (null_cost <= cost).mean()))

# ---------------------------------------------------------------- cribado tablas
print("\n=== Cribado de todas las tablas (R>=3, K>=4) ===")
c = C.cargar()
T = C.tablas(c, min_filas=3, min_cols=4)
print("tablas reconstruibles:", len(T), "; con K<=12:", sum(1 for m in T.values() if m["K"]<=12))
res = []
for k, m in T.items():
    if m["K"] > 12:      # los censos incas usan 10-12 grados; K>12 no es edad
        continue
    Vk = m["V"]
    tk = np.nansum(Vk, axis=1)
    shk = Vk / tk[:, None]
    perfil = np.nanmean(shk, axis=0)
    if not np.all(np.isfinite(perfil)) or perfil.min() <= 0:
        continue
    mod, b = modelo_bandas(m["K"])
    cv_o = cv_col(shk)
    d, perm = d_aitchison(perfil, mod)
    # p bajo H0 demografico (B corto)
    s0k = ajustar_s0(shk, tk)
    sims, dsims = [], []
    for _ in range(200):
        S = sim_dm(tk, mod, s0k, rng)
        sims.append(cv_col(S))
        dsims.append(d_aitchison(np.nanmean(S, axis=0), mod)[0])
    sims, dsims = np.array(sims), np.array(dsims)
    res.append(dict(kfg=k, R=m["R"], K=m["K"], cv_obs=cv_o,
                    cv_mod=mod.std(ddof=1) / mod.mean(),
                    ratio=cv_o / (mod.std(ddof=1) / mod.mean()),
                    mm_obs=perfil.max() / perfil.min(),
                    mm_mod=mod.max() / mod.min(), D=d,
                    p_modelo=float((sims <= cv_o).mean()),
                    p_D=float((dsims >= d).mean())))
R = pd.DataFrame(res)
R["q_modelo"] = C.bh(R.p_modelo.to_numpy())
R["q_D"] = C.bh(R.p_D.to_numpy())
print("CV observado: mediana %.2f  p5-p95 [%.2f, %.2f]" %
      (R.cv_obs.median(), *np.percentile(R.cv_obs, [5, 95])))
print("CV modelo (misma K): mediana %.2f" % R.cv_mod.median())
print("ratio CVobs/CVmodelo: mediana %.2f  p5-p95 [%.2f, %.2f]" %
      (R.ratio.median(), *np.percentile(R.ratio, [5, 95])))
print("tablas con ratio >= 0.6 (forma piramidal plausible): %d/%d (%.0f%%)" %
      ((R.ratio >= .6).sum(), len(R), 100 * (R.ratio >= .6).mean()))
print("tablas con ratio >= 0.8: %d/%d" % ((R.ratio >= .8).sum(), len(R)))
print("tablas con max/min >= 3.6: %d/%d" % ((R.mm_obs >= 3.6).sum(), len(R)))
print("tablas que NO rechazan el modelo de edad (q>=0.05): %d/%d" %
      ((R.q_modelo >= .05).sum(), R.q_modelo.notna().sum()))
print("tablas que no rechazan por forma (q_D>=0.05): %d/%d" %
      ((R.q_D >= .05).sum(), R.q_D.notna().sum()))
print("tablas que pasan AMBOS filtros (q_modelo>=0.05 y q_D>=0.05): %d/%d" %
      (((R.q_modelo >= .05) & (R.q_D >= .05)).sum(), len(R)))

R.to_csv(C.OUT / "demografia_tablas.csv", index=False)
pd.DataFrame(filas).to_csv(C.OUT / "demografia_ur278.csv", index=False)
print("\nguardado demografia_tablas.csv, demografia_ur278.csv")
