# -*- coding: utf-8 -*-
"""
04_controles.py -- descomposicion de varianza, estabilidad de la firma y
controles de la lectura "9 partes".
"""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
rng = np.random.default_rng(20261018)
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
T = pd.read_csv(RAIZ/"analisis/13_sistema_incahuasi/ur278_tabla.csv")
T = T[T.n == 9]
cols = [f"c{i}" for i in range(1, 10)]
X = T[cols].to_numpy(float)
L = np.log(X)
n, k = L.shape

# --- 1. descomposicion de varianza (modelo aditivo en log) ---------------
gm = L.mean(); fe = L.mean(1) - gm; ce = L.mean(0) - gm
sst = ((L - gm)**2).sum()
ss_row = k*(fe**2).sum(); ss_col = n*(ce**2).sum()
res = L - (gm + fe[:, None] + ce[None, :])
ss_res = (res**2).sum()
print("Varianza de log(valor):")
print("  filas  R2=%.3f" % (ss_row/sst))
print("  columnas R2=%.3f" % (ss_col/sst))
print("  filas+columnas R2=%.3f (residuo %.3f)" % ((ss_row+ss_col)/sst, ss_res/sst))
print("  => el perfil de columnas explica %.1f%% de la varianza; la fila (tamaño del registro) %.1f%%"
      % (100*ss_col/sst, 100*ss_row/sst))

# --- 2. estabilidad bootstrap de la firma --------------------------------
B = 10000
orders = []; top2 = 0; bot2 = 0; rho_split = []
p_obs = X.sum(0)/X.sum()
for b in range(B):
    idx = rng.integers(0, n, n)
    s = X[idx].sum(0); p = s/s.sum()
    orders.append(tuple(np.argsort(-p)))
    t2 = set(np.argsort(-p)[:2]) == {0, 1}
    b2 = set(np.argsort(p)[:2]) == {7, 8}
    top2 += t2; bot2 += b2
# split-half
rh = []
for b in range(5000):
    idx = rng.permutation(n); a, bb = idx[:n//2], idx[n//2:]
    p1 = X[a].sum(0); p2 = X[bb].sum(0)
    rh.append(stats.spearmanr(p1, p2)[0])
print("\nBootstrap de filas (B=%d):" % B)
print("  P(máximas c1 y c2) = %.3f" % (top2/B))
print("  P(mínimas c8 y c9) = %.3f" % (bot2/B))
print("  orden completo observado se repite en %.3f de las réplicas" % (np.mean([o == tuple(np.argsort(-p_obs)) for o in orders])))
print("  split-half Spearman: mediana %.2f (IC90 %.2f-%.2f)"
      % (np.median(rh), *np.percentile(rh, [5, 95])))

# --- 3. influencia de cada fila en el orden ------------------------------
base = tuple(np.argsort(-p_obs))
cambios = 0
for i in range(n):
    s = X.sum(0) - X[i]; p = s/s.sum()
    if tuple(np.argsort(-p)) != base: cambios += 1
print("\nLeave-one-row-out: el orden completo cambia al quitar %d/%d filas" % (cambios, n))

# --- 4. el perfil de columnas y el tamaño del registro -------------------
tot = X.sum(1)
rho_tam = stats.spearmanr(tot, X[:, 8]/X.sum(1))[0]  # c9 vs total
print("Correlación total de fila vs cuota de c9: rho=%.2f" % rho_tam)
print("  (control: si las columnas fueran periodos, el tamaño del registro no debería fijar la cuota)")

# --- 4b. la cuota de cada columna y el tamano del registro ---------------
P = X/X.sum(1, keepdims=True)
filas_tam = []
for j in range(k):
    r, pv = stats.spearmanr(tot, P[:, j])
    filas_tam.append((cols[j], r, pv))
# Holm sobre las 9 correlaciones
F = pd.DataFrame(filas_tam, columns=["parte", "rho_tam", "p"])
F = F.sort_values("p").reset_index(drop=True)
adj = []; prev = 0
for i, pv in enumerate(F.p):
    a_ = min(1.0, (k-i)*pv); a_ = max(a_, prev); adj.append(a_); prev = a_
F["p_holm"] = adj
print("\nCuota de cada columna vs tamaño de la fila (Spearman, Holm sobre 9):")
print(F.to_string(index=False))
F.to_csv(AQUI/"columnas_vs_tamano.csv", index=False)

# --- 5. cuantas columnas se necesitan para describir el perfil -----------
# PCA sobre clr
clr = np.log(X) - np.log(X).mean(1, keepdims=True)
u, s, vt = np.linalg.svd(clr - clr.mean(0), full_matrices=False)
var = s**2/np.sum(s**2)
print("\nPCA del perfil (CLR): varianza explicada PC1=%.2f PC2=%.2f PC3=%.2f"
      % tuple(var[:3]))
print("  (si el perfil fuera un gradiente de 1 dimensión, PC1 sería alto)")

pd.DataFrame({"parte": cols, "cuota": p_obs}).to_csv(AQUI/"perfil_columnas.csv", index=False)
print("\nGuardado: perfil_columnas.csv")
