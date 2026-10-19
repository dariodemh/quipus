# -*- coding: utf-8 -*-
"""ATAQUE 5: el emparejamiento 2+1+2+2+2 de UR278.

¿Cuanto del exceso de igualdades (11) se explica por igualdades entre columnas
VECINAS en general? Controles:
  - las 8 parejas adyacentes y su complemento
  - las 5 rotaciones contiguas de 2+1+2+2+2
  - los 945 emparejamientos (ya hecho por n_espinoza1963) y el maximo sobre
    subconjuntos de 4 parejas adyacentes
  - tasa de igualdad adyacente vs no adyacente en todo el corpus
"""
import itertools
import numpy as np
import pandas as pd

RAIZ = r"."
d = pd.read_csv(RAIZ + "/analisis/13_sistema_incahuasi/ur278_tabla.csv")
C = [f"c{i}" for i in range(1, 10)]
D = d[d.n == 9].dropna(subset=C).reset_index(drop=True)
X = D[C].astype(float).values
n = len(X)
print(f"UR278: {n} filas de 9 columnas")

T = np.zeros((9, 9), int)
for i in range(9):
    for j in range(i + 1, 9):
        T[i, j] = T[j, i] = int(np.sum(X[:, i] == X[:, j]))
print("\nmatriz de igualdades:")
print(pd.DataFrame(T, index=C, columns=C).to_string())

ady = [(i, i + 1) for i in range(8)]
print("\nparejas adyacentes:", [(C[i] + "-" + C[j], T[i, j]) for i, j in ady])
target = [(0, 1), (3, 4), (5, 6), (7, 8)]
comp = [(1, 2), (2, 3), (4, 5), (6, 7)]
t_t = sum(T[i, j] for i, j in target)
t_c = sum(T[i, j] for i, j in comp)
print(f"objetivo 2+1+2+2+2 (1-2)(4-5)(6-7)(8-9) = {t_t}")
print(f"complemento adyacente (2-3)(3-4)(5-6)(7-8) = {t_c}")
print(f"suma de las 8 adyacentes = {sum(T[i,j] for i,j in ady)}; esperado de 4 al azar = "
      f"{sum(T[i,j] for i,j in ady)/2:.1f}")

# las 5 rotaciones contiguas que dejan una columna impar suelta
print("\npatrones contiguos 2+1+2+2+2 (dejan suelta una columna):")
for libre in range(0, 9, 2):
    idx = [i for i in range(9) if i != libre]
    mm = [(idx[0], idx[1]), (idx[2], idx[3]), (idx[4], idx[5]), (idx[6], idx[7])]
    print(f"  deja c{libre+1}: {sum(T[i,j] for i,j in mm)} igualdades "
          f"{[(C[i]+'-'+C[j], T[i,j]) for i,j in mm]}")

# todas las parejas de 4 aristas disjuntas tomadas de las 8 adyacentes
def matchings4(items):
    if len(items) < 2:
        yield []
        return
    a = items[0]
    yield from matchings4(items[1:])
    for k in range(1, len(items)):
        b = items[k]
        for rest in matchings4(items[k + 1:]):
            yield [(a, b)] + rest


S = sorted({tuple(sorted(m)) for m in matchings4(ady) if len(m) == 4})
vals = np.array([sum(T[i, j] for i, j in m) for m in S])
print(f"\nsubconjuntos de 4 parejas adyacentes disjuntas: {len(S)}; "
      f"media={vals.mean():.2f} max={vals.max()} min={vals.min()}")
print(f"objetivo {t_t}: rank {1+int(np.sum(vals>t_t))}/{len(vals)}, "
      f"p unilateral={np.mean(vals>=t_t):.3f}")

# 945 emparejamientos: rank del objetivo
def all_matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for k in range(1, len(items)):
        b = items[k]
        for rest in all_matchings(items[1:k] + items[k + 1:]):
            yield [(a, b)] + rest

ALL = [(s, tuple(mm)) for s in range(9) for mm in all_matchings([i for i in range(9) if i != s])]
vt = np.array([sum(T[i, j] for i, j in mm) for s, mm in ALL])
print(f"945 emparejamientos: objetivo {t_t}, rank {1+int(np.sum(vt>t_t))}/945, "
      f"p={np.mean(vt>=t_t):.3f}, max={vt.max()}")

# ---- corpus: igualdad adyacente vs no adyacente ----
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
c["val"] = pd.to_numeric(c.valor, errors="coerce")
c = c[(c.nivel == 0) & c.val.notna() & (c.val > 0)].sort_values(["kfg", "orden"])
ad_same = ad_tot = no_same = no_tot = 0
for (k, gr), g in c.groupby(["kfg", "grupo"]):
    v = g.val.values
    m = len(v)
    if m < 4:
        continue
    for i in range(m):
        for j in range(i + 1, m):
            same = v[i] == v[j]
            if j == i + 1:
                ad_tot += 1; ad_same += same
            else:
                no_tot += 1; no_same += same
print(f"\ncorpus: igualdad entre cuerdas ADYACENTES {ad_same}/{ad_tot} = {ad_same/ad_tot:.4f}")
print(f"        igualdad entre NO adyacentes    {no_same}/{no_tot} = {no_same/no_tot:.4f}")
print(f"        razon = {(ad_same/ad_tot)/(no_same/no_tot):.2f}x")
# solo UR278
g = c[c.kfg == "UR278"]
v = g.val.values
aa = [(i, i + 1) for i in range(len(v) - 1)]
print(f"UR278 cordones nivel 0: {len(v)}; igualdad adyacente "
      f"{np.mean([v[i]==v[i+1] for i,j in aa]):.3f}")

out = pd.DataFrame([dict(prueba="objetivo", igualdades=t_t),
                    dict(prueba="complemento_adyacente", igualdades=t_c),
                    dict(prueba="media_4_adyacentes", igualdades=round(float(vals.mean()), 2)),
                    dict(prueba="max_4_adyacentes", igualdades=int(vals.max())),
                    dict(prueba="max_945", igualdades=int(vt.max()))])
out.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/ur278_control.csv", index=False)
print("\n", out.to_string(index=False))
