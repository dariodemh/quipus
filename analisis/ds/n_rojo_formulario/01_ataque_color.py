# -*- coding: utf-8 -*-
"""ATAQUE 1: ¿sobrevive 'el color predice el valor dentro del quipu en 167/403'?

Controles que se anaden al nulo original (barajar color dentro del grupo):
  A) posicion dentro del grupo (rango normalizado, cuadratico)
  B) nivel de la cuerda (solo nivel 0 por diseno, pero se comprueba)
  C) numero de racimos de nudos por cuerda
  D) largo de la cuerda (log)
  E) cuerdas de total / maximas del grupo (se excluyen)
  F) quipus con copias conocidas (se excluyen)
Salida: color_controles.csv, color_resumen.csv
"""
import re
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(20261018)
RAIZ = r"."
NPERM = 400

c = pd.read_csv(RAIZ + r"/analisis/datos/cuerdas.csv", low_memory=False)
p = c[(c.nivel == 0) & c.color.notna() & c.valor.notna()].copy()
p["col"] = p.color.astype(str).map(lambda s: re.sub(r"\([^)]*\)", "", s))
p["y"] = np.log1p(p.valor.astype(float))
p["nrac"] = p.nudos.fillna("").map(lambda s: 0 if s == "" else s.count(";") + 1)
p["L"] = pd.to_numeric(p.largo, errors="coerce")
p.loc[p.L <= 0, "L"] = np.nan
p["logL"] = np.log(p.L)

# posicion normalizada dentro del grupo
p = p.sort_values(["kfg", "orden"]).reset_index(drop=True)
p["pos"] = 0.0
for (k, g), idx in p.groupby(["kfg", "grupo"]).groups.items():
    n = len(idx)
    if n > 1:
        p.loc[idx, "pos"] = np.arange(n) / (n - 1)

# cuerdas de total: valor == suma del resto del grupo (nivel 0)
p["es_total"] = False
p["es_max"] = False
for (k, g), idx in p.groupby(["kfg", "grupo"]).groups.items():
    v = p.loc[idx, "valor"].astype(float)
    if len(idx) >= 4:
        tot = v.sum()
        for j in idx:
            if abs(2 * p.loc[j, "valor"] - tot) < 1e-9:
                p.loc[j, "es_total"] = True
    if len(idx) >= 2:
        p.loc[p.loc[idx, "valor"].idxmax(), "es_max"] = True

# copias conocidas
try:
    cp = pd.read_csv(RAIZ + "/analisis/14_copias/filas_alineadas.csv", low_memory=False)
    copias = set(cp.A.dropna()) | set(cp.B.dropna())
except Exception:
    copias = set()


def eta2(y, g):
    m = y.mean()
    ss = ((y - m) ** 2).sum()
    if ss <= 0:
        return np.nan
    b = pd.DataFrame({"y": y, "g": g}).groupby("g").y.agg(["mean", "size"])
    return ((b["mean"] - m) ** 2 * b["size"]).sum() / ss


def eta2_fast(y, codes, k):
    """eta2 con codigos enteros 0..k-1."""
    n = len(y)
    cnt = np.bincount(codes, minlength=k).astype(float)
    sm = np.bincount(codes, weights=y, minlength=k)
    m = y.mean()
    ss = ((y - m) ** 2).sum()
    if ss <= 0:
        return np.nan
    return ((sm / np.maximum(cnt, 1) - m) ** 2 * cnt).sum() / ss


def residualiza(g):
    """y ~ C(grupo) + pos + pos^2 + nrac + logL ; devuelve residuo."""
    y = g.y.values
    X = [np.ones(len(g)), g.pos.values, g.pos.values ** 2,
         g.nrac.values.astype(float), g.logL.fillna(g.logL.median()).values]
    for u in pd.unique(g.grupo):
        X.append((g.grupo.values == u).astype(float))
    X = np.column_stack(X)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta


def prueba(g, ycol, control):
    """control: 'ninguno' (y), 'global' (barajar en todo el quipu), 'resid' (residuo de A-D)."""
    vc = g.col.value_counts()
    keep = vc[vc >= 3].index
    if len(keep) < 2:
        return None
    g = g[g.col.isin(keep)]
    if control == "resid":
        y = residualiza(g)
    else:
        y = g.y.values
    col = g.col.values
    codes = pd.Categorical(col).codes
    k = codes.max() + 1
    if k < 2:
        return None
    obs = eta2_fast(y, codes, k)
    if not np.isfinite(obs):
        return None
    gr = g.grupo.values
    n = len(y)
    cnt = 0
    for _ in range(NPERM):
        if control == "global":
            cc = rng.permutation(codes)
        else:
            cc = codes.copy()
            for u in np.unique(gr):
                ix = np.where(gr == u)[0]
                cc[ix] = rng.permutation(cc[ix])
        if eta2_fast(y, cc, k) >= obs - 1e-12:
            cnt += 1
    return obs, k, len(g), (cnt + 1) / (NPERM + 1)


filas = []
for k, g in p.groupby("kfg"):
    if len(g) < 20:
        continue
    for control in ("global", "ninguno", "resid"):
        r = prueba(g, None, control)
        if r:
            filas.append(dict(kfg=k, control=control, n=r[2], ncol=r[1], eta2=r[0], p=r[3],
                              copia=k in copias))
R = pd.DataFrame(filas)
for control in ("global", "ninguno", "resid"):
    m = R.control == control
    R.loc[m, "q"] = multipletests(R.loc[m, "p"], method="fdr_bh")[1]
R.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/color_controles.csv", index=False)

print("quipus con >=20 colgantes:", R.kfg.nunique())
for control in ("global", "ninguno", "resid"):
    m = R.control == control
    print(f"{control:8s}: n={m.sum()} q<0.05={(R.loc[m,'q']<0.05).sum()} "
          f"eta2_med={R.loc[m,'eta2'].median():.3f} q_med={R.loc[m,'q'].median():.3f}")

# ---- E) sin cuerdas de total / sin la mayor del grupo ----
p2 = p[~p.es_total & ~p.es_max].copy()
filas2 = []
for k, g in p2.groupby("kfg"):
    if len(g) < 20:
        continue
    for control in ("ninguno", "resid"):
        r = prueba(g, None, control)
        if r:
            filas2.append(dict(kfg=k, control=control, n=r[2], ncol=r[1], eta2=r[0], p=r[3],
                               copia=k in copias))
R2 = pd.DataFrame(filas2)
for control in ("ninguno", "resid"):
    m = R2.control == control
    R2.loc[m, "q"] = multipletests(R2.loc[m, "p"], method="fdr_bh")[1]
R2.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/color_sin_totales.csv", index=False)
for control in ("ninguno", "resid"):
    m = R2.control == control
    print(f"sin total/max, {control}: n={m.sum()} q<0.05={(R2.loc[m,'q']<0.05).sum()} "
          f"eta2_med={R2.loc[m,'eta2'].median():.3f}")

# ---- F) sin quipus con copias ----
for nombre, tab in (("base-resid", R[R.control == "resid"]),
                    ("sin_totales-resid", R2[R2.control == "resid"])):
    sub = tab[~tab.copia]
    print(f"{nombre} sin copias: n={len(sub)} q<0.05={(sub.q<0.05).sum()} "
          f"eta2_med={sub.eta2.median():.3f}")
print("quipus marcados como copia:", len(copias))

# ---- binomial: cuantos aciertos esperamos con q<0.05 ----
from scipy.stats import binom
for control in ("global", "ninguno", "resid"):
    m = R.control == control
    k = int((R.loc[m, "q"] < 0.05).sum()); n = int(m.sum())
    print(f"binomial {control}: {k}/{n} vs {0.05*n:.1f} esperados, p={binom.sf(k-1,n,0.05):.2e}")

# ---- cuanto del eta2 del color lo explica la posicion dentro del grupo ----
r2pos = []
for k, g in p.groupby("kfg"):
    if len(g) < 20:
        continue
    v = pd.get_dummies(g.col).values
    Xp = np.column_stack([np.ones(len(g)), g.pos.values, g.pos.values ** 2])
    B, *_ = np.linalg.lstsq(Xp, v, rcond=None)
    res = v - Xp @ B
    ss = ((v - v.mean(0)) ** 2).sum()
    r2 = 1 - (res ** 2).sum() / ss if ss > 0 else np.nan
    r2pos.append((k, r2))
r2p = pd.Series(dict(r2pos), name="r2_pos")
print(f"\nR2 de color ~ posicion+pos2 (mediana): {r2p.median():.3f}; "
      f"P25={r2p.quantile(.25):.3f} P75={r2p.quantile(.75):.3f}")

# ---- cuanto del efecto lo cargan las cuerdas de total ----
print("\ncuerdas total:", int(p.es_total.sum()), "| maximas de grupo:", int(p.es_max.sum()))
print("eta2 mediana con vs sin totales:",
      round(R[R.control == 'ninguno'].eta2.median(), 3),
      round(R2.eta2.median(), 3))

# ---- diagnostico: valor medio por color entre los quipus con efecto ----
hits = set(R[(R.control == "resid") & (R.q < 0.05)].kfg)
pp = p[p.kfg.isin(hits)]
print("\nEn quipus con efecto (resid): valor mediano por color (n>=200 cuerdas):")
t = pp.groupby("col").valor.agg(["size", "median"]).query("size>=200").sort_values("median", ascending=False)
print(t.head(10).to_string())
