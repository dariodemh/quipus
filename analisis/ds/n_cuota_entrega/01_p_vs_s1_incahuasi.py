"""Paso 1: contraste P (colgante) vs S1 (primera subsidiaria) en los 28 quipus de Incahuasi.

Para cada celda (colgante con S1) se mide:
  - redondez: múltiplo de 10, 50, 100
  - igualdades exactas entre celdas del mismo grupo (pares)
  - CV dentro de grupo (grupos con >=3 celdas)
Nulo: intercambiar P y S1 dentro de cada celda (preserva el par y la distribución
conjunta; destruye solo la etiqueta de rol). 5000 réplicas por quipu, 20000 global.
Salida: p_vs_s1_incahuasi.csv, salida_01.txt
"""
import numpy as np
import pandas as pd
from scipy import stats

import lib_cuota as L

RNG = np.random.default_rng(L.SEED)
NPER_Q = 5000
NPER_G = 20000

c, q = L.cargar()
incs = L.incahuasi(q)
print(f"quipus Incahuasi: {len(incs)}")

filas = []
allc = []
for k in incs:
    m = L.celdas(c, k)
    allc.append(m[m.tiene_s1])
    obs, ps = L.test_quipu(m, nperm=NPER_Q, rng=RNG)
    obs.update(ps)
    obs["kfg"] = k
    obs["sistema"] = "Incahuasi"
    filas.append(obs)

res = pd.DataFrame(filas)
res = res[["kfg", "sistema", "n_celdas", "n_obs", "n_grupos", "medP", "medS1",
           "r10P", "r10S1", "dr10", "r50P", "r50S1", "dr50",
           "r100P", "r100S1", "dr100", "eqP", "eqS1", "pares", "deq",
           "cvP", "cvS1", "dcv", "p_r10", "p_r50", "p_r100", "p_eq", "p_cv"]]
res.to_csv("p_vs_s1_incahuasi.csv", index=False)

# ---------- pruebas globales ----------
C = pd.concat(allc, ignore_index=True)
C["gid"] = C.kfg + "|" + C.grupo.astype(str)
C = C[(C.presP) & (C.P > 0) & (C.presS1) & (C.S1 > 0)].copy()


lineas = []
P = C.P.to_numpy()
S1 = C.S1.to_numpy()
gidx = [g.index.to_numpy() for _, g in C.groupby("gid")]
pos = {ix: i for i, ix in enumerate(C.index)}
gidx = [np.array([pos[i] for i in ix]) for ix in gidx]
obs_met = L.metricas_mat(P[None, :], S1[None, :], gidx)
stats_def = {
    "redondez10": "dr10",
    "redondez50": "dr50",
    "redondez100": "dr100",
    "igualdades": "deq",
    "CV(plano)": "dcv",
}
nulls = {k: [] for k in stats_def}
NPER_G = 20000
LOTE = 2000
hechos = 0
while hechos < NPER_G:
    b = min(LOTE, NPER_G - hechos)
    Pp, Ss = L._swap_mat(P, S1, RNG, b)
    met = L.metricas_mat(Pp, Ss, gidx)
    for k, col in stats_def.items():
        nulls[k].append(met[col])
    hechos += b
for nom, col in stats_def.items():
    arr = np.concatenate(nulls[nom])
    o = float(obs_met[col][0])
    p = float((np.sum(arr >= o) + 1) / (NPER_G + 1))
    lineas.append(dict(prueba=nom, n_celdas=len(C), observado=o,
                       nulo_media=float(arr.mean()), nulo_sd=float(arr.std(ddof=1)),
                       p_perm=p))
glob = pd.DataFrame(lineas)
glob["p_holm"] = L.holm(glob.p_perm.values)

# ---------- nivel quipu ----------
qlineas = []
for nom, col in [("redondez10", "dr10"), ("redondez50", "dr50"),
                 ("redondez100", "dr100"), ("igualdades", "deq"),
                 ("CV(plano)", "dcv")]:
    x = res[col].dropna().values
    if len(x) < 3:
        continue
    npos = int(np.sum(x > 0))
    # sign test exacto (dos colas)
    sp = stats.binomtest(npos, len(x), 0.5).pvalue
    # Wilcoxon una cola (P más redondo/plano)
    try:
        wp = stats.wilcoxon(x, alternative="greater").pvalue
    except ValueError:
        wp = np.nan
    # sign-flip
    fl = np.array([np.mean(x * RNG.choice([-1, 1], size=len(x))) for _ in range(NPER_G)])
    fp = (np.sum(fl >= np.mean(x)) + 1) / (NPER_G + 1)
    qlineas.append(dict(prueba=nom, n_quipus=len(x), n_positivos=npos,
                        media=float(np.mean(x)), p_signos=sp, p_wilcoxon=wp,
                        p_signflip=fp))
qres = pd.DataFrame(qlineas)
qres["p_holm_signos"] = L.holm(qres.p_signos.values)
glob.to_csv("pruebas_globales.csv", index=False)
qres.to_csv("pruebas_quipu.csv", index=False)

# ---------- control de magnitud ----------
C["dec"] = C.P.map(L.decada)
C["decS"] = C.S1.map(L.decada)
S = C[C.dec == C.decS].copy()
mag = []
for nom, base in [("redondez10", 10), ("redondez50", 50), ("redondez100", 100)]:
    o = float(np.mean(S.P % base == 0) - np.mean(S.S1 % base == 0))
    rp = (S.P % base == 0).to_numpy()
    rs = (S.S1 % base == 0).to_numpy()
    b = int(np.sum(rp & ~rs))
    cc = int(np.sum(~rp & rs))
    p = stats.binomtest(b, b + cc, 0.5).pvalue if b + cc else np.nan
    mag.append(dict(prueba=nom, n_celdas_misma_decada=len(S), dif_obs=o,
                    disc_P=b, disc_S1=cc, p_mcnemar=p))
mag = pd.DataFrame(mag)
mag.to_csv("control_magnitud.csv", index=False)

# regresión logística con efecto fijo de quipu y log10(valor)
import statsmodels.api as sm
long = pd.concat([
    pd.DataFrame({"y": (C.P % 10 == 0).astype(int), "rol": 1, "logv": np.log10(C.P), "k": C.kfg, "gid": C.gid}),
    pd.DataFrame({"y": (C.S1 % 10 == 0).astype(int), "rol": 0, "logv": np.log10(C.S1), "k": C.kfg, "gid": C.gid}),
], ignore_index=True)
X = pd.get_dummies(long[["rol", "logv", "k"]], columns=["k"], drop_first=True, dtype=float)
X = sm.add_constant(X)
mod = sm.Logit(long.y, X).fit(disp=0, cov_type="cluster", cov_kwds={"groups": long.gid})
reg = pd.DataFrame({"coef": mod.params, "se": mod.bse, "p": mod.pvalues}).loc[["rol", "logv"]]

with open("salida_01.txt", "w", encoding="utf-8") as f:
    f.write("== métricas por quipu ==\n")
    f.write(res.round(3).to_string(index=False) + "\n\n")
    f.write("== pruebas globales (nulo intercambio P<->S1 en celda, 20000) ==\n")
    f.write(glob.round(5).to_string(index=False) + "\n\n")
    f.write("== nivel quipu (dirección: P más redondo/repetido/plano) ==\n")
    f.write(qres.round(5).to_string(index=False) + "\n\n")
    f.write("== control de magnitud: celdas con P y S1 en la misma década ==\n")
    f.write(mag.round(5).to_string(index=False) + "\n\n")
    f.write("== logit redondez10 ~ rol + log10(valor) + EF quipu, SE cluster por celda ==\n")
    f.write(reg.round(4).to_string() + "\n")

print(glob.round(5).to_string(index=False))
print(qres.round(4).to_string(index=False))
print(mag.round(4).to_string(index=False))
print(reg.round(4).to_string())
print("celdas observadas:", len(C), "quipus con >=1 celda:", C.kfg.nunique())
