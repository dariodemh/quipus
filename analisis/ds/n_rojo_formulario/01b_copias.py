# -*- coding: utf-8 -*-
"""Post-proceso del ataque 1: excluir quipus con copias conocidas (14_copias)."""
import pandas as pd
from statsmodels.stats.multitest import multipletests
from scipy.stats import binom
R = pd.read_csv(r"./analisis/ds/n_rojo_formulario/color_controles.csv")
cp = pd.read_csv(r"./analisis/14_copias/filas_alineadas.csv", low_memory=False)
copias = set(cp.A.dropna()) | set(cp.B.dropna())
R["copia"] = R.kfg.isin(copias)
for control in ("global", "ninguno", "resid"):
    m = (R.control == control) & (~R.copia)
    q = R.loc[m, "q"]  # q ya viene corregido sobre las 403; se recalcula sobre el subconjunto
    q2 = multipletests(R.loc[m, "p"], method="fdr_bh")[1]
    print(f"{control:8s} sin copias: n={m.sum()} q_original<.05={(q<.05).sum()} "
          f"q_recalc<.05={(q2<.05).sum()} eta2_med={R.loc[m,'eta2'].median():.3f} "
          f"binom_p={binom.sf((q2<.05).sum()-1, m.sum(), .05):.2e}")
print("quipus en familias de copia:", len(copias))
print("de los 44 resid, cuantos son copia:", int(((R.control=='resid')&(R.q<0.05)&R.copia).sum()))
