# -*- coding: utf-8 -*-
"""05: Trio Lluta (UR131A/B/C), jerarquia detalle/resumen, ratio de subsidiarias.
Nulo: permutar valores dentro de cada quipu (500, semilla 0)."""
import pandas as pd, numpy as np, os, itertools
from collections import Counter

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]
c["v"] = pd.to_numeric(c.valor, errors="coerce")
sub = c[c.kfg.isin(CHILE)].copy()
rng = np.random.default_rng(0)

# 1) Trio: sumas por grupo (colgantes)
print("=== Trio UR131: grupos, suma de colgantes por grupo ===")
for kfg in ["UR131A", "UR131B", "UR131C"]:
    G = sub[sub.kfg == kfg]
    gs = G[G.nivel == 0].groupby("grupo")["v"].sum().astype(int).tolist()
    print(f"{kfg}: total={int(G.v.sum())}  group-sums={gs}")

# 2) A's group sums -> B's cord values, con nulo
byv = {k: set(sub[(sub.kfg == k) & (sub.v > 0)].v.astype(int).tolist()) for k in CHILE}
cordv = {k: sub[sub.kfg == k].v.fillna(0).astype(int).values.copy() for k in CHILE}
grp = {k: sub[sub.kfg == k].grupo.values for k in CHILE}

def cand_sums(vals, groups):
    df = pd.DataFrame({"v": vals, "g": groups})
    gs = df.groupby("g")["v"].sum()
    s = set(int(x) for x in gs if x > 0)
    s.add(int(vals.sum()))
    return s

obs = {}
for A in CHILE:
    ca = cand_sums(cordv[A], grp[A])
    for B in CHILE:
        if A == B:
            continue
        obs[(A, B)] = len(ca & byv[B])

NITER = 500
null = {k: [] for k in obs}
for it in range(NITER):
    perm = {}
    for A in CHILE:
        v = cordv[A].copy()
        rng.shuffle(v)
        perm[A] = v
    for A in CHILE:
        ca = cand_sums(perm[A], grp[A])
        for B in CHILE:
            if A != B:
                null[(A, B)].append(len(ca & byv[B]))

rows = []
for (A, B), o in obs.items():
    nl = np.array(null[(A, B)])
    p = (np.sum(nl >= o) + 1) / (NITER + 1)
    rows.append(dict(A=A, B=B, hits=o, null_mean=round(nl.mean(), 2), p=p))
R = pd.DataFrame(rows).sort_values("p")
pd.set_option("display.width", 200)
print("\n=== A: sumas de grupo totales -> valores en B (nulo=shuffle A) ===")
print(R.head(14).to_string(index=False))

# Holm
def holm(p):
    p = np.asarray(p, float); n = len(p); order = np.argsort(p)
    adj = np.empty(n); prev = 0.0
    for r, idx in enumerate(order):
        v = min(1.0, (n - r) * p[idx]); prev = max(prev, v); adj[idx] = prev
    return adj
R["p_holm"] = holm(R["p"].values)
print("\nsignificativos Holm<0.05:", (R.p_holm < 0.05).sum(), "de", len(R))

# 3) ratio de subsidiarias por colgante
print("\n=== ratio subsidiarias/colgante ===")
allc = c.copy()
allc["v"] = pd.to_numeric(allc.valor, errors="coerce")
rat = allc.groupby("kfg").apply(lambda g: (g.nivel > 0).sum() / max(1, (g.nivel == 0).sum()))
for k in CHILE:
    print(f"  {k}: {rat[k]:.2f}")
print("  mediana corpus:", round(rat.median(), 3), " p90:", round(rat.quantile(0.9), 3),
      " p99:", round(rat.quantile(0.99), 3))
for k in CHILE:
    print(f"  percentil de {k}: {100*(rat<=rat[k]).mean():.1f}")

# 4) top cords (union T) en todo el corpus
print("\n=== top cords (union T) en el corpus ===")
u = c.union.astype(str).str.upper()
print("quipus con >=1 T:", c[u == "T"].kfg.nunique(), "de", c.kfg.nunique())
print("cuerdas T totales:", (u == "T").sum())
print("en Chile:", c[u == "T"].kfg.isin(CHILE).sum())
