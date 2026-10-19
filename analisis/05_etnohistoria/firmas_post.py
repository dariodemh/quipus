"""Post-proceso: sustituye el p empirico por la cola exacta (Poisson/binomial) cuando el p empirico esta en su piso 1/(N+1), agrega la prueba exploratoria
de pares-mismo-contexto y aplica Holm y BH sobre todas las pruebas de firmas coloniales."""
import pandas as pd, numpy as np
from scipy import stats
R=pd.read_csv('firmas_resultados.csv').drop(columns=['p_holm','q_bh','n_pruebas'])
pf=[]
for r in R.itertuples():
    p=r.p
    if r.p<=0.0021 and r.quipus_obs>0:
        if 'Wald' in r.firma:
            ne=int(str(r.nota).split()[0]); p=stats.binom.sf(int(r.quipus_obs)-1,ne,0.05)   # cota conservadora: tasa nula <=5%
        else: p=stats.poisson.sf(int(r.quipus_obs)-1,r.nulo_media)
    pf.append(p)
R['p_final']=pf
R=pd.concat([R,pd.DataFrame([dict(categoria='depositos/cuentas duplicadas (archivos)',firma='pares con secuencia compartida que ademas comparten procedencia (5/41 vs 1.4 al azar)',quipus_obs=5,nulo_media=1.4,p=0.0140,nota='exploratoria, post hoc',p_final=0.0140)])],ignore_index=True)
def holm(p):
    p=np.asarray(p); o=np.argsort(p); m=len(p); adj=np.empty(m); r=0
    for i,ix in enumerate(o): r=max(r,(m-i)*p[ix]); adj[ix]=min(1,r)
    return adj
def bh(p):
    p=np.asarray(p); m=len(p); o=np.argsort(p); q=np.empty(m); prev=1
    for i in range(m-1,-1,-1): prev=min(prev,p[o[i]]*m/(i+1)); q[o[i]]=prev
    return q
R['p_holm']=holm(R.p_final); R['q_bh']=bh(R.p_final); R['n_pruebas']=len(R)
R.to_csv('firmas_resultados_final.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',95)
print(len(R),'pruebas; p_final<0.05:',(R.p_final<0.05).sum(),'Holm<0.05:',(R.p_holm<0.05).sum(),'BH<0.05:',(R.q_bh<0.05).sum())
print(R.sort_values('p_final').head(8)[['categoria','firma','quipus_obs','nulo_media','p_final','p_holm','q_bh']].to_string())
