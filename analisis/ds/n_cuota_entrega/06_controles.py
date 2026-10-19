"""Controles adicionales:
(a) efecto agregado dejando fuera UR270 (¿todo el efecto es un quipu?)
(b) celdas con el MISMO color limpio en P y S1 (¿es efecto del color/rol?)
(c) tamaño: proporción de celdas con P>S1 y mediana de S1/P
(d) estabilidad por columna de P y de S1 en UR270 (¿P fijo = cuota?)
(e) Holm sobre todas las pruebas por quipu de p_vs_s1.csv
Salida: salida_06.txt
"""
import numpy as np
import pandas as pd
from scipy import stats

import lib_cuota as L

RNG = np.random.default_rng(L.SEED)
NP = 20000

c, q = L.cargar()
incs = L.incahuasi(q)

# ---------- (a) leave-one-quipu-out ----------
celdas = []
for k in incs:
    m = L.celdas(c, k)
    m = m[(m.presP) & (m.P > 0) & (m.presS1) & (m.S1 > 0)].copy()
    m["kfg"] = k
    celdas.append(m)
C = pd.concat(celdas, ignore_index=True)
print("P>S1:", int((C.P > C.S1).sum()), "/", len(C), "=", round(float((C.P > C.S1).mean()), 3))
print("S1/P mediana:", round(float((C.S1 / C.P).median()), 3))


def efecto(D, nperm=NP):
    D = D.reset_index(drop=True)
    P = D.P.to_numpy()
    S1 = D.S1.to_numpy()
    grupos = [g.index.to_numpy() for _, g in D.groupby(["kfg", "grupo"])]
    pos = {ix: i for i, ix in enumerate(D.index)}
    gidx = [np.array([pos[i] for i in ix]) for ix in grupos]
    o = float(L.metricas_mat(P[None, :], S1[None, :], gidx)["dr10"][0])
    arr = []
    hechos = 0
    while hechos < nperm:
        b = min(2000, nperm - hechos)
        Pp, Ss = L._swap_mat(P, S1, RNG, b)
        arr.append(L.metricas_mat(Pp, Ss, gidx)["dr10"])
        hechos += b
    arr = np.concatenate(arr)
    return o, float((np.sum(arr >= o) + 1) / (nperm + 1)), float(arr.mean())


loo = []
for k in ["(todos)"] + incs:
    D = C if k == "(todos)" else C[C.kfg != k]
    if len(D) < 20:
        continue
    o, p, mn = efecto(D)
    loo.append(dict(excluido=k, n=len(D), dr10=o, nulo=mn, p=p))
LOO = pd.DataFrame(loo)

# ---------- (b) mismo color ----------
same = []
for k in incs:
    m = L.celdas(c, k)
    m = m[(m.presP) & (m.P > 0) & (m.presS1) & (m.S1 > 0)]
    # color de la subsidiaria
    s1 = c[(c.kfg == k) & (c.nivel == 1) & c.cuerda.str.endswith("s1")][["padre", "color_limpio"]]
    s1.columns = ["cuerda", "colS1"]
    m = m.merge(s1, on="cuerda", how="left")
    same.append(m[m.color_limpio == m.colS1])
SC = pd.concat(same) if same else pd.DataFrame()
if len(SC) >= 10:
    b = int(np.sum((SC.P % 10 == 0) & ~(SC.S1 % 10 == 0)))
    cc = int(np.sum(~(SC.P % 10 == 0) & (SC.S1 % 10 == 0)))
    p_sc = stats.binomtest(b, b + cc, 0.5).pvalue if b + cc else np.nan
    sc_txt = (f"celdas mismo color: {len(SC)}; disc P {b} vs S1 {cc}; "
              f"p McNemar {p_sc:.4f}; P>S1 en {np.mean(SC.P>SC.S1):.2f}")
else:
    sc_txt = f"celdas mismo color: {len(SC)} (insuficientes para probar)"

# ---------- (d) estabilidad por columna de P y S1 en UR270 ----------
m = L.celdas(c, "UR270")
g9 = [g for g, x in m.groupby("grupo") if len(x) == 9 and x.j.max() == 9]
filas = []
for g in g9:
    x = m[m.grupo == g].sort_values("j")
    for _, r in x.iterrows():
        if r.presP and r.P > 0 and r.presS1 and r.S1 > 0:
            filas.append((g, int(r.j), r.P, r.S1))
rat = pd.DataFrame(filas, columns=["grupo", "j", "P", "S1"])
comp = [g for g in g9 if len(rat[rat.grupo == g]) == 9]
MP = rat[rat.grupo.isin(comp)].pivot(index="grupo", columns="j", values="P")
MS = rat[rat.grupo.isin(comp)].pivot(index="grupo", columns="j", values="S1")


def ss_col(A):
    A = np.asarray(A, float)
    gm = np.nanmean(A)
    st = np.nansum((A - gm) ** 2)
    return np.nansum((np.nanmean(A, axis=0) - gm) ** 2) * A.shape[0] / st if st else np.nan


ssP, ssS = ss_col(MP.values), ss_col(MS.values)
cvP_col = (MP.std(axis=0, ddof=1) / MP.mean(axis=0)).mean()
cvS_col = (MS.std(axis=0, ddof=1) / MS.mean(axis=0)).mean()
# nulo: permutar dentro de fila
nP, nS = [], []
for _ in range(NP):
    nP.append(ss_col(np.array([RNG.permutation(r) for r in MP.values])))
    nS.append(ss_col(np.array([RNG.permutation(r) for r in MS.values])))
pP = (np.sum(np.array(nP) >= ssP) + 1) / (NP + 1)
pS = (np.sum(np.array(nS) >= ssS) + 1) / (NP + 1)

# ---------- (e) Holm sobre todas las pruebas por quipu ----------
res = pd.read_csv("p_vs_s1.csv")
pcols = ["p_r10", "p_r50", "p_r100", "p_eq", "p_cv"]
flat = res[pcols].to_numpy().ravel()
adj = L.holm(flat)
from scipy.stats import false_discovery_control
bh = false_discovery_control(np.where(np.isnan(flat), 1.0, flat))
for i, col in enumerate(pcols):
    res[col + "_holm"] = adj.reshape(res[pcols].shape)[:, i]
    res[col + "_bh"] = bh.reshape(res[pcols].shape)[:, i]
res.to_csv("p_vs_s1.csv", index=False)

with open("salida_06.txt", "w", encoding="utf-8") as f:
    f.write(f"P>S1: {int((C.P>C.S1).sum())}/{len(C)} = {(C.P>C.S1).mean():.3f}\n")
    f.write(f"S1/P mediana {float((C.S1/C.P).median()):.3f}\n\n")
    f.write("== (a) leave-one-quipu-out, redondez10 ==\n")
    f.write(LOO.round(5).to_string(index=False) + "\n\n")
    f.write("== (b) mismo color ==\n" + sc_txt + "\n\n")
    f.write("== (d) UR270: estabilidad por columna ==\n")
    f.write(f"SS_col P={ssP:.3f} (p={pP:.5f}); SS_col S1={ssS:.3f} (p={pS:.5f})\n")
    f.write(f"CV entre filas por columna: P={cvP_col:.3f}; S1={cvS_col:.3f}\n")
    f.write("MP:\n" + MP.round(1).to_string() + "\nMS:\n" + MS.round(1).to_string() + "\n\n")
    f.write("== (e) Holm/BH añadidos a p_vs_s1.csv ==\n")

print(LOO.round(4).to_string(index=False))
print(sc_txt)
print(f"SS_col P={ssP:.3f} p={pP:.5f}; S1={ssS:.3f} p={pS:.5f}")
print(f"CV col P={cvP_col:.3f} S1={cvS_col:.3f}")
