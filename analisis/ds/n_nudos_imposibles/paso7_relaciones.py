# -*- coding: utf-8 -*-
"""Paso 7: inventario de relaciones de suma interna disponibles.
A) madre = suma de hijas directas (padre)
B) cabeza de grupo = suma del resto del grupo
"""
import pandas as pd, numpy as np
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_clasificadas.pkl")
df["valor"]=pd.to_numeric(df.valor,errors="coerce")

# padres reales
padres = set(df.padre[df.padre!=""])
print("cuerdas:",len(df),"padres distintos:",len(padres))
pc = df[df.padre!=""].groupby(["kfg","padre"]).agg(n_hijas=("cuerda","size"), suma=("valor","sum")).reset_index()
pc = pc.merge(df[["kfg","cuerda","valor"]].rename(columns={"cuerda":"padre","valor":"v_padre"}),on=["kfg","padre"],how="left")
pc["cierra"]=np.isclose(pc.v_padre,pc.suma)
print("relaciones madre-hijas:",len(pc),"quipus:",pc.kfg.nunique())
print("cierran (todas):",pc.cierra.sum(),round(pc.cierra.mean(),4))
print("\nPor quipu candidato:")
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS014","AS090_N2"]:
    s=pc[pc.kfg==k]
    print(k,"relaciones:",len(s),"cierran:",int(s.cierra.sum()),"suma>0:",int((s.suma>0).sum()))

# grupos con >=2 level0
g0=df[df.nivel==0].copy()
head=g0.sort_values("orden").groupby(["kfg","grupo"]).first().reset_index()[["kfg","grupo","cuerda","valor"]]
head=head.rename(columns={"cuerda":"cabeza","valor":"v_head"})
agg=g0.groupby(["kfg","grupo"]).agg(n=("cuerda","size"),suma=("valor","sum")).reset_index()
gg=agg.merge(head,on=["kfg","grupo"])
gg["suma_resto"]=gg.suma-gg.v_head
gg["cierra"]=np.isclose(gg.v_head,gg.suma_resto)
gg=gg[gg.n>=2]
print("\nGrupos con >=2 colgantes:",len(gg),"quipus:",gg.kfg.nunique(),"cierran:",int(gg.cierra.sum()),round(gg.cierra.mean(),4))
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS014","AS090_N2"]:
    s=gg[gg.kfg==k]
    print(k,"grupos:",len(s),"cierran:",int(s.cierra.sum()))
pc.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\relaciones_madre_hija.csv",index=False)
gg.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\relaciones_grupo.csv",index=False)
