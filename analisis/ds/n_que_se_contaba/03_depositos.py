"""03. Arqueologia de depositos: ¿que magnitudes fisicas admiten las cifras?

Anclas (Urton 2017, cap. 9; Urton y Chu 2015):
  Qolqawasi (Inkawasi): 6 estructuras al norte (4 kallankas + 2 espacios de
  clasificacion), 36 camaras grandes, 209 colcas pequenas; ~6 400 m3.
  34 quipus. Cuadriculas de 23 x 23 cm en U.A. 07 (paneles 3 x 39, ~30 paneles
  = ~3 510 cuadros).
  Cabeceras del flujo 47 (UR266/UR269/UR275): mediana 2 000, p5-p95 482-3 317,
  max 4 273. UR278: 28 filas x 9 columnas conservadas = 61 790 unidades.

Se calcula, para cada hipotesis de unidad, la masa y el volumen de:
  - una cabecera mediana (2 000 unidades),
  - el archivo UR278 completo (61 790),
  - la cuota fija 47.
y se compara con los 6 400 m3 y con una colca media (6 400/245 = 26 m3).
Densidad aparente central 0,6 t/m3 (rango 0,3-0,8).
"""
import numpy as np
import pandas as pd
import comun as C

CAP_M3 = 6400.0
N_BINS = 209 + 36          # colcas pequenas + camaras grandes
M3_BIN = CAP_M3 / N_BINS   # 26,1 m3
DENS = 0.6                 # t/m3
CAB = 2000                 # cabecera mediana
TOT = 61790                # UR278
CUOTA = 47

# unidad: (masa kg, nota)
UNIDADES = [
    ("grano de maiz", 0.0003, "0,3 g"),
    ("grano de frijol", 0.0004, "0,4 g"),
    ("mani en cascara", 0.0008, "0,8 g"),
    ("aji seco", 0.005, "5 g"),
    ("aji fresco", 0.015, "15 g"),
    ("papa", 0.10, "100 g"),
    ("mazorca de maiz", 0.25, "250 g"),
    ("kilogramo", 1.0, "unidad de masa"),
    ("arroba", 11.5, "11,5 kg"),
    ("carga de llama", 30.0, "30 kg"),
    ("costal / saco", 25.0, "25 kg"),
    ("costal grande", 50.0, "50 kg"),
    ("fanega de maiz", 45.0, "~55 L"),
]

filas = []
for nombre, kg, nota in UNIDADES:
    for etiqueta, n in [("cabecera", CAB), ("UR278", TOT), ("cuota 47", CUOTA)]:
        masa_t = n * kg / 1000
        vol_m3 = masa_t / DENS
        filas.append(dict(unidad=nombre, nota=nota, magnitud=etiqueta, n=n,
                          masa_t=masa_t, vol_m3=vol_m3,
                          frac_cap=vol_m3 / CAP_M3,
                          bins_equiv=vol_m3 / M3_BIN,
                          cargas_llama=masa_t * 1000 / 30))
D = pd.DataFrame(filas)

print("=== Capacidad del deposito ===")
print("Qolqawasi: %.0f m3; %d unidades de almacenamiento; media %.1f m3/unidad" %
      (CAP_M3, N_BINS, M3_BIN))
print("Masa almacenable a %.1f t/m3: %.0f t" % (DENS, CAP_M3 * DENS))

print("\n=== Cabecera mediana (2 000 unidades) segun unidad ===")
p = D[D.magnitud == "cabecera"].copy()
p["% capacidad"] = 100 * p.frac_cap
print(p[["unidad", "nota", "masa_t", "vol_m3", "% capacidad", "bins_equiv", "cargas_llama"]]
      .round(3).to_string(index=False))

print("\n=== UR278 completo (61 790 unidades) ===")
p = D[D.magnitud == "UR278"].copy()
p["% capacidad"] = 100 * p.frac_cap
print(p[["unidad", "nota", "masa_t", "vol_m3", "% capacidad", "bins_equiv", "cargas_llama"]]
      .round(3).to_string(index=False))

print("\n=== Cuota fija 47 ===")
p = D[D.magnitud == "cuota 47"].copy()
print(p[["unidad", "masa_t", "vol_m3", "cargas_llama"]].round(4).to_string(index=False))

# sensibilidad a la densidad (solo UR278, unidades limite)
print("\n=== Sensibilidad a la densidad aparente (UR278) ===")
for nombre, kg in [("mazorca de maiz", .25), ("kilogramo", 1.), ("carga de llama", 30.), ("costal", 25.), ("costal grande", 50.)]:
    v = TOT * kg / 1000 / np.array([0.3, 0.6, 0.8])
    print("%-16s volumen %.0f-%.0f m3 = %.1f-%.1f %% de 6 400" %
          (nombre, v.min(), v.max(), 100 * v.min() / CAP_M3, 100 * v.max() / CAP_M3))

# coherencia con la cuadricula de clasificacion
print("\n=== Cuadricula de 23 x 23 cm (U.A. 07) ===")
print("~3 510 cuadros; superficies 23x23 cm = 529 cm2")
for h_cm in (5, 10, 20):
    vol_l = 23 * 23 * h_cm / 1000
    kg = vol_l / 1000 * DENS * 1000
    print("  altura %2d cm: %.1f L por cuadro, %.2f kg de maiz; 2 000 unidades = %.0f kg" %
          (h_cm, vol_l, kg, CAB * kg))
print("  3 510 cuadros x 2,0 kg (10 cm) = %.1f t; x 4,1 kg (20 cm) = %.1f t" %
      (3510 * 2.0 / 1000, 3510 * 4.1 / 1000))

# coincidencias estructurales (marcar como especulativas)
print("\n=== Coincidencias estructurales (especulativo) ===")
print("UR278: 28 filas x 9 columnas = %d celdas; deposito: %d colcas/camaras" %
      (28 * 9, N_BINS))
print("UR278: 33 registros x 9 = %d celdas (si se conservaran las 33 filas)" % (33 * 9))
print("celda media UR278 = %.0f unidades; colca media = %.1f m3 = %.0f kg = %.0f costales de 25 kg" %
      (TOT / 249, M3_BIN, M3_BIN * DENS * 1000, M3_BIN * DENS * 1000 / 25))

D.to_csv(C.OUT / "depositos_unidades.csv", index=False)
print("\nguardado depositos_unidades.csv")
