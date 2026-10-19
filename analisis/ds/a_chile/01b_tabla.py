# -*- coding: utf-8 -*-
"""01b: Tabla descriptiva por quipu (norte de Chile)."""
import pandas as pd, numpy as np, os, re, json

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
q = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "quipus.csv"))

CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]
ORD = {k: i for i, k in enumerate(CHILE)}
# procedencia
M = q[q.kfg.isin(CHILE)].set_index("kfg")

def kn_letters(nudos):
    out = []
    if not isinstance(nudos, str):
        return out
    for cl in nudos.split(";"):
        cl = cl.strip()
        if not cl:
            continue
        left = cl.split("(")[0]
        out.append("".join(ch for ch in left if ch.isalpha()))
    return out

def kn_dirs(nudos):
    if not isinstance(nudos, str):
        return []
    return re.findall(r"\(([0-9.]+),([A-Za-z?])", nudos)

rows = []
for kfg, grp in c[c.kfg.isin(CHILE)].groupby("kfg"):
    vv = pd.to_numeric(grp.valor, errors="coerce")
    knall = []
    dirs = []
    for kn in grp.nudos:
        knall += kn_letters(kn)
        dirs += [d for _, d in kn_dirs(kn)]
    pend = grp[grp.nivel == 0]
    vp = pd.to_numeric(pend.valor, errors="coerce")
    vp_pos = vp[vp > 0]
    kc = pd.Series(knall).value_counts()
    dc = pd.Series(dirs).value_counts()
    tcol = grp.color.value_counts()
    # color base (mayusculas antes de : - /)
    base = grp.color.astype(str).str.split(r"[:/\-]").str[0]
    rows.append(dict(
        kfg=kfg, procedencia=M.loc[kfg, "procedencia"],
        n_cuerdas=len(grp), n_pend=len(pend),
        n_subsid=int((grp.nivel > 0).sum()), prof=int(grp.nivel.max()),
        n_grupos=int(grp.grupo.nunique()),
        n_colores=int(grp.color.nunique()),
        color_top=",".join(tcol.head(4).index.astype(str)),
        base_top=",".join(base.value_counts().head(3).index.astype(str)),
        vmin=vp_pos.min() if len(vp_pos) else np.nan,
        vmax=vp_pos.max() if len(vp_pos) else np.nan,
        vmed=round(vp_pos.median(), 1) if len(vp_pos) else np.nan,
        n_v1=int((vp_pos == 1).sum()),
        n_v10=int((vp_pos <= 10).sum()),
        torsion=",".join(sorted(grp.torsion.dropna().astype(str).unique())),
        n_R=int((grp.union.astype(str).str.upper() == "R").sum()),
        n_V=int((grp.union.astype(str).str.upper() == "V").sum()),
        n_T=int((grp.union.astype(str).str.upper() == "T").sum()),
        n_U=int(grp.union.astype(str).str.upper().isin(["U", "UNKNOWN", "?"]).sum()),
        kn_S=int(kc.get("S", 0)), kn_L=int(kc.get("L", 0)),
        kn_E=int(kc.get("E", 0) + kc.get("EE", 0)),
        dir_kn=",".join(f"{k}:{v}" for k, v in dc.head(3).items()),
    ))
D = pd.DataFrame(rows).sort_values("kfg", key=lambda s: s.map(ORD))
pd.set_option("display.width", 300, "display.max_columns", 60)
print(D.to_string(index=False))
D.to_csv(os.path.join(OUT, "tabla_descriptiva.csv"), index=False)
