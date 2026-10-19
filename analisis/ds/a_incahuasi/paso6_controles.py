# -*- coding: utf-8 -*-
"""Paso 6: (B) cross-matches con nulo correcto (reagrupa valores) y filtros;
(H) jerarquia interna padre=suma(hijas>=2) con nulo; (E) quipus especiales."""
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
seqval, gvals, gsizes = {}, {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]
    seqval[k] = d.loc[~d["sin_nudos"], "valor"].astype(int).tolist()
    gr = list(d.groupby("grupo"))
    gvals[k] = [x.loc[~x["sin_nudos"], "valor"].astype(int).tolist() for _, x in gr]
    gsizes[k] = [int(len(x)) for _, x in gr]
val_by_quipu = {k: set(seqval[k]) for k in ids}

def obs_cross(vmin, ex):
    tot = 0
    for i in ids:
        if i in ex: continue
        for g in [sum(x) for x in gvals[i]]:
            if g < vmin: continue
            for j in ids:
                if j != i and j not in ex and g in val_by_quipu[j]:
                    tot += 1
    return tot

def null_cross(vmin, ex):
    outs = []
    for _ in range(NPERM):
        # recomputa sumas de grupo de cada i reagrupando sus valores permutados
        newg = {}
        for i in ids:
            flat = [v for x in gvals[i] for v in x]
            if not flat: newg[i] = []; continue
            pv = rng.permutation(flat); idx = 0; o = []
            for sz in gsizes[i]:
                o.append(int(pv[idx:idx+sz].sum())); idx += sz
            newg[i] = o
        t = 0
        for i in ids:
            if i in ex: continue
            for g in newg[i]:
                if g < vmin: continue
                for j in ids:
                    if j != i and j not in ex and g in val_by_quipu[j]:
                        t += 1
        outs.append(t)
    return np.array(outs)

print("B) cross-matches suma_grupo(i)==valor_cuerda(j):")
for vmin, ex, name in [(0, set(), "todas"), (10, set(), "suma>=10"),
                       (0, {"UR263"}, "sin UR263"), (10, {"UR263"}, "suma>=10 sin UR263"),
                       (100, set(), "suma>=100")]:
    o = obs_cross(vmin, ex); nl = null_cross(vmin, ex)
    print(f"  [{name}] obs={o} nulo={nl.mean():.1f} p={(1+(nl>=o).sum())/(1+NPERM):.4f}")

# jerarquia interna padre=suma(hijas>=2)
def count_hier():
    hits = []
    for k in ids:
        d = ci[ci["kfg"] == k]; byname = {r["cuerda"]: r for _, r in d.iterrows()}
        hijos = defaultdict(list)
        for _, r in d.iterrows():
            if pd.notna(r["padre"]): hijos[r["padre"]].append(r)
        for name, hs in hijos.items():
            p = byname.get(name)
            if p is None or p["sin_nudos"] or len(hs) < 2: continue
            vals = [h["valor"] for h in hs if not h["sin_nudos"]]
            if len(vals) >= 2 and abs(p["valor"] - sum(vals)) < 1e-6:
                hits.append((k, name, int(p["valor"]), len(vals)))
    return hits
h = count_hier()
print(f"\nH) padre==suma(>=2 hijas no vacias): obs={len(h)}  casos={h}")
base = 0
for k in ids:
    d = ci[ci["kfg"] == k]; byname = {r["cuerda"]: r for _, r in d.iterrows()}
    hijos = defaultdict(list)
    for _, r in d.iterrows():
        if pd.notna(r["padre"]) and r["padre"] in byname: hijos[r["padre"]].append(r)
    base += sum(1 for name, hs in hijos.items() if len([x for x in hs if not x["sin_nudos"]]) >= 2)
print("base nodos con >=2 hijas no vacias:", base)
# nulo: permutar valores dentro del quipu
nlh = 0
for _ in range(NPERM):
    cnt = 0
    for k in ids:
        d = ci[ci["kfg"] == k].copy()
        perm = rng.permutation(d["valor"].values)
        d["valor"] = perm
        # recolocar sin_nudos segun nuevo valor? no: sin_nudos depende de nudos; aquí mezclamos valor entre cuerdas
        byname = {r["cuerda"]: r for _, r in d.iterrows()}
        hijos = defaultdict(list)
        for _, r in d.iterrows():
            if pd.notna(r["padre"]): hijos[r["padre"]].append(r)
        for name, hs in hijos.items():
            if name not in byname: continue
            p = byname[name]
            vals = [x["valor"] for x in hs]
            if len(vals) >= 2 and abs(p["valor"] - sum(vals)) < 1e-6: cnt += 1
    nlh += cnt
print(f"nulo padre==suma(hijas>=2): media={nlh/NPERM:.2f}")

# E) quipus especiales
for k in ["JC007", "UR257", "UR268", "JC017", "JC020", "JC021"]:
    d = ci[ci["kfg"] == k]
    print(f"\n{k}: {len(d)} cuerdas, valores={d.loc[~d.sin_nudos,'valor'].astype(int).tolist()[:20]}")
