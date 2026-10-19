# -*- coding: utf-8 -*-
"""Jerarquia detalle/resumen: sumas de grupo de un quipu como valor/total en otro.
Y control del test2 con nulos pooled. Ademas: control positivo de sensibilidad."""
import pandas as pd, numpy as np, itertools
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
g = pd.read_csv(BASE + r"\analisis\datos\grupos.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
site = dict(zip(sel["kfg"], sel["sitio"]))
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]

# valores nivel 0 por quipu y sumas de grupo
V0, GSUM = {}, {}
for k in solo:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V0[k] = d["valor"].fillna(0).astype(int).values
    gg = g[g["kfg"] == k].sort_values("grupo")
    s = []
    v = V0[k]
    for _, r in gg.iterrows():
        a, b = int(r["desde"]) - 1, int(r["hasta"])
        s.append(int(v[a:b].sum()))
    GSUM[k] = s

tot = {k: int(V0[k].sum()) for k in solo}

# coincidencias: total(A) como suma de un grupo de B
rows = []
for a in solo:
    for b in solo:
        if a != b and tot[a] > 0 and tot[a] in GSUM[b]:
            rows.append((a, site[a], tot[a], b, site[b]))
print("total(A) == suma de un grupo de B:", len(rows), "| mismo sitio:",
      sum(1 for r in rows if r[1] == r[4]))
print(pd.Series([r[2] for r in rows]).value_counts().head(8).to_string())

# coincidencias: suma de grupo de A == valor de nivel0 de B
rows2 = []
for a in solo:
    sa = set(x for x in GSUM[a] if x > 0)
    for b in solo:
        if a != b:
            inter = sa & set(x for x in V0[b] if x > 0)
            if inter:
                rows2.append((a, b, len(inter), site[a] == site[b]))
print("\nsuma_grupo(A) coincide con valor nivel0(B): pares =", len(rows2),
      "| total coincidencias =", sum(r[2] for r in rows2), "| mismo sitio:", sum(r[2] for r in rows2 if r[3]))

# nulo pooled para 'total(A) en GSUM(B)'
allg = [x for k in solo for x in GSUM[k]]
ns = len(solo)
nullA = np.zeros(NC)
for it in range(NC):
    perm = rng.permutation(allg); idx = 0; gg = {}
    for k in solo:
        gg[k] = set(perm[idx:idx + len(GSUM[k])]); idx += len(GSUM[k])
    # total(A) fijo pero grupos barajados globalmente; usar tot de valores barajados
    allv = np.concatenate([V0[k] for k in solo])
    rng.shuffle(allv); idx = 0; tt = {}
    for k in solo:
        seg = allv[idx:idx + len(V0[k])]; idx += len(V0[k]); tt[k] = int(seg.sum())
    cnt = 0
    for a in solo:
        for b in solo:
            if a != b and tt[a] > 0 and tt[a] in gg[b]:
                cnt += 1
    nullA[it] = cnt
obsA = len(rows)
print(f"\nNulo pooled (total en suma de grupo): obs={obsA} nulo={nullA.mean():.1f} sd={nullA.std():.1f} "
      f"p={(np.sum(nullA>=obsA)+1)/(NC+1):.4f}")

# CONTROL POSITIVO de sensibilidad: duplicar un quipu y ver que se detecta
def bg(v): return set(zip(list(v)[:-1], list(v)[1:]))
# tomar UR060 (114 cuerdas) y crear copia exacta + ruido
base = list(V0["UR060"])
copy = base[:]
print("\nControl positivo: bigramas(UR060) & bigramas(copia exacta) =", len(bg(base) & bg(copy)),
      "(debe ser = nº bigramas =", len(bg(base)), ")")
# control: bigramas con un quipu no relacionado
print("bigramas(UR060) & bigramas(UR061) =", len(bg(base) & bg(list(V0["UR061"]))))

# HP047 y UR186: cuerdas superiores y sumas internas
print("\n--- HP047 (Armatambo, con cuerdas superiores) ---")
d = cc[cc["kfg"] == "HP047"].sort_values("orden")
print(d[["cuerda", "nivel", "grupo", "valor", "color", "union"]].head(30).to_string(index=False))
print("\n--- UR186 (Chancay/Huando) cuerdas union T ---")
d = cc[(cc["kfg"] == "UR186")].sort_values("orden")
print(d[d["union"] == "T"][["cuerda", "nivel", "grupo", "valor", "color", "union"]].to_string(index=False))
