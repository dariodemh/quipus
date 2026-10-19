# -*- coding: utf-8 -*-
"""Consolida los p-valores de todas las convenciones y aplica Holm global
(26 pruebas primarias). Genera resultados_globales.csv y un resumen legible."""
import numpy as np
import pandas as pd
from utils import holm

files = {
    "torsion": "res_torsion.csv",
    "direccion": "res_direccion.csv",
    "subsidiarias": "res_subsidiarias.csv",
    "color": "res_color_global.csv",
    "canutos": "res_canutos.csv",
}
primary = {
    "torsion": ["T1", "T2", "T3", "T4", "T5"],
    "direccion": ["D1", "D2", "D2b", "D2c", "D3", "D3b", "D4", "D5"],
    "subsidiarias": ["S1", "S2", "S3", "S4", "S5"],
    "color": ["C1", "C2", "C3c"],
    "canutos": ["K1", "K2", "K3", "K4", "K5"],
}
rows = []
for fam, tests in primary.items():
    d = pd.read_csv(files[fam])
    d = d[d.test.isin(tests)].copy()
    d["familia"] = fam
    rows.append(d)
R = pd.concat(rows, ignore_index=True)
R["q_global"] = holm(R.p.values)
for fam in primary:
    m = R.familia == fam
    R.loc[m, "q_familia"] = holm(R.loc[m, "p"].values)
R["sig_global"] = R.q_global < 0.05
R = R.sort_values(["familia", "p"])
R.to_csv("resultados_globales.csv", index=False, encoding="utf-8-sig")
pd.set_option("display.width", 200)
print(R[["familia", "test", "descripcion", "obs", "null_mean", "efecto_z",
         "p", "q_familia", "q_global", "sig_global"]].round(4).to_string(index=False))
print("\nPruebas primarias:", len(R), "| significativas tras Holm global:",
      int(R.sig_global.sum()))
