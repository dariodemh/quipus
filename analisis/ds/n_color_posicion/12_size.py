# -*- coding: utf-8 -*-
"""12 - Modelo C: grupo + posicion + nrac + log(largo) + color.

Controla que el color sea un proxy del tamano de la cuerda (la explicacion
aburrida del equipo rojo).  Variante primaria.  Salida: tamano_C.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd
from scipy.stats import binom
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NQ, NG = 299, 499

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[(B.k >= 2) & (~B.ausente) & (~B.es_total)].copy()
vc = B.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
B = B.merge(vc, on=["kfg", "col3"], how="left")
B["col3"] = np.where(B.nc >= 3, B.col3, "OTRO")

rows, fits = [], {}
for kfg, g in B.groupby("kfg"):
    L = np.log(g.L.where(g.L > 0))
    extra = np.column_stack([g.nrac.values.astype(float), L.fillna(L.median()).values])
    f = QuipuFit(g, "B", extra=extra)
    st = f.stat()
    df2 = f.n - f.q - st["df1"]
    if f.rank == 0 or df2 < 2 or f.rss0 <= 1e-12:
        continue
    cnt = sum(f.stat(onehot(f.perm_codes(rng), f.C))["r2"] >= st["r2"] - 1e-12
              for _ in range(NQ))
    rows.append(dict(kfg=kfg, n=f.n, C=f.C, df1=st["df1"], df2=df2, r2=st["r2"],
                     r2_abs=st["r2"] * f.rss0 / max(f.tss, 1e-12),
                     p=(1 + cnt) / (NQ + 1)))
    fits[kfg] = f

R = pd.DataFrame(rows)
R["q"] = multipletests(R.p, method="fdr_bh")[1]
obs = sum(f.stat()["r2"] * f.rss0 / max(f.tss, 1e-12) for f in fits.values())
nul = []
for _ in range(NG):
    T = 0.0
    for f in fits.values():
        T += f.stat(onehot(f.perm_codes(rng), f.C))["r2"] * f.rss0 / max(f.tss, 1e-12)
    nul.append(T)
pg = (1 + np.sum(np.array(nul) >= obs)) / (NG + 1)
R.to_csv(OUT + r"\tamano_C.csv", index=False)
kq = int((R.q < .05).sum())
print(f"modelo C (tamano): n={len(R)} q<.05={kq} (esp {0.05*len(R):.1f}, "
      f"p {binom.sf(kq-1,len(R),0.05):.2g}) r2med {R.r2.median():.4f} "
      f"r2abs_med {R.r2_abs.median():.4f} suma {obs:.3f} pglob {pg:.4f}")
