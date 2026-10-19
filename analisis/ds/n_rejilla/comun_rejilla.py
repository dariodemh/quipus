"""Utilidades comunes para la rejilla de categorias de Incahuasi.
Lee solo analisis/datos/*.csv y las salidas de 13/14/19. No modifica nada fuera de esta carpeta.
"""
import numpy as np
import pandas as pd

SEMILLA = 20261018
RAIZ = "./analisis"
COLS9 = [f"c{i}" for i in range(1, 10)]


def cargar_cuerdas():
    c = pd.read_csv(f"{RAIZ}/datos/cuerdas.csv")
    q = pd.read_csv(f"{RAIZ}/datos/quipus.csv")
    inc = set(q.loc[q.procedencia == "Incahuasi", "kfg"])
    c = c[c.kfg.isin(inc)].copy()
    # valor 0 sin nudos = ausente (regla del brief)
    c["sin_nudos"] = c.nudos.isna() | (c.nudos.astype(str).str.strip() == "")
    c["valor_ok"] = np.where(c.sin_nudos & (c.valor == 0), np.nan, c.valor)
    c["color"] = c.color.fillna("?").astype(str)
    c["union"] = c.union.fillna("?").astype(str)
    c["torsion"] = c.torsion.fillna("?").astype(str)
    return c, q


def color_familia(x):
    """Familia gruesa de color Ascher."""
    x = str(x)
    if ":" in x or "/" in x or "-" in x:
        return "mezcla"
    if x.startswith("W"):
        return "W"
    if x.startswith(("NB", "KB")):
        return "NB/KB"
    if x.startswith(("AB", "MB", "LB", "B")):
        return "AB/MB"
    if x.startswith("PK"):
        return "PK"
    return "otro"


def color_base(x):
    """Primer codigo de dos letras (p. ej. 'W:NB' -> 'W')."""
    import re
    m = re.search(r"[A-Z]{2}", str(x))
    return m.group(0) if m else "?"


def registrar(edges):
    """Aristas como DataFrame con columnas nodo_u, nodo_v, tipo."""
    return pd.DataFrame(edges, columns=["nodo_u", "nodo_v", "tipo"])


def componentes(nodos, aristas):
    padre = {n: n for n in nodos}

    def find(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            padre[rb] = ra

    for u, v in aristas:
        if u in padre and v in padre:
            union(u, v)
    comp = {}
    for n in nodos:
        comp.setdefault(find(n), []).append(n)
    return comp


def bh(pvals, alpha=0.05):
    """Benjamini-Hochberg. Devuelve q-valores en el orden de entrada."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    orden = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        idx = orden[i]
        prev = min(prev, p[idx] * n / (i + 1))
        q[idx] = prev
    return np.clip(q, 0, 1)


def ic_bootstrap(vals, B=5000, rng=None):
    """IC 95 % percentil de la media, remuestreando filas."""
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return np.nan, np.nan
    rng = rng or np.random.default_rng(SEMILLA)
    med = rng.choice(vals, size=(B, len(vals)), replace=True).mean(axis=1)
    return float(np.percentile(med, 2.5)), float(np.percentile(med, 97.5))
