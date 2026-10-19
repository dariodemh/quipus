"""Verificación de las afirmaciones de color de K-CAT.

1) "El blanco (W) es el 27,5% de las entradas de color y aparece en el 77,7%
   de los khipus."
2) "El color primario predice el orden de magnitud del valor
   (Kruskal-Wallis H=1.419, p=3,6e-267)."

La segunda se prueba a nivel de cuerda (como K-CAT, que trata decenas de miles
de cuerdas como independientes) y a nivel de quipu (unidad correcta):
  - estadístico: diferencia de mediana de log10(valor) entre cuerdas blancas
    y no blancas, dentro de cada quipu;
  - nulo: barajar etiquetas de color DENTRO de cada quipu, 3000 permutaciones,
    p bilateral; se informa también el test de signos por quipu.
"""
import json
import os
import re

import numpy as np
import pandas as pd
from scipy.stats import kruskal, wilcoxon, binomtest

from comun import cargar_cuerdas, SALIDA, SEMILLA

rng = np.random.default_rng(SEMILLA)
c = cargar_cuerdas()
R = {}

# ---------------------------------------------------------------- (1) prevalencia de W
col = c.color.dropna().astype(str)
prim = col.str.extract(r"^([A-Z]+)", expand=False)
c["color_prim"] = c.color.astype(str).str.extract(r"^([A-Z]+)", expand=False)
w_exacta = col.eq("W")
w_contiene = col.str.contains("W", regex=False)
khipus = c.kfg.nunique()
print("--- (1) blanco ---")
print(f"cuerdas con color={len(col)}; W exacto={w_exacta.sum()} "
      f"({100*w_exacta.mean():.2f}%); contiene W={w_contiene.sum()} "
      f"({100*w_contiene.mean():.2f}%)")
print(f"khipus con W exacto={c[c.color.astype(str) == 'W'].kfg.nunique()}/{khipus} "
      f"({100*c[c.color.astype(str) == 'W'].kfg.nunique()/khipus:.1f}%)")
masc = c.color.astype(str).str.contains("W", regex=False) & c.color.notna()
print(f"khipus con alguna cuerda que contiene W={c[masc].kfg.nunique()}/{khipus} "
      f"({100*c[masc].kfg.nunique()/khipus:.1f}%)")
print("K-CAT declara 27,5% de ENTRADAS (no cuerdas) y 77,7% de khipus; "
      "las entradas de color pueden ser varias por cuerda.")
R["blanco"] = dict(pct_W_exacto=round(100*float(w_exacta.mean()), 2),
                   pct_contiene_W=round(100*float(w_contiene.mean()), 2),
                   pct_khipus_W=round(100*c[c.color.astype(str) == 'W'].kfg.nunique()/khipus, 1),
                   pct_khipus_contiene=round(100*c[masc].kfg.nunique()/khipus, 1))

# ---------------------------------------------------------------- (2) color vs valor
d = c[(c.v > 0) & c.color_prim.notna()].copy()
d["logv"] = np.log10(d.v)
d["blanco"] = d.color_prim.eq("W")
print("\n--- (2) color y magnitud del valor ---")
print(f"cuerdas con valor>0 y color primario={len(d)} en {d.kfg.nunique()} khipus")

# 2a. Test a nivel de cuerda (pseudorreplicación, como K-CAT)
grupos = [g.logv.values for _, g in d.groupby("color_prim") if len(g) >= 30]
H, p_kw = kruskal(*grupos)
print(f"Kruskal-Wallis a nivel de CUERDA: {len(grupos)} colores con n>=30, "
      f"H={H:.1f}, p={p_kw:.3g}  (K-CAT: H=1419, p=3,6e-267)")
R["kw_cuerda"] = dict(n_colores=len(grupos), H=round(float(H), 1),
                      p=float(f"{p_kw:.3g}"))

# 2b. Test a nivel de quipu: diferencia de medianas blanco - no blanco
filas = []
for k, g in d.groupby("kfg"):
    w = g[g.blanco].logv
    nw = g[~g.blanco].logv
    if len(w) >= 3 and len(nw) >= 3:
        filas.append((k, float(w.median() - nw.median()), len(w), len(nw)))
q = pd.DataFrame(filas, columns=["kfg", "dif", "nw", "nnw"])
print(f"khipus con >=3 cuerdas blancas y >=3 no blancas: {len(q)}")
if len(q):
    pos, neg = int((q.dif > 0).sum()), int((q.dif < 0).sum())
    p_sign = binomtest(pos, pos + neg, 0.5).pvalue if pos + neg else np.nan
    print(f"  mediana de la diferencia (W - no W)={q.dif.median():+.3f} log10; "
          f"khipus W>noW={pos}, W<noW={neg}; p_signos={p_sign:.3g}")
    R["quipu_signos"] = dict(n=int(len(q)), mediana_dif=round(float(q.dif.median()), 3),
                             pos=pos, neg=neg, p=float(p_sign))

# 2c. Nulo: barajar color dentro de cada quipu
# estadístico = media de las diferencias de medianas por quipu
obs = q.dif.mean() if len(q) else np.nan
grupos_idx = [np.asarray(idx) for idx in d.groupby("kfg").indices.values()]
blanco = d.blanco.values.astype(bool)
logv = d.logv.values.astype(float)


def stat_perm(b):
    difs = []
    for idx in grupos_idx:
        bb, x = b[idx], logv[idx]
        w, nw = x[bb], x[~bb]
        if len(w) >= 3 and len(nw) >= 3:
            difs.append(np.median(w) - np.median(nw))
    return np.mean(difs) if difs else np.nan


n_perm = 1000
mayores = 0
for _ in range(n_perm):
    b = blanco.copy()
    for idx in grupos_idx:
        b[idx] = rng.permutation(b[idx])
    if abs(stat_perm(b)) >= abs(obs):
        mayores += 1
p_perm = (mayores + 1) / (n_perm + 1)
print(f"  nulo intra-quipu: observado={obs:+.3f}; p bilateral={p_perm:.4f} "
      f"(N={n_perm})")
R["nulo_color"] = dict(obs=round(float(obs), 3), p_perm=float(p_perm), n_perm=n_perm)

with open(os.path.join(SALIDA, "res_07_color.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_07_color.json")
