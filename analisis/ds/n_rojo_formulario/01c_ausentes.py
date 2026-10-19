# -*- coding: utf-8 -*-
"""ATAQUE 1c (robustez, regla 6 del BRIEF): repetir el ataque 1 excluyendo las
cuerdas con valor 0 y `nudos` vacio (ausentes, no ceros reales).
Solo condicion 'resid' (la conservadora) y 'ninguno' (nulo dentro de grupo).
"""
import re
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
from scipy.stats import binom

rng = np.random.default_rng(20261018)
RAIZ = r"."
NPERM = 300
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
p = c[(c.nivel == 0) & c.color.notna() & c.valor.notna()].copy()
vacia = (pd.to_numeric(p.valor, errors="coerce") == 0) & (p.nudos.isna() | (p.nudos.astype(str) == ""))
print("cuerdas nivel 0 con color y valor:", len(p), "| valor 0 y sin nudos:", int(vacia.sum()))
p = p[~vacia].copy()
p["col"] = p.color.astype(str).map(lambda s: re.sub(r"\([^)]*\)", "", s))
p["y"] = np.log1p(p.valor.astype(float))
p["nrac"] = p.nudos.fillna("").map(lambda s: 0 if s == "" else s.count(";") + 1)
p["L"] = pd.to_numeric(p.largo, errors="coerce")
p.loc[p.L <= 0, "L"] = np.nan
p["logL"] = np.log(p.L)
p = p.sort_values(["kfg", "orden"]).reset_index(drop=True)
p["pos"] = 0.0
for (k, g), idx in p.groupby(["kfg", "grupo"]).groups.items():
    if len(idx) > 1:
        p.loc[idx, "pos"] = np.arange(len(idx)) / (len(idx) - 1)
p["es_total"] = False
p["es_max"] = False
for (k, g), idx in p.groupby(["kfg", "grupo"]).groups.items():
    v = p.loc[idx, "valor"].astype(float)
    if len(idx) >= 4:
        for j in idx:
            if abs(2 * p.loc[j, "valor"] - v.sum()) < 1e-9:
                p.loc[j, "es_total"] = True
    if len(idx) >= 2:
        p.loc[p.loc[idx, "valor"].idxmax(), "es_max"] = True
cp = pd.read_csv(RAIZ + "/analisis/14_copias/filas_alineadas.csv", low_memory=False)
copias = set(cp.A.dropna()) | set(cp.B.dropna())


def eta2(y, codes, k):
    cnt = np.bincount(codes, minlength=k).astype(float)
    sm = np.bincount(codes, weights=y, minlength=k)
    m = y.mean()
    ss = ((y - m) ** 2).sum()
    if ss <= 0:
        return np.nan
    return ((sm / np.maximum(cnt, 1) - m) ** 2 * cnt).sum() / ss


def resid(g):
    y = g.y.values
    X = [np.ones(len(g)), g.pos.values, g.pos.values ** 2, g.nrac.values.astype(float),
         g.logL.fillna(g.logL.median()).values]
    for u in pd.unique(g.grupo):
        X.append((g.grupo.values == u).astype(float))
    X = np.column_stack(X)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ b


filas = []
for etiqueta, tab in (("todas", p), ("sin_total_max", p[~p.es_total & ~p.es_max])):
    for k, g in tab.groupby("kfg"):
        if len(g) < 20:
            continue
        vc = g.col.value_counts()
        keep = vc[vc >= 3].index
        if len(keep) < 2:
            continue
        g = g[g.col.isin(keep)]
        y = resid(g)
        codes = pd.Categorical(g.col.values).codes
        kk = codes.max() + 1
        obs = eta2(y, codes, kk)
        gr = g.grupo.values
        cnt = 0
        for _ in range(NPERM):
            cc = codes.copy()
            for u in np.unique(gr):
                ix = np.where(gr == u)[0]
                cc[ix] = rng.permutation(cc[ix])
            if eta2(y, cc, kk) >= obs - 1e-12:
                cnt += 1
        filas.append(dict(cond=etiqueta, kfg=k, n=len(g), eta2=obs,
                          p=(cnt + 1) / (NPERM + 1), copia=k in copias))
R = pd.DataFrame(filas)
for etiqueta in ("todas", "sin_total_max"):
    m = R.cond == etiqueta
    R.loc[m, "q"] = multipletests(R.loc[m, "p"], method="fdr_bh")[1]
    sub = R[m & ~R.copia]
    q2 = multipletests(sub.p, method="fdr_bh")[1]
    print(f"{etiqueta}: n={m.sum()} q<.05={(R.loc[m,'q']<.05).sum()} | "
          f"sin copias n={len(sub)} q<.05={(q2<.05).sum()} "
          f"(esperado {0.05*len(sub):.1f}, p={binom.sf((q2<.05).sum()-1,len(sub),.05):.3g}) "
          f"eta2_med={sub.eta2.median():.3f}")
R.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/color_sin_ausentes.csv", index=False)
