# -*- coding: utf-8 -*-
"""Descriptivo por quipu del conjunto 'Santa' (KH0227, UR087-UR092, UR198).
Imprime tablas cortas y guarda CSV auxiliares en esta carpeta."""
import pandas as pd, re, os

BASE = r"."
DAT = os.path.join(BASE, "analisis", "datos")
OUT = os.path.join(BASE, "analisis", "ds", "a_santa")

IDS = ["KH0227", "UR087", "UR088", "UR089", "UR090", "UR091", "UR092", "UR198"]

cu = pd.read_csv(os.path.join(DAT, "cuerdas.csv"))
gr = pd.read_csv(os.path.join(DAT, "grupos.csv"))
qp = pd.read_csv(os.path.join(DAT, "quipus.csv"))

cu = cu[cu["kfg"].isin(IDS)].copy()
# valor ausente = 0 con nudos vacio
cu["tiene_nudos"] = cu["nudos"].notna() & (cu["nudos"].astype(str).str.strip() != "")
cu["valor_real"] = cu.apply(lambda r: r["valor"] if r["tiene_nudos"] else None, axis=1)

# direcciones y tipos de nudo a partir de la cadena nudos
def parse_nudos(s):
    if not isinstance(s, str) or not s.strip():
        return [], []
    dirs, tipos = [], []
    for m in re.finditer(r"\(([\d.]+),([SZU])\)", s):
        dirs.append(m.group(2))
    for m in re.finditer(r"\d+([A-Z]+)\(", s):
        tipos.append(m.group(1))
    return dirs, tipos

filas = []
for k in IDS:
    d = cu[cu["kfg"] == k]
    g = gr[gr["kfg"] == k]
    dirs, tipos = [], []
    for s in d["nudos"]:
        a, b = parse_nudos(s)
        dirs += a; tipos += b
    vc = d["valor_real"].dropna()
    pend = d[d["nivel"] == 0]
    subs = d[d["nivel"] > 0]
    colors = d["color"].dropna().astype(str)
    # color principal ignorando combinaciones
    ctop = colors.str.replace(r"[:/\-].*", "", regex=True).value_counts()
    filas.append(dict(
        kfg=k, n_cuerdas=len(d), n_pend=len(pend), n_subs=len(subs),
        n_grupos=len(g),
        color_top=";".join(f"{c}:{n}" for c, n in ctop.head(3).items()),
        n_colores=d["color"].nunique(),
        val_min=(vc.min() if len(vc) else None), val_max=(vc.max() if len(vc) else None),
        val_med=(vc.median() if len(vc) else None),
        n_cero_ausente=int((~d["tiene_nudos"]).sum()),
        u_R=int((d["union"] == "R").sum()), u_V=int((d["union"] == "V").sum()),
        u_T=int((d["union"] == "T").sum()),
        u_otro=int(d["union"].isin(["R", "V", "T"]).eq(False).sum()),
        t_S=int((d["torsion"] == "S").sum()), t_Z=int((d["torsion"] == "Z").sum()),
        t_U=int((d["torsion"] == "U").sum()),
        kd_S=dirs.count("S"), kd_Z=dirs.count("Z"), kd_U=dirs.count("U"),
        n_knots=len(dirs),
        termin_S=int((d["terminacion"] == "S").sum()),
        termin_Z=int((d["terminacion"] == "Z").sum()),
        termin_U=int((d["terminacion"] == "U").sum()),
    ))
tab = pd.DataFrame(filas)
pd.set_option("display.width", 260)
print("=== TABLA DESCRIPTIVA POR QUIPU ===")
print(tab.to_string(index=False))
tab.to_csv(os.path.join(OUT, "tabla_descriptiva.csv"), index=False)

# sumas Ascher
sa = pd.read_csv(os.path.join(BASE, "data", "external", "data-science-khipu-article", "data",
                              "ascher_sum_relations", "ascher_sum_relationships.csv"))
sa["n"] = sa["name"].str.extract(r">([^<]+)</a>")
sums = sa[sa["n"].isin(IDS)][["n", "num_banded_clusters", "num_seriated_clusters",
                              "num_pendant_pendant_sum", "num_pendant_pendants_color_sum",
                              "num_indexed_pendant_sum"]]
print("\n=== SUMAS (Ascher) por quipu ===")
print(sums.to_string(index=False))

# estructuras de grupo: tamano de cada grupo
print("\n=== TAMANO DE GRUPOS (n cuerdas por grupo) ===")
gt = gr[gr["kfg"].isin(IDS)].copy()
gt["n"] = gt["hasta"] - gt["desde"] + 1
piv = gt.groupby("kfg")["n"].apply(lambda x: ",".join(map(str, x)))
print(piv.to_string())
gt.to_csv(os.path.join(OUT, "grupos_tamano.csv"), index=False)
