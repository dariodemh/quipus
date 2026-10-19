# -*- coding: utf-8 -*-
"""UR006: reconstruccion de estructura. Salidas a estructura_*.csv y resumen corto."""
import pandas as pd, numpy as np, os, re

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "k_UR006")
dat = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"))
gru = pd.read_csv(os.path.join(BASE, "analisis", "datos", "grupos.csv"))
qui = pd.read_csv(os.path.join(BASE, "analisis", "datos", "quipus.csv"))

u = dat[dat.kfg == "UR006"].copy().sort_values("orden").reset_index(drop=True)
g = gru[gru.kfg == "UR006"].copy()

# metadatos
meta = qui[qui.kfg == "UR006"].iloc[0]
print("META:", meta.to_dict())

# pendants (nivel 0) numerados pN -> indice
u["pnum"] = u["cuerda"].str.extract(r"^p(\d+)$").astype(float)

# mapear grupo a cada pendiente por rango desde..hasta
grp_of = {}
for _, r in g.iterrows():
    for i in range(int(r["desde"]), int(r["hasta"]) + 1):
        grp_of[i] = int(r["grupo"])
u["root_p"] = u["cuerda"].str.extract(r"^p(\d+)").astype(float)
u["grupo_g"] = u["root_p"].map(grp_of)

# numero de nivel0
print("N pendants nivel0:", (u.nivel == 0).sum(), " grupos:", g.grupo.nunique())

# estructura por grupo
rows = []
for gid, sub in u.groupby("grupo_g"):
    pend = sub[sub.nivel == 0]
    subs = sub[sub.nivel > 0]
    rows.append(dict(grupo=gid, n_pend=len(pend), n_subs=len(subs),
                     pends=",".join(pend.cuerda.tolist()),
                     vals=",".join(str(v) for v in pend.valor.tolist())))
est = pd.DataFrame(rows)
est.to_csv(os.path.join(OUT, "estructura_grupos.csv"), index=False)
u.to_csv(os.path.join(OUT, "cuerdas_ur006.csv"), index=False)

print("\n-- grupos: n_pend y n_subs --")
print(est[["grupo", "n_pend", "n_subs"]].to_string(index=False))

# nudos: parsear direccion y tipo
def dirs(s):
    if pd.isna(s): return []
    return re.findall(r"\(([\d.]+),([SZU])\)", s)
def tipos(s):
    if pd.isna(s): return []
    return re.findall(r"\d+([A-Z]+)\(", s)

u["ndir"] = u.nudos.map(lambda s: "".join(d for _, d in dirs(s)))
u["ntip"] = u.nudos.map(lambda s: "|".join(tipos(s)))
print("\n-- direcciones de nudo (global) --")
from collections import Counter
print(Counter("".join(u.ndir.tolist()) if False else [d for s in u.ndir for d in s]).most_common())
