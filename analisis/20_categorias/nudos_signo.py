import pandas as pd, numpy as np, re
from collections import Counter
rng=np.random.default_rng(3)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
c=c[c.nudos.notna()].copy()
R=re.compile(r'(\d+)([A-Z]+)\(([\d.]+),([A-Z])\)')
def parse(s):
    k=[(int(n),t,float(p),d) for n,t,p,d in R.findall(str(s))]
    return sorted(k,key=lambda x:x[2])
c['k']=c.nudos.map(parse)
print('tipos de nudo:',Counter(t for ks in c.k for _,t,_,_ in ks).most_common(8))
U={'L','E'}
def viol(ks):
    t=[x[1] for x in ks]
    nu=sum(1 for x in t if x in U)
    if nu>1: return 'multi_unidad'
    if nu==1 and t[-1] not in U: return 'unidad_no_al_final'
    return ''
c['viol']=c.k.map(viol)
c['ndir']=c.k.map(lambda ks:len({d for *_,d in ks if d in 'SZ'}))
print('cuerdas con nudos:',len(c),' violan:',(c.viol!='').sum(), c.viol.value_counts().to_dict())
v=c[c.viol!=''].copy()
print('quipus con >=5 cuerdas que violan:',(v.kfg.value_counts()>=5).sum())
print(v.kfg.value_counts().head(12).to_dict())
# firma = secuencia (tipo,direccion) sin cantidades + cantidad de los nudos unidad
v['firma']=v.k.map(lambda ks:'|'.join(f'{t}{n if t in U else ""}{d}' for n,t,p,d in ks))
v['col']=v.color.astype(str).map(lambda s: re.sub(r'\([^)]*\)','',s))
# (a) vocabulario recurrente: firmas en >=2 quipus vs nulo barajando grupos de nudos entre cuerdas violadoras (misma long.)
def rec(fir,kf):
    d={}
    for f,k in zip(fir,kf): d.setdefault(f,set()).add(k)
    return sum(1 for s in d.values() if len(s)>=2)
obs=rec(v.firma,v.kfg)
allk=[x for ks in v.k for x in ks]; L=v.k.map(len).values
nul=[]
for _ in range(300):
    pk=rng.permutation(len(allk)); i=0; fs=[]
    for l in L:
        ks=sorted([allk[j] for j in pk[i:i+l]],key=lambda x:x[2]); i+=l  # orden por posición original
        fs.append('|'.join(f'{t}{n if t in U else ""}{d}' for n,t,p,d in ks))
    nul.append(rec(fs,v.kfg))
nul=np.array(nul); print(f'(a) firmas compartidas entre quipus: obs={obs} nulo={nul.mean():.1f} p={(nul>=obs).mean():.3f}')
# (b) color x firma dentro de cada quipu: MI vs permutar color dentro del quipu
def mi(a,b):
    t=pd.crosstab(a,b).values; n=t.sum(); pa=t.sum(1,keepdims=True)/n; pb=t.sum(0,keepdims=True)/n; pj=t/n
    m=pj>0; return (pj[m]*np.log(pj[m]/(pa@pb)[m])).sum()
res=[]
for k,g in v.groupby('kfg'):
    if len(g)<10 or g.col.nunique()<2 or g.firma.nunique()<2: continue
    o=mi(g.col,g.firma); n=np.array([mi(rng.permutation(g.col.values),g.firma) for _ in range(500)])
    res.append((k,len(g),g.col.nunique(),g.firma.nunique(),o,(n>=o).mean()))
r=pd.DataFrame(res,columns=['kfg','n','ncol','nfirma','MI','p'])
from statsmodels.stats.multitest import multipletests
if len(r): r['q']=multipletests(r.p+1/501,method='fdr_bh')[1]
print('(b) quipus probados',len(r),' q<0.05:',(r.q<0.05).sum()); print(r.sort_values('p').head(10).round(3).to_string(index=False))
# (c) dirección: en cuerdas violadoras, ¿el nudo "fuera de lugar" tiene dirección distinta a los demás?
def fuera(ks):
    t=[x[1] for x in ks]
    idx=[i for i,x in enumerate(t) if x in U][:-1] if sum(x in U for x in t)>1 else [i for i,x in enumerate(t) if x in U]
    if not idx or len(ks)<2: return None
    i=idx[0]; otros=[x[3] for j,x in enumerate(ks) if j!=i and x[3] in 'SZ']
    if ks[i][3] not in 'SZ' or not otros: return None
    return ks[i][3]!=Counter(otros).most_common(1)[0][0]
f=v.k.map(fuera).dropna(); 
base=c[c.viol==''].k.map(lambda ks: None if len(ks)<2 or not all(x[3] in 'SZ' for x in ks) else ks[-1][3]!=Counter(x[3] for x in ks[:-1]).most_common(1)[0][0]).dropna()
print(f'(c) nudo fuera de lugar con dirección distinta: {f.mean():.3f} (n={len(f)}) vs último nudo en cuerdas normales: {base.mean():.3f} (n={len(base)})')
v.to_csv('analisis/20_categorias/nudos_fuera_de_regla.csv',index=False)
