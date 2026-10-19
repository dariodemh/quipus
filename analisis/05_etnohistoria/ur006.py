"""UR006 (Urton 2001/2005): estructura calendarica en el registro KFG y regularidad de tamano de grupos frente al corpus."""
import numpy as np, pandas as pd
D='./analisis/datos/'
c=pd.read_csv(D+'cuerdas.csv',low_memory=False); c['valor']=c.valor.fillna(0)
u=c[c.kfg=='UR006']
g=u.groupby('grupo').agg(cuerdas=('cuerda','size'),pend=('nivel',lambda x:(x==0).sum()),suma=('valor','sum')).reset_index()
big=g[g.pend>=15]
print('UR006: cuerdas',len(u),'pendientes',(u.nivel==0).sum(),'subs',(u.nivel>0).sum(),'| suma valores',u.valor.sum(),'| pendientes',u[u.nivel==0].valor.sum())
print('grupos grandes (>=15 pendientes):',len(big),'| pendientes por grupo:',big.pend.tolist())
print('cuerdas (con subsidiarias) por grupo grande:',big.cuerdas.tolist(),'-> total',big.cuerdas.sum(),'| en 29-31:',((big.cuerdas>=29)&(big.cuerdas<=31)).sum(),'| media %.1f'%big.cuerdas.mean())
print('pendientes en grupos grandes:',big.pend.sum(),'; con los pendientes-lazo que los siguen:',big.pend.sum()+ (g.pend==1).sum())
# grupo grande + pendiente-lazo siguiente (suma de cuerdas)
seq=g.cuerdas.tolist(); 
print('sumas de valores por grupo grande:',big.suma.astype(int).tolist(),'total',big.suma.sum())
print('nudos: total valor UR006 =',u.valor.sum(),'(Urton 2005: 2962 tras correccion; 3005 en 2001)')
# regularidad: racha mas larga de grupos consecutivos (>=10 pendientes) con rango de pendientes <=2 ; corpus
rows=[]
for k,x in c.groupby('kfg',sort=False):
    gg=x[x.nivel==0].groupby('grupo').size().tolist()
    best=0;i=0
    s=[t for t in gg if t>=10]          # solo grupos 'grandes'
    # racha en la secuencia de grupos grandes (pueden intercalarse separadores pequenos)
    for i in range(len(s)):
        j=i
        while j+1<len(s) and max(s[i:j+2])-min(s[i:j+2])<=2: j+=1
        best=max(best,j-i+1)
    rows.append((k,len(gg),best))
R=pd.DataFrame(rows,columns=['kfg','ngrupos','racha']).sort_values('racha',ascending=False)
print('\nRacha de grupos grandes consecutivos con #pendientes en rango<=2 (corpus 651):')
print(R.head(12).to_string(index=False)); print({t:int((R.racha>=t).sum()) for t in (6,8,12,18,24)})
# lo mismo con permutacion del ORDEN de grupos dentro del quipu para UR006 (conserva tamanos)
rng=np.random.default_rng(1)
s=[t for t in u[u.nivel==0].groupby('grupo').size().tolist() if t>=10]
def racha(s):
    b=0
    for i in range(len(s)):
        j=i
        while j+1<len(s) and max(s[i:j+2])-min(s[i:j+2])<=2: j+=1
        b=max(b,j-i+1)
    return b
print('UR006 racha obs',racha(s),'| tamanos permutados (orden barajado): media',np.mean([racha(list(rng.permutation(s))) for _ in range(2000)]))
R.to_csv('ur006_regularidad_corpus.csv',index=False)
