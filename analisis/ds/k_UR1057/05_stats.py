import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
rng = np.random.default_rng(0)
n = pd.read_csv('analisis/ds/k_UR1057/pendientes_estructurado.csv')
n['blank'] = n.nudos.isna()
n['parte'] = np.where(n.grupo_a<=7,'P1','P2')
n['vk'] = pd.cut(n.valor,[-0.1,0.1,1.1,2.1,4.1,1e9],labels=['0','1','2','4','>4'])
out=[]
def rec(test,stat,obs,p,note=''):
    out.append(dict(test=test,estadistico=stat,observado=obs,p=p,nota=note))
    print(f"{test:38s} {stat:12s} obs={obs:8.3f}  p={p:.4f}  {note}")

# ---------- A. plantilla de color ----------
# firma canonica por (sg,pos): sg1-4 = Y W Y Y ; sg5 = W Y 0
canon = {(1,1):'YB',(1,2):'W',(1,3):'YB',(1,4):'YB',
         (2,1):'YB',(2,2):'W',(2,3):'YB',(2,4):'YB',
         (3,1):'YB',(3,2):'W',(3,3):'YB',(3,4):'YB',
         (4,1):'YB',(4,2):'W',(4,3):'YB',(4,4):'YB',
         (5,1):'W:FB',(5,2):'YB',(5,3):'0G'}
d = n[n.sg>0].copy()
d['match'] = [canon.get((int(r.sg),int(r.pos)),None)==r.col for r in d.itertuples()]
obs = d.match.mean()
# nulo: barajar colores entre cuerdas del quipu
col = d.col.values.copy(); stats=[]
for _ in range(1000):
    rng.shuffle(col)
    stats.append(np.mean([canon.get((int(sg),int(pos)),None)==c for sg,pos,c in zip(d.sg,d.pos,col)]))
p=(np.sum(np.array(stats)>=obs)+1)/1001
rec('A plantilla color (acierto)', 'proporcion', obs, p, f'n={len(d)}; nulo baraja colores')

# ---------- B. asociacion sg x clase de valor ----------
ct = pd.crosstab(d.sg,d.vk)
def chi2(ct):
    e=np.outer(ct.sum(1),ct.sum(0))/ct.values.sum()
    return ((ct.values-e)**2/np.maximum(e,1e-9)).sum()
obsB=chi2(ct)
vals=d.vk.values.copy(); stats=[]
for _ in range(1000):
    rng.shuffle(vals)
    stats.append(chi2(pd.crosstab(d.sg,vals)))
pB=(np.sum(np.array(stats)>=obsB)+1)/1001
rec('B sg x clase de valor', 'chi2', obsB, pB, 'nulo baraja valores (global)')

# ---------- C. blancura x sg ----------
obsC = d.groupby('sg').blank.mean().std()
bl=d.blank.values.copy(); stats=[]
for _ in range(1000):
    rng.shuffle(bl)
    stats.append(pd.Series(bl).groupby(d.sg.values).mean().std())
pC=(np.sum(np.array(stats)>=obsC)+1)/1001
rec('C blancura por subgrupo (sd)', 'sd', obsC, pC, 'nulo baraja blank')

# ---------- D. sg4 = cuatro 1s ----------
def n_ones4(df):
    c=0
    for g,s in df[df.sg==4].groupby('grupo_a'):
        v=s.sort_values('pos').valor.values
        if len(v)==4 and (v==1).all(): c+=1
    return c
obsD=n_ones4(d); stats=[]
for _ in range(1000):
    dd=d.copy()
    dd['valor']=dd.groupby('grupo_a').valor.transform(lambda s: rng.permutation(s.values))
    stats.append(n_ones4(dd))
pD=(np.sum(np.array(stats)>=obsD)+1)/1001
rec('D sg4=(1,1,1,1) por grupo', 'n grupos', obsD, pD, 'nulo permuta valores dentro de grupo')

# ---------- E. aritmetica ----------
# E1 madre = suma de subsidiarias (datos crudos, incluye subsidiarias)
raw = pd.read_csv('analisis/datos/cuerdas.csv'); raw = raw[raw.kfg=='UR1057']
m = raw[raw.nivel==0][['cuerda','valor']]
sub = raw[raw.nivel>0].groupby('padre').valor.sum()
mm = m[m.cuerda.isin(sub.index)].copy(); mm['subsum']=mm.cuerda.map(sub); mm['ok']=mm.valor==mm.subsum
e1 = int(mm[mm.subsum>0].ok.sum())
rec('E1 madre=suma subsidiarias', 'aciertos no triviales', e1, np.nan,
    f'{len(mm)} madres con subsidiarias; con subsidiaria>0: {int((mm.subsum>0).sum())}; pares={list(zip(mm.cuerda,mm.valor,mm.subsum))}')

# E2 top cords = suma de grupo
tops = raw[raw.cuerda.isin(['p441','p537'])]
rec('E2 top cord vs suma grupo', 'valores', np.nan, np.nan, f'T={tops[["cuerda","valor"]].values.tolist()}; sumas de grupo={n.groupby("grupo_a").valor.sum().tolist()}')

# E3 suma de subgrupos = total de grupo con top cord? no hay
# E4 suma de los 4 cordones de un subgrupo = valor del 5o? buscar coincidencias exactas entre sumas de sg1-4 y valores de sg5
hits=0; tot=0
for g,s in d.groupby('grupo_a'):
    ss={sg:x.valor.sum() for sg,x in s.groupby('sg')}
    for a in [1,2,3,4]:
        for b in [5]:
            if ss.get(a,0)==ss.get(b,0): hits+=1
            tot+=1
rec('E4 suma sg vs suma sg5 (exploratoria)', 'n coincidencias', hits, np.nan, f'{tot} comparaciones; nulo propio en 07_stats2.py')

# ---------- F. duplicados de filas ----------
rows=[]
for g,s in d.groupby('grupo_a'):
    rows.append(tuple(s.sort_values(['sg','pos']).valor.values[:19]))
from collections import Counter
cnt=Counter(rows)
rep=sum(v for v in cnt.values() if v>1)
rec('F filas de grupo duplicadas', 'n filas en duplicados', rep, np.nan, f'{len(cnt)} filas unicas de 24')

# ---------- G. autocorrelacion ----------
seq = d.sort_values('ord').valor.values.astype(float)
def ac(x,lag):
    x=x-x.mean(); return float((x[:-lag]*x[lag:]).sum()/(x*x).sum())
obsG=max(abs(ac(seq,l)) for l in range(1,21)); lagmax=int(np.argmax([abs(ac(seq,l)) for l in range(1,21)])+1)
stats=[]
for _ in range(1000):
    rng.shuffle(seq.copy())
    s2=rng.permutation(d.sort_values('ord').valor.values.astype(float))
    stats.append(max(abs(ac(s2,l)) for l in range(1,21)))
pG=(np.sum(np.array(stats)>=obsG)+1)/1001
rec('G autocorrelacion max |rho| lags1-20','|rho|',obsG,pG,f'lag={lagmax}')

# ---------- H. tendencia por indice de grupo ----------
gs=n.groupby('grupo_a').valor.sum().values.astype(float)
rho=np.corrcoef(np.arange(1,25),gs)[0,1]
stats=[]
for _ in range(1000):
    stats.append(np.corrcoef(np.arange(1,25),rng.permutation(gs))[0,1])
pH=(np.sum(np.abs(np.array(stats))>=abs(rho))+1)/1001
rec('H tendencia suma~indice grupo','rho',rho,pH,'nulo permuta sumas')

pd.DataFrame(out).to_csv('analisis/ds/k_UR1057/tests.csv',index=False)
