# -*- coding: utf-8 -*-
"""UR270: mismos diagnosticos de planitud que UR278, sobre los 6 grupos de 9
que tienen P (colgante) + S1 (primera subsidiaria) completos.

UR270 es la fuente de 6 filas de UR278; sirve como control de que las filas
planas de UR278 no son un artefacto de la suma P+S1.
Salida: ur270_filas.csv, ur270_pruebas.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SEED = 20261018
NPERM = 20000
rng = np.random.default_rng(SEED)

P = pd.read_csv(RAIZ / "analisis/ds/n_nueve_unidades/ur270_parts.csv")
C = [f"c{i}" for i in range(1, 10)]
parts = {
    "P+S1": P[[f"B{c}" for c in C]].values + P[[f"A{c}" for c in C]].values,
    "P": P[[f"B{c}" for c in C]].values,
    "S1": P[[f"A{c}" for c in C]].values,
}


def met(v):
    m = v.mean()
    cv = v.std() / m
    return dict(media=m, cv=cv, rango=v.max() - v.min(), distintos=len(set(v)),
                eq_all=int(len(set(v)) == 1), range1=int(v.max() - v.min() <= 1),
                cv05=int(cv <= .05), cv10=int(cv <= .10), cv15=int(cv <= .15),
                ties=sum(v[i] == v[j] for i in range(9) for j in range(i + 1, 9)))


filas = []
for nombre, X in parts.items():
    for i in range(len(X)):
        filas.append(dict(matriz=nombre, grupo=int(P.grupo[i]), **met(X[i])))
F = pd.DataFrame(filas)
F.to_csv(AQUI / "ur270_filas.csv", index=False)
print("UR270: 6 grupos de 9 (P+S1, P y S1)")
print(F.to_string(index=False))

res = []
for nombre, X in parts.items():
    n = len(X)
    T = X.sum(1)
    p = (X / T[:, None]).mean(0)
    p = p / p.sum()
    sig = (np.log(X) - np.log(T)[:, None] - np.log(p)[None, :]).std(0)
    obs = dict(cv_mean=(X.std(1) / X.mean(1)).mean())
    for k in ["eq_all", "range1", "cv05", "cv10", "cv15", "ties"]:
        obs[k] = F[F.matriz == nombre][k].sum()
    sim = {k: np.empty(NPERM) for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties"]}
    p_row = np.zeros(n)
    for b in range(NPERM):
        Z = rng.normal(0, 1, size=(n, 9)) * sig[None, :]
        M = np.maximum(np.rint(T[:, None] * p[None, :] * np.exp(Z - .5 * sig[None, :] ** 2)), 1)
        cvs = M.std(1) / M.mean(1)
        sim["cv_mean"][b] = cvs.mean()
        sim["eq_all"][b] = sum(len(set(r)) == 1 for r in M)
        sim["range1"][b] = sum(r.max() - r.min() <= 1 for r in M)
        sim["cv05"][b] = sum(cvs <= .05)
        sim["cv10"][b] = sum(cvs <= .10)
        sim["cv15"][b] = sum(cvs <= .15)
        sim["ties"][b] = sum(sum(r[i] == r[j] for i in range(9) for j in range(i + 1, 9)) for r in M)
        p_row += (cvs <= (X.std(1) / X.mean(1)))
    for k in ["cv_mean", "eq_all", "range1", "cv05", "cv10", "cv15", "ties"]:
        cola = "baja" if k == "cv_mean" else "alta"
        pv = (1 + np.sum(sim[k] <= obs[k] if cola == "baja" else sim[k] >= obs[k])) / (NPERM + 1)
        res.append(dict(matriz=nombre, prueba=k, observado=obs[k], nulo=sim[k].mean(), p=pv))
    p_row = (1 + p_row) / (NPERM + 1)
    for i in range(n):
        res.append(dict(matriz=nombre, prueba=f"fila_g{P.grupo[i]}", observado=float(X[i].std() / X[i].mean()),
                        nulo=float(np.mean(sim["cv_mean"])), p=p_row[i]))
R = pd.DataFrame(res)
# Holm por matriz y prueba (filas por separado)
R["p_holm"] = 1.0
for (m, pr), sub in R.groupby(["matriz", "prueba"]):
    pv = sub.p.values
    orden = np.argsort(pv)
    adj = np.empty(len(pv))
    prev = 0
    for rank, j in enumerate(orden):
        prev = max(prev, min(1, (len(pv) - rank) * pv[j]))
        adj[j] = prev
    R.loc[sub.index, "p_holm"] = adj
R.to_csv(AQUI / "ur270_pruebas.csv", index=False)

print("\nPruebas globales por matriz:")
print(R[R.prueba != "fila_g0"].query("prueba != 'fila_g4' and prueba != 'fila_g5' and prueba != 'fila_g6' and prueba != 'fila_g8' and prueba != 'fila_g9'")
      .pivot(index="prueba", columns="matriz", values=["observado", "p"]).round(4).to_string())

print("\nFilas (CV) frente al nulo parametrico:")
fil = R[R.prueba.str.startswith("fila_g")]
print(fil.sort_values(["matriz", "p"]).to_string(index=False))
