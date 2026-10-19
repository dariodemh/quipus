# -*- coding: utf-8 -*-
"""Paso 17: controles de color y cabeza de grupo por permutacion dentro de quipu.
Evita pseudorreplicacion (unidad = quipu).
"""
import pandas as pd, numpy as np
from statsmodels.stats.multitest import multipletests
from scipy.stats import combine_pvalues
BASE = r"."
rng=np.random.default_rng(20261018)
df=pd.read_pickle(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_valores2.pkl")
gen_q=sorted(df[df.clase_L=="vueltas_reales"].kfg.unique())
sub=df[df.kfg.isin(gen_q)].copy()
lvl0=sub[sub.nivel==0]
head=lvl0.sort_values("orden").groupby(["kfg","grupo"]).first().reset_index()[["kfg","grupo","cuerda"]]
head["es_cabeza"]=True
sub=sub.merge(head,on=["kfg","grupo","cuerda"],how="left")
sub["es_cabeza"]=sub.es_cabeza.fillna(False).astype(bool)

rows=[]
for k,g in sub.groupby("kfg"):
    gen=g.clase_L=="vueltas_reales"
    if gen.sum()<3: continue
    modal=g.color_limpio.value_counts().index[0]
    obs=int((g.color_limpio[gen]==modal).sum())
    null=np.array([int((rng.permutation(gen.values)&(g.color_limpio.values==modal)).sum()) for _ in range(10000)])
    p=(1+np.sum(null>=obs))/(1+len(null))
    rows.append(dict(kfg=k,n=int(gen.sum()),obs=obs,modal=modal,p_color=p))
col=pd.DataFrame(rows); col["p_color_holm"]=multipletests(col.p_color,method="holm")[1]
print("COLOR por permutacion:")
print(col.round(4).to_string(index=False))
print("Fisher combinado:",combine_pvalues(col.p_color,method="fisher"))

rows=[]
g2=sub.groupby(["kfg","grupo"]).filter(lambda x:(x.nivel==0).sum()>=2)
for k,g in g2.groupby("kfg"):
    gg=g[g.nivel==0]
    gen=gg.clase_L=="vueltas_reales"
    if gen.sum()==0 or (~gen).sum()==0: continue
    obs=int((gg.es_cabeza&gen).sum())
    null=np.array([int((rng.permutation(gen.values)&gg.es_cabeza.values).sum()) for _ in range(10000)])
    p=(1+np.sum(null>=obs))/(1+len(null))
    rows.append(dict(kfg=k,n=int(gen.sum()),obs=obs,p_head=p))
cab=pd.DataFrame(rows); cab["p_head_holm"]=multipletests(cab.p_head,method="holm")[1]
print("\nCABEZA DE GRUPO por permutacion:")
print(cab.round(4).to_string(index=False))
print("Fisher combinado:",combine_pvalues(cab.p_head,method="fisher"))
col.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\control_color_perm.csv",index=False)
cab.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\control_cabeza_perm.csv",index=False)
