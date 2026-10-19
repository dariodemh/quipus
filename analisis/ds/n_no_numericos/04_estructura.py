import pandas as pd, numpy as np
K=pd.read_csv('analisis/ds/n_no_numericos/clusters.csv')
K['exp']=K['exp'].fillna(-1).astype(int)
K['turns']=K.val/ (10.0**K.exp)
K['isLE']=K.tipo.isin(['L','LL','E','EE'])
print('LE turns>9:', ((K.isLE)&(K.turns>9)).sum(), 'quipus', K[(K.isLE)&(K.turns>9)].kfg.nunique())
print(K[(K.isLE)&(K.turns>9)].groupby('kfg').size().sort_values(ascending=False).head(12).to_string())
print('\nLE exp distribution'); print(K[K.isLE].exp.value_counts().sort_index().to_string())
print('\nS exp distribution'); print(K[K.tipo=='S'].exp.value_counts().sort_index().to_string())
print('\nE value weird (not power10):', ((K.tipo.isin(['E','EE']))&(K.val>0)&(~np.log10(K.val).round(6).mod(1)==0)).sum())
# per cord structure
g=K.groupby(['kfg','cuerda'])
cord=g.agg(ncl=('k','size'), nexp=('exp','nunique'), minexp=('exp','min'), maxexp=('exp','max'),
           first=('exp','first'), last=('exp','last'), dup=('exp',lambda x: x.duplicated().any()),
           same=('exp',lambda x: x.nunique()==1), nseq=('exp','size'))
# inversions
K['exp_next']=g['exp'].shift(-1)
K['inv']=(K.exp_next>K.exp)&(K.exp_next>=0)&(K.exp>=0)
inv=K.groupby(['kfg','cuerda']).inv.sum().rename('ninv')
cord=cord.join(inv)
cord['multi']=cord.ncl>=2
print('\ncords multi',cord.multi.sum(),'dup',(cord.dup&cord.multi).sum(),'same-exp',(cord.same&cord.multi).sum(),'inv',(cord.ninv>0).sum())
print('cords with exp<0 (unknown val)',(cord.minexp<0).sum())
print('\nquipus with multi cords >=5:')
q=cord[cord.multi].groupby('kfg').agg(nmulti=('multi','size'), dupfrac=('dup','mean'), samefrac=('same','mean'), invfrac=('ninv',lambda x:(x>0).mean()))
q=q[q.nmulti>=5].sort_values('samefrac',ascending=False)
print(q.head(30).round(3).to_string())
