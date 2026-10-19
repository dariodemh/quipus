import pandas as pd, numpy as np
rng=np.random.default_rng(0)
c=pd.read_csv('analisis/datos/cuerdas.csv')
d=c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['pos_in']=d.orden-d.groupby('grupo').orden.transform('min')
val=d.valor.to_numpy(float); nz=val>0; w=val[nz]
groups={k:g.valor.to_numpy(float) for k,g in d.groupby('pos_in')}

def indexed_subset(df_vals, vals):
    # vals aligned to d; recompute groups is expensive; use mapping
    pass

# Precompute group assignment arrays for speed
pos_in = d.pos_in.to_numpy()
uniq_pos = sorted(d.pos_in.unique())
def stat(vals):
    total=0
    for p in uniq_pos:
        arr = vals[pos_in==p]
        arr = arr[arr>0].astype(int)
        if len(arr)<2: continue
        dp1=0; dp2=0
        for a in arr:
            dp2 |= dp1<<a
            dp1 |= (1<<a) | (dp1<<a)
        # count members v with bit v in dp2
        for v in np.unique(arr):
            if (dp2>>int(v))&1: total+= (arr==v).sum()
    return total

obs=stat(val)
print("Test C2 (value = subset-sum of >=2 same-index cords): observed", obs, "de", int(nz.sum()))
out=np.empty(1000)
for t in range(1000):
    vv=val.copy(); vv[nz]=rng.permutation(w); out[t]=stat(vv)
print("null mean",round(out.mean(),1),"max",out.max(),"min",out.min(),"p",(1+(out>=obs).sum())/1001)
np.save('analisis/ds/k_AS069/nullC2.npy',out)
