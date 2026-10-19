# -*- coding: utf-8 -*-
"""04: sumas dentro de cada quipu y jerarquia del archivo.
- cuentas de relaciones de suma de KFG (ascher_sum_relationships)
- comprobacion propia: es cada colgante-grupo la suma de sus cuerdas?
- detalle vs resumen: perfiles de tamano/valor; totales de grupo de un quipu en otro.
"""
import pandas as pd, numpy as np, os, re
RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]

# --- KFG sum relations ---
d = pd.read_csv(os.path.join(ROOT, "data/external/data-science-khipu-article/data/ascher_sum_relations/ascher_sum_relationships.csv"))
d["kfg"] = d["name"].str.extract(r">(UR\d+)<")
sub = d[d.kfg.isin(LE)].copy()
cols = ["kfg", "num_banded_clusters", "num_seriated_clusters", "num_pendant_pendant_sum",
        "num_pendant_pendants_color_sum", "num_indexed_pendant_sum", "num_subsidiary_pendant_sum",
        "num_cluster_cluster_sum", "num_cluster_sum_bands", "num_ascher_decreasing_cluster"]
sub = sub[cols].fillna(0).astype({c: int for c in cols[1:]})
sub["sum_total"] = sub[cols[1:]].sum(axis=1)
print("Relaciones de suma (KFG) por quipu:")
print(sub.sort_values("kfg").to_string(index=False))
print("\nQuipus SIN ninguna relacion de suma:", sub[sub.sum_total == 0].kfg.tolist())
sub.to_csv(os.path.join(RUTA, "sumas_kfg.csv"), index=False)

# --- comprobacion propia: suma de hijos (padre = suma de hijas) y grupo ---
c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
c = c[c.kfg.isin(LE)].copy()
c["sn"] = c.nudos.isna() | (c.nudos.astype(str).str.strip().isin(["", "nan"]))
c["v"] = np.where(c.sn, np.nan, c.valor)
print("\nSuma de subsidiarias -> madre (padre == suma hijas):")
tot = 0
for kfg, s in c.groupby("kfg"):
    h = s[s.padre.notna()].groupby("padre").v.sum()
    hits = []
    for p, sm in h.items():
        pv = s.loc[s.cuerda == p, "v"]
        if len(pv) and not np.isnan(pv.iloc[0]) and abs(pv.iloc[0] - sm) < 1e-6 and sm > 0:
            hits.append((p, int(pv.iloc[0])))
    if hits:
        print(f"  {kfg}: {hits}")
        tot += len(hits)
print("  total relaciones madre=suma(hijas):", tot)
