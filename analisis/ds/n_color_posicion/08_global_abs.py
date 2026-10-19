# -*- coding: utf-8 -*-
"""08 - Test agregado en varianza absoluta y z por quipu (difuso vs concentrado).

T_abs = suma de DeltaSS/TSS (proporcion de varianza total explicada por color
despues de los controles).  Ademas, z por quipu = (r2_obs - media_nula)/sd_nula
y Stouffer sobre quipus.  Variante primaria, modelos A y B.
Salida: agregados_abs.csv, z_quipu.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd
from scipy.stats import norm

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NG, NZ = 999, 199

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[(B.k >= 2) & (~B.ausente) & (~B.es_total)].copy()
vc = B.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
B = B.merge(vc, on=["kfg", "col3"], how="left")
B["col3"] = np.where(B.nc >= 3, B.col3, "OTRO")

filas, zs = [], []
for modelo in ("A", "B"):
    fits = {k: QuipuFit(g, modelo) for k, g in B.groupby("kfg")}
    obs = {k: f.stat()["r2"] for k, f in fits.items()}
    Tobs = sum(obs[k] * fits[k].rss0 / max(fits[k].tss, 1e-12) for k in fits)
    nulT = np.empty(NG)
    for b in range(NG):
        T = 0.0
        for k, f in fits.items():
            M = onehot(f.perm_codes(rng), f.C)
            T += f.stat(M)["r2"] * f.rss0 / max(f.tss, 1e-12)
        nulT[b] = T
    pT = (1 + np.sum(nulT >= Tobs)) / (NG + 1)

    # z por quipu
    zk = {}
    for k, f in fits.items():
        vals = np.array([f.stat(onehot(f.perm_codes(rng), f.C))["r2"] for _ in range(NZ)])
        zk[k] = (obs[k] - vals.mean()) / (vals.std() + 1e-12)
        zs.append(dict(modelo=modelo, kfg=k, r2=obs[k], r2_media_nula=vals.mean(),
                       r2_sd_nula=vals.std(), z=zk[k], n=f.n, C=f.C,
                       df1=f.stat()["df1"], df2=f.stat()["df2"],
                       r2_abs=obs[k] * f.rss0 / max(f.tss, 1e-12),
                       copia=bool(f.df.en_copias.iloc[0])))
    Z = np.array(list(zk.values()))
    st = Z.sum() / np.sqrt(len(Z))
    filas.append(dict(modelo=modelo, n_quipus=len(Z), T_abs=Tobs,
                      nulo_media=nulT.mean(), nulo_sd=nulT.std(), p_abs=pT,
                      z_medio=Z.mean(), stouffer=st,
                      p_stouffer=1 - norm.cdf(st),
                      frac_z_pos=float((Z > 0).mean()),
                      frac_z_15=float((Z > 1.5).mean()),
                      z_mediana=float(np.median(Z))))
    print(f"modelo {modelo}: T_abs {Tobs:.4f} (nulo {nulT.mean():.4f}±{nulT.std():.4f}) "
          f"p {pT:.4f} | z medio {Z.mean():.3f} Stouffer {st:.2f} "
          f"p {1-norm.cdf(st):.2g} | frac z>0 {(Z>0).mean():.3f} | "
          f"frac z>1.5 {(Z>1.5).mean():.3f}", flush=True)

pd.DataFrame(filas).to_csv(OUT + r"\agregados_abs.csv", index=False)
pd.DataFrame(zs).to_csv(OUT + r"\z_quipu.csv", index=False)
