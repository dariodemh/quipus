# -*- coding: utf-8 -*-
"""Aritmetica interna de UR006 + consulta OKR."""
import pandas as pd, numpy as np, sqlite3, os
BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "k_UR006")
u = pd.read_csv(os.path.join(OUT, "cuerdas_ur006.csv"))

# --- (a) pendiente vs suma de SUS subsidiarias (hijos directos, nivel padre=pend)
u["nudos"] = u["nudos"].fillna("")
sub = u[u.nivel > 0].copy()
print("=== A) pendiente vs suma hijos directos ===")
hits = 0; tested = 0
for code, grp in sub.groupby("padre"):
    par = u[u.cuerda == code]
    if len(par) == 0: continue
    pv = par.valor.iloc[0]
    ssum = grp.valor.sum()
    tested += 1
    if abs(pv - ssum) < 1e-6: hits += 1
print(f"padres con hijos: {tested}; igualdad pendiente=suma hijos: {hits}")

# --- (b) valor unico repetido por quipu ---
print("=== B) valores ===")
p = u[u.nivel == 0]
print("n pendientes:", len(p), " suma valores pendientes:", p.valor.sum())
print("distribucion valores pendientes (top):")
print(p.valor.value_counts().head(12).to_dict())

# --- (c) grupos: suma de pendientes del grupo ---
gsum = u[u.nivel == 0].groupby("grupo_g").valor.agg(["count", "sum"])
print("=== C) grupos grandes (n>=20): suma valores ===")
big = gsum[gsum["count"] >= 20]
print(big.to_string())
print("total suma grupos grandes:", big["sum"].sum())
print("total suma todos pendientes:", gsum["sum"].sum())

# --- OKR ---
print("=== OKR KH0242 ===")
c = sqlite3.connect(os.path.join(BASE, "data", "external", "open-khipu-repository", "data", "khipu.db"))
cur = c.cursor()
cur.execute("PRAGMA table_info(khipu_main)")
cols = [r[1] for r in cur.fetchall()]
cur.execute("SELECT * FROM khipu_main")
allr = cur.fetchall()
idx = {c: i for i, c in enumerate(cols)}
row = None
for r in allr:
    vals = [str(x) for x in r]
    if any("242" in v for v in vals[:3]): row = r
print("cols:", cols)
if row: print("row:", row)
# cords
cur.execute("PRAGMA table_info(cord)")
print("cord cols:", [r[1] for r in cur.fetchall()])
