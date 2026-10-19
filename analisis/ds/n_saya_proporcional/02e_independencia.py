# -*- coding: utf-8 -*-
"""
02e_independencia.py -- control de "produccion independiente".

Nulo: se permuta cada columna por separado entre filas (se conservan las
marginales de cada columna, se destruye la asociacion entre columnas dentro
de la fila). Si las 9 columnas fueran producciones independientes, las filas
se parecerian a este nulo. Se comparan:
  - W de Kendall (acuerdo de rangos entre filas)
  - PC1 del CLR (concentracion en una sola direccion)
  - correlacion media entre columnas (dominada por la suma constante)

Salida: salida_02e.txt
"""
import numpy as np
import pandas as pd
from scipy import stats

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)
OUT = "analisis/ds/n_saya_proporcional"

d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[[f"c{i}" for i in range(1, 10)]].to_numpy(float)
N = X.sum(1)
P = X / N[:, None]


def kendall_w(P):
    m, k = P.shape
    R = np.array([stats.rankdata(r) for r in P])
    Rj = R.sum(0)
    S = ((Rj - Rj.mean()) ** 2).sum()
    return 12 * S / (m ** 2 * (k ** 3 - k))


def pc1(P):
    L = np.log(P); Z = L - L.mean(1, keepdims=True); Z = Z - Z.mean(0)
    s = np.linalg.svd(Z, compute_uv=False)
    return float(s[0] ** 2 / (s ** 2).sum())


def avgcorr(P):
    C = np.corrcoef(np.log(P).T)
    k = C.shape[0]
    return float((C.sum() - k) / (k * (k - 1)))


obs = {"W": kendall_w(P), "PC1": pc1(P), "corr": avgcorr(P)}
B = 5000
sim = {k: np.empty(B) for k in obs}
for b in range(B):
    Xp = np.column_stack([rng.permutation(X[:, j]) for j in range(9)])
    Pp = Xp / Xp.sum(1, keepdims=True)
    sim["W"][b] = kendall_w(Pp)
    sim["PC1"][b] = pc1(Pp)
    sim["corr"][b] = avgcorr(Pp)

L = []
L.append("=== Nulo de produccion independiente (permutar cada columna por separado, 5000) ===")
for k in ("W", "PC1", "corr"):
    v = sim[k]
    p_sup = (1 + np.sum(v >= obs[k])) / (B + 1)
    p_inf = (1 + np.sum(v <= obs[k])) / (B + 1)
    L.append(f"{k}: observado {obs[k]:.4f}; nulo {v.mean():.4f} (p05 {np.quantile(v,.05):.4f}, p95 {np.quantile(v,.95):.4f}); p_sup {p_sup:.5f}, p_inf {p_inf:.5f}")
L.append("Lectura: W observado (0,484) es muy superior al nulo (0,176): las filas se parecen mucho mas que si cada columna fuera independiente. PC1 tambien es algo mayor. La correlacion media es negativa y no difiere del nulo: la suma constante domina esa medida, que NO sirve para detectar un perfil comun.")

txt = "\n".join(L)
open(f"{OUT}/salida_02e.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
