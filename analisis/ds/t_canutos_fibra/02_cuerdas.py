"""
Reconstruye el nombre jerarquico (p3s2...) de cada cuerda OKR caminando
PENDANT_FROM + CORD_ORDINAL, y la une con la tabla KFG `cuerdas.csv`
(que trae valor, nudos, color, largo).  Genera cuerdas_okr.csv.

Validacion: % de quipus/cuerdas con match y comparacion de largo (cm).
"""
import sqlite3, os, re
import numpy as np
import pandas as pd

BASE = r"."
DB = os.path.join(BASE, "data", "external", "open-khipu-repository", "data", "khipu.db")
OUT = os.path.dirname(os.path.abspath(__file__))

con = sqlite3.connect(DB)
cord = pd.read_sql("select CORD_ID,KHIPU_ID,PENDANT_FROM,CORD_ORDINAL,CORD_LEVEL,"
                   "FIBER,CORD_LENGTH,THICKNESS,TWIST,ATTACHMENT_TYPE,TERMINATION,"
                   "CANUTO_ID from cord", con)

# padres: para las cuerdas colgantes el padre es la PC (nivel negativo)
parent_ok = set(cord.CORD_ID)
name = {}

def build(cid, depth=0):
    if cid in name:
        return name[cid]
    r = cord.loc[cid]
    p = r.PENDANT_FROM
    if pd.isna(p) or p not in parent_ok or depth > 8:
        nm = "p%d" % r.CORD_ORDINAL if r.CORD_LEVEL > 0 else "pc%d" % r.CORD_ORDINAL
    else:
        nm = build(p, depth + 1) + "s%d" % r.CORD_ORDINAL
    name[cid] = nm
    return nm

cord = cord.set_index("CORD_ID")
for cid in cord.index:
    try:
        build(cid)
    except Exception:
        name[cid] = "?"
cord = cord.reset_index()
cord["cuerda"] = cord.CORD_ID.map(name)
print("nombres unicos por quipu:",
      (cord.groupby("KHIPU_ID").cuerda.nunique() == cord.groupby("KHIPU_ID").size()).mean())

# ------------------------------------------------------------------ KFG
kf = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"))
q = pd.read_csv(os.path.join(BASE, "analisis", "datos", "quipus.csv"))
kmap = dict(zip(q.kfg, q.okr))
kf["okr"] = kf.kfg.map(kmap)

km = pd.read_sql("select KHIPU_ID,OKR_NUM from khipu_main", con)
idmap = dict(zip(km.OKR_NUM.astype(str).str.strip(), km.KHIPU_ID))
kf["KHIPU_ID"] = kf.okr.astype(str).str.strip().map(idmap)
kf = kf.dropna(subset=["KHIPU_ID"])
kf["KHIPU_ID"] = kf.KHIPU_ID.astype(int)

m = cord.merge(kf[["KHIPU_ID", "cuerda", "valor", "alt", "nudos", "color",
                   "torsion", "union", "largo", "terminacion", "grupo"]],
               on=["KHIPU_ID", "cuerda"], how="left", suffixes=("_okr", "_kfg"))
print("cuerdas OKR:", len(cord), " con match KFG:", m.valor.notna().sum(),
      "(%.1f%%)" % (100 * m.valor.notna().mean()))
print("quipus con >=90%% match:",
      (m.groupby("KHIPU_ID").valor.apply(lambda s: s.notna().mean()) > 0.9).sum(),
      "de", m.KHIPU_ID.nunique())

# validacion de largo: OKR CORD_LENGTH vs KFG largo
v = m.dropna(subset=["largo"])
v = v[(v.CORD_LENGTH > 0) & (v.largo > 0)]
print("correlacion largo OKR vs KFG: %.3f (n=%d)" % (v.CORD_LENGTH.corr(v.largo), len(v)))
print(v[["cuerda", "CORD_LENGTH", "largo"]].head(5).to_string())

m.to_csv(os.path.join(OUT, "cuerdas_okr.csv"), index=False)
print(m.shape)
