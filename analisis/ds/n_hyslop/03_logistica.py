# -*- coding: utf-8 -*-
"""
Puente cuantitativo entre el deposito de Inkawasi y la gente que pudo
habitarlo/consumirlo. No introduce datos nuevos: usa la capacidad de
Hyslop/Urton & Chu y los escenarios de mano de obra de n_almacenes.

Salidas: logistica.csv, salida_03.txt
"""
import csv
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
NALM = BASE.parent / "n_almacenes"

# ---------------------------------------------------------------------------
# 1. Escenarios de mit'a de n_almacenes (costal de 25 kg, el que usa su informe)
# ---------------------------------------------------------------------------
m = pd.read_csv(NALM / "mita_escenarios.csv")
m = m[m.unidad == "costal_25"].copy()
m["trab_total_p5"] = 9 * m.trab_p5
m["trab_total_mediana"] = 9 * m.trab_mediana
m["trab_total_p95"] = 9 * m.trab_p95
m = m[["cultivo", "kg_unidad", "total_t", "t_por_grupo",
       "trab_total_p5", "trab_total_mediana", "trab_total_p95"]]
m.to_csv(BASE / "logistica_mita.csv", index=False, encoding="utf-8")

# ---------------------------------------------------------------------------
# 2. Personas-dia que puede sostener el deposito
# ---------------------------------------------------------------------------
def person_days(vol_m3, density_t_m3, ration_kg_day):
    tonnes = vol_m3 * density_t_m3
    return tonnes * 1000 / ration_kg_day

escenarios = []
for vol, nombre in [(6400, "S1_6400"), (10876, "S3_10876"), (16200, "S4_16200")]:
    for dens in (0.4, 0.7):
        for racion in (0.7, 1.5):
            pd_ = person_days(vol, dens, racion)
            escenarios.append(dict(
                volumen_m3=vol, escenario=nombre, densidad_t_m3=dens,
                racion_kg_dia=racion, toneladas=vol * dens,
                personas_dia=pd_,
                hombres_10000_dias=pd_ / 10000,
                hombres_20000_dias=pd_ / 20000,
            ))
with open(BASE / "logistica.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(escenarios[0].keys()))
    w.writeheader()
    w.writerows(escenarios)

# ---------------------------------------------------------------------------
# 3. Almacenaje por 1000 habitantes (referencia LeVine 1992, tabla 4-4)
# ---------------------------------------------------------------------------
ref = {"Pumpu": 605, "Huanuco Pampa": 705, "Xauxa": 780}
percap = []
for vol in (6400, 10876, 16200):
    for pob in (1000, 2000):
        percap.append(dict(volumen_m3=vol, poblacion=pob,
                           m3_por_1000=1000 * vol / pob,
                           veces_sobre_605=(1000 * vol / pob) / 605,
                           veces_sobre_780=(1000 * vol / pob) / 780))

lines = []
lines.append("MIT'A (costal 25 kg; trabajadores totales = 9 grupos)")
for _, row in m.iterrows():
    lines.append("  %-14s p5=%5.0f  mediana=%5.0f  p95=%5.0f" % (
        row.cultivo, row.trab_total_p5, row.trab_total_mediana, row.trab_total_p95))
lines.append("")
lines.append("PERSONAS-DIA DEL DEPOSITO (0,4-0,7 t/m3; 0,7-1,5 kg/dia)")
for vol, nombre in [(6400, "S1"), (16200, "S4")]:
    vals = [e for e in escenarios if e["volumen_m3"] == vol]
    lo = min(e["personas_dia"] for e in vals)
    hi = max(e["personas_dia"] for e in vals)
    lines.append("  %s: %.2f-%.2f millones de personas-dia; 10.000 hombres %.0f-%.0f dias; 20.000 %.0f-%.0f dias" % (
        nombre, lo / 1e6, hi / 1e6,
        lo / 10000, hi / 10000, lo / 20000, hi / 20000))
lines.append("")
lines.append("ALMACENAJE POR 1000 HABITANTES")
for r in percap:
    lines.append("  %5d m3 / %4d hab = %6.0f m3/1000; %.1f-%.1f x la sierra" % (
        r["volumen_m3"], r["poblacion"], r["m3_por_1000"],
        r["veces_sobre_780"], r["veces_sobre_605"]))

(BASE / "salida_03.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
