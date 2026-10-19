"""N-gramas de color/torsion como 'palabras' y entropia condicional, con nulo intra-quipu.
Solo cuerdas de nivel 0, ordenadas por 'orden' dentro de cada grupo.
"""
import pandas as pd, numpy as np
from collections import Counter
RNG=np.random.default_rng(20261018)
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv',dtype={'color':str,'torsion':str})
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
C=C[C.nivel==0].copy()
C['color']=C.color.fillna('NA')
C['coarse']=C.color.str.split(r'[:\-/]').str[0]
C['tors']=C.torsion.fillna('U')
C['sym_exact']=C.color+'|'+C.tors
C['sym_coarse']=C.coarse+'|'+C.tors
C=C.sort_values(['kfg','grupo','orden'])

def seqs(d,col):
    out=[]
    for g,x in d.groupby('grupo',sort=False):
        out.append(list(x[col]))
    return [s for s in out if len(s)>=2]

def stats(ss,n):
    cnt=Counter(); tot=0
    for s in ss:
        for i in range(len(s)-n+1):
            cnt[tuple(s[i:i+n])]+=1; tot+=1
    if tot==0: return np.nan,np.nan,0,0
    rep=sum(v for v in cnt.values() if v>1)/tot
    mx=max(cnt.values()) if cnt else 0
    return rep,mx,len(cnt),tot

def cond_ent(ss):
    # H(next|current) sobre bigramas, normalizada por H1
    trans=Counter(); cur=Counter(); tot=0
    for s in ss:
        for a,b in zip(s,s[1:]):
            trans[(a,b)]+=1; cur[a]+=1; tot+=1
    if tot==0: return np.nan,np.nan
    H=0
    for (a,b),v in trans.items():
        H -= (v/tot)*np.log2(v/cur[a])
    p=Counter(x for s in ss for x in s); N=sum(p.values())
    H1=-sum((v/N)*np.log2(v/N) for v in p.values())
    return H, H/H1 if H1>0 else np.nan

rows=[]
for q,d in C.groupby('kfg'):
    r={'kfg':q,'n_pend':len(d)}
    for col,tag in [('sym_coarse','c'),('sym_exact','e')]:
        ss=seqs(d,col)
        for n in [1,2,3]:
            rep,mx,nv,tot=stats(ss,n)
            r[f'rep{n}_{tag}']=rep; r[f'max{n}_{tag}']=mx; r[f'V{n}_{tag}']=nv; r[f'not{n}_{tag}']=tot
        H,Hn=cond_ent(ss); r[f'H_{tag}']=H; r[f'Hn_{tag}']=Hn
        # nulo: barajar simbolos dentro de cada grupo
        obs=r[f'rep2_{tag}']; B=499; ge=0; le=0; nulls=[]
        obsH=r[f'Hn_{tag}']
        for b in range(B):
            sh=[list(RNG.permutation(s)) for s in ss]
            v,_,_,_=stats(sh,2); nulls.append(v)
            h,hn=cond_ent(sh)
            if hn<=obsH if pd.notna(obsH) else False: le+=1
            if v>=obs: ge+=1
        r[f'p_rep2_{tag}']=(1+ge)/(B+1)
        r[f'p_cond_{tag}']=(1+le)/(B+1)
        r[f'rep2null_{tag}']=np.mean(nulls)
    rows.append(r)
R=pd.DataFrame(rows)
Q=Q.merge(R,on='kfg',how='left')
Q.to_csv('analisis/ds/n_no_numericos/quipus_colorgram.csv',index=False)
print('quipus con >=10 pendientes:', (Q.n_pend>=10).sum())
m=Q[Q.n_pend>=10]
print('\nClase vs resto (medianas):')
for v in ['rep2_c','rep3_c','Hn_c','p_rep2_c','p_cond_c','V1_c']:
    a=m[m.ND][v].dropna(); b=m[~m.ND][v].dropna()
    from scipy import stats
    print(v,'ND',round(a.median(),3),'resto',round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
print('\nTop repeticion bigramas (p<0.05, >=20 pendientes):')
t=m[(m.p_rep2_c<0.05)&(m.n_pend>=20)].sort_values('rep2_c',ascending=False)
print(t[['kfg','n_pend','ND','NC','rep2_c','rep2null_c','max2_c','p_rep2_c','Hn_c','p_cond_c','procedencia']].head(30).round(3).to_string(index=False))
print('\nTop cond ent baja (p<0.05, >=20 pend):')
t=m[(m.p_cond_c<0.05)&(m.n_pend>=20)].sort_values('Hn_c')
print(t[['kfg','n_pend','ND','NC','Hn_c','rep2_c','p_cond_c','p_rep2_c','procedencia']].head(25).round(3).to_string(index=False))
