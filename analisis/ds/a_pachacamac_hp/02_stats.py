"""Estadisticas detalladas del conjunto HP001-HP032."""
import pandas as pd
import numpy as np
import re

RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
g = pd.read_csv(RAIZ + "analisis/datos/grupos.csv")
HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()
hpg = g[g.kfg.isin(HP)].copy()

def nn(s):
    return s.notna() & (s != "") & (s != "[]")

print("=== torsion (todas las cuerdas HP) ===")
print(hp.torsion.value_counts(dropna=False).to_string())
print("=== union ===")
print(hp.union.value_counts(dropna=False).to_string())
print("=== terminacion ===")
print(hp.terminacion.value_counts(dropna=False).head(15).to_string())
print("=== nivel ===")
print(hp.nivel.value_counts(dropna=False).to_string())

# color codes (limpiar separadores)
print("=== color top 25 ===")
col = hp.color.dropna().astype(str)
print(col.value_counts().head(25).to_string())
print("n colores distintos:", col.nunique())

# colores basicos (primer token)
def base_col(s):
    s = str(s)
    m = re.findall(r"[A-Z]{1,3}", s)
    return m[0] if m else "?"
hp["cbase"] = hp.color.map(base_col)
print("=== color base (primer token) top 15 ===")
print(hp.cbase.value_counts().head(15).to_string())

# direccion de nudo desde nudos: buscar S/Z en los racimos
def dirs(s):
    if not nn(pd.Series([s])).iloc[0] if False else True:
        pass
    s = "" if pd.isna(s) else str(s)
    return re.findall(r"\d+[SLE](?:E|L)?\([\d.]+,([SZU])\)", s)
hp["dirs"] = hp.nudos.map(lambda s: ",".join(dirs(s)))
from collections import Counter
cnt = Counter()
for d in hp.dirs:
    for x in d.split(","):
        if x:
            cnt[x] += 1
print("=== direcciones de nudo (racimos) ===", dict(cnt))

# nudos por tipo
def tipos(s):
    s = "" if pd.isna(s) else str(s)
    return re.findall(r"\d+([SLE]+)\(", s)
cnt2 = Counter()
for t in hp.nudos.map(tipos):
    for x in t:
        cnt2[x] += 1
print("=== tipos de racimo ===", dict(cnt2.most_common(12)))

# valores: distribucion
v = pd.to_numeric(hp.loc[nn(hp.nudos), "valor"], errors="coerce").dropna()
print("=== valores HP ===")
print("n con valor:", len(v), "min", v.min(), "max", v.max(), "median", v.median())
print("top 15 valores:")
print(v.value_counts().head(15).to_string())
print("multiplos de 10:", (v % 10 == 0).mean().round(3), "| terminan en 5:", (v % 10 == 5).mean().round(3))

# grupos
print("=== grupos: n por quipu ===")
gg = hpg.groupby("kfg").agg(n_grupos=("grupo", "nunique"),
                            max_pos=("pos_cm", "max"),
                            n_con_espacio=("espacio_cm", lambda x: (pd.to_numeric(x, errors="coerce") > 0).sum()))
print(gg.to_string())
