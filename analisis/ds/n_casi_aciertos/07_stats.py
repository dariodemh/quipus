# -*- coding: utf-8 -*-
"""Cifras de apoyo para el informe (binomiales y patrones)."""
import os
import pandas as pd
import numpy as np
from scipy.stats import binom, hypergeom

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")
c = pd.read_csv(os.path.join(OUT, "subset_cuerdas.csv"), dtype={"valor": float, "largo": float})

# --- UR274B: cuotas 17 vs 10 ---
x = c[(c.kfg == "UR274B") & (c.nivel == 0) & (c.valor.isin([10, 17]))]
n10, n17 = int((x.valor == 10).sum()), int((x.valor == 17).sum())
p_om = 2.59e-4                       # tasa de racimo omitido por cuerda (catalogo, resto)
print("UR274B cuotas: 10 =", n10, " 17 =", n17, " otras =", 19-n10-n17)
print("  P(>=4 omisiones en 19 cuerdas | p=2.6e-4) =", binom.sf(n10 - 1, n10 + n17, p_om))
print("  P(las 4 cuerdas mas cortas sean justo las 4 de valor 10) =", 1 / hypergeom.pmf(4, n10 + n17, 4, 4), "  (1/C(16,4))")
print("  largos: 10 ->", sorted(x[x.valor == 10].largo.round(1)), " 17 -> min", x[x.valor == 17].largo.min())

# --- UR275 p51 ---
y = c[(c.kfg == "UR275") & (c.nivel == 0) & (c.valor == 47)]
print("\nUR275 cuotas 47: n =", len(y), " largo min =", y.largo.min(), " mediana =", y.largo.median())
print("  p51 largo = 26.5; P(>=1 omision en 25 cuerdas) =", binom.sf(0, 25, p_om))

# --- patron columna 1 ---
print("\nPatron columna 1 (2 filas 9/9): P(misma columna | azar) = 1/9 =", round(1 / 9, 3))
print("  P(misma columna y mismo signo) = 1/18 =", round(1 / 18, 3))
print("  Holm x4 pruebas de patron =", round(min(1, 4 * 1 / 18), 3))

# --- g12 ladder ---
print("\ng12: UR269 p181 = 2433 (4 cientos), UR278 fila = 2533 (5), UR266 p64 = UR275 p41 = 2633 (6)")

# --- reparabilidad global ---
S = pd.read_csv(os.path.join(OUT, "resumen_relaciones.csv"))
v = S[S.residual.notna()]
print(f"\nRelaciones: {len(S)} | con destino: {len(v)} | reparables 1 edicion: {(v.n_ediciones>0).sum()}")
print(f"Candidatas por relacion: mediana {v.n_ediciones.median():.0f}, media {v.n_ediciones.mean():.1f}")
print(f"p_nulo medio: {v.p_nulo_relacion.mean():.3f} (prob. de que una relacion aleatoria sea reparable)")

cat = pd.read_csv(os.path.join(OUT, "catalogo_cuerdas.csv"))
cat["pref"] = cat.kfg.str[:2]
tot = 35223
OUTL = {"UR090", "UR144", "UR235", "UR193", "UR190"}
resto = cat[~cat.kfg.isin(OUTL)]
tab = cat.tipo_error.value_counts().rename("n").to_frame()
tab["pct"] = (tab.n / len(cat) * 100).round(1)
tab["por_1000_global"] = (tab.n / tot * 1000).round(3)
tab["n_resto"] = resto.tipo_error.value_counts()
tab["por_1000_resto"] = (tab.n_resto / 34729 * 1000).round(4)
tab.to_csv(os.path.join(OUT, "catalogo_tipos.csv"))
print("\nCatalogo por tipo:"); print(tab.fillna(0).to_string())
print("\nPor prefijo:"); print(cat.pref.value_counts().to_string())
