"""SUPERSEDIDO por e3b (el valor OKR no esta en knot_cluster.TOTAL_VALUE, que
esta vacio, sino en knot.knot_value_type / NUM_TURNS). Se conserva solo como
registro de la exploracion.
"""
"""Comparacion de transcripciones KFG (cuerdas.csv) vs OKR (khipu.db) para los
quipus con el mismo numero de cuerdas. Da la tasa EMPIRICA de desacuerdo de
transcripcion a nivel de cuerda, sin necesidad de la columna `alt` (vacia).
"""
import sqlite3, re
from pathlib import Path
import pandas as pd, numpy as np

RAIZ = Path(__file__).resolve().parents[3]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
q = pd.read_csv(RAIZ/"analisis/datos/quipus.csv", dtype=str, keep_default_na=False)
con = sqlite3.connect(f"file:{RAIZ}/data/external/open-khipu-repository/data/khipu.db?mode=ro", uri=True)

kid = {r[0]: r[1] for r in con.execute("select OKR_NUM, KHIPU_ID from khipu_main")}
# valor OKR por cuerda = suma de TOTAL_VALUE de sus racimos
val = pd.read_sql_query(
    "select c.KHIPU_ID, c.CORD_ID, c.CORD_ORDINAL, "
    "coalesce(sum(case when k.TYPE_CODE='S' then k.knot_value_type "
    "                  else coalesce(k.NUM_TURNS,0) end),0) as v_okr, "
    "count(k.KNOT_ID) as nk_okr "
    "from cord c left join knot k on k.CORD_ID=c.CORD_ID group by c.CORD_ID", con)
# direccion desconocida por cuerda
dirs = pd.read_sql_query(
    "select CORD_ID, sum(case when DIRECTION='U' then 1 else 0 end) as nU, count(*) as nk "
    "from knot group by CORD_ID", con)
val = val.merge(dirs, on="CORD_ID", how="left")
val["nU"] = val.nU.fillna(0)

d["v"] = pd.to_numeric(d.valor, errors="coerce").fillna(0)
d["orden_i"] = pd.to_numeric(d.orden, errors="coerce")

pares = []
for kfg, o in zip(q.kfg, q.okr):
    k = kid.get(o)
    if k is None:
        continue
    a = d[d.kfg == kfg].sort_values("orden_i")
    b = val[val.KHIPU_ID == k].sort_values("CORD_ORDINAL")
    if len(a) == 0 or len(a) != len(b):
        continue
    pares.append(pd.DataFrame(dict(kfg=kfg, cuerda=a.cuerda.values, v_kfg=a.v.values,
                                   v_okr=b.v_okr.values.astype(float), nU=b.nU.values,
                                   nk=b.nk.values)))
P = pd.concat(pares, ignore_index=True)
P["dif"] = P.v_okr - P.v_kfg
print("quipus con mismo n de cuerdas:", P.kfg.nunique(), " cuerdas:", len(P))
print("cuerdas con valor identico:", (P.dif == 0).sum(), f"({100*(P.dif==0).mean():.2f}%)")
print("desacuerdo:", (P.dif != 0).sum(), f"({100*(P.dif!=0).mean():.2f}%)")
print("\n-- |dif| cuantiles --")
print(P.dif.abs().describe(percentiles=[.5,.75,.9,.95,.99]).to_string())
print("\n-- desacuerdo por quipu (fraccion de cuerdas) --")
g = P.groupby("kfg").apply(lambda x: (x.dif != 0).mean(), include_groups=False)
print(g.describe(percentiles=[.5,.75,.9]).to_string())
print("quipus 100% identicos:", (g == 0).sum(), "de", len(g))
print("\n-- ejemplos de desacuerdo --")
print(P[P.dif != 0].head(15).to_string(index=False))
P.to_csv(Path(__file__).parent/"kfg_vs_okr_cuerdas.csv", index=False)
