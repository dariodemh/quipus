# -*- coding: utf-8 -*-
"""Paso 14: sumas internas en quipus con 'multiunidad_real' (varias unidades
que suman >9), sin necesidad de L>=10. Lectura H (suma de contribuciones KFG).
"""
import pandas as pd, numpy as np
from statsmodels.stats.multitest import multipletests
BASE = r"."
rng=np.random.default_rng(20261018)
df=pd.read_pickle(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_valores2.pkl")
df["H"]=pd.to_numeric(df.valor,errors="coerce")
qs=df[df.cat_pos=="multiunidad_real"].kfg.value_counts()
qs=qs[qs>=5].index.tolist()
print("quipus con >=5 cuerdas multiunidad_real:",len(qs),qs)
sub=df[df.kfg.isin(qs)].copy()

rel=[]
for (k,p),g in sub[sub.padre!=""].groupby(["kfg","padre"]):
    par=sub[(sub.kfg==k)&(sub.cuerda==p)]
    if len(par)==1: rel.append(dict(kfg=k,tipo="madre",parent=p,children=list(g.cuerda)))
g0=sub[sub.nivel==0]
for (k,gr),g in g0.groupby(["kfg","grupo"]):
    if len(g)<2: continue
    h=g.sort_values("orden").iloc[0]
    rel.append(dict(kfg=k,tipo="grupo",parent=h.cuerda,children=list(g[g.cuerda!=h.cuerda].cuerda)))
rel=pd.DataFrame(rel)
vmap=sub.set_index("cuerda").H.to_dict()
def ok(x):
    pv=vmap.get(x.parent,np.nan); cs=[vmap.get(c,np.nan) for c in x.children]
    return np.isfinite(pv) and all(np.isfinite(cs)) and np.isclose(pv,sum(cs))
rows=[]
for tipo in ["madre","grupo"]:
    rr=rel[rel.tipo==tipo].copy(); rr["ok"]=rr.apply(ok,axis=1)
    rr=rr[rr.ok.notna()]
    O=int(rr.ok.sum()); n=len(rr)
    groups=[g for _,g in rr.groupby("kfg") if len(g)>1]
    null=[]
    for b in range(5000):
        tot=0
        for g in groups:
            pv=g.parent.map(vmap).values; sv=np.array([sum(vmap.get(c,np.nan) for c in ch) for ch in g.children])
            null.append(0)  # placeholder
        # recomputar bien
        tot=0
        for g in groups:
            pv=g.parent.map(vmap).values; sv=np.array([sum(vmap.get(c,np.nan) for c in ch) for ch in g.children])
            tot+=int(np.sum(np.isclose(rng.permutation(pv),sv)))
        null[-1]=tot
    null=np.array(null)
    p=(1+np.sum(null>=O))/(1+len(null))
    rows.append(dict(tipo=tipo,n=n,cierran=O,tasa=O/n,p=p,nulo=null.mean()))
res=pd.DataFrame(rows)
print(res.round(4).to_string(index=False))
print("\nDetalle por quipu (H, madre):")
for k in qs:
    rr=rel[(rel.kfg==k)&(rel.tipo=="madre")].copy()
    if len(rr)==0: continue
    rr["ok"]=rr.apply(lambda x: ok(x),axis=1); rr=rr[rr.ok.notna()]
    if len(rr): print(k,f"{int(rr.ok.sum())}/{len(rr)}")
print("\nGrupos que cierran:")
gg=rel[rel.tipo=="grupo"].copy(); gg["ok"]=gg.apply(lambda x: ok(x),axis=1)
print(gg[gg.ok==True][["kfg","parent","children"]].to_string(index=False))
