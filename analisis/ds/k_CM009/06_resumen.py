# -*- coding: utf-8 -*-
"""CM009: resumen de cifras y corrección de Holm para la familia de tests globales."""
import numpy as np

def holm(ps):
    order = np.argsort(ps); m = len(ps); adj = [0.0] * m; prev = 0.0
    for rank, i in enumerate(order):
        val = min(1.0, (m - rank) * ps[i]); prev = max(prev, val); adj[i] = prev
    return adj

names = ["color lag4 (periodicidad de color)",
         "valor lag20 (nulo color-preservado)",
         "patrón de nudo lag20",
         "sumas contiguas de >=2 cuerdas",
         "valores repetidos",
         "valor lag4 (nulo color-preservado)"]
p = [0.0010, 0.0010, 0.0010, 0.3317, 1.0000, 0.1249]
adj = holm(p)
print("Familia A (patrones globales, Holm, m=6):")
for nm, pp, aa in zip(names, p, adj):
    print(f"  {nm:45s} p={pp:.4f}  p_holm={aa:.4f}  {'SIG' if aa<0.05 else 'ns'}")

print("\nCifras clave:")
print("  65 cuerdas colgantes, nivel 0, largo 45 cm, sin subsidiarias, sin cuerdas superiores.")
print("  colores: W=17, AB=16, GG=16, W:KB=16; ciclo estricto W,AB,GG,W:KB desde p6.")
print(f"  valor total = 3486; media = {3486/65:.1f}; 15 cuerdas sin nudo (23 por ciento).")
print("  15 registros de 4 cuerdas (W,AB,GG,W:KB) + cabecera de 5.")
print("  3 valores W grandes: 1213 (rec5), 1236 (rec10), 459 (rec15).")
print("  W!=AB+GG+W:KB en 0/15 registros -> sin aritmética interna.")
print("  Spearman W-AB=0.95, W-GG=0.88, W-W:KB=0.83, AB-GG=0.86 (n=15, p<0.001).")
