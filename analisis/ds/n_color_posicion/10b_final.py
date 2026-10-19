# -*- coding: utf-8 -*-
"""10b - Igual que 10_final pero solo variantes clave y guardado incremental.

Variantes: primario (sin ausentes, sin totales) y sin_copias_max.
Modelos A y B.  Filtro df2>=2.  Salida: color_posicion.csv (partes + final).
"""
import sys
import warnings
import numpy as np
import pandas as pd
from scipy.stats import norm, binom
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NQ, NG, NZ = 299, 499, 79

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[B.k >= 2].copy()
B["es_max"] = False
for (k, g), idx in B.groupby(["kfg", "grupo"]).groups.items():
    B.loc[B.loc[idx, "valor"].idxmax(), "es_max"] = True


def variante(nombre):
    d = B[~B.ausente].copy()
    d = d[~d.es_total]
    if nombre == "sin_copias_max":
        d = d[d.es_rep & ~d.es_max]
    vc = d.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
    d = d.merge(vc, on=["kfg", "col3"], how="left")
    d["col3"] = np.where(d.nc >= 3, d.col3, "OTRO")
    return d


def r2_marg(d):
    y = d.y.values
    tss = ((y - y.mean()) ** 2).sum()
    if tss <= 0:
        return np.nan
    m = d.groupby("col3").y.transform("mean").values
    return 1 - ((y - m) ** 2).sum() / tss


partes, ags = [], []
for var in ("primario", "sin_copias_max"):
    d = variante(var)
    for modelo in ("A", "B"):
        fits, rows = {}, []
        for kfg, g in d.groupby("kfg"):
            f = QuipuFit(g, modelo)
            st = f.stat(full=True)
            df2 = f.n - f.q - st["df1"]
            base = dict(kfg=kfg, n=f.n, ngrupos=f.df.grupo.nunique(),
                        npos=f.df[["k", "pos"]].drop_duplicates().shape[0],
                        npos_var=int((f.df.groupby(["k", "pos"]).col3.nunique() >= 2).sum()),
                        C=f.C, rank=f.rank, df1=st["df1"], df2=df2,
                        r2_pos=1 - f.rss0 / f.tss if f.tss > 0 else np.nan,
                        r2_marg=r2_marg(g))
            if not (f.rank > 0 and df2 >= 2 and f.rss0 > 1e-12):
                rows.append(dict(**base, r2=0.0, r2_abs=0.0, F=0.0, p=1.0, q=1.0,
                                 valido=False, ef_rango=0.0, ef_W=np.nan))
                continue
            cnt = sum(f.stat(onehot(f.perm_codes(rng), f.C))["r2"] >= st["r2"] - 1e-12
                      for _ in range(NQ))
            ef = st["efectos"]
            isW = f.df.col3.astype(str).values == "W"
            dW = (f.r0[isW].mean() - f.r0[~isW].mean()) if (isW.sum() >= 2 and (~isW).sum() >= 2) else np.nan
            rows.append(dict(**base, r2=st["r2"], r2_abs=st["r2"] * f.rss0 / max(f.tss, 1e-12),
                             F=st["F"], p=(1 + cnt) / (NQ + 1), q=np.nan, valido=True,
                             ef_rango=float(np.max(ef) - np.min(ef)) if len(ef) else np.nan,
                             ef_W=dW))
            fits[kfg] = f
        R = pd.DataFrame(rows)
        R["q"] = multipletests(R.p, method="fdr_bh")[1]
        R["variante"] = var
        R["modelo"] = modelo
        R["copia"] = R.kfg.map(d.groupby("kfg").en_copias.first())
        R["es_rep"] = R.kfg.map(d.groupby("kfg").es_rep.first())
        R.to_csv(OUT + rf"\parte_{var}_{modelo}.csv", index=False)
        partes.append(R)
        obs = sum(f.stat()["r2"] * f.rss0 / max(f.tss, 1e-12) for f in fits.values())
        nul = np.empty(NG)
        for b in range(NG):
            T = 0.0
            for f in fits.values():
                T += f.stat(onehot(f.perm_codes(rng), f.C))["r2"] * f.rss0 / max(f.tss, 1e-12)
            nul[b] = T
        pg = (1 + np.sum(nul >= obs)) / (NG + 1)
        Z = []
        for f in fits.values():
            r2o = f.stat()["r2"]
            vals = np.array([f.stat(onehot(f.perm_codes(rng), f.C))["r2"] for _ in range(NZ)])
            Z.append((r2o - vals.mean()) / (vals.std() + 1e-12))
        Z = np.array(Z)
        stz = Z.sum() / np.sqrt(len(Z))
        kq = int(((R.q < .05) & R.valido).sum())
        nv = int(R.valido.sum())
        ags.append(dict(variante=var, modelo=modelo, n_valid=nv, n_total=len(R),
                        cuerdas=int(R[R.valido].n.sum()), q05=kq, esperado=0.05 * nv,
                        binom_p=binom.sf(kq - 1, nv, 0.05),
                        r2_med=R[R.valido].r2.median(),
                        r2_abs_med=R[R.valido].r2_abs.median(),
                        r2_abs_suma=obs, p_global=pg, nulo_media=nul.mean(),
                        z_medio=Z.mean(), stouffer=stz, p_stouffer=1 - norm.cdf(stz),
                        frac_z_pos=float((Z > 0).mean()),
                        df2_med=R[R.valido].df2.median()))
        print(f"{var:14s} {modelo}: n {nv}/{len(R)} q<.05 {kq} (esp {0.05*nv:.1f}, "
              f"p {binom.sf(kq-1,nv,0.05):.2g}) r2_abs_med {R[R.valido].r2_abs.median():.4f} "
              f"suma {obs:.3f} pglob {pg:.4f} | z {Z.mean():.2f} "
              f"frac+ {(Z>0).mean():.2f}", flush=True)

RES = pd.concat(partes, ignore_index=True)
RES.to_csv(OUT + r"\color_posicion.csv", index=False)
AG = pd.DataFrame(ags)
AG["holm"] = multipletests(AG.p_global, method="holm")[1]
AG.to_csv(OUT + r"\agregados_final.csv", index=False)
print("\n", AG.round(4).to_string(index=False))
