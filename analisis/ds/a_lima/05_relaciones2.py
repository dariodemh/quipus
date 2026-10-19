# -*- coding: utf-8 -*-
"""Refinamiento: per-pair p/q correctos, robustez (barajar dentro de grupos),
desglose por sitio (Armatambo, Huaquerones), y jerarquia detalle/resumen."""
import pandas as pd, numpy as np, itertools
from collections import Counter
from scipy.stats import false_discovery_control as fdr
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
site = dict(zip(sel["kfg"], sel["sitio"]))
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]

# secuencias nivel 0 por quipu, con indice de grupo
def seq_of(kfg, onlygroup=False):
    d = cc[cc["kfg"] == kfg].sort_values("orden")
    d0 = d[d["nivel"] == 0]
    return list(zip(d0["grupo"].values, d0["valor"].fillna(0).astype(int).values))

SEQ = {k: seq_of(k) for k in solo}
VALS = {k: [v for _, v in SEQ[k]] for k in solo}

def bgset(vals):
    return set(zip(vals[:-1], vals[1:]))

# --- per-pair bigram test (nulo: barajar dentro de cada quipu) ---
obs = {}
bg0 = {k: bgset(VALS[k]) for k in solo}
for a, b in itertools.combinations(solo, 2):
    obs[(a, b)] = len(bg0[a] & bg0[b])
perm = {k: list(VALS[k]) for k in solo}
ge = {kk: 0 for kk in obs}
for it in range(NC):
    for k in solo:
        rng.shuffle(perm[k])
    pb = {k: bgset(perm[k]) for k in solo}
    for a, b in obs:
        if len(pb[a] & pb[b]) >= obs[(a, b)]:
            ge[(a, b)] += 1
p = np.array([(ge[kk] + 1) / (NC + 1) for kk in obs])
q = fdr(p, method="bh")
keys = list(obs)
R = pd.DataFrame({"A": [k[0] for k in keys], "B": [k[1] for k in keys],
                  "obs": [obs[k] for k in keys], "p": p, "q": q})
R.to_csv(BASE + r"\analisis\ds\a_lima\test1_bigramas_perpair.csv", index=False)
print("Test1 pares significativos q<0.05:", (q < 0.05).sum(), "de", len(keys), "| min q =", round(q.min(), 4))
print("Top 8 pares por obs:")
print(R.sort_values("obs", ascending=False).head(8).to_string(index=False))

# --- robustez: barajar dentro de cada grupo ---
def shuffle_in_groups(k, rr):
    z = SEQ[k][:]
    groups = {}
    for i, (gg, v) in enumerate(z):
        groups.setdefault(gg, []).append(i)
    vals = [v for _, v in z]
    for gg, idxs in groups.items():
        vv = [z[i][1] for i in idxs]
        rr.shuffle(vv)
        for i, v in zip(idxs, vv):
            vals[i] = v
    return vals

bg_g = {k: bgset(VALS[k]) for k in solo}
obs_g = sum(len(bg_g[a] & bg_g[b]) for a, b in itertools.combinations(solo, 2))
null_g = np.zeros(NC)
for it in range(NC):
    pg = {k: bgset(shuffle_in_groups(k, rng)) for k in solo}
    for a, b in itertools.combinations(solo, 2):
        null_g[it] += len(pg[a] & pg[b])
print(f"\nRobustez (barajar dentro de grupos): obs={obs_g} nulo medio={null_g.mean():.1f} sd={null_g.std():.1f} "
      f"z={(obs_g-null_g.mean())/null_g.std():.2f} p={(np.sum(null_g>=obs_g)+1)/(NC+1):.4f}")

# --- por sitio ---
print("\n--- Coherencia por sitio (obs medio de bigramas dentro del sitio vs entre sitios) ---")
for s in sorted(set(site.values())):
    ks = [k for k in solo if site[k] == s]
    dentro = [obs[(a, b)] for a, b in itertools.combinations(solo, 2) if a in ks and b in ks]
    fuera = [obs[(a, b)] for a, b in itertools.combinations(solo, 2)
             if (a in ks) != (b in ks)]
    if dentro:
        # nulo por permutacion de etiqueta de sitio, mismo tamano
        kd = np.mean([v for v in dentro]); 
        nk = len(ks)
        arr = np.array([obs[(a,b)] for a,b in itertools.combinations(solo,2)])
        # permutacion: elegir nk quipus al azar y tomar su subgrafo
        null = np.zeros(NC)
        for it in range(NC):
            pick = set(rng.choice(solo, size=nk, replace=False))
            dd = [obs[(a,b)] for a,b in itertools.combinations(solo,2) if a in pick and b in pick]
            null[it] = np.mean(dd) if dd else 0
        print(f"{s:12s} n={nk:2d} dentro obs={kd:.3f} (pares={len(dentro)}) nulo={null.mean():.3f} "
              f"p={(np.sum(null>=kd)+1)/(NC+1):.3f}")

# --- jerarquia detalle/resumen ---
print("\n--- Jerarquia detalle/resumen ---")
# UR1124 y su detalle
for k in ["UR1124", "UR1124_Detail_1"]:
    d = cc[cc["kfg"] == k]
    print(k, "nivel max", d["nivel"].max(), "n cuerdas", len(d),
          "valores n0", list(cc[(cc["kfg"]==k)&(cc["nivel"]==0)].sort_values("orden")["valor"].astype(int)))
# totales y cuerdas top / union T
tot = {}
for k in sel["kfg"]:
    d0 = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)]
    tot[k] = int(d0["valor"].fillna(0).sum())
# busqueda: total(A) como valor de nivel 0 en B (pares ordenados), con sitio
rows = []
for a in sel["kfg"]:
    for b in sel["kfg"]:
        if a == b:
            continue
        vb = set(cc[(cc["kfg"] == b) & (cc["nivel"] == 0)]["valor"].fillna(0).astype(int))
        if tot[a] > 0 and tot[a] in vb:
            rows.append((a, site[a], tot[a], b, site[b], site[a] == site[b]))
E = pd.DataFrame(rows, columns=["A", "sitioA", "totalA", "B", "sitioB", "mismoSitio"])
print("Coincidencias total(A) en nivel0(B):", len(E), "| mismo sitio:", E["mismoSitio"].sum())
print("Distribucion de totalA mas repetidos:")
print(E["totalA"].value_counts().head(8).to_string())
