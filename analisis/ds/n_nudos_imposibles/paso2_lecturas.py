# -*- coding: utf-8 -*-
"""Paso 2: comparar la lectura ordinal decimal con el valor KFG.
Objetivo: entender que convencion usa KFG cuando hay nudos imposibles.
"""
import pandas as pd, numpy as np
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_imposibles.pkl")

def ordinal(ks):
    """lectura decimal ordinal: cada racimo n * 10^(racimos debajo)."""
    return sum(k["n"] * 10**(len(ks)-1-i) for i,k in enumerate(ks))
def unario(ks):
    return sum(k["n"] for k in ks)

df["v_ord"] = df.knots.map(ordinal)
df["v_una"] = df.knots.map(unario)
df["v_kfg"] = df.valor
ok = df[df.n_rac > 0]
print("cuerdas con >=1 racimo:", len(ok))
for lab, sub in [("normales", ok[~ok.imposible]), ("imposibles", ok[ok.imposible])]:
    print(lab, len(sub),
          "| KFG==ordinal:", round((sub.v_kfg==sub.v_ord).mean(),3),
          "| KFG==unario:", round((sub.v_kfg==sub.v_una).mean(),3),
          "| ordinal==unario:", round((sub.v_ord==sub.v_una).mean(),3))
from collections import Counter
print("\nEn imposibles: patron de coincidencia")
c = Counter(zip(ok[ok.imposible].v_kfg==ok[ok.imposible].v_ord, ok[ok.imposible].v_kfg==ok[ok.imposible].v_una))
print(c)
print("\nEjemplos imposibles donde KFG!=ordinal y KFG==unario:")
print(ok[ok.imposible & (ok.v_kfg!=ok.v_ord) & (ok.v_kfg==ok.v_una)][["kfg","cuerda","valor","v_ord","v_una","nudos"]].head(10).to_string())
print("\nEjemplos imposibles donde KFG!=ambos:")
print(ok[ok.imposible & (ok.v_kfg!=ok.v_ord) & (ok.v_kfg!=ok.v_una)][["kfg","cuerda","valor","v_ord","v_una","nudos"]].head(10).to_string())
df.to_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_lecturas.pkl")
