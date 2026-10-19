import sqlite3, pandas as pd
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 200)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cords = pd.read_sql("SELECT * FROM cord WHERE KHIPU_ID=1000096", con)
print("CORD_CLASSIFICATION:", cords.CORD_CLASSIFICATION.value_counts(dropna=False).to_dict())
print("ATTACHMENT_TYPE:", cords.ATTACHMENT_TYPE.value_counts(dropna=False).to_dict())
print("CORD_LEVEL:", cords.CORD_LEVEL.value_counts(dropna=False).to_dict())
print("n clusters:", cords.CLUSTER_ID.nunique())
cc = pd.read_sql("SELECT * FROM cord_cluster WHERE KHIPU_ID=1000096", con)
print("cord_cluster cols:", cc.columns.tolist())
print("n clusters rows:", len(cc))
print(cc.head(10).to_string())
# grouping_class
try:
    gc = pd.read_sql("SELECT * FROM grouping_class_dc", con)
    print("grouping_class_dc:", gc.head(20).to_string())
except Exception as e: print(e)
con.close()
