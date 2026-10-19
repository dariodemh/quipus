# UR011 (cap. 11): 15 pares de valores altos que decrecen; comparacion con tributarios de Chachapoya
from util import *
from scipy import stats
rng=np.random.default_rng(12017)
d=q('UR011'); idx={r.cuerda:r.valor for r in d.itertuples()}
pairs=[('p4','p5'),('p9','p10'),('p14','p15'),('p19','p20'),('p24','p25'),('p29','p30'),('p34','p35'),('p39','p40'),('p44','p45'),('p49s1','p50s1'),('p54','p55'),('p59','p60'),('p64','p65'),('p69','p70'),('p75','p76')]
U=[(15746,15448),(10809,11056),(11532,9547),(8764,8592),(8483,5713),(9681,6153),(6308,6250),(8263,8319),(8441,9446),(2220,2225),(1500,1418),(1316,1671),(2306,2750),(2335,3111),(2082,4527)]
K=[(int(idx[a]),int(idx[b])) for a,b in pairs]
print('pares KFG == Tabla 11.2 de Urton:',sum(k==u for k,u in zip(K,U)),'/15')
m=np.array([(a+b)/2 for a,b in K]); print('medias',m.round(0).tolist())
rho,p=stats.spearmanr(range(15),m); print('Spearman medias vs orden:',rho,p)
print('razon ultimo/primero',m[-1]/m[0],' caida %',100*(1-m[-1]/m[0]))
print('razon entre miembros del par (b/a) mediana',np.median([b/a for a,b in K]),' |log| mediano',np.median([abs(np.log(b/a)) for a,b in K]))
# escalon: caida mayor entre pares 9 y 10
print('cambio relativo consecutivo',(m[1:]/m[:-1]).round(2).tolist())
# punto de cambio: ajuste de dos mesetas vs pendiente lineal (R2)
x=np.arange(15); 
sl=stats.linregress(x,np.log(m)); print('R2 lineal en log',sl.rvalue**2)
best=min(((np.sum((np.log(m[:k])-np.log(m[:k]).mean())**2)+np.sum((np.log(m[k:])-np.log(m[k:]).mean())**2)),k) for k in range(2,14)); 
tot=np.sum((np.log(m)-np.log(m).mean())**2); print('R2 dos mesetas (k=%d)'%best[1],1-best[0]/tot)
# ¿es raro? series de maximos por grupo en todos los quipus con >=12 grupos
res=[]
for k,dd in C.groupby('kfg'):
    p0=dd[dd.nivel==0]
    mx=p0.groupby('grupo').valor.max()
    mx=mx[mx>0]
    if len(mx)>=12:
        r,pp=stats.spearmanr(range(len(mx)),mx.values); res.append((k,len(mx),r,pp))
R=pd.DataFrame(res,columns=['kfg','n','rho','p'])
print('quipus con >=12 grupos con valor:',len(R),' rho<=-0.8:',(R.rho<=-0.8).sum(),' rho>=0.8:',(R.rho>=0.8).sum(),' UR011:',R[R.kfg=='UR011'].values.tolist())
# serie propia de 15 pares: comparar con 15 maximos de grupo de cada quipu (n=15 primeros grupos)
res2=[]
for k,dd in C.groupby('kfg'):
    p0=dd[dd.nivel==0]; mx=p0.groupby('grupo').valor.max(); mx=mx[mx>0]
    if len(mx)>=15: res2.append((k,stats.spearmanr(range(15),mx.values[:15])[0]))
R2=pd.DataFrame(res2,columns=['kfg','rho15']); print('con >=15 grupos:',len(R2),' frac rho15<=-0.87:',(R2.rho15<=-0.87).mean())
# Tabla 11.3 vs UR011: ¿los 15 pasos caen sobre la curva? cada anio con interpolacion lineal 1559..1608
yrs=np.array([1549,1559,1583,1586,1591,1601,1608]); tr=np.array([17550,16309,10699,8062,7042,5626,4000])
for a,b in [(1559,1608),(1570,1625)]:
    t=np.linspace(a,b,15); 
    if b<=1608: curve=np.interp(t,yrs,tr)
    else: curve=np.interp(t,yrs,tr,right=np.nan)
    ok=~np.isnan(curve); print('periodo',a,b,'corr Pearson log',np.corrcoef(np.log(curve[ok]),np.log(m[ok]))[0,1], 'n',ok.sum())
# nulo: misma correlacion con 15 maximos de grupo decrecientes ordenados de otros quipus (cualquier serie monotona decreciente da corr alta)
t=np.linspace(1559,1608,15); curve=np.interp(t,yrs,tr)
cs=[]
for k,dd in C.groupby('kfg'):
    p0=dd[dd.nivel==0]; mx=p0.groupby('grupo').valor.max(); mx=mx[mx>0]
    if len(mx)>=15:
        s=np.sort(mx.values[:15])[::-1]
        if s.min()>0: cs.append(np.corrcoef(np.log(curve),np.log(s))[0,1])
print('corr con curva usando maximos ordenados decrecientemente de %d quipus: mediana %.2f'%(len(cs),np.median(cs)),' (UR011 en orden natural: ver arriba)')
flat=np.array([v for pr in K for v in pr],float)
obs=np.median([abs(np.log(b/a)) for a,b in K])
nul=[]
for _ in range(10000):
    s=rng.permutation(flat).reshape(15,2); nul.append(np.median(np.abs(np.log(s[:,1]/s[:,0]))))
print('similitud interna de pares: mediana |log razon| obs %.3f; nulo media %.3f; P(nulo<=obs)=%.5f'%(obs,np.mean(nul),np.mean(np.array(nul)<=obs)))
