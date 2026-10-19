# -*- coding: utf-8 -*-
"""Discrepancias por quipu y por investigador (prefijo), con controles."""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
j["prefijo"] = j.kfg.str.extract(r"^([A-Z]+)")[0]
j["tiene_kfg"] = j.nudos.notna()
j["disc"] = (~j.coincide) & j.tiene_kfg
j["dlargo_mal"] = (j.dlargo > 0.51)
j["okr_solo"] = (~j.tiene_kfg) & (j.valor_okr > 0)

# UR196 y MM007 tienen cuerdas duplicadas en el propio KFG: fuera de tasas
dup_kfg = {"UR196", "MM007_AN002"}
jj = j[~j.kfg.isin(dup_kfg)]

g = jj.groupby("kfg").agg(
    quipu_n_cuerdas=("cuerda", "size"),
    n_con_nudos=("tiene_kfg", "sum"),
    disc=("disc", "sum"),
    dlargo_mal=("dlargo_mal", "sum"),
    okr_solo=("okr_solo", "sum"),
    dlargo_med=("dlargo", "median"),
)
g["tasa"] = g.disc / g.n_con_nudos.replace(0, np.nan)
g["frac_largo_mal"] = g.dlargo_mal / g.quipu_n_cuerdas
g["prefijo"] = list(g.index.str.extract(r"^([A-Z]+)")[0])
g.to_csv(os.path.join(SAL, "por_quipu.csv"))

print("quipus con cuerdas comparables:", (g.n_con_nudos > 0).sum())
print("quipus con >5% discrepancias:", ((g.tasa > 0.05)).sum())
print("de ellos con >=10 cuerdas con nudos:", ((g.tasa > 0.05) & (g.n_con_nudos >= 10)).sum())
print()
cols = ["prefijo", "n_con_nudos", "disc", "tasa", "frac_largo_mal", "okr_solo", "dlargo_med"]
print(g[g.tasa > 0.05].sort_values("tasa", ascending=False)[cols].to_string())
print()
print("=== por prefijo (agregado de cuerdas) ===")
p = g.groupby("prefijo").agg(quipus=("n_con_nudos", "size"),
                             cuerdas=("n_con_nudos", "sum"),
                             disc=("disc", "sum"),
                             okr_solo=("okr_solo", "sum"),
                             largo_mal=("dlargo_mal", "sum"))
p["tasa"] = p.disc / p.cuerdas
print(p.to_string())
