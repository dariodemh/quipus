# -*- coding: utf-8 -*-
"""Controles: binomial por quipu + BH, permutacion de prefijos, sensibilidad."""
import os
import pandas as pd
import numpy as np
from scipy import stats

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
rng = np.random.default_rng(20261018)

g = pd.read_csv(os.path.join(SAL, "por_quipu_final.csv"), index_col=0)
g = g[~g.index.isin({"KH0197", "KH0227", "KH0267", "KH0350",
                     "UR196", "MM007_AN002"})]
g = g[g.n_valor > 0].copy()
GLOBAL = g.disc_valor.sum() / g.n_valor.sum()
print("tasa global de discrepancia de valor:", round(GLOBAL, 5),
      f"({int(g.disc_valor.sum())}/{int(g.n_valor.sum())})")

# --- 1. binomial por quipu + BH ---
g["p_bin"] = stats.binom.sf(g.disc_valor - 1, g.n_valor, GLOBAL)
g.loc[g.disc_valor == 0, "p_bin"] = 1.0
m = len(g)
o = g.p_bin.sort_values()
bh = o * m / np.arange(1, m + 1)
bh = np.minimum.accumulate(bh[::-1])[::-1]
g["q_bh"] = pd.Series(bh, index=o.index).reindex(g.index)
sig = g[(g.q_bh < 0.05)].sort_values("q_bh")
print("\nquipus con exceso significativo tras BH (q<0.05):", len(sig))
print(sig[["prefijo", "n_valor", "disc_valor", "tasa_valor", "p_bin", "q_bh"]].head(20).to_string())
g.to_csv(os.path.join(SAL, "por_quipu_controles.csv"))

# --- 2. permutacion de prefijos (unidad = quipu) ---
def chi2_pref(df):
    tab = df.groupby("prefijo")[["disc_valor", "n_valor"]].sum()
    tab["ok"] = tab.n_valor - tab.disc_valor
    obs = tab[["disc_valor", "ok"]].values.astype(float)
    exp = obs.sum(1, keepdims=True) * obs.sum(0, keepdims=True) / obs.sum()
    return np.nansum((obs - exp) ** 2 / np.where(exp == 0, np.nan, exp))

pref = g[g.prefijo.isin(["AS", "UR", "HP", "JC", "KH"])].copy()
obs_stat = chi2_pref(pref)
B = 20000
perm = np.empty(B)
vals = pref.prefijo.values
for b in range(B):
    tmp = pref.copy()
    tmp["prefijo"] = rng.permutation(vals)
    perm[b] = chi2_pref(tmp)
p_perm = (1 + (perm >= obs_stat).sum()) / (B + 1)
print(f"\nheterogeneidad entre prefijos: chi2={obs_stat:.1f}, p_perm={p_perm:.4f} (B={B})")

# --- 3. tasas por prefijo y permutacion por pares ---
print("\ntasas por prefijo:")
tab = pref.groupby("prefijo").agg(quipus=("n_valor", "size"), n=("n_valor", "sum"),
                                  d=("disc_valor", "sum"))
tab["tasa"] = tab.d / tab.n
print(tab.to_string())

pares = [("AS", "UR"), ("AS", "HP"), ("AS", "JC"), ("AS", "KH"), ("UR", "HP"),
         ("UR", "JC"), ("UR", "KH"), ("HP", "JC"), ("HP", "KH"), ("JC", "KH")]
res = []
for a, b in pares:
    sub = pref[pref.prefijo.isin([a, b])]
    d = sub.disc_valor.values.astype(float)
    n = sub.n_valor.values.astype(float)
    na = (sub.prefijo == a).values
    obs = abs(d[na].sum() / n[na].sum() - d[~na].sum() / n[~na].sum())
    cnt = 0
    for _ in range(5000):
        mask = rng.permutation(na)
        diff = abs(d[mask].sum() / n[mask].sum() - d[~mask].sum() / n[~mask].sum())
        if diff >= obs - 1e-12:
            cnt += 1
    res.append((f"{a}-{b}", obs, (cnt + 1) / 5001))
pr = pd.DataFrame(res, columns=["par", "dif", "p"])
# Holm
pr = pr.sort_values("p").reset_index(drop=True)
pr["p_holm"] = np.minimum(1, np.maximum.accumulate(pr.p * (len(pr) - pr.index)))
print("\npares (permutacion, Holm):")
print(pr.to_string(index=False))

# --- 4. sensibilidad: sin los 5 quipus de valor mas discrepante ---
top = g.sort_values("disc_valor", ascending=False).head(5)
print("\ntop5 quipus por discrepancias de valor:")
print(top[["prefijo", "n_valor", "disc_valor"]].to_string())
sin = pref[~pref.index.isin(top.index)]
t2 = sin.groupby("prefijo").agg(n=("n_valor", "sum"), d=("disc_valor", "sum"))
t2["tasa"] = t2.d / t2.n
print("\nprefijos sin top5:")
print(t2.to_string())
