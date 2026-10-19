"""
Correccion de multiplicidad (Benjamini-Hochberg) sobre la familia de pruebas
pre-especificadas de este informe.

Los p-valores se producen en:
  03_canutos.py, 04_fibra.py, 05_canutos_test.py, 07_fibra_perfil.py,
  08_canuto_color.py, 09_canutito_robusto.py
Aqui solo se reunen y se corrigen.  Se separan dos familias porque responden
preguntas distintas: (A) canutos/canutitos, (B) fibra.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

OUT = os.path.dirname(os.path.abspath(__file__))

canutos = [
    ("A1 prevalencia canuto ~ zona (chi2 perm)", 0.0002, "05"),
    ("A2 canuto ~ num_cords (Mann-Whitney)", 1e-6, "05"),
    ("A3 canuto ~ fibra camelido (Fisher)", 0.0380, "05"),
    ("A4 canuto ~ estilo S (Fisher)", 1.0000, "05"),
    ("A5 UR052 limites canuto = limites grupo (perm)", 0.00005, "05"),
    ("A6 suma redonda por segmento, UR055", 0.008, "05"),
    ("A6 suma redonda por segmento, mejor de 8", 0.056, "05"),
    ("A7 color canuto ~ color cuerdas (mejor de 8)", 0.634, "08"),
    ("A8 canutito ~ valor>0 (AUC, perm)", 0.0075, "09"),
    ("A9 canutito ~ log valor (AUC, perm)", 0.9676, "09"),
    ("A10 canutito ~ blanco (AUC, perm)", 0.0015, "09"),
    ("A11 canutito ~ nivel (AUC, perm)", 0.3469, "09"),
    ("A12 canutito ~ largo (AUC, perm)", 0.00005, "09"),
]
fibra = [
    ("B1 camelido ~ zona (chi2 perm)", 0.0336, "04"),
    ("B2 camelido ~ num_cords (perm)", 0.302, "04"),
    ("B3 camelido ~ colores/cuerda (perm)", 0.138, "04"),
    ("B4 camelido ~ mean_cord_value (perm)", 0.385, "04"),
    ("B5 camelido ~ percent_s_knots (perm)", 0.00005, "04"),
    ("B6 camelido ~ knot_cluster_count (perm)", 0.989, "04"),
    ("B7 tamano estratificado (perm)", 1.000, "04"),
    ("B8 colores/cuerda controlando log n (perm)", 0.335, "07"),
    ("B9 camelido ~ mean_cord_value (MW)", 0.746, "07"),
    ("B10 camelido ~ estilo S (Fisher)", 0.0000079, "07"),
    ("B11 S dentro de Temple Radicati (Fisher)", 0.089, "07"),
    ("B12 KH0281 log valor CL vs CN (perm)", 0.319, "04"),
    ("B13 KH0281 blanco CL vs CN (perm)", 1.000, "04"),
]

for nombre, lista in [("A. CANUTOS Y CANUTITOS", canutos), ("B. FIBRA", fibra)]:
    d = pd.DataFrame(lista, columns=["prueba", "p", "script"])
    d["p_BH"] = stats.false_discovery_control(d.p.values)
    d = d.sort_values("p")
    print("=" * 78)
    print(nombre, "(BH sobre %d pruebas)" % len(d))
    print(d.assign(p=d.p.map(lambda x: "%.2g" % x),
                   p_BH=d.p_BH.map(lambda x: "%.3g" % x)).to_string(index=False))
    d.to_csv(os.path.join(OUT, "pvalores_%s.csv" % nombre[0].lower()), index=False)

print("\nLectura: sobreviven a BH (q<0.05) A1,A2,A5,A8,A10,A12 y B5,B10;")
print("B10 se cae al estratificar por museo (B11), y A4/B7/B9/B13 son negativos limpios.")
