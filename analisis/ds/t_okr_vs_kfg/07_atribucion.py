# -*- coding: utf-8 -*-
"""Atribucion de cada discrepancia: comparar racimo a racimo KFG vs OKR."""
import os, re, sqlite3
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
DB = os.path.join(ROOT, "data", "external", "open-khipu-repository", "data", "khipu.db")
RE_NUDO = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")


def kfg_racimos(s):
    out = []
    if not isinstance(s, str):
        return out
    for rac in s.split(";"):
        m = RE_NUDO.search(rac.strip())
        if m:
            out.append((float(m.group(3)), m.group(2), int(m.group(1)), float(m.group(5))))
    return out


con = sqlite3.connect(DB)
kn = pd.read_sql("select CORD_ID,TYPE_CODE,knot_value_type,NUM_TURNS,CLUSTER_ID from knot", con)
kc = pd.read_sql("select CORD_ID,CLUSTER_ID,ORDINAL,START_POS from knot_cluster", con)
con.close()
kn["val"] = pd.to_numeric(kn.knot_value_type, errors="coerce").fillna(0)
falta = (kn.val <= 0) & kn.TYPE_CODE.isin(["L", "LL"]) & (kn.NUM_TURNS > 0)
kn.loc[falta, "val"] = kn.loc[falta, "NUM_TURNS"]
kc = kc.merge(kn.groupby("CLUSTER_ID").agg(val=("val", "sum"), nk=("val", "size")),
              on="CLUSTER_ID", how="left")
kc["val"] = kc.val.fillna(0)
kc = kc.sort_values(["CORD_ID", "ORDINAL"])

d = pd.read_csv(os.path.join(SAL, "discrepancias_valor.csv"))
okr_by = {cid: g for cid, g in kc.groupby("CORD_ID")}

filas = []
for _, r in d.iterrows():
    kr = kfg_racimos(r.nudos)
    g = okr_by.get(int(r.CORD_ID))
    ov = list(g.val) if g is not None else []
    op = list(g.START_POS) if g is not None else []
    kv = [x[3] for x in kr]
    if len(kv) == len(ov):
        ratio10 = sum(1 for a, b in zip(kv, ov) if a > 0 and b > 0 and
                      (abs(b / a - 10) < 1e-9 or abs(a / b - 10) < 1e-9))
        if ratio10:
            causa = "factor10"
        elif len(kv) == 0:
            causa = "sin_datos"
        else:
            causa = "mismo_n_racimos_otro"
    elif len(kv) > len(ov):
        causa = "KFG_mas_racimos"
    else:
        causa = "OKR_mas_racimos"
    filas.append(dict(kfg=r.kfg, cuerda=r.cuerda, CORD_ID=int(r.CORD_ID),
                      valor=r.valor, valor_okr=r.valor_okr, delta=r.delta,
                      kfg_rac=kv, okr_rac=ov, causa=causa))

res = pd.DataFrame(filas)
res.to_csv(os.path.join(SAL, "atribucion.csv"), index=False)
print(res.causa.value_counts().to_string())
print()
print(pd.crosstab(res.causa, res.delta.apply(lambda x: "positivo" if x > 0 else "negativo")).to_string())
print()
print("factor10 por prefijo:")
res["prefijo"] = list(res.kfg.str.extract(r"^([A-Z]+)")[0])
print(pd.crosstab(res.prefijo, res.causa).to_string())
