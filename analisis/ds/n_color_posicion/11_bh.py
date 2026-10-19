# -*- coding: utf-8 -*-
"""11 - BH con resolucion suficiente (999 permutaciones por quipu).

299/499 permutaciones no permiten que un p-valor baje de 0.002-0.003, y el
umbral de BH para 200 tests es ~0.00025: el conteo de quipus significativos
queda artificialmente en 0.  Aqui se usan 999 permutaciones (p_min=0.001)
para primario A/B y sin_copias_max B.
Salida: bh_999.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NQ = 999

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[B.k >= 2].copy()
B["es_max"] = False
for (k, g), idx in B.groupby(["kfg", "grupo"]).groups.items():
    B.loc[B.loc[idx, "valor"].idxmax(), "es_max"] = True


def variante(nombre):
    d = B.copy()
    d = d[~d.ausente]
    if nombre in ("primario", "sin_copias_max"):
        d = d[~d.es_total]
    if nombre == "sin_copias_max":
        d = d[d.es_rep & ~d.es_max]
    vc = d.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
    d = d.merge(vc, on=["kfg", "col3"], how="left")
    d["col3"] = np.where(d.nc >= 3, d.col3, "OTRO")
    return d


filas = []
for var, modelo in (("primario", "A"), ("primario", "B"), ("sin_copias_max", "B")):
    d = variante(var)
    rows = []
    for kfg, g in d.groupby("kfg"):
        f = QuipuFit(g, modelo)
        st = f.stat()
        df2 = f.n - f.q - st["df1"]
        if f.rank == 0 or df2 < 2 or f.rss0 <= 1e-12:
            continue
        obs = st["r2"]
        cnt = sum(f.stat(onehot(f.perm_codes(rng), f.C))["r2"] >= obs - 1e-12
                  for _ in range(NQ))
        rows.append(dict(variante=var, modelo=modelo, kfg=kfg, n=f.n, C=f.C,
                         df1=st["df1"], df2=df2, r2=obs,
                         r2_abs=obs * f.rss0 / max(f.tss, 1e-12),
                         p=(1 + cnt) / (NQ + 1)))
    R = pd.DataFrame(rows)
    R["q"] = multipletests(R.p, method="fdr_bh")[1]
    print(f"{var:14s} {modelo}: n={len(R)} q<.05={int((R.q<.05).sum())} "
          f"q<.10={int((R.q<.10).sum())} p_min={R.p.min():.4f} | "
          f"sig: {', '.join(R[R.q<.05].sort_values('p').kfg.head(20))}", flush=True)
    filas.append(R)

pd.concat(filas).to_csv(OUT + r"\bh_999.csv", index=False)
