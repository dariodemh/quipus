# -*- coding: utf-8 -*-
"""Exploracion inicial: distribucion de valores, colores, procedencias."""
import pandas as pd, numpy as np, re

RUTA = r"./analisis/datos"
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False)

# cuerdas con nudos (valor decodificado real); excluye 0 sin nudos
c["con_nudos"] = c.nudos.notna() & c.valor.notna()
k = c[c.con_nudos].copy()
k["valor"] = k.valor.astype(int)

print("quipus:", c.kfg.nunique(), "cuerdas:", len(c), "con nudos:", len(k))
print("cuerdas por quipu: mediana", c.groupby("kfg").size().median(),
      "media", round(c.groupby("kfg").size().mean(), 1))
print("top cord (union=T):", (k.union == "T").sum())
print("nivel 0:", (k.nivel == 0).sum(), "nivel>=1:", (k.nivel >= 1).sum())

# tabla de frecuencias global
f = k.valor.value_counts().sort_values(ascending=False)
preval = k.groupby("valor").kfg.nunique()
print("\nTOP 25 valores (n cuerdas, n quipus):")
for v, n in f.head(25).items():
    print(f"{v:>8} {n:>6} {preval[v]:>5}")

print("\nvalores distintos:", len(f))
print("cuerdas cubiertas por top10:", f.head(10).sum(), "/", len(k))
print("cuerdas cubiertas por top50:", f.head(50).sum(), "/", len(k))

# colores: token primario
def color_prim(x):
    if not isinstance(x, str): return None
    return re.split(r"[\(:/,\-]", x.strip())[0].strip()
k["cprim"] = k.color.map(color_prim)
print("\ntop colores primarios:")
print(k.cprim.value_counts().head(12).to_string())

print("\nprocedencia (quipus):")
print(q.procedencia.fillna("NA").value_counts().head(12).to_string())
print("\nregion:")
print(q.region.fillna("NA").value_counts().head(12).to_string())
