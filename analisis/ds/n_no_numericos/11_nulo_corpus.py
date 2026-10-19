"""Nulo de corpus: compara el patron de exponentes de cada quipu con cuerdas de igual
numero de racimos extraidas del resto del corpus (nulo decimal 'tipico').
"""
import pandas as pd, numpy as np
from collections import defaultdict
RNG=np.random.default_rng(20261018)
K=pd.read_csv('analisis/ds/n_no_numericos/clusters.csv')
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv')
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
K=K[K.exp>=0].sort_values(['kfg','cuerda','k'])
seq=K.groupby(['kfg','cuerda']).exp.apply(lambda x: tuple(x)).reset_index()
seq['k']=seq.exp.str.len()
# pool por k (todas las secuencias)
pool={k:list(g.exp) for k,g in seq.groupby('k') if 2<=k<=8}
allseq={k:np.array(v,dtype=object) for k,v in pool.items()}

def metrics(seqs):
    multi=len(seqs); dup=0; same=0; inv=0; pairs=0
    for e in seqs:
        if len(e)>=2:
            if len(set(e))<len(e): dup+=1
            if len(set(e))==1: same+=1
            pairs+=len(e)-1
            inv+=sum(1 for a,b in zip(e,e[1:]) if b>a)
    return dup/max(multi,1), inv/max(pairs,1), same/max(multi,1)

rows=[]
for q,d in seq.groupby('kfg'):
    d=d[d.k>=2]
    if len(d)<5: continue
    obs=np.array(metrics(list(d.exp)))
    # pool leave-one-out
    n_by_k=d.k.value_counts()
    B=4999; null=np.zeros((B,3))
    for b in range(B):
        samp=[]
        for k,n in n_by_k.items():
            if k not in allseq: continue
            arr=allseq[k]
            idx=RNG.integers(0,len(arr),n)
            samp += [arr[i] for i in idx]
        null[b]=metrics(samp)
    p_hi=[(1+(null[:,j]>=obs[j]).sum())/(B+1) for j in range(3)]
    p_lo=[(1+(null[:,j]<=obs[j]).sum())/(B+1) for j in range(3)]
    rows.append(dict(kfg=q,n_multi=len(d),D=obs[0],I=obs[1],Q=obs[2],
        D_null=null[:,0].mean(),I_null=null[:,1].mean(),Q_null=null[:,2].mean(),
        pD_hi=p_hi[0],pI_hi=p_hi[1],pQ_hi=p_hi[2],
        pD_lo=p_lo[0],pI_hi_lo=p_lo[1],pQ_lo=p_lo[2]))
R=pd.DataFrame(rows)
# BH por familia
from scipy import stats
for c in ['pD_hi','pI_hi','pQ_hi']:
    R['q'+c[1:]]=stats.false_discovery_control(R[c],method='bh')
R.to_csv('analisis/ds/n_no_numericos/nulo_corpus.csv',index=False)
Q=Q.merge(R,on='kfg',how='left')
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
print('quipus',len(R))
print(R[['D','D_null','I','I_null','Q','Q_null']].describe().round(3).to_string())
print('\nSignificativos Q alto (q<0.05):',(R.qQ_hi<0.05).sum(),' I alto:',(R.qI_hi<0.05).sum(),' D alto:',(R.qD_hi<0.05).sum())
m=R.merge(Q[['kfg','ND','NC','NU','procedencia','ncuerdas_nudo']],on='kfg')
print('\nTop Q exceso (q<0.05):')
print(m[m.qQ_hi<0.05].sort_values('Q',ascending=False)[['kfg','n_multi','Q','Q_null','pQ_hi','qQ_hi','ND','procedencia']].head(30).round(3).to_string(index=False))
print('\nTop I exceso (q<0.05):')
print(m[m.qI_hi<0.05].sort_values('I',ascending=False)[['kfg','n_multi','I','I_null','pI_hi','qI_hi','ND','procedencia']].head(25).round(3).to_string(index=False))
