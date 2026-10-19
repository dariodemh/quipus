import pandas as pd, numpy as np, sqlite3, json
pd.set_option('display.width',200)

c = pd.read_csv('analisis/datos/cuerdas.csv')
u = c[c.kfg=='UR1057'].sort_values('orden').reset_index(drop=True)
n0 = u[u.nivel==0].reset_index(drop=True)
n0['ord'] = np.arange(1, len(n0)+1)          # ordinal OKR de colgantes (nivel 1)
print('nivel0:', len(n0))

# clases y colores OKR
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
oc = pd.read_sql('SELECT CORD_ID,CORD_ORDINAL,CORD_LEVEL,CORD_CLASSIFICATION FROM cord WHERE KHIPU_ID=1000183',con)
oc['cls'] = oc.CORD_CLASSIFICATION.fillna('').str.strip()
cls = oc[(oc.CORD_LEVEL==1)].drop_duplicates('CORD_ORDINAL').set_index('CORD_ORDINAL').cls
n0['cls'] = n0.ord.map(cls).fillna('')

# color normalizado desde KFG
def cbase(s):
    if pd.isna(s): return '?'
    s=str(s)
    for part in s.split('/'):   # cordón bicolor -> primera mitad
        pass
    return s.split('(')[0]
n0['col'] = n0.color.map(cbase)

# separadores: clase M/F/T
n0['sep'] = n0.cls.isin(['M','F','T'])
# terminadores: 0G
n0['term'] = (n0.col=='0G') & (~n0.sep)
print('markers', (n0.cls=='M').sum(), 'flags',(n0.cls=='F').sum(),'T',(n0.cls=='T').sum())

terms = n0.index[n0.term].tolist()
starts=[0]
for t in terms:
    j=t+1
    while j<len(n0) and (n0.sep[j] or n0.col[j]=='0G'):
        j+=1
    if j<len(n0): starts.append(j)
starts = sorted(set(starts))
print('n starts',len(starts))
rows=[]
for i,s in enumerate(starts):
    e = starts[i+1]-1 if i+1<len(starts) else len(n0)-1
    # recortar separadores al final
    seg = n0.iloc[s:e+1]
    seg = seg[~seg.sep]
    rows.append(dict(g=i+1, ini=n0.ord[s], fin=int(seg.ord.iloc[-1]) if len(seg) else np.nan,
                     n=len(seg), cols=''.join(seg.col.str[0].fillna('?')),
                     vals=[int(v) for v in seg.valor]))
for r in rows:
    print(r['g'], r['ini'], r['fin'], r['n'], r['cols'], r['vals'])
