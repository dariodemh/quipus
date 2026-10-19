# -*- coding: utf-8 -*-
"""Paso 9: prueba de sumas internas bajo lecturas alternativas + nulo por permutacion.
Relaciones: madre = suma de hijas directas; cabeza de grupo = suma del resto.
Cada prueba: p empirico permutando el valor de la madre/cabeza dentro del quipu.
Correccion Holm y BH sobre todas las pruebas.
"""
import pandas as pd, numpy as np
from scipy.stats import binomtest
BASE = r"."
rng=np.random.default_rng(20261018)

df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
df["valor"]=pd.to_numeric(df.valor,errors="coerce")
df["H"]=df.valor  # lectura del transcriptor = suma de contribuciones KFG
df["valid"]=df.knots.map(len)>0
gen_q = sorted(df[df.clase_L=="vueltas_reales"].kfg.unique().tolist())
sub=df[df.kfg.isin(gen_q)].copy()
READ=["H","D","U","M","LU","B5","B8","B12","B16","B20"]

# relaciones madre-hija
rel=[]
for (k,p),g in sub[sub.padre!=""].groupby(["kfg","padre"]):
    par=sub[(sub.kfg==k)&(sub.cuerda==p)]
    if len(par)!=1: continue
    rel.append(dict(kfg=k, tipo="madre", parent=p, children=list(g.cuerda), n=len(g)))
rel=pd.DataFrame(rel)
# grupos
g0=sub[sub.nivel==0]
for (k,gr),g in g0.groupby(["kfg","grupo"]):
    if len(g)<2: continue
    head=g.sort_values("orden").iloc[0]
    rel=pd.concat([rel,pd.DataFrame([dict(kfg=k,tipo="grupo",parent=head.cuerda,children=list(g[g.cuerda!=head.cuerda].cuerda),n=len(g)-1)])],ignore_index=True)
print("relaciones totales:",len(rel),rel.tipo.value_counts().to_dict())

vmap={r.cuerda:r for _,r in sub.iterrows()}
def val(cord,read):
    r=vmap.get(cord)
    if r is None or not bool(r.valid): return np.nan
    return r[read]

def obs_closures(rel,read):
    ok=[]
    for _,x in rel.iterrows():
        pv=val(x.parent,read)
        cs=[val(c,read) for c in x.children]
        if not np.isfinite(pv) or any(not np.isfinite(c) for c in cs):
            ok.append(np.nan); continue
        ok.append(bool(np.isclose(pv,sum(cs))))
    return np.array(ok,dtype=float)

rows=[]
NPERM=5000
for read in READ:
    for tipo in ["madre","grupo"]:
        rr=rel[rel.tipo==tipo].copy()
        ok=obs_closures(rr,read)
        base=rr.assign(ok=ok)
        base=base[np.isfinite(ok)]
        if len(base)==0: continue
        O=int(base.ok.sum())
        # nulo: permutar valores de padres entre relaciones dentro de cada quipu
        null=np.zeros(NPERM,dtype=int)
        groups=[g for _,g in base.groupby("kfg") if len(g)>1]
        for b in range(NPERM):
            tot=0
            for g in groups:
                pv=g.parent.map(lambda c:val(c,read)).values
                sv=np.array([sum(val(c,read) for c in ch) for ch in g.children])
                perm=rng.permutation(pv)
                tot+=int(np.sum(np.isclose(perm,sv)))
            # relaciones en quipus con 1 sola relacion: no aportan al nulo (siempre cierran o no)
            null[b]=tot
        p=(1+np.sum(null>=O))/(1+NPERM)
        rows.append(dict(lectura=read,tipo=tipo,n=len(base),cierran=O,tasa=O/len(base),p=p,
                         nulo_medio=null.mean()))
res=pd.DataFrame(rows)
# corregir multiple
from statsmodels.stats.multitest import multipletests
res["p_holm"]=multipletests(res.p,method="holm")[1]
res["q_bh"]=multipletests(res.p,method="fdr_bh")[1]
print("\nRESULTADOS POOL (14 quipus con vueltas reales):")
print(res.round(4).to_string(index=False))
res.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\resultados_sumas.csv",index=False)

# detalle por quipu para los 6 principales, lectura H y D
print("\nDETALLE POR QUIPU (H / D / U):")
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS014","AS078"]:
    out=[]
    for read in ["H","D","U"]:
        for tipo in ["madre","grupo"]:
            rr=rel[(rel.kfg==k)&(rel.tipo==tipo)]
            if len(rr)==0: continue
            ok=obs_closures(rr,read); ok=ok[np.isfinite(ok)]
            out.append(f"{read}-{tipo}:{int(ok.sum())}/{len(ok)}")
    print(k," ".join(out))
