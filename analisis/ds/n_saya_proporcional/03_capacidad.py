# -*- coding: utf-8 -*-
"""
03_capacidad.py -- Prueba B: capacidad de Inkawasi con los datos de Hyslop/Snead
(LeVine 1992): 202 cuartos documentados (250 estimados), lado 3,5-4 m,
altura 2-3,5 m, llenado 40-80 %.

Calcula:
  - volumen bruto y ocupado del sitio;
  - intervalo admisible de volumen por unidad si todo un ledger se almacena
    a la vez (cota inferior y superior);
  - comparacion con fanega (56 L) y saco (30-55 L);
  - tabla de escenarios actualizada;
  - probabilidad de compatibilidad bajo supuestos uniformes y descomposicion
    exacta de la incertidumbre en log-volumen.

Salidas: capacidad_inkawasi.csv, escenarios_unidad.csv,
         incertidumbre_capacidad.csv, salida_03.txt
"""
import json
import numpy as np
import pandas as pd

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)
OUT = "analisis/ds/n_saya_proporcional"

# ---------------------------------------------------------------- parametros
CASOS = [(202, "documentados"), (250, "estimados")]
LADO = (3.5, 4.0)
ALTO = (2.0, 3.5)
LLEN = (0.40, 0.80)
FANEGA_L = 56.0
SACO = (30.0, 55.0)

LEDGERS = [
    ("UR278 (flujo 47, libro completo)", 61790, "L2"),
    ("UR266 (copia resumida)", 56986, "L2b"),
    ("UR269 (libro maestro)", 122609, "L3"),
    ("UR268 (nivel de periodo)", 300378, "L4"),
]

# ---------------------------------------------------------------- volumen
filas = []
for nr, et in CASOS:
    for lado in LADO:
        for alto in ALTO:
            bruto = nr * lado ** 2 * alto
            filas.append({"cuartos": nr, "tipo": et, "lado_m": lado,
                          "alto_m": alto, "bruto_m3": bruto,
                          "ocupado_40_m3": 0.40 * bruto,
                          "ocupado_80_m3": 0.80 * bruto})
cap = pd.DataFrame(filas)
cap_resumen = cap.groupby(["cuartos", "tipo"]).agg(
    bruto_min=("bruto_m3", "min"), bruto_max=("bruto_m3", "max"),
    ocup_min=("ocupado_40_m3", "min"), ocup_max=("ocupado_80_m3", "max")).reset_index()
cap_resumen["factor_max_min"] = cap_resumen.ocup_max / cap_resumen.ocup_min
cap_resumen.to_csv(f"{OUT}/capacidad_inkawasi.csv", index=False)

# ---------------------------------------------------------------- por unidad
adm = []
for nombre, N, nivel in LEDGERS:
    for _, r in cap_resumen.iterrows():
        adm.append({"ledger": nombre, "nivel": nivel, "N": N,
                    "cuartos": int(r.cuartos),
                    "v_min_L": 1000 * r.ocup_min / N,
                    "v_max_L": 1000 * r.ocup_max / N,
                    "factor": r.ocup_max / r.ocup_min})
adm = pd.DataFrame(adm)

# ---------------------------------------------------------------- escenarios
unidades = [
    ("item suelto (grano)", 0.001, 0.05, 0.0005, 0.05),
    ("racion persona-dia (0,7 kg)", 1.0, 1.75, 0.7, 0.7),
    ("cuadro 23x23 cm (capa 3-10 cm)", 1.6, 5.3, 0.4, 4.2),
    ("arroba (11,5 kg)", 15.5, 15.5, 11.5, 11.5),
    ("saco 30 L", 30.0, 30.0, 7.0, 24.0),
    ("costal 25 kg (34,5 L)", 34.5, 34.5, 25.0, 25.0),
    ("carga de llama (30-40 L)", 30.0, 40.0, 23.0, 30.0),
    ("saco 40 L", 40.0, 40.0, 9.0, 32.0),
    ("saco 55 L", 55.0, 55.0, 11.0, 44.0),
    ("fanega (56 L)", FANEGA_L, FANEGA_L, 14.0, 44.0),
    ("costal 50 kg (69 L)", 69.0, 69.0, 50.0, 50.0),
]

# Monte Carlo de la capacidad bajo supuestos uniformes
B = 200000
cuartos_s = rng.uniform(202, 250, B)
lado_s = rng.uniform(*LADO, B)
alto_s = rng.uniform(*ALTO, B)
llen_s = rng.uniform(*LLEN, B)
cap_bruta_s = cuartos_s * lado_s ** 2 * alto_s
cap_s = cap_bruta_s * llen_s

esc = []
for nombre, vmin, vmax, mmin, mmax in unidades:
    fila = {"unidad": nombre, "L_min": vmin, "L_max": vmax,
            "kg_min": mmin, "kg_max": mmax}
    for lnombre, N, nivel in LEDGERS:
        dem_min = N * vmin / 1000.0
        dem_max = N * vmax / 1000.0
        # probabilidad de que el sitio sea lo bastante grande (cota superior)
        fila[f"p_cabe_{nivel}"] = float(np.mean(cap_s >= dem_max))
        # compatibilidad de dos lados: 40 % <= N*v <= 80 % del volumen bruto
        fila[f"p_compatible_{nivel}"] = float(np.mean(
            (0.40 * cap_bruta_s <= dem_max) & (0.80 * cap_bruta_s >= dem_min)))
        fila[f"pct_cap_{nivel}"] = 100 * dem_max / np.median(cap_s)
    # veredicto para UR278
    lo = adm[(adm.ledger.str.startswith("UR278")) & (adm.cuartos == 202)].v_min_L.iloc[0]
    hi = adm[(adm.ledger.str.startswith("UR278")) & (adm.cuartos == 250)].v_max_L.iloc[0]
    fila["dentro_UR278"] = bool(vmax >= lo and vmin <= hi)
    fila["v_mediana_UR278"] = float(np.median(cap_s / 61790 * 1000))
    esc.append(fila)
esc = pd.DataFrame(esc)
esc.to_csv(f"{OUT}/escenarios_unidad.csv", index=False)

# ---------------------------------------------------------------- incertidumbre
def var_log_uniforme(a, b):
    return (np.log(b / a)) ** 2 / 12

v_cuartos = var_log_uniforme(202, 250)
v_lado = 4 * var_log_uniforme(*LADO)   # lado^2
v_alto = var_log_uniforme(*ALTO)
v_llen = var_log_uniforme(*LLEN)
total_sin_N = v_cuartos + v_lado + v_alto + v_llen

# con eleccion de ledger uniforme entre L2, L3 y L4
Ns = np.array([61790.0, 122609.0, 300378.0])
v_N = float(np.var(np.log(Ns), ddof=0))
total_con_N = total_sin_N + v_N

inc = pd.DataFrame([
    {"supuesto": "llenado (40-80 %)", "var_log": v_llen,
     "pct_sin_N": 100 * v_llen / total_sin_N, "pct_con_N": 100 * v_llen / total_con_N},
    {"supuesto": "altura (2-3,5 m)", "var_log": v_alto,
     "pct_sin_N": 100 * v_alto / total_sin_N, "pct_con_N": 100 * v_alto / total_con_N},
    {"supuesto": "lado (3,5-4 m)", "var_log": v_lado,
     "pct_sin_N": 100 * v_lado / total_sin_N, "pct_con_N": 100 * v_lado / total_con_N},
    {"supuesto": "cuartos (202-250)", "var_log": v_cuartos,
     "pct_sin_N": 100 * v_cuartos / total_sin_N, "pct_con_N": 100 * v_cuartos / total_con_N},
    {"supuesto": "que ledger se almacena a la vez", "var_log": v_N,
     "pct_sin_N": 0.0, "pct_con_N": 100 * v_N / total_con_N},
])
inc.to_csv(f"{OUT}/incertidumbre_capacidad.csv", index=False)

# ---------------------------------------------------------------- comparaciones
cap_mid = float(np.median(cap_s))
fanegas = cap_s / 0.056
res = {
    "cap_resumen": cap_resumen.to_dict(orient="records"),
    "adm": adm.to_dict(orient="records"),
    "cap_mediana_m3": cap_mid,
    "cap_p05_m3": float(np.quantile(cap_s, 0.05)),
    "cap_p95_m3": float(np.quantile(cap_s, 0.95)),
    "v_ur278_mediana_L": float(np.median(cap_s / 61790 * 1000)),
    "v_ur278_p05_L": float(np.quantile(cap_s / 61790 * 1000, 0.05)),
    "v_ur278_p95_L": float(np.quantile(cap_s / 61790 * 1000, 0.95)),
    "v_ur269_mediana_L": float(np.median(cap_s / 122609 * 1000)),
    "v_ur268_mediana_L": float(np.median(cap_s / 300378 * 1000)),
    "p_fanega_ur278": float(np.mean(cap_s >= 61790 * 0.056)),
    "p_saco55_ur278": float(np.mean(cap_s >= 61790 * 0.055)),
    "p_saco30_ur278": float(np.mean(cap_s >= 61790 * 0.030)),
    "p_fanega_ur268": float(np.mean(cap_s >= 300378 * 0.056)),
    "p_saco30_ur268": float(np.mean(cap_s >= 300378 * 0.030)),
    "p_cap_6400": float(np.mean(cap_s <= 6400)),
    "p_ur278_v_103_6": float(np.mean(cap_s / 61790 * 1000 <= 103.6)),
    "fanegas_p05": float(np.quantile(fanegas, 0.05)),
    "fanegas_mediana": float(np.median(fanegas)),
    "fanegas_p95": float(np.quantile(fanegas, 0.95)),
    "inc": inc.to_dict(orient="records"),
}
json.dump(res, open(f"{OUT}/resultados_03.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- imprimir
L = []
L.append("=== Capacidad de Inkawasi (Hyslop/Snead en LeVine 1992) ===")
L.append("202 cuartos documentados, 250 estimados; lado 3,5-4 m; alto 2-3,5 m; llenado 40-80 %")
L.append(cap_resumen.to_string(index=False, float_format=lambda z: f"{z:.0f}"))
L.append(f"Capacidad ocupada (mediana MC): {cap_mid:.0f} m3; IC90 {res['cap_p05_m3']:.0f}-{res['cap_p95_m3']:.0f} m3")
L.append("")
L.append("=== Volumen admisible por unidad si TODO el ledger se almacena a la vez ===")
L.append(adm.pivot_table(index=["ledger", "N"], columns="cuartos",
                         values=["v_min_L", "v_max_L"]).to_string(float_format=lambda z: f"{z:.1f}"))
L.append("")
L.append("=== Comparacion con fanega (56 L) y saco (30-55 L) ===")
L.append(f"UR278: volumen implicado mediana {res['v_ur278_mediana_L']:.1f} L (IC90 {res['v_ur278_p05_L']:.1f}-{res['v_ur278_p95_L']:.1f})")
L.append(f"  P(cabe la fanega de 56 L) = {res['p_fanega_ur278']:.3f}")
L.append(f"  P(cabe un saco de 55 L)   = {res['p_saco55_ur278']:.3f}")
L.append(f"  P(cabe un saco de 30 L)   = {res['p_saco30_ur278']:.3f}")
L.append(f"UR268 (300 378): mediana {res['v_ur268_mediana_L']:.1f} L; P(fanega) = {res['p_fanega_ur268']:.3f}; P(saco 30 L) = {res['p_saco30_ur268']:.3f}")
L.append(f"Fanegas que caben en el sitio: mediana {res['fanegas_mediana']:.0f} (IC90 {res['fanegas_p05']:.0f}-{res['fanegas_p95']:.0f})")
L.append("")
L.append("=== Escenarios de unidad (actualizacion de n_almacenes) ===")
L.append(esc[["unidad", "L_min", "L_max", "kg_min", "kg_max",
              "pct_cap_L2", "pct_cap_L3", "pct_cap_L4",
              "p_compatible_L2", "p_compatible_L3", "p_compatible_L4",
              "dentro_UR278"]].to_string(index=False, float_format=lambda z: f"{z:.3g}"))
L.append("")
L.append(f"El punto de 6 400 m3 de n_almacenes cae en el percentil {100*res['p_cap_6400']:.0f} de la capacidad nueva.")
L.append(f"El volumen unitario implicado de 103,6 L (UR278 con 6 400 m3) cae en el percentil {100*res['p_ur278_v_103_6']:.0f}.")
L.append("")
L.append("=== Descomposicion de la incertidumbre (varianza de log volumen) ===")
L.append(inc.to_string(index=False, float_format=lambda z: f"{z:.4f}"))
L.append(f"Varianza total sin elegir ledger: {total_sin_N:.4f}; con ledger: {total_con_N:.4f}")

txt = "\n".join(L)
open(f"{OUT}/salida_03.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
