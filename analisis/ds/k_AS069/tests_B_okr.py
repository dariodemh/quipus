import sqlite3, pandas as pd, numpy as np
pd.set_option('display.width',160)
con=sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cc=pd.read_sql("SELECT * FROM cord_cluster WHERE KHIPU_ID=1000096",con)
con.close()
cc=cc.sort_values('ORDINAL').reset_index(drop=True)
print("clusters:", len(cc), "ordin monotonic in BEG?", cc.BEG_CORD.is_monotonic_increasing)
print("sum NUM_CORDS:", cc.NUM_CORDS.sum())
# index within cluster: use POSITION_IN_CLUSTER? no. Use cord ordinal ordering.
# build cordinal -> (cluster_ordinal, idx)
recs=[]
for _,r in cc.iterrows():
    for k in range(int(r.BEG_CORD), int(r.END_CORD)+1):
        recs.append((k, int(r.ORDINAL), k-int(r.BEG_CORD), int(r.NUM_CORDS)))
mp=pd.DataFrame(recs, columns=['cordinal','clu','idx','nclu'])
print("covered cords:", len(mp), "unique:", mp.cordinal.nunique(), "clu range", mp.clu.min(), mp.clu.max())
c=pd.read_csv('analisis/datos/cuerdas.csv')
d=c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['cordinal']=d.orden+1
d=d.merge(mp, on='cordinal', how='left')
print("unmatched cords:", d.clu.isna().sum())

rng=np.random.default_rng(0); val=d.valor.to_numpy(float); nz=val>0; w=val[nz]
def indexed_contig(df,vals):
    df=df.copy(); df['v']=vals; cnt=0
    for idx,g in df.groupby('idx'):
        arr=g.sort_values('clu').v.to_numpy(float); n=len(arr)
        for j in range(n):
            v=arr[j]
            if v<=0: continue
            s=0
            for i in range(j-1,-1,-1):
                s+=arr[i]
                if s==v: cnt+=1; break
                if s>v: break
    return cnt
obs=indexed_contig(d,val)
print("OKR-cluster indexed contiguous-run sums observed:", obs)
out=np.empty(1000)
for t in range(1000):
    vv=val.copy(); vv[nz]=rng.permutation(w); out[t]=indexed_contig(d,vv)
print("null mean",round(out.mean(),1),"max",out.max(),"p",(1+(out>=obs).sum())/1001)
np.save('analisis/ds/k_AS069/nullB_okr.npy',out)
