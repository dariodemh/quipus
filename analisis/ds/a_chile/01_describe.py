# -*- coding: utf-8 -*-
"""01: Describe el conjunto de quipus del norte de Chile.
Procedencias: Lluta Valley, Arica, Playa Miller (incluye 'Mollepampa / Playa Miller').
Escribe tablas resumen por quipu en la carpeta.
"""
import pandas as pd, numpy as np, os, json

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
q = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "quipus.csv"))
g = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "grupos.csv"))

CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]

meta = q[q.kfg.isin(CHILE)][["kfg", "okr", "museo", "procedencia", "region",
                             "pc_largo", "pc_color", "pc_estructura"]].copy()
print("=== META ===")
print(meta.to_string(index=False))

sub = c[c.kfg.isin(CHILE)].copy()
print("\n=== cuerdas por quipu ===")
print(sub.groupby("kfg").size().reindex(CHILE).to_string())

# nudos parse: tipo de nudo y direccion
def parse_kn(nudos):
    types, dirs, nclusters = [], set(), 0
    if not isinstance(nudos, str) or nudos.strip() == "":
        return types, dirs, nclusters
    for cl in nudos.split(";"):
        cl = cl.strip()
        if not cl or "(" not in cl:
            continue
        nclusters += 1
        head = cl.split(")")[0]        # e.g. "3S(7.5,U"
        if "(" in head:
            knob = head.split("(")[0]  # "3S"
        else:
            knob = head
        # knob = digits + letters
        letters = "".join(ch for ch in knob if ch.isalpha())
        if letters:
            types.append(letters)
        after = cl.split(")", 1)
        if len(after) > 1:
            inner = after[0].split("(")[1]
            parts = inner.split(",")
            if len(parts) > 1:
                dirs.add(parts[1].strip())
    return types, dirs, nclusters

rows = []
for kfg, grp in sub.groupby("kfg"):
    n = len(grp)
    ncol = grp.color.nunique()
    col_dom = grp.color.value_counts().head(3)
    vv = pd.to_numeric(grp.valor, errors="coerce")
    # nudos vacios
    vac = (grp.nudos.isna()) | (grp.nudos.astype(str).str.strip() == "")
    nv0 = ((vv == 0) & vac).sum()
    pos = vv[vv > 0]
    kn_types, dirs, ncl = [], set(), 0
    for kn in grp.nudos:
        t, d, nc = parse_kn(kn)
        kn_types += t
        dirs |= d
        ncl += nc
    tops = (grp.union.astype(str).str.upper() == "T").sum()
    RV = grp.union.astype(str).str.upper().isin(["R", "V"])
    rows.append(dict(kfg=kfg, n_cuerdas=n, n_niveles=grp.nivel.nunique(),
        prof=grp.nivel.max(), n_grupos=grp.grupo.nunique(),
        n_colores=ncol, color_top="|".join(col_dom.index.astype(str)),
        color_top_n="|".join(col_dom.values.astype(str)),
        vmin=pos.min() if len(pos) else np.nan, vmax=pos.max() if len(pos) else np.nan,
        n_ceros_reales=int((vv == 0).sum() - nv0), n_sin_nudos=int(vv.isna().sum()) + int(vv.fillna(0).eq(0).sum()) - int((vv == 0).sum()),
        n_nudos_clusters=ncl, torsion="|".join(sorted(grp.torsion.dropna().astype(str).unique())),
        union_set="|".join(sorted(grp.union.dropna().astype(str).unique())),
        n_top_t=int(tops), n_RV=int(RV.sum()), n_R=int((grp.union.astype(str).str.upper()=="R").sum()),
        n_V=int((grp.union.astype(str).str.upper()=="V").sum()),
        kn_types_top="|".join(pd.Series(kn_types).value_counts().head(4).index.astype(str)),
        dirs="|".join(sorted(dirs))))
D = pd.DataFrame(rows)
print("\n=== RESUMEN POR QUIPU ===")
pd.set_option("display.width", 250, "display.max_columns", 50)
print(D.to_string(index=False))
D.to_csv(os.path.join(OUT, "resumen_quipus.csv"), index=False)

# sumas: presencia de cuerdas superiores / valores que son suma
print("\n=== cuerdas superiores (union T) y su valor ===")
top = sub[sub.union.astype(str).str.upper()=="T"]
for kfg, grp in top.groupby("kfg"):
    print(kfg, list(zip(grp.cuerda, grp.valor)))
