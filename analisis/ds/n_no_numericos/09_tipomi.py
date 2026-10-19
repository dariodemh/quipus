"""Informacion del tipo/orden de nudo mas alla del valor: MI(patron;color | valor)."""
import pandas as pd, numpy as np
from collections import Counter
RNG=np.random.default_rng(20261018)
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv',dtype={'nudos':str,'color':str})
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
C=C[(C.nivel==0)&C.nudos.notna()].copy()
C['color']=C.color.fillna('NA'); C['coarse']=C.color.str.split(r'[:\-/]').str[0]

import re
pat=re.compile(r'(\d+)([A-Z?]+)\(')
def types(s):
    return ''.join('E' if t.startswith('E') else ('L' if t.startswith('L') else ('S' if t=='S' else 'X')) for _,t in pat.findall(s))
C['pat']=[types(s) for s in C.nudos]
C['pat_n']=C.pat.str.len()
C=C[C.pat_n>0]

def mi(x,y):
    n=len(x)
    if n==0: return np.nan
    cx=Counter(x); cy=Counter(y); cxy=Counter(zip(x,y))
    out=0.0
    for (a,b),v in cxy.items():
        out += (v/n)*np.log2((v*n)/(cx[a]*cy[b]))
    return out

rows=[]
for q,d in C.groupby('kfg'):
    if len(d)<20: continue
    d=d.reset_index(drop=True)
    x=list(d.pat); y=list(d.coarse); v=list(d.valor)
    obs=mi(x,y); obs_v=mi(v,y)
    # estratos por valor exacto (si hay >=2 por valor), si no decil
    d=d.copy(); d['vb']=pd.qcut(d.valor.rank(method='dense'),min(10,d.valor.nunique()),duplicates='drop',labels=False)
    strata=[list(g.index) for _,g in d.groupby('vb')]
    B=499; ge=0; nulls=[]; gev=0
    for b in range(B):
        xs=list(x)
        for idx in strata:
            if len(idx)<2: continue
            vals=[xs[i] for i in idx]
            perm=RNG.permutation(vals)
            for i,val in zip(idx,perm): xs[i]=val
        m=mi(xs,y); nulls.append(m)
        if m>=obs: ge+=1
        # nulo valor: barajar valores dentro de estratos no tiene sentido (constante); usar patron vs valor observado
    rows.append(dict(kfg=q,n=len(d),mi_pat=obs,mi_val=obs_v,mi_pat_null=np.mean(nulls),
                     p_mi=(1+ge)/(B+1), Hcolor=-sum((c/len(y))*np.log2(c/len(y)) for c in Counter(y).values()),
                     Vpat=len(set(x)), Hpat=-sum((c/len(x))*np.log2(c/len(x)) for c in Counter(x).values()),
                     Vcolor=len(set(y))))
R=pd.DataFrame(rows)
Q=Q.merge(R,on='kfg',how='left'); Q.to_csv('analisis/ds/n_no_numericos/quipus_tipomi.csv',index=False)
print('quipus >=20',len(R))
m=Q[Q.n>=20]
from scipy import stats
for v in ['mi_pat','mi_val','mi_pat_null','Hcolor','Vpat','Hpat','p_mi']:
    a=m[m.ND][v].dropna(); b=m[~m.ND][v].dropna()
    print(v,'ND',round(a.median(),3),'resto',round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
print('\nMI patron-color > nulo (p<0.05), top exceso:')
m=m.copy(); m['exceso']=m.mi_pat-m.mi_pat_null
t=m[(m.p_mi<0.05)].sort_values('exceso',ascending=False)
print(t[['kfg','n','ND','NC','mi_pat','mi_pat_null','mi_val','p_mi','Vpat','Vcolor','procedencia']].head(25).round(3).to_string(index=False))
print('\nClase con p_mi<0.05:', ((m.ND)&(m.p_mi<0.05)).sum(),'de',m.ND.sum())
