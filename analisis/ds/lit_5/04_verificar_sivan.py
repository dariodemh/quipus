"""Verificación de dos afirmaciones cuantitativas de Sivan (2026).

1) STRING = cuerdas incompatibles con lectura decimal (>1 nudo L/LL o >1 E/EE):
   1.992/37.206 = 5,35%.
2) knot_value_type = NUM_TURNS × PLACE_VALUE en 586/588 nudos L de cuerdas
   STRING (99,8%). El OKR no tiene columna PLACE_VALUE: se comprueba si
   knot_value_type coincide con NUM_TURNS (dígito de vueltas).
"""
import json
import os

import numpy as np
import pandas as pd

from comun import okr_conectar, SALIDA

R = {}
con = okr_conectar()
k = pd.read_sql("select CORD_ID, TYPE_CODE, NUM_TURNS, knot_value_type, CLUSTER_ID "
                "from knot", con)
k["esL"] = k.TYPE_CODE.isin(["L", "LL"])
k["esE"] = k.TYPE_CODE.isin(["E", "EE"])
g = k.groupby("CORD_ID").agg(nL=("esL", "sum"), nE=("esE", "sum"),
                             nudos=("TYPE_CODE", "size"))
g["string"] = (g.nL > 1) | (g.nE > 1)
n_str = int(g.string.sum())
print(f"cuerdas con nudos={len(g)}; STRING (>1 L o >1 E)={n_str} "
      f"({100*n_str/len(g):.2f}%)  [Sivan: 1.992/37.206 = 5,35%]")
print(f"  desglose: >1 L={int((g.nL>1).sum())}; >1 E={int((g.nE>1).sum())}; "
      f"ambos={int(((g.nL>1)&(g.nE>1)).sum())}")
R["string"] = dict(cuerdas_con_nudos=int(len(g)), string=n_str,
                   pct=round(100*n_str/len(g), 2),
                   multiL=int((g.nL > 1).sum()), multiE=int((g.nE > 1).sum()))

print("\n--- knot_value_type vs NUM_TURNS en nudos L ---")
L = k[k.esL].copy()
Lt = L.dropna(subset=["NUM_TURNS"])
match = (Lt.knot_value_type == Lt.NUM_TURNS)
print(f"nudos L={len(L)}; con NUM_TURNS={len(Lt)}; "
      f"knot_value_type==NUM_TURNS={int(match.sum())} ({100*match.mean():.2f}%)")
print("valores de knot_value_type en L:", L.knot_value_type.value_counts().head(6).to_dict())
print("PLACE_VALUE existe en el esquema:", "PLACE_VALUE" in
      [r[1] for r in con.execute("pragma table_info(knot)")])
# cuerdas STRING: el subconjunto exacto que cita Sivan
Ls = L[L.CORD_ID.isin(g[g.string].index)].dropna(subset=["NUM_TURNS"])
ms = (Ls.knot_value_type == Ls.NUM_TURNS)
print(f"nudos L en cuerdas STRING={len(Ls)}; coinciden={int(ms.sum())} "
      f"({100*ms.mean():.2f}%)  [Sivan: 586/588 = 99,8%]")
R["L_value_type"] = dict(n=int(len(Lt)), match=int(match.sum()),
                         pct=round(100*float(match.mean()), 2),
                         n_string=int(len(Ls)), match_string=int(ms.sum()),
                         pct_string=round(100*float(ms.mean()), 2))

# control aburrido: ¿la coincidencia es trivial?
print("\nControl: si knot_value_type fuese solo el dígito de las vueltas, la "
      "coincidencia sería ~100% por construcción; no hay información de lugar "
      "(posición) en el campo.")
print("Distribución de NUM_TURNS en L:", L.NUM_TURNS.value_counts().sort_index().head(10).to_dict())

with open(os.path.join(SALIDA, "res_04_sivan.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_04_sivan.json")
