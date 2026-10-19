# -*- coding: utf-8 -*-
"""UR278: filas planas (posible 'tasa') frente a filas de entrega.
- mide planitud por fila (CV, rango, igualdades exactas)
- nulos: (a) barajar todas las celdas, (b) barajar cada columna por separado,
  (c) muestrear valores del mismo quipu con magnitud parecida a la media de la fila
- prueba de mezcla (1 vs 2 componentes gaussianos sobre log CV)
- prueba dirigida del emparejamiento 2+1+2+2+2 que predice la Visita
  (Mongoy 2, Cancay 1, Chuquitanga 2, Chumbillan 2, Antachumbi 2)
Salidas: ur278_filas.csv, ur278_pruebas.csv, ur278_pares.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr, spearmanr
from sklearn.mixture import GaussianMixture

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SEED = 20261018
NPERM = 20000
rng = np.random.default_rng(SEED)

d = pd.read_csv(RAIZ / "analisis/13_sistema_incahuasi/ur278_tabla.csv")
C = [f"c{i}" for i in range(1, 10)]
D = d[d.n == 9].dropna(subset=C).reset_index(drop=True)
X = D[C].astype(float).values
n = len(X)
print(f"UR278: {len(d)} filas con >=7 colgantes; {n} filas de exactamente 9 cuerdas")


def met(v):
    m = v.mean()
    cv = v.std() / m
    return dict(media=m, cv=cv, rango=v.max() - v.min(), distintos=len(set(v)),
                eq_all=int(len(set(v)) == 1), range1=int(v.max() - v.min() <= 1),
                cv05=int(cv <= 0.05), cv10=int(cv <= 0.10), cv15=int(cv <= 0.15),
                ties=sum(v[i] == v[j] for i in range(9) for j in range(i + 1, 9)))


F = pd.DataFrame([dict(grupo=int(D.grupo[i]), **met(X[i])) for i in range(n)])
F["fase"] = np.where(F.grupo < 15, 1, 2)
F["total"] = X.sum(1)
F.to_csv(AQUI / "ur278_filas.csv", index=False)
print("\nFilas ordenadas por CV:")
print(F.sort_values("cv")[["grupo", "fase", "total", "media", "cv", "rango", "distintos", "ties"]].to_string(index=False))

print("\nResumen observado:")
for col in ["eq_all", "range1", "cv05", "cv10", "cv15", "ties"]:
    print(f"  {col}: {int(F[col].sum())}")
print(f"  CV medio: {F.cv.mean():.3f}")

# ---------------- Nulos ----------------
flat = X.ravel()


def stats(M):
    cvs = M.std(1) / M.mean(1)
    return dict(cv_mean=cvs.mean(), eq_all=sum(len(set(r)) == 1 for r in M),
                range1=sum(r.max() - r.min() <= 1 for r in M),
                cv05=sum(c <= .05 for c in cvs), cv10=sum(c <= .10 for c in cvs),
                cv15=sum(c <= .15 for c in cvs),
                ties=sum(sum(r[i] == r[j] for i in range(9) for j in range(i + 1, 9)) for r in M))


N1 = {k: np.empty(NPERM) for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties"]}
N2 = {k: np.empty(NPERM) for k in N1}
for b in range(NPERM):
    s = stats(rng.permutation(flat).reshape(n, 9))
    for k in N1:
        N1[k][b] = s[k]
    M = np.column_stack([rng.permutation(X[:, j]) for j in range(9)])
    s = stats(M)
    for k in N2:
        N2[k][b] = s[k]

res = []
obs = stats(X)
for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties"]:
    cola = "baja" if k == "cv_mean" else "alta"
    p1 = (1 + np.sum(N1[k] <= obs[k] if cola == "baja" else N1[k] >= obs[k])) / (NPERM + 1)
    p2 = (1 + np.sum(N2[k] <= obs[k] if cola == "baja" else N2[k] >= obs[k])) / (NPERM + 1)
    res.append(dict(prueba=k, observado=obs[k], nulo_filas_barajadas=N1[k].mean(), p_filas=p1,
                    nulo_columnas=N2[k].mean(), p_columnas=p2))
R = pd.DataFrame(res)
print("\nNulos de matriz completa:")
print(R.to_string(index=False))

# ---------------- Nulo parametrico: perfil de columnas + ruido por columna ----------------
# x_ij = T_i * p_j * exp(z_ij), con p_j el perfil observado y z_ij ~ N(0, sigma_j)
# Conserva total de fila, perfil de columnas y dispersion de cada columna;
# rompe la covariacion entre columnas. Es el nulo correcto para "fila plana".
T = X.sum(1)
p = (X / T[:, None]).mean(0)
p = p / p.sum()
resid = np.log(X) - np.log(T)[:, None] - np.log(p)[None, :]
sig = resid.std(0)
print("\nPerfil de columnas p_j:", np.round(p, 4))
print("SD de log-residuo por columna:", np.round(sig, 3))


def stat_perfil(M):
    """Distancia de cada fila al perfil de columnas (SD del log-residuo)."""
    return np.std(np.log(M) - np.log(M.sum(1))[:, None] - np.log(p)[None, :], axis=1)


obs_perfil = stat_perfil(X)
NP = {k: np.empty(NPERM) for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties", "perfil_mean"]}
p_row = np.zeros(n)
p_row_cv = np.zeros(n)
for b in range(NPERM):
    Z = rng.normal(0, 1, size=(n, 9)) * sig[None, :]
    M = np.rint(T[:, None] * p[None, :] * np.exp(Z - 0.5 * sig[None, :] ** 2))
    M = np.maximum(M, 1)
    cvs = M.std(1) / M.mean(1)
    NP["cv_mean"][b] = cvs.mean()
    NP["eq_all"][b] = sum(len(set(r)) == 1 for r in M)
    NP["range1"][b] = sum(r.max() - r.min() <= 1 for r in M)
    NP["cv05"][b] = sum(cvs <= .05)
    NP["cv10"][b] = sum(cvs <= .10)
    NP["cv15"][b] = sum(cvs <= .15)
    NP["ties"][b] = sum(sum(r[i] == r[j] for i in range(9) for j in range(i + 1, 9)) for r in M)
    NP["perfil_mean"][b] = stat_perfil(M).mean()
    p_row += (stat_perfil(M) <= obs_perfil)
    p_row_cv += (cvs <= F.cv.values)

res2 = []
for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties", "perfil_mean"]:
    cola = "baja" if k in ("cv_mean", "perfil_mean") else "alta"
    o = obs_perfil.mean() if k == "perfil_mean" else obs[k]
    pv = (1 + np.sum(NP[k] <= o if cola == "baja" else NP[k] >= o)) / (NPERM + 1)
    res2.append(dict(prueba=k, observado=o, nulo_parametrico=NP[k].mean(), p=pv))
R2 = pd.DataFrame(res2)
print("\nNulo parametrico (perfil de columnas + ruido):")
print(R2.to_string(index=False))

# p por fila contra el nulo parametrico, y Holm
p_row = (1 + p_row) / (NPERM + 1)
p_row_cv = (1 + p_row_cv) / (NPERM + 1)
F["p_perfil"] = p_row
F["p_cv"] = p_row_cv
F["dist_perfil"] = obs_perfil
orden = np.argsort(p_row)
m = n
adj = np.empty(m)
prev = 0
for rank, j in enumerate(orden):
    prev = max(prev, min(1, (m - rank) * p_row[j]))
    adj[j] = prev
F["p_holm_perfil"] = adj
orden = np.argsort(p_row_cv)
adj = np.empty(m)
prev = 0
for rank, j in enumerate(orden):
    prev = max(prev, min(1, (m - rank) * p_row_cv[j]))
    adj[j] = prev
F["p_holm_cv"] = adj
print("\nFilas mas planas (CV) frente al nulo parametrico:")
print(F.sort_values("p_cv")[["grupo", "fase", "total", "cv", "dist_perfil", "p_cv", "p_holm_cv"]].head(8).to_string(index=False))
print("\nFilas mas cercanas al perfil (proporcionales) frente al nulo parametrico:")
print(F.sort_values("p_perfil")[["grupo", "fase", "total", "cv", "dist_perfil", "p_perfil", "p_holm_perfil"]].head(8).to_string(index=False))

# ---------------- Fase y tamano ----------------
print("\nFase 1 vs fase 2:")
print(F.groupby("fase")[["total", "cv", "ties"]].agg(["mean", "median", "count"]).round(3).to_string())
print("correlacion CV vs log(total): Pearson %.3f (p=%.4f), Spearman %.3f (p=%.4f)" %
      (*pearsonr(F.cv, np.log(F.total)), *spearmanr(F.cv, F.total)))
b = np.polyfit(np.log(F.total), F.cv, 1)
F["resid_cv"] = F.cv - np.polyval(b, np.log(F.total))
print("residuo CV (tras quitar log total) por fase:", F.groupby("fase").resid_cv.mean().round(3).to_dict())
# permutacion de etiquetas de fase sobre el residuo
dif = F[F.fase == 1].resid_cv.mean() - F[F.fase == 2].resid_cv.mean()
perm = np.array([rng.permutation(F.fase.values) for _ in range(NPERM)])
dperm = np.array([F.resid_cv.values[p == 1].mean() - F.resid_cv.values[p == 2].mean() for p in perm])
print("diferencia de residuo fase1-fase2 = %.3f; p (permutacion de fase) = %.4f" % (dif, (1 + np.sum(dperm >= dif)) / (NPERM + 1)))
# concentracion de filas planas en fase 1
from math import comb
for thr, col in [(.15, "cv15"), (.10, "cv10")]:
    k = int(F[col].sum())
    n1 = int((F.fase == 1).sum())
    p = comb(n1, k) / comb(n, k)
    print(f"  {k} filas con CV<={thr}, todas en fase 1: p exacta = {p:.4f}")

# ---------------- Mezcla 1 vs 2 componentes ----------------
print("\nMezcla gaussiana sobre log(CV):")
Y = np.log(F.cv.values).reshape(-1, 1)
for k in [1, 2, 3]:
    gm = GaussianMixture(k, n_init=20, random_state=SEED).fit(Y)
    print(f"  k={k}: BIC={gm.bic(Y):.2f} AIC={gm.aic(Y):.2f} pesos={np.round(gm.weights_,3)} medias={np.round(gm.means_.ravel(),3)}")
gm = GaussianMixture(2, n_init=20, random_state=SEED).fit(Y)
lab = gm.predict(Y)
F["comp"] = lab
print("  componente 2 (el de CV bajo): filas", F[lab == np.argmin(gm.means_.ravel())].grupo.tolist())

# ---------------- Emparejamiento dirigido 2+1+2+2+2 ----------------
L = np.log(X)
Z = L - L.mean(1, keepdims=True)
R = np.corrcoef(Z.T)


def matchings(items):
    if not items:
        yield []
    else:
        a = items[0]
        for k in range(1, len(items)):
            b = items[k]
            for mm in matchings(items[1:k] + items[k + 1:]):
                yield [(a, b)] + mm


ALL = []
for sing in range(9):
    for mm in matchings([i for i in range(9) if i != sing]):
        ALL.append((sing, mm))


def rintra(mm):
    return np.mean([R[i, j] for i, j in mm])


def ties(M, mm):
    return sum(int(np.sum(M[:, i] == M[:, j])) for i, j in mm)


vals_r = np.array([rintra(m) for s, m in ALL])
vals_t = np.array([ties(X, m) for s, m in ALL])

# orden de la Visita: Mongoy 2 (c1-c2), Cancay 1 (c3), Chuquitanga 2 (c4-c5),
# Chumbillan 2 (c6-c7), Antachumbi 2 (c8-c9)
target = [(0, 1), (3, 4), (5, 6), (7, 8)]
r_t = rintra(target)
t_t = ties(X, target)
print("\nEmparejamiento dirigido de la Visita 2+1+2+2+2: (1-2)(4-5)(6-7)(8-9)+c3")
print("  r intra-par (log-razon, sin efecto de fila) = %.3f; rank %d/945; p = %.4f" %
      (r_t, 1 + np.sum(vals_r > r_t), (1 + np.sum(vals_r > r_t)) / len(vals_r)))
print("  igualdades exactas = %d; rank %d/945; p = %.4f (media 945 = %.1f, max = %d)" %
      (t_t, 1 + np.sum(vals_t > t_t), (1 + np.sum(vals_t > t_t)) / len(vals_t), vals_t.mean(), vals_t.max()))
print("  mejor emparejamiento por r:", ALL[vals_r.argmax()], "r=%.3f" % vals_r.max())
print("  mejor emparejamiento por igualdades:", ALL[vals_t.argmax()], "ties=%d" % vals_t.max())

# nulo dentro de fila para las igualdades del emparejamiento dirigido
cnt = np.empty(NPERM)
mx = np.empty(2000)
for b in range(NPERM):
    P = np.array([rng.permutation(r) for r in X])
    cnt[b] = ties(P, target)
    if b < 2000:
        mx[b] = max(ties(P, m) for s, m in ALL)
print("  nulo dentro de fila, emparejamiento dirigido: media %.2f; p = %.4f" %
      (cnt.mean(), (1 + np.sum(cnt >= t_t)) / (NPERM + 1)))
print("  nulo dentro de fila, maximo sobre 945 emparejamientos (2000 reps): media %.1f; p = %.4f" %
      (mx.mean(), (1 + np.sum(mx >= t_t)) / 2001))

# rotaciones del patron contiguo 2+1+2+2+2
print("\nRotaciones del patron contiguo 2+1+2+2+2 (inicio en cada columna):")
for start in range(9):
    idx = [(start + k) % 9 for k in range(9)]
    mm = [(idx[0], idx[1]), (idx[3], idx[4]), (idx[5], idx[6]), (idx[7], idx[8])]
    rr = rintra(mm)
    print("  inicio c%d: r=%.3f rank=%d ties=%d" % (start + 1, rr, 1 + np.sum(vals_r > rr), ties(X, mm)))

# sin las filas mas planas
sin = F.cv > .15
Xs = X[sin.values]
vals_ts = np.array([ties(Xs, m) for s, m in ALL])
ts = ties(Xs, target)
print("\nSin las %d filas con CV<=0.15: igualdades dirigidas = %d; rank %d/945; p = %.4f (max %d)" %
      ((~sin).sum(), ts, 1 + np.sum(vals_ts > ts), (1 + np.sum(vals_ts > ts)) / len(vals_ts), vals_ts.max()))

# matriz de igualdades
T = np.zeros((9, 9), int)
for i in range(9):
    for j in range(i + 1, 9):
        T[i, j] = T[j, i] = int(np.sum(X[:, i] == X[:, j]))
print("\nMatriz de igualdades exactas entre columnas (36 pares):")
print(pd.DataFrame(T, index=[f"c{i+1}" for i in range(9)], columns=[f"c{i+1}" for i in range(9)]).to_string())

Rd = pd.DataFrame(res)
Rd.to_csv(AQUI / "ur278_pruebas.csv", index=False)
R2.to_csv(AQUI / "ur278_pruebas_parametrico.csv", index=False)
F.to_csv(AQUI / "ur278_filas.csv", index=False)

# ---------------- Robustez: 26 filas (incluye grupos 18 y 32 recortados a 9) ----------------
D26 = d.dropna(subset=C).reset_index(drop=True)
X26 = D26[C].astype(float).values
cv26 = X26.std(1) / X26.mean(1)
print("\nRobustez con 26 filas (grupos 18 y 32 recortados a c1-c9):")
print("  filas CV<=.15: %d; CV<=.10: %d; ties totales: %d" %
      (sum(cv26 <= .15), sum(cv26 <= .10),
       sum(sum(X26[r, i] == X26[r, j] for i in range(9) for j in range(i + 1, 9)) for r in range(len(X26)))))
L26 = np.log(X26)
Z26 = L26 - L26.mean(1, keepdims=True)
R26 = np.corrcoef(Z26.T)
t26 = ties(X26, target)
r26 = np.mean([R26[i, j] for i, j in target])
print("  emparejamiento dirigido: r = %.3f; igualdades = %d" % (r26, t26))
