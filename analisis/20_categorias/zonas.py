import pandas as pd, numpy as np, re
rng=np.random.default_rng(5)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
R=re.compile(r'(\d+)([A-Z]+)\(([\d.]+),([A-Z])\)')
for q in ['UR050','UR054','UR055','UR052','UR051']:
    g=c[(c.kfg==q)&(c.nivel==0)&c.nudos.notna()]
    rows=[[(float(p),int(n)) for n,t,p,d in R.findall(s) if t=='L'] for s in g.nudos]
    rows=[sorted(r) for r in rows if len(r)>=2]
    nk=pd.Series([len(r) for r in rows]).value_counts().sort_index().to_dict()
    pos=np.concatenate([[p for p,_ in r] for r in rows])
    # agrupar alturas con k-medias 1D para k=2..6, elegir k por BIC simple; comparar con alturas uniformes
    from sklearn.mixture import GaussianMixture
    X=pos.reshape(-1,1); bic={k:GaussianMixture(k,random_state=0).fit(X).bic(X) for k in range(1,7)}
    kb=min(bic,key=bic.get); gm=GaussianMixture(kb,random_state=0).fit(X)
    mu=np.sort(gm.means_.ravel()).round(1)
    # coherencia: ¿la k-ésima cuenta de cada cuerda cae en la misma zona? (posición relativa al largo omitida)
    # efecto de zona sobre el valor y correlación entre zonas a través de cuerdas
    lab=np.argsort(np.argsort(gm.means_.ravel()))[gm.predict(X)]
    i=0; tab=[]
    for r in rows:
        d={}
        for (p,n) in r: d.setdefault(lab[i],[]).append(n); i+=1
        tab.append({z:sum(v) for z,v in d.items()})
    T=pd.DataFrame(tab).reindex(columns=range(kb))
    full=T.dropna()
    print(f'== {q}: cuerdas={len(rows)} nudos/cuerda={nk} zonas(BIC)={kb} centros={mu.tolist()} filas completas={len(full)}')
    print('   media por zona', T.mean().round(2).tolist(), ' n por zona', T.notna().sum().tolist())
    if len(full)>=10 and kb>=2:
        from scipy.stats import friedmanchisquare, spearmanr
        if kb>=3: print('   Friedman zonas', friedmanchisquare(*[full[z] for z in range(kb)]))
        cr=full.corr(method='spearman').values[np.triu_indices(kb,1)]; print('   corr entre zonas (spearman) media', cr.mean().round(3))

print('--- ¿reparto de un total fijo? CV de la suma de la fila frente a barajar columnas entre filas')
for q in ['UR050','UR054','UR055','UR052','UR051']:
    g=c[(c.kfg==q)&(c.nivel==0)&c.nudos.notna()]
    rows=[sorted([(float(p),int(n)) for n,t,p,d in R.findall(s) if t=='L']) for s in g.nudos]
    rows=[r for r in rows if len(r)>=2]
    pos=np.concatenate([[p for p,_ in r] for r in rows]).reshape(-1,1)
    from sklearn.mixture import GaussianMixture
    bic={k:GaussianMixture(k,random_state=0).fit(pos).bic(pos) for k in range(1,7)}; kb=min(bic,key=bic.get)
    gm=GaussianMixture(kb,random_state=0).fit(pos); lab=np.argsort(np.argsort(gm.means_.ravel()))[gm.predict(pos)]
    i=0; tab=[]
    for r in rows:
        d={}
        for (p,n) in r: d[lab[i]]=d.get(lab[i],0)+n; i+=1
        tab.append(d)
    T=pd.DataFrame(tab).reindex(columns=range(kb)).dropna().values
    cv=lambda s: s.std()/s.mean()
    o=cv(T.sum(1)); nul=np.array([cv(np.column_stack([rng.permutation(T[:,j]) for j in range(kb)]).sum(1)) for _ in range(5000)])
    print(f'{q}: filas={len(T)} CV suma={o:.3f} nulo={nul.mean():.3f} p(menor)={(nul<=o).mean():.4f}  suma media={T.sum(1).mean():.1f}')
