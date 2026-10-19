# -*- coding: utf-8 -*-
"""V5: 'sumas categóricas' de Ascher & Ascher (1981): ¿madre = suma de sus subsidiarias?
Nulo: permutar valores de todas las cuerdas dentro de cada quipu, preservando la jerarquía.
"""
import pandas as pd, numpy as np, os
RNG = np.random.default_rng(20261017)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
for c in ["valor", "nivel"]:
    D[c] = pd.to_numeric(D[c], errors="coerce")
D["valor"] = D["valor"].fillna(0)
D = D.reset_index(drop=True)

child = D[D.padre.notna()].copy()
# índice de la madre
pos = {(r.kfg, r.cuerda): i for i, r in D.iterrows()}
child["mi"] = [pos.get((r.kfg, r.padre), -1) for r in child.itertuples()]
child = child[child.mi >= 0]
agg = child.groupby(["kfg", "mi"]).agg(s=("valor", "sum"), n=("valor", "size")).reset_index()
agg["mv"] = D.loc[agg.mi, "valor"].to_numpy()
agg["ok"] = agg.mv == agg.s
print("=== V5. Madre = suma de subsidiarias ===")
print("madres con >=1 subsidiaria:", len(agg), "| quipus:", agg.kfg.nunique(),
      "| coincidencias:", int(agg.ok.sum()), f"({100*agg.ok.mean():.1f}%)")
print(agg.groupby("n").ok.agg(["size", "sum", "mean"]).round(3).to_string())
print("sólo madres con valor>0 y >=2 hijas:",
      int(((agg.mv > 0) & (agg.n >= 2)).sum()), "coincidencias:",
      int(agg[(agg.mv > 0) & (agg.n >= 2)].ok.sum()),
      f"({100*agg[(agg.mv>0)&(agg.n>=2)].ok.mean():.1f}%)")

# ---- nulo ----
prep = []
for k, g in D.groupby("kfg"):
    a = agg[agg.kfg == k]
    if len(a) == 0:
        continue
    idx = g.index.to_numpy()
    # valores en el orden global
    vals = g.valor.to_numpy(float)
    # mapear mi (índice global) a posición local
    loc = {gi: j for j, gi in enumerate(idx)}
    mi_loc = np.array([loc[m] for m in a.mi])
    ch = child[child.kfg == k]
    ci_loc = np.array([loc[i] for i in ch.index])
    mi_for_child = np.array([loc[m] for m in ch.mi])
    prep.append((vals, mi_loc, ci_loc, mi_for_child))
B = 2000
obs = int(agg.ok.sum())
null = np.zeros(B, dtype=int)
for b in range(B):
    cnt = 0
    for vals, mi_loc, ci_loc, mi_for_child in prep:
        v = vals.copy(); RNG.shuffle(v)
        s = np.bincount(mi_for_child, weights=v[ci_loc], minlength=len(v))
        cnt += int((v[mi_loc] == s[mi_loc]).sum())
    null[b] = cnt
p = (1 + (null >= obs).sum()) / (B + 1)
print(f"nulo B={B}: observado={obs}, media={null.mean():.0f}, p95={np.percentile(null,95):.0f}, p={p:.4g}")
print("resumen:", dict(madres=len(agg), ok=obs, rate=round(float(agg.ok.mean()),3), p=float(p)))
