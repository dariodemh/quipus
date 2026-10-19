# -*- coding: utf-8 -*-
"""
03 · ¿La copia (doble registro fisico) es un rasgo contable o una practica general?
Cruza los 25 pares de copia de 14_copias con los 20 quipus con contabilidad
interna verificable de 08. Prueba exacta de Fisher y version sin Incahuasi
(para separar el efecto "archivo" del efecto "contabilidad").
Salidas: resultados_03.txt
"""
import pandas as pd, os
from scipy import stats
BASE = os.path.dirname(os.path.abspath(__file__))
R14 = os.path.join(BASE, "..", "..", "14_copias")

pares = pd.read_csv(os.path.join(R14, "pares_resumen.csv"))
pares["A"] = pares.A.astype(str); pares["B"] = pares.B.astype(str)
# 13 descubrio 5 parejas estructurales que 14 (basado en valores) no tiene.
nuevos = pd.DataFrame([["UR255","UR267A",28,0.964],["UR256","UR267B",20,1.0],
                       ["UR266","UR275",25,1.0],["UR273A","UR274A",15,1.0],
                       ["UR273B","UR274B",17,1.0]],
                      columns=["A","B","n_alineadas","pct_exacta"])
pares = pd.concat([pares, nuevos], ignore_index=True).drop_duplicates(subset=["A","B"])
en_pares = set(pares.A) | set(pares.B)

contab = {"UR255","UR256","UR266","UR267A","UR267B","UR269","UR270","UR274B","UR275",
          "AS006","AS199","UR118","UR119","UR166",
          "AS001","AS007","QU009","QU015","QU016","UR1152"}
inca = {"UR255","UR256","UR266","UR267A","UR267B","UR269","UR270","UR274B","UR275",
        "UR273A","UR273B","UR274A","UR278","UR268"}
no_inca = contab - inca

def fisher(sub, nombre):
    a = len(sub & en_pares); b = len(sub - en_pares)
    c = len(en_pares - sub); d = 651 - a - b - c
    OR, p = stats.fisher_exact([[a, b], [c, d]])
    print(f"{nombre}: {a}/{len(sub)} con copia vs {c}/{651-len(sub)} fuera; OR={OR:.2f} p={p:.5f}")

print("Pares de copia:", len(pares), "| quipus implicados:", len(en_pares))
fisher(contab, "Contabilidad verificable (20)")
fisher(no_inca, "Contabilidad fuera de Incahuasi (11)")
fisher(inca, "Incahuasi (14)")

# Cuantos pares tocan Incahuasi
pares["inca"] = pares.A.str.startswith(("UR255","UR256","UR266","UR267","UR269","UR270","UR273","UR274","UR275","UR278"))
print("\nPares que tocan el archivo de Incahuasi:", int(pares.inca.sum()), "de", len(pares))
print("Pares fuera de Incahuasi:", int((~pares.inca).sum()))
# Unidad de analisis alternativa: el archivo (procedencia)
q = pd.read_csv(os.path.join(BASE, "..", "..", "datos", "quipus.csv"), usecols=["kfg", "procedencia"])
q["kfg"] = q.kfg.astype(str)
q["copia"] = q.kfg.isin(en_pares)
q["contab"] = q.kfg.isin(contab)
agg = q.groupby("procedencia").agg(n=("kfg", "size"), copias=("copia", "sum"), contab=("contab", "sum"))
agg = agg[(agg.n >= 5) & ((agg.copias > 0) | (agg.contab > 0))].sort_values(["contab", "copias"], ascending=False)
print("\nArchivos con copias y/o contabilidad verificable (n>=5):")
print(agg.to_string())
print("\nArchivos con AMBOS:", int(((agg.copias > 0) & (agg.contab > 0)).sum()), "de", len(agg))
