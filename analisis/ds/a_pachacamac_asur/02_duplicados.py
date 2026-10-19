# -*- coding: utf-8 -*-
"""02 - Duplicados de objeto (mismo quipu con varios nombres) y colores globales."""
from pathlib import Path
import pandas as pd

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"

q = pd.read_csv(DAT / "quipus.csv")
m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
sub = q[m & q["kfg"].str.startswith(("AS", "UR"))].copy()

okr = pd.read_csv(RAIZ / "data/external/open-khipu-repository/data/okr-kh-numbers.csv")
# normalizar
okr["OKR Number"] = okr["OKR Number"].astype(str).str.strip()

# mapa: para cada kfg nuestro, su okr number oficial
# intentos: (a) columna okr de quipus.csv ya trae KH; (b) buscar kfg en Other Names
name2okr = {}
for _, r in okr.iterrows():
    others = [x.strip() for x in str(r["Other Names"]).split(",") if x.strip()]
    for o in others:
        name2okr.setdefault(o, set()).add(r["OKR Number"])

filas = []
for _, r in sub.iterrows():
    k = r["kfg"]
    o = str(r["okr"]).strip()
    okrs = set()
    if o.startswith("KH"):
        okrs.add(o)
    if k in name2okr:
        okrs |= name2okr[k]
    filas.append((k, o, ",".join(sorted(okrs))))
mp = pd.DataFrame(filas, columns=["kfg", "okr_quipus", "okr_okrfile"])
print("Quipus sin OKR KH resoluble:", (mp["okr_okrfile"] == "").sum())
print(mp[mp["okr_okrfile"] == ""][["kfg", "okr_quipus"]].to_string(index=False))
print()

# colisiones: varios kfg -> mismo OKR KH
from collections import defaultdict
rev = defaultdict(list)
for _, r in mp.iterrows():
    if r["okr_okrfile"]:
        for x in r["okr_okrfile"].split(","):
            rev[x].append(r["kfg"])
col = {k: v for k, v in rev.items() if len(v) > 1}
print("Colisiones de OKR Number entre nuestros quipus:")
for k, v in col.items():
    print("  ", k, "->", v)

# AS101 part1/part2
print()
print("AS101 partes okr:", mp[mp["kfg"].str.contains("AS101")].to_string(index=False))

# ¿alguna pareja comparte museo + numero de coleccion? revisar Other Names con varios AS/UR
print()
print("OKR entries cuyos Other Names contienen >=2 de nuestros ids:")
ids = set(sub["kfg"])
for _, r in okr.iterrows():
    others = {x.strip() for x in str(r["Other Names"]).split(",") if x.strip()}
    inter = others & ids
    if len(inter) >= 2:
        print("  ", r["OKR Number"], sorted(inter))
