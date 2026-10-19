# -*- coding: utf-8 -*-
"""UR093: aritmetica vectorizada, nulo por permutacion (1000x, seed 0) + Holm."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy(); u['valor']=u.valor.fillna(0).astype(int)
u=u.reset_index(drop=True)
l1=u[u.nivel==1].copy()
l1['pos']=l1.groupby('padre').cumcount()+1
l2=u[u.nivel==2]
sum2=l2.groupby('padre').valor.sum().to_dict()
child2=l1.cuerda.map(lambda c: sum2.get(c,0)).values.astype(int)  # aporte nivel2 de c/u nivel1
# indice de cada nivel1 en su propio array
l1names=l1.cuerda.values
pidx={c:i for i,c in enumerate(l1names)}
l0=u[u.nivel==0]
# solo pendantes con >=1 sub
has=set(l1.padre)
pend0=[c for c in l0.cuerda if c in has]
pend0i={c:i for i,c in enumerate(pend0)}

# para cada pendante: indices de sus nivel1 por posicion
pos_of={}   # p -> {pos: [k,...]}
for p,grp in l1.groupby('padre'):
    d={}
    for k,(c,pos) in enumerate(zip(grp.cuerda,grp.pos)):
        d.setdefault(int(pos),[]).append(pidx[c])
    pos_of[p]=d

def suma_vec(Vsub, p, poslist):
    d=pos_of[p]; s=0
    for pos in poslist:
        for k in d.get(pos,[]): s+=Vsub[k]
    return s

# valor real de nivel1 (V + child2)
baseV=np.array([u.set_index('cuerda').valor[c] for c in l1names])
Sreal=baseV+child2
# pendantes sin subs que tengan valor>0
sin=[c for c in l0.cuerda if c not in has]
print('pendantes total',len(l0),'con subs',len(pend0),'sin subs',len(sin),
      'sin subs con valor>0',int((l0.set_index("cuerda").valor[sin]>0).sum()))

# pendante valor real por indice
pv=l0.set_index('cuerda').valor.to_dict()

def hyp_subs(poslist):
    return sum(1 for p in pend0 if pv[p]==suma_vec(Sreal,p,poslist))

# nulo: permutar Sreal
rng=np.random.default_rng(0)
NP=1000
perms=[rng.permutation(Sreal) for _ in range(NP)]

def emp_p(hyp):
    obs=hyp(Sreal)
    ge=sum(1 for Sp in perms if hyp(Sp)>=obs)
    nullmean=np.mean([hyp(Sp) for Sp in perms])
    return obs,(ge+1)/(NP+1),nullmean

tests={
 'H1 c=sum(todas)':        [1,2,3,4,5,6,7,8,9,10],
 'H1b c=sum(sin 6,7)':     [1,2,3,4,5,8,9,10],
 'H1c c=sum(pos1..5)':     [1,2,3,4,5],
 'H1d c=sum(pos2..5)':     [2,3,4,5],
 'H1e c=sum(pos1..4)':     [1,2,3,4],
 'H1f c=sum(pos8..10)':    [8,9,10],
}
res={}
for name,pl in tests.items():
    res[name]=emp_p(lambda V,pl=pl: sum(1 for p in pend0 if pv[p]==suma_vec(V,p,pl)))
for name,(o,p,nm) in res.items():
    print(f'{name:24s} obs={o:3d}/{len(pend0)}  p={p:.3f}  nuloMedio={nm:.1f}')

# H nivel1 anidado = sum nivel2
nest=[c for c in l1names if c in set(l2.padre)]
obsn=sum(1 for c in nest if pv.get(c,None)==sum2.get(c,0))
# ojo: pv solo claves de nivel0; recalcular
lin={c:v for c,v in zip(l1names,baseV)}
obsn=sum(1 for c in nest if lin[c]==sum2.get(c,0))
print('\nnivel1=sum(nivel2): obs',obsn,'/',len(nest))
for c in nest: print('  ',c,lin[c],'vs',sum2.get(c,0))

# triviales H1
triv=sum(1 for p in pend0 if pv[p]==0 and suma_vec(Sreal,p,tests['H1 c=sum(todas)'])==0)
print('\nH1: matches triviales 0=0:',triv,'de',res['H1 c=sum(todas)'][0])
print('pendantes con suma-subs=0:',sum(1 for p in pend0 if suma_vec(Sreal,p,[1,2,3,4,5,6,7,8,9,10])==0))
