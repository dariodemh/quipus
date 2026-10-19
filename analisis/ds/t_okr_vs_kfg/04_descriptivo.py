# -*- coding: utf-8 -*-
"""Estadistica descriptiva de discrepancias KFG vs OKR (mapeo por nombre jerarquico)."""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
MAL = {"KH0197", "KH0227", "KH0267", "KH0350"}
DUP = {"UR196", "MM007_AN002"}
j = j[~j.kfg.isin(MAL | DUP)].copy()

j["tiene_kfg"] = j.nudos.notna()
j["tiene_okr"] = j.valor_okr > 0
j["prefijo"] = j.kfg.str.extract(r"^([A-Z]+)")[0]
j["disc"] = (~j.coincide) & j.tiene_kfg
j["dlargo_ok"] = j.dlargo <= 0.51

cat = pd.crosstab(j.tiene_kfg, j.tiene_okr)
print("categorias (KFG tiene nudos x OKR valor>0):")
print(cat.to_string())
print()
print("total cuerdas KFG emparejadas:", len(j))
print("KFG con nudos:", j.tiene_kfg.sum(), "| OKR con valor>0:", j.tiene_okr.sum())
print("ambos con datos:", (j.tiene_kfg & j.tiene_okr).sum())
print("discrepancias de valor entre ambos:", j.disc.sum(),
      "tasa:", round(j.disc.sum() / (j.tiene_kfg & j.tiene_okr).sum(), 4))
print("KFG nudos pero OKR 0:", (j.tiene_kfg & ~j.tiene_okr).sum())
print("OKR nudos pero KFG vacio:", (~j.tiene_kfg & j.tiene_okr).sum())
print("ambos vacios:", (~j.tiene_kfg & ~j.tiene_okr).sum())
print()
print("prefijos:")
print(j.groupby("prefijo").agg(quipus=("kfg", "nunique"), cuerdas=("kfg", "size"),
                                con_nudos=("tiene_kfg", "sum"), disc=("disc", "sum")).to_string())
