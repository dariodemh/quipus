# -*- coding: utf-8 -*-
"""05 - Potencia declarada: efecto de color plantado sobre datos reales.

Procedimiento por simulacion:
  1) se permutan los colores dentro de (quipu,k,pos) -> se destruye la asociacion real
  2) se suma delta a y=log1p(valor) en las cuerdas del color objetivo (modal, o W)
  3) se calcula T = suma de R2 parcial del color
Deteccion: T >= percentil 95 del nulo (999 permutaciones sin plantado).
Salida: potencia.csv, potencia_resumen.csv
"""
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, r"./analisis/ds/n_color_posicion")
from motor import QuipuFit, onehot

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NSIM = 200
NPERM_NULO = 499

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[(B.k >= 2) & (~B.ausente) & (~B.es_total)].copy()
vc = B.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
B = B.merge(vc, on=["kfg", "col3"], how="left")
B["col3"] = np.where(B.nc >= 3, B.col3, "OTRO")


def fits_de(modelo):
    out = {}
    for kfg, g in B.groupby("kfg"):
        f = QuipuFit(g, modelo)
        st = f.stat()
        if f.rank > 0 and (f.n - f.q - st["df1"]) >= 2 and f.tss > 0:
            out[kfg] = f
    return out


def T_de(fits, codes_dict=None):
    T = 0.0
    for f in fits.values():
        if codes_dict is None:
            M = f.M
        else:
            M = onehot(codes_dict[f.df.kfg.iloc[0]], f.C)
        T += f.stat(M)["r2"]
    return T


def perms(fits):
    return {k: f.perm_codes(rng) for k, f in fits.items()}


filas = []
for modelo in ("A", "B"):
    fits = fits_de(modelo)
    # ---- nulo ----
    nul = np.array([T_de(fits, perms(fits)) for _ in range(NPERM_NULO)])
    crit = np.quantile(nul, 0.95)
    obs = T_de(fits)
    print(f"modelo {modelo}: obs T={obs:.3f} | nulo media {nul.mean():.3f} "
          f"sd {nul.std():.3f} | crit95 {crit:.3f}", flush=True)

    # ---- calibracion: 300 simulaciones bajo el nulo ----
    cal = np.array([T_de(fits, perms(fits)) for _ in range(NSIM)])
    print(f"  calibracion: rechazo al 5% = {(cal >= crit).mean():.3f}", flush=True)

    # ---- potencia ----
    for objetivo in ("modal", "W"):
        if objetivo == "W" and "W" not in fits[list(fits)[0]].cols:
            # W puede no existir en todos; se planta donde exista
            pass
        for delta in (0.0, 0.2, 0.35, 0.5, 0.7):
            det = 0
            for s in range(NSIM):
                codes = perms(fits)
                T = 0.0
                for k, f in fits.items():
                    c = codes[k].copy()
                    if objetivo == "modal":
                        target = 0
                    else:
                        target = f.cols.index("W") if "W" in f.cols else None
                    y0 = f.y.copy()
                    if target is not None:
                        y0[c == target] += delta
                    # estadistico con y plantado y colores permutados
                    # (se reusa la maquinaria cambiando y temporalmente)
                    f_old = f.y
                    f.y = y0
                    f.r0 = y0 - f.Qw @ (f.Qw.T @ y0)
                    f.rss0 = float(f.r0 @ f.r0)
                    T += f.stat(onehot(c, f.C))["r2"]
                    f.y = f_old
                    f.r0 = f_old - f.Qw @ (f.Qw.T @ f_old)
                    f.rss0 = float(f.r0 @ f.r0)
                det += (T >= crit)
            filas.append(dict(modelo=modelo, objetivo=objetivo, delta=delta,
                              potencia=det / NSIM, crit95=crit, obs_T=obs,
                              nulo_media=nul.mean(), nulo_sd=nul.std(),
                              calibracion=float((cal >= crit).mean()),
                              n_quipus=len(fits)))
            print(f"  {objetivo:5s} delta={delta:.2f}: potencia {(det/NSIM):.3f}", flush=True)

P = pd.DataFrame(filas)
P.to_csv(OUT + r"\potencia.csv", index=False)

# resumen: MDE al 80%
res = []
for (m, o), g in P.groupby(["modelo", "objetivo"]):
    g = g.sort_values("delta")
    ok = g[g.potencia >= 0.8]
    if len(ok):
        d1 = ok.delta.iloc[0]
        prev = g[g.delta < d1]
        if len(prev):
            x0, y0 = prev.delta.iloc[-1], prev.potencia.iloc[-1]
            mde = x0 + (0.8 - y0) * (d1 - x0) / (ok.potencia.iloc[0] - y0)
        else:
            mde = d1
    else:
        mde = np.nan
    res.append(dict(modelo=m, objetivo=o, mde80=mde,
                    pot_05=float(g.loc[g.delta == 0.5, "potencia"].iloc[0]),
                    pot_07=float(g.loc[g.delta == 0.7, "potencia"].iloc[0]),
                    calibracion=float(g.calibracion.iloc[0])))
R = pd.DataFrame(res)
R.to_csv(OUT + r"\potencia_resumen.csv", index=False)
print("\n", R.round(3).to_string(index=False))
