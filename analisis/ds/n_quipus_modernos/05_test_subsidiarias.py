# -*- coding: utf-8 -*-
"""Convencion 'subsidiaria = cria / subcategoria'.
En los khipus de pastores la subsidiaria es la cria (mismo color, menor
valor); en la contabilidad inca la subsidiaria suele ser una parte que suma
al total de la madre. Ambas predicciones se prueban.

S1 fraccion de pares hijo<madre
S2 mediana de log(hijo/madre)
S3 fraccion de pares que son exactamente madre/k (k=2..10)
S4 fraccion de madres cuyo valor = suma de sus hijos (jerarquia aditiva)
S5 correlacion (Spearman) entre valor de la madre y numero de hijos
Nulo: barajar los valores de las madres entre madres DENTRO de cada quipu,
preservando los hijos y el numero de hijos por madre.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from utils import load, describe, SEMILLA

rng = np.random.default_rng(SEMILLA)
B = 1000

c = load()
sub = c[(c.nivel > 0) & c.padre.notna()].copy()
mv = dict(zip(zip(c.kfg, c.cuerda), c.valor))
sub["mv"] = [mv.get((k, p), np.nan) for k, p in zip(sub.kfg, sub.padre)]
sub = sub.dropna(subset=["mv"])

blocks = []
for k, d in sub.groupby("kfg"):
    # una fila por madre, con lista de hijos
    moms = []
    for p, dd in d.groupby("padre"):
        m = mv.get((k, p), np.nan)
        if np.isfinite(m):
            moms.append(dict(padre=p, mv=float(m), kids=dd.valor.fillna(0).values.astype(float)))
    if len(moms):
        blocks.append(dict(kfg=k, moms=moms))

def stats_from_mvals(mvals_list):
    s1n = s1d = 0.0
    logs = []
    simple_n = simple_d = 0.0
    add_n = add_d = 0.0
    rhos = []
    for b, mvals in zip(blocks, mvals_list):
        obs_pairs = []
        for m, mv_ in zip(b["moms"], mvals):
            for kid in m["kids"]:
                obs_pairs.append((kid, mv_))
                s1d += 1
                if kid < mv_:
                    s1n += 1
                if mv_ > 0:
                    logs.append(np.log((kid + 1e-9) / mv_))
                    for kk in range(2, 11):
                        simple_d += 1
                        if abs(kid - mv_ / kk) < 1e-6:
                            simple_n += 1
            add_d += 1
            if abs(np.sum(m["kids"]) - mv_) < 1e-6:
                add_n += 1
        # rho madre-valor vs n hijos
        if len(mvals) >= 5:
            r = spearmanr(mvals, [len(m["kids"]) for m in b["moms"]], nan_policy="omit").statistic
            if np.isfinite(r):
                rhos.append(r)
    return dict(S1=s1n / s1d if s1d else np.nan,
                S2=float(np.median(logs)) if logs else np.nan,
                S3=simple_n / simple_d if simple_d else np.nan,
                S4=add_n / add_d if add_d else np.nan,
                S5=float(np.mean(rhos)) if rhos else np.nan)


obs = stats_from_mvals([[m["mv"] for m in b["moms"]] for b in blocks])
null = {k: [] for k in ["S1", "S2", "S3", "S4", "S5"]}
for it in range(B):
    mvals = []
    for b in blocks:
        v = np.array([m["mv"] for m in b["moms"]], float)
        rng.shuffle(v)
        mvals.append(v)
    st = stats_from_mvals(mvals)
    for k in null:
        null[k].append(st[k])

labels = {"S1": "fraccion hijo < madre", "S2": "mediana log(hijo/madre)",
          "S3": "fraccion hijo = madre/k (k=2..10)",
          "S4": "fraccion madre = suma(hijos)", "S5": "rho(valor madre, n hijos)"}
sides = {"S1": "greater", "S2": "less", "S3": "greater", "S4": "greater", "S5": "greater"}
rows = []
for k in ["S1", "S2", "S3", "S4", "S5"]:
    d = describe(obs[k], null[k], sides[k])
    d.update(test=k, descripcion=labels[k], n_quipus=len(blocks), lado=sides[k])
    rows.append(d)
res = pd.DataFrame(rows)
res.to_csv("res_subsidiarias.csv", index=False, encoding="utf-8-sig")
print(res.round(4).to_string())

# descriptivos
pairs = []
for b in blocks:
    for m in b["moms"]:
        for kid in m["kids"]:
            pairs.append((b["kfg"], m["mv"], kid))
pairs = pd.DataFrame(pairs, columns=["kfg", "madre", "hijo"])
print("\npares", len(pairs), "madres", len(sub.groupby(['kfg','padre'])))
print("ratio cuantiles", np.round((pairs.hijo / pairs.madre.replace(0, np.nan)).quantile([.1,.25,.5,.75,.9]).values, 3))
print("hijo=0", round((pairs.hijo == 0).mean(), 3), "madre=0", round((pairs.madre == 0).mean(), 3))
print("n hijos por madre", sub.groupby(['kfg','padre']).size().value_counts().head(8).to_dict())
