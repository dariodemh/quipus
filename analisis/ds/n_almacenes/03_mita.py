# -*- coding: utf-8 -*-
"""03. Si las 9 columnas fueran grupos de trabajo (mit'a) o depositos:
que fuerza laboral / que volumen implica cada unidad?

Monte Carlo sobre supuestos agronomicos (rendimiento por jornal y duracion de
la temporada) para dar intervalos, no puntos.
"""
import numpy as np, pandas as pd
from comun import leer_ur278, RNG, VOL_SITIO_M3, N_CAMARAS, UNIDADES

d, cols = leer_ur278()
N = float(np.nansum(d[cols].values))   # 61 790
V = d[cols].values.astype(float)
col_tot = np.nansum(V, axis=0)
print(f"UR278: {N:.0f} unidades, 28 registros, 9 columnas")
print(f"por columna (total del ledger): {col_tot.min():.0f}-{col_tot.max():.0f} u. "
      f"(media {col_tot.mean():.0f})")
print()

# ---------- 1. Escenario "9 grupos de trabajo" ----------
print("=== 1. Si las 9 columnas son 9 cuadrillas de mit'a ===")
# rendimiento por jornal (kg de producto por persona-dia), rangos por cultivo
REND = {
    "maiz (grano)":     (100, 300),
    "frijol":           (60, 150),
    "mani (vaina)":     (30, 80),
    "aji (seco)":       (8, 25),
    "papa/chuno":       (300, 600),
}
TEMPORADA = (20, 60)   # dias de campana
filas = []
for u in ["racion_persona_dia", "arroba", "carga_llama", "costal_25", "fanega", "costal_50"]:
    kmin, kmax, _, _ = UNIDADES[u]
    kg = (kmin + kmax) / 2
    total_t = N * kg / 1000
    por_grupo = total_t / 9
    for cultivo, (rmin, rmax) in REND.items():
        # simulacion: rendimiento ~ U(rmin,rmax), temporada ~ U(TEMPORADA)
        rr = RNG.uniform(rmin, rmax, 20000)
        tt = RNG.uniform(*TEMPORADA, 20000)
        trabajadores = por_grupo * 1000 / (rr * tt)
        filas.append(dict(unidad=u, kg_unidad=kg, total_t=total_t, t_por_grupo=por_grupo,
                          cultivo=cultivo, trab_p5=np.percentile(trabajadores, 5),
                          trab_mediana=np.median(trabajadores),
                          trab_p95=np.percentile(trabajadores, 95)))
M = pd.DataFrame(filas)
pd.set_option("display.width", 220)
print(M[M.unidad.isin(["racion_persona_dia", "costal_25", "fanega"])]
      .round(1).to_string(index=False))
M.to_csv("mita_escenarios.csv", index=False)
print()
print("Lectura: trabajadores por cuadrilla (mediana, p5-p95) para costal de 25 kg:")
for _, r in M[(M.unidad == "costal_25")].iterrows():
    print(f"   {r.cultivo:16s}: {r.trab_mediana:6.0f} ({r.trab_p5:5.0f}-{r.trab_p95:5.0f})")
print()
print("La misma cuenta con racion de 0,7 kg da cuadrillas de:")
for _, r in M[(M.unidad == "racion_persona_dia")].iterrows():
    print(f"   {r.cultivo:16s}: {r.trab_mediana:6.1f} ({r.trab_p5:5.1f}-{r.trab_p95:5.1f}) trabajadores")
print()

# ---------- 2. Escenario "9 depositos" ----------
print("=== 2. Si las 9 columnas son 9 depositos ===")
cap_util = VOL_SITIO_M3 * 0.85           # volumen util (pasillos, muros, altura de carga)
camara_m3 = cap_util / N_CAMARAS
print(f"volumen util estimado {cap_util:.0f} m3; si las 9 columnas son las camaras grandes, "
      f"{camara_m3:.0f} m3 por camara")
for u in ["arroba", "carga_llama", "costal_25", "fanega"]:
    kmin, kmax, lmin, lmax = UNIDADES[u]
    l = (lmin + lmax) / 2000            # m3 por unidad
    for nombre_col, tot in [("columna menor", col_tot.min()), ("columna mayor", col_tot.max())]:
        print(f"   {u:12s} ({l*1000:4.1f} L): {nombre_col} = {tot:5.0f} u. = "
              f"{tot*l:6.1f} m3 = {tot*l/camara_m3:4.1f} camaras")
print()

# ---------- 3. Jornal por grupo y por dia ----------
print("=== 3. Ritmo diario implicado (temporada de 30-60 dias) ===")
for u in ["racion_persona_dia", "costal_25", "fanega"]:
    kmin, kmax, _, _ = UNIDADES[u]
    kg = (kmin + kmax) / 2
    for dias in [30, 60]:
        t_dia = N * kg / 1000 / 9 / dias
        print(f"   {u:20s}: {t_dia:6.2f} t por grupo y dia en una temporada de {dias} dias")
print()

# ---------- 4. Contraste con la capacidad (llenados por ledger) ----------
print("=== 4. Coherencia con la rotacion del deposito ===")
cap_t = VOL_SITIO_M3 * np.array([0.40, 0.55, 0.70])
for u in ["arroba", "carga_llama", "costal_25", "fanega", "costal_50"]:
    kmin, kmax, _, _ = UNIDADES[u]
    kg = (kmin + kmax) / 2
    t = N * kg / 1000
    print(f"   {u:12s}: ledger del flujo = {t:7.0f} t = {t/cap_t[2]:.2f}-{t/cap_t[0]:.2f} "
          f"del deposito; si el ledger es 1 anio, rotacion {t/cap_t[2]:.1f}-{t/cap_t[0]:.1f}/anio")
print()
print("OK -> mita_escenarios.csv")
