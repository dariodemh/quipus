"""Calibracion: estructura de grupos en Incahuasi, pares de copia conocidos y repeticion de valores."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "datos"
c = pd.read_csv(D / "cuerdas.csv", dtype={"kfg": str, "cuerda": str, "padre": str, "nudos": str})
c["nudos"] = c["nudos"].fillna("")
c["pres"] = ~((c["valor"] == 0) & (c["nudos"].str.strip() == ""))

sis = ["UR270","UR273A","UR273B","UR274A","UR274B","UR278","UR266","UR275","UR269","UR267A","UR267B","UR255","UR256"]
l0 = c[(c.nivel == 0) & c.kfg.isin(sis)]
sig = l0.groupby("kfg").apply(lambda d: tuple(d.sort_values("orden").groupby("grupo").size().tolist()), include_groups=False)
for k in sis:
    print(k, "grupos", len(sig[k]), "colgantes", sum(sig[k]), sig[k])
print()
pares = [("HP055","UR1084"),("UR1175","UR233"),("KH0049","UR122"),("UR053B","UR053C"),
         ("UR006","UR009"),("UR064","UR068"),("UR1114","UR1123"),("UR066","UR067"),
         ("UR1118","UR218"),("QU002","UR137"),("AS159","AS173"),("UR255","UR267A"),("MM016","UR212")]
for a,b in pares:
    if a in sig.index and b in sig.index:
        print(a,b,"n0",sum(sig[a]),sum(sig[b]),"grupos",len(sig[a]),len(sig[b]),"sig igual",sig[a]==sig[b])
    else:
        print(a,b,"FALTA", a in sig.index, b in sig.index)
print("\nvalores mas frecuentes en el corpus (solo nivel 0):")
print(l0[l0.pres].valor.value_counts().head(12).to_dict())
print("\nquipus con un solo valor distinto entre sus colgantes con valor:",
      (l0[l0.pres].groupby("kfg").valor.nunique()==1).sum())
print("cuerdas por quipu con valor: mediana", l0[l0.pres].groupby("kfg").size().median())
