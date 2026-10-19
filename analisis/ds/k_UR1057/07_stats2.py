import pandas as pd, numpy as np
from collections import Counter
rng=np.random.default_rng(0)
n=pd.read_csv('analisis/ds/k_UR1057/pendientes_estructurado.csv')
n['blank']=n.nudos.isna(); n['parte']=np.where(n.grupo_a<=7,'P1','P2')
res=[]
def rec(t,obs,p,note=''):
    pp='  n/a' if p is None or (isinstance(p,float) and np.isnan(p)) else f'{p:.4f}'
    res.append((t,obs,p,note)); print(f'{t:44s} obs={str(obs):>12}  p={pp}  {note}')

def e4(df):
    h=0
    for g,s in df.groupby('grupo_a'):
        ss={sg:x.valor.sum() for sg,x in s.groupby('sg')}
        for a in [1,2,3,4]:
            if ss.get(a,0)>0 and ss.get(a,0)==ss.get(5,0): h+=1
    return h
obs=e4(n); st=[]
for _ in range(1000):
    d=n.copy(); d['valor']=d.groupby('grupo_a').valor.transform(lambda s: rng.permutation(s.values))
    st.append(e4(d))
rec('E4 suma sg1-4 = suma sg5 (no trivial)',obs,(np.sum(np.array(st)>=obs)+1)/1001,'nulo intra-grupo')

def rows(df):
    out={}
    for g,s in df.groupby('grupo_a'):
        v=s.sort_values(['sg','pos']); out[g]=tuple(v.valor.tolist())
    return out
def ndup(df):
    c=Counter(rows(df).values()); return sum(v for v in c.values() if v>1)
obs=ndup(n); st=[]
for _ in range(1000):
    d=n.copy(); d['valor']=d.groupby(['sg','pos']).valor.transform(lambda s: rng.permutation(s.values))
    st.append(ndup(d))
rec('F filas de grupo duplicadas',obs,(np.sum(np.array(st)>=obs)+1)/1001,'nulo intra-(sg,pos)')

seq=n.sort_values('ord').valor.values.astype(float)
def acmax(x,lags=range(1,21)):
    x=x-x.mean(); return max(abs((x[:-l]*x[l:]).sum()/(x*x).sum()) for l in lags)
obs=acmax(seq); st=[]
for _ in range(1000):
    d=n.copy(); v=d.groupby('grupo_a').valor.transform(lambda s: rng.permutation(s.values)).values
    st.append(acmax(v))
rec('G autocorr max |rho| lags1-20 (nulo intra-grupo)',round(obs,3),(np.sum(np.array(st)>=obs)+1)/1001,'nulo intra-grupo')

gs=n[n.parte=='P2'].groupby('grupo_a').valor.sum().values.astype(float)
rho=np.corrcoef(np.arange(len(gs)),gs)[0,1]
st=[np.corrcoef(np.arange(len(gs)),rng.permutation(gs))[0,1] for _ in range(1000)]
rec('H tendencia suma~indice (solo P2)',round(rho,3),(np.sum(np.abs(st)>=abs(rho))+1)/1001,'nulo permuta')

w=n[n.parte=='P2'].groupby('grupo_a').valor.apply(lambda s:int((s>0).sum())).values
rec('I peso (n>0) por grupo P2',f'{w.mean():.1f} +- {w.std():.1f}',None,f'dist={dict(sorted(Counter(w).items()))}')

tot=n.valor.sum(); p1=n[n.parte=='P1'].valor.sum(); p2=n[n.parte=='P2'].valor.sum()
rec('K numeros calendario (total/P1/P2)',f'{tot:.0f}/{p1:.0f}/{p2:.0f}',None,'365,584,354,260,145 ausentes')
gsm=n.groupby('grupo_a').valor.sum().to_dict()
rec('L top cords T1,T2 vs sumas de grupo','T1=5,T2=20',None,f'g19={gsm[19]:.0f}, g20={gsm[20]:.0f}, g23={gsm[23]:.0f}, g24={gsm[24]:.0f}')
print('\nduplicados:',[k for k,v in Counter(rows(n).values()).items() if v>1])
print('filas con todos ceros:',[g for g,v in rows(n).items() if sum(v)==0])
print('blank P1/P2:',round(n[n.parte=="P1"].blank.mean(),3),round(n[n.parte=="P2"].blank.mean(),3))
print('P1 valores: n=%d max=%.0f suma=%.0f'%(len(n[n.parte=='P1']),n[n.parte=='P1'].valor.max(),p1))
print('P2 valores: n>0=%d de %d, max=%d, suma=%.0f'%((n[n.parte=='P2'].valor>0).sum(),len(n[n.parte=='P2']),n[n.parte=='P2'].valor.max(),p2))
pd.DataFrame(res,columns=['test','obs','p','nota']).to_csv('analisis/ds/k_UR1057/tests2.csv',index=False)
fam=[r for r in res if isinstance(r[2],float) and not np.isnan(r[2])]
fam=sorted(fam,key=lambda r:r[2]); m=len(fam); print('\nHolm (m=%d):'%m); prev=0
for i,(t,o,p,no) in enumerate(fam):
    adj=min(1,max(prev,(m-i)*p)); prev=adj
    print(f'  {t:44s} p={p:.4f} -> p_holm={adj:.4f}')
