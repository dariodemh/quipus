# -*- coding: utf-8 -*-
"""Paso 11: auditoria KFG vs OKR de las 362 cuerdas con nL>=10 y notas del transcriptor.
"""
import pandas as pd, numpy as np, sqlite3, textwrap
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
m = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\match_okr.pkl").drop_duplicates(["kfg","cuerda"])
mm=m.set_index(["kfg","cuerda"])
con=sqlite3.connect("file:"+BASE.replace("\\","/")+"/data/external/open-khipu-repository/data/khipu.db?mode=ro",uri=True)

# acuerdo por racimo L
tot=0; eq_kvt=0; eq_turns=0; both=0
for _,r in df[df.L10].iterrows():
    if (r.kfg,r.cuerda) not in mm.index: continue
    x=mm.loc[(r.kfg,r.cuerda)]
    if not isinstance(x.okr_kvt,list) or len(x.okr_kvt)!=len(r.knots): continue
    for k,kvt,tr,tp in zip(r.knots,x.okr_kvt,x.okr_turns,x.okr_tipos):
        if tp!="L": continue
        tot+=1
        if kvt is not None and k["n"]==kvt: eq_kvt+=1
        if tr is not None and k["n"]==tr: eq_turns+=1
        if kvt is not None and tr is not None and k["n"]==kvt and k["n"]==tr: both+=1
print(f"racimos L en cuerdas L10 emparejadas: {tot}")
print(f"KFG n == OKR knot_value_type: {eq_kvt}/{tot} = {eq_kvt/tot:.3f}")
print(f"KFG n == OKR NUM_TURNS:       {eq_turns}/{tot} = {eq_turns/tot:.3f}")

# discrepancias KFG n ni kvt ni turns
bad=[]
for _,r in df[df.L10].iterrows():
    if (r.kfg,r.cuerda) not in mm.index: continue
    x=mm.loc[(r.kfg,r.cuerda)]
    if not isinstance(x.okr_kvt,list) or len(x.okr_kvt)!=len(r.knots): continue
    for k,kvt,tr,tp in zip(r.knots,x.okr_kvt,x.okr_turns,x.okr_tipos):
        if tp=="L" and kvt is not None and tr is not None and k["n"] not in (kvt,tr):
            bad.append((r.kfg,r.cuerda,k["n"],tr,kvt))
print("discrepancias KFG n distinto de kvt y turns:",len(bad),bad[:5])

# no emparejadas
un=df[df.L10 & ~df.set_index(["kfg","cuerda"]).index.isin(mm.index)]
print("\nL10 sin match OKR:",len(un),"quipus:",un.kfg.value_counts().to_dict())

# notas por quipu genuino
print("\nNOTAS DE TRANSCRIPTOR (quipus con vueltas reales):")
gen=sorted(df[df.clase_L=="vueltas_reales"].kfg.unique())
for k in gen:
    row=con.execute("select m.NOTES from khipu_main m join (select OKR_NUM from khipu_main) x on 1=1 where m.INVESTIGATOR_NUM like ? limit 1",(k+"%",)).fetchone()
    if not row:
        # por OKR
        okr=df[df.kfg==k].okr.dropna().iloc[0] if df[df.kfg==k].okr.notna().any() else None
        row=con.execute("select NOTES from khipu_main where OKR_NUM=?",(okr,)).fetchone()
    note=row[0] if row and row[0] else ""
    print("---",k,"|",textwrap.shorten(note,220))

# notas de cuerdas en esos quipus
print("\nNOTAS DE CUERDA (no vacias) en quipus genuinos:")
for k in gen:
    okr=df[df.kfg==k].okr.dropna()
    if not len(okr): continue
    rows=con.execute("select d.CORD_ORDINAL,d.CORD_NOTES from cord d join khipu_main m on d.KHIPU_ID=m.KHIPU_ID where m.OKR_NUM=? and d.CORD_NOTES!='' limit 6",(okr.iloc[0],)).fetchall()
    if rows: print(k,rows)
