# -*- coding: utf-8 -*-
"""Estructura de grupos (base rate corpus), colores y jerarquia."""
import pandas as pd, numpy as np, itertools, os

BASE = r"."
DAT = os.path.join(BASE, "analisis", "datos")
OUT = os.path.join(BASE, "analisis", "ds", "a_santa")
RNG = np.random.default_rng(0)
NB = 500

IDS = ["KH0227", "UR087", "UR088", "UR089", "UR090", "UR091", "UR092", "UR198"]
SANTA = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]

gr = pd.read_csv(os.path.join(DAT, "grupos.csv"))
gr["n"] = gr["hasta"] - gr["desde"] + 1

# --- base rate corpus de grupos de tamano 6 ---
allk = gr.groupby("kfg").size()
q6 = gr[gr["n"] == 6].groupby("kfg").size()
print("=== base rate: quipus (de 651) con >=1 grupo de tamano 6 ===")
print("con al menos un grupo de 6:", q6.shape[0], "de", gr['kfg'].nunique(),
      f"({100*q6.shape[0]/gr['kfg'].nunique():.1f}%)")
# entre los que tienen la misma cantidad de grupos que los Santa
santa_g = {k: g for k, g in gr[gr['kfg'].isin(SANTA)].groupby('kfg')}
print("Santa: n grupos / n grupos de 6 ->",
      {k: (len(g), int((g['n'] == 6).sum())) for k, g in santa_g.items()})

# --- colores: similitud de secuencia de colores entre pares ---
cu = pd.read_csv(os.path.join(DAT, "cuerdas.csv"))
cu = cu[cu["kfg"].isin(IDS)].copy()
cseq = {k: cu[cu["kfg"] == k].sort_values("orden")["color"].fillna("NA").tolist() for k in IDS}
def cgram(a, L=4):
    return set(tuple(a[i:i+L]) for i in range(len(a)-L+1))
print("\n=== 4-gramas de COLOR compartidos (obs vs nulo 500x) ===")
rows = []
for a, b in itertools.combinations(IDS, 2):
    A, B = cseq[a], cseq[b]
    obs = len(cgram(A) & cgram(B))
    null = np.array([len(cgram(list(RNG.permutation(A))) & cgram(list(RNG.permutation(B))))
                     for _ in range(NB)])
    p = (1 + (null >= obs).sum()) / (NB + 1)
    rows.append(dict(A=a, B=b, obs=obs, null_mean=round(null.mean(), 2), p=p))
rc = pd.DataFrame(rows)
print(rc.sort_values("p").head(10).to_string(index=False))
rc.to_csv(os.path.join(OUT, "pares_color4gramas.csv"), index=False)
print("pares p<0.05 crudo:", (rc['p'] < 0.05).sum())

# --- jerarquia: quipus de resumen? cordones superiores (T) y valores grandes ---
print("\n=== indicadores de 'resumen' ===")
cu["has"] = cu["nudos"].notna() & (cu["nudos"].astype(str).str.strip() != "")
cu["v"] = np.where(cu["has"], cu["valor"], np.nan)
tab = cu.groupby("kfg").agg(
    n=("cuerda", "size"),
    n_T=("union", lambda s: (s == "T").sum()),
    maxv=("v", "max"), tot=("v", "sum"),
    media=("v", "mean"))
print(tab.round(2).to_string())
