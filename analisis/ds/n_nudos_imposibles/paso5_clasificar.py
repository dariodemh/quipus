# -*- coding: utf-8 -*-
"""Paso 5: clasificar cada cuerda L>=10 en:
 - 'valor_posicional': KFG n es valor de posicion; vueltas reales 2-9 (OKR)
 - 'vueltas_reales': vueltas OKR >=10 (anomalia genuina)
 - 'ambiguo': sin match OKR
Agrega por quipu y describe candidatos.
"""
import pandas as pd, numpy as np, re, sqlite3
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_lecturas.pkl")
m = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\match_okr.pkl")

m = m.drop_duplicates(["kfg","cuerda"])
mm = m.set_index(["kfg","cuerda"])
def clas(r):
    if not r.L10: return ""
    if (r.kfg,r.cuerda) not in mm.index: return "ambiguo"
    x=mm.loc[(r.kfg,r.cuerda)]
    turns=[t for t in x.okr_turns if t is not None]
    kvt=[t for t in x.okr_kvt if t is not None]
    if turns and max(turns)>=10: return "vueltas_reales"
    if turns and max(turns)<10 and kvt and max(kvt)>=10: return "valor_posicional"
    return "ambiguo"
df["clase_L"]=df.apply(clas,axis=1)

print("clase de las 362 cuerdas con KFG nL>=10:")
print(df[df.L10].clase_L.value_counts().to_string())

# por quipu
g=df[df.L10].groupby(["kfg","clase_L"]).size().unstack(fill_value=0)
for c in ["vueltas_reales","valor_posicional","ambiguo"]:
    if c not in g: g[c]=0
g["total"]=g.sum(axis=1)
g=g.sort_values(["vueltas_reales","total"],ascending=False)
q=pd.read_csv(BASE+r"\analisis\datos\quipus.csv",dtype=str,keep_default_na=False).set_index("kfg")
g=g.join(q[["okr","museo","procedencia","region"]])
print("\nQuipus con cuerdas L>=10 (top 25):")
print(g.head(25).to_string())
g.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\quipus_L10_clase.csv")

print("\nSolo 'vueltas_reales': quipus:", (g.vueltas_reales>0).sum(), "cuerdas:", int(g.vueltas_reales.sum()))
print("Quipus donde TODAS las L10 son valor_posicional:", ((g.vueltas_reales==0)&(g.valor_posicional>0)).sum())

# candidatos: UR193, KH0001, AS090_N2
for k in ["UR193","KH0001","AS090_N2"]:
    sub=df[df.kfg==k]
    print(f"\n=== {k}: {len(sub)} cuerdas, L10={int(sub.L10.sum())}, clases={sub[sub.L10].clase_L.value_counts().to_dict()}, "
          f"posimp={int(sub.pos_imp.sum())}, frac_imp={sub.imposible.mean():.2f}")
    print("niveles:",sub.nivel.value_counts().sort_index().to_dict(),"grupos:",sub.grupo.nunique())
df.to_pickle(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_clasificadas.pkl")
