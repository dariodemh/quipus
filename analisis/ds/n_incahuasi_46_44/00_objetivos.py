"""00. Fija los objetivos: filas 2-4 de los bloques de UR269.

Imprime los bloques reconstruidos y guarda ur269_filas.csv y ur269_objetivos.csv.
Dos definiciones de objetivo:
  A) filas 2-4 por posición en bloques de >=5 filas (excluye el bloque doble b4).
  B) todos los registros con cuota explícita 46 o 44 (que por definición son filas 2-4),
     siempre que tengan cabecera >=100.
"""
import numpy as np
import pandas as pd
import comun_n as C

pd.set_option("display.width", 220)
c, q = C.cargar_todo()
F, B = C.registros_ur269(c[c.kfg == "UR269"])
print(F[["bloque", "fila", "tam", "grupo", "cab", "cuota", "vals"]].to_string(index=False))
print("\ntamaños de bloque:", [len(b["filas"]) for b in B])
F.to_csv(C.AQUI / "ur269_filas.csv", index=False)

# A) filas 2-4 en bloques de 5 filas (b4 tiene 8 -> doble, se excluye)
A = F[(F.tam == 5) & F.fila.isin([2, 3, 4])].copy()
A["definicion"] = "A_posicion"
A["orden"] = A.bloque * 10 + A.fila
# B) cuota 46/44 con cabecera
Bq = F[F.cuota.isin([44, 46]) & (F.cab >= 100)].copy()
Bq["definicion"] = "B_cuota"
Bq["orden"] = Bq.bloque * 10 + Bq.fila
O = pd.concat([A, Bq]).sort_values(["definicion", "orden"])
O[["definicion", "orden", "bloque", "fila", "tam", "grupo", "cab", "cuota"]].to_csv(
    C.AQUI / "ur269_objetivos.csv", index=False)
print("\nA) filas 2-4 en bloques de 5:", len(A))
print(A[["bloque", "fila", "grupo", "cab"]].to_string(index=False))
print("\nB) registros con cuota 46/44:", len(Bq))
print(Bq[["bloque", "fila", "grupo", "cab", "cuota"]].to_string(index=False))
