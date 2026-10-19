"""Panorama del corpus para el mapa de legibilidad. Solo imprime resumenes."""
import pandas as pd, numpy as np
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "datos"
c = pd.read_csv(D / "cuerdas.csv", dtype={"kfg": str, "cuerda": str, "padre": str, "nudos": str})
q = pd.read_csv(D / "quipus.csv", dtype={"kfg": str})

# valor valido: 0 con nudos vacio = ausente
c["nudos"] = c["nudos"].fillna("")
c["pres"] = ~((c["valor"] == 0) & (c["nudos"].str.strip() == ""))
print("cuerdas", len(c), "quipus", c.kfg.nunique())
print("con valor", c.pres.sum(), "sin valor", (~c.pres).sum())
print("\nnivel:\n", c.nivel.value_counts().sort_index())
print("\nunion:\n", c.union.fillna("?").value_counts().head(10))
print("\nquipus por tamano (cuerdas):")
s = c.groupby("kfg").size()
print(s.describe().round(1))
print("quipus con >=1 subsidiaria:", c[c.nivel > 0].kfg.nunique())
print("quipus con >=1 T:", c[c.union == "T"].kfg.nunique())
print("quipus con >=1 padre con >=2 hijas:",
      c[c.nivel > 0].groupby(["kfg", "padre"]).size().loc[lambda x: x >= 2].reset_index().kfg.nunique())

print("\nprocedencia (top 15):")
print(q.procedencia.fillna("?").value_counts().head(15))
print("n procedencias distintas:", q.procedencia.nunique())
print("\nregion:")
print(q.region.fillna("?").value_counts().head(10))

# grupos
g = pd.read_csv(D / "grupos.csv", dtype={"kfg": str})
print("\ngrupos filas", len(g), "cols", list(g.columns))
print(g.head(3).to_string())
