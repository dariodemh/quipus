# -*- coding: utf-8 -*-
"""Aritmetica interna de UR262 con nulos de permutacion (1000, semilla 0).

Estadisticos (sobre el arbol fijo de cuerdas, se permutan los VALORES):
  A1 pendiente = suma de hijos directos (excluye 0=0)
  A2 pendiente = suma de todos sus descendientes (excluye 0=0)
  A3 cuerda con un solo hijo cuyo valor coincide (excluye 0=0)
  A4 total de un grupo que aparece como valor de una cuerda de otro grupo
  A5 pendiente = suma de un bloque contiguo de >=2 otras pendientes de su grupo
  A6 razon suma_hijos / valor_pendiente en [6.5,7.5]
  A7 pendiente = 2 * suma de hijos
Dos nulos: (i) barajar valores en todo el quipu; (ii) barajar dentro de cada nivel.
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)
NPERM = 1000
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0).astype(int)
q["grupo"] = q["grupo"].astype(int)

cords = q.cuerda.tolist()
ix = {c: i for i, c in enumerate(cords)}
n = len(cords)
val = q.valor.values.astype(float)
nivel = q.nivel.values.astype(int)
grupo = q.grupo.values
padre = q.padre.fillna("").values

child_idx = {i: [ix[c] for c in q.cuerda[q.padre == cords[i]]] for i in range(n)}
desc_idx = {}
for i in range(n):
    out, stack = [], list(child_idx[i])
    while stack:
        x = stack.pop()
        out.append(x)
        stack += child_idx[x]
    desc_idx[i] = out

pend = np.where(nivel == 0)[0]
with_kids = np.array([i for i in pend if len(child_idx[i]) > 0])
one_kid = np.array([i for i in range(n) if len(child_idx[i]) == 1])
groups = sorted(set(grupo))
gpend = {g: np.where((nivel == 0) & (grupo == g))[0] for g in groups}
pos_in_group = {g: {c: k for k, c in enumerate(sorted(gpend[g], key=lambda i: q.orden.iloc[i]))} for g in groups}

# bloques contiguos de >=2 pendientes del mismo grupo, para A5
BLOCKS = []
for g in groups:
    members = sorted(gpend[g], key=lambda i: q.orden.iloc[i])
    m = len(members)
    for a in range(m):
        for b in range(a + 1, m):
            block = members[a:b + 1]
            for ci in members:
                if ci not in block:
                    BLOCKS.append((ci, block))
print("bloques A5:", len(BLOCKS))


def stats(v):
    s = {}
    s["A1"] = sum(1 for i in with_kids if v[i] > 0 and v[i] == sum(v[j] for j in child_idx[i]))
    s["A2"] = sum(1 for i in with_kids if v[i] > 0 and v[i] == sum(v[j] for j in desc_idx[i]))
    s["A3"] = sum(1 for i in one_kid if v[i] > 0 and v[i] == v[child_idx[i][0]])
    # A4: total de grupo == valor de una cuerda de otro grupo
    tot = {g: v[gpend[g]].sum() for g in groups}
    s["A4"] = sum(1 for g in groups for i in range(n)
                  if tot[g] > 0 and grupo[i] != g and v[i] == tot[g])
    # A5: bloque contiguo de >=2 pendientes (otras) del mismo grupo
    a5 = 0
    for ci, block in BLOCKS:
        if v[ci] > 0 and abs(sum(v[j] for j in block) - v[ci]) < 1e-9:
            a5 += 1
    s["A5"] = a5
    # A6 razon ~7, A7 duplicacion exacta
    r = [sum(v[j] for j in child_idx[i]) / v[i] for i in with_kids if v[i] > 0 and sum(v[j] for j in child_idx[i]) > 0]
    s["A6"] = sum(1 for x in r if 6.5 <= x <= 7.5)
    s["A7"] = sum(1 for i in with_kids if v[i] > 0 and sum(v[j] for j in child_idx[i]) == 2 * v[i])
    return s


def permute_global(v):
    return RNG.permutation(v)


def permute_by_level(v):
    out = v.copy()
    for lv in np.unique(nivel):
        m = np.where(nivel == lv)[0]
        out[m] = RNG.permutation(v[m])
    return out


obs = stats(val)
print("Observado:", obs)

res = {}
nulls = {"global": [], "por_nivel": []}
for name, fn in [("global", permute_global), ("por_nivel", permute_by_level)]:
    for _ in range(NPERM):
        nulls[name].append(stats(fn(val)))

for name in nulls:
    nd = pd.DataFrame(nulls[name])
    print(f"\n== Nulo {name} (n={NPERM}) ==")
    rows = []
    for key in obs:
        arr = nd[key].values
        p = (1 + int((arr >= obs[key]).sum())) / (1 + NPERM)
        rows.append(dict(stat=key, obs=obs[key], media_nula=round(arr.mean(), 2),
                         p95=np.percentile(arr, 95), p=p))
    t = pd.DataFrame(rows)
    print(t.to_string(index=False))
    res[name] = t

# Holm sobre la familia de 7 pruebas con el nulo global
def holm(pvals):
    order = np.argsort(pvals)
    m = len(pvals)
    out = np.empty(m)
    prev = 0
    for rank, i in enumerate(order):
        adj = min(1.0, max(prev, (m - rank) * pvals[i]))
        out[i] = adj
        prev = adj
    return out

t = res["global"].copy()
t["p_holm"] = holm(t.p.values)
print("\n== Holm (nulo global, 7 pruebas) ==")
print(t[["stat", "obs", "media_nula", "p", "p_holm"]].to_string(index=False))
t.to_csv(os.path.join(OUT, "ur262_aritmetica_nulos.csv"), index=False)
