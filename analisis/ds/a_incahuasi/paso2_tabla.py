# -*- coding: utf-8 -*-
"""Paso 2: tabla por quipu."""
import pandas as pd, numpy as np, re

RAIZ = "./"
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
g = pd.read_csv(RAIZ + "analisis/datos/grupos.csv")
inc = q[q["procedencia"] == "Incahuasi"]
ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))

def dirs(s):
    if pd.isna(s): return []
    return re.findall(r"\((?:[\d.]+),([SZU])\)", str(s))

rows = []
for k in ids:
    d = ci[ci["kfg"] == k]
    v = d.loc[~d["sin_nudos"], "valor"]
    dd = [x for s in d["nudos"].dropna() for x in dirs(s)]
    shifted = (dd.count("Z"), dd.count("S"))
    colores = d["color"].fillna("?").str.split("-").str[0].str.split(":").str[0]
    top1 = colores.value_counts().idxmax() if len(colores) else "?"
    rows.append(dict(
        kfg=k, n_cuerdas=len(d), n_grupos=d["grupo"].nunique(),
        nivel_max=d["nivel"].max(), n_sub=(d["nivel"] > 0).sum(),
        sin_nudos=int(d["sin_nudos"].sum()),
        vmin=(v.min() if len(v) else 0), vmax=(int(v.max()) if len(v) else 0),
        vmed=(v.median() if len(v) else 0),
        R=int((d["union"] == "R").sum()), V=int((d["union"] == "V").sum()),
        U=int(d["union"].isin(["U", "Unknown"]).sum()),
        S=int((d["torsion"] == "S").sum()), Z=int((d["torsion"] == "Z").sum()),
        nudo_Z=shifted[0], nudo_S=shifted[1],
        color_top=top1, pc_largo=inc[inc["kfg"] == k]["pc_largo"].values[0],
    ))
tab = pd.DataFrame(rows)
tab.to_csv("tabla_por_quipu.csv", index=False)
pd.set_option("display.width", 200)
print(tab.to_string(index=False))
print("\nTOTALES: cuerdas", tab.n_cuerdas.sum(), "| grupos", tab.n_grupos.sum())
print("union R total", tab.R.sum(), "V", tab.V.sum(), "U", tab.U.sum())
