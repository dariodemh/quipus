# -*- coding: utf-8 -*-
"""Tabla descriptiva por quipu de la cohorte de costa central de Lima."""
import pandas as pd, numpy as np, re

BASE = r"."
q = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
g = pd.read_csv(BASE + r"\analisis\datos\grupos.csv")
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")

cc = c[c["kfg"].isin(sel["kfg"])].copy()
cc["nudos"] = cc["nudos"].fillna("")
# direcciones de nudo presentes
def dirs(s):
    ds = set()
    for m in re.finditer(r"\([^,]+,\s*([SZU?])\)", s):
        ds.add(m.group(1))
    return ds

rows = []
for kfg, d in cc.groupby("kfg"):
    d = d.sort_values("orden")
    col = d["color"].astype(str)
    # color base: tomar primer token antes de separadores
    cbase = col.str.split(r"[:/\-]").str[0]
    colmix = (col.str.contains(r"[:/\-]")).sum()
    vals = d["valor"].dropna().astype(int)
    vals_nz = vals[vals > 0]
    dset = set()
    for s in d["nudos"]:
        dset |= dirs(s)
    # grupos
    gg = g[g["kfg"] == kfg]
    tam_grupos = []
    for _, gr in gg.iterrows():
        n = int(gr["hasta"]) - int(gr["desde"]) + 1
        tam_grupos.append(n)
    top = cbase.value_counts()
    rows.append(dict(
        kfg=kfg,
        procedencia=sel.loc[sel["kfg"] == kfg, "procedencia"].iloc[0],
        n_cuerdas=len(d),
        n_niveles=int(d["nivel"].max()) if len(d) else 0,
        n_subs=(d["nivel"] > 0).sum(),
        n_grupos=len(gg),
        tam_grupos=",".join(map(str, tam_grupos))[:40],
        color_top=";".join(f"{k}:{v}" for k, v in top.head(3).items()),
        color_mix=int(colmix),
        val_min=int(vals_nz.min()) if len(vals_nz) else 0,
        val_max=int(vals_nz.max()) if len(vals_nz) else 0,
        val_med=round(float(vals_nz.median()), 1) if len(vals_nz) else 0,
        n_cero_sin_nudo=int(((d["valor"] == 0) & (d["nudos"] == "")).sum()),
        tors_S=int((d["torsion"] == "S").sum()),
        tors_Z=int((d["torsion"] == "Z").sum()),
        tors_U=int((d["torsion"] == "U").sum()),
        uni_R=int((d["union"] == "R").sum()),
        uni_V=int((d["union"] == "V").sum()),
        uni_T=int((d["union"] == "T").sum()),
        uni_U=int(d["union"].isin(["U", "Unknown", "?"]).sum()),
        dirs="".join(sorted(x for x in dset if x not in "?")),
        pc_estructura=sel.loc[sel["kfg"] == kfg, "pc_estructura"].iloc[0],
    ))
T = pd.DataFrame(rows).sort_values("procedencia")
T.to_csv(BASE + r"\analisis\ds\a_lima\tabla_quipus.csv", index=False)
print(T[["kfg","procedencia","n_cuerdas","n_subs","n_grupos","color_top","tors_S","tors_Z","uni_R","uni_V","uni_T","dirs"]].to_string())
print("\nTorsión: S en", T["kfg"].nunique(), "quipus; total S", T["tors_S"].sum(), "Z", T["tors_Z"].sum())
print("Unión R total", T["uni_R"].sum(), "V", T["uni_V"].sum(), "T", T["uni_T"].sum())
print("Quipus con alguna R:", (T["uni_R"]>0).sum(), "con alguna V:", (T["uni_V"]>0).sum(), "solo R:", ((T["uni_R"]>0)&(T["uni_V"]==0)).sum(), "solo V:", ((T["uni_V"]>0)&(T["uni_R"]==0)).sum())
