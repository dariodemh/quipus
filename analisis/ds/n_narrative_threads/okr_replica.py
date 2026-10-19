# -*- coding: utf-8 -*-
"""Réplica en OKR (khipu.db, solo lectura) de los resultados estructurales:
pureza de torsión y unión, y asociación unión V x nudo S estratificada."""
import sqlite3
import numpy as np
import pandas as pd

DB = "file:data/external/open-khipu-repository/data/khipu.db?mode=ro"
con = sqlite3.connect(DB, uri=True)
cord = pd.read_sql("select KHIPU_ID,CORD_ID,ATTACHMENT_TYPE,TWIST,CORD_LEVEL from cord where CORD_LEVEL=1", con)
print("cuerdas nivel 1:", len(cord), "| quipus:", cord.KHIPU_ID.nunique())
print("union:", cord.ATTACHMENT_TYPE.value_counts().head(6).to_dict())
print("torsion:", cord.TWIST.value_counts().head(5).to_dict())

for col in ["TWIST", "ATTACHMENT_TYPE"]:
    x = cord[cord[col].isin(["S", "Z", "R", "V"])]
    pur = x.groupby("KHIPU_ID")[col].agg(lambda s: s.value_counts(normalize=True).iloc[0])
    print(f"{col}: pureza mediana={pur.median():.3f}; quipus con >1 categoría={int((x.groupby('KHIPU_ID')[col].nunique()>1).sum())}/{len(pur)}")

kn = pd.read_sql("""select c.KHIPU_ID,k.CORD_ID,k.TYPE_CODE,k.DIRECTION,
                           c.ATTACHMENT_TYPE
                    from knot k join cord c on k.CORD_ID=c.CORD_ID
                    where c.CORD_LEVEL=1""", con)
kn = kn[kn.DIRECTION.isin(["S", "Z"]) & kn.ATTACHMENT_TYPE.isin(["R", "V"])]
kn["S"] = (kn.DIRECTION == "S").astype(int)
kn["V"] = (kn.ATTACHMENT_TYPE == "V").astype(int)
print("nudos:", len(kn), "| S:", round(kn.S.mean(), 3))


def cmh(df, strata, min_n=6):
    rows = []
    for key, x in df.groupby(strata):
        if len(x) < min_n or x.S.nunique() < 2 or x.V.nunique() < 2:
            continue
        A = int(((x.S == 1) & (x.V == 1)).sum())
        B = int((x.S == 1).sum()) - A
        C = int((x.V == 1).sum()) - A
        D = len(x) - A - B - C
        rows.append((len(x), A, B, C, D))
    t = pd.DataFrame(rows, columns=["n", "A", "B", "C", "D"])
    ormh = (t.A * t.D / t.n).sum() / (t.B * t.C / t.n).sum()
    o = t.A.sum(); e = (t.A + t.B).sum() * (t.A + t.C).sum() / t.n.sum()
    return ormh, len(t), o, e


for strata in [["KHIPU_ID"], ["KHIPU_ID", "TYPE_CODE"]]:
    print(strata, cmh(kn, strata))
