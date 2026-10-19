# -*- coding: utf-8 -*-
"""Paso 10: controles estructurales de las cuerdas con vueltas reales >=10.
- color: enriquecimiento en el color modal del quipu (Fisher por quipu + combinado)
- cabeza de grupo (solo grupos >=2)
- posicion relativa y rango del racimo vs nudos L normales (2-9)
- coocurrencia con S y con L normales
"""
import pandas as pd, numpy as np
from scipy.stats import fisher_exact, mannwhitneyu, wilcoxon, combine_pvalues
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
df["largo_num"]=pd.to_numeric(df.largo,errors="coerce")
gen_q = sorted(df[df.clase_L=="vueltas_reales"].kfg.unique().tolist())
sub=df[df.kfg.isin(gen_q)].copy()

# cabeza de grupo
lvl0=sub[sub.nivel==0]
head=lvl0.sort_values("orden").groupby(["kfg","grupo"]).first().reset_index()[["kfg","grupo","cuerda"]]
head["es_cabeza"]=True
sub=sub.merge(head,on=["kfg","grupo","cuerda"],how="left")
sub["es_cabeza"]=sub.es_cabeza.fillna(False).astype(bool)

# color modal y Fisher
rows=[]
for k,g in sub.groupby("kfg"):
    gen=g[g.clase_L=="vueltas_reales"]
    if len(gen)<3: continue
    modal=g.color_limpio.value_counts().index[0]
    a=int((gen.color_limpio==modal).sum()); b=len(gen)-a
    c=int(((g.clase_L!="vueltas_reales")&(g.color_limpio==modal)).sum())
    d=int(((g.clase_L!="vueltas_reales")&(g.color_limpio!=modal)).sum())
    if c+d==0: continue
    orr,p=fisher_exact([[a,b],[c,d]])
    rows.append(dict(kfg=k,color_modal=modal,gen_modal=f"{a}/{len(gen)}",resto_modal=f"{c}/{c+d}",OR=orr,p=p))
col=pd.DataFrame(rows)
print("COLOR (color modal del quipu):")
print(col.round(4).to_string(index=False))
if len(col)>1: print("combinado Fisher:",combine_pvalues(col.p,method="fisher"))

# cabeza de grupo, solo grupos >=2
g2=sub.groupby(["kfg","grupo"]).filter(lambda x: (x.nivel==0).sum()>=2)
rows=[]
for k,g in g2.groupby("kfg"):
    gen=g[(g.clase_L=="vueltas_reales")&(g.nivel==0)]; rest=g[(g.clase_L!="vueltas_reales")&(g.nivel==0)]
    if len(gen)==0 or len(rest)==0: continue
    a=int(gen.es_cabeza.sum()); b=len(gen)-a; c=int(rest.es_cabeza.sum()); d=len(rest)-c
    orr,p=fisher_exact([[a,b],[c,d]])
    rows.append(dict(kfg=k,gen=f"{a}/{len(gen)}",resto=f"{c}/{len(rest)}",OR=orr,p=p))
cab=pd.DataFrame(rows)
print("\nCABEZA DE GRUPO (grupos >=2):")
print(cab.round(4).to_string(index=False))
if len(cab)>1: print("combinado Fisher:",combine_pvalues(cab.p,method="fisher"))

# posicion relativa: L genuinos vs L normales por quipu
rows=[]
for k,g in sub.groupby("kfg"):
    gen=[x["pos"]/r.largo_num for _,r in g[g.clase_L=="vueltas_reales"].iterrows()
         for x in r.knots if x["tipo"]=="L" and x["n"]>=10 and r.largo_num]
    nor=[x["pos"]/r.largo_num for _,r in g.iterrows()
         for x in r.knots if x["tipo"]=="L" and 2<=x["n"]<10 and r.largo_num]
    if len(gen)>=3 and len(nor)>=3:
        u,p=mannwhitneyu(gen,nor,alternative="two-sided")
        rows.append(dict(kfg=k,n_gen=len(gen),n_nor=len(nor),med_gen=np.median(gen),med_nor=np.median(nor),p=p))
pos=pd.DataFrame(rows)
print("\nPOSICION RELATIVA (L>=10 vs L 2-9, mismo quipu):")
print(pos.round(4).to_string(index=False))
if len(pos)>1:
    print("Wilcoxon pareado mediana gen vs nor:",wilcoxon(pos.med_gen,pos.med_nor))
    print("combinado Fisher:",combine_pvalues(pos.p,method="fisher"))

# rango del racimo (0=arriba) para L>=10
def ranks(r,cond):
    ks=r.knots
    return [i for i,x in enumerate(ks) if cond(x)]
gen_ranks=[]; nor_ranks=[]
for _,r in sub.iterrows():
    K=len(r.knots)
    for i,x in enumerate(r.knots):
        if x["tipo"]=="L" and x["n"]>=10: gen_ranks.append(i/max(K-1,1))
        elif x["tipo"]=="L" and 2<=x["n"]<10: nor_ranks.append(i/max(K-1,1))
print("\nRANGO relativo del racimo: genuinos n=%d med=%.2f IQR=%.2f-%.2f | normales n=%d med=%.2f IQR=%.2f-%.2f"%(
 len(gen_ranks),np.median(gen_ranks),np.percentile(gen_ranks,25),np.percentile(gen_ranks,75),
 len(nor_ranks),np.median(nor_ranks),np.percentile(nor_ranks,25),np.percentile(nor_ranks,75)))
print("MWU rango:",mannwhitneyu(gen_ranks,nor_ranks,alternative="two-sided"))

# coocurrencia
print("\nCOOCURRENCIA en cuerdas genuinas (por quipu):")
for k,g in sub.groupby("kfg"):
    gen=g[g.clase_L=="vueltas_reales"]
    if len(gen)<3: continue
    print(k,"n=%d S=%.2f Lnorm=%.2f nrac_med=%.0f"%(
      len(gen),gen.knots.map(lambda ks:any(x['tipo']=='S' for x in ks)).mean(),
      gen.knots.map(lambda ks:any(x['tipo']=='L' and x['n']<10 for x in ks)).mean(),
      gen.n_rac.median()))
col.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\control_color.csv",index=False)
cab.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\control_cabeza.csv",index=False)
pos.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\control_posicion.csv",index=False)
