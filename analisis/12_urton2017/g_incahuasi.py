# Incahuasi (cap. 9): suma interna con valor fijo (208, 47, 15, 10, 30, 17), copias y paradigmas X/c/Y vs X/Y/c
from util import *
rng=np.random.default_rng(12017)
def fams(k):
    d=q(k); d['pn']=d.cuerda.str.extract(r'^p(\d+)')[0].astype(int)
    f=d.groupby('pn').valor.sum()           # familia = pendiente + descendientes
    own=d[d.nivel==0].set_index('pn').valor
    return own,f
def sets(k,c,tol=0):
    own,f=fams(k); pn=list(own.index)
    fixed=[i for i,p in enumerate(pn) if abs(own[p]-c)<=tol and i>0]
    out=[]
    for j,i in enumerate(fixed):
        X=pn[i-1]
        end=(fixed[j+1]-1) if j+1<len(fixed) else min(len(pn),i+8)
        mem=pn[i:end]
        out.append((X,float(f[X]),float(sum(f[m] for m in mem)),len(mem)))
    return pd.DataFrame(out,columns=['X','valorX','suma_resto','n'])
def report(k,c,tol=0):
    S=sets(k,c,tol); S=S[S.valorX>0]
    S['err']=(S.suma_resto-S.valorX)/S.valorX
    ex=(S.suma_resto==S.valorX).sum(); w1=(S.err.abs()<=0.01).sum(); w3=(S.err.abs()<=0.03).sum()
    # nulo: permutar los valores X entre conjuntos
    obs=S.err.abs().median()
    nul=[np.median(np.abs((S.suma_resto.values-rng.permutation(S.valorX.values))/S.valorX.values)) for _ in range(2000)]
    # conjuntos con X>suma?  
    return dict(quipu=k,c=c,n_sets=len(S),exactos=int(ex),dentro_1pct=int(w1),dentro_3pct=int(w3),err_mediano=round(obs,4),nulo_mediana=round(np.median(nul),3),p=round((np.sum(np.array(nul)<=obs)+1)/2001,4))
rows=[report('UR268',208,1),report('UR275',47),report('UR266',47),report('UR255',15),report('UR267A',15),report('UR256',10),report('UR267B',10),report('UR274A',30),report('UR274B',17)]
R=pd.DataFrame(rows); print(R.to_string()); R.to_csv('incahuasi_sets.csv',index=False)
print(sets('UR268',208,1).head(14).to_string())
# presencia del valor fijo: nº de cuerdas con ese valor y en cuántos otros quipus de Incahuasi
inc=[k for k in Q.index if str(Q.loc[k,'procedencia'])=='Incahuasi']
print('quipus Incahuasi en KFG:',len(inc))
for c in [208,47,15,10,30,17]:
    cnt={k:int((pend(k).valor==c).sum()) for k in inc}
    print(c,{k:v for k,v in cnt.items() if v>=3})
print('--- paradigmas de tripletas')
def trip(k,c):
    v=pend(k).valor.astype(int).tolist(); A=B=0; ex=[]
    for i in range(len(v)-2):
        x,y,z=v[i:i+3]
        if x>c and y==c and x==y+z and z>0: A+=1; ex.append(('X,c,Y',i+1,x,y,z))
        if x>c and z==c and x==y+z and y>0: B+=1; ex.append(('X,Y,c',i+1,x,y,z))
    return A,B,ex
for k,c in [('UR255',15),('UR267A',15),('UR256',10),('UR267B',10),('UR275',47),('UR266',47)]:
    A,B,ex=trip(k,c); print(k,c,'X,c,Y:',A,' X,Y,c:',B, ex[:3])
d=pend('UR267B'); print('UR267B cuerdas 86-100:',d.valor.astype(int).tolist()[85:100])
d=pend('UR256'); print('UR256 cuerdas 104-118:',d.valor.astype(int).tolist()[103:118])
d=pend('UR267A'); print('UR267A 44-58',d.valor.astype(int).tolist()[43:58]); d=pend('UR255'); print('UR255 50-65',d.valor.astype(int).tolist()[49:65])
print('UR267A union',pend('UR267A').union.value_counts().to_dict(),' UR255 union',pend('UR255').union.value_counts().to_dict(),'UR267B',pend('UR267B').union.value_counts().to_dict(),'UR256',pend('UR256').union.value_counts().to_dict())
# copias: UR255~UR267A, UR256~UR267B, UR266~UR275: cuantos valores >=20 compartidos
from collections import Counter
def shared(a,b,thr):
    ca=Counter(int(v) for v in q(a).valor if v>=thr); cb=Counter(int(v) for v in q(b).valor if v>=thr); return sum((ca&cb).values()),sum(ca.values()),sum(cb.values())
for a,b,thr in [('UR255','UR267A',20),('UR256','UR267B',20),('UR266','UR275',1000),('UR273B','UR266',1000),('UR273B','UR275',1000)]:
    print(a,b,'valores compartidos >=%d'%thr,shared(a,b,thr))
# UR266 vs UR275: tabla 9.3 valores >1000: exactos
a=[int(v) for v in q('UR266').valor if v>1000]; b=[int(v) for v in q('UR275').valor if v>1000]
print('UR266 >1000:',len(a),' UR275 >1000:',len(b),' exactos compartidos',sum((Counter(a)&Counter(b)).values()))
close=0; usedb=Counter(b)
cl=[(x,y) for x in a for y in b if x!=y and abs(x-y)<=0.03*max(x,y)]
print('pares cercanos (<=3%) distintos de exactos:',len(set(cl)),sorted(set(cl))[:12])
print('sumas: 1070+1217 =',1070+1217,'en UR275:',2287 in b,'; 2106+1153, 1653+1606=3259')
