# -*- coding: utf-8 -*-
"""Archivo de Huaquerones (= grupo de Puruchuco, UR060-UR082 segun Clindaniel 2019).
Busca cuentas duplicadas / totales coincidentes (Urton y Brezine 2005) y control
positivo de deteccion de duplicados exactos."""
import pandas as pd, numpy as np, itertools
BASE = r"."
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
V0 = {}
for k in sel["kfg"]:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V0[k] = list(d["valor"].fillna(0).astype(int))

H = sorted(sel[sel["sitio"] == "Huaquerones"]["kfg"])
print("Huaquerones (= Puruchuco?) n =", len(H), H)
print("\nDescribe:")
for k in H:
    v = np.array(V0[k]); vnz = v[v > 0]
    print(f"  {k:8s} n_cuerdas={len(v):3d} n_nz={len(vnz):3d} total={int(v.sum()):6d} "
          f"max={int(v.max()) if len(v) else 0:6d} mediana={int(np.median(vnz)) if len(vnz) else 0}")

# totales duplicados dentro de Huaquerones
print("\nPares de Huaquerones con TOTAL identico:")
tot = {k: int(np.sum(V0[k])) for k in H}
for a, b in itertools.combinations(H, 2):
    if tot[a] == tot[b]:
        print(f"  {a} y {b}: total={tot[a]}")
# totales coincidentes en TODO el cohorte
allt = {k: int(np.sum(V0[k])) for k in sel["kfg"]}
print("\nPares con total identico en todo el cohorte (top):")
cnt = 0
for a, b in itertools.combinations(sel["kfg"], 2):
    if allt[a] == allt[b]:
        cnt += 1
        if cnt <= 15:
            print(f"  {a}({sel.set_index('kfg').loc[a,'sitio']}) = {b}({sel.set_index('kfg').loc[b,'sitio']}) : {allt[a]}")
print("  ... total pares:", cnt)

# Jaccard de conjuntos de valores (multiset): Huaquerones
def jac(a, b):
    A, B = set(x for x in V0[a] if x > 0), set(x for x in V0[b] if x > 0)
    return len(A & B) / len(A | B) if (A | B) else 0
pairs = list(itertools.combinations(H, 2))
J = sorted(((jac(a, b), a, b) for a, b in pairs), reverse=True)
print("\nTop Jaccard de conjuntos de valores (Huaquerones):")
for j, a, b in J[:8]:
    print(f"  {a} x {b}: J={j:.3f}")
# control positivo: duplicado exacto
print("\nControl positivo: J(UR060, copia exacta) =", jac("UR060", "UR060"))
print("Duplicado exacto en el cohorte (secuencias iguales):")
seen = {}
for k in sel["kfg"]:
    key = tuple(V0[k])
    if key in seen:
        print("  ", seen[key], "==", k)
    seen[key] = k
print("  (fin)")
# tamano de conjuntos de valores vs Jaccard: cuanto explica el vocabulario comun
print("\nVocabulario compartido: |valores distintos| Huaquerones =",
      len(set(x for k in H for x in V0[k] if x > 0)))
