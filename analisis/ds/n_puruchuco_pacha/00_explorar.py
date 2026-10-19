"""00: estructura de los 20 quipus de Puruchuco (region Puruchuco) en KFG y OKR."""
import numpy as np
import pandas as pd
import comun_np as L

c, q = L.cargar_kfg()
pur = sorted(q[q.region == "Puruchuco"].kfg)
print("Puruchuco region:", len(pur), pur)
print(q[q.region == "Puruchuco"][["kfg", "okr", "procedencia", "museo"]].to_string())

okr, mapa = L.cargar_okr(pur)
print("\nOKR cord count por quipu (vs KFG):")
for k in pur:
    d = c[c.kfg == k]
    o = okr[okr.kfg == k]
    nm = int((o.CORD_CLASSIFICATION.fillna("") == "M").sum()) if len(o) else 0
    nt = int(((o.nivel_okr == 0)).sum()) if len(o) else 0
    print(f"{k}: KFG {len(d):3d} cuerdas (n0={(d.nivel==0).sum():3d}, subs={(d.nivel>0).sum():2d}) | "
          f"OKR {len(o):3d} (top={nt:3d}, M={nm}) | valores KFG={int(d.valor.sum()):6d} OKR={int(o.valor.sum()):6d}")

print("\nDetalle grupos KFG de la jerarquia:")
for k in ["UR063", "UR073", "UR064", "UR068", "UR066", "UR067"]:
    regs = L.registros_kfg(c, k)
    print(f"== {k}: {len(regs)} grupos; " + " ".join(
        f"g{r['grupo']}[n={r['n']},cab={r['x']},P={r['p']},S={r['s']}]" for r in regs))

print("\nUR073 marcadoras OKR (rule d):")
o = okr[okr.kfg == "UR073"].sort_values("CORD_ORDINAL")
print(o[["CORD_ORDINAL", "CORD_CLASSIFICATION", "valor", "nivel_okr"]].to_string())
