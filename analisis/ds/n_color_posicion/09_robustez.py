# -*- coding: utf-8 -*-
"""09 - Robustez: colores simples vs compuestos, y escala de rangos.

1) simple: se excluyen cuerdas con color compuesto (':', '/', '-').
2) mixto : los compuestos se colapsan a 'MIX'.
3) rango : y = rango normalizado dentro del quipu (probit), modelo A/B.
Salida: robustez.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NQ, NG = 199, 299

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[(B.k >= 2) & (~B.ausente) & (~B.es_total)].copy()
B["compuesto"] = B.col3.astype(str).str.contains(r"[:/\-]", regex=True)

filas = []
for nombre, d in (("simple", B[~B.compuesto].copy()),
                  ("mixto", B.assign(col3=np.where(B.compuesto, "MIX", B.col3)))):
    d = d.copy()
    vc = d.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
    d = d.merge(vc, on=["kfg", "col3"], how="left")
    d["col3"] = np.where(d.nc >= 3, d.col3, "OTRO")
    for modelo in ("A", "B"):
        fits, rows = {}, []
        for k, g in d.groupby("kfg"):
            if len(g) < 8:
                continue
            f = QuipuFit(g, modelo)
            st = f.stat()
            if f.rank == 0 or (f.n - f.q - st["df1"]) < 2 or f.tss <= 0:
                continue
            p = sum(f.stat(onehot(f.perm_codes(rng), f.C))["r2"] >= f.stat()["r2"] - 1e-12
                    for _ in range(NQ))
            p = (1 + p) / (NQ + 1)
            rows.append(dict(variante=nombre, modelo=modelo, kfg=k, n=f.n,
                             r2=f.stat()["r2"], p=p,
                             r2_abs=f.stat()["r2"] * f.rss0 / max(f.tss, 1e-12)))
            fits[k] = f
        R = pd.DataFrame(rows)
        R["q"] = multipletests(R.p, method="fdr_bh")[1]
        obs = sum(R.set_index("kfg").r2_abs)
        nul = []
        for _ in range(NG):
            T = 0.0
            for k, f in fits.items():
                T += f.stat(onehot(f.perm_codes(rng), f.C))["r2"] * f.rss0 / max(f.tss, 1e-12)
            nul.append(T)
        pg = (1 + np.sum(np.array(nul) >= obs)) / (NG + 1)
        filas.append(dict(variante=nombre, modelo=modelo, n_quipus=len(R),
                          q05=int((R.q < .05).sum()), r2_med=R.r2.median(),
                          r2_abs_med=R.r2_abs.median(), T_abs=obs,
                          p_global_abs=pg))
        print(f"{nombre:7s} {modelo}: q<.05 {int((R.q<.05).sum()):3d}/{len(R):3d} "
              f"r2med {R.r2.median():.4f} r2abs {R.r2_abs.median():.4f} "
              f"T_abs {obs:.3f} p {pg:.4f}", flush=True)

# ---- rango ----
d = B.copy()
d["y"] = d.groupby("kfg").valor.rank(pct=True)
d["y"] = norm.ppf(np.clip(d.y, 0.01, 0.99))
vc = d.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
d = d.merge(vc, on=["kfg", "col3"], how="left")
d["col3"] = np.where(d.nc >= 3, d.col3, "OTRO")
for modelo in ("A", "B"):
    fits, rows = {}, []
    for k, g in d.groupby("kfg"):
        f = QuipuFit(g, modelo)
        st = f.stat()
        if f.rank == 0 or (f.n - f.q - st["df1"]) < 2 or f.tss <= 0:
            continue
        p = sum(f.stat(onehot(f.perm_codes(rng), f.C))["r2"] >= f.stat()["r2"] - 1e-12
                for _ in range(NQ))
        rows.append(dict(variante="rango", modelo=modelo, kfg=k, n=f.n,
                         r2=f.stat()["r2"], p=(1 + p) / (NQ + 1)))
        fits[k] = f
    R = pd.DataFrame(rows)
    R["q"] = multipletests(R.p, method="fdr_bh")[1]
    print(f"rango   {modelo}: q<.05 {int((R.q<.05).sum()):3d}/{len(R):3d} "
          f"r2med {R.r2.median():.4f}", flush=True)
    filas.append(dict(variante="rango", modelo=modelo, n_quipus=len(R),
                      q05=int((R.q < .05).sum()), r2_med=R.r2.median()))

pd.DataFrame(filas).to_csv(OUT + r"\robustez.csv", index=False)
