# -*- coding: utf-8 -*-
"""
01_datos.py -- estructura de las 9 columnas de UR278 y comparacion con UR270.
Se usan las 24 filas con exactamente 9 columnas (54 601 unidades) para la
composicion; el total del libro (61 790) incluye las 4 filas incompletas.
Salidas: columnas_ur278.csv, filas_ur278.csv
"""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
rng = np.random.default_rng(20261018)
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
T = pd.read_csv(RAIZ/"analisis/13_sistema_incahuasi/ur278_tabla.csv")
cols = [f"c{i}" for i in range(1, 10)]
T9 = T[T.n == 9].copy()
X = T9[cols].to_numpy(float)
total_libro = int(T[cols].sum(numeric_only=True).sum())

suma = X.sum(0); total = suma.sum()
cuota = suma/total
d = pd.DataFrame({"parte": cols, "suma": suma.astype(int), "cuota": cuota,
                  "media_fila": X.mean(0), "sd_fila": X.std(0, ddof=1),
                  "cv_fila": X.std(0, ddof=1)/X.mean(0)})
d["rango"] = d.suma.rank(ascending=False).astype(int)

rho_fila = np.array([stats.spearmanr(np.arange(1, 10), X[i])[0] for i in range(len(X))])
es_max = (X == X.max(1, keepdims=True)).sum(0)
es_min = (X == X.min(1, keepdims=True)).sum(0)
d["es_max"] = es_max; d["es_min"] = es_min
rango_rel = (X.max(1) - X.min(1)) / X.mean(1)
cv_fila = X.std(1, ddof=1) / X.mean(1)

print("UR278: %d filas completas (de 28), %d unidades; libro completo %d"
      % (len(X), total, total_libro))
print(d[["parte", "suma", "cuota", "rango", "es_max", "es_min"]].to_string(index=False))
print("\nSpearman(indice,col) por fila: media %.3f, mediana %.3f, min %.3f, max %.3f"
      % (rho_fila.mean(), np.median(rho_fila), rho_fila.min(), rho_fila.max()))
print("filas con rho<0: %d/%d ; con rho<=-0.5: %d" %
      ((rho_fila < 0).sum(), len(X), (rho_fila <= -0.5).sum()))
print("rango relativo dentro de fila: mediana %.3f (IQR %.3f-%.3f)"
      % (np.median(rango_rel), *np.percentile(rango_rel, [25, 75])))
print("CV dentro de fila: mediana %.3f" % np.median(cv_fila))

orden = d.sort_values("suma", ascending=False).parte.tolist()
print("\nOrden observado por suma:", " > ".join(orden))
print("Cuotas: " + ", ".join("%s=%.4f" % (r.parte, r.cuota) for r in d.itertuples()))

# comparacion con el total de las 28 filas (incluye filas incompletas)
s28 = T[cols].sum(numeric_only=True)
p28 = s28/s28.sum()
o28 = [cols[i] for i in np.argsort(-p28.to_numpy())]
print("28 filas (incl. incompletas): " + " > ".join(o28))
print("  cuotas: " + ", ".join("%s=%.4f" % (c, p28[c]) for c in cols))
print("  CV=%.3f, max/min=%.2f" % (p28.std(ddof=1)/p28.mean(), p28.max()/p28.min()))
pd.DataFrame({"parte": cols, "suma_24filas": suma.astype(int), "cuota_24filas": cuota,
              "suma_28filas": s28.astype(int).to_numpy(), "cuota_28filas": p28.to_numpy()}
             ).to_csv(AQUI/"columnas_dos_versiones.csv", index=False)

f9 = pd.read_csv(RAIZ/"analisis/ds/n_rejilla/firma_9_partes.csv", encoding="utf-8-sig")
u270 = f9.set_index("parte").loc[cols, "prop_media_UR270"].to_numpy()
rho270 = stats.spearmanr(cuota, u270)
r_p = stats.pearsonr(cuota, u270)
print("\nUR278 vs UR270: Spearman rho=%.3f (p=%.4f); Pearson r=%.3f (p=%.4f)"
      % (rho270[0], rho270[1], r_p[0], r_p[1]))
print("UR270 cuotas:", ", ".join("%.3f" % v for v in u270))

# --- nulo: permutar etiquetas de columna DENTRO de cada fila --------------
B = 20000
rho_null = np.empty(B); r2_null = np.empty(B)
def stat_col(Y):
    s = Y.sum(0); p = s/s.sum()
    rho = stats.spearmanr(np.arange(1, 10), p)[0]
    return rho, np.corrcoef(np.arange(1, 10), p)[0, 1]**2
rho_obs, r2_obs = stat_col(X)
for b in range(B):
    Y = np.array([rng.permutation(row) for row in X])
    rho_null[b], r2_null[b] = stat_col(Y)
p_rho = (1 + (rho_null <= rho_obs).sum()) / (B + 1)
p_r2 = (1 + (r2_null >= r2_obs).sum()) / (B + 1)
print("\nNulo de posicion (permutar columnas dentro de fila, B=%d):" % B)
print("  rho observado=%.3f; nulo media=%.3f; p(una cola, rho<=obs)=%.5f"
      % (rho_obs, rho_null.mean(), p_rho))
print("  R2 observado=%.3f; p=%.5f" % (r2_obs, p_r2))

d.to_csv(AQUI/"columnas_ur278.csv", index=False)
pd.DataFrame({"fila": np.arange(len(X)), "total": X.sum(1), "rho_pos": rho_fila,
              "rango_rel": rango_rel, "cv_fila": cv_fila}).to_csv(AQUI/"filas_ur278.csv", index=False)
print("\nGuardado: columnas_ur278.csv, filas_ur278.csv")
