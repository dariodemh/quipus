"""Valida la reimplementación contra los conteos publicados por el KFG (por quipu y tipo)."""
import numpy as np, pandas as pd
from kfg import *
Qs = cargar()
F = {"PPS": "pendant_pendant_sum", "COL": "pendant_pendants_color_sum", "IDX": "indexed_pendant_sum", "SUB": "subsidiary_pendant_sum"}
rows = []
for k, Q in Qs.items():
    o = obs(Q)
    rows.append(dict(kfg=k, **{t: int(o[j]) for j, t in enumerate(["PPS", "COL", "IDX", "SUB"])}))
d = pd.DataFrame(rows).set_index("kfg")
for t, f in F.items():
    r = pd.read_csv(REL / f"{f}_relation.csv")
    r["kfg"] = r["name"].map(kfg_name)
    d[t + "_kfg"] = r.groupby("kfg").size().reindex(d.index).fillna(0).astype(int)
lines = []
for t in F:
    a, b = d[t], d[t + "_kfg"]
    lines.append(f"{t}: total nuestro {a.sum()} vs KFG {b.sum()} | quipus >=1: {(a>0).sum()} vs {(b>0).sum()} | quipus con conteo idéntico {(a==b).mean():.3f} | corr {np.corrcoef(a,b)[0,1]:.3f}")
s = pd.read_csv(REL / "ascher_sum_relationships.csv"); s["kfg"] = s["name"].str.extract(r">([^<]+)<")[0].map(kfg_name)
d["en_74"] = d.index.isin(s["kfg"])
d["any4"] = (d[list(F)] > 0).any(axis=1); d["any4_kfg"] = (d[[t + "_kfg" for t in F]] > 0).any(axis=1)
lines.append(f"quipus con >=1 de los 4 tipos: nuestro {d.any4.sum()} / KFG {d.any4_kfg.sum()} ; en la lista del 74 %: {d.en_74.sum()} (de {len(d)})")
lines.append(f"en la lista del 74 % solo por tipos no reimplementados (cluster-cluster, bandas, decreciente): {(d.en_74 & ~d.any4_kfg).sum()}")
print("\n".join(lines))
bad = d[(d.PPS != d.PPS_kfg)].assign(dif=lambda x: x.PPS - x.PPS_kfg).sort_values("dif")
print(bad[["PPS", "PPS_kfg", "COL", "COL_kfg"]].head(8)); print(bad[["PPS", "PPS_kfg"]].tail(5))
d.to_csv("validacion_por_quipu.csv")
open("salida_01_validar.txt", "w", encoding="utf8").write("\n".join(lines) + "\n")
