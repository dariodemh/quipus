import sqlite3, pandas as pd, numpy as np
pd.set_option('display.width', 240)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
k = pd.read_sql("SELECT * FROM knot LIMIT 3", con)
print("knot cols:", k.columns.tolist())
cords = pd.read_sql("SELECT CORD_ID FROM cord WHERE KHIPU_ID=1000096", con)
ids = tuple(int(x) for x in cords.CORD_ID)
q = f"SELECT * FROM knot WHERE CORD_ID IN {ids}"
kk = pd.read_sql(q, con)
print("n knots:", len(kk))
for c in kk.columns:
    vc = kk[c].value_counts(dropna=False)
    if len(vc) <= 12: print(c, ":", vc.to_dict())
kt = pd.read_sql("SELECT * FROM knot_type_dc", con)
print("knot_type_dc:\n", kt.to_string())
kc = pd.read_sql(f"SELECT * FROM knot_cluster WHERE CORD_ID IN {ids}", con)
print("knot_cluster cols:", kc.columns.tolist(), "n:", len(kc))
for c in kc.columns:
    vc = kc[c].value_counts(dropna=False)
    if len(vc)<=12: print(c,":",vc.to_dict())
con.close()
