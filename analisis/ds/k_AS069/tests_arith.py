import pandas as pd, numpy as np, itertools
rng = np.random.default_rng(0)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['pos_in'] = d.orden - d.groupby('grupo').orden.transform('min')
val = d.valor.to_numpy(float)
nonzero = val>0
w = val[nonzero]

def stat_A(values_by_mother):
    # placeholder
    return 0

# ---------- Test A: madre = suma de subsidiarias (direct hierarchy) ----------
kids = d[d.padre.notna()].groupby('padre')['valor'].sum()
moms = d.set_index('cuerda')['valor']
common = kids.index.intersection(moms.index)
obsA = int(np.isclose(moms.loc[common].to_numpy(), kids.loc[common].to_numpy()).sum())
print("Test A (madre=suma subsidiarias): madres con hijas:", len(common),
      " coincidencias exactas:", obsA, " con suma>0:", int((kids.loc[common]>0).sum()))

# ---------- Test B: indexed contiguous runs at grupo level ----------
# group cords by pos_in, order by grupo, test value = sum of >=2 consecutive same-index cords
def indexed_contig(df, vals):
    df = df.copy(); df['v']=vals
    cnt=0
    for idx,g in df.groupby('pos_in'):
        g = g.sort_values('grupo')
        arr = g.v.to_numpy(float)
        n=len(arr)
        for j in range(n):
            if arr[j]<=0: continue
            s=0
            for i in range(j-1,-1,-1):
                s+=arr[i]
                if s==arr[j]: cnt+=1; break
                if s>arr[j]: break
    return cnt
obsB = indexed_contig(d, val)
print("Test B observed (indexed contiguous-run sums):", obsB)

# ---------- Test C: indexed subset sums size 2..4 at grupo level ----------
def indexed_subset(df, vals, kmin=2, kmax=4):
    df=df.copy(); df['v']=vals
    cnt=0
    for idx,g in df.groupby('pos_in'):
        arr=g.sort_values('grupo').v.to_numpy(float)
        arr=arr[arr>0]
        n=len(arr)
        if n<kmin: continue
        sums=set()
        for k in range(kmin,kmax+1):
            for comb in itertools.combinations(range(n),k):
                sums.add(int(sum(arr[i] for i in comb)))
        for v in arr:
            if int(v) in sums: cnt+=1
    return cnt
obsC = indexed_subset(d, val)
print("Test C observed (indexed subset-sum k=2..4):", obsC)

# ---------- Null distributions ----------
def perm_stat(func, reps=1000):
    out=np.empty(reps)
    for t in range(reps):
        vs = w.copy(); rng.shuffle(vs)
        vv = val.copy(); vv[nonzero]=vs
        out[t]=func(d, vv)
    return out

print("running nulls...")
nB = perm_stat(indexed_contig, 300)
print("Test B null mean/max/p:", nB.mean(), nB.max(), (1+(nB>=obsB).sum())/(1+300))
nC = perm_stat(indexed_subset, 200)
print("Test C null mean/max/p:", nC.mean(), nC.max(), (1+(nC>=obsC).sum())/(1+200))
np.save('analisis/ds/k_AS069/nullB.npy', nB); np.save('analisis/ds/k_AS069/nullC.npy', nC)
