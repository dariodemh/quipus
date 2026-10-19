import pandas as pd, numpy as np, re
from collections import defaultdict
rng=np.random.default_rng(7)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
q=pd.read_csv('analisis/datos/quipus.csv'); prov=q.set_index('kfg').procedencia.astype(str).to_dict()
p=c[(c.nivel==0)&c.color.notna()].copy()
p['col']=p.color.astype(str).map(lambda s: re.sub(r'\([^)]*\)','',s))
p=p.sort_values(['kfg','orden'])
grupos=[(k,g2.col.tolist()) for (k,_),g2 in p.groupby(['kfg','grupo']) if 3<=len(g2)<=12]
print('grupos 3-12 cuerdas:',len(grupos))
def compartidos(gr):
    # patrones ordenados (tupla completa del grupo) con >=2 colores distintos, en cuántos quipus aparecen
    d=defaultdict(set)
    for k,s in gr:
        if len(set(s))>=2: d[tuple(s)].add(k)
    multi={t:v for t,v in d.items() if len(v)>=2}
    n=sum(len(v) for v in multi.values())
    same=sum(1 for t,v in multi.items() if len({prov.get(k,'Unknown') for k in v}-{'Unknown','nan'})==1 and all(prov.get(k,'Unknown') not in('Unknown','nan') for k in v))
    return len(multi), n, same, multi
obs=compartidos(grupos); print('obs patrones compartidos:',obs[:3])
nul=[]
for _ in range(500):
    g2=[(k,list(rng.permutation(s))) for k,s in grupos]
    nul.append(compartidos(g2)[:3])
nul=np.array(nul); print('nulo (orden barajado dentro del grupo) media:',nul.mean(0).round(1),'p:',[(nul[:,i]>=obs[i]).mean() for i in range(3)])
multi=obs[3]
top=sorted(multi.items(),key=lambda x:-len(x[1]))[:25]
for t,v in top: print(len(v),'-'.join(t),sorted({prov.get(k,'?') for k in v})[:4])
