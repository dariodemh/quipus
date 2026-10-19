# -*- coding: utf-8 -*-
"""
06_bootstrap.py -- IC95% por bootstrap de quipus para los efectos principales
(estimador de efectos fijos ponderado por n1*n0/n).
"""
import os, importlib.util
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
spec = importlib.util.spec_from_file_location("p02", os.path.join(OUT, "02_permutaciones.py"))
p02 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p02)

df = p02.load()
d0 = p02.add_position(df)
k = d0[(d0.terminacion == "K") & (d0.nivel == 0) & (d0.L > 0)].copy()
k = k.sort_values(["kfg", "grupo", "orden"], kind="stable").reset_index(drop=True)
k["rank"] = k.groupby(["kfg", "grupo"]).cumcount() + 1
k["gsize"] = k.groupby(["kfg", "grupo"]).orden.transform("size")
k["is_last"] = k["rank"] == k.gsize

def per_quipu(sub, ycol, flagcol):
    out = []
    for q, s in sub.groupby("kfg"):
        y = s[ycol].values.astype(float); f = s[flagcol].values.astype(bool)
        n1 = f.sum(); n0 = len(s) - n1
        if n1 == 0 or n0 == 0:
            continue
        d = y[f].mean() - y[~f].mean()
        w = n1 * n0 / len(s)
        out.append((q, w, d))
    return pd.DataFrame(out, columns=["kfg", "w", "d"])

def boot(tab, B=4000, seed=5):
    rng = np.random.default_rng(seed)
    d = tab.d.values; w = tab.w.values; n = len(tab)
    est = np.sum(w * d) / np.sum(w)
    bs = np.empty(B)
    for b in range(B):
        ix = rng.integers(0, n, n)
        bs[b] = np.sum(w[ix] * d[ix]) / np.sum(w[ix])
    return est, np.percentile(bs, 2.5), np.percentile(bs, 97.5)

rows = []
tests = [
    ("última posición", k, "sin", "is_last"),
    ("largo K (cm)", k, "L", "sin"),
    ("unión U", k.assign(flag=k.un.eq("DESCONOCIDA")), "sin", "flag"),
    ("color B", k.assign(flag=k.pc.eq("B")), "sin", "flag"),
    ("color RB", k.assign(flag=k.pc.eq("RB")), "sin", "flag"),
    ("color DB", k.assign(flag=k.pc.eq("DB")), "sin", "flag"),
    ("color LB", k.assign(flag=k.pc.eq("LB")), "sin", "flag"),
]
for name, sub, ycol, flag in tests:
    tab = per_quipu(sub, ycol, flag)
    est, lo, hi = boot(tab)
    unit = "cm" if ycol == "L" else "pp"
    mult = 1 if ycol == "L" else 100
    print(f"{name}: {mult*est:+.2f} {unit} IC95 [{mult*lo:+.2f}, {mult*hi:+.2f}] (quipus={len(tab)})", flush=True)
    rows.append(dict(test=name, efecto=mult*est, lo=mult*lo, hi=mult*hi, n_quipus=len(tab)))

pd.DataFrame(rows).to_csv(os.path.join(OUT, "bootstrap_ic.csv"), index=False, encoding="utf-8-sig")
print("guardado bootstrap_ic.csv", flush=True)
