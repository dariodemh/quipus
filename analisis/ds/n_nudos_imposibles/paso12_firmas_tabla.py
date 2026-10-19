# -*- coding: utf-8 -*-
"""Paso 12: firmas de racimos en cuerdas genuinas + tabla final por quipu.
"""
import pandas as pd, numpy as np, sqlite3, re
from collections import Counter
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
df["largo_num"]=pd.to_numeric(df.largo,errors="coerce")

def sig(ks):
    out=[]
    for x in ks:
        t=x["tipo"]
        if t=="L" and x["n"]>=10: out.append("X")
        elif t=="L": out.append("l")
        elif t=="S": out.append("s")
        elif t=="E": out.append("e")
        else: out.append(t.lower())
    return "-".join(out)
df["firma"]=df.knots.map(sig)

print("FIRMAS en cuerdas con vueltas reales (top por quipu):")
for k in ["UR1095","UR193","KH0001","UR055","UR1087","UR203","AS014"]:
    g=df[(df.kfg==k)&(df.clase_L=="vueltas_reales")]
    print("---",k,"n=",len(g))
    print(g.firma.value_counts().head(6).to_dict())
    # rango del primer X
    rr=[]
    for ks in g.knots:
        for i,x in enumerate(ks):
            if x["tipo"]=="L" and x["n"]>=10: rr.append((i,len(ks)-1)); break
    print("rango del 1er nudo X (0=arriba):",Counter(rr).most_common(6))

# tabla final por quipu
q=pd.read_csv(BASE+r"\analisis\datos\quipus.csv",dtype=str,keep_default_na=False)
g=df.groupby("kfg").agg(n_cuerdas=("cuerda","size"),
                        n_imp=("imposible","sum"),
                        n_L10=("L10","sum"),
                        n_real=("clase_L",lambda s:(s=="vueltas_reales").sum()),
                        n_pv=("clase_L",lambda s:(s=="valor_posicional").sum()),
                        n_amb=("clase_L",lambda s:(s=="ambiguo").sum()),
                        n_posimp=("pos_imp","sum"))
g["frac_imp"]=g.n_imp/g.n_cuerdas
g["frac_real"]=g.n_real/g.n_cuerdas
g=g[g.n_imp>0].reset_index()
g=g.merge(q[["kfg","okr","museo","procedencia","region"]],on="kfg",how="left")

con=sqlite3.connect("file:"+BASE.replace("\\","/")+"/data/external/open-khipu-repository/data/khipu.db?mode=ro",uri=True)
okr_map={r[0]:r[1] for r in con.execute("select OKR_NUM,KHIPU_ID from khipu_main")}
nota={r[0]:r[1] for r in con.execute("select OKR_NUM,NOTES from khipu_main")}
can={r[0]:r[1] for r in con.execute("select KHIPU_ID,count(*) from canuto group by KHIPU_ID")}
fib={}
for kid,f,n in con.execute("select KHIPU_ID,FIBER,count(*) from cord where FIBER!='' group by KHIPU_ID,FIBER"):
    fib.setdefault(kid,[]).append((f,n))
def get(k,mp): return mp.get(k,np.nan) if isinstance(k,str) else np.nan
g["canutos"]=g.okr.map(lambda x: can.get(okr_map.get(x),np.nan) if x else np.nan)
def fibmode(x):
    kid=okr_map.get(x) if x else None
    if not kid or kid not in fib: return ""
    return max(fib[kid],key=lambda z:z[1])[0]
g["fibra"]=g.okr.map(fibmode)
g["nota"]=g.okr.map(lambda x: (nota.get(x,"") or "").replace("\n"," ")[:180])

def verdict(r):
    if r.n_real>=3: return "otra_notacion_no_numerica" if r.nota else "candidato_no_numerico"
    if r.n_real>=1: return "caso_aislado"
    if r.n_pv>0: return "decimal_valor_posicional"
    if r.n_posimp>0: return "variante_posicional"
    return "sin_clasificar"
g["veredicto"]=g.apply(verdict,axis=1)
g=g.sort_values(["n_real","n_imp"],ascending=False)
g.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\nudos_imposibles.csv",index=False)
print("\nVEREDICTOS:",g.veredicto.value_counts().to_dict())
print("\nTOP 20:")
print(g[["kfg","okr","n_cuerdas","n_imp","frac_imp","n_L10","n_real","n_pv","n_amb","n_posimp","canutos","fibra","veredicto"]].head(20).to_string(index=False))
print("\nProcedencia/museo de los 8 primeros:")
print(g[["kfg","museo","procedencia","region"]].head(8).to_string(index=False))
