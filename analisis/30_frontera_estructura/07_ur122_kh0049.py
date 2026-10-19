"""Seguimiento post hoc (fuera del diseno congelado) de la fila T6 de UR122: totales por columna.
UR122 (frontera, Goteborg) es copia parcial de KH0049 (Lima; 04/14). Se prueba en KH0049, completa, si sus bloques
de 18 colgantes forman una tabla jerarquica: B0 = B1 + B2 y B1 = B3 + B4 + B5 (posicion a posicion).
Nulo: permutar las posiciones de un sumando (B2, o B5) dentro de su bloque; 20 000 replicas.
Uso: python 07_ur122_kh0049.py"""
import numpy as np
from comun import *

rng = np.random.default_rng(SEMILLA)
v = quipu("KH0049").v; B = [v[i * 18:(i + 1) * 18] for i in range(6)]
u = quipu("UR122").v; U = [u[i * 18:(i + 1) * 18] for i in range(4)]
ex = lambda a, b: int(((a == b) & (a > 0)).sum())
for nombre, tot, partes in [("B0 = B1 + B2", B[0], [B[1], B[2]]), ("B1 = B3 + B4 + B5", B[1], [B[3], B[4], B[5]])]:
    obs = ex(tot, sum(partes))
    z = np.array([ex(tot, sum(partes[:-1]) + rng.permutation(partes[-1])) for _ in range(20000)])
    print(f"KH0049 {nombre}: {obs}/18 exactas; nulo media {z.mean():.2f}, max {z.max()}; p = {(np.sum(z >= obs) + 1) / 20001:.1e}")
    print("   diferencias:", list(map(int, tot - sum(partes))))
print("UR122 bloque j coincide (exacto, >0) con KH0049 bloque k:")
for i in range(4): print("  UR122 B%d:" % i, [ex(U[i], B[k]) for k in range(6)])
print("UR122 B0 - (B1+B2+B3):", list(map(int, U[0] - (U[1] + U[2] + U[3]))))
print("Discrepancia compartida: KH0049 B1[1] =", B[1][0], "UR122 B0[1] =", U[0][0], "; B3+B4+B5 =", int(B[3][0] + B[4][0] + B[5][0]),
      "; B0[1] - B2[1] =", int(B[0][0] - B[2][0]))
