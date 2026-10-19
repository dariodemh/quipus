"""Verificación de la réplica de Santa Valley de Khipu-ML (Contreras 2026).

Afirmación: en KH0323-KH0328, 5 de 6 khipus son R o V puros; KH0326 es el
único mixto (40 R / 69 V); el agregado es 49%/51%; y los conteos por khipu
son KH0323 310/0, KH0324 0/54, KH0325 0/207, KH0327 0/93, KH0328 56/0.

Se cuenta ATTACHMENT_TYPE por KHIPU_ID en la tabla cord del OKR (todos los
niveles, como hace el notebook). No se necesita nulo: es una afirmación
descriptiva y la comprobación es una replicación exacta de conteos.
"""
import json
import os

import pandas as pd

from comun import okr_conectar, SALIDA

IDS = ["KH0323", "KH0324", "KH0325", "KH0326", "KH0327", "KH0328"]
con = okr_conectar()
d = pd.read_sql(f"""
    select k.OKR_NUM, c.ATTACHMENT_TYPE, count(*) n
    from cord c join khipu_main k on k.KHIPU_ID = c.KHIPU_ID
    where k.OKR_NUM in ({','.join("?"*len(IDS))})
    group by 1,2
""", con, params=IDS)
piv = d.pivot_table(index="OKR_NUM", columns="ATTACHMENT_TYPE",
                    values="n", aggfunc="sum", fill_value=0)
for col in ["R", "V", "U"]:
    if col not in piv:
        piv[col] = 0
piv = piv[["R", "V", "U"]].astype(int).reindex(IDS)

esperado = {"KH0323": (310, 0), "KH0324": (0, 54), "KH0325": (0, 207),
            "KH0326": (40, 69), "KH0327": (0, 93), "KH0328": (56, 0)}
print(piv.to_string())
ok = 0
for k in IDS:
    r, v = int(piv.loc[k, "R"]), int(piv.loc[k, "V"])
    match = (r, v) == esperado[k]
    ok += match
    print(f"{k}: R={r:3d} V={v:3d}  esperado={esperado[k]}  {'OK' if match else 'DIF'}")
tot_r, tot_v = int(piv.R.sum()), int(piv.V.sum())
print(f"\nagregado R={tot_r} V={tot_v} -> R%={100*tot_r/(tot_r+tot_v):.2f} "
      f"(Khipu-ML: 49/51)")
mixtos = [k for k in IDS if piv.loc[k, "R"] > 0 and piv.loc[k, "V"] > 0]
print(f"khipus con R>0 y V>0: {mixtos} (Khipu-ML: solo KH0326)")
print(f"coincidencias exactas de conteo: {ok}/6")

R = dict(conteos=piv.reset_index().to_dict(orient="records"),
         agregado=dict(R=tot_r, V=tot_v, pct_R=round(100*tot_r/(tot_r+tot_v), 2)),
         mixtos=mixtos, coincidencias=ok)
with open(os.path.join(SALIDA, "res_05_santa.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_05_santa.json")
