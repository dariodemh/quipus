# UR028 / UR029 / UR023 (cap. 3 y 10)
from util import *
from scipy import stats
rng=np.random.default_rng(12017)
d=q('UR028'); d['pn']=d.cuerda.str.extract(r'^p(\d+)')[0].astype(int)
un=lambda n: n if n<=34 else (n-1 if n<=55 else n-2)   # numeracion de Urton (KFG p35 y p56 son marcadores M1,M2)
mk=d.pn.isin([35,56]); print('marcadores sin valor:',d[mk][['cuerda','color','largo']].values.tolist())
d=d[~mk].copy(); d['u']=d.pn.map(un)
print('pendientes',int((d.nivel==0).sum()),'(Urton 74) subs',int((d.nivel==1).sum()),'(Urton 15)')
print('cuerda1=',d[d.u==1].valor.sum(),'; suma cuerdas 2-4 con subs=',d[(d.u>=2)&(d.u<=4)].valor.sum())
print('valores cuerdas2-4 pend/sub:',[(r.cuerda,r.valor) for r in d[(d.u>=2)&(d.u<=4)].itertuples()])
def agg(dd,sub=False):
    p=dd if sub else dd[dd.nivel==0]
    f=lambda ranges: int(sum(p[(p.u>=a)&(p.u<=b)].valor.sum() for a,b in ranges))
    odd=[[(5,9),(15,19),(25,29)],[(35,39),(45,49)],[(55,59),(65,69)]]
    ev=[[(10,14),(20,24),(30,34)],[(40,44),(50,54)],[(60,64),(70,74)]]
    return [f(r) for r in odd],[f(r) for r in ev]
kb0=d.copy(); kb0.loc[(d.nivel==1)&(d.color=='KB'),'valor']=0   # Urton: subsidiarias KB = 0
print('KFG subsidiarias KB con valor 1 (Urton: todas 0):',d[(d.nivel==1)&(d.color=='KB')&(d.valor>0)].cuerda.tolist())
print('sumas de conjuntos de 5 (impares A,B,C | pares A,B,C), pendientes solos:',agg(d),'  con subs KB=0:',agg(kb0,True),' con todas las subs:',agg(d,True))
T=[29,13,14,14,10,24]   # lo que Urton lee (impares 29,13,14[=error, esperaba 12]; pares 14,10,24)
o,e=agg(d); obs=o+e
print('coincidencias exactas con las seis sumas de Urton:',sum(a==b for a,b in zip(obs,T)),'/6')
# nulo: permutar valores de los 70 pendientes 5-74 (conserva el total y la distribucion)
idx=d[(d.nivel==0)&(d.u>=5)].index
cnt=[];cnt3=[]
for _ in range(5000):
    dd=d.copy(); dd.loc[idx,'valor']=rng.permutation(d.loc[idx,'valor'].values)
    o2,e2=agg(dd); k=o2+e2
    cnt.append(sum(a==b for a,b in zip(k,T)))
print('nulo (permutar 70 pendientes): media coincidencias',np.mean(cnt),'P(>=%d)='%sum(a==b for a,b in zip(obs,T)),np.mean(np.array(cnt)>=sum(a==b for a,b in zip(obs,T))))
print('suma pendientes 5-74 =',d[(d.nivel==0)&(d.u>=5)].valor.sum(),' (+ subs KB =',d[(d.u>=5)].valor.sum(),') vs cuerda 1 = 102')
# estructura mitades: AB vs MB
for col in ['AB','MB']:
    print(col,'suma pendientes 5-74',d[(d.nivel==0)&(d.u>=5)&(d.color==col)].valor.sum())
# nulo para 'cuerda1=suma de 2-4': permutar valores de cuerdas y subs 2..74 (excepto cuerda 1)
rest=d[d.u>=2].index
c1=[]
for _ in range(20000):
    v=rng.permutation(d.loc[rest,'valor'].values); dd=d.copy(); dd.loc[rest,'valor']=v
    c1.append(dd[(dd.u>=2)&(dd.u<=4)].valor.sum()==102)
print('P(suma 2-4 con subs ==102) bajo permutacion de 2..74:',np.mean(c1))
print('--- UR029')
e=q('UR029'); p=e[e.nivel==0]; s=e[e.nivel==1]
print('pendientes',len(p),'con >=1 sub',p.cuerda.isin(s.padre).sum(),'subs',len(s),'suma total',e.valor.sum(),'(Urton 123)','suma pend',p.valor.sum(),'suma subs',s.valor.sum())
print('grupos',G[G.kfg=='UR029'].apply(lambda r:int(r.hasta-r.desde+1),axis=1).tolist())
p=p.reset_index(drop=True)
print('pendientes sin nudos (num):',[i+1 for i,r in p.iterrows() if r.valor==0],' (Urton: 5,6,21,28,35)'); print('primer pend=',p.valor[0])
print('valores pend:',p.valor.astype(int).tolist()); print('valores subs:',s.valor.astype(int).tolist())
print(e[e.valor>0].shape, e[['cuerda','nudos']].head(3).values.tolist())
