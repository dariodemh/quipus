"""Chequeos de la ficha de Thompson (2026) y de la cobertura de identificadores.

1) AS030/AS031/AS032/AS033A-G no están en el KFG preparado (651 khipus).
2) En el OKR sí están como KH0032-KH0041.
3) La lectura citada de AS033A p1 = 1S(,10) + 2L(,2) = 12 no coincide con los
   nudos del OKR para KH0035 cord 1 (dos nudos S, ambos valor 10).
4) Cobertura del puente KFG<->OKR: cuántos OKR no tienen fila en quipus.csv.
"""
import json
import os

import pandas as pd

from comun import cargar_cuerdas, cargar_quipus, okr_conectar, SALIDA

R = {}
c = cargar_cuerdas()
ids = sorted(c.kfg.unique())
buscados = ["AS030", "AS031", "AS032"] + [f"AS033{x}" for x in "ABCDEFG"]
print("En KFG preparado:", {b: (b in ids) for b in buscados})
print("Total khipus en cuerdas.csv:", len(ids))

con = okr_conectar()
kh = [f"KH00{i}" for i in range(32, 42)]
d = pd.read_sql(f"select OKR_NUM, KHIPU_ID, INVESTIGATOR_NUM, PROVENANCE from khipu_main "
                f"where OKR_NUM in ({','.join('?'*len(kh))})", con, params=kh)
print("\nEn OKR:")
print(d.to_string(index=False))

print("\nKH0035 (AS033A) cord 1, nudos:")
q = """select c.CORD_ORDINAL ord, k.TYPE_CODE, k.NUM_TURNS, k.DIRECTION,
              k.CLUSTER_ORDINAL, k.knot_value_type
       from cord c join knot k on k.CORD_ID = c.CORD_ID
       where c.KHIPU_ID = 1000105 and c.CORD_ORDINAL = 1
       order by k.CLUSTER_ORDINAL, k.KNOT_ORDINAL"""
t = pd.read_sql(q, con)
print(t.to_string(index=False))
print("Thompson cita p1 = 1S(5,0,Z),10 + 2L(14,0,Z),2 = 12")

q_df = cargar_quipus()
okr = set(pd.read_sql("select OKR_NUM from khipu_main", con).OKR_NUM)
mapa = set(q_df.okr.dropna().astype(str))
print(f"\nOKR en khipu.db={len(okr)}; OKR_NUM presentes en quipus.csv={len(okr & mapa)}; "
      f"sin fila de metadatos={len(okr - mapa)}")

R = dict(ausentes_kfg=[b for b in buscados if b not in ids],
         okr_presentes=d.OKR_NUM.tolist(),
         thompson_p1=t.to_dict(orient="records"),
         okr_sin_metadata=sorted(okr - mapa))
with open(os.path.join(SALIDA, "res_08_thompson.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_08_thompson.json")
