# -*- coding: utf-8 -*-
"""02. Prueba de capacidad fisica: cuantas unidades de cada tipo caben en Qolqawasi
y que fraccion del deposito representaria el archivo.

Unidad de analisis: el quipu/ledger (no la cuerda). No hay test de significacion
posible con n=1 ledger: se hacen intervalos por Monte Carlo sobre los supuestos
fisicos y un contraste de coincidencia (que probabilidad hay de que un tamano de
unidad cualquiera caiga dentro de un factor 2 de la capacidad).
"""
import numpy as np, pandas as pd
from comun import (leer_ur278, leer_libro, VOL_SITIO_M3, N_UNIDADES, DENS,
                   UNIDADES, RNG, CUADROS_UA07)

d, cols = leer_ur278()
LEDGER_FLUJO = float(np.nansum(d[cols].values))      # 61 790
L = leer_libro()
LEDGER_MAESTRO = float(L[L.quipu == "UR269"].cabecera.sum())   # 122 609
N_REG_FLUJO = len(d)
N_REG_MAESTRO = int((L.quipu == "UR269").sum())

# Cuarto nivel: UR268, maximos por grupo (30 grupos con valor)
_c = pd.read_csv("../../datos/cuerdas.csv")
_q = _c[(_c.kfg == "UR268") & (_c.nivel == 0)].copy()
_q["v"] = pd.to_numeric(_q.valor, errors="coerce")
LEDGER_PERIODO = float(_q.groupby("grupo").v.max().sum())      # 300 378
LEDGERS = {
    "registro (una entrega, media)": 2207.0,
    "flujo 47 (UR278, 9 col.)": LEDGER_FLUJO,
    "maestro UR269 (67 reg.)": LEDGER_MAESTRO,
    "periodos UR268 (30 reg.)": LEDGER_PERIODO,
}
print(f"UR278 (flujo 47): {LEDGER_FLUJO:.0f} unidades en {N_REG_FLUJO} registros")
print(f"UR269 (libro maestro): {LEDGER_MAESTRO:.0f} unidades en {N_REG_MAESTRO} registros, ~12 bloques")
print(f"UR268 (nivel de periodo): {LEDGER_PERIODO:.0f} unidades en 30 grupos")
print(f"Qolqawasi: {VOL_SITIO_M3:.0f} m3 en {N_UNIDADES} unidades (36 camaras + 209 colcas); "
      f"media {VOL_SITIO_M3/N_UNIDADES:.1f} m3/unidad")
print()

# ---------- 1. Capacidad en masa y en volumen ----------
print("=== 1. Capacidad fisica del deposito ===")
dens_lo, dens_hi = 0.40, 0.70     # mezcla de productos, incluido mani en cascara
cap_t_lo, cap_t_hi = VOL_SITIO_M3 * dens_lo, VOL_SITIO_M3 * dens_hi
print(f"masa almacenable = 6 400 m3 x densidad aparente 0,40-0,70 t/m3 = "
      f"{cap_t_lo:,.0f}-{cap_t_hi:,.0f} t")
for prod, (lo, hi) in DENS.items():
    print(f"   si todo fuera {prod:13s}: {VOL_SITIO_M3*lo:,.0f}-{VOL_SITIO_M3*hi:,.0f} t")
print()

# ---------- 2. Escenarios de unidad ----------
print("=== 2. Masa y volumen del ledger segun la unidad ===")
filas = []
for nombre, (kmin, kmax, lmin, lmax) in UNIDADES.items():
    for etiqueta, ledger in LEDGERS.items():
        m_lo, m_hi = ledger * kmin / 1000, ledger * kmax / 1000        # t
        v_lo, v_hi = ledger * lmin / 1000, ledger * lmax / 1000        # m3
        filas.append(dict(unidad=nombre, ledger=etiqueta, n=ledger,
                          t_min=m_lo, t_max=m_hi, m3_min=v_lo, m3_max=v_hi,
                          pct_cap_vol_min=100 * v_lo / VOL_SITIO_M3,
                          pct_cap_vol_max=100 * v_hi / VOL_SITIO_M3,
                          llenados_min=m_lo / cap_t_hi, llenados_max=m_hi / cap_t_lo))
T = pd.DataFrame(filas)
pd.set_option("display.width", 200)
print(T.round(3).to_string(index=False))
T.to_csv("capacidad_escenarios.csv", index=False)
print()

# ---------- 3. Cuantos "periodos" harian falta para llenar el deposito ----------
print("=== 3. Numero de ledgers necesarios para llenar Qolqawasi (masa) ===")
for nombre in ["racion_persona_dia", "arroba", "carga_llama", "costal_25", "fanega", "costal_50"]:
    kmin, kmax, _, _ = UNIDADES[nombre]
    k = (kmin + kmax) / 2
    n_lleno = cap_t_lo * 1000 / k, cap_t_hi * 1000 / k
    print(f"{nombre:20s} ({k:4.1f} kg): caben {n_lleno[0]:,.0f}-{n_lleno[1]:,.0f} unidades; "
          f"el ledger maestro es el {100*LEDGER_MAESTRO/n_lleno[1]:.2f}-{100*LEDGER_MAESTRO/n_lleno[0]:.2f} % del deposito")
print()

# ---------- 4. Cota inferior de la masa unitaria segun el periodo cubierto ----------
print("=== 4. Cota inferior de la masa unitaria (kg) para que el archivo quepa ===")
print("supuesto: el ledger es TODO lo que paso por el deposito en T anios")
print("y el deposito estaba razonablemente lleno (2 560-4 480 t)")
print(f"{'T':>5s} {'L3 UR269 (122 609)':>22s} {'L4 UR268 (300 378)':>22s}")
for T_anios in [1, 2, 2.5, 5, 10, 20]:
    lo3 = cap_t_lo * 1000 / (LEDGER_MAESTRO * T_anios)
    lo4 = cap_t_lo * 1000 / (LEDGER_PERIODO * T_anios)
    print(f"{T_anios:5.1f} {lo3:17.2f} kg {lo4:17.2f} kg")
print("   (cota con la densidad MINIMA 0,40 t/m3; con 0,55-0,70 sube 1,4-1,75x)")
print()

# ---------- 5. Contraste de coincidencia (nulo) ----------
print("=== 5. Que significa la coincidencia 'ledger ~ 1 llenado' ===")
print("Nulo: el tamano de la unidad es desconocido y log-uniforme entre 5e-5 y 0,5 m3 (4 decadas).")
def p_factor(ledger, factor=2.0, vmin=5e-5, vmax=0.5):
    lo = VOL_SITIO_M3 / factor / ledger
    hi = VOL_SITIO_M3 * factor / ledger
    lo, hi = max(lo, vmin), min(hi, vmax)
    if hi <= lo:
        return 0.0
    return np.log10(hi / lo) / np.log10(vmax / vmin)
for factor in [1.25, 1.5, 2.0, 3.0]:
    print(f"   P(volumen del ledger dentro de un factor {factor:.2f} de la capacidad) = "
          f"{p_factor(LEDGER_MAESTRO, factor):.3f}   (flujo 47: {p_factor(LEDGER_FLUJO, factor):.3f})")
print("   => la coincidencia NO es significativa por si sola; solo sirve para excluir")
print("      unidades que se alejan ordenes de magnitud (items, raciones).")
print()

# ---------- 6. Cuadricula de 23 x 23 cm como regla fisica ----------
print("=== 6. La unica regla fisica del sitio: 3 510 cuadros de 23 x 23 cm (U.A. 07) ===")
area = 0.23 ** 2
for prof in [0.03, 0.05, 0.10, 0.20]:
    vol = area * prof
    print(f"   capa de {prof*100:4.0f} cm -> {vol*1000:5.1f} L por cuadro; "
          f"maiz {vol*0.75*1000:5.1f} kg, mani en cascara {vol*0.25*1000:5.1f} kg")
print(f"   61 790 unidades / 3 510 cuadros = {LEDGER_FLUJO/CUADROS_UA07:.1f} cuadros por unidad registrada")
print(f"   (si 1 cuadro = 1 unidad, el ledger del flujo son {LEDGER_FLUJO/CUADROS_UA07:.1f} 'vueltas' de la cuadricula)")
print()

# ---------- 7. Logistica de caravana ----------
print("=== 7. Logistica: cargas de llama necesarias ===")
for nombre, kg in [("racion 0,7 kg", 0.7), ("arroba 11,5", 11.5), ("carga 25", 25.0), ("fanega 43", 43.0)]:
    cargas_reg = 2207 * kg / 25          # registro medio del flujo (2 207 u.)
    cargas_dia = LEDGER_MAESTRO * kg / 25 / 365
    print(f"   {nombre:14s}: registro medio = {cargas_reg:7.1f} cargas de 25 kg; "
          f"ledger maestro = {LEDGER_MAESTRO*kg/1000:7.1f} t = {cargas_dia:7.1f} cargas/dia si es 1 anio")
print()

# ---------- 8. Raciones: dias de guarnicion ----------
print("=== 8. Si la unidad fuera una racion-persona-dia ===")
for guarnicion in [1000, 5000, 10000]:
    dias = LEDGER_MAESTRO / guarnicion
    cap_dias = cap_t_lo * 1000 / 0.7 / guarnicion
    print(f"   guarnicion {guarnicion:5d}: el ledger maestro = {dias:5.1f} dias; "
          f"el deposito lleno = {cap_dias:6.0f} dias ({cap_dias/365:.1f} anios)")
print()

print("OK -> capacidad_escenarios.csv")
