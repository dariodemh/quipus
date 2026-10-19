# -*- coding: utf-8 -*-
"""UR262: verificacion de la decimalidad de los racimos de unidades.

Detecta cuerdas con mas de un racimo L/E (digito de unidades partido) y
comprueba que la suma de esos racimos reproduce el digito de unidades.
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0).astype(int)
k = pd.read_csv(os.path.join(OUT, "ur262_nudos.csv"))

u = k[k.tipo.isin(["L", "E"])]
c = u.groupby("cuerda").agg(n_racimos=("aporte", "size"), suma=("aporte", "sum"))
m = c.join(q.set_index("cuerda")[["valor", "nudos", "largo"]])

multi = m[m.n_racimos > 1]
print("cuerdas con racimos L/E:", len(m))
print("cuerdas con el digito de unidades partido en 2 racimos:", len(multi))
print(multi.to_string())
mal = m[m.suma != m.valor % 10]
print("\ncuerdas donde la suma L/E != valor mod 10:", len(mal))
print(mal.to_string())

# posiciones crecientes dentro de la cuerda
bad = 0
for _, g in k.groupby("cuerda"):
    p = g.pos.values
    if len(p) > 1 and any(p[i + 1] <= p[i] for i in range(len(p) - 1)):
        bad += 1
print("\ncuerdas con >1 racimo:", int((k.groupby('cuerda').size() > 1).sum()),
      "| con posiciones no crecientes:", bad)
print("vueltas maximas por tipo:", k.groupby("tipo").ncl.max().to_dict())
