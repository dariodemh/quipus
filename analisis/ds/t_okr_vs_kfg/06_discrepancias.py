# -*- coding: utf-8 -*-
"""Caracterizacion de las discrepancias de valor (no de estructura)."""
import os, re
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
RE_NUDO = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")

j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
j["prefijo"] = list(j.kfg.str.extract(r"^([A-Z]+)")[0])


def nk(s):
    if not isinstance(s, str):
        return 0
    n = 0
    for m in RE_NUDO.finditer(s):
        tipo = m.group(2)
        n += 1 if tipo.startswith("L") else int(m.group(1))
    return n


j["n_nudos_kfg"] = j.nudos.apply(nk).astype(int)
j["tiene_kfg"] = j.nudos.notna()
d = j[(~j.coincide) & j.tiene_kfg].copy()
d["delta"] = d.valor_okr - d.valor
d["absdelta"] = d.delta.abs()
print("discrepancias:", len(d), "de", d.tiene_kfg.sum(), "cuerdas con nudos KFG")
print("mediana |delta|:", d.absdelta.median(), "media:", round(d.absdelta.mean(), 2))
print("delta>0 (OKR mayor):", (d.delta > 0).sum(), "| delta<0:", (d.delta < 0).sum())
print()
print("magnitud de |delta|:")
bins = [0, 1, 10, 100, 1000, 10**9]
lab = ["0", "1-9", "10-99", "100-999", ">=1000"]
print(pd.cut(d.absdelta, bins=bins, labels=lab, right=False).value_counts().sort_index().to_string())
print()
# desplazamiento decimal exacto
def pot10(x):
    if x <= 0:
        return False
    return abs(np.log10(x) - round(np.log10(x))) < 1e-9
d["ratio"] = d.valor_okr / d.valor.replace(0, np.nan)
d["es_pot10"] = d.ratio.apply(lambda x: pot10(x) if pd.notna(x) else False)
print("OKR/KFG es potencia exacta de 10:", d.es_pot10.sum())
print("mismo numero de nudos:", (d.n_nudos_kfg == d.n_nudos_okr).sum(),
      "| KFG mas nudos:", (d.n_nudos_kfg > d.n_nudos_okr).sum(),
      "| OKR mas nudos:", (d.n_nudos_kfg < d.n_nudos_okr).sum())
print()
print("por nivel KFG:")
print(d.groupby("nivel").agg(n=("delta", "size"), med=("absdelta", "median")).to_string())
print()
print("por prefijo:")
print(d.groupby("prefijo").agg(n=("delta", "size"), med=("absdelta", "median"),
                               shift=("es_pot10", "sum")).to_string())
print()
print("delta mas frecuentes:")
print(d.delta.value_counts().head(12).to_string())
print()
print("cuerdas con delta y mismo largo, ejemplos:")
print(d[d.dlargo <= 0.51].head(20)[["kfg", "cuerda", "valor", "nudos", "valor_okr",
                                    "n_nudos_kfg", "n_nudos_okr", "delta"]].to_string())
d.to_csv(os.path.join(SAL, "discrepancias_valor.csv"), index=False)
