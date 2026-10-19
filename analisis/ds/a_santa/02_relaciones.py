# -*- coding: utf-8 -*-
"""Relaciones ENTRE quipus del conjunto + modelo nulo (barajar valores dentro
de cada quipu, 500 veces, semilla 0)."""
import pandas as pd, numpy as np, itertools, os

BASE = r"."
DAT = os.path.join(BASE, "analisis", "datos")
OUT = os.path.join(BASE, "analisis", "ds", "a_santa")
RNG = np.random.default_rng(0)
NB = 500

IDS = ["KH0227", "UR087", "UR088", "UR089", "UR090", "UR091", "UR092", "UR198"]
SANTA = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]

cu = pd.read_csv(os.path.join(DAT, "cuerdas.csv"))
cu = cu[cu["kfg"].isin(IDS)].copy()
cu["has"] = cu["nudos"].notna() & (cu["nudos"].astype(str).str.strip() != "")

seq = {}
for k in IDS:
    d = cu[(cu["kfg"] == k)].sort_values("orden")
    seq[k] = d.loc[d["has"], "valor"].astype(int).to_numpy()

def trigrams(a):
    return set(tuple(a[i:i+3]) for i in range(len(a)-2))

def stat_shared3(a, b):
    return len(trigrams(a) & trigrams(b))

print("=== PARES: 3-gramas compartidos (obs vs nulo 500x) ===")
rows = []
pairs = list(itertools.combinations(IDS, 2))
for a, b in pairs:
    obs = stat_shared3(seq[a], seq[b])
    null = np.array([stat_shared3(RNG.permutation(seq[a]), RNG.permutation(seq[b]))
                     for _ in range(NB)])
    p = (1 + (null >= obs).sum()) / (NB + 1)
    rows.append(dict(A=a, B=b, obs=obs, null_mean=round(null.mean(), 2),
                     null_max=int(null.max()), p=p))
res = pd.DataFrame(rows)
print(res.sort_values("obs", ascending=False).head(12).to_string(index=False))
res.to_csv(os.path.join(OUT, "pares_trigramas.csv"), index=False)
n_sig = (res["p"] < 0.05).sum()
print("pares con p<0.05 crudo:", n_sig, "de", len(res))

# ---- estructura de grupos ----
gr = pd.read_csv(os.path.join(DAT, "grupos.csv"))
gr = gr[gr["kfg"].isin(IDS)].copy()
gr["n"] = gr["hasta"] - gr["desde"] + 1
gstats = gr.groupby("kfg")["n"].apply(lambda x: sorted(x.tolist()))
print("\n=== MULTISET de tamanos de grupo (por quipu) ===")
for k in IDS:
    from collections import Counter
    print(k, dict(Counter(gstats[k])))

# ---- totales y sumas de grupo ----
print("\n=== TOTALES ===")
cu["v"] = np.where(cu["has"], cu["valor"], np.nan)
tot = cu.groupby("kfg")["v"].sum()
print(tot.to_string())
# suma de solo colgantes (nivel 0)
pend = cu[cu["nivel"] == 0]
print("\nsuma colgantes (nivel0):"); print(pend.groupby("kfg")["v"].sum().to_string())

# sumas por grupo (colgantes)
gs = cu[(cu["nivel"] == 0)].groupby(["kfg", "grupo"])["v"].sum().reset_index()
print("\n=== SUMAS DE GRUPO (colgantes) por quipu ===")
for k in IDS:
    print(k, gs[gs["kfg"] == k]["v"].dropna().astype(int).tolist())

# ---- test: 'totales de A aparecen en B' ----
print("\n=== Totales de grupo de A presentes como VALOR en B (obs vs nulo) ===")
valset = {k: set(seq[k]) for k in IDS}
rows2 = []
for a in IDS:
    gA = gs[gs["kfg"] == a]["v"].dropna().astype(int).to_numpy()
    if len(gA) == 0:
        continue
    for b in IDS:
        if a == b:
            continue
        obs = sum(1 for x in gA if x in valset[b])
        null = np.array([sum(1 for x in gA if x in set(RNG.permutation(seq[b])))
                         for _ in range(NB)])
        p = (1 + (null >= obs).sum()) / (NB + 1)
        rows2.append(dict(A=a, B=b, n_gA=len(gA), obs=obs,
                          null_mean=round(null.mean(), 2), p=p))
r2 = pd.DataFrame(rows2)
print(r2.sort_values("p").head(12).to_string(index=False))
r2.to_csv(os.path.join(OUT, "totales_grupo_en_valores.csv"), index=False)
