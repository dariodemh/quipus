"""Panorama de ambiguedad de transcripcion en cuerdas.csv (KFG).
Solo lectura de datos; imprime <=40 lineas.
"""
import re
from pathlib import Path
import pandas as pd, numpy as np

RAIZ = Path(__file__).resolve().parents[3]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)

R = re.compile(r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Z])\)(?:,(-?\d+))?$")
d["has_nudos"] = d.nudos != ""

rows = []
for i, s in zip(d.index, d.nudos):
    if not s:
        continue
    for j, k in enumerate(s.split(";")):
        m = R.match(k)
        rows.append((i, j, k, m.group(1) if m else None, m.group(2) if m else "?",
                     m.group(4) if m else "?", m.group(5) if m else None))
c = pd.DataFrame(rows, columns=["i", "j", "raw", "n", "tipo", "dir", "ap"])
print("cuerdas", len(d), "con nudos", d.has_nudos.sum(), "racimos", len(c))
print("\n-- tipos de racimo --")
print(c.tipo.value_counts().to_string())
print("\n-- direcciones --")
print(c.dir.value_counts().to_string())
print("\n-- aporte ausente --", c.ap.isna().sum(), f"({100*c.ap.isna().mean():.2f}%)")
print("-- racimos no parseables --", (c.tipo == "?").sum())
print("\n-- dir U por tipo --")
print(pd.crosstab(c.tipo, c.dir).to_string())
