# -*- coding: utf-8 -*-
"""01. Estructura interna de UR278 y granularidad de las cifras.

No decide la unidad; comprueba si las cifras se comportan como recuentos
de lotes estandarizados (pares, decenas, veintenas) o como cuentas continuas.
"""
import numpy as np, pandas as pd, json
from comun import leer_ur278, leer_libro, RNG, F_LIBRO

d, cols = leer_ur278()
V = d[cols].values.astype(float)
vals = V[~np.isnan(V)]

print("=== 1. Totales ===")
print(f"filas={len(d)}  celdas={int((~np.isnan(V)).sum())}  suma 9 columnas={np.nansum(V):.0f}")
print(f"suma columna 'total'={d.total.sum():.0f} (incluye cuerdas 10 y 12 de g18 y g32)")
print(f"media celda={vals.mean():.1f}  mediana={np.median(vals):.0f}  min={vals.min():.0f}  max={vals.max():.0f}")
print(f"suma por fila: min={d.s9.min():.0f} max={d.s9.max():.0f} mediana={d.s9.median():.0f}")
print("suma por columna:", dict(zip(cols, np.nansum(V, axis=0).astype(int))))

print("\n=== 2. Granularidad de las celdas ===")
def frac_mod(x, m):
    return float(np.mean(np.isclose(x % m, 0)))

for m, esperado in [(2, 0.5), (5, 0.2), (10, 0.1), (25, 0.04), (50, 0.02)]:
    o = frac_mod(vals, m)
    # nulo: cualquier entero 0..m-1 igual de probable
    B = 20000
    sim = (RNG.integers(0, m, size=(B, len(vals))) == 0).mean(axis=1)
    p = (np.sum(sim >= o) + 1) / (B + 1)
    print(f"multiplos de {m:2d}: obs={o:.3f}  esperado={esperado:.3f}  p(una cola, mayor)={p:.4f}")

print("\n=== 3. Ultimo digito de las celdas ===")
u = (vals.astype(int) % 10)
tab = np.bincount(u, minlength=10) / len(u)
print("digito 0..9:", " ".join(f"{t:.3f}" for t in tab))
# chi2 contra uniforme
chi2 = ((np.bincount(u, minlength=10) - len(u) / 10) ** 2 / (len(u) / 10)).sum()
from scipy.stats import chi2 as chi2d
print(f"chi2={chi2:.1f} gl=9 p={chi2d.sf(chi2, 9):.4f}")

print("\n=== 4. Tamano relativo de las 9 columnas (control de particion) ===")
prop = V / np.nansum(V, axis=1, keepdims=True)
med = np.nanmedian(prop, axis=0)
print("mediana de la proporcion por columna:", " ".join(f"{m:.3f}" for m in med))
print(f"CV entre columnas={np.std(med, ddof=1)/np.mean(med):.3f}  max/min={med.max()/med.min():.2f}")

print("\n=== 5. Libro consolidado: totales por quipu ===")
L = leer_libro()
g = L.groupby("quipu").agg(n=("cabecera", "size"), suma=("cabecera", "sum"),
                           media=("cabecera", "mean"), mn=("cabecera", "min"),
                           mx=("cabecera", "max"))
print(g.round(0).to_string())

# guardar
d.to_csv("ur278_filas.csv", index=False)
json.dump({"suma_9col": float(np.nansum(V)), "n_filas": int(len(d)),
           "media_celda": float(vals.mean()), "mediana_celda": float(np.median(vals)),
           "suma_por_columna": [float(x) for x in np.nansum(V, axis=0)]},
          open("resumen_ur278.json", "w"), ensure_ascii=False, indent=1)
print("\nOK -> ur278_filas.csv, resumen_ur278.json")
