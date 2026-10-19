import sqlite3, pandas as pd
pd.set_option('display.width', 240)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("tables:", [r[0] for r in cur.fetchall()])
# find khipu id for KH0082
cur.execute("PRAGMA table_info(khipu_main)")
print("khipu_main cols:", [r[1] for r in cur.fetchall()])
try:
    km = pd.read_sql("SELECT * FROM khipu_main WHERE KHIPU_ID LIKE '%0082%' OR OKR_NUM LIKE '%0082%'", con)
    print(km.T)
except Exception as e:
    print("err", e)
con.close()
