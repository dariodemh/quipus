"""Paso 4: control externo. Mismo contraste P vs S1 en 20 quipus de otros sitios.

Selección: quipus no Incahuasi (ni JC, que el metadato también marca Incahuasi) con
>=10 celdas P/S1 observadas; muestra aleatoria de 20, semilla 20261018.
Se repiten las métricas y el nulo de intercambio P<->S1; se compara Incahuasi vs control
a nivel de quipu (Mann-Whitney y permutación de etiquetas).
Salida: p_vs_s1.csv (Incahuasi + control), salida_04.txt
"""
import numpy as np
import pandas as pd
from scipy import stats

import lib_cuota as L

RNG = np.random.default_rng(L.SEED)
NP = 20000
NP_Q = 5000

c, q = L.cargar()
incs = set(L.incahuasi(q))

# celdas de todos los quipus
todas = []
for k in q.kfg:
    m = L.celdas(c, k)
    m = m[m.tiene_s1]
    m = m[(m.presP) & (m.P > 0) & (m.presS1) & (m.S1 > 0)]
    if len(m):
        m = m.copy()
        m["kfg"] = k
        todas.append(m)
T = pd.concat(todas, ignore_index=True)
print("quipus con celdas:", T.kfg.nunique(), "celdas:", len(T))

qidx = q.set_index("kfg")
T["proc"] = T.kfg.map(qidx.procedencia)
elig = (T.groupby("kfg").size() >= 10)
elig = [k for k in elig[elig].index if k not in incs
        and not k.startswith("JC") and qidx.loc[k, "procedencia"] != "Incahuasi"]
print("elegibles no Incahuasi con >=10 celdas:", len(elig))
control = sorted(RNG.choice(elig, size=min(20, len(elig)), replace=False).tolist())
print("control:", [(k, qidx.loc[k, "procedencia"]) for k in control])

filas = []
for k in sorted(incs) + control:
    m = L.celdas(c, k)
    obs, ps = L.test_quipu(m, nperm=NP_Q, rng=RNG)
    obs.update(ps)
    obs["kfg"] = k
    obs["sistema"] = "Incahuasi" if k in incs else "Control"
    obs["procedencia"] = qidx.loc[k, "procedencia"]
    filas.append(obs)
res = pd.DataFrame(filas)
cols = ["kfg", "sistema", "procedencia", "n_celdas", "n_obs", "n_grupos", "medP", "medS1",
        "r10P", "r10S1", "dr10", "r50P", "r50S1", "dr50", "r100P", "r100S1", "dr100",
        "eqP", "eqS1", "pares", "deq", "cvP", "cvS1", "dcv",
        "p_r10", "p_r50", "p_r100", "p_eq", "p_cv"]
res = res[cols]
res.to_csv("p_vs_s1.csv", index=False)

# ---------- agregados Incahuasi vs control ----------
def agregado(ks, nombre, nperm=NP):
    C = T[T.kfg.isin(ks)].reset_index(drop=True)
    P = C.P.to_numpy()
    S1 = C.S1.to_numpy()
    grupos = [g.index.to_numpy() for _, g in C.groupby(["kfg", "grupo"])]
    pos = {ix: i for i, ix in enumerate(C.index)}
    gidx = [np.array([pos[i] for i in ix]) for ix in grupos]
    o = L.metricas_mat(P[None, :], S1[None, :], gidx)
    out = {}
    for nom, col in [("redondez10", "dr10"), ("redondez50", "dr50"),
                     ("redondez100", "dr100"), ("igualdades", "deq"), ("CV(plano)", "dcv")]:
        arr = []
        hechos = 0
        while hechos < nperm:
            b = min(2000, nperm - hechos)
            Pp, Ss = L._swap_mat(P, S1, RNG, b)
            arr.append(L.metricas_mat(Pp, Ss, gidx)[col])
            hechos += b
        arr = np.concatenate(arr)
        out[nom] = (float(o[col][0]), float((np.sum(arr >= o[col][0]) + 1) / (nperm + 1)),
                    float(arr.mean()))
    return dict(nombre=nombre, n_quipus=len(ks), n_celdas=len(C), **{
        f"{k}_obs": v[0] for k, v in out.items()}, **{
        f"{k}_p": v[1] for k, v in out.items()}, **{
        f"{k}_nulo": v[2] for k, v in out.items()})


AGG = pd.DataFrame([agregado(sorted(incs), "Incahuasi UR255-UR279"),
                    agregado(control, "Control 20 quipus"),
                    agregado([k for k in q.kfg if k.startswith("JC")], "JC (Sector B)")])

# ---------- Incahuasi vs control a nivel quipu ----------
cmp = []
for col, nom in [("dr10", "redondez10"), ("deq", "igualdades"), ("dcv", "CV(plano)")]:
    a = res.loc[res.sistema == "Incahuasi", col].dropna().values
    b = res.loc[res.sistema == "Control", col].dropna().values
    if len(a) > 2 and len(b) > 2:
        u = stats.mannwhitneyu(a, b, alternative="two-sided")
        # permutación de etiquetas sobre la media
        obs = np.mean(a) - np.mean(b)
        pool = np.concatenate([a, b])
        na = len(a)
        nd = np.array([(lambda z: np.mean(z[:na]) - np.mean(z[na:]))(RNG.permutation(pool))
                       for _ in range(NP)])
        p = (np.sum(np.abs(nd) >= abs(obs)) + 1) / (NP + 1)
        cmp.append(dict(prueba=nom, media_inc=float(np.mean(a)), media_control=float(np.mean(b)),
                        dif=float(obs), p_mannwhitney=float(u.pvalue), p_perm=p,
                        n_inc=len(a), n_control=len(b)))
CMP = pd.DataFrame(cmp)

with open("salida_04.txt", "w", encoding="utf-8") as f:
    f.write(f"quipus con celdas: {T.kfg.nunique()}, celdas: {len(T)}\n")
    f.write(f"elegibles no Incahuasi con >=10 celdas: {len(elig)}\n")
    f.write("control: " + str([(k, qidx.loc[k, "procedencia"]) for k in control]) + "\n\n")
    f.write("== por quipu ==\n")
    f.write(res.round(3).to_string(index=False) + "\n\n")
    f.write("== agregados ==\n")
    f.write(AGG.round(5).to_string(index=False) + "\n\n")
    f.write("== Incahuasi vs control (nivel quipu) ==\n")
    f.write(CMP.round(5).to_string(index=False) + "\n")

print(AGG.round(5).to_string(index=False))
print(CMP.round(5).to_string(index=False))
