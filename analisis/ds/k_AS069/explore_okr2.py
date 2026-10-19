import sqlite3, pandas as pd
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 300)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
km = pd.read_sql("SELECT * FROM khipu_main WHERE KHIPU_ID=1000096", con)
print("NOTES:", km.NOTES.iloc[0])
print("REGION:", km.REGION.iloc[0], "| COND:", km.CONDITIONOFKHIPU.iloc[0])
# cord table
cords = pd.read_sql("SELECT * FROM cord WHERE KHIPU_ID=1000096", con)
print("cord cols:", cords.columns.tolist())
print("n cords:", len(cords))
print(cords.head(3).T)
print("cord_classification:", cords.CORD_CLASSIFICATION_DC_ID.value_counts(dropna=False).to_dict() if 'CORD_CLASSIFICATION_DC_ID' in cords else 'n/a')
con.close()
