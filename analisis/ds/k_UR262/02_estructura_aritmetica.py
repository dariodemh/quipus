# -*- coding: utf-8 -*-
"""Detectores aritmeticos basicos en UR262 + resumen estructural por grupo."""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0)

# ---- arbol: hijos directos y descendientes ----
children = {c: g for c, g in q.groupby("padre")}
def desc(c):
    out = []
    stack = list(children.get(c, pd.DataFrame()).cuerda) if c in children else []
    while stack:
        x = stack.pop()
        out.append(x)
        if x in children:
            stack += list(children[x].cuerda)
    return out

q["n_hijos"] = q.cuerda.apply(lambda c: len(children[c]) if c in children else 0)
q["suma_hijos"] = q.cuerda.apply(lambda c: children[c].valor.sum() if c in children else 0.0)
q["suma_desc"] = q.cuerda.apply(lambda c: q[q.cuerda.isin(desc(c))].valor.sum())
q["n_desc"] = q.cuerda.apply(lambda c: len(desc(c)))

print("== Estructura por grupo ==")
g = q[q.nivel == 0].groupby("grupo").agg(
    n_pend=("cuerda", "size"), suma_pend=("valor", "sum"),
    mediana=("valor", "median"), maximo=("valor", "max"),
    con_hijos=("n_hijos", lambda s: int((s > 0).sum())))
g["cuerdas"] = q.groupby("grupo").size()
g["sin_nudos"] = q[q.sin_nudos].groupby("grupo").size().reindex(g.index).fillna(0).astype(int)
g["suma_total"] = q.groupby("grupo").valor.sum()
print(g.to_string())

print("\n== Niveles ==")
print(q.groupby("nivel").agg(n=("cuerda", "size"), valor=("valor", "sum"),
                              sin_nudos=("sin_nudos", "sum"), hijos=("n_hijos", "mean")).to_string())

# ---- candidatos de igualdad ----
pend = q[q.nivel == 0].copy()
subs = q[q.nivel > 0]
print("\n== Igualdades exactas ==")
m = q[(q.n_hijos == 1)]
print("cuerdas con 1 hijo:", len(m), "| hijo == madre:", int((m.valor == m.suma_hijos).sum()))
print("pendientes con hijos:", int((pend.n_hijos > 0).sum()),
      "| pend == suma hijos:", int((pend.valor == pend.suma_hijos).sum()),
      "| pend == suma descendientes:", int((pend.valor == pend.suma_desc).sum()))
print("pendientes cuyo valor aparece tambien en algun descendiente:",
      int(sum(r.valor in set(q[q.cuerda.isin(desc(r.cuerda))].valor) for _, r in pend.iterrows())))

# valores mas repetidos
vc = q[q.valor > 0].valor.value_counts()
print("\nvalores repetidos (top 12):", vc.head(12).to_dict())
print("cuerdas con valor>0:", int((q.valor > 0).sum()), "| valores distintos:", q[q.valor > 0].valor.nunique())

# ---- cuerdas vacias: donde estan ----
print("\nsin nudos por nivel:", q.groupby("nivel").sin_nudos.sum().to_dict())
print("sin nudos y con hijos:", int(((q.sin_nudos) & (q.n_hijos > 0)).sum()))
print("pendientes vacios con hijos:", int(((q.nivel == 0) & q.sin_nudos & (q.n_hijos > 0)).sum()))

q.to_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), index=False)
