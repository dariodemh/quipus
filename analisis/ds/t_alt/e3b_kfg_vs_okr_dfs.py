"""Ordena las cuerdas OKR en DFS (hijos por CORD_ID, que sigue el orden de transcripcion)
y las empareja 1-a-1 con las cuerdas KFG ordenadas por `orden`.
Comprueba la calidad del alineamiento y mide el desacuerdo de valor.
"""
import sqlite3
from pathlib import Path
import pandas as pd, numpy as np

RAIZ = Path(__file__).resolve().parents[3]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
q = pd.read_csv(RAIZ/"analisis/datos/quipus.csv", dtype=str, keep_default_na=False)
con = sqlite3.connect(f"file:{RAIZ}/data/external/open-khipu-repository/data/khipu.db?mode=ro", uri=True)
kid = {r[0]: r[1] for r in con.execute("select OKR_NUM, KHIPU_ID from khipu_main")}

cords = pd.read_sql_query("select KHIPU_ID,CORD_ID,CORD_ORDINAL,PENDANT_FROM from cord", con)
knots = pd.read_sql_query(
    "select CORD_ID, TYPE_CODE, DIRECTION, knot_value_type, NUM_TURNS from knot", con)
# aporte = knot_value_type si != 0; si es 0, NUM_TURNS (nudos largos sin valor codificado)
kv = knots.knot_value_type.fillna(0)
ap = np.where(kv != 0, kv, knots.NUM_TURNS.fillna(0))
# un nudo S vale knot_value_type; un L/E vale su numero de vueltas si knot_value_type falta
knots["ap"] = ap
Vk = knots.groupby("CORD_ID").agg(v=("ap", "sum"), nk=("ap", "size"),
                                  nU=("DIRECTION", lambda s: (s == "U").sum()))

def dfs_order(g):
    g = g.copy()
    ch = {p: s for p, s in g.groupby("PENDANT_FROM")}
    roots = g[~g.PENDANT_FROM.isin(g.CORD_ID)].sort_values("CORD_ORDINAL")
    # el cordon principal es un 'padre' que no esta en la lista de cuerdas
    out = []
    def rec(cid):
        out.append(cid)
        sub = ch.get(cid)
        if sub is not None:
            for c in sub.sort_values("CORD_ID").CORD_ID:
                rec(c)
    for r in roots.CORD_ID:
        rec(r)
    return out

pares = []
for kfg, o in zip(q.kfg, q.okr):
    k = kid.get(o)
    if k is None:
        continue
    a = d[d.kfg == kfg].assign(o=pd.to_numeric(d[d.kfg == kfg].orden, errors="coerce")).sort_values("o")
    g = cords[cords.KHIPU_ID == k]
    if len(a) == 0 or len(a) != len(g):
        continue
    seq = dfs_order(g)
    b = pd.DataFrame(dict(cuerda_okr=seq)).join(Vk, on="cuerda_okr")
    b["orden"] = np.arange(len(b))
    a["oidx"] = np.arange(len(a))
    m = a[["oidx", "orden", "cuerda", "valor"]].merge(b, left_on="oidx", right_on="orden", suffixes=("", "_okr"))
    m["kfg"] = kfg
    pares.append(m)
P = pd.concat(pares, ignore_index=True)
P["v_kfg"] = pd.to_numeric(P.valor, errors="coerce").fillna(0)
P["dif"] = P.v.where(P.v.notna(), 0) - P.v_kfg
for c in ["nk", "nU"]:
    P[c] = P[c].fillna(0)
print("quipus:", P.kfg.nunique(), "cuerdas:", len(P))
print("identicas:", (P.dif == 0).sum(), f"({100*(P.dif==0).mean():.2f}%)")
print(P.dif.abs().describe(percentiles=[.5,.75,.9,.95,.99]).to_string())
print("\n-- solo cuerdas con >=2 nudos en ambas --")
print("(pendiente)")
print("\n-- por quipu --")
g = P.groupby("kfg").apply(lambda x: (x.dif != 0).mean(), include_groups=False)
print(g.describe(percentiles=[.5,.75,.9]).to_string())
print("quipus 100% identicos:", (g == 0).sum(), "de", len(g))
print("\n-- ejemplos --")
print(P[P.dif != 0][["kfg", "cuerda", "valor", "v", "nk", "nU"]].head(12).to_string(index=False))
P.to_csv(Path(__file__).parent/"kfg_vs_okr_cuerdas.csv", index=False)
