# -*- coding: utf-8 -*-
"""Paso 13: reclasificar las cuerdas con 'posicion imposible' usando OKR.
Una E/L en decenas o centenas es una variante posicional, no un imposible.
Imposible real: >=2 unidades en el mismo lugar que suman >9, o L con >=10 vueltas.
"""
import pandas as pd, numpy as np
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
m = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\match_okr.pkl").drop_duplicates(["kfg","cuerda"])
mm=m.set_index(["kfg","cuerda"])

def cat(r):
    if (r.kfg,r.cuerda) not in mm.index: return "sin_OKR"
    x=mm.loc[(r.kfg,r.cuerda)]
    if not isinstance(x.okr_kvt,list) or len(x.okr_kvt)!=len(r.knots): return "sin_OKR"
    units=[]; higher=0; l10=False; unknown=False
    for i,(k,kvt,tr,tp) in enumerate(zip(r.knots,x.okr_kvt,x.okr_turns,x.okr_tipos)):
        if tp not in ("L","E"): continue
        d = tr if tp=="L" else (x.okr_nk[i] if tp=="E" and isinstance(x.okr_nk,list) and i<len(x.okr_nk) else k["n"])
        if tp=="L" and tr is not None and tr>=10: l10=True
        if d is None or d==0 or kvt is None: unknown=True; continue
        pl=kvt/d
        if abs(pl-1)<1e-9: units.append(d)
        elif pl>1.5: higher+=1
        else: unknown=True
    if l10: return "L10_real"
    if len(units)>=2 and sum(units)>9: return "multiunidad_real"
    if higher>0 and sum(units)<=9: return "unidad_en_decenas"
    if len(units)>=2 and sum(units)<=9: return "unidad_multiple_ok"
    if unknown: return "ambiguo"
    return "otro"

df["cat_pos"]=df.apply(lambda r: cat(r) if r.pos_imp else "",axis=1)
print("Categoria de las cuerdas con pos_imp:",df[df.pos_imp].cat_pos.value_counts().to_dict())
print("\nCategoria de TODAS las marcadas (imposible):",df[df.imposible].cat_pos.value_counts().to_dict())

# por quipu
g=df[df.imposible].groupby("kfg").agg(n_imp=("imposible","sum"),
    n_real=("clase_L",lambda s:(s=="vueltas_reales").sum()),
    n_multi=("cat_pos",lambda s:(s=="multiunidad_real").sum()),
    n_dec=("cat_pos",lambda s:(s=="unidad_en_decenas").sum()),
    n_multok=("cat_pos",lambda s:(s=="unidad_multiple_ok").sum()),
    n_sinokr=("cat_pos",lambda s:(s=="sin_OKR").sum()))
print("\nQuipus con multiunidad_real:",(g.n_multi>0).sum(),"cuerdas:",int(g.n_multi.sum()))
print(g.sort_values("n_multi",ascending=False).head(15).to_string())
df.to_pickle(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_valores2.pkl")
g.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\posimp_por_quipu.csv")
