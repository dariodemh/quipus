"""Parser de la columna `nudos` del Khipu Field Guide.

Devuelve, por cuerda, una lista de racimos (diccionarios con n, tipo,
pos, dir, val), donde `pos` es la distancia medida desde el cordón
principal (según KFG) y `val` es la contribución decimal del racimo
(p. ej. 30 si codifica 3 decenas, 300 si codifica 3 centenas).
"""
import re
import numpy as np
import pandas as pd

CLUSTER_RE = re.compile(
    r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Za-z?]+)\)(?:,([\d.]+))?$"
)


def parse_nudos(s):
    """Lista de racimos de una cuerda. Ignora segmentos vacíos/malformados."""
    out = []
    if not isinstance(s, str) or s.strip() == "":
        return out
    for part in s.split(";"):
        part = part.strip()
        m = CLUSTER_RE.match(part)
        if not m:
            continue
        out.append(
            dict(
                n=int(m.group(1)),
                tipo=m.group(2),
                pos=float(m.group(3)),
                dir=m.group(4),
                val=float(m.group(5)) if m.group(5) is not None else np.nan,
            )
        )
    return out


def add_parsed(df):
    df = df.copy()
    df["cl"] = df["nudos"].map(parse_nudos)
    df["ncl"] = df["cl"].map(len)
    return df


def exponente(v):
    """Exponente decimal de una contribución digit*10^e (p. ej. 40 -> 1).

    Se cuentan los ceros finales del entero. Devuelve None si el valor no es
    un dígito 1..9 multiplicado por una potencia de 10.
    """
    if not np.isfinite(v) or v <= 0:
        return None
    iv = int(round(v))
    if abs(iv - v) > 1e-9:
        return None
    if not (1 <= iv <= 9 * 10 ** 12):
        return None
    e = 0
    while iv % 10 == 0:
        iv //= 10
        e += 1
    if not (1 <= iv <= 9):
        return None
    return e


def clasifica_aportes(cl):
    """Convierte contribución (1..9, 10..90, 100..900, ...) a exponente decimal.

    Devuelve lista de (exponente, val, pos). Los racimos sin valor o con
    valor no decimal se descartan para el análisis posicional.
    """
    out = []
    for c in cl:
        e = exponente(c["val"])
        if e is None:
            continue
        out.append((e, c["val"], c["pos"]))
    return out
