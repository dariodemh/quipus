# -*- coding: utf-8 -*-
"""Paso 1: descripcion del conjunto Incahuasi. Solo imprime resumenes cortos."""
import pandas as pd, numpy as np

RAIZ = "./"
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
g = pd.read_csv(RAIZ + "analisis/datos/grupos.csv")

inc = q[q["procedencia"] == "Incahuasi"]
ids = sorted(inc["kfg"].tolist())
print("N quipus Incahuasi:", len(ids))
print("ids:", ids)

ci = c[c["kfg"].isin(ids)].copy()
print("\nN cuerdas totales:", len(ci))
print("cuerdas por quipu (min/med/max):",
      ci.groupby("kfg").size().min(), ci.groupby("kfg").size().median(), ci.groupby("kfg").size().max())

# valores con nudos (0 sin nudos = ausente)
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
print("\nFraccion cuerdas sin nudos:", round(ci["sin_nudos"].mean(), 3))
val = ci.loc[~ci["sin_nudos"], "valor"]
print("valores: min", val.min(), "max", val.max(), "mediana", val.median())
print("rango por quipu:")
for k, d in ci[~ci["sin_nudos"]].groupby("kfg")["valor"]:
    pass

# union, torsion
print("\nunion (todas):")
print(ci["union"].value_counts().to_string())
print("\ntorsion:")
print(ci["torsion"].value_counts().to_string())
print("\nnivel (profundidad arbol):")
print(ci["nivel"].value_counts().sort_index().to_string())
print("\ncolores top 15:")
print(ci["color"].value_counts().head(15).to_string())

# direccion de nudos
import re
def dirs(s):
    if pd.isna(s): return []
    return re.findall(r"\((?:[\d.]+),([SZU])\)", str(s))
alld = {}
for d in ci["nudos"].dropna():
    for x in dirs(d):
        alld[x] = alld.get(x, 0) + 1
print("\ndirecciones de nudo (racimos):", alld)
