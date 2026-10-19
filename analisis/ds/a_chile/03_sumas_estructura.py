# -*- coding: utf-8 -*-
"""03: Sumas, estructura de grupos, colores, totales cruzados."""
import pandas as pd, numpy as np, os, itertools

ROOT = r"."
BASE = os.path.join(ROOT, "data", "external", "data-science-khipu-article", "data",
                    "ascher_sum_relations")
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]

print("=== Relaciones de suma Ascher (KFG) por quipu ===")
for f in ["pendant_pendant_sum_relation.csv", "indexed_pendant_sum_relation.csv",
          "pendant_pendants_color_sum_relation.csv", "indexed_subsidiary_sum_relation.csv",
          "subsidiary_pendant_sum_relation.csv", "cluster_sum_bands_relation.csv"]:
    d = pd.read_csv(os.path.join(BASE, f))
    s = d[d["name"].isin(CHILE)]
    print(f"\n-- {f}  filas={len(s)}")
    if len(s):
        cols = [x for x in ["name", "cord_name", "cord_value", "num_summands",
                            "sum_string", "handedness"] if x in s.columns]
        print(s.groupby("name").size().to_string())
        print(s[cols].head(8).to_string(index=False))

# --- Verificacion propia: padre = suma de hijas; colgante = suma de vecinos ---
print("\n=== Verificacion propia de sumas (grupo a grupo) ===")
res = []
for kfg in CHILE:
    grp = c[c.kfg == kfg].copy()
    grp["valor"] = pd.to_numeric(grp.valor, errors="coerce")
    hits_par, hits_vec = 0, 0
    for gid, G in grp.groupby("grupo"):
        pends = G[G.nivel == 0]
        vals = pends.valor.fillna(-1).tolist()
        # vecinos: valor = suma de 2-4 contiguos
        for i, x in enumerate(vals):
            if x is None or x <= 0:
                continue
            for j in range(max(0, i - 4), i):
                for k in range(i + 1, min(len(vals), i + 4)):
                    sub = [v for v in vals[j:k + 1] if v > 0]
                    s = sum(sub)
                    if len(sub) >= 2 and abs(s - x) < 1e-6:
                        hits_vec += 1
        # padre = suma de subsidiarias directas
        for _, r in G[G.nivel > 0].iterrows():
            pass
    # padre-hijo directo
    for padre, Hg in grp[grp.nivel > 0].groupby("padre"):
        pv = grp[grp.cuerda == padre].valor
        if len(pv) and pv.iloc[0] and pv.iloc[0] > 0:
            hs = Hg.valor.fillna(0)
            if abs(hs.sum() - pv.iloc[0]) < 1e-6 and len(hs) >= 2:
                hits_par += 1
    res.append(dict(kfg=kfg, sum_vecinos=hits_vec, sum_padre_hijas=hits_par))
print(pd.DataFrame(res).to_string(index=False))

# --- Estructura de grupos: vectores de nº cuerdas por grupo ---
print("\n=== Estructura de grupos (n cuerdas por grupo) ===")
gv = {}
for kfg in CHILE:
    grp = c[c.kfg == kfg]
    gv[kfg] = tuple(grp.groupby("grupo").size().tolist())

def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    return dp[-1][-1]

# base rate: comparar cada quipu Chile con TODO el corpus
allg = {}
for kfg, grp in c.groupby("kfg"):
    allg[kfg] = tuple(grp.groupby("grupo").size().tolist())

for A, B in itertools.combinations(CHILE, 2):
    la, lb = gv[A], gv[B]
    if len(la) < 2 or len(lb) < 2:
        continue
    l = lcs(la, lb)
    norm = l / max(len(la), len(lb))
    # base rate vs corpus
    br = [lcs(la, allg[z]) / max(len(la), len(allg[z])) for z in allg if z != A and len(allg[z]) >= 2]
    pct = np.mean(np.array(br) <= norm)
    if norm > 0.5:
        print(f"{A}-{B}: LCS={l} norm={norm:.2f} pct_corpus={pct:.2f} (base media={np.mean(br):.2f})")
