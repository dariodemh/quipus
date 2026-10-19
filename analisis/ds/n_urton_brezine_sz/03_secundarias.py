# -*- coding: utf-8 -*-
"""
03_secundarias.py
Cifras secundarias de U&B 2009 (U08-U14) y controles descriptivos:
tamano de khipu por archivo, subsidiarias, fibra, torsion por archivo,
tasa de direccion desconocida (U) y khipus canuto.
"""
import sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = BASE + r"\analisis\ds\n_urton_brezine_sz"
DB = BASE + r"\data\external\open-khipu-repository\data\khipu.db"

quipus = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")
quipus["prov"] = quipus.procedencia.fillna("").str.strip()
quipus.loc[quipus.prov.str.lower().isin(["unknown", ""]), "prov"] = "SIN"
exec(open(OUT + r"\arch12.py", encoding="utf-8").read())
quipus["arch"] = quipus.prov.map(arch12)
quipus.loc[quipus.region.fillna("").str.strip() == "Puruchuco", "arch"] = "Puruchuco"

cuerdas = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cuerdas["arch"] = cuerdas.kfg.map(quipus.set_index("kfg").arch)

L = []
A = L.append
A("=== U08/U09: TAMANO DE KHIPU POR ARCHIVO (KFG, cuerdas.csv) ===")
sz = cuerdas.groupby("kfg").size().rename("n_cuerdas").reset_index()
sz = sz.merge(quipus[["kfg", "arch"]], on="kfg", how="left")
g = sz.groupby("arch").n_cuerdas.agg(["count", "mean", "median", "max", "min"]).round(1)
A(g.loc[[a for a in g.index if a not in ("SIN", "Otros/vago")]].to_string())
A("")
A("Khipus mas grandes (n cuerdas):")
A(sz.sort_values("n_cuerdas", ascending=False).head(8).to_string(index=False))

A("")
A("=== U10: SUBSIDIARIAS ===")
sub = cuerdas[cuerdas.nivel >= 1].groupby("kfg").size().rename("n_sub")
sz2 = sz.merge(sub, on="kfg", how="left").fillna({"n_sub": 0})
A(f"KFG: {int((sz2.n_sub>0).sum())} de {len(sz2)} quipus con >=1 subsidiaria "
  f"({100*(sz2.n_sub>0).mean():.1f}%)")
# solo los 12 archivos
x = sz2[sz2.arch.isin(g.index) & ~sz2.arch.isin(["SIN", "Otros/vago"])]
A(f"KFG, 12 archivos: {int((x.n_sub>0).sum())} de {len(x)} ({100*(x.n_sub>0).mean():.1f}%)")

A("")
A("=== U12: FIBRA (OKR, cord.FIBER) ===")
con = sqlite3.connect(DB)
cord = pd.read_sql("select KHIPU_ID, CORD_ID, FIBER, TWIST from cord", con)
fib = cord.FIBER.fillna("").replace("", "sin dato").value_counts()
A(f"cordeles con fibra registrada: {len(cord)-fib.get('sin dato',0)} de {len(cord)} "
  f"({100*(1-fib.get('sin dato',0)/len(cord)):.1f}%)")
A(fib.head(8).to_string())
known = cord[~cord.FIBER.isna() & (cord.FIBER != "")]
A("Porcentajes entre los conocidos: " + ", ".join(
    f"{k}={100*v/len(known):.1f}%" for k, v in known.FIBER.value_counts().head(6).items()))

A("")
A("=== U14: TORSION POR ARCHIVO (KFG) ===")
tor = cuerdas.assign(t=cuerdas.torsion.fillna("NA").replace("", "NA"))
g2 = tor.groupby(["arch", "t"]).size().unstack(fill_value=0)
for c in ["S", "Z", "U", "NA"]:
    if c not in g2:
        g2[c] = 0
g2["n_ conocido"] = g2.S + g2.Z
g2["pct_Z"] = (100 * g2.Z / g2["n_ conocido"].replace(0, np.nan)).round(1)
A(g2.loc[[a for a in g2.index if a not in ("SIN",) and g2.loc[a, "n_ conocido"] >= 50],
        ["S", "Z", "U", "NA", "n_ conocido", "pct_Z"]].sort_values("pct_Z", ascending=False).to_string())
A("")
A("Torsion y fibra (OKR): Z entre S/Z")
ct = cord[cord.TWIST.isin(["S", "Z"])]
A(ct.groupby("FIBER").TWIST.value_counts().unstack(fill_value=0).assign(
    pct_Z=lambda d: (100 * d.Z / (d.S + d.Z)).round(1)).to_string())
A("")
# excluir Incahuasi y camelidos
inc = set(quipus.loc[quipus.arch == "Incahuasi", "kfg"])
tor2 = tor[~tor.kfg.isin(inc)]
A(f"KFG torsion Z%% sin Incahuasi (n={len(tor2)} cuerdas): "
  f"{100*(tor2.t=='Z').sum()/((tor2.t=='S').sum()+(tor2.t=='Z').sum()):.2f}%")
# KHIPU_ID vs okr no siempre; usar quipus okr->arch
con2 = sqlite3.connect(DB)
km = pd.read_sql("select KHIPU_ID, OKR_NUM from khipu_main", con2)
okcord = cord.merge(km, on="KHIPU_ID").merge(quipus.set_index("okr")[["arch"]], left_on="OKR_NUM", right_index=True, how="left")
for a in ["Incahuasi", "Pachacamac", "Leymebamba"]:
    x = okcord[okcord.arch == a]
    x = x[x.TWIST.isin(["S", "Z"])]
    if len(x):
        A(f"OKR torsion Z% en {a}: {100*(x.TWIST=='Z').mean():.1f}% (n={len(x)})")
cn = okcord[(okcord.FIBER == "CN") & okcord.TWIST.isin(["S", "Z"])]
cl = okcord[(okcord.FIBER == "CL") & okcord.TWIST.isin(["S", "Z"])]
A(f"OKR torsion Z% solo algodon: {100*(cn.TWIST=='Z').mean():.1f}% (n={len(cn)}); "
  f"solo camelido: {100*(cl.TWIST=='Z').mean():.1f}% (n={len(cl)})")

A("")
A("=== TASA DE DIRECCION DESCONOCIDA (U) POR ARCHIVO (KFG) ===")
import re
PAT = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([SZUszu]?)\)")
rows = []
for r in cuerdas.itertuples():
    if not isinstance(r.nudos, str):
        continue
    for m in PAT.finditer(r.nudos):
        t = m.group(2)
        d = (m.group(4) or "U").upper()
        n = int(m.group(1)) if t in ("S", "SP") else 1
        if d not in ("S", "Z"):
            d = "U"
        rows.append((r.kfg, r.arch, t, d, n))
kk = pd.DataFrame(rows, columns=["kfg", "arch", "t", "d", "n"])
g3 = kk.groupby(["arch", "d"]).n.sum().unstack(fill_value=0)
for c in ["S", "Z", "U"]:
    if c not in g3:
        g3[c] = 0
g3["total"] = g3.S + g3.Z + g3.U
g3["pct_U"] = (100 * g3.U / g3.total).round(1)
A(g3.loc[[a for a in g3.index if a not in ("SIN", "Otros/vago") and g3.loc[a, "total"] >= 100],
        ["S", "Z", "U", "total", "pct_U"]].sort_values("pct_U").to_string())

A("")
A("=== KHIPUS CANUTO ===")
d = pd.read_csv(BASE + r"\data\external\data-science-khipu-article\data\khipu_summary.csv")
d["arch"] = d.provenance.fillna("").str.strip().map(arch12)
can = d[d.num_canuto_cords > 0]
A(f"{len(can)} khipus con >=1 cuerda canuto; {int(can.num_canuto_cords.sum())} cuerdas canuto")
A(can.groupby("arch").agg(n=("kfg_name", "count"), canutos=("num_canuto_cords", "sum")).to_string())

with open(OUT + r"\salida_03.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
