"""
Construye la tabla a nivel de QUIPU que usan los demas scripts.

Fuentes:
  - data/external/open-khipu-repository/data/khipu.db  (OKR: canuto, canutito,
    canuto_cluster, cord.FIBER, primary_cord.FIBER, khipu_main)
  - data/external/data-science-khipu-article/data/khipu_summary.csv (KFG: 650 quipus)
  - analisis/datos/quipus.csv (metadatos ya preparados por el equipo)

Salida: quipus.csv en esta carpeta (una fila por quipu).
"""
import sqlite3, os
import numpy as np
import pandas as pd

BASE = r"."
DB = os.path.join(BASE, "data", "external", "open-khipu-repository", "data", "khipu.db")
KFG = os.path.join(BASE, "data", "external", "data-science-khipu-article", "data", "khipu_summary.csv")
OUT = os.path.dirname(os.path.abspath(__file__))

con = sqlite3.connect(DB)

# ---------------------------------------------------------------- OKR por quipu
cord = pd.read_sql("select * from cord", con)
pc = pd.read_sql("select * from primary_cord", con)
km = pd.read_sql("select * from khipu_main", con)
can = pd.read_sql("select * from canuto", con)
canit = pd.read_sql("select * from canutito", con)
clu = pd.read_sql("select * from canuto_cluster", con)

# canutito trae KHIPU_ID=0 en toda la tabla: se recupera por CORD_ID
canit = canit.drop(columns=["KHIPU_ID"]).merge(
    cord[["CORD_ID", "KHIPU_ID"]], on="CORD_ID", how="left")

okr = km[["KHIPU_ID", "OKR_NUM", "PROVENANCE", "REGION", "MUSEUM_NAME",
          "NICKNAME", "EARLIEST_AGE", "LATEST_AGE"]].copy()
okr["okr"] = okr.OKR_NUM.astype(str).str.strip()

fib = (cord.assign(es_CN=(cord.FIBER == "CN"), es_CL=(cord.FIBER == "CL"),
                   es_mezcla=(cord.FIBER.isin(["CC", "CW", "AH", "H", "W"])))
          .groupby("KHIPU_ID")
          .agg(n_cord=("CORD_ID", "size"),
               n_CN=("es_CN", "sum"), n_CL=("es_CL", "sum"),
               n_mezcla=("es_mezcla", "sum"),
               n_fibra_NA=("FIBER", lambda s: s.isna().sum() + (s == "").sum())))

# atributos de las cuerdas (para comparar fibras dentro de quipu)
cord["valor_n"] = pd.to_numeric(cord["ATTACH_POS"], errors="coerce")  # placeholder
okr = okr.merge(fib, on="KHIPU_ID", how="left")

okr["n_canuto"] = okr.KHIPU_ID.map(can.groupby("KHIPU_ID").size()).fillna(0).astype(int)
okr["n_canuto_cluster"] = okr.KHIPU_ID.map(clu.groupby("KHIPU_ID").size()).fillna(0).astype(int)
okr["n_cord_en_canuto"] = okr.KHIPU_ID.map(
    can.groupby("KHIPU_ID").NUM_CORDS.sum()).fillna(0).astype(int)
okr["n_canutito"] = okr.KHIPU_ID.map(canit.groupby("KHIPU_ID").size()).fillna(0).astype(int)
okr["n_cord_con_canutito"] = okr.KHIPU_ID.map(
    canit.groupby("KHIPU_ID").CORD_ID.nunique()).fillna(0).astype(int)

pc_f = pc.groupby("KHIPU_ID").FIBER.agg(lambda s: s.iloc[0] if len(s) else None)
okr["pc_fibra"] = okr.KHIPU_ID.map(pc_f)
pc_s = pc.groupby("KHIPU_ID").STRUCTURE.agg(lambda s: s.iloc[0] if len(s) else None)
okr["pc_estructura"] = okr.KHIPU_ID.map(pc_s)

# ---------------------------------------------------------------- KFG
kfg = pd.read_csv(KFG, low_memory=False)
kfg["okr"] = kfg.okr_name.astype(str).str.strip()
keep = ["okr", "kfg_name", "num_cords", "num_pendant_cords", "num_subsidiary_cords",
        "num_canuto_cords", "num_ascher_colors", "mean_cord_value", "knot_cluster_count",
        "knot_count", "percent_s_knots", "percent_z_knots", "num_s_cords", "num_z_cords",
        "num_banded_clusters", "num_seriated_clusters", "num_decreasing_clusters",
        "r_ratio", "v_ratio", "benford_match", "num_top_cords"]
kfg = kfg[keep].copy()
kfg["prop_canuto"] = kfg.num_canuto_cords / kfg.num_cords.replace(0, np.nan)

d = kfg.merge(okr, on="okr", how="left", suffixes=("", "_okr"))
print("KFG quipus:", len(kfg), " con match OKR:", d.KHIPU_ID.notna().sum())

# procedencia normalizada (solo para agrupar; NO se usa como lugar de origen)
def norm(s):
    if pd.isna(s):
        return "desconocida"
    s = str(s).lower().replace('"', "").strip()
    if s in ("", "unknown", "nan"):
        return "desconocida"
    if "incahuasi" in s:
        return "Incahuasi"
    if "armatambo" in s or "san pedro" in s:
        return "Armatambo"
    if "leymebamba" in s:
        return "Leymebamba"
    if "pachacamac" in s:
        return "Pachacamac"
    if "arica" in s or "lluta" in s or "playa miller" in s:
        return "Arica/Lluta"
    if "puruchuco" in s or "la molina" in s:
        return "Puruchuco"
    if "ica" in s or "ocucaje" in s or "callango" in s:
        return "Ica/Ocucaje"
    if "nazca" in s:
        return "Nazca"
    if "paracas" in s or "pisco" in s:
        return "Paracas/Pisco"
    if "santa" in s:
        return "Santa"
    if "huari" in s:
        return "Huari"
    if "cusco" in s or "cuzco" in s:
        return "Cusco"
    return "otra/incierta"

d["proc"] = d.PROVENANCE.where(d.PROVENANCE.notna(), d.get("provenance"))
d["zona"] = d.proc.map(norm)

d.to_csv(os.path.join(OUT, "quipus.csv"), index=False)
print(d.shape)
print(d[["prop_canuto", "n_canuto", "n_canutito", "n_CL", "n_CN"]].describe().round(3).to_string())
print(d.zona.value_counts().to_string())
