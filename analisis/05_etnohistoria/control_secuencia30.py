"""Control: el exceso de sumas de colgantes consecutivos = 30 (p=.001 antes de corregir) ¿es calendarico o es un efecto de numeros redondos decimales?
Perfil de exceso (observado - nulo permutado) para T=15..45; si 20/30/40 sobresalen por igual, es redondez decimal."""
import numpy as np, pandas as pd
rng=np.random.default_rng(7)
c=pd.read_csv('./analisis/datos/cuerdas.csv',low_memory=False); c['valor']=c.valor.fillna(0)
P=[g.sort_values('orden').query('nivel==0').valor.values.astype(int) for k,g in c.groupby('kfg')]
P=[p for p in P if p.sum()>0]
T=np.arange(15,46)
def stat(p):
    cs=np.r_[0,np.cumsum(p)]; s=np.concatenate([cs[L:]-cs[:-L] for L in range(3,min(30,len(p))+1)]) if len(p)>=3 else np.array([])
    return np.isin(T,s)
obs=sum(stat(p) for p in P); NS=300
null=np.array([sum(stat(rng.permutation(p)) for p in P) for _ in range(NS)])
D=pd.DataFrame(dict(T=T,obs=obs,nulo=null.mean(0).round(1),exceso=(obs-null.mean(0)).round(1),p=[(1+(null[:,i]>=obs[i]).sum())/(1+NS) for i in range(len(T))]))
print(D.to_string(index=False)); D.to_csv('control_secuencia30.csv',index=False)
print('media exceso multiplos de 10 (20,30,40): %.1f ; resto: %.1f'%(D[D['T']%10==0].exceso.mean(),D[D['T']%10!=0].exceso.mean()))
