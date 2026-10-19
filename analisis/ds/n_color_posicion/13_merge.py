# -*- coding: utf-8 -*-
"""13 - Integra los p/q de 999 permutaciones en color_posicion.csv."""
import pandas as pd
from scipy.stats import binom

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
R = pd.read_csv(OUT + r"\color_posicion.csv")
B = pd.read_csv(OUT + r"\bh_999.csv")

idx = R.set_index(["variante", "modelo", "kfg"]).index
B["match"] = B.set_index(["variante", "modelo", "kfg"]).index.isin(idx)
B = B[B.match]
mp = B.set_index(["variante", "modelo", "kfg"])[["p", "q"]]
R = R.set_index(["variante", "modelo", "kfg"])
R.loc[mp.index, "p"] = mp["p"].values
R.loc[mp.index, "q"] = mp["q"].values
R = R.reset_index()
R.to_csv(OUT + r"\color_posicion.csv", index=False)

AG = pd.read_csv(OUT + r"\agregados_final.csv")
for i, row in AG.iterrows():
    g = R[(R.variante == row.variante) & (R.modelo == row.modelo) & R.valido]
    k = int((g.q < .05).sum())
    AG.loc[i, "q05"] = k
    AG.loc[i, "binom_p"] = binom.sf(k - 1, len(g), 0.05)
AG.to_csv(OUT + r"\agregados_final.csv", index=False)
print(AG[["variante", "modelo", "n_valid", "q05", "esperado", "binom_p",
          "r2_abs_med", "p_global", "holm"]].round(4).to_string(index=False))
