# -*- coding: utf-8 -*-
"""Tabla final por quipu: separa discrepancias de valor (largo coincide) de
desalineacion estructural (largo no coincide)."""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
j["prefijo"] = list(j.kfg.str.extract(r"^([A-Z]+)")[0])
j["tiene_kfg"] = j.nudos.notna()
j["largo_ok"] = j.dlargo <= 0.51
j["disc"] = (~j.coincide) & j.tiene_kfg
dup = {"UR196", "MM007_AN002"}
j = j[~j.kfg.isin(dup)].copy()

j["grupo"] = np.select(
    [~j.tiene_kfg,
     j.tiene_kfg & j.largo_ok & j.disc,
     j.tiene_kfg & j.largo_ok & ~j.disc,
     j.tiene_kfg & ~j.largo_ok],
    ["kfg_vacio", "disc_valor", "ok_valor", "desc_estructura"], default="otro")

j["okr_solo"] = (~j.tiene_kfg) & (j.valor_okr > 0)
g = j.groupby("kfg").agg(
    cuerdas=("cuerda", "size"),
    kfg_con_nudos=("tiene_kfg", "sum"),
    n_valor=("grupo", lambda s: (s == "ok_valor").sum() + (s == "disc_valor").sum()),
    disc_valor=("grupo", lambda s: (s == "disc_valor").sum()),
    n_estruct=("grupo", lambda s: (s == "desc_estructura").sum()),
    okr_solo=("okr_solo", "sum"),
)
g["tasa_valor"] = g.disc_valor / g.n_valor.replace(0, np.nan)
g["frac_estruct"] = g.n_estruct / g.cuerdas
g["prefijo"] = list(g.index.str.extract(r"^([A-Z]+)")[0])
g.to_csv(os.path.join(SAL, "por_quipu_final.csv"))

print("cuerdas comparables por valor (largo OK):", int(g.n_valor.sum()))
print("discrepancias de valor:", int(g.disc_valor.sum()),
      "tasa:", round(g.disc_valor.sum() / g.n_valor.sum(), 4))
print("cuerdas con desalineacion de largo:", int(g.n_estruct.sum()),
      "de", int(g.kfg_con_nudos.sum()), "con nudos KFG")
print()
print("=== quipus con tasa_valor > 5% ===")
x = g[(g.tasa_valor > 0.05) & (g.n_valor >= 5)].sort_values("tasa_valor", ascending=False)
print(x[["prefijo", "n_valor", "disc_valor", "tasa_valor", "n_estruct"]].to_string())
print()
print("=== quipus con desalineacion estructural > 20% de sus cuerdas ===")
y = g[(g.frac_estruct > 0.20) & (g.cuerdas >= 5)].sort_values("frac_estruct", ascending=False)
print(y[["prefijo", "cuerdas", "n_estruct", "frac_estruct", "disc_valor", "n_valor"]].to_string())
print()
print("=== por prefijo ===")
p = g.groupby("prefijo").agg(quipus=("cuerdas", "size"), n_valor=("n_valor", "sum"),
                             disc=("disc_valor", "sum"), n_estruct=("n_estruct", "sum"),
                             cuerdas=("cuerdas", "sum"))
p["tasa_valor"] = p.disc / p.n_valor.replace(0, np.nan)
p["frac_estruct"] = p.n_estruct / p.cuerdas
print(p.to_string())
