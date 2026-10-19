import pandas as pd, numpy as np
rng = np.random.default_rng(0)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['pos_in'] = d.orden - d.groupby('grupo').orden.transform('min')
val = d.valor.to_numpy(float)
nz = val>0
w = val[nz]

# ---- Test A: madre = suma de subsidiarias ----
def testA(df, vals):
    df=df.copy(); df['v']=vals
    kids = df[df.padre.notna()].groupby('padre')['v'].sum()
    moms = df.set_index('cuerda')['v']
    common = kids.index.intersection(moms.index)
    return int(np.isclose(moms.loc[common].to_numpy(), kids.loc[common].to_numpy()).sum())
obsA = testA(d,val)
oA=np.array([testA(d, (lambda vv: (lambda x: (x.__setitem__(nz, rng.permutation(w)), x)[1])(val.copy()))(None)) for _ in range(300)])
# simpler: redo properly
oA=np.empty(300)
for t in range(300):
    vv=val.copy(); vv[nz]=rng.permutation(w); oA[t]=testA(d,vv)
print("Test A madre=suma hijos: obs", obsA, "null mean", round(oA.mean(),2), "max", oA.max(), "p", (1+(oA>=obsA).sum())/301)

# ---- Test D: igualdad de sumas de grupo ----
gs = d.groupby('grupo')['valor'].sum()
def testD(df, vals):
    df=df.copy(); df['v']=vals
    s = df[df.v>0].groupby('grupo')['v'].sum()
    vc = s[s>0].value_counts()
    return int((vc*(vc-1)//2).sum())  # number of equal pairs
obsD=testD(d,val)
oD=np.empty(1000)
for t in range(1000):
    vv=val.copy(); vv[nz]=rng.permutation(w); oD[t]=testD(d,vv)
print("Test D grupos con suma igual (pares): obs", obsD, "null mean", round(oD.mean(),1), "max", oD.max(), "p", (1+(oD>=obsD).sum())/1001)

# ---- Test E1: clustering de color (marker flag) ----
flag = (d.color != 'W').to_numpy()
def runs(f):
    return 1+int((f[1:]!=f[:-1]).sum())
obsE = runs(flag)
oE=np.array([runs(rng.permutation(flag)) for _ in range(1000)])
print("Test E1 runs de color: obs", obsE, "null mean", round(oE.mean(),1), "min", oE.min(), "p(low)", (1+(oE<=obsE).sum())/1001)

# ---- Test E2: pos_in 0 mas coloreado ----
obsE2 = int((flag & (d.pos_in.to_numpy()==0)).sum())
firstmask = (d.pos_in.to_numpy()==0)
print("Test E2: cuerdas coloreadas con pos_in=0:", obsE2, "de", int(firstmask.sum()), "cords en pos_in=0")
print("   total coloreadas:", int(flag.sum()), "de", len(d))
# expected under independence
exp = flag.mean()*firstmask.sum()
print("   esperado si independiente:", round(exp,1))
oE2=np.empty(1000)
for t in range(1000):
    oE2[t]=int((rng.permutation(flag) & firstmask).sum())
print("   p(>=obs):", (1+(oE2>=obsE2).sum())/1001)
