"""04_incahuasi.py — Métricas comparables de UR278 (Incahuasi) para contrastar con el registro wanka.
Salida: resultados_04.json, salida_04.txt
"""
import os, json
import numpy as np, pandas as pd
from scipy import stats
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(20261018)

t = pd.read_csv("../../13_sistema_incahuasi/ur278_tabla.csv")
cols = [f"c{i}" for i in range(1, 10)]
X = t[cols].astype(float)
completas = X.dropna()
print("UR278:", len(t), "filas;", X.notna().sum().sum(), "celdas con dato;",
      len(completas), "filas completas")

# CV dentro de fila (las 9 partes)
cv_fila = (completas.std(axis=1, ddof=1) / completas.mean(axis=1))
maxmin = (completas.max(axis=1) / completas.min(axis=1))
print(f"CV entre las 9 partes, por fila: mediana={cv_fila.median():.3f} "
      f"[{cv_fila.quantile(.05):.3f}; {cv_fila.quantile(.95):.3f}]")
print(f"max/min por fila: mediana={maxmin.median():.2f} [{maxmin.quantile(.05):.2f}; {maxmin.quantile(.95):.2f}]")

# perfil medio de proporciones
P = completas.div(completas.sum(axis=1), axis=0)
perfil = P.mean()
cv_perfil = perfil.std(ddof=1) / perfil.mean()
print("perfil medio (%):", np.round(100 * perfil.values, 1).tolist())
print(f"CV del perfil medio entre las 9 columnas = {cv_perfil:.3f}")

# estructura de columnas: Friedman + nulo permutando dentro de fila
chi, pfried = stats.friedmanchisquare(*[completas[c].values for c in cols])
print(f"Friedman (26 filas completas): chi2={chi:.1f}, p={pfried:.2e}")

# variabilidad entre filas (los 28 registros): CV de los totales
tot = completas.sum(axis=1)
print(f"totales de fila: mediana={tot.median():.0f} rango [{tot.min():.0f},{tot.max():.0f}] "
      f"CV entre filas={tot.std(ddof=1)/tot.mean():.2f}")

# co-movimiento entre columnas (análogo de T1 wanka): correlación de perfiles por fila
C = completas.corr(method="spearman")
iu = np.triu_indices_from(C.values, 1)
obs = np.nanmean(C.values[iu])
vals = []
for _ in range(20000):
    Y = completas.apply(lambda col: rng.permutation(col.values))
    vals.append(np.nanmean(Y.corr(method="spearman").values[iu]))
vals = np.array(vals)
print(f"co-movimiento entre las 9 columnas: rho medio={obs:.3f}, "
      f"p={(np.sum(vals>=obs)+1)/20001:.4f} (nulo {np.percentile(vals,97.5):.3f})")

# ¿cuotas enteras? proporción de celdas múltiplo de 5/10
v = completas.values.ravel()
print(f"múltiplos de 10 en UR278: {np.mean(v%10==0):.3f}; de 5: {np.mean(v%5==0):.3f} (n={len(v)})")

json.dump(dict(n_filas=len(t), n_completas=len(completas),
               cv_fila=float(cv_fila.median()), maxmin=float(maxmin.median()),
               cv_perfil=float(cv_perfil), friedman=[float(chi), float(pfried)],
               comov=float(obs), comov_p=float((np.sum(vals>=obs)+1)/20001)),
          open("resultados_04.json", "w"), indent=1)
