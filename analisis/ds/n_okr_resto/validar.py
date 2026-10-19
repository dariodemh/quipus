"""Validacion final de los CSV nuevos: valor = regla aplicada a los nudos, estructura de nombres,
orden y conteos. Falla ruidosamente si algo no cuadra.
"""
import re

import pandas as pd

import os

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r"(\d+)([A-Za-z]+)\(([\d.]+),([A-Za-z0-9?]+)\),(\d+)")


def posicional(nudos):
    cl = [(int(m.group(1)), m.group(2).upper()) for m in PAT.finditer(nudos)]
    if not cl:
        return 0
    lug = [0] * len(cl)
    lug[-1] = 0 if cl[-1][1] in ("L", "E", "EE", "LL") else 1
    for i in range(len(cl) - 2, -1, -1):
        lug[i] = lug[i + 1] + 1
    return sum(n * 10 ** p for (n, _), p in zip(cl, lug))


def aditivo(nudos):
    tot = 0
    for m in PAT.finditer(nudos):
        n, t = int(m.group(1)), m.group(2).upper()
        tot += 10 * n if t == "S" else n
    return tot


for kh, fn in (("KH0674", posicional), ("KH0675", posicional), ("KH0676", aditivo)):
    d = pd.read_csv(os.path.join(HERE, "cuerdas_%s.csv" % kh), dtype={"cuerda": str})
    d["nudos"] = d.nudos.fillna("")
    calc = d.nudos.map(fn)
    ilegibles = d.nudos.eq("?")
    mal = ((calc != d.valor) & ~ilegibles).sum()
    nivel = d.cuerda.str.count(r"s\d+")
    padre_ok = all(
        (r.padre == (r.cuerda[: r.cuerda.rfind("s")] if r.nivel else "")) or pd.isna(r.padre) and r.nivel == 0
        for r in d.itertuples())
    print(kh, "filas", len(d), "valor!=calc", mal, "nivel_ok", (nivel == d.nivel).all(),
          "padre_ok", padre_ok, "orden_unico", d.orden.is_unique,
          "rango_orden", (d.orden.min(), d.orden.max()),
          "nudos_ilegibles", int(ilegibles.sum()))
    if mal:
        print(d[calc != d.valor][["cuerda", "valor", "nudos"]].head())
