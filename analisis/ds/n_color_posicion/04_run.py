# -*- coding: utf-8 -*-
"""04 - Tests color|posicion por quipu y agregados.

Variantes:
  todo          : k>=2, incluye ausentes y totales (comparabilidad)
  sin_aus       : excluye cuerdas ausentes (valor 0 sin nudos)
  primario      : sin ausentes y sin cuerdas de total
  sin_copias    : primario, un representante por familia de copia
  sin_copias_max: primario, sin copias y sin la mayor del grupo
Modelos: A (posicion), B (grupo+posicion), C (B + nrac + log largo).
Salida: color_posicion.csv, agregados.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd
from scipy.stats import binom
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot, pvalor

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NPERM_Q = 499
NPERM_G = 999

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[B.k >= 2].copy()

# mayor del grupo
B["es_max"] = False
for (k, g), idx in B.groupby(["kfg", "grupo"]).groups.items():
    B.loc[B.loc[idx, "valor"].idxmax(), "es_max"] = True


def variante(nombre):
    d = B.copy()
    if nombre != "todo":
        d = d[~d.ausente]
    if nombre in ("primario", "sin_copias", "sin_copias_max"):
        d = d[~d.es_total]
    if nombre in ("sin_copias", "sin_copias_max"):
        d = d[d.es_rep]
    if nombre == "sin_copias_max":
        d = d[~d.es_max]
    # re-colapsar colores raros dentro del quipu
    vc = d.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
    d = d.merge(vc, on=["kfg", "col3"], how="left")
    d["col3"] = np.where(d.nc >= 3, d.col3, "OTRO")
    d = d.sort_values(["kfg", "k", "grupo", "pos"]).reset_index(drop=True)
    return d


def r2_color_marginal(d):
    y = d.y.values
    tss = ((y - y.mean()) ** 2).sum()
    m = d.groupby("col3").y.transform("mean").values
    return 1 - ((y - m) ** 2).sum() / tss if tss > 0 else np.nan


def preparar(d, modelo):
    extra = None
    if modelo == "C":
        L = np.log(d.L.where(d.L > 0))
        extra = np.column_stack([d.nrac.values.astype(float),
                                 L.fillna(L.median()).values])
    try:
        return QuipuFit(d, "B" if modelo in ("B", "C") else "A", extra=extra)
    except Exception:
        return None


def corre_quipu(d, modelo, nperm=NPERM_Q):
    qf = preparar(d, modelo)
    if qf is None or qf.n < 8:
        return None
    st = qf.stat(full=True)
    if qf.rank == 0:
        p, r2, F = 1.0, 0.0, 0.0
    else:
        r2, p = pvalor(qf, rng, nperm, stat="r2")
        F = st["F"]
    ef = st.get("efectos", np.array([0.0]))
    isW = (qf.df.col3.astype(str).values == "W")
    dW = np.nan
    if isW.sum() >= 2 and (~isW).sum() >= 2:
        dW = qf.r0[isW].mean() - qf.r0[~isW].mean()
    npos = d[["k", "pos"]].drop_duplicates().shape[0]
    nvar = (d.groupby(["k", "pos"]).col3.nunique() >= 2).sum()
    return dict(kfg=d.kfg.iloc[0], n=len(d), ngrupos=d.grupo.nunique(),
                npos=npos, npos_var=int(nvar), C=qf.C, rank=qf.rank,
                r2=r2, F=F, df1=st["df1"], df2=st["df2"], p=p,
                r2_pos=1 - qf.rss0 / qf.tss if qf.tss > 0 else np.nan,
                r2_color_marg=r2_color_marginal(d),
                ef_rango=float(np.max(ef) - np.min(ef)) if len(ef) else np.nan,
                ef_W=dW,
                copia=bool(d.en_copias.iloc[0]),
                es_rep=bool(d.es_rep.iloc[0]),
                familia=d.familia.iloc[0] if pd.notna(d.familia.iloc[0]) else ""), qf


def global_test(fits, nperm=NPERM_G):
    obs = sum(f.stat()["r2"] for f in fits)
    cnt = 0
    for _ in range(nperm):
        T = 0.0
        for f in fits:
            T += f.stat(onehot(f.perm_codes(rng), f.C))["r2"]
        if T >= obs - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (nperm + 1)


filas, ags = [], []
for var in ("todo", "sin_aus", "primario", "sin_copias", "sin_copias_max"):
    d = variante(var)
    for modelo in ("A", "B", "C"):
        if modelo == "C" and var not in ("primario", "sin_copias"):
            continue
        fits, rows = [], []
        for kfg, g in d.groupby("kfg"):
            out = corre_quipu(g, modelo)
            if out:
                r, qf = out
                r.update(variante=var, modelo=modelo)
                rows.append(r)
                fits.append(qf)
        R = pd.DataFrame(rows)
        if len(R) == 0:
            continue
        R["q"] = multipletests(R.p, method="fdr_bh")[1]
        T, pg = global_test(fits)
        kq = int((R.q < 0.05).sum())
        ags.append(dict(variante=var, modelo=modelo, n_quipus=len(R),
                        cuerdas=int(R.n.sum()),
                        q05=kq, esperado=0.05 * len(R),
                        binom_p=binom.sf(kq - 1, len(R), 0.05),
                        r2_med=R.r2.median(), r2_pos_med=R.r2_pos.median(),
                        r2_marg_med=R.r2_color_marg.median(),
                        ef_rango_med=R.ef_rango.median(),
                        ef_W_med=R.ef_W.median(),
                        frac_W_pos=float((R.ef_W > 0).mean()),
                        T=T, p_global=pg,
                        n_rank0=int((R["rank"] == 0).sum()),
                        npos_var=int(R.npos_var.sum())))
        filas.append(R)
        print(f"{var:14s} {modelo}: q<.05 {kq:3d}/{len(R):3d} (esp {0.05*len(R):4.1f}, "
              f"binom {binom.sf(kq-1,len(R),0.05):.2g}) r2med {R.r2.median():.4f} "
              f"r2pos {R.r2_pos.median():.3f} r2marg {R.r2_color_marg.median():.3f} "
              f"T {T:.2f} pglob {pg:.4f} rank0 {int((R['rank']==0).sum())}", flush=True)

RES = pd.concat(filas, ignore_index=True)
RES.to_csv(OUT + r"\color_posicion.csv", index=False)
AG = pd.DataFrame(ags)
AG["holm_global"] = multipletests(AG.p_global, method="holm")[1]
AG.to_csv(OUT + r"\agregados.csv", index=False)
print("\nGuardado color_posicion.csv:", RES.shape)
print(AG[["variante", "modelo", "q05", "p_global", "holm_global"]].to_string(index=False))
