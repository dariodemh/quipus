# -*- coding: utf-8 -*-
"""Paso 5: B refinado (excluye coincidencias triviales y quipus dominantes) y
jerarquia interna: padre == suma(hijas); cordon principal/grupo == suma de cuerdas."""
import pandas as pd, numpy as np
from collections import Counter, defaultdict

RAIZ = "./"
rng = np.random.default_rng(0); NPERM = 500
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]; ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
ci = ci.sort_values(["kfg", "orden"])
seqval, gvals = {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]
    seqval[k] = d.loc[~d["sin_nudos"], "valor"].astype(int).tolist()
    gvals[k] = [x.loc[~x["sin_nudos"], "valor"].astype(int).tolist() for _, x in d.groupby("grupo")]

val_by_quipu = {k: set(seqval[k]) for k in ids}

def cross(vmin, exclude):
    tot = 0; hit = Counter()
    for i in ids:
        if i in exclude: continue
        for g in [sum(x) for x in gvals[i]]:
            if g < vmin: continue
            for j in ids:
                if j == i or j in exclude: continue
                if g in val_by_quipu[j]:
                    tot += 1; hit[(i, j)] += 1
    return tot, hit

print("B) suma_grupo(i)==valor_cuerda(j), variantes:")
for vmin, ex, name in [(0, set(), "todas"), (10, set(), "suma>=10"), (0, {"UR263"}, "sin UR263"), (10, {"UR263"}, "suma>=10 y sin UR263")]:
    obs, hit = cross(vmin, ex)
    nulls = []
    for _ in range(NPERM):
        sv = {k: set(rng.permutation(seqval[k]).tolist()) if seqval[k] else set() for k in ids}
        t = 0
        for i in ids:
            if i in ex: continue
            for g in [sum(x) for x in gvals[i]]:
                if g < vmin: continue
                for j in ids:
                    if j != i and j not in ex and g in sv[j]:
                        t += 1
        nulls.append(t)
    nulls = np.array(nulls)
    p = (1 + (nulls >= obs).sum()) / (1 + NPERM)
    print(f"  [{name}] obs={obs} nulo={nulls.mean():.1f} p={p:.4f}")

# --- jerarquia interna: padre == suma(hijas) ---
print("\nHIERARQUIA INTERNA: cuerda padre == suma de sus subsidiarias inmediatas")
res = []
for k in ids:
    d = ci[ci["kfg"] == k]
    byname = {r["cuerda"]: r for _, r in d.iterrows()}
    hijos = defaultdict(list)
    for _, r in d.iterrows():
        if pd.notna(r["padre"]):
            hijos[r["padre"]].append(r)
    for name, hs in hijos.items():
        p = byname.get(name)
        if p is None or p["sin_nudos"]: continue
        vals = [h["valor"] for h in hs if not h["sin_nudos"]]
        if not vals: continue
        if abs(p["valor"] - sum(vals)) < 1e-6:
            res.append((k, name, int(p["valor"]), len(hs)))
print("casos padre=suma(hijas):", len(res))
for r in res[:25]:
    print("  ", r)
tot_parents = 0
for k in ids:
    d = ci[ci["kfg"] == k]
    names = set(d["cuerda"])
    tot_parents += sum(1 for _, r in d.iterrows() if pd.notna(r["padre"]) and r["padre"] in names)
print("cuerdas con padre presente (base):", tot_parents)

# --- gran total de un quipu aparece en otro (valor de cuerda) ---
print("\ngran total (suma de todas las cuerdas) de i aparece como valor en j:")
totals = {k: sum(seqval[k]) for k in ids}
hits = 0
for i in ids:
    for j in ids:
        if j != i and totals[i] in val_by_quipu[j]:
            hits += 1; print("   ", i, "total", totals[i], "->", j)
print("total matches:", hits)
