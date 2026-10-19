# -*- coding: utf-8 -*-
"""V1: ¿la cuerda superior (union=T) suma el grupo de pendientes a su izquierda?
Locke 1912/1927/1928, Ascher & Ascher 1981.
Unidad de análisis: quipu. Nulo: permutación de valores nivel 0 dentro de cada quipu,
preservando tamaños de grupo y la posición de la marca T.
"""
import pandas as pd, numpy as np, json, os
from scipy.stats import fisher_exact

RNG = np.random.default_rng(20261017)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
for c in ["valor", "grupo", "nivel", "orden"]:
    D[c] = pd.to_numeric(D[c], errors="coerce")
D["valor"] = D["valor"].fillna(0)

l0 = D[D.nivel == 0].copy()
sizes = l0.groupby(["kfg", "grupo"]).size()
sums = l0.groupby(["kfg", "grupo"]).valor.sum()

rows = []
for (k, g), n in sizes.items():
    if n != 1:
        continue
    prev_n = sizes.get((k, g - 1), 0)
    if prev_n < 3:
        continue
    cand = l0[(l0.kfg == k) & (l0.grupo == g)].iloc[0]
    rows.append(dict(kfg=k, cuerda=cand.cuerda, union=cand.union, val=cand.valor,
                     prev_sum=sums[(k, g - 1)], prev_n=prev_n,
                     ok=int(cand.valor == sums[(k, g - 1)])))
R = pd.DataFrame(rows)

print("=== V1. Top cord vs suma del grupo previo (nivel 0, grupo previo >=3 cuerdas) ===")
print("candidatos:", len(R), "quipus:", R.kfg.nunique())
tab = R.assign(T=R.union == "T").groupby("T")["ok"].agg(["size", "sum", "mean"])
print(tab.round(3).to_string())
tab2 = pd.crosstab(R.union == "T", R.ok)
print(tab2.to_string())
odds, pfish = fisher_exact([[tab2.loc[True, 1], tab2.loc[True, 0]],
                            [tab2.loc[False, 1], tab2.loc[False, 0]]], alternative="greater")
print(f"Fisher one-sided (T>noT): OR={odds:.2f} p={pfish:.4g}")

# dentro de quipus que tienen al menos una T
tq = R[R.union == "T"].kfg.unique()
sub = R[R.kfg.isin(tq)]
tab3 = sub.assign(T=sub.union == "T").groupby("T")["ok"].agg(["size", "sum", "mean"])
print("\n--- sólo quipus con alguna T ---")
print(tab3.round(3).to_string())
t3 = pd.crosstab(sub.union == "T", sub.ok)
odds3, p3 = fisher_exact([[t3.loc[True, 1], t3.loc[True, 0]],
                          [t3.loc[False, 1], t3.loc[False, 0]]], alternative="greater")
print(f"Fisher: OR={odds3:.2f} p={p3:.4g}")

print("\n--- desglose por quipu (T) ---")
per = R[R.union == "T"].groupby("kfg")["ok"].agg(["size", "sum"])
per["rate"] = (per["sum"] / per["size"]).round(2)
print(per.to_string())

# ---- Nulo: permutar valores nivel 0 dentro de cada quipu ----
# Se preserva: tamaño de cada grupo, qué cuerda es T, cuántas cuerdas nivel 0 hay.
# Sólo se permuta en los quipus que aportan candidatos T (los demás no cambian el estadístico).
B = 5000
obs = int(R[R.union == "T"].ok.sum())
prep = []
for k in R[R.union == "T"].kfg.unique():
    g = l0[l0.kfg == k].reset_index(drop=True)
    gs = g.groupby("grupo").size()
    # índice de grupo previo para cada cuerda
    prev_idx = np.array([g.index[(g.grupo == gr - 1)].tolist() for gr in g.grupo], dtype=object)
    sums_cache = {}
    is_cand = np.array([(gs.get(gr, 0) == 1 and gs.get(gr - 1, 0) >= 3 and u == "T")
                        for gr, u in zip(g.grupo, g.union)])
    prep.append((g.valor.to_numpy(float), g.grupo.to_numpy(), is_cand))
null = np.zeros(B, dtype=int)
for b in range(B):
    cnt = 0
    for vals, grp, cand in prep:
        v = vals.copy(); RNG.shuffle(v)
        s = np.bincount(grp, weights=v)
        sz = np.bincount(grp)
        for i in np.where(cand)[0]:
            gi = grp[i]
            if gi - 1 < len(s) and s[gi - 1] == v[i]:
                cnt += 1
    null[b] = cnt
p_perm = (1 + (null >= obs).sum()) / (B + 1)
print(f"\nNulo permutación (B={B}): observado={obs}, media nula={null.mean():.1f}, "
      f"p95={np.percentile(null,95):.0f}, p={p_perm:.4g}")

# ---- Variante: suma incluyendo subsidiarias del grupo previo ----
rows2 = []
for (k, g), n in sizes.items():
    if n != 1:
        continue
    if sizes.get((k, g - 1), 0) < 3:
        continue
    cand = l0[(l0.kfg == k) & (l0.grupo == g)].iloc[0]
    prev_all = D[(D.kfg == k) & (D.grupo == g - 1)].valor.sum()
    rows2.append((cand.union == "T", int(cand.valor == prev_all)))
R2 = pd.DataFrame(rows2, columns=["T", "ok"])
print("\n--- variante: grupo previo incluye subsidiarias ---")
print(R2.groupby("T")["ok"].agg(["size", "sum", "mean"]).round(3).to_string())

# ---- Control negativo: ¿cuántos grupos SIN candidato T tienen suma detectable en el grupo siguiente? ----
# (mismo estadístico pero la marca T se ignora)
all_single = R.copy()
print("\nresumen para informe:", json.dumps(dict(
    n_cand=len(R), n_T=int((R.union == "T").sum()), ok_T=obs,
    n_noT=int((R.union != "T").sum()), ok_noT=int(R[R.union != "T"].ok.sum()),
    fisher_p=float(pfish), fisher_p_within=float(p3), perm_p=float(p_perm),
    null_mean=float(null.mean()), quipus_T=int(R[R.union=="T"].kfg.nunique()))))
