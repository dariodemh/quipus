"""Sensibilidad del nulo de corpus: excluye las secuencias del propio quipu."""
import pandas as pd, numpy as np
RNG=np.random.default_rng(20261018)
K=pd.read_csv('analisis/ds/n_no_numericos/clusters.csv')
K=K[K.exp>=0].sort_values(['kfg','cuerda','k'])
seq=K.groupby(['kfg','cuerda']).exp.apply(lambda x: tuple(x)).reset_index()
seq['k']=seq.exp.str.len()
top=['UR179','UR180','UR178','UR050','UR054','UR052','UR055','KH0001','UR177','UR203','UR215']
def metrics(seqs):
    multi=len(seqs); dup=same=inv=pairs=0
    for e in seqs:
        if len(e)>=2:
            if len(set(e))<len(e): dup+=1
            if len(set(e))==1: same+=1
            pairs+=len(e)-1; inv+=sum(1 for a,b in zip(e,e[1:]) if b>a)
    return dup/max(multi,1),inv/max(pairs,1),same/max(multi,1)
out=[]
for q in top:
    d=seq[(seq.kfg==q)&(seq.k>=2)]
    if len(d)<5: out.append((q,len(d),None,None,None)); continue
    obs=np.array(metrics(list(d.exp)))
    n_by=d.k.value_counts()
    pools={k:np.array([e for kk,e,qq in zip(seq.k,seq.exp,seq.kfg) if kk==k and qq!=q],dtype=object)
           for k in n_by.index}
    B=1999; null=np.zeros((B,3))
    for b in range(B):
        samp=[]
        for k,n in n_by.items():
            arr=pools[k]; idx=RNG.integers(0,len(arr),n)
            samp += [arr[i] for i in idx]
        null[b]=metrics(samp)
    p=[(1+(null[:,j]>=obs[j]).sum())/(B+1) for j in range(3)]
    out.append((q,len(d),obs.round(3).tolist(),null.mean(0).round(3).tolist(),[round(x,4) for x in p]))
print(pd.DataFrame(out,columns=['kfg','n_multi','obs_D_I_Q','null_D_I_Q','pD_pI_pQ']).to_string(index=False))
