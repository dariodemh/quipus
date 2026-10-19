import pandas as pd, numpy as np
rng=np.random.default_rng(0)
n=pd.read_csv('analisis/ds/k_UR1057/pendientes_estructurado.csv')
n['parte']=np.where(n.grupo_a<=7,'P1','P2')
S={}
for g,s in n.groupby('grupo_a'):
    S[g]={sg:x.valor.sum() for sg,x in s.groupby('sg')}
def hits(df,which='R1'):
    h=0
    for g,s in df.groupby('grupo_a'):
        ss={sg:x.valor.sum() for sg,x in s.groupby('sg')}
        a=ss.get(1,0)+ss.get(2,0)+ss.get(3,0); b=ss.get(4,0); c=ss.get(5,0)
        if which=='R1' and a>0 and a==b: h+=1
        if which=='R2' and a+b>0 and a+b==c: h+=1
        if which=='R3' and ss.get(1,0)>0 and ss.get(5,0)==ss.get(1,0): h+=1
    return h
for w,lbl in [('R1','sg4=sg1+sg2+sg3'),('R2','sg5=sg1..sg4'),('R3','sg5=sg1')]:
    for sub,df in [('todos',n),('P1',n[n.parte=='P1'])]:
        obs=hits(df,w); st=[]
        for _ in range(1000):
            d=df.copy(); d['valor']=d.groupby('grupo_a').valor.transform(lambda s: rng.permutation(s.values))
            st.append(hits(d,w))
        print(f'{w} {lbl:18s} {sub:5s} obs={obs} p={(np.sum(np.array(st)>=obs)+1)/1001:.3f} nulo={np.mean(st):.2f}')
print()
# monotonia / seriacion por subgrupo
dec=0; inc=0
for g,s in n[n.parte=='P1'].groupby('grupo_a'):
    for sg,x in s.groupby('sg'):
        v=x.sort_values('pos').valor.values
        if len(v)>1 and all(np.diff(v)<=0): dec+=1
        if len(v)>1 and all(np.diff(v)>=0): inc+=1
print('vectores monotonos P1: decrecientes',dec,'crecientes',inc,'de',7*5)
# posicion de los 1s en sg4 P2
z=n[(n.parte=='P2')&(n.sg==4)].groupby('grupo_a').apply(lambda s:''.join('1' if v>0 else '0' for v in s.sort_values('pos').valor),include_groups=False)
print('\nsg4 P2 (pos1-4):',z.value_counts().to_dict())
print('grupos duplicados:',[k for k,v in __import__('collections').Counter({g:tuple(s.sort_values(['sg','pos']).valor.tolist()) for g,s in n.groupby('grupo_a')}.values()).items() if v>1])
