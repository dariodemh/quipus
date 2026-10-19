"""Verificacion OKR de los 10 candidatos: composicion de tipos de nudo."""
import sqlite3, pandas as pd
con=sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
mp=pd.read_csv('analisis/ds/t_okr_vs_kfg/salidas/mapa_quipus.csv')
top=['UR179','UR180','UR178','UR050','UR054','UR052','UR055','KH0001','UR177','UR203']
rows=[]
for q in top:
    r=mp[mp.kfg==q]
    if not len(r): rows.append((q,None,'sin match')); continue
    kid=int(r.KHIPU_ID.iloc[0])
    d=pd.read_sql(f'select TYPE_CODE,count(*) n from knot where CORD_ID in (select CORD_ID from cord where KHIPU_ID={kid}) group by TYPE_CODE order by n desc',con)
    rows.append((q,kid,'; '.join(f'{a or "vacio"}:{b}' for a,b in zip(d.TYPE_CODE,d.n))))
print(pd.DataFrame(rows,columns=['kfg','KHIPU_ID','tipos_OKR']).to_string(index=False))
