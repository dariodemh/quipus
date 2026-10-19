import sqlite3, pandas as pd, numpy as np
pd.set_option('display.width', 240)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
k = pd.read_sql("SELECT * FROM knot WHERE KHIPU_ID=1000096", con)
print("knot cols:", k.columns.tolist())
print("n knots:", len(k))
for c in ['KNOT_TYPE_DC_ID','KNOT_DIRECTION','KNOT_DIRECTION_DC_ID','KNOT_ORDINAL','NUM_TURNS','KNOT_VALUE']:
    if c in k.columns: print(c, ":", k[c].value_counts(dropna=False).head(8).to_dict())
# knot_type_dc
kt = pd.read_sql("SELECT * FROM knot_type_dc", con)
print("knot_type_dc:", kt.to_string())
con.close()
