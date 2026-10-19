import pandas as pd, numpy as np, re
rng=np.random.default_rng(11)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
p=c[(c.nivel==0)&c.color.notna()&c.valor.notna()].copy()
p['col']=p.color.astype(str).map(lambda s: re.sub(r'\([^)]*\)','',s))
p['y']=np.log1p(p.valor.astype(float))
def eta2(y,g):
    m=y.mean(); ss=((y-m)**2).sum()
    if ss==0: return np.nan
    df=pd.DataFrame({'y':y,'g':g}); b=df.groupby('g').y.agg(['mean','size'])
    return ((b['mean']-m)**2*b['size']).sum()/ss
res=[]
for k,g in p.groupby('kfg'):
    vc=g.col.value_counts()
    if len(g)<20 or (vc>=3).sum()<2: continue
    g=g[g.col.isin(vc[vc>=3].index)]
    y=g.y.values; col=g.col.values
    o=eta2(y,col)
    if np.isnan(o): continue
    # nulo 1: color barajado en todo el quipu; nulo 2: barajado dentro de cada grupo (controla posición/grupo)
    n1=np.array([eta2(y,rng.permutation(col)) for _ in range(300)])
    gr=g.grupo.values; n2=[]
    for _ in range(300):
        cc=col.copy()
        for u in np.unique(gr):
            ix=np.where(gr==u)[0]; cc[ix]=rng.permutation(cc[ix])
        n2.append(eta2(y,cc))
    n2=np.array(n2)
    res.append((k,len(g),len(vc[vc>=3]),o,(n1>=o).mean(),(n2>=o).mean()))
r=pd.DataFrame(res,columns=['kfg','n','ncol','eta2','p_global','p_engrupo'])
from statsmodels.stats.multitest import multipletests
r['q1']=multipletests(r.p_global+1/301,method='fdr_bh')[1]; r['q2']=multipletests(r.p_engrupo+1/301,method='fdr_bh')[1]
print('quipus probados',len(r)); print('mediana eta2',r.eta2.median().round(3))
print('q<0.05 color barajado en todo el quipu:',(r.q1<0.05).sum(),'| barajado dentro de grupo:',(r.q2<0.05).sum())
print('esperado por azar ~',round(0.05*len(r),1))
r.to_csv('analisis/20_categorias/categorias_color_valor.csv',index=False)
print(r.sort_values('eta2',ascending=False).head(12).round(3).to_string(index=False))
