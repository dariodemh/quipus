# -*- coding: utf-8 -*-
"""Pares de quipus con union opuesta (patron UR273A V / UR273B R).
Busca pares A/B del mismo catalogo y pares del mismo sitio; compara con nulo
de pares del mismo sitio y tamano comparable.
"""
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng = np.random.default_rng(SEED)
d, q = prep.load()
q = q.set_index("kfg")
d0 = d[d.nivel == 0].copy()
d0["valor_n"] = pd.to_numeric(d0["valor_n"], errors="coerce")

g = d0.groupby("kfg").agg(n=("cuerda", "size"),
                          pV=("union2", lambda x: (x == "V").mean()),
                          pR=("union2", lambda x: (x == "R").mean()),
                          pZ=("torsion2", lambda x: (x == "Z").mean()),
                          tot=("valor_n", "sum"))
g = g.join(q[["procedencia", "region"]])
g["site"] = g.procedencia.fillna("Unknown")
g["strongV"] = g.pV >= 0.7
g["strongR"] = g.pR >= 0.7
g = g[g.n >= 10]
print("khipus >=10 cuerdas:", len(g), "| V-dominantes:", int(g.strongV.sum()),
      "| R-dominantes:", int(g.strongR.sum()))

COLORS = {k: set(x.color_f.dropna()) for k, x in d0.groupby("kfg")}


def content_sim(a, b):
    ca, cb = COLORS.get(a, set()), COLORS.get(b, set())
    jac = len(ca & cb) / max(1, len(ca | cb))
    ta, tb = g.loc[a, "tot"], g.loc[b, "tot"]
    ratio = min(ta, tb) / max(ta, tb) if max(ta, tb) > 0 else 0
    return jac, ratio


# ---------------- 1. pares A/B del catalogo ----------------
print("\n=== 1. Pares A/B (mitades de catalogo) ===")
d0["base"] = d0.kfg.str.replace(r"[_]?[AB]$", "", regex=True)
d0["suf"] = d0.kfg.str.extract(r"[_]?([AB])$")
ab = d0[d0.suf.notna()].groupby("base").kfg.unique()
rows = []
for b, ks in ab.items():
    if len(ks) < 2:
        continue
    a, c = ks[0], ks[1]
    if a not in g.index or c not in g.index:
        continue
    jac, ratio = content_sim(a, c)
    rows.append(dict(base=b, A=a, B=c, pV_A=g.loc[a, "pV"], pV_B=g.loc[c, "pV"],
                     nA=g.loc[a, "n"], nB=g.loc[c, "n"], site=g.loc[a, "site"],
                     jac=jac, ratio=ratio,
                     opp=((g.loc[a, "pV"] >= .7 and g.loc[c, "pV"] <= .3) or
                          (g.loc[c, "pV"] >= .7 and g.loc[a, "pV"] <= .3))))
pairs = pd.DataFrame(rows)
print(pairs.round(2).to_string(index=False))
obs = int(pairs.opp.sum())
print(f"Pares con union opuesta (>=70% V vs <=30% V): {obs}/{len(pairs)}")

idx_all = list(g.index)
cands = {}
for _, r in pairs.iterrows():
    s0 = r.site
    base_pool = list(g.index[g.site == s0]) if (s0 != "Unknown" and (g.site == s0).sum() >= 2) else idx_all
    ok = [k for k in base_pool if k not in (r.A, r.B) and
          0.6 <= g.loc[k, "n"] / max(1, r.nA) <= 1.7]
    cands[r.base] = np.array([idx_all.index(k) for k in ok])
pVs = g.pV.values
null = np.empty(3000)
for i in range(3000):
    cnt = 0
    for _, r in pairs.iterrows():
        ok = cands[r.base]
        if len(ok) < 2:
            continue
        x, y = rng.choice(ok, 2, replace=False)
        if (pVs[x] >= .7 and pVs[y] <= .3) or (pVs[y] >= .7 and pVs[x] <= .3):
            cnt += 1
    null[i] = cnt / len(pairs)
p = (1 + (null >= obs / len(pairs)).sum()) / 3001
print(f"nulo mismo sitio/tamano: {null.mean():.3f} (DE {null.std():.3f}); p={p:.4f}")

jac_obs = pairs.jac.mean(); ratio_obs = pairs.ratio.mean()
jac_null = []; ratio_null = []
for i in range(1500):
    js, rs = [], []
    for _, r in pairs.iterrows():
        ok = cands[r.base]
        if len(ok) < 2:
            continue
        x, y = rng.choice(ok, 2, replace=False)
        j, ra = content_sim(idx_all[x], idx_all[y])
        js.append(j); rs.append(ra)
    jac_null.append(np.mean(js)); ratio_null.append(np.mean(rs))
p_j = (1 + (np.array(jac_null) >= jac_obs).sum()) / 1501
p_r = (1 + (np.array(ratio_null) >= ratio_obs).sum()) / 1501
print(f"Jaccard colores A/B={jac_obs:.3f} vs nulo={np.mean(jac_null):.3f} p={p_j:.4f}")
print(f"Razon de totales A/B={ratio_obs:.3f} vs nulo={np.mean(ratio_null):.3f} p={p_r:.4f}")

# ---------------- 2. todos los pares del mismo sitio ----------------
print("\n=== 2. Todos los pares mismo sitio, tamano comparable ===")
allpairs = []
for i in range(len(idx_all)):
    for j in range(i + 1, len(idx_all)):
        a, b = idx_all[i], idx_all[j]
        if g.loc[a, "site"] != g.loc[b, "site"] or g.loc[a, "site"] == "Unknown":
            continue
        if not (0.6 <= g.loc[a, "n"] / g.loc[b, "n"] <= 1.7):
            continue
        pa, pb = g.loc[a, "pV"], g.loc[b, "pV"]
        allpairs.append((a, b, g.loc[a, "site"], pa, pb,
                         ((pa >= .7 and pb <= .3) or (pb >= .7 and pa <= .3))))
ap = pd.DataFrame(allpairs, columns=["a", "b", "site", "pV_a", "pV_b", "opp"])
print("pares mismo sitio con >=10 cuerdas:", len(ap), "| opuestos:", int(ap.opp.sum()),
      f"({ap.opp.mean():.3f})")
print(ap.groupby("site").agg(n=("opp", "size"), opp=("opp", "sum"), tasa=("opp", "mean")).round(2).to_string())

inc = g[g.site == "Incahuasi"]
print(f"\nIncahuasi: {len(inc)} quipus, {int(inc.strongV.sum())} V-dominantes, {int(inc.strongR.sum())} R-dominantes")
print(inc[["n", "pV", "pR", "tot"]].sort_values("pV").round(2).to_string())
