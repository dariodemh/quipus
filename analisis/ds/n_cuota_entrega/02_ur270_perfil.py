"""Paso 2: ¿S1/P es un perfil de cumplimiento estable por columna en UR270?

UR270 tiene grupos de 9 colgantes (filas) x 9 posiciones (columnas). Si P=cuota y
S1=entrega, el cociente S1/P de cada columna debe ser estable entre filas.
Pruebas:
  - perfil de medias por columna (6 filas completas)
  - estadístico SS_col/SS_tot y nulo permutando cocientes dentro de cada fila
  - split-half (filas pares vs impares) y su nulo
  - RMSE de predicción leave-one-out por media de columna frente a nulo
Además: proporción de celdas con S1>P (entrega > cuota) en todo Incahuasi.
Salida: salida_02.txt, ur270_ratios.csv
"""
import numpy as np
import pandas as pd
from scipy import stats

import lib_cuota as L

RNG = np.random.default_rng(L.SEED)
NP = 20000

c, q = L.cargar()

# ---------- UR270 ----------
m = L.celdas(c, "UR270")
g9 = [g for g, x in m.groupby("grupo") if (x.j.max() == 9) and (len(x) == 9)]
print("grupos de 9 en UR270:", g9)
filas = []
for g in g9:
    x = m[m.grupo == g].sort_values("j")
    for _, r in x.iterrows():
        if r.presP and r.P > 0 and r.presS1 and r.S1 > 0:
            filas.append(dict(grupo=g, j=int(r.j), P=int(r.P), S1=int(r.S1),
                              ratio=r.S1 / r.P))
rat = pd.DataFrame(filas)
rat.to_csv("ur270_ratios.csv", index=False)

# matriz 6 filas completas x 9 columnas
completas = [g for g in g9 if len(rat[rat.grupo == g]) == 9]
M = rat[rat.grupo.isin(completas)].pivot(index="grupo", columns="j", values="ratio")
M = M.reindex(columns=range(1, 10))
print("filas completas:", completas, M.shape)


def ss_col(A):
    """Fracción de varianza explicada por columna (filas x columnas, sin NaN)."""
    A = np.asarray(A, float)
    gm = np.nanmean(A)
    ss_tot = np.nansum((A - gm) ** 2)
    if ss_tot == 0:
        return np.nan
    ss_col = np.nansum((np.nanmean(A, axis=0) - gm) ** 2) * A.shape[0]
    return ss_col / ss_tot


def rmse_loo(A):
    A = np.asarray(A, float)
    err = []
    for i in range(A.shape[0]):
        otros = np.delete(A, i, axis=0)
        pred = np.nanmean(otros, axis=0)
        ok = ~np.isnan(A[i])
        err.extend((A[i][ok] - pred[ok]) ** 2)
    return float(np.sqrt(np.mean(err)))


obs_ss = ss_col(M.values)
obs_rm = rmse_loo(M.values)
col_means = M.mean(axis=0)
col_cv = M.std(axis=0, ddof=1) / M.mean(axis=0)

# nulo: permutar cocientes dentro de cada fila (rompe la alineación por columna)
nss, nrm = [], []
A = M.values.copy()
for _ in range(NP):
    B = np.array([RNG.permutation(row) for row in A])
    nss.append(ss_col(B))
    nrm.append(rmse_loo(B))
nss = np.array(nss)
nrm = np.array(nrm)
p_ss = (np.sum(nss >= obs_ss) + 1) / (NP + 1)
p_rm = (np.sum(nrm <= obs_rm) + 1) / (NP + 1)

# split-half: correlación de medias por columna entre filas pares e impares
impar = M.iloc[::2].mean(axis=0)
par = M.iloc[1::2].mean(axis=0)
r_split = float(np.corrcoef(impar, par)[0, 1])
sp_split = float(pd.Series(impar).corr(pd.Series(par), method="spearman"))
nsplit = []
for _ in range(NP):
    B = np.array([RNG.permutation(row) for row in A])
    a = B[::2].mean(axis=0)
    b = B[1::2].mean(axis=0)
    nsplit.append(np.corrcoef(a, b)[0, 1])
nsplit = np.array(nsplit)
p_split = (np.sum(nsplit >= r_split) + 1) / (NP + 1)
p_split_sp = (np.sum(nsplit >= sp_split) + 1) / (NP + 1)

# ---------- S1 > P en todo Incahuasi ----------
C = []
for k in L.incahuasi(q):
    mm = L.celdas(c, k)
    mm = mm[(mm.presP) & (mm.P > 0) & (mm.presS1) & (mm.S1 > 0)]
    mm["kfg"] = k
    C.append(mm)
C = pd.concat(C)
mayor = C[C.S1 > C.P]
print(f"celdas S1>P: {len(mayor)}/{len(C)} = {len(mayor)/len(C):.3f}; "
      f"quipus con alguna: {mayor.kfg.nunique()}/{C.kfg.nunique()}")
ratio_all = C.S1 / C.P
print("ratio global cuantiles:", np.round(np.quantile(ratio_all, [0, .1, .25, .5, .75, .9, 1]), 2))

# Friedman: ¿los rangos de las 9 columnas son consistentes entre las 6 filas?
fr = stats.friedmanchisquare(*[M.values[i] for i in range(M.shape[0])])
rank_med = pd.DataFrame(M.values).rank(axis=1).mean(axis=0)

# robustez: quitar la columna 8 (la de ratio más alto) y recalcular
cols_sin8 = [j for j in M.columns if j != 8]
Ms = M[cols_sin8]
ss_sin8 = ss_col(Ms.values)
r_split_sin8 = float(np.corrcoef(Ms.iloc[::2].mean(axis=0), Ms.iloc[1::2].mean(axis=0))[0, 1])

with open("salida_02.txt", "w", encoding="utf-8") as f:
    f.write(f"UR270 grupos de 9: {g9}\nfilas completas: {completas}\n\n")
    f.write("matriz S1/P (filas=grupo, columnas=j)\n")
    f.write(M.round(3).to_string() + "\n\n")
    f.write("media por columna:\n" + col_means.round(3).to_string() + "\n\n")
    f.write("CV entre filas por columna:\n" + col_cv.round(3).to_string() + "\n\n")
    f.write(f"SS_col/SS_tot = {obs_ss:.3f}; nulo media {nss.mean():.3f}, sd {nss.std():.3f}, p={p_ss:.5f}\n")
    f.write(f"RMSE LOO por columna = {obs_rm:.3f}; nulo media {nrm.mean():.3f}, sd {nrm.std():.3f}, p={p_rm:.5f}\n")
    f.write(f"split-half r = {r_split:.3f} (p={p_split:.5f}); rho = {sp_split:.3f} (p={p_split_sp:.5f})\n\n")
    f.write(f"Friedman (rangos por fila): chi2={fr.statistic:.3f}, p={fr.pvalue:.5f}\n")
    f.write("rango medio por columna (1=bajo, 9=alto):\n" + rank_med.round(2).to_string() + "\n")
    f.write(f"sin columna 8: SS_col={ss_sin8:.3f}; split-half r={r_split_sin8:.3f}\n\n")
    f.write(f"celdas con S1>P en Incahuasi: {len(mayor)}/{len(C)} = {len(mayor)/len(C):.3f}\n")
    f.write(f"quipus con S1>P: {mayor.kfg.nunique()}/{C.kfg.nunique()}\n")
    f.write("ratio S1/P cuantiles 0/10/25/50/75/90/100: " +
            str(np.round(np.quantile(ratio_all, [0, .1, .25, .5, .75, .9, 1]), 3)) + "\n")
    f.write("\npor quipu:\n")
    tab = C.assign(mayor=(C.S1 > C.P), ratio=C.S1 / C.P).groupby("kfg").agg(
        n=("P", "size"), mayor=("mayor", "sum"), med_ratio=("ratio", "median"))
    f.write(tab.round(3).to_string())

print("\nmedia por columna:\n", col_means.round(3).to_string())
print("SS_col", round(obs_ss, 3), "p", round(p_ss, 5), "| RMSE", round(obs_rm, 3), "p", round(p_rm, 5))
print("split-half r", round(r_split, 3), "p", round(p_split, 5), "| rho", round(sp_split, 3), "p", round(p_split_sp, 5))
print("ratios mediana", round(float(ratio_all.median()), 3),
      "IQR", np.round(np.quantile(ratio_all, [.25, .75]), 3))
