"""Utilidades comunes para lit_5 (extracción y verificación de afirmaciones).

Reglas del brief:
- unidad de análisis = quipu (permutaciones dentro de cada quipu o agregación por quipu)
- valor 0 con `nudos` vacío = ausente, no cero
- semilla fija
"""
import os
import sqlite3
import numpy as np
import pandas as pd

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATOS = os.path.join(RAIZ, "analisis", "datos")
OKR_DB = os.path.join(RAIZ, "data", "external", "open-khipu-repository", "data", "khipu.db")
KFG_SUM = os.path.join(RAIZ, "data", "external", "data-science-khipu-article",
                       "data", "ascher_sum_relations")
SALIDA = os.path.dirname(os.path.abspath(__file__))
SEMILLA = 20261017
RNG = np.random.default_rng(SEMILLA)


def cargar_cuerdas():
    c = pd.read_csv(os.path.join(DATOS, "cuerdas.csv"), dtype={"nudos": str})
    c["nudos"] = c["nudos"].fillna("").astype(str).str.strip()
    c["con_nudos"] = c["nudos"] != ""
    # 0 con nudos vacío = ausente
    c["v"] = np.where(c["con_nudos"] & c["valor"].notna(), c["valor"], np.nan)
    return c


def cargar_quipus():
    return pd.read_csv(os.path.join(DATOS, "quipus.csv"))


def okr_conectar():
    return sqlite3.connect(OKR_DB)


def bootstrap_ic(x, n_boot=5000, alpha=0.05, rng=None):
    """IC bootstrap percentil de la media de x (unidad = fila)."""
    rng = rng or np.random.default_rng(SEMILLA)
    x = np.asarray(x, dtype=float)
    if len(x) == 0:
        return (np.nan, np.nan)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    medias = x[idx].mean(axis=1)
    return tuple(np.quantile(medias, [alpha / 2, 1 - alpha / 2]))


def p_binomial_dos_colas(k, n, p=0.5):
    from scipy.stats import binomtest
    if n == 0:
        return np.nan
    return binomtest(int(k), int(n), p).pvalue
