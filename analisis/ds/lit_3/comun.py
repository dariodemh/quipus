"""Utilidades comunes para lit_3 (afirmaciones comprobables de la literatura).

Regla del brief: la unidad de analisis es el quipu, no la cuerda.
Todas las rutas son relativas a la raiz del repo.
"""
from __future__ import annotations

import os
import re
import numpy as np
import pandas as pd

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATOS = os.path.join(RAIZ, "analisis", "datos")
SEMILLA = 20261017
RNG = np.random.default_rng(SEMILLA)

RE_NUDO = re.compile(r"(\d+)(S|L|E|EE|LL)\(([0-9.]+),\s*([SZU])\)")


def cargar():
    c = pd.read_csv(os.path.join(DATOS, "cuerdas.csv"))
    q = pd.read_csv(os.path.join(DATOS, "quipus.csv"))
    g = pd.read_csv(os.path.join(DATOS, "grupos.csv"))
    return c, q, g


def nudos_de(s: str):
    """Devuelve lista de (n, tipo, pos_cm, direccion) de una cadena `nudos`."""
    if not isinstance(s, str):
        return []
    return [(int(m.group(1)), m.group(2), float(m.group(3)), m.group(4))
            for m in RE_NUDO.finditer(s)]


def contar_nudos(c: pd.DataFrame):
    """Conteo de nudos individuales por khipu y por (tipo, direccion)."""
    filas = []
    for k, g in c.groupby("kfg"):
        d = {}
        for s in g["nudos"].dropna():
            for n, t, _pos, dire in nudos_de(s):
                clase = "simple" if t == "S" else "largo_E"
                d[(clase, dire)] = d.get((clase, dire), 0) + n
        filas.append((k, d.get(("simple", "S"), 0), d.get(("simple", "Z"), 0),
                      d.get(("largo_E", "S"), 0), d.get(("largo_E", "Z"), 0)))
    return pd.DataFrame(filas, columns=["kfg", "simple_S", "simple_Z",
                                        "largo_S", "largo_Z"])


def bloques_de_6(c: pd.DataFrame, khipus):
    """Bloques de 6 colgantes consecutivos dentro de cada grupo del KFG.

    Devuelve un DataFrame con una fila por bloque (id, posicion, valores,
    color y union del primer cordel). Los restos (<6) se descartan.
    """
    s = c[c.kfg.isin(khipus) & (c.nivel == 0)].sort_values(["kfg", "orden"])
    filas = []
    for (k, gr), d in s.groupby(["kfg", "grupo"]):
        d = d.sort_values("orden")
        n = len(d)
        for i in range(0, n - n % 6, 6):
            b = d.iloc[i:i + 6]
            filas.append({
                "kfg": k, "grupo": gr, "inicio": i,
                "valores": list(b["valor"].astype(float)),
                "v1": float(b["valor"].iloc[0]),
                "total": float(b["valor"].sum()),
                "union1": b["union"].iloc[0],
                "color1": b["color"].iloc[0],
                "colores": list(b["color"]),
            })
    return pd.DataFrame(filas)


def bootstrap_por_quipu(d: pd.DataFrame, col_num: str, col_den: str, B=5000):
    """IC 95% del cociente agregado, remuestreando quipus (clusters)."""
    ks = d["kfg"].to_numpy()
    num = d[col_num].to_numpy(float)
    den = d[col_den].to_numpy(float)
    vals = []
    n = len(d)
    for _ in range(B):
        idx = RNG.integers(0, n, n)
        s = den[idx].sum()
        if s > 0:
            vals.append(num[idx].sum() / s)
    return np.percentile(vals, [2.5, 97.5])


def bh_fdr(pvals):
    """Benjamini-Hochberg: devuelve q-valores en el orden original."""
    p = np.asarray(pvals, float)
    n = len(p)
    orden = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank, i in enumerate(orden[::-1], start=1):
        k = n - rank + 1
        val = min(prev, p[i] * n / k)
        q[i] = val
        prev = val
    return q
