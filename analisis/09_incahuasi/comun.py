"""Carga comun para analisis/09_incahuasi. Valor 0 sin nudos = cuerda ausente."""
import numpy as np, pandas as pd
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "analisis/datos"
OUT = Path(__file__).resolve().parent
def cargar():
    c = pd.read_csv(D/"cuerdas.csv", low_memory=False, keep_default_na=False)
    q = pd.read_csv(D/"quipus.csv", keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    return c, q
def incahuasi(q):
    return [k for k in q.kfg if q.set_index("kfg").loc[k,"procedencia"]=="Incahuasi"]
