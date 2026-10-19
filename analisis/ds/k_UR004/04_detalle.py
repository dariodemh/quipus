"""UR004 - detalle de coincidencias y grupos con suma repetida; chequeo OKR."""
import pandas as pd, numpy as np, io
D='analisis/datos'
u = pd.read_csv(f'{D}/cuerdas.csv'); g=pd.read_csv(f'{D}/grupos.csv')
u=u[u.kfg=='UR004'].copy().reset_index(drop=True); g=g[g.kfg=='UR004'].copy().reset_index(drop=True)
valmap=dict(zip(u['cuerda'],u['valor']))
out=io.StringIO()
def P(*a): print(*a); print(*a,file=out)

# por grupo
info=[]
for _,r in g.iterrows():
    sub=u[(u.orden>=r['desde'])&(u.orden<=r['hasta'])]
    info.append((int(r['grupo']),int(r['desde']),int(r['hasta']),round(sub['valor'].sum(),1),len(sub)))
d=pd.DataFrame(info,columns=['grupo','desde','hasta','suma','n'])
rep=d[(d.n>1)&(d['suma']>0)&(d['suma'].duplicated(keep=False))].sort_values('suma')
P('=== GRUPOS MULTI CON SUMA REPETIDA ===')
for s,grp in rep.groupby('suma'):
    P(f'suma={s}')
    for _,row in grp.iterrows():
        sub=u[(u.orden>=row.desde)&(u.orden<=row.hasta)]
        P('   g%-2d'%row.grupo, list(zip(sub.cuerda, sub.valor.astype(int), sub.color)))

# coincidencias T4: que cuerda ajena iguala la suma de cada grupo multi
P()
P('=== T4: quien iguala la suma de cada grupo multi ===')
vset=u[u.nudos.notna()][['cuerda','valor','grupo']]
for _,row in d[d.n>1].iterrows():
    s=row['suma']
    hits=vset[(np.isclose(vset.valor,s))&(vset.grupo!=row.grupo)]
    if len(hits):
        P(f'g{int(row.grupo):2d} suma={s:7.1f} <- ' + '; '.join(f'{h.cuerda}=g{int(h.grupo)}' for h in hits.itertuples()))
with open('analisis/ds/k_UR004/04_detalle.txt','w',encoding='utf-8') as f: f.write(out.getvalue())

# ---- OKR ----
import sqlite3
db='data/external/open-khipu-repository/data/khipu.db'
con=sqlite3.connect(db)
P2=out
try:
    q=con.execute("select name from sqlite_master where type='table'").fetchall()
    P('OKR tablas:', [x[0] for x in q])
    # buscar khipu KH0240
    cols=[c[1] for c in con.execute('PRAGMA table_info(khipu_main)').fetchall()]
    P('khipu_main cols:', cols)
    row=con.execute("select * from khipu_main where khipu_id like '%240%' or khipu_id='UR004'").fetchall()
    P('khipu_main match:', row[:2])
except Exception as e:
    P('ERR', e)
with open('analisis/ds/k_UR004/04_detalle.txt','w',encoding='utf-8') as f: f.write(out.getvalue())
print('WROTE 04_detalle.txt')
