# -*- coding: utf-8 -*-
"""
Inkawasi (Hyslop 1985) + Qolqawasi (Urton & Chu 2015):
sectores, cuartos de almacén, capacidad y distribución espacial de los quipus.

Fuentes primarias (solo se leen, no se copian):
  analisis/fuentes_txt/Hyslop1985_Inkawasi.txt
  analisis/fuentes_txt/Accounting_in_the_Kings_Storehouse_The_I.txt
  analisis/fuentes_txt/UrtonChu2015_suplemento.txt
  analisis/fuentes_txt/InkaHistoryinKnotsReadingKhipusas.txt (2017)
  analisis/fuentes_txt/LeVine1992_InkaStorageSystems.txt
Salidas: sectores.csv, quipus_ua.csv, capacidad_escenarios.csv, salida_01.txt
"""
import csv
import re
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
FT = BASE.parent.parent / "fuentes_txt"
SEED = 20261018

# ---------------------------------------------------------------------------
# 1. Sectores (Hyslop 1985, cap. 2; Urton & Chu 2015 para el desglose de A)
# ---------------------------------------------------------------------------
# Los conteos son los que el texto afirma explícitamente. Los rangos se
# conservan como texto para no fabricar una precisión que la fuente no tiene.
sectores = [
    dict(
        sector="A", subsector="Qolqawasi",
        funcion="Almacén estatal (depósito); recepción, conteo y almacenamiento",
        n_cuartos_almacen="202-250 bins cuadrados + 36 cámaras rectangulares",
        medidas="110 x 110 m; bins de 3,5-4,5 m de lado y ~2 m de alto",
        filas_columnas="Bins en 3 lados (NE, SE, SO); 36 cámaras = 2 filas de 9 por lado del eje (4x9); 4 kallankas + 2 secaderos al N",
        volumen_m3="6400 (A3, central; rango 5120-8465) + 0-5184 (A2) = 6400-11584; maximo geometrico 13649",
        evidencia="Hyslop 1985:98-102; Urton & Chu 2015:517-519",
        notas="Una sola entrada (NO); plataforma central; sin residencia; 1/3-1/2 de los cuartos del sitio serían almacén",
    ),
    dict(
        sector="A", subsector="A1",
        funcion="Recepción, contabilidad inicial y secado (kallankas + secaderos)",
        n_cuartos_almacen="4 kallankas + 2 secaderos",
        medidas="Kallankas rectangulares (U.A. 1,2,4,5); secaderos con 30 paneles de 3x39 cuadros de 23 cm = 3510 cuadros",
        filas_columnas="2 kallankas + 1 secadero por lado del corredor central U.A.3",
        volumen_m3="0 (no computado como almacén)",
        evidencia="Urton & Chu 2015:517-525; Urton 2017:156-159",
        notas="14 quipus con maní en la esquina SO de U.A.4; UR271 con frijol; 7 quipus en el corredor U.A.3",
    ),
    dict(
        sector="A", subsector="A2",
        funcion="Cámaras grandes (¿almacén o secado/conteo?)",
        n_cuartos_almacen="36",
        medidas="18 por lado; 9 exteriores más cortas en su eje largo y 9 interiores más largas",
        filas_columnas="2 filas de 9 por lado del eje central = 4x9",
        volumen_m3="0-5184 (si son almacén; supuesto 15x6 m x 1,3-1,6 m de carga)",
        evidencia="Urton & Chu 2015:517; Hyslop 1985:99-101",
        notas="Hyslop las llama '>=30 rectangular enclosures', sin techo, y duda de su función (secado/conteo); Urton & Chu las cuentan como storage bins. Conflicto interpretativo.",
    ),
    dict(
        sector="A", subsector="A3",
        funcion="Bins pequeños de almacén",
        n_cuartos_almacen="209 (Hyslop: 202-250)",
        medidas="3,5-4,5 m de lado y ~2 m de alto; 3 lados (O, S, E)",
        filas_columnas="Filas multiples en 3 lados; el texto no da el numero de filas por lado",
        volumen_m3="5120-8465; 6400 central (30,6 m3/bin)",
        evidencia="Hyslop 1985:98-102; Urton & Chu 2015:518",
        notas="6400/209 = 30,6 m3 por bin, exactamente dentro del rango 3,5-4,5 m x 2 m. 209 = 11x19, no multiple de 9.",
    ),
    dict(
        sector="B", subsector="-",
        funcion="Residencia de élite; posible templo de Wiracocha (Compound 1)",
        n_cuartos_almacen="0 (almacén ocasional en pocos cuartos)",
        medidas="200 x 100 m; muros de hasta 4 m; >=120 cuartos; 4-5 compuestos",
        filas_columnas="Compound 2 = residencia principal; Compound 1 = recinto sin subdividir de 45 m",
        volumen_m3="0",
        evidencia="Hyslop 1985:103-108",
        notas="Poyos, nichos, ventanas, cerámica carbonizada; sin evidencia de guarnición",
    ),
    dict(
        sector="C", subsector="-",
        funcion="Ceremonial: plaza trapezoidal, posible Templo del Sol, entierro, corrales",
        n_cuartos_almacen="0",
        medidas="110 x 100 m; ~25 cuartos; 11 recintos de 7-13 m; plaza con 20 columnas",
        filas_columnas="4 subdivisiones",
        volumen_m3="0",
        evidencia="Hyslop 1985:109-111",
        notas="Plaza secundaria al E de la principal; enterramiento; ocupación post-Inka menor",
    ),
    dict(
        sector="D", subsector="-",
        funcion="Residencia de baja condición y cocina principal",
        n_cuartos_almacen="0",
        medidas="200 m de extensión; ~120 cuartos; muros <=40 cm",
        filas_columnas="Aglutinado asimétrico, sin patio regular",
        volumen_m3="0",
        evidencia="Hyslop 1985:111-113",
        notas="Mita workers/state retainers; midden doméstico; ~mitad de la cerámica carbonizada",
    ),
    dict(
        sector="E", subsector="E1",
        funcion="Complejo administrativo/ceremonial; posible almacén diversificado",
        n_cuartos_almacen="96 (posible almacén, no confirmado)",
        medidas="100 m de ancho; muro de hasta 4 m; 7 filas de cubiculos; columnas cada 3,2 m",
        filas_columnas="7 filas con corredores; 2 corredores centrales",
        volumen_m3="desconocido",
        evidencia="Hyslop 1985:113-117",
        notas="Puertas selladas; casi sin artefactos; se barajan 'work areas' y 'diversified storage'",
    ),
    dict(
        sector="E", subsector="E2",
        funcion="Cuartos de función ceremonial/administrativa",
        n_cuartos_almacen="9 (4+5)",
        medidas="Estructura cuadrada de 4 cuartos + rectangular de 5; pasillo alineado con el ushnu",
        filas_columnas="4+5, separados por un corredor",
        volumen_m3="0",
        evidencia="Hyslop 1985:113-116",
        notas="El único 9 explícito del sitio. No se reportan quipus en E2.",
    ),
    dict(
        sector="E", subsector="E3",
        funcion="Plaza principal y ushnu",
        n_cuartos_almacen="0",
        medidas="Plaza >=120 m; plataforma sobre calzada elevada",
        filas_columnas="-",
        volumen_m3="0",
        evidencia="Hyslop 1985:113-117",
        notas="Dualidad de la plaza comparada con Cuzco (Rostworowski)",
    ),
    dict(
        sector="F", subsector="F1",
        funcion="Residencia de estatus intermedio; almacén ocasional",
        n_cuartos_almacen="0 (pocos cuartos ocasionales)",
        medidas="120 m de ancho; 14 unidades de 3-4 cuartos = 42-56 cuartos",
        filas_columnas="14 unidades radiales (Kunti Suyu), 3 niveles por unidad",
        volumen_m3="0",
        evidencia="Hyslop 1985:118-123",
        notas="Modelo de ceques: 14 unidades, no 9; muros, nichos, poyos, pintura",
    ),
    dict(
        sector="F", subsector="F2",
        funcion="Plazas, recintos y cuartos; función incierta",
        n_cuartos_almacen="desconocido",
        medidas="Cuartos profundos sin puertas en filas de 2-3; dos filas contra el muro",
        filas_columnas="2 filas de cuartos profundos",
        volumen_m3="desconocido",
        evidencia="Hyslop 1985:123-125",
        notas="Fuertemente destruido por deslizamiento y ocupación moderna",
    ),
    dict(
        sector="G", subsector="-",
        funcion="Almacén",
        n_cuartos_almacen=">=63 (+5 al O de C)",
        medidas="100 x 200 m; cuartos cuadrados sin puertas en filas",
        filas_columnas="Al menos 63 en los montículos A y B; 5 cuartos al O de C",
        volumen_m3="1544-2552 (estimación propia con 3,5-4,5 m x 2 m)",
        evidencia="Hyslop 1985:125-127",
        notas="'appear to have been a storage facility'; muy destruido; no incluido en los 6400 de A",
    ),
    dict(
        sector="H", subsector="-",
        funcion="Puesto de observación",
        n_cuartos_almacen="0",
        medidas="35 x 40 m; ~7 cuartos",
        filas_columnas="-",
        volumen_m3="0",
        evidencia="Hyslop 1985:127",
        notas="Colina nivelada; vista amplia del río y del sitio",
    ),
    dict(
        sector="TOTAL", subsector="-",
        funcion="Almacén A+G (+E1 posible, no confirmado)",
        n_cuartos_almacen="265-313 (A 202-250 + G >=63); 245 + 63 = 308 en el punto medio",
        medidas="—",
        filas_columnas="—",
        volumen_m3="7944-16200 según escenarios (ver capacidad_escenarios.csv)",
        evidencia="cálculo propio sobre Hyslop 1985 y Urton & Chu 2015",
        notas="A+G = 42% de los 734 cuartos contados (rango 39-45%), dentro de '1/3-1/2' de Hyslop",
    ),
]

cols = ["sector", "subsector", "funcion", "n_cuartos_almacen", "medidas",
        "filas_columnas", "volumen_m3", "evidencia", "notas"]
with open(BASE / "sectores.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(sectores)

# ---------------------------------------------------------------------------
# 2. Capacidad: escenarios explícitos
# ---------------------------------------------------------------------------
small_bin = (3.5**2 * 2.0, 4.5**2 * 2.0)          # 24.5 - 40.5 m3
big_bin = (15 * 6 * 1.3, 15 * 6 * 1.6)            # 117 - 144 m3 (supuesto)
g_room = small_bin

cap = {
    "A3_209_bins": (209 * small_bin[0], 209 * small_bin[1]),
    "A2_36_camaras": (36 * big_bin[0], 36 * big_bin[1]),
    "G_63_cuartos": (63 * g_room[0], 63 * g_room[1]),
}
cap["A_total_si_6400_es_A3_mas_A2"] = (
    cap["A3_209_bins"][0] + cap["A2_36_camaras"][0],
    cap["A3_209_bins"][1] + cap["A2_36_camaras"][1],
)
cap["sitio_si_A2_es_almacen"] = (
    cap["A_total_si_6400_es_A3_mas_A2"][0] + cap["G_63_cuartos"][0],
    cap["A_total_si_6400_es_A3_mas_A2"][1] + cap["G_63_cuartos"][1],
)

with open(BASE / "capacidad_escenarios.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["escenario", "m3_min", "m3_max", "supuesto"])
    w.writerow(["S1_solo_A_6400_de_Hyslop", 6400, 6400,
                "lectura literal: 6400 m3 para los 'square storage bins' de A"])
    w.writerow(["S2_A3_209_bins_3.5-4.5m", round(cap["A3_209_bins"][0]), round(cap["A3_209_bins"][1]),
                "209 bins de 3,5-4,5 m de lado x 2 m"])
    w.writerow(["S3_A3+A2_si_A2_es_almacen", round(cap["A_total_si_6400_es_A3_mas_A2"][0]),
                round(cap["A_total_si_6400_es_A3_mas_A2"][1]),
                "36 camaras de 15x6 m x 1,3-1,6 m"])
    w.writerow(["S4_sitio_A+G_si_A2_es_almacen", round(cap["sitio_si_A2_es_almacen"][0]),
                round(cap["sitio_si_A2_es_almacen"][1]),
                "S3 + 63 cuartos de G de 3,5-4,5 m x 2 m"])
    w.writerow(["S5_sitio_A+G_sin_A2", 6400 + round(cap["G_63_cuartos"][0]),
                6400 + round(cap["G_63_cuartos"][1]),
                "6400 (A) + G"])

# ---------------------------------------------------------------------------
# 3. Quipus por Unidad Arquitectónica (suplemento Urton & Chu 2015)
# ---------------------------------------------------------------------------
txt = (FT / "UrtonChu2015_suplemento.txt").read_text(encoding="utf-8", errors="ignore")
blocks = re.split(r"(?=#\d)", txt)[1:]
manual_cords = {"258": 41, "261": 12, "280": 37}
entries = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines()]
    ur = lines[1]
    loc = " | ".join(lines[2:8])
    cords = manual_cords.get(ur)
    if cords is None:
        for l in lines[2:]:
            if re.fullmatch(r"\d+", l):
                cords = int(l)
                break
    if re.search(r"U\.A\.\s*4", loc):
        ua = "U.A.4"
    elif re.search(r"U\.A\.\s*2", loc):
        ua = "U.A.2"
    elif re.search(r"U\.A\.\s*7", loc):
        ua = "U.A.7"
    else:
        ua = "corredor (U.A.3)"
    entries.append(dict(ur=ur, ua=ua, cuerdas=cords, loc=loc))

# correcciones de la transcripcion (los tres casos con el numero de cuerdas
# en la misma linea que el comentario o con U.E. partido)
for e in entries:
    if e["ur"] in manual_cords:
        e["cuerdas"] = manual_cords[e["ur"]]

by_ua = {}
for e in entries:
    by_ua.setdefault(e["ua"], []).append(e)

rows = []
for ua in ["U.A.2", "U.A.4", "U.A.7", "corredor (U.A.3)"]:
    es = by_ua[ua]
    rows.append(dict(
        ua=ua, n_quipus=len(es), n_cuerdas=sum(e["cuerdas"] for e in es),
        quipus=", ".join(e["ur"] for e in es),
        notas={
            "U.A.2": "kallanka; contra muro S y centro del muro E",
            "U.A.4": "kallanka; 14 con mani + UR271 con frijol; incluye los dos unicos quipus de 9 partes (UR270, UR278)",
            "U.A.7": "secadero O; cesta con aji; UR267A/B atados",
            "corredor (U.A.3)": "pila de 7 bajo muro caido; el suplemento lo rotula 'sector C, subsector 5' (inconsistente con el texto)",
        }[ua],
    ))
rows.append(dict(ua="TOTAL", n_quipus=sum(r["n_quipus"] for r in rows),
                 n_cuerdas=sum(r["n_cuerdas"] for r in rows),
                 quipus="UR255-UR280", notas="29 quipus estudiados; Urton 2017 dice 34 recuperados"))

with open(BASE / "quipus_ua.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["ua", "n_quipus", "n_cuerdas", "quipus", "notas"])
    w.writeheader()
    w.writerows(rows)

# ---------------------------------------------------------------------------
# 4. Consistencia demografica y de almacenaje
# ---------------------------------------------------------------------------
# Conteo de cuartos por sector (punto medio de los rangos)
rooms = dict(A=245, B=120, C=25, D=120, E=96 + 9, F=49, G=63, H=7)
total_rooms = sum(rooms.values())
storage_A_G = 245 + 63
frac = storage_A_G / total_rooms

# Volumen por cada 1000 habitantes, comparacion con la tabla 4-4 de LeVine 1992
pob = (1000, 2000)
vol = 6400
per1000 = tuple(sorted(1000 * vol / p for p in pob))  # menor a mayor
ref = (605, 705, 780)  # Pumpu, Huanuco Pampa, Xauxa

lines = []
lines.append("SECTORES Y CAPACIDAD")
lines.append(f"cuartos contados en el sitio (punto medio): {total_rooms}")
lines.append(f"almacen A+G / total: {storage_A_G}/{total_rooms} = {frac:.1%} (Hyslop: 1/3-1/2)")
lines.append("capacidad (m3):")
for k, v in cap.items():
    lines.append(f"  {k}: {v[0]:,.0f}-{v[1]:,.0f}")
lines.append("6400/209 = %.1f m3/bin; 6400/245 = %.1f m3/bin" % (6400 / 209, 6400 / 245))
lines.append("volumen por 1000 habitantes: %.0f-%.0f m3 (ref. sierra 605-780) -> %.1f-%.1f x" % (
    per1000[0], per1000[1], per1000[0] / max(ref), per1000[1] / min(ref)))
lines.append("")
lines.append("QUIPUS POR U.A.")
for r in rows:
    lines.append(f"  {r['ua']}: {r['n_quipus']} quipus, {r['n_cuerdas']} cuerdas")
lines.append("")
lines.append("14 del mani: UR266,268,269,270,272,273A,273B,274A,274B,275,276,277,278,279")
lines.append("cuerdas de los 14: %d (%.1f%% del total)" % (
    sum(e["cuerdas"] for e in entries if e["ur"] in
        {"266", "268", "269", "270", "272", "273A", "273B", "274A", "274B", "275", "276", "277", "278", "279"}),
    100 * sum(e["cuerdas"] for e in entries if e["ur"] in
              {"266", "268", "269", "270", "272", "273A", "273B", "274A", "274B", "275", "276", "277", "278", "279"}) /
    sum(e["cuerdas"] for e in entries)))

(BASE / "salida_01.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
