# -*- coding: utf-8 -*-
"""Paso 7: (a) nulo GLOBAL (barajar valores entre quipus) para test B;
(b) difusion de los matches; (c) detalle de quipus especiales."""
import pandas as pd, numpy as np
from collections import Counter
RAIZ = "./"
rng = np.random.default_rng(0); NPERM = 500
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]; ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
ci = ci.sort_values(["kfg", "orden"])
seqval, gvals, gsizes = {}, {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]
    seqval[k] = d.loc[~d["sin_nudos"], "valor"].astype(int).tolist()
    gr = list(d.groupby("grupo")); gvals[k] = [x.loc[~x["sin_nudos"], "valor"].astype(int).tolist() for _, x in gr]
    gsizes[k] = [int(len(x)) for _, x in gr]
val_by_quipu = {k: set(seqval[k]) for k in ids}
allvals = [v for k in ids for v in seqval[k]]

def count(gsum_of, vsets):
    t = 0
    for i in ids:
        for g in gsum_of[i]:
            if g == 0: continue
            for j in ids:
                if j != i and g in vsets[j]: t += 1
    return t

obsg = {i: [sum(x) for x in gvals[i]] for i in ids}
obs = count(obsg, val_by_quipu)
print("obs cross-matches:", obs)
# nulo global: reasignar TODOS los valores entre quipus (mismos tamanos de grupo por quipu)
nulls = []
for _ in range(NPERM):
    pool = list(allvals); rng.shuffle(pool)
    gs = {}; vs = {}; idx = 0
    for i in ids:
        need = sum(gsizes[i])
        myvals = pool[idx:idx + need]; idx += need
        o = []; p = 0
        for sz in gsizes[i]:
            o.append(int(sum(myvals[p:p + sz]))); p += sz
        gs[i] = o; vs[i] = set(myvals)
    nulls.append(count(gs, vs))
nulls = np.array(nulls)
print(f"nulo GLOBAL: media={nulls.mean():.1f} p={(1+(nulls>=obs).sum())/(1+NPERM):.4f}")

# difusion: cuantos pares y reparto
pc = Counter()
for i in ids:
    for g in obsg[i]:
        if g == 0: continue
        for j in ids:
            if j != i and g in val_by_quipu[j]: pc[(i, j)] += 1
vals = np.array(list(pc.values()))
print(f"pares con >=1 match: {len(pc)} / {len(ids)*(len(ids)-1)}; "
      f"max={vals.max()} p90={np.percentile(vals,90):.0f} mediana={np.median(vals):.0f}")

# detalle quipus especiales
pd.set_option("display.width", 200)
for k in ["JC007", "UR257", "JC017"]:
    d = ci[ci["kfg"] == k]
    print(f"\n{k}:")
    print(d[["cuerda", "grupo", "valor", "color", "torsion", "union", "notas"]].to_string(index=False))
