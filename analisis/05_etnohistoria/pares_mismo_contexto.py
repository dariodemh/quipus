"""De los pares de quipus que comparten 6 colgantes consecutivos: cuantos comparten procedencia/museo frente a pares al azar (prueba de permutacion)."""
import pandas as pd, numpy as np
rng=np.random.default_rng(3)
q=pd.read_csv('./analisis/datos/quipus.csv').set_index('kfg')
P=pd.read_csv('pares_secuencia_compartida.csv')
def ctx(k,f): return str(q.loc[k,f])
for f in ('procedencia','museo'):
    same=lambda a,b: ctx(a,f)==ctx(b,f) and ctx(a,f) not in ('Unknown','nan')
    obs=sum(same(a,b) for a,b in zip(P.quipu_a,P.quipu_b))
    ks=list(q.index); nl=[]
    for _ in range(5000):
        idx=rng.integers(0,len(ks),(len(P),2)); nl.append(sum(same(ks[i],ks[j]) for i,j in idx if i!=j))
    print(f,'pares del mismo contexto:',obs,'de',len(P),'| al azar media %.1f'%np.mean(nl),'p=%.4f'%((1+(np.array(nl)>=obs).sum())/5001))
print(P.assign(prov_a=[ctx(a,'procedencia') for a in P.quipu_a],prov_b=[ctx(b,'procedencia') for b in P.quipu_b]).query('prov_a==prov_b and prov_a!="Unknown"').to_string())
