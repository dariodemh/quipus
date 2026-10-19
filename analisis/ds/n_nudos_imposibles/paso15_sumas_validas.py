# -*- coding: utf-8 -*-
"""Paso 15b: sumas internas solo con cuerdas con nudos.
L10 y multiunidad con nulo de 5000 permutaciones; base con muestra de 120 quipus.
"""
import pandas as pd, numpy as np, time
from statsmodels.stats.multitest import multipletests
BASE = r"."
rng=np.random.default_rng(20261018)
df=pd.read_pickle(BASE+r"\análisis\ds\n_nudos_imposibles\cuerdas_valores2.pkl".replace("á","a"))
df["H"]=pd.to_numeric(df.valor,errors="coerce")
df["valid"]=df.knots.map(len)>0
df.loc[~df.valid,"H"]=np.nan
print("cuerdas:",len(df),"validas:",int(df.valid.sum()),flush=True)

def relations(sub):
    rel=[]
    for (k,p),g in sub[sub.padre!=""].groupby(["kfg","padre"]):
        par=sub[(sub.kfg==k)&(sub.cuerda==p)]
        if len(par)==1: rel.append(dict(kfg=k,tipo="madre",parent=p,children=list(g.cuerda)))
    g0=sub[sub.nivel==0]
    for (k,gr),g in g0.groupby(["kfg","grupo"]):
        if len(g)<2: continue
        h=g.sort_values("orden").iloc[0]
        rel.append(dict(kfg=k,tipo="grupo",parent=h.cuerda,children=list(g[g.cuerda!=h.cuerda].cuerda)))
    return pd.DataFrame(rel)

def test(sub,label,nperm=5000):
    rel=relations(sub)
    vm=sub.set_index("cuerda").H.to_dict()
    def ok(x):
        pv=vm.get(x.parent,np.nan); cs=[vm.get(c,np.nan) for c in x.children]
        if not np.isfinite(pv) or any(not np.isfinite(c) for c in cs): return np.nan
        return bool(np.isclose(pv,sum(cs)))
    rel["ok"]=rel.apply(ok,axis=1)
    rel=rel[rel.ok.notna()].copy()
    rows=[]
    for tipo in ["madre","grupo"]:
        rr=rel[rel.tipo==tipo]
        if len(rr)==0: continue
        O=int(rr.ok.sum()); n=len(rr)
        groups=[g for _,g in rr.groupby("kfg") if len(g)>1]
        null=np.zeros(nperm,dtype=int)
        for b in range(nperm):
            tot=0
            for g in groups:
                pv=g.parent.map(vm).values
                sv=np.array([sum(vm.get(c,np.nan) for c in ch) for ch in g.children])
                tot+=int(np.sum(np.isclose(rng.permutation(pv),sv)))
            null[b]=tot
        p=(1+np.sum(null>=O))/(1+nperm)
        rows.append(dict(conjunto=label,tipo=tipo,n=n,cierran=O,tasa=round(O/n,4),p=p,nulo=round(null.mean(),2)))
    return pd.DataFrame(rows),rel

gen_q=sorted(df[df.clase_L=="vueltas_reales"].kfg.unique())
t0=time.time(); r1,rel1=test(df[df.kfg.isin(gen_q)].copy(),"L10_real"); print("L10 listo",time.time()-t0,flush=True)
qs=df[df.cat_pos=="multiunidad_real"].kfg.value_counts(); qs=qs[qs>=5].index.tolist()
t0=time.time(); r2,rel2=test(df[df.kfg.isin(qs)].copy(),"multiunidad"); print("multi listo",time.time()-t0,flush=True)
# base: muestra de 120 quipus con >=50 cuerdas
big=df.groupby("kfg").size(); cand=big[big>=50].index.tolist()
sample=list(rng.choice(cand,size=min(120,len(cand)),replace=False))
t0=time.time(); r3,rel3=test(df[df.kfg.isin(sample)].copy(),"base_120q",nperm=1000); print("base listo",time.time()-t0,flush=True)
res=pd.concat([r1,r2,r3],ignore_index=True)
res["p_holm"]=multipletests(res.p,method="holm")[1]
res["q_bh"]=multipletests(res.p,method="fdr_bh")[1]
print(res.round(4).to_string(index=False))
res.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\resultados_sumas_validas.csv",index=False)

print("\nDetalle L10 por quipu:")
for k in gen_q:
    rr=rel1[rel1.kfg==k]
    if len(rr): print(k,rr.tipo.value_counts().to_dict(),"cierran:",int(rr.ok.sum()),"/",len(rr))
print("\nCierres L10:")
print(rel1[rel1.ok==True][["kfg","tipo","parent","children"]].to_string(index=False))
print("\nCierres multiunidad:")
print(rel2[rel2.ok==True][["kfg","tipo","parent","children"]].head(20).to_string(index=False))
