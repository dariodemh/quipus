# -*- coding: utf-8 -*-
"""06: Tasas base del corpus para las senales de los quipus de Chile."""
import pandas as pd, numpy as np, os

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
c["v"] = pd.to_numeric(c.valor, errors="coerce")
CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]
PLM = ["KH0083", "KH0267", "UR058A", "UR084", "UR130", "UR132"]  # Playa Miller/Arica
LLU = ["AS069", "UR131A", "UR131B", "UR131C"]                    # Lluta

# ratio subsidiarias/colgante
rat = c.groupby("kfg").apply(
    lambda g: (g.nivel > 0).sum() / max(1, (g.nivel == 0).sum()), include_groups=False)
print("corpus n=", len(rat))
for thr in (1, 2, 3, 4):
    print(f"  quipus con ratio>={thr}: {(rat>=thr).sum()} ({(rat>=thr).mean()*100:.1f}%)")

print("\nPlaya Miller/Arica:", {k: round(rat[k], 2) for k in PLM})
print("  >=2 todos? ", all(rat[k] >= 2 for k in PLM))
# probabilidad de que 6 al azar sean todos >=2
p = (rat >= 2).mean()
print(f"  P(un quipu al azar ratio>=2)={p:.3f}; P(6/6)={p**6:.2e}")
print("Lluta:", {k: round(rat[k], 2) for k in LLU})

# color: fraccion AB (marron claro) por quipu
def basecol(s):
    return str(s).split(":")[0].split("/")[0].split("-")[0]
c["base"] = c.color.map(basecol)
ab = c.groupby("kfg").apply(lambda g: (g.base == "AB").mean(), include_groups=False)
print("\nfraccion de cuerdas AB:")
for k in CHILE:
    print(f"  {k}: {ab[k]:.2f}")
print(f"  corpus mediana={ab.median():.2f} p90={ab.quantile(0.9):.2f} p95={ab.quantile(0.95):.2f}")
# cuantos quipus >=0.8 AB
print(f"  quipus con AB>=0.8: {(ab>=0.8).sum()} de {len(ab)}")
print("  trio UR131 en ese grupo? ", {k: bool(ab[k]>=0.8) for k in ['UR131A','UR131B','UR131C']})

# magnitud (log10 max colgante)
mag = c[c.nivel == 0].groupby("kfg")["v"].max().apply(lambda x: np.log10(x) if x and x > 0 else 0)
print("\nmagnitud (log10 max colgante):")
for k in CHILE:
    print(f"  {k}: {mag[k]:.2f}")
print(f"  corpus mediana={mag.median():.2f} p90={mag.quantile(0.9):.2f}")

# numero de colores
ncol = c.groupby("kfg").color.nunique()
print("\nn colores Ascher:")
for k in CHILE:
    print(f"  {k}: {ncol[k]}")
print(f"  corpus mediana={ncol.median():.0f} p90={ncol.quantile(0.9):.0f}")
