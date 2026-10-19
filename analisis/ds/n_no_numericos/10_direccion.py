"""Direccion de nudo y torsion como codigo binario (Urton 2003): clase vs resto."""
import pandas as pd, numpy as np
from scipy import stats
K=pd.read_csv('analisis/ds/n_no_numericos/clusters.csv')
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv',dtype={'torsion':str})
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
K['dir']=K.dir.fillna('U')
d=K[K.dir.isin(['S','Z'])]
g=d.groupby('kfg').agg(n_dir=('dir','size'), nS=('dir',lambda x:(x=='S').sum()), nZ=('dir',lambda x:(x=='Z').sum()))
g['fracS']=g.nS/g.n_dir
# entropia binaria
p=g.fracS.clip(1e-9,1-1e-9)
g['Hdir']=-(p*np.log2(p)+(1-p)*np.log2(1-p))
C['tors']=C.torsion.fillna('U')
t=C[C.tors.isin(['S','Z'])].groupby('kfg').agg(n_t=('tors','size'), nS_t=('tors',lambda x:(x=='S').sum()))
t['fracS_t']=t.nS_t/t.n_t
Q=Q.merge(g,on='kfg',how='left').merge(t,on='kfg',how='left')
Q.to_csv('analisis/ds/n_no_numericos/quipus_direccion.csv',index=False)
m=Q[Q.n_dir>=20]
print('quipus con >=20 nudos con direccion:',len(m))
for v in ['fracS','Hdir','fracS_t']:
    a=m[m.ND][v].dropna(); b=m[~m.ND][v].dropna()
    print(v,'ND',round(a.median(),3),'resto',round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
print('\nDistribucion fracS (nudos):')
print(m.fracS.describe(percentiles=[.1,.25,.5,.75,.9]).round(3).to_string())
print('\nQuipus con direccion mas balanceada (0.2<fracS<0.8, >=30 nudos):')
b=m[(m.fracS>0.2)&(m.fracS<0.8)&(m.n_dir>=30)].sort_values('fracS')
print(b[['kfg','n_dir','fracS','Hdir','ND','NC','fracS_t','procedencia']].head(30).round(3).to_string(index=False))
print('\nClase ND con fracS>0.2:',((m.ND)&(m.fracS>0.2)).sum(),'de',m.ND.sum())
print('\nUR178 detalle:'); print(Q[Q.kfg.isin(['UR178','UR179','UR180','UR050','KH0001','UR177'])][['kfg','n_dir','fracS','Hdir','n_t','fracS_t','ND']].round(3).to_string(index=False))
