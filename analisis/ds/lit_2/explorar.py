# -*- coding: utf-8 -*-
"""Exploracion basica del corpus para contrastar afirmaciones de la literatura.
Solo lectura de analisis/datos/*.csv; imprime resumenes cortos.
"""
import pandas as pd, numpy as np

D = r"./analisis/datos"
c = pd.read_csv(D + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(D + r"\quipus.csv", low_memory=False)
g = pd.read_csv(D + r"\grupos.csv", low_memory=False)

c["tiene_nudos"] = c["nudos"].notna() & (c["nudos"].astype(str).str.strip() != "")
c["valor_real"] = np.where(c["tiene_nudos"], c["valor"], np.nan)

# --- 1. estructura por quipu ---
n_cuerdas = c.groupby("kfg").size()
n_pend = c[c.nivel == 0].groupby("kfg").size()
n_subs = c[c.nivel > 0].groupby("kfg").size().reindex(n_cuerdas.index, fill_value=0)
max_nivel = c.groupby("kfg")["nivel"].max()
prof = c.groupby("kfg")["nivel"].max()

res = pd.DataFrame({
    "n_cuerdas": n_cuerdas,
    "n_pend": n_pend,
    "n_subs": n_subs,
    "max_nivel": prof,
})
res["prop_subs"] = res.n_subs / res.n_cuerdas

print("=== Estructura por quipu (n=%d) ===" % len(res))
print(res.describe().round(2).to_string())
print("\nMedia cuerdas/quipu: %.1f | mediana: %.0f" % (res.n_cuerdas.mean(), res.n_cuerdas.median()))
print("Media pendientes/quipu: %.1f | mediana: %.0f" % (res.n_pend.mean(), res.n_pend.median()))
print("%% cuerdas que son subsidiarias: %.1f%%" % (100 * res.n_subs.sum() / res.n_cuerdas.sum()))
print("%% de quipus con >=1 subsidiaria: %.1f%%" % (100 * (res.n_subs > 0).mean()))
print("Profundidad maxima observada: %d ; distribucion:" % res.max_nivel.max())
print(res.max_nivel.value_counts().sort_index().to_string())
print("Quipus con 1500+ cuerdas:", int((res.n_cuerdas >= 1500).sum()),
      "| con 1 cuerda:", int((res.n_cuerdas == 1).sum()))

# --- 2. colores ---
col = c["color"].dropna().astype(str)
col = col[~col.isin(["", "nan", "None"])]
print("\n=== Color ===")
print("Cadenas de color distintas (tal cual):", col.nunique())
print("Codigos Ascher simples distintos (split : - /):", len({p for s in col for p in s.replace(":", "-").replace("/", "-").split("-") if p}))
print("Top 12:", col.value_counts().head(12).to_dict())

# --- 3. nudos / direccion ---
import re
def dirs(s):
    if not isinstance(s, str):
        return []
    return re.findall(r"\(([\d.]+),([SZU])\)", s)

D_all = []
for k, s in zip(c.kfg, c.nudos):
    for pos, d in dirs(s):
        D_all.append((k, d))
D_all = pd.DataFrame(D_all, columns=["kfg", "dir"])
print("\n=== Direccion de nudos ===")
print(D_all.dir.value_counts().to_string())
porq = D_all.groupby("kfg")["dir"].agg(lambda x: set(x))
print("Quipus con nudos:", len(porq))
print("Con solo S:", sum(1 for s in porq if s == {"S"}),
      "| solo Z:", sum(1 for s in porq if s == {"Z"}),
      "| ambos S y Z:", sum(1 for s in porq if {"S", "Z"} <= s),
      "| incluye U:", sum(1 for s in porq if "U" in s))
