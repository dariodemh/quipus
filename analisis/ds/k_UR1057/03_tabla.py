import pandas as pd, numpy as np, sqlite3
pd.set_option('display.width',220)

c = pd.read_csv('analisis/datos/cuerdas.csv')
u = c[c.kfg=='UR1057'].sort_values('orden').reset_index(drop=True)
n0 = u[u.nivel==0].reset_index(drop=True).copy()
n0['ord'] = np.arange(1, len(n0)+1)

con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
oc = pd.read_sql('SELECT CORD_ID,CORD_ORDINAL,CORD_LEVEL,CORD_CLASSIFICATION FROM cord WHERE KHIPU_ID=1000183',con)
oc['cls'] = oc.CORD_CLASSIFICATION.fillna('').str.strip()
cls = oc[oc.CORD_LEVEL==1].drop_duplicates('CORD_ORDINAL').set_index('CORD_ORDINAL').cls
n0['cls'] = n0.ord.map(cls).fillna('')
n0['col'] = n0.color.fillna('?').astype(str).str.split('(').str[0]
n0['sep'] = n0.cls.isin(['M','F','T'])

# limites manuales derivados de terminadores 0G + marcador interno (ver informe)
bounds = [(1,21),(22,43),(45,66),(67,88),(90,111),(112,133),(134,155),(157,178),(180,201),
          (206,227),(228,248),(250,272),(273,293),(294,315),(319,340),(341,363),(364,386),
          (388,410),(414,437),(439,463),(469,490),(491,513),(514,535),(538,559)]
assert len(bounds)==24
n0['grupo_a']=0; n0['sg']=0; n0['pos']=0
tabs=[]
for gi,(a,b) in enumerate(bounds,1):
    seg = n0[(n0.ord>=a)&(n0.ord<=b)&(~n0.sep)].copy()
    # indice del marcador interno (por color/ordinal conocido)
    mks = n0[(n0.ord>=a)&(n0.ord<=b)&(n0.cls=='M')].ord.tolist()
    m = mks[0] if mks else np.nan
    if len(mks)>1:
        cand=[x for x in mks if 12<=(x-a)<=17]
        m = cand[0] if cand else mks[-1]
    n0.loc[seg.index,'grupo_a']=gi
    # asignacion posicional: cola fija = 3 (sg5); sg4 = 4 antes; cabeza = 4,4,4 (sg1-3) saltando BB
    idx = seg.index.tolist()
    sg5 = idx[-3:]; sg4 = idx[-7:-3]
    head = idx[:-7]
    # quitar BB de la cabeza
    head_nb = [i for i in head if n0.loc[i,'col']!='BB']
    # repartir: sg3 = ultimos 4, sg2 = previos 4, sg1 = previos 4
    sg3 = head_nb[8:12]; sg2 = head_nb[4:8]; sg1 = head_nb[0:4]
    extra = head_nb[12:]
    for sg,idxs in [(1,sg1),(2,sg2),(3,sg3),(4,sg4),(5,sg5)]:
        for p,i in enumerate(idxs,1):
            n0.loc[i,'sg']=sg; n0.loc[i,'pos']=p
    tabs.append(dict(g=gi, ini=a, fin=b, nM=len(mks), nmk_len=len(seg)))
tab=pd.DataFrame(tabs)
print(tab.to_string(index=False))
print('\nsg sizes:', n0[n0.grupo_a>0].groupby('sg').size().to_dict())
n0[n0.grupo_a>0].to_csv('analisis/ds/k_UR1057/pendientes_estructurado.csv',index=False)
print(n0[n0.grupo_a>0][['ord','cuerda','valor','col','grupo_a','sg','pos']].head(0))

# matriz grupo x (sg,pos)
piv = n0[n0.grupo_a>0].pivot_table(index='grupo_a',columns=['sg','pos'],values='valor',aggfunc='first')
print('\n=== VALORES: filas=grupo, columnas=(sg,pos) ===')
print(piv.fillna(-1).astype(int).to_string())
