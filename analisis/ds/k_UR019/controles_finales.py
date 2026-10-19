# -*- coding: utf-8 -*-
"""Tabla final de controles: reune los p-valores del estudio y aplica Holm y BH-FDR.
(Valores recalculados de forma reproducible; el nulo es permutacion de valores/indicadores,
1000x, semilla 0, salvo donde se indica.)
"""
import numpy as np, pandas as pd, os, re
from scipy.stats import fisher_exact
rng = np.random.default_rng(0); NPERM=1000
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
C = pd.read_csv(os.path.join(ROOT,'analisis','datos','cuerdas.csv'))
d = C[C['kfg']=='UR019'].sort_values('orden').reset_index(drop=True)
val=d['valor'].to_numpy(float); lvl=d['nivel'].to_numpy(int); name=d['cuerda'].astype(str).to_numpy(); n=len(val)
p=d[d['nivel']==0].reset_index(drop=True); kn=p['nudos'].notna().to_numpy().astype(int)
def fam(c):
    c=c.upper()
    if ':' in c or '-' in c or '/' in c: return 'mixed'
    b=re.sub(r'[^A-Z]','',c)
    return 'white' if b=='W' else ('blue' if b in('BL','B','LB','NB') else ('brown' if b in('AB','MB','KB','YB') else 'other'))
famv=np.array([fam(c) for c in p['color']]); grp=p['grupo'].to_numpy()
def adj(s): return int(np.sum(s[:-1]==s[1:]))
def autoc(s,lag): return int(np.sum(s[:-lag]==s[lag:]))

def pval(stat, obs, draws):
    return (np.sum(draws>=obs)+1)/(NPERM+1)

# 1 madre==suma hijas
pairs=[(i,j) for i in range(n) if lvl[i]==0 for j in range(n) if name[j].startswith(name[i]+'s')]
obs1=sum(1 for i in range(n) if lvl[i]==0 and (ks:=[j for j in range(n) if name[j].startswith(name[i]+'s')]) and abs(val[i]-sum(val[j] for j in ks))<1e-9)
dr1=np.array([sum(1 for i in range(n) if lvl[i]==0 and (ks:=[j for j in range(n) if name[j].startswith(name[i]+'s')]) and abs(v[i]-sum(v[j] for j in ks))<1e-9) for v in (rng.permutation(val) for _ in range(NPERM))])
# 4 Saez multiplicidad pi
def SZ(v): return sum(v[i]*v[j] for i,j in pairs)
FAM={'pi':3.14159,'2pi':6.28318,'e':2.71828,'phi':1.61803,'raiz2':1.41421,'29.5':29.5,'27.25':27.25,'327':327,'328':328,'110':110,'2.5':2.5,'365':365,'360':360,'12':12,'24':24}
DIV=sorted(set(dd for k in list(range(1,31))+[13,26,100,1000,10000] for dd in (k,10*k,100*k)))
def score(v):
    s=SZ(v); return sum(1 for dd in DIV for c in FAM.values() if abs(s/dd-c)/c<0.005)
obs4=score(val); dr4=np.array([score(rng.permutation(val)) for _ in range(NPERM)])
# 5/6 color
obs_c=adj(famv)
dr_c=np.array([adj(rng.permutation(famv)) for _ in range(NPERM)])
dr_cg=[]
for _ in range(NPERM):
    f=famv.copy()
    for g in sorted(set(grp)):
        idx=np.where(grp==g)[0]; f[idx]=rng.permutation(f[idx])
    dr_cg.append(adj(f))
dr_cg=np.array(dr_cg)
# 7 lag3
obs7=autoc(kn,3); dr7=np.array([autoc(rng.permutation(kn),3) for _ in range(NPERM)])
# 8 pares de 1
def pares(s): return int(np.sum((s[:-1]==1)&(s[1:]==1)))
obs8=pares(kn); dr8=np.array([pares(rng.permutation(kn)) for _ in range(NPERM)])
# 9 fisher color sub
def wb(x): return str(x).upper().startswith('W')
tab=pd.crosstab(d['nivel'], d['color'].map(wb)); f9=fisher_exact(tab.values)[1]

tests={
 'madre = suma(hijas)':(obs1,dr1),'Saez pi (multiplicidad)':(obs4,dr4),
 'color adyacente (global)':(obs_c,dr_c),'color adyacente (intragrupo)':(obs_cg if False else obs_c,dr_cg),
 'tiene-nudo lag3':(obs7,dr7),'tiene-nudo pares':(obs8,dr8),
}
ps=[]; names=[]; obss=[]
for k,(o,dr) in tests.items():
    ps.append(pval(None,o,dr)); names.append(k); obss.append(o)
names.append('subsidiaria blanca (Fisher)'); ps.append(f9); obss.append(np.nan)
ps=np.array(ps); m=len(ps); order=np.argsort(ps)
holm=np.empty(m); prev=0
for r,i in enumerate(order):
    holm[i]=min(1.0,max(prev,(m-r)*ps[i])); prev=holm[i]
bh=np.empty(m); prev=1
for r,i in enumerate(order[::-1]):
    bh[i]=min(prev,ps[i]*m/(m-r)); prev=bh[i]
print(f'{"test":32s} {"obs":>4s} {"p":>7s} {"Holm":>7s} {"BH":>7s}')
for i in order:
    o='' if np.isnan(obss[i]) else str(obss[i])
    print(f'{names[i]:32s} {o:>4s} {ps[i]:7.4f} {holm[i]:7.4f} {bh[i]:7.4f}')
print(f'\n(m={m} tests; umbral 0.05; nulo = permutacion 1000x semilla 0)')
