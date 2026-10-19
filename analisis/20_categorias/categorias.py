import pandas as pd, numpy as np, re, itertools
from scipy.stats import kendalltau
rng=np.random.default_rng(20261018)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
q=pd.read_csv('analisis/datos/quipus.csv')
p=c[(c.nivel==0)&c.color.notna()].copy()
p['col']=p.color.astype(str).map(lambda s: re.sub(r'\([^)]*\)','',s))
p=p.sort_values(['kfg','orden'])
prov=q.set_index('kfg').procedencia.to_dict()
seqs={k:g.col.tolist() for k,g in p.groupby('kfg') if len(g)>=10}
ks=[k for k in seqs if str(prov.get(k,'Unknown')) not in ('Unknown','nan')]
print('quipus con procedencia y >=10 colgantes:',len(ks), 'procedencias:',len({prov[k] for k in ks}))
# --- Prueba 1: orden de categorías (posición media relativa de cada color)
pos={}
for k in ks:
    s=seqs[k]; n=len(s); d={}
    for i,x in enumerate(s): d.setdefault(x,[]).append(i/(n-1))
    pos[k]={x:np.mean(v) for x,v in d.items() if len(s)>0}
pares=[]
for a,b in itertools.combinations(ks,2):
    sh=[x for x in pos[a] if x in pos[b]]
    if len(sh)>=4:
        t=kendalltau([pos[a][x] for x in sh],[pos[b][x] for x in sh]).statistic
        if not np.isnan(t): pares.append((a,b,t))
P=pd.DataFrame(pares,columns=['a','b','tau'])
lab=np.array([prov[k] for k in ks]); idx={k:i for i,k in enumerate(ks)}
ia=P.a.map(idx).values; ib=P.b.map(idx).values; tau=P.tau.values
def stat(l): same=l[ia]==l[ib]; return tau[same].mean()-tau[~same].mean(), same.sum()
obs,ns=stat(lab); null=np.array([stat(rng.permutation(lab))[0] for _ in range(5000)])
print(f'P1 pares={len(P)} mismos_sitio={ns} tau_mismo={tau[lab[ia]==lab[ib]].mean():.3f} tau_distinto={tau[lab[ia]!=lab[ib]].mean():.3f} dif={obs:.3f} p={(null>=obs).mean()+1/5001:.4f}')
# sin Incahuasi ni pares casi idénticos (copias): excluir tau>0.9
m=tau<0.9; ia2,ib2,t2=ia[m],ib[m],tau[m]
def stat2(l): same=l[ia2]==l[ib2]; return t2[same].mean()-t2[~same].mean()
o2=stat2(lab); n2=np.array([stat2(rng.permutation(lab)) for _ in range(5000)])
print(f'P1 sin copias (tau<0.9): dif={o2:.3f} p={(n2>=o2).mean()+1/5001:.4f}')
# por sitio
P['sa']=lab[ia]; P['same']=lab[ia]==lab[ib]
print(P[P.same].groupby('sa').tau.agg(['size','mean']).sort_values('size',ascending=False).head(10).round(3))
P.to_csv('analisis/20_categorias/categorias_pares_tau.csv',index=False)
