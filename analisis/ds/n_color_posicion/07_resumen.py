# -*- coding: utf-8 -*-
"""07 - Resumenes para el informe a partir de color_posicion.csv."""
import numpy as np
import pandas as pd

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
R = pd.read_csv(OUT + r"\color_posicion.csv")
AG = pd.read_csv(OUT + r"\agregados.csv")

print("=== por variante/modelo ===")
for (v, m), g in R.groupby(["variante", "modelo"]):
    print(f"{v:14s} {m}: n={len(g):3d} p<.05 bruto={int((g.p<.05).sum()):3d} "
          f"q<.05={int((g.q<.05).sum()):3d} r2med={g.r2.median():.4f} "
          f"r2*pos={ (g.r2*(1-g.r2_pos)).median():.4f} "
          f"W>0={ (g.ef_W>0).mean():.2f} ef_rango={g.ef_rango.median():.3f}")

print("\n=== consistencia de direccion (modelo B, primario) ===")
g = R[(R.variante == "primario") & (R.modelo == "B")]
print("quipus con W>resto:", int((g.ef_W > 0).sum()), "/", int(g.ef_W.notna().sum()),
      "| mediana ef_W %.3f" % g.ef_W.median())
print("correlacion r2 A vs B (primario):",
      round(R[(R.variante == 'primario') & (R.modelo == 'A')].set_index('kfg').r2.corr(
          R[(R.variante == 'primario') & (R.modelo == 'B')].set_index('kfg').r2), 3))

print("\n=== top quipus por r2 parcial (primario, B) ===")
g = R[(R.variante == "primario") & (R.modelo == "B")].sort_values("r2", ascending=False)
print(g[["kfg", "n", "ngrupos", "npos_var", "C", "df1", "df2", "r2", "r2_pos",
         "ef_rango", "ef_W", "p", "q", "copia"]].head(12).round(3).to_string(index=False))

print("\n=== top quipus por r2 parcial (primario, A) ===")
g = R[(R.variante == "primario") & (R.modelo == "A")].sort_values("r2", ascending=False)
print(g[["kfg", "n", "ngrupos", "npos_var", "C", "r2", "r2_pos", "ef_rango", "ef_W",
         "p", "q", "copia"]].head(12).round(3).to_string(index=False))

print("\n=== agregados ===")
print(AG.round(4).to_string(index=False))
