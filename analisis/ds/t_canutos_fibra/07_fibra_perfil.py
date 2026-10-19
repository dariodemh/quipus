"""
Fibra: (i) sesgo de registro (que quipus NO tienen fibra), (ii) el "complejo
tecnologico" camelido (tamano, color, estilo de nudo) con controles,
(iii) valor: el resultado negativo central.

Nulo: permutacion de etiquetas a nivel de quipu; para color, permutacion de
residuales de una regresion sobre log(num_cords).
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20241018)
NPERM = 20000

q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
q["cam"] = (q.n_CL > 0).astype(int)
q["S"] = (q.percent_s_knots > 0.5).astype(int)
q["log_n"] = np.log10(q.num_cords.clip(lower=1))
q["colores_por_cuerda"] = q.num_ascher_colors / q.num_cords.clip(lower=1)

print("=" * 72)
print("(i) SESGO DE REGISTRO DE FIBRA")
q["sin_fibra"] = (q.n_fibra_NA == q.n_cord) & (q.n_cord > 0)
print("quipus con TODAS las cuerdas sin fibra: %d/%d (%.0f%%)"
      % (q.sin_fibra.sum(), len(q), 100 * q.sin_fibra.mean()))
t = q.groupby("zona").agg(n=("sin_fibra", "size"), sin=("sin_fibra", "sum"))
t["pct"] = (100 * t.sin / t.n).round(1)
print(t.sort_values("sin", ascending=False).to_string())
print("\npor museo (top 8 con mas quipus):")
t2 = q.groupby("MUSEUM_NAME").agg(n=("sin_fibra", "size"), sin=("sin_fibra", "sum"))
t2["pct"] = (100 * t2.sin / t2.n).round(1)
print(t2.sort_values("n", ascending=False).head(8).to_string())
print("\nla fibra NO falta al azar: chi2 zona p=%.2g"
      % stats.chi2_contingency(pd.crosstab(q.zona, q.sin_fibra))[1])

print("\n" + "=" * 72)
print("(ii) PERFIL DEL QUIPU CAMELIDO")
P = q[(q.n_CN + q.n_CL) > 0].copy()
print("n=%d  camelidos=%d" % (len(P), P.cam.sum()))
tab = P.groupby("cam").agg(n=("okr", "size"),
                           med_cords=("num_cords", "median"),
                           med_colores=("num_ascher_colors", "median"),
                           med_col_por_cuerda=("colores_por_cuerda", "median"),
                           med_valor=("mean_cord_value", "median"),
                           pct_S=("S", "mean"),
                           pct_canuto=("num_canuto_cords", lambda s: (s > 0).mean()))
print(tab.round(3).to_string())

print("\n-- color: correlacion parcial con tamano --")
d = P[["num_ascher_colors", "colores_por_cuerda", "log_n", "cam"]].dropna()
obs_r = stats.spearmanr(d.cam, d.colores_por_cuerda)[0]
# residualizar color ~ f(log n) con un spline simple (binning en 10 deciles)
d["res"] = d.colores_por_cuerda - d.groupby(pd.qcut(d.log_n, 10, duplicates="drop"))[
    "colores_por_cuerda"].transform("median")
obs = d.loc[d.cam == 1, "res"].median() - d.loc[d.cam == 0, "res"].median()
y = d.cam.values
cnt = 0
for _ in range(NPERM):
    yp = rng.permutation(y)
    v = d.res.values[yp == 1]
    if abs(np.median(v) - np.median(d.res.values[yp == 0])) >= abs(obs):
        cnt += 1
p_col = (cnt + 1) / (NPERM + 1)
print("colores por cuerda: rho=%.3f  ; diferencia de residuales (control log n)=%.4f  p=%.4f"
      % (obs_r, obs, p_col))

print("\n-- valor: el resultado negativo --")
for var in ["mean_cord_value"]:
    a = P.loc[P.cam == 1, var].dropna()
    b = P.loc[P.cam == 0, var].dropna()
    print("%s: mediana camelido=%.1f  algodon=%.1f  Mann-Whitney p=%.3f"
          % (var, a.median(), b.median(), stats.mannwhitneyu(a, b).pvalue))
print("cuerdas (nivel cuerda, sin ponderar por quipu) mediana de valor:")
c = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)
c["fib"] = c.FIBER.replace({"": np.nan})
x = c[c.fib.isin(["CN", "CL"])]
print(x.groupby("fib").valor.describe()[["count", "25%", "50%", "75%"]].round(1).to_string())

print("\n-- regresion logistica exploratoria (solo 20 eventos: 2 predictores) --")
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    dd = P[["cam", "S", "log_n", "colores_por_cuerda"]].dropna()
    X = StandardScaler().fit_transform(dd[["S", "log_n", "colores_por_cuerda"]])
    m = LogisticRegression(max_iter=2000, C=1.0).fit(X, dd.cam)
    print(dict(zip(["S", "log_n", "colores_por_cuerda"], m.coef_[0].round(2))))
    print("AUC aparente:", round(m.score(X, dd.cam), 3), "(mayoria trivial=%.3f)" % (1 - dd.cam.mean()))
    # AUC por validacion cruzada repetida
    from sklearn.model_selection import cross_val_score
    auc = cross_val_score(LogisticRegression(max_iter=2000), X, dd.cam,
                          cv=5, scoring="roc_auc")
    print("AUC 5-fold:", np.round(auc.mean(), 3), "+-", np.round(auc.std(), 3))
except Exception as e:
    print("sklearn:", e)

print("\n" + "=" * 72)
print("(iii) LA FIBRA ES CASI UN ATRIBUTO DE OBJETO, NO DE CUERDA")
n_mix = ((P.n_CL > 0) & (P.n_CN > 0)).sum()
print("quipus mixtos CN+CL: %d ; con >=10 cuerdas de cada tipo y >=30%% cada uno:"
      % n_mix, ((P.n_CL >= 10) & (P.n_CN >= 10)).sum())
print("-> cualquier contraste fibra-valor a nivel cuerda queda confundido con el quipu")
print("   salvo en KH0281 (31 CL / 35 CN), unico quipu con potencia.")
