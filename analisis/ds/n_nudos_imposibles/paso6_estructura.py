# -*- coding: utf-8 -*-
"""Paso 6: estructura de los quipus con vueltas reales >=10.
Descriptivo: nivel, color, cabeza de grupo, coexistencia con decimales normales,
posiciones, direccion. Guarda tabla por quipu.
"""
import pandas as pd, numpy as np
from collections import Counter
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_clasificadas.pkl")
gr = pd.read_csv(BASE + r"\analisis\datos\grupos.csv", dtype=str, keep_default_na=False)

# cabeza de grupo: primer colgante (nivel 0) de cada (kfg,grupo) por orden
lvl0 = df[df.nivel==0].copy()
head = lvl0.sort_values("orden").groupby(["kfg","grupo"]).first().reset_index()[["kfg","grupo","cuerda"]]
head["es_cabeza"]=True
df = df.merge(head, on=["kfg","grupo","cuerda"], how="left")
df["es_cabeza"]=df.es_cabeza.fillna(False).astype(bool)

def norm_color(s):
    return str(s).split(":")[0].split("-")[0].split("/")[0]

df["largo_num"]=pd.to_numeric(df.largo,errors="coerce")
def stats(k):
    sub=df[df.kfg==k]; gen=sub[sub.clase_L=="vueltas_reales"]; pv=sub[sub.clase_L=="valor_posicional"]
    n0=sub[sub.nivel==0]
    des=dict(kfg=k, n=len(sub), n_gen=len(gen), n_pv=len(pv),
             frac_gen=len(gen)/len(sub),
             niveles_gen=gen.nivel.value_counts().sort_index().to_dict(),
             colores_gen=gen.color_limpio.value_counts().head(6).to_dict(),
             colores_resto=sub[sub.clase_L!="vueltas_reales"].color_limpio.value_counts().head(6).to_dict(),
             cabeza_gen=round(gen.es_cabeza.mean(),3) if len(gen) else np.nan,
             cabeza_base=round(n0.es_cabeza.mean(),3),
             gen_con_S=round(gen.knots.map(lambda ks:any(x['tipo']=='S' for x in ks)).mean(),3) if len(gen) else np.nan,
             gen_con_Lnormal=round(gen.knots.map(lambda ks:any(x['tipo']=='L' and x['n']<10 for x in ks)).mean(),3) if len(gen) else np.nan,
             gen_nrac=gen.n_rac.value_counts().sort_index().to_dict(),
             dirs=Counter(x['dir'] for ks in gen.knots for x in ks if x['tipo']=='L').most_common(4),
             pos_med=round(gen.knots.map(lambda ks:np.median([x['pos'] for x in ks if x['tipo']=='L' and x['n']>=10])).median(),2) if len(gen) else np.nan,
             relpos_med=round(gen.apply(lambda r: np.median([x['pos']/r.largo_num if r.largo_num else np.nan for x in r.knots if x['tipo']=='L' and x['n']>=10]),axis=1).median(),2) if len(gen) else np.nan,
             n_padres=int(sub.padre.notna().sum()), n_grupos=int(sub.grupo.nunique()))
    return des

rows=[]
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS014","AS090_N2"]:
    rows.append(stats(k))
s=pd.DataFrame(rows)
pd.set_option("display.width",250)
print(s.to_string(index=False))
s.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\estructura_quipus.csv",index=False)

# ejemplos breves por quipu
print("\nEJEMPLOS (3 por quipu):")
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS090_N2"]:
    sub=df[(df.kfg==k)&(df.clase_L=="vueltas_reales")].head(3)
    print("---",k)
    print(sub[["cuerda","nivel","grupo","es_cabeza","color_limpio","largo","valor","nudos"]].to_string(index=False))
