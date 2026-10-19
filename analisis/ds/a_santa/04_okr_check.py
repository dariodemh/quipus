# -*- coding: utf-8 -*-
"""Consulta puntual al OKR (khipu.db) para los 8 quipus. Salida corta."""
import sqlite3, pandas as pd
con = sqlite3.connect(r"./data/external/open-khipu-repository/data/khipu.db")
tabs = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con)["name"].tolist()
print("tablas:", tabs)
khs = ["KH0227","KH0323","KH0324","KH0325","KH0326","KH0327","KH0328","KH0436"]
m = pd.read_sql("SELECT * FROM khipu_main", con)
cols = [c for c in m.columns if c.lower() in ("okr_number","provenance","region","museum_name","attachment_type","top_cord","num_cords","notes") or "prov" in c.lower() or "museum" in c.lower() or "okr" in c.lower()]
print("cols relevantes:", cols)
sub = m[m.apply(lambda r: r.astype(str).str.contains("|".join(khs)).any(), axis=1)]
print(sub[cols].head(12).to_string(index=False))
