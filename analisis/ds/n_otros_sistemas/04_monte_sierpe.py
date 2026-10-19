# -*- coding: utf-8 -*-
"""
04 · Monte Sierpe frente a Incahuasi: que se puede y que no se puede comparar.
Datos del articulo (Bongers et al. 2025, Antiquity 100, doi 10.15184/aqy.2025.10237)
y de su OSM: ~5200 hoyos, >=60 secciones; seccion a = >=9 filas de 8 hoyos;
seccion b = 6 filas de 7 + 1 de 8 = 50; seccion c = 12+ filas alternando 7/8,
conteos diagonales 1,3,5,7,9,11,11,14,12,10,8,6,4,2,1 (OSM Fig. S40).
Salidas: resultados_04.txt
"""
import numpy as np
rng = np.random.default_rng(20261018)

HOLES, SECCIONES = 5200, 60
print(f"Hoyos/seccion (si 60 secciones): {HOLES/SECCIONES:.1f}")
print(f"Si fueran 65 secciones: {HOLES/65:.1f}; si 70: {HOLES/70:.1f}")

diag = np.array([1,3,5,7,9,11,11,14,12,10,8,6,4,2,1])
print("\nDiagonales seccion c: n=", len(diag), "suma=", diag.sum(), "media=", round(diag.mean(),2))
print("Perfil unimodal:", bool(np.all(np.diff(diag[:8]) >= 0) and np.all(np.diff(diag[7:]) <= 0)))
print("Si la serie cubre toda la seccion, la suma de diagonales (104) = numero de hoyos.")

# Nulo: rachas de 9 filas iguales en 60 secciones de ~11 filas, anchos 7/8
def racha_max(x):
    best = cur = 1
    for i in range(1, len(x)):
        cur = cur + 1 if x[i] == x[i-1] else 1
        best = max(best, cur)
    return best
sims = []
for _ in range(20000):
    hay = False
    for _s in range(SECCIONES):
        n = rng.integers(8, 14)  # 8-13 filas por seccion
        w = rng.integers(7, 9, n)  # 7 u 8 hoyos
        if racha_max(w) >= 9:
            hay = True; break
    sims.append(hay)
print(f"\nP(>=1 racha de 9 filas iguales en 60 secciones, anchos 7/8 al azar) = {np.mean(sims):.3f}")

# Comparacion con cuotas de Incahuasi
cuotas = {10,15,17,25,30,44,46,47,208}
obs = {"a":72, "b":50, "c":int(diag.sum()), "media":HOLES/SECCIONES}
print("\nNumeros de Monte Sierpe frente a cuotas de Incahuasi:")
for k,v in obs.items():
    hits = [c for c in cuotas if c == round(v)]
    print(f"  {k}: {v:.1f} -> coincidencia exacta: {hits if hits else 'ninguna'}")
print("  50 = 2 x 25 (multiplo trivial). 104 = 2 x 52; 72 = 8 x 9; 86.7 ~ 9 x 9.6")
# Nulo de coincidencia exacta: 4 numeros U(10,210) contra 9 cuotas
sims2 = []
for _ in range(20000):
    nums = rng.integers(10, 211, 4)
    sims2.append(any(n in cuotas for n in nums))
print(f"P(>=1 coincidencia exacta si los 4 numeros fueran U(10,210)) = {np.mean(sims2):.3f}")

# El quipu citado por el articulo (VA16135) no esta en KFG
print("\nVA16135a/b (Berlin) citado por el articulo: 80 grupos de 10-12 cuerdas.")
print("En KFG/OKR no aparece: la comparacion con ese quipu no se puede replicar aqui.")
