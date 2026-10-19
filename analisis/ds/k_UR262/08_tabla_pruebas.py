# -*- coding: utf-8 -*-
"""Tabla maestra de pruebas de UR262 con p empiricos y correccion de Holm.

Reune los resultados de 05, 06 y 07 mas dos pruebas exactas (hipergeometrica)
y aplica Holm a la familia de pruebas confirmatorias.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats as st

OUT = os.path.dirname(os.path.abspath(__file__))
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0).astype(float)
q["grupo"] = q["grupo"].astype(int)

p = q[q.nivel == 0].copy()
p["pos"] = p.groupby("grupo").cumcount() + 1
data_groups = [1, 3, 4, 5, 6, 7]
pd_ = p[p.grupo.isin(data_groups)]

# AB en la primera posicion de grupos con datos
K = int((pd_.color == "AB").sum())
N = len(pd_)
n = len(data_groups)
x = int(((pd_.pos == 1) & (pd_.color == "AB")).sum())
p_ab = st.hypergeom.sf(x - 1, N, K, n)
print(f"AB en posicion 1: {x}/{n} grupos; AB totales {K}/{N} pendientes; hipergeometrica p={p_ab:.5f}")

# primer pendiente = maximo, solo grupos con datos
first_max = 0
for g in data_groups:
    s = pd_[pd_.grupo == g].sort_values("orden")
    first_max += int(s.valor.iloc[0] == s.valor.max())
print(f"primer pendiente = maximo: {first_max}/{len(data_groups)}")

# expectativa exacta bajo aleatorizacion de valores dentro del grupo
rng = np.random.default_rng(0)
exp = np.mean([sum(1 for g in data_groups if (lambda v: v[0] == v.max())(
    rng.permutation(pd_[pd_.grupo == g].sort_values("orden").valor.values)))
    for _ in range(2000)])
print(f"esperado por azar (permutando dentro del grupo): {exp:.2f}")

rows = [
    ("A1 pendiente = suma de hijos", 0.0729, "nulo global, 1000 perm"),
    ("A1 pendiente = suma de hijos", 0.0370, "nulo por nivel, 1000 perm"),
    ("A3 cuerda unica hija con valor identico", 0.0030, "nulo global"),
    ("A4 total de grupo repetido en otra cuerda", 1.0000, "nulo global"),
    ("A5 pendiente = bloque contiguo del grupo", 0.3067, "nulo global"),
    ("A6 razon suma_hijos/valor en [6.5,7.5]", 0.0020, "nulo global (ventana post hoc)"),
    ("A6b razon: maximo sobre ventanas (corrige post hoc)", 0.6154, "nulo global"),
    ("D1 duplicados de valor", 1.0000, "nulo de digitos"),
    ("D2 similitud entre pendientes adyacentes", 0.1798, "nulo global"),
    ("D3 AB en primera posicion del grupo (6 grupos)", p_ab, "hipergeometrica exacta"),
    ("D3b periodicidad del color (lags 2-15)", 0.0799, "permutar colores"),
    ("D5 largo vs valor (Spearman 0.45)", 0.0010, "nulo global"),
    ("D6 primer pendiente = maximo (6 grupos)", 0.0027, "permutacion dentro de grupo"),
    ("D7 madre-hijo duplicado exacto (7 casos)", 0.0050, "nulo global"),
    ("D7b madre-hijo duplicado <=1% (8 casos)", 0.0040, "nulo global"),
]
t = pd.DataFrame(rows, columns=["prueba", "p", "nulo"])

def holm(pv):
    order = np.argsort(pv)
    m = len(pv)
    out = np.empty(m)
    prev = 0.0
    for rank, i in enumerate(order):
        adj = min(1.0, max(prev, (m - rank) * pv[i]))
        out[i] = adj
        prev = adj
    return out

t["p_holm"] = holm(t.p.values)
print("\n== Tabla maestra (Holm sobre 15 pruebas) ==")
print(t.to_string(index=False))
t.to_csv(os.path.join(OUT, "ur262_tabla_pruebas.csv"), index=False)
