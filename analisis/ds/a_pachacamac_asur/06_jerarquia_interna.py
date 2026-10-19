# -*- coding: utf-8 -*-
"""06 - Jerarquia interna: top-cords (UR201), madre=suma de hijas, grupo resumen."""
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"

q = pd.read_csv(DAT / "quipus.csv")
c = pd.read_csv(DAT / "cuerdas.csv")
m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
ids = sorted(q[m & q["kfg"].str.startswith(("AS", "UR"))]["kfg"].tolist())
cc = c[c["kfg"].isin(ids)].copy()

def vr(v, n):
    if pd.isna(v): return np.nan
    if v == 0 and (pd.isna(n) or str(n).strip() == ""): return np.nan
    return float(v)
cc["vreal"] = [vr(r["valor"], r["nudos"]) for _, r in cc.iterrows()]

# --- top cords (union T) ---
print("== Cuerdas superiores (union T) ==")
t = cc[cc["union"] == "T"]
print(t[["kfg", "orden", "cuerda", "grupo", "valor", "color", "largo", "nudos"]].to_string(index=False))
for _, r in t.iterrows():
    k = r["kfg"]; gr = r["grupo"]
    grp = cc[(cc["kfg"] == k) & (cc["grupo"] == gr)]
    vs = [x for x in grp["vreal"] if not np.isnan(x)]
    print(f"  {k} top-cord grupo {gr}: valor={r['valor']} | suma grupo (incl)={np.nansum(vs)} | otras={np.nansum([x for x in vs if x != r['valor']])}")

# --- madre = suma de hijas directas: por quipu ---
hijas = defaultdict(list)
for _, r in cc.iterrows():
    if isinstance(r["padre"], str) and r["padre"] == r["padre"]:
        hijas[(r["kfg"], r["padre"])].append(r["vreal"])
madre_sum = defaultdict(list)
for (k, madre), vs in hijas.items():
    vs = [x for x in vs if not np.isnan(x)]
    mr = cc[(cc["kfg"] == k) & (cc["cuerda"] == madre)]["vreal"]
    if len(mr) == 0 or np.isnan(mr.iloc[0]) or not vs: continue
    if abs(sum(vs) - mr.iloc[0]) < 1e-9:
        madre_sum[k].append((madre, mr.iloc[0], len(vs)))
print("\n== madre = suma de hijas directas, por quipu ==")
for k in sorted(madre_sum, key=lambda x: -len(madre_sum[x])):
    print(f"  {k}: {len(madre_sum[k])} casos -> {madre_sum[k][:6]}")

# --- grupos donde 1a cuerda = suma de las demas ---
print("\n== Grupo: 1a cuerda = suma de las demas ==")
for k in ids:
    for gr, rows in cc[cc["kfg"] == k].groupby("grupo"):
        r = rows.sort_values("orden")
        v = [x for x in r["vreal"] if not np.isnan(x)]
        if len(v) >= 2 and abs(v[0] - sum(v[1:])) < 1e-9:
            print(f"  {k} grupo {gr}: n={len(v)} 1a={v[0]:.0f} resto={ [int(x) for x in v[1:]] }")

# --- grupos con >=3 cuerdas: cuantas veces la ultima cuerda = suma de las anteriores (top-cord-like) ---
cnt_last = 0
for k in ids:
    for gr, rows in cc[cc["kfg"] == k].groupby("grupo"):
        r = rows.sort_values("orden")
        v = [x for x in r["vreal"] if not np.isnan(x)]
        if len(v) >= 3 and abs(v[-1] - sum(v[:-1])) < 1e-9:
            cnt_last += 1
print("\nGrupos con ultima cuerda = suma de las anteriores:", cnt_last)

# --- resumen por quipu de rasgos de jerarquia ---
filas = []
for k in ids:
    tot = float(np.nansum(cc[(cc["kfg"] == k) & (cc["nivel"] == 0)]["vreal"]))
    filas.append(dict(kfg=k,
        n_sumas_madre=len(madre_sum.get(k, [])),
        n_top=len(cc[(cc["kfg"] == k) & (cc["union"] == "T")]),
        total_colgantes=round(tot)))
pd.DataFrame(filas).to_csv(OUT / "jerarquia_interna.csv", index=False)
print("\n(guardado salida/jerarquia_interna.csv)")
