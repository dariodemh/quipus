# Réplica de zonas con altura RELATIVA al largo de la cuerda (posición/largo) en la familia UR050–055 y tally puros
import pandas as pd, numpy as np, re
from sklearn.mixture import GaussianMixture
rng=np.random.default_rng(20261018)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
R=re.compile(r'(\d+)([A-Z]+)\(([\d.]+),([A-Z])\)')
def analiza(q):
    g=c[(c.kfg==q)&(c.nivel==0)&c.nudos.notna()&(pd.to_numeric(c.largo,errors='coerce')>0)]
    rows=[]
    for s,L in zip(g.nudos,pd.to_numeric(g.largo)):
        r=sorted((float(p)/L,int(n)) for n,t,p,d in R.findall(s) if t=='L')
        if len(r)>=2 and all(x[0]<=1.05 for x in r): rows.append(r)
    if len(rows)<20: return None
    X=np.concatenate([[p for p,_ in r] for r in rows]).reshape(-1,1)
    bic={k:GaussianMixture(k,random_state=0).fit(X).bic(X) for k in range(1,6)}; kb=min(bic,key=bic.get)
    # separación: BIC(kb) vs BIC(1) y nulo de alturas uniformes con el mismo nº de nudos por cuerda
    d_obs=bic[1]-bic[kb]
    nul=[]
    for _ in range(100):
        Xn=rng.uniform(X.min(),X.max(),size=X.shape)
        b={k:GaussianMixture(k,random_state=0).fit(Xn).bic(Xn) for k in (1,kb)}; nul.append(b[1]-b[kb])
    gm=GaussianMixture(kb,random_state=0).fit(X); lab=np.argsort(np.argsort(gm.means_.ravel()))[gm.predict(X)]
    i=0; tab=[]
    for r in rows:
        d={}
        for (p,n) in r: d[lab[i]]=d.get(lab[i],0)+n; i+=1
        tab.append(d)
    T=pd.DataFrame(tab).reindex(columns=range(kb)).dropna().values
    cv=lambda s: s.std()/s.mean()
    pc=np.nan
    if kb>=2 and len(T)>=15:
        o=cv(T.sum(1)); nn=np.array([cv(np.column_stack([rng.permutation(T[:,j]) for j in range(kb)]).sum(1)) for _ in range(5000)]); pc=(nn<=o).mean()
    return dict(kfg=q,cuerdas=len(rows),zonas=kb,centros=np.sort(gm.means_.ravel()).round(2).tolist(),dBIC=round(d_obs,1),dBIC_nulo_max=round(max(nul),1),filas=len(T),p_compensa=pc)
qs=['UR050','UR051','UR052','UR054','UR055','UR003','UR007','UR112','UR110','UR282','UR289','HP019','HP020','AS076','JC012','UR178']
res=[r for r in map(analiza,qs) if r]
out=pd.DataFrame(res); 
from statsmodels.stats.multitest import multipletests
m=out.p_compensa.notna(); out.loc[m,'holm']=multipletests(out.loc[m,'p_compensa']+1/5001,method='holm')[1]
print(out.to_string(index=False)); out.to_csv('analisis/20_categorias/zonas_relativas.csv',index=False)
