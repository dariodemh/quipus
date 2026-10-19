# -*- coding: utf-8 -*-
"""Paso 16: tabla final por quipu (nudos_imposibles.csv) y por cuerda.
"""
import pandas as pd, numpy as np, sqlite3
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_valores2.pkl")
q = pd.read_csv(BASE + r"\analisis\datos\quipus.csv", dtype=str, keep_default_na=False)

g = df.groupby("kfg").agg(
    n_cuerdas=("cuerda","size"),
    n_imp=("imposible","sum"),
    n_L10=("L10","sum"),
    n_real=("clase_L",lambda s:(s=="vueltas_reales").sum()),
    n_pv=("clase_L",lambda s:(s=="valor_posicional").sum()),
    n_amb=("clase_L",lambda s:(s=="ambiguo").sum()),
    n_posimp=("pos_imp","sum"),
    n_multi=("cat_pos",lambda s:(s=="multiunidad_real").sum()),
    n_dec=("cat_pos",lambda s:(s=="unidad_en_decenas").sum()),
    n_multok=("cat_pos",lambda s:(s=="unidad_multiple_ok").sum()),
    n_sinokr=("cat_pos",lambda s:(s=="sin_OKR").sum())).reset_index()
g["frac_imp"]=(g.n_imp/g.n_cuerdas).round(4)
g["frac_L10_real"]=(g.n_real/g.n_cuerdas).round(4)
g = g[g.n_imp>0].merge(q[["kfg","okr","museo","procedencia","region"]],on="kfg",how="left")

con=sqlite3.connect("file:"+BASE.replace("\\","/")+"/data/external/open-khipu-repository/data/khipu.db?mode=ro",uri=True)
okr_map={r[0]:r[1] for r in con.execute("select OKR_NUM,KHIPU_ID from khipu_main")}
nota={r[0]:(r[1] or "") for r in con.execute("select OKR_NUM,NOTES from khipu_main")}
can={r[0]:r[1] for r in con.execute("select KHIPU_ID,count(*) from canuto group by KHIPU_ID")}
fib={}
for kid,f,n in con.execute("select KHIPU_ID,FIBER,count(*) from cord where FIBER!='' group by KHIPU_ID,FIBER"):
    fib.setdefault(kid,[]).append((f,n))
g["canutos"]=g.okr.map(lambda x: can.get(okr_map.get(x),0) if x else 0)
def fibmode(x):
    kid=okr_map.get(x) if x else None
    if not kid or kid not in fib: return ""
    return max(fib[kid],key=lambda z:z[1])[0]
g["fibra"]=g.okr.map(fibmode)
FIB={"CN":"algodón","CL":"camélido","W":"lana","H":"pelo","V":"vegetal","AH":"animal?"}
g["fibra_es"]=g.fibra.map(lambda x:FIB.get(x,x))
g["nota"]=g.okr.map(lambda x: nota.get(x,"").replace("\n"," ")[:300])
KW=["no numerical","no observable pattern","spiral","do not conform","does not conform","not conform","non-decimal","base ten","values","value 10"]
g["nota_relevante"]=g.nota.str.lower().map(lambda s: any(k in s for k in KW))
def verdict(r):
    if r.n_real>=3: return "otra_notacion_no_numerica" if r.nota_relevante else "candidato_no_numerico"
    if r.n_multi>=5: return "multiunidad_aditiva"
    if r.n_real>=1: return "caso_aislado"
    if r.n_pv>0 and r.n_multi<5: return "decimal_valor_posicional"
    if r.n_multok>0: return "variante_unidades_suma<=9"
    if r.n_dec>0: return "variante_posicional"
    if r.n_sinokr>0: return "ambiguo_sin_OKR"
    return "variante_menor"
g["veredicto"]=g.apply(verdict,axis=1)
g=g.sort_values(["n_real","n_multi","n_imp"],ascending=False)
g.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\nudos_imposibles.csv",index=False)
print("filas:",len(g),"| veredictos:",g.veredicto.value_counts().to_dict())
print(g[["kfg","okr","n_cuerdas","n_imp","frac_imp","n_L10","n_real","n_pv","n_multi","n_dec","canutos","fibra","veredicto"]].head(25).to_string(index=False))

# tabla por cuerda
cols=["kfg","okr","cuerda","nivel","padre","grupo","valor","nudos","color_limpio","torsion","union","largo",
      "n_rac","L10","pos_imp","imposible","clase_L","cat_pos","detalle","museo","procedencia"]
c=df[df.imposible][cols].copy()
c.to_csv(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_nudos_imposibles.csv",index=False)
print("cuerdas guardadas:",len(c))
