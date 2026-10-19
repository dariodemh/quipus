import pandas as pd, numpy as np
rng = np.random.default_rng(0)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['pos_in'] = d.orden - d.groupby('grupo').orden.transform('min')
val = d.valor.to_numpy(float)
nonzero = val>0
w = val[nonzero]

def indexed_contig(df, vals):
    df = df.copy(); df['v']=vals
    cnt=0
    for idx,g in df.groupby('pos_in'):
        arr = g.sort_values('grupo').v.to_numpy(float)
        n=len(arr)
        for j in range(n):
            v=arr[j]
            if v<=0: continue
            s=0
            for i in range(j-1,-1,-1):
                s+=arr[i]
                if s==v: cnt+=1; break
                if s>v: break
    return cnt

obsB = indexed_contig(d, val)
print("Test B observed (value = sum of >=2 consecutive same-index cords):", obsB)
out=np.empty(1000)
for t in range(1000):
    vs=w.copy(); rng.shuffle(vs); vv=val.copy(); vv[nonzero]=vs
    out[t]=indexed_contig(d,vv)
p=(1+(out>=obsB).sum())/(1+1000)
print("Test B null mean", round(out.mean(),1), "max", out.max(), "p=",p)
np.save('analisis/ds/k_AS069/nullB.npy', out)

# Also: 'forward' variant: value = sum of the FOLLOWING consecutive same-index cords only
def indexed_fwd(df, vals):
    df=df.copy(); df['v']=vals; cnt=0
    for idx,g in df.groupby('pos_in'):
        arr=g.sort_values('grupo').v.to_numpy(float); n=len(arr)
        for j in range(n):
            v=arr[j]
            if v<=0: continue
            s=0
            for i in range(j+1,n):
                s+=arr[i]
                if s==v: cnt+=1; break
                if s>v: break
    return cnt
obsF=indexed_fwd(d,val)
outF=np.empty(1000)
for t in range(1000):
    vs=w.copy(); rng.shuffle(vs); vv=val.copy(); vv[nonzero]=vs
    outF[t]=indexed_fwd(d,vv)
print("Test B-fwd observed", obsF, "null mean", round(outF.mean(),1), "max", outF.max(), "p=",(1+(outF>=obsF).sum())/(1+1000))
