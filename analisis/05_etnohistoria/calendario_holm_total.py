"""Une calendario_resultados.csv (96 pruebas) con los conteos estructurales calendarios de firmas_resultados.csv y aplica Holm/BH sobre TODAS."""
import pandas as pd, numpy as np
A=pd.read_csv('calendario_resultados.csv'); B=pd.read_csv('firmas_resultados.csv'); B=B[B.categoria.str.startswith('calendario')]
B=B.assign(familia='conteo_estructural',objetivo=B.firma)[['familia','objetivo','quipus_obs','nulo_media','p']]
A=A[['familia','objetivo','quipus_obs','nulo_media','p']]
R=pd.concat([A,B],ignore_index=True)
def holm(p):
    p=np.asarray(p); o=np.argsort(p); m=len(p); adj=np.empty(m); r=0
    for i,ix in enumerate(o): r=max(r,(m-i)*p[ix]); adj[ix]=min(1,r)
    return adj
def bh(p):
    p=np.asarray(p); m=len(p); o=np.argsort(p); q=np.empty(m); prev=1
    for i in range(m-1,-1,-1): prev=min(prev,p[o[i]]*m/(i+1)); q[o[i]]=prev
    return q
R['p_holm']=holm(R.p); R['q_bh']=bh(R.p); R['n_pruebas']=len(R); R.to_csv('calendario_holm_total.csv',index=False)
pd.set_option('display.width',200)
print('n pruebas',len(R),'| p<0.05 sin corregir:',(R.p<0.05).sum(),'| esperado por azar ~',round(0.05*len(R),1),'| Holm<0.05:',(R.p_holm<0.05).sum(),'| BH<0.05:',(R.q_bh<0.05).sum())
print(R.sort_values('p').head(15).round(4).to_string())
