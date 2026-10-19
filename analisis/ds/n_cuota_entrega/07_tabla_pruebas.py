"""Tabla única de pruebas primarias con Holm y BH sobre TODAS ellas.

Los p-values se leen de los CSV de salida cuando existen; los pocos que solo se
imprimen en los .txt se transcriben con su fuente indicada.
Salida: pruebas_primarias.csv, salida_07.txt
"""
import numpy as np
import pandas as pd
from scipy.stats import false_discovery_control

import lib_cuota as L

g = pd.read_csv("pruebas_globales.csv")
qm = pd.read_csv("pruebas_quipu.csv")
mag = pd.read_csv("control_magnitud.csv")
ps = pd.read_csv("p_vs_s1.csv")

T = []
for _, r in g.iterrows():
    T.append(dict(bloque="Incahuasi global (nulo intercambio)",
                  prueba=f"P vs S1: {r.prueba}", estadistico=round(float(r.observado), 4),
                  p=float(r.p_perm), fuente="pruebas_globales.csv"))
for _, r in qm.iterrows():
    T.append(dict(bloque="Incahuasi nivel quipu (signos)",
                  prueba=f"P vs S1: {r.prueba}", estadistico=round(float(r.media), 4),
                  p=float(r.p_signos), fuente="pruebas_quipu.csv"))
for _, r in mag.iterrows():
    T.append(dict(bloque="Control de magnitud (misma década)",
                  prueba=f"P vs S1: {r.prueba}", estadistico=round(float(r.dif_obs), 4),
                  p=float(r.p_mcnemar), fuente="control_magnitud.csv"))

extra = [
    ("Logit redondez10 rol + log10(valor) + EF quipu", 0.2826, 0.2348, "salida_01.txt"),
    ("Incahuasi sin UR270: redondez10", 0.0307, 0.1842, "salida_06.txt"),
    ("Mismo color P/S1: McNemar redondez10", 0.0, 1.0, "salida_06.txt"),
    ("UR270 SS_col del cociente S1/P", 0.495, 0.00010, "salida_02.txt"),
    ("UR270 split-half del cociente S1/P (Pearson)", 0.952, 0.00050, "salida_02.txt"),
    ("UR270 Friedman del cociente S1/P (rangos)", 8.937, 0.11162, "salida_02.txt"),
    ("UR270 sin columna 8: SS_col del cociente", 0.160, np.nan, "salida_02.txt"),
    ("UR270->UR278 con P", 11, 1.0, "salida_03.txt"),
    ("UR270->UR278 con S1", 4, 0.652669, "salida_03.txt"),
    ("UR270->UR278 con P+S1", 51, 0.0002, "salida_03.txt"),
    ("UR270 P = cabecera parte B (exactas)", 4, 0.0004, "salida_03.txt"),
    ("UR270 S1 = cabecera parte A (exactas)", 1, 0.1142, "salida_03.txt"),
    ("Control 20 quipus: redondez10", 0.02846, 0.10774, "salida_04.txt"),
    ("Control 20 quipus: redondez50", 0.03605, 0.00050, "salida_04.txt"),
    ("Control 20 quipus: redondez100", 0.00569, 0.18909, "salida_04.txt"),
    ("Control 20 quipus: igualdades", -0.04231, 0.99900, "salida_04.txt"),
    ("Control 20 quipus: CV plano", 0.02077, 0.38033, "salida_04.txt"),
    ("Incahuasi vs control: redondez10", 0.03725, 0.67617, "salida_04.txt"),
    ("Incahuasi vs control: igualdades", 0.08476, 0.07755, "salida_04.txt"),
    ("Incahuasi vs control: CV plano", 0.08235, 0.41633, "salida_04.txt"),
    ("JC (Sector B): CV plano", 0.17546, 0.01680, "salida_04.txt"),
    ("UR270: P más estable por columna que S1 (CV col)", 0.299, np.nan, "salida_06.txt"),
    ("UR270 g6 único grupo 100/200 entre 142 grupos (post hoc)", 1.0, 1 / 142, "consulta directa"),
]
for nom, est, p, fuente in extra:
    T.append(dict(bloque="Otras pruebas primarias", prueba=nom,
                  estadistico=est, p=p, fuente=fuente))
R = pd.DataFrame(T)
R["p_holm"] = L.holm(R.p.values)
R["p_bh"] = false_discovery_control(np.where(np.isnan(R.p.values), 1.0, R.p.values))
R = R.sort_values("p")
R.to_csv("pruebas_primarias.csv", index=False)
with open("salida_07.txt", "w", encoding="utf-8") as f:
    f.write(R.round(6).to_string(index=False) + "\n")
print(R.round(5).to_string(index=False))
print("\nsobreviven Holm:", int((R.p_holm < 0.05).sum()), "de", len(R))
