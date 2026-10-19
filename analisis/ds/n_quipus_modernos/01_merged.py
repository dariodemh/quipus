# -*- coding: utf-8 -*-
"""Construye una tabla de cuerdas unida KFG <-> OKR, con color grueso y
atributos de OKR (twist, fibra, attachment, canuto). Solo lectura del OKR.
Salida: cuerdas_merged.csv (en esta carpeta)."""
import sqlite3
import re
import numpy as np
import pandas as pd

BASE = r"."
DB = BASE + r"\data\external\open-khipu-repository\data\khipu.db"

c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv").drop_duplicates(["kfg", "cuerda"])
s = pd.read_csv(BASE + r"\data\external\data-science-khipu-article\data\khipu_summary.csv")

# KFG -> KH (okr_name) -> KHIPU_ID
kfg2kh = dict(zip(s.kfg_name, s.okr_name))
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
km = pd.read_sql("select KHIPU_ID, OKR_NUM from khipu_main", con)
kh2kid = dict(zip(km.OKR_NUM, km.KHIPU_ID))
co = pd.read_sql(
    "select KHIPU_ID, CORD_ORDINAL, TWIST, FIBER, ATTACHMENT_TYPE, "
    "CANUTO_ORDINAL, CORD_LEVEL, CORD_LENGTH from cord", con)
col = pd.read_sql("select AS_COLOR_CD, COLOR from ascher_color_dc", con)
con.close()

c["okr"] = c.kfg.map(kfg2kh)
c["kid"] = c.okr.map(kh2kid)

# color grueso: primer codigo Ascher -> clase ISCC-NBS (A blanco, B marron,
# G verde, H azul, L oliva, M gris, N naranja, R rojo, Y amarillo, Z negro)
code2fam = dict(zip(col.AS_COLOR_CD.str.strip(), col.COLOR.str.strip()))


def fam(raw):
    if not isinstance(raw, str):
        return None
    first = re.split(r"[:/\-()]", raw)[0].strip()
    first = first.replace("%", "").strip()
    return code2fam.get(first, None)


c["colfam"] = c.color.map(fam)
c["n_colores_cuerda"] = c.color.fillna("").map(
    lambda x: len([z for z in re.split(r"[:/\-]", x) if z.strip()]) if x else 0)

co = co.drop_duplicates(["KHIPU_ID", "CORD_ORDINAL"])
j = c.merge(co, left_on=["kid", "orden"], right_on=["KHIPU_ID", "CORD_ORDINAL"],
            how="left", suffixes=("", "_okr"))
j = j.drop_duplicates(["kfg", "cuerda"])

# unificar torsion: KFG y OKR; usamos OKR si KFG es U/NaN
j["twist"] = j["torsion"].where(j["torsion"].isin(["S", "Z"]), j["TWIST"])
j["twist"] = j["twist"].where(j["twist"].isin(["S", "Z"]), None)

# direccion de nudos por cuerda: mayoria S/Z entre los nudos con direccion
def dir_may(s):
    if not isinstance(s, str):
        return None, 0, 0
    ds = re.findall(r"\(([-\d.]+),([SZU])\)", s)
    ss = sum(1 for _, d in ds if d == "S")
    zz = sum(1 for _, d in ds if d == "Z")
    if ss + zz == 0:
        return None, 0, 0
    return ("S" if ss >= zz else "Z"), ss, zz


dm = j.nudos.map(dir_may)
j["dir"] = [x[0] for x in dm]
j["dir_s"] = [x[1] for x in dm]
j["dir_z"] = [x[2] for x in dm]

j["canuto"] = (j.CANUTO_ORDINAL.fillna(0) > 0).astype(int)
j["fibra"] = j.FIBER.fillna("")
j["attach"] = j.ATTACHMENT_TYPE.fillna("")

keep = ["kfg", "okr", "kid", "orden", "cuerda", "nivel", "padre", "grupo",
        "valor", "alt", "nudos", "color", "colfam", "n_colores_cuerda",
        "torsion", "twist", "union", "attach", "largo", "CORD_LENGTH",
        "fibra", "canuto", "dir", "dir_s", "dir_z", "notas"]
j[keep].to_csv("cuerdas_merged.csv", index=False)
print("filas", len(j), "quipus", j.kfg.nunique(), "con OKR", j.kid.notna().sum())
print("twist S/Z", j.twist.notna().sum(), "colfam", j.colfam.notna().sum())
print("canutos", j.canuto.sum(), "quipus con canuto", j[j.canuto == 1].kfg.nunique())
print("direccion S/Z", j.dir.notna().sum())
print(j.colfam.value_counts(dropna=False).to_string())
