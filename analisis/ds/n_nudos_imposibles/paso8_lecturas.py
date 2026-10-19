# -*- coding: utf-8 -*-
"""Paso 8: lecturas alternativas por cuerda a partir de OKR y prueba de sumas internas.
Lecturas:
 H  = suma de knot_value_type (lectura del transcriptor, lugar asignado)
 D  = decimal ordinal: digito fisico (vueltas en L, nº nudos en S/E) x 10^(racimos debajo)
 U  = unario: suma de digitos fisicos, posicion ignorada
 M  = mod 10: digito = vueltas mod 10, lugar ordinal
 LU = H pero los L de >=10 vueltas se leen como n unidades (lugar 1)
 Bb = base b ordinal (b=5,8,12,16,20)
"""
import pandas as pd, numpy as np
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_clasificadas.pkl")
m = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\match_okr.pkl").drop_duplicates(["kfg","cuerda"])
df = df.merge(m[["kfg","cuerda","okr_tipos","okr_turns","okr_kvt","okr_nk"]], on=["kfg","cuerda"], how="left")

def digits_places(r):
    ks=r.knots; tipos=r.okr_tipos; turns=r.okr_turns; kvt=r.okr_kvt; nk=r.okr_nk
    if not isinstance(tipos,list) or len(tipos)!=len(ks): return None
    digs=[]; kv=[]
    for i,k in enumerate(ks):
        t=tipos[i] if i<len(tipos) else k["tipo"]
        tr=turns[i] if i<len(turns) else None
        v=kvt[i] if i<len(kvt) else None
        if t=="L":
            d=tr if tr is not None else k["n"]
        elif t=="E" and isinstance(nk,list) and i<len(nk):
            d=nk[i]
        else:
            d=k["n"]
        digs.append(d); kv.append(v if v is not None else np.nan)
    return digs, kv

vals={}
for name in ["H","D","U","M","LU"]+[f"B{b}" for b in [5,8,12,16,20]]:
    vals[name]=[]
for _,r in df.iterrows():
    dp=digits_places(r)
    if dp is None or len(dp[0])==0:
        for name in vals: vals[name].append(np.nan)
        continue
    digs,kv=dp; K=len(digs)
    H=np.nansum(kv) if not all(np.isnan(kv)) else np.nan
    D=sum(d*10**(K-1-i) for i,d in enumerate(digs))
    U=sum(digs)
    M=sum((d%10)*10**(K-1-i) for i,d in enumerate(digs))
    LU=0
    ok=True
    for i,(d,v) in enumerate(zip(digs,kv)):
        if r.okr_tipos[i]=="L" and d>=10:
            LU+=d
        elif not np.isnan(v):
            LU+=v
        else: ok=False
    vals["H"].append(H); vals["D"].append(D); vals["U"].append(U); vals["M"].append(M)
    vals["LU"].append(LU if ok else np.nan)
    for b in [5,8,12,16,20]:
        vals[f"B{b}"].append(sum(d*b**(K-1-i) for i,d in enumerate(digs)))
for k,v in vals.items(): df[k]=v

gen_q = df[df.clase_L=="vueltas_reales"].kfg.unique().tolist()
print("quipus con vueltas reales:",len(gen_q),gen_q)
sub=df[df.kfg.isin(gen_q)]
print("cuerdas en esos quipus:",len(sub),"con valores H:",sub.H.notna().sum())
print("H vs valor KFG (cuerdas con match):",np.isclose(sub.H,sub.valor).mean().round(3))
print("\nEjemplos:")
print(sub[sub.clase_L=="vueltas_reales"][["kfg","cuerda","valor","H","D","U","M","LU"]].head(12).to_string())
df.to_pickle(BASE+r"\analisis\ds\n_nudos_imposibles\cuerdas_valores.pkl")
