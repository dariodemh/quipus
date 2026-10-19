# -*- coding: utf-8 -*-
"""Define la cohorte de costa central de Lima y describe el conjunto."""
import pandas as pd, numpy as np, re

BASE = r"."
q = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
g = pd.read_csv(BASE + r"\analisis\datos\grupos.csv")

# Procedencias objetivo (costa central de Lima)
PAT = "Armatambo|Huaquerones|near Lima|Chancay|Huacho|Chuquitanta|Marquez"
q["proc"] = q["procedencia"].astype(str)
sel = q[q["proc"].str.contains(PAT, case=False, na=False)].copy()
print("N quipus cohorte:", len(sel))
print(sel["procedencia"].value_counts().to_string())

# Duplicados por OKR (dos nombres del mismo objeto)
sel["okr_norm"] = sel["okr"].astype(str).str.strip()
dups = sel[sel.duplicated("okr_norm", keep=False)].sort_values("okr_norm")
print("\nPosibles duplicados por OKR:")
print(dups[["kfg", "okr", "procedencia", "museo"]].to_string())

# Etiqueta normalizada de sitio (agrupa variantes de procedencia)
def sitio(p):
    p = str(p).lower()
    if "armatambo" in p or "san pedro" in p: return "Armatambo"
    if "huaquerones" in p: return "Huaquerones"
    if "marquez" in p: return "Marquez"
    if "huacho" in p: return "Huacho"
    if "chancay" in p or "huando" in p: return "Chancay"
    if "lima" in p: return "near Lima"
    if "chuquitanta" in p: return "Chuquitanta"
    return "?"
sel["sitio"] = sel["procedencia"].map(sitio)

# Guardar cohorte
sel.to_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv", index=False)

# Cuerdas de la cohorte
cc = c[c["kfg"].isin(sel["kfg"])].copy()
print("\nN cuerdas cohorte:", len(cc))
print("\nResumen por quipu:")
g2 = cc.groupby("kfg").agg(n_cuerdas=("cuerda", "size")).reset_index()
print(g2.describe().to_string())
