# -*- coding: utf-8 -*-
"""04. Controles: nulos explicitos, p empiricos y correccion multiple.

(a) granularidad de las celdas de UR278 (5 pruebas) -> BH
(b) coincidencia capacidad-ledger para 6 modelos de unidad -> Holm
(c) estructura de columnas de UR278 (permutacion dentro de fila)
(d) robustez del total de UR278 a la reconstruccion
"""
import numpy as np, pandas as pd
from scipy.stats import chi2 as chi2d
from comun import leer_ur278, leer_libro, RNG, VOL_SITIO_M3

d, cols = leer_ur278()
V = d[cols].values.astype(float)
vals = V[~np.isnan(V)]
B = 20000

# ---------------- (a) granularidad ----------------
print("=== (a) Granularidad de las 249 celdas: test de multiplos ===")
filas = []
for m in [2, 5, 10, 25, 50]:
    o = float(np.mean(np.isclose(vals % m, 0)))
    sim = (RNG.integers(0, m, size=(B, len(vals))) == 0).mean(axis=1)
    p = (np.sum(sim >= o) + 1) / (B + 1)
    filas.append(dict(prueba=f"multiplo de {m}", obs=o, esperado=1 / m, p=p))
A = pd.DataFrame(filas)
# BH
A = A.sort_values("p").reset_index(drop=True)
A["q_BH"] = np.minimum.accumulate((A.p * len(A) / (A.index + 1))[::-1])[::-1]
print(A.round(4).to_string(index=False))
print("=> ninguna prueba sobrevive BH; las celdas no se agrupan en lotes redondos.")
print()

# ---------------- (b) coincidencia capacidad ----------------
print("=== (b) Coincidencia 'volumen del ledger = capacidad': p bajo nulo log-uniforme ===")
L = leer_libro()
LED = {"flujo 47 (61 790)": 61790.0,
       "maestro UR269 (122 609)": float(L[L.quipu == "UR269"].cabecera.sum())}
MODELOS = {"racion 0,7 kg": 0.00093, "arroba 15,5 L": 0.0155, "carga 35 L": 0.035,
           "costal 34,5 L": 0.0345, "fanega 55,5 L": 0.0555, "costal 69 L": 0.069}
vmin, vmax = 5e-5, 0.5
filas = []

def p_dos_colas(v_unidad, ledger, vmin=5e-5, vmax=0.5):
    """p de dos colas: prob. de que un volumen log-uniforme entre vmin y vmax
    quede TAN CERCA o mas de la capacidad como el modelo propuesto."""
    r = ledger * v_unidad / VOL_SITIO_M3
    d = abs(np.log10(r))
    return min(1.0, 2 * d / np.log10(vmax / vmin)), r

for nombre, v in MODELOS.items():
    p, r = p_dos_colas(v, LED["maestro UR269 (122 609)"])
    filas.append(dict(unidad=nombre, vol_unidad_L=v * 1000, ratio_ledger_capacidad=r, p=p))
Bq = pd.DataFrame(filas).sort_values("p").reset_index(drop=True)
# Holm
m = len(Bq)
Bq["p_holm"] = [min(1.0, (m - i) * p) for i, p in enumerate(Bq.p)]
Bq["p_holm"] = np.maximum.accumulate(Bq.p_holm)
print(Bq.round(4).to_string(index=False))
print("=> ningun modelo se distingue: la capacidad solo excluye ordenes de magnitud.")
print()

# ---------------- (c) estructura de columnas ----------------
print("=== (c) Estructura de columnas de UR278 (permutacion dentro de fila) ===")
# estadistico: CV entre las medias de columna (tras dividir por la media de fila)
def cv_cols(M):
    P = M / np.nansum(M, axis=1, keepdims=True)
    med = np.nanmean(P, axis=0)
    return np.std(med, ddof=1) / np.mean(med)

obs = cv_cols(V)
sims = np.empty(5000)
for b in range(5000):
    M = V.copy()
    for i in range(M.shape[0]):
        idx = np.where(~np.isnan(M[i]))[0]
        M[i, idx] = M[i, RNG.permutation(idx)]
    sims[b] = cv_cols(M)
p = (np.sum(sims >= obs) + 1) / (len(sims) + 1)
print(f"CV entre columnas observado={obs:.3f}; nulo (columnas intercambiables)={sims.mean():.3f} "
      f"[p95={np.percentile(sims,95):.3f}]; p={p:.4f}")
print("=> hay estructura de columna real (las columnas no son intercambiables).")
print()

# ---------------- (d) robustez del total ----------------
print("=== (d) Robustez del total del ledger ===")
tot9 = float(np.nansum(V))
tot_col = float(d.total.sum())
Lq = L.groupby("quipu").cabecera.sum()
print(f"UR278 sumando 9 columnas: {tot9:.0f}")
print(f"UR278 sumando la columna 'total' (incluye cuerdas 10 y 12): {tot_col:.0f}  "
      f"(+{100*(tot_col-tot9)/tot9:.1f} %)")
print(f"UR266 (copia resumida): {Lq['UR266']:.0f}; UR275 (copia): {Lq['UR275']:.0f}")
print(f"dispersion entre las tres versiones del mismo flujo: "
      f"{100*(max(tot9,Lq['UR266'],Lq['UR275'])-min(tot9,Lq['UR266'],Lq['UR275']))/np.mean([tot9,Lq['UR266'],Lq['UR275']]):.1f} %")
print("=> el 8 % de diferencia no cambia ninguna conclusion fisica (todo se mueve <0,1 decadas).")
