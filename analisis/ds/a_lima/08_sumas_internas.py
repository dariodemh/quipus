# -*- coding: utf-8 -*-
"""(a) Enriquecimiento dentro de sitio de coincidencias suma-grupo/valor.
(b) Detector interno de sumas: cord = suma de bloque consecutivo contiguo en su grupo.
(c) HP047 como posible quipu de resumen."""
import pandas as pd, numpy as np, itertools
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
g = pd.read_csv(BASE + r"\analisis\datos\grupos.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
site = dict(zip(sel["kfg"], sel["sitio"]))
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]
V0, GSUM = {}, {}
for k in solo:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V0[k] = d["valor"].fillna(0).astype(int).values
    gg = g[g["kfg"] == k].sort_values("grupo")
    V0[k] = d["valor"].fillna(0).astype(int).values
    GSUM[k] = [int(V0[k][int(r["desde"]) - 1:int(r["hasta"])].sum()) for _, r in gg.iterrows()]

# (a) coincidencia suma_grupo(A) == valor(B): fraccion mismo sitio vs baseline
coinc = []  # (A,B)
for a in solo:
    sa = set(x for x in GSUM[a] if x > 0)
    for b in solo:
        if a != b and (sa & set(x for x in V0[b] if x > 0)):
            coinc.append((a, b))
same = sum(1 for a, b in coinc if site[a] == site[b])
frac = same / len(coinc)
# baseline esperado bajo etiquetas permutadas
base = 0
for _ in range(NC):
    perm = rng.permutation([site[k] for k in solo]); gm = dict(zip(solo, perm))
    base += sum(1 for a, b in coinc if gm[a] == gm[b]) / len(coinc)
print(f"(a) mismo-sitio en coincidencias: obs={frac:.3f} vs baseline(nulo)={base/NC:.3f}")
# nulo completo: permutar valores de B -> recomputar coincidencias y su fraccion mismo sitio
null_frac = np.zeros(NC)
tot_vals = {k: list(V0[k]) for k in solo}
for it in range(NC):
    for k in solo: rng.shuffle(tot_vals[k])
    sets = {k: set(x for x in tot_vals[k] if x > 0) for k in solo}
    c2 = [(a, b) for a in solo for b in solo if a != b and (set(x for x in GSUM[a] if x > 0) & sets[b])]
    null_frac[it] = sum(1 for a, b in c2 if site[a] == site[b]) / len(c2) if c2 else 0
print(f"    nulo barajando valores: media={null_frac.mean():.3f} sd={null_frac.std():.3f} "
      f"p={(np.sum(null_frac>=frac)+1)/(NC+1):.3f}")

# (b) detector interno de sumas
def find_sums(k):
    res = []
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    for grp, dd in d.groupby("grupo"):
        vals = dd["valor"].fillna(0).astype(int).values
        names = dd["cuerda"].values
        n = len(vals)
        for j in range(n):
            tgt = vals[j]
            if tgt <= 0: continue
            for i in range(j):
                # bloques contiguos hasta j-1 que sumen tgt
                s = 0
                for m in range(i, j):
                    s += vals[m]
                    if s == tgt and m > i:
                        res.append((k, names[j], tgt, names[i], names[m]))
    return res
S = []
for k in sel["kfg"]:
    S += find_sums(k)
S = pd.DataFrame(S, columns=["kfg", "cord", "valor", "desde", "hasta"])
print("\n(b) Sumas internas (cord = suma de bloque consecutivo en su grupo):", len(S), "relaciones,",
      S["kfg"].nunique(), "quipus")
if len(S):
    S["sitio"] = S["kfg"].map(site)
    print(S.groupby("sitio")["kfg"].nunique().to_string())
    print(S.to_string(index=False)[:1500])

# (c) HP047: cuerdas y sumas
print("\n(c) HP047: total sumas internas:", (S["kfg"] == "HP047").sum())
print(S[S["kfg"] == "HP047"].to_string(index=False))
print("V0 HP047:", list(V0["HP047"]), " suma n0 (sin p1):", int(V0["HP047"].sum()))
