"""Descripcion del conjunto HP001-HP032 (Pachacamac, Museo de Sitio).
Imprime solo resumenes cortos. No lee archivos grandes completos.
"""
import pandas as pd
import numpy as np

RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
g = pd.read_csv(RAIZ + "analisis/datos/grupos.csv")

HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()
hpq = q[q.kfg.isin(HP)].copy()
hpg = g[g.kfg.isin(HP)].copy()

print("N quipus con cuerdas:", hp.kfg.nunique())
print("Total cuerdas:", len(hp))

# Resumen por quipu
rows = []
for k in HP:
    d = hp[hp.kfg == k]
    if len(d) == 0:
        rows.append(dict(kfg=k, n=0))
        continue
    vals = d[d.nudos.notna() & (d.nudos != "") & (d.nudos != "[]")]["valor"]
    vals = pd.to_numeric(vals, errors="coerce").dropna()
    nudos_sin = (d.nudos.isna() | (d.nudos == "") | (d.nudos == "[]")).sum()
    rows.append(dict(
        kfg=k,
        n_cuerdas=len(d),
        n_grupos=d.grupo.nunique(),
        n_sub=int((d.nivel > 0).sum()),
        max_nivel=int(d.nivel.max()),
        n_con_nudos=int(d.nudos.notna().sum() - nudos_sin) if False else int(((d.nudos.notna()) & (d.nudos != "") & (d.nudos != "[]")).sum()),
        n_sin_nudos=int(nudos_sin),
        val_min=vals.min() if len(vals) else np.nan,
        val_max=vals.max() if len(vals) else np.nan,
        val_sum=vals.sum() if len(vals) else np.nan,
        n_union_T=int((d.union == "T").sum()),
        n_union_R=int((d.union == "R").sum()),
        n_union_V=int((d.union == "V").sum()),
        n_torsion_S=int((d.torsion == "S").sum()),
        n_torsion_Z=int((d.torsion == "Z").sum()),
    ))
tab = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print(tab.to_string(index=False))
tab.to_csv("tabla_por_quipu.csv", index=False)
