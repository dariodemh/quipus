# -*- coding: utf-8 -*-
"""01 - Descripcion del conjunto AS+UR con procedencia Pachacamac.
Genera salida/tabla_quipus.csv y imprime resumenes compactos."""
import re
from pathlib import Path
import pandas as pd
import numpy as np

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"
OUT.mkdir(exist_ok=True)

q = pd.read_csv(DAT / "quipus.csv")
c = pd.read_csv(DAT / "cuerdas.csv")
g = pd.read_csv(DAT / "grupos.csv")

m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
sub = q[m & q["kfg"].str.startswith(("AS", "UR"))].copy()
ids = sorted(sub["kfg"].tolist())
print("N quipus AS+UR Pachacamac:", len(ids))

cc = c[c["kfg"].isin(ids)].copy()
gg = g[g["kfg"].isin(ids)].copy()
print("N cuerdas:", len(cc), " N grupos:", len(gg))

# --- utilidades ---
def dir_nudos(s):
    """direcciones de nudo presentes en la cadena nudos (S/Z/U dentro de nTIPO(pos,dir))"""
    if not isinstance(s, str):
        return set()
    ds = set(re.findall(r"\(([^,]+),([SZU])\)", s))
    return {d for _, d in ds}

def valor_real(row):
    v = row["valor"]
    if pd.isna(v):
        return np.nan
    if v == 0 and (pd.isna(row["nudos"]) or str(row["nudos"]).strip() == ""):
        return np.nan  # 0 sin nudos = ausente
    return v

# children map: para cada (kfg, cuerda) lista de subsidiarias directas
def es_suma_madre(rows):
    """cuenta cuerdas madre cuyo valor == suma de sus hijas directas (hijas con valor real)"""
    porq = {}
    for _, r in rows.iterrows():
        porq.setdefault(r["cuerda"], []).append(r)
    # hijos directos por padre
    hijos = {}
    for _, r in rows.iterrows():
        p = r["padre"]
        if isinstance(p, str) and p == p:
            hijos.setdefault(p, []).append(r)
    ok = 0
    for madre, hs in hijos.items():
        mr = rows[rows["cuerda"] == madre]
        if len(mr) == 0:
            continue
        vmadre = valor_real(mr.iloc[0])
        if pd.isna(vmadre):
            continue
        vs = [valor_real(h) for h in hs]
        vs = [v for v in vs if not pd.isna(v)]
        if not vs:
            continue
        if abs(sum(vs) - vmadre) < 1e-9:
            ok += 1
    return ok

filas = []
for k in ids:
    rows = cc[cc["kfg"] == k]
    gc = gg[gg["kfg"] == k]
    vals = rows.apply(valor_real, axis=1).dropna()
    colores = rows["color"].dropna().astype(str)
    nudos_str = rows["nudos"].fillna("")
    dirs = set()
    for s in nudos_str:
        dirs |= dir_nudos(s)
    topor = rows[rows["union"] == "T"]
    nsuma = es_suma_madre(rows)
    filas.append(dict(
        kfg=k,
        n_cuerdas=len(rows),
        n_colgantes=int((rows["nivel"] == 0).sum()),
        max_nivel=int(rows["nivel"].max()) if len(rows) else 0,
        n_grupos=len(gc),
        n_color=colores.nunique(),
        color_top=colores.value_counts().index[0] if len(colores) else "",
        color_top_n=int(colores.value_counts().iloc[0]) if len(colores) else 0,
        v_min=vals.min() if len(vals) else np.nan,
        v_max=vals.max() if len(vals) else np.nan,
        v_mediana=vals.median() if len(vals) else np.nan,
        n_sin_nudos=int((nudos_str.str.strip() == "").sum()),
        n_sumas_madre=nsuma,
        n_top_cords=len(topor),
        n_R=int((rows["union"] == "R").sum()),
        n_V=int((rows["union"] == "V").sum()),
        n_S=int((rows["torsion"] == "S").sum()),
        n_Z=int((rows["torsion"] == "Z").sum()),
        n_U_tor=int((rows["torsion"] == "U").sum()),
        dirs=",".join(sorted(dirs)),
        okr=sub[sub["kfg"] == k]["okr"].iloc[0],
        museo=sub[sub["kfg"] == k]["museo"].iloc[0],
    ))
tab = pd.DataFrame(filas).sort_values("n_cuerdas", ascending=False)
tab.to_csv(OUT / "tabla_quipus.csv", index=False)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
print()
print("== Resumen agregado ==")
print(tab[["n_cuerdas", "n_colgantes", "max_nivel", "n_grupos", "v_min", "v_max"]].describe().round(1).to_string())
print()
print("Torsion S total:", tab["n_S"].sum(), " Z:", tab["n_Z"].sum(), " U:", tab["n_U_tor"].sum())
print("Union R total:", tab["n_R"].sum(), " V:", tab["n_V"].sum(), " TopCords:", tab["n_top_cords"].sum(), "n quipus con T:", (tab['n_top_cords']>0).sum())
print("Quipus con >=1 suma madre=hijas:", (tab["n_sumas_madre"] > 0).sum(), "de", len(tab))
print("Cuerdas totales sin nudos:", tab["n_sin_nudos"].sum(), "de", tab["n_cuerdas"].sum())
print("Direcciones de nudo observadas:", tab["dirs"].value_counts().to_dict())
print()
print("== Top 20 quipus por tamano ==")
print(tab.head(20)[["kfg", "n_cuerdas", "n_colgantes", "max_nivel", "n_grupos", "n_color", "color_top", "v_min", "v_max", "n_sin_nudos", "n_sumas_madre", "n_top_cords", "okr"]].to_string(index=False))
