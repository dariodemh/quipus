# UR053B / UR053C (cap. 8): par "ceque"
from util import *
rng=np.random.default_rng(12017)
c=q('UR053C'); b=q('UR053B')
print('53C pendientes',len(c),'color seq',' '.join(c.color.fillna('?').head(12)),' union',c.union.value_counts().to_dict())
print('53B pend',(b.nivel==0).sum(),'subs',(b.nivel==1).sum(),' union',b[b.nivel==0].union.value_counts().to_dict(),'sub union',b[b.nivel==1].union.value_counts().to_dict())
vc=c.valor.astype(int).tolist(); print('53C',vc)
vb=b.valor.astype(int).tolist(); print('53B (orden cuerda,subs)',vb)
print('53B colores',' '.join(b.color.fillna('?').head(15)))
# patron de color triple W/RL/AB
def triple(cols): 
    return np.mean([cols[i]==['W','RL','AB'][i%3] for i in range(len(cols))])
print('frac color W/RL/AB periodico 53C',triple(c.color.fillna('?').tolist()),' 53B',triple(b.color.fillna('?').tolist()))
print('53C colores:',c.color.value_counts().to_dict()); print('53B colores:',b.color.value_counts().to_dict())
best=None
res=[]
for s in range(0,25):
    n=min(len(vb),len(vc)-s)
    x=np.array(vb[:n]); y=np.array(vc[s:s+n])
    ex=int(np.sum(x==y)); cl=int(np.sum(np.abs(x-y)<=np.maximum(1,0.1*np.maximum(x,y))))
    res.append((s,n,ex,cl))
print(sorted(res,key=lambda r:-r[2])[:5])
s=10; n=51; x=np.array(vb[:n]); y=np.array(vc[s:s+n])
obs=int(np.sum(x==y)); nul=[int(np.sum(rng.permutation(np.array(vc[s:s+n]))==x)) for _ in range(5000)]
print('desfase 10: exactas',obs,'/51; nulo media',np.mean(nul),'max',max(nul),'p',(np.sum(np.array(nul)>=obs)+1)/5001)
# nulo mas duro: mejor desfase 0..24 con valores permutados de 53C
mx=[]
for _ in range(500):
    yy=rng.permutation(vc)
    mx.append(max(int(np.sum(np.array(vb[:min(len(vb),len(yy)-s2)])==yy[s2:s2+min(len(vb),len(yy)-s2)])) for s2 in range(25)))
print('nulo del maximo sobre 25 desfases: media',np.mean(mx),'max',max(mx))
# cuantos de los 51 son trivialmente 0/1
print('exactas con valor>=5:',int(np.sum((x==y)&(x>=5))),'de',int(np.sum(x>=5)))
print('R/V opuestos: 53C union',set(c.union),' 53B pend union',set(b[b.nivel==0].union))
