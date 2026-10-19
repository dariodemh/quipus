# -*- coding: utf-8 -*-
"""Constantes y utilidades comunes. Semilla fija. Solo lectura de datos del repo."""
import numpy as np
import pandas as pd

SEMILLA = 20261018
RNG = np.random.default_rng(SEMILLA)

RAIZ = "../../"          # analisis/ds/n_almacenes -> analisis/
F_UR278 = RAIZ + "13_sistema_incahuasi/ur278_tabla.csv"
F_LIBRO = RAIZ + "13_sistema_incahuasi/libro_consolidado.csv"
F_CUERDAS = RAIZ + "datos/cuerdas.csv"

# --- Anclas arqueologicas (Urton 2017 cap. 9; Urton & Chu 2015) ---
VOL_SITIO_M3 = 6400.0        # capacidad estimada de Qolqawasi en uso
N_CAMARAS = 36               # camaras grandes rectangulares
N_COLCAS = 209               # colcas pequenas cuadradas
N_UNIDADES = N_CAMARAS + N_COLCAS   # 245
CUADROS_UA07 = 3510          # 30 paneles x 117 cuadros de 23x23 cm
LADO_CUADRO_M = 0.23

# --- Densidades aparentes (t/m3) de producto almacenado, rango de literatura ---
# grano suelto / en sacos comprimido / mazorca / mani con cascara / aji seco / chuno
DENS = {
    "maiz_grano":   (0.60, 0.80),
    "maiz_mazorca": (0.25, 0.35),
    "frijol":       (0.65, 0.80),
    "mani_cascara": (0.20, 0.30),
    "aji_seco":     (0.25, 0.40),
    "chuno":        (0.40, 0.55),
    "papa":         (0.60, 0.75),
}

# --- Unidades de carga andinas / coloniales ---
# arroba = 25 libras = 11.5 kg
# carga de llama = 2 arrobas = 23-25 kg (alguna fuente hasta 30)
# costal = saco de Porteo 25-50 kg
# fanega = 55.5 L (1/2 carga); de maiz 41-45 kg
UNIDADES = {
    # nombre: (kg_min, kg_max, litros_min, litros_max)
    "racion_persona_dia": (0.6, 0.8, 0.8, 1.1),
    "arroba":             (11.5, 11.5, 15.0, 16.0),
    "carga_llama":        (23.0, 30.0, 30.0, 40.0),
    "costal_25":          (25.0, 25.0, 33.0, 36.0),
    "fanega":             (41.0, 45.0, 55.5, 55.5),
    "costal_50":          (50.0, 50.0, 66.0, 72.0),
    "cuadro_23cm_10cm":   (1.6, 8.0, 2.6, 10.6),   # 529 cm2 x 5-20 cm de profundidad
}

def leer_ur278():
    d = pd.read_csv(F_UR278)
    cols = [f"c{i}" for i in range(1, 10)]
    d["s9"] = d[cols].sum(axis=1)
    return d, cols

def leer_libro():
    return pd.read_csv(F_LIBRO)
