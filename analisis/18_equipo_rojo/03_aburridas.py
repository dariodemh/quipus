"""Ataque 3. Explicaciones aburridas.

(a) ¿Lecturas "corregidas" por el transcriptor? Para los quipus implicados: notas y valores alt de KFG en las
    cuerdas que participan en las coincidencias; comparación cuerda a cuerda (multiconjunto de valores por quipu
    y por grupo) entre KFG (cuerdas.csv) y OKR khipu.db (valor = Σ TOTAL_VALUE de knot_cluster por cuerda).
    Si las cuerdas que "cuadran" fueran las que más discrepan entre bases, o las que llevan notas/alt, sería mala señal.
(b) ¿Mismo objeto registrado varias veces? Se comparan, entre UR273A, UR273B, UR274A, UR274B, UR270 y UR278,
    las cuerdas con la misma huella física (valor + cadena de nudos + largo + color) y la secuencia de largos.
(c) ¿Valores frecuentes o redondos? Para cada suma acertada: nº de veces que aparece en el archivo, en todo KFG,
    y si es múltiplo de 10/100.
Salida: salida_03_aburridas.txt
"""
import sqlite3
from collections import Counter
import numpy as np
import pandas as pd
import lib18 as L

c, q = L.cargar()
out = open(L.AQUI / "salida_03_aburridas.txt", "w", encoding="utf-8")


def pr(*a, **kw):
    print(*a, **kw)
    print(*a, file=out, **kw)


IMPL = ["UR266", "UR275", "UR269", "UR273A", "UR273B", "UR274A", "UR274B", "UR270", "UR278", "UR267A", "UR267B"]

# ---------- (a1) notas y alt
pr("(a1) Notas y valores alt en KFG")
for k in IMPL:
    s = c[c.kfg == k]
    nn = s[s.notas != ""]
    na = s[s.alt != ""]
    pr(f"  {k}: {len(s)} cuerdas, con notas {len(nn)}, con alt {len(na)}")
    for r in pd.concat([nn, na]).drop_duplicates("orden").head(8).itertuples():
        pr(f"     {r.cuerda} g{r.grupo} valor={r.valor} alt={r.alt!r} notas={r.notas[:90]!r}")

# ---------- (a2) KFG frente a OKR
con = sqlite3.connect(L.RAIZ / "data/external/open-khipu-repository/data/khipu.db")
km = pd.read_sql("select KHIPU_ID, INVESTIGATOR_NUM, OKR_NUM, CHANGED_BY, CHANGED_ON from khipu_main", con)
cord = pd.read_sql("select KHIPU_ID, CORD_ID, CORD_LEVEL, CORD_ORDINAL, CLUSTER_ID, CORD_LENGTH from cord", con)
# TOTAL_VALUE viene vacío en estos quipus; el valor se reconstruye nudo a nudo (knot_value_type = valor del nudo:
# 100/10/1 en los simples, nº de vueltas en los largos, 1 en la figura de ocho)
kn = pd.read_sql("select CORD_ID, knot_value_type from knot", con)
val = kn.groupby("CORD_ID").knot_value_type.sum()
cord["v"] = cord.CORD_ID.map(val).fillna(0).round().astype(int)
okr_of = dict(zip(q.kfg, q.okr))
pr("\n(a2) KFG frente a OKR (multiconjunto de valores anudados > 0 y nº de cuerdas); se listan los implicados y los que discrepan")
ARCH = sorted(q[q.procedencia == "Incahuasi"].kfg)
n_igual = 0
for k in ARCH:
    row = km[km.OKR_NUM == okr_of.get(k)]
    if row.empty:
        pr(f"  {k}: no está en OKR")
        continue
    kid = row.KHIPU_ID.iloc[0]
    o = Counter(cord[(cord.KHIPU_ID == kid) & (cord.v > 0)].v)
    f = Counter(c[(c.kfg == k) & (c.valor > 0)].valor)
    solo_kfg, solo_okr = f - o, o - f
    n_cuerdas = (len(c[c.kfg == k]), int((cord.KHIPU_ID == kid).sum()))
    if not solo_kfg and not solo_okr and n_cuerdas[0] == n_cuerdas[1]:
        n_igual += 1
        if k not in IMPL:
            continue
    pr(f"  cuerdas KFG/OKR {n_cuerdas}", end=" ")
    pr(f"  {k} (OKR {okr_of[k]}, modificado por {row.CHANGED_BY.iloc[0]} {str(row.CHANGED_ON.iloc[0])[:10]}): "
       f"KFG {sum(f.values())} valores, OKR {sum(o.values())}; solo en KFG {sum(solo_kfg.values())} "
       f"{sorted(solo_kfg.elements())[:12]}; solo en OKR {sum(solo_okr.values())} {sorted(solo_okr.elements())[:12]}")

pr(f"  quipus del archivo idénticos en ambas bases (valores y nº de cuerdas): {n_igual} de {len(ARCH)}")

# ---------- valores que participan en las coincidencias (de 13, tablas §2.2 y §2.3)
SUMAS_47 = [2950, 1278, 2020, 2106, 1653, 1737, 1827, 1780, 2247, 1765]
COMP = {"UR273A": [808, 453, 448, 502, 448, 672, 509, 325], "UR273B": [2142, 887, 1129, 1334, 1200, 1289, 1325, 1332, 1575, 1256, 1181],
        "UR274A": [391, 891, 772], "UR267A": [215, 141, 127, 201, 63], "UR267B": [613, 601, 535, 321, 329]}
SUMAS_25 = [828, 742, 662, 522, 392]
pr("\n   ¿Las cuerdas que cuadran llevan notas o alt?")
for k, vs in list(COMP.items()) + [("UR266", SUMAS_47), ("UR275", SUMAS_47), ("UR269", SUMAS_47 + SUMAS_25)]:
    s = c[(c.kfg == k) & c.valor.isin(vs)]
    pr(f"     {k}: {len(s)} cuerdas implicadas; con notas {int((s.notas != '').sum())}, con alt {int((s.alt != '').sum())}")

# UR278 filas 21-29 y UR270 (celdas coincidentes)
u278 = c[(c.kfg == "UR278") & c.grupo.isin(range(21, 30))]
u270 = c[(c.kfg == "UR270") & c.grupo.isin([0, 4, 5, 8, 9, 10])]
pr(f"     UR278 g21-29: {len(u278)} cuerdas, con notas {int((u278.notas != '').sum())}, con alt {int((u278.alt != '').sum())}")
pr(f"     UR270 g0,4,5,8,9,10: {len(u270)} cuerdas, con notas {int((u270.notas != '').sum())}, con alt {int((u270.alt != '').sum())}")

# ---------- (b) huellas físicas compartidas
pr("\n(b) ¿Mismo objeto registrado varias veces?")
G = ["UR273A", "UR273B", "UR274A", "UR274B", "UR270", "UR278", "UR266", "UR275"]
s = c[c.kfg.isin(G) & (c.nudos != "")].copy()
s["huella"] = s.nudos + "|" + s.largo.astype(str) + "|" + s.color
dup = s[s.duplicated("huella", keep=False)].sort_values("huella")
cruz = dup.groupby("huella").kfg.nunique()
pr(f"  cuerdas anudadas con huella idéntica (nudos+posiciones+largo+color) en ≥2 quipus distintos: {int((cruz > 1).sum())}")
for h in cruz[cruz > 1].index[:10]:
    d = dup[dup.huella == h]
    pr(f"     {h[:70]} → {list(zip(d.kfg, d.cuerda))}")
s["huella2"] = s.nudos
cruz2 = s.groupby("huella2").kfg.nunique()
pr(f"  misma cadena de nudos con posiciones (sin largo/color) en ≥2 quipus: {int((cruz2 > 1).sum())} "
   f"(de {s.huella2.nunique()} cadenas; las de 1 racimo son triviales: "
   f"{int(((cruz2 > 1) & ~cruz2.index.str.contains(';')).sum())})")
# UR270 g0 frente a UR278 g21: largos
for g, h in [(0, 21), (4, 25), (8, 27)]:
    a = c[(c.kfg == "UR270") & (c.grupo == g) & (c.nivel == 0)]
    b = c[(c.kfg == "UR278") & (c.grupo == h) & (c.nivel == 0)]
    pr(f"  UR270 g{g} largos {a.largo.tolist()} | UR278 g{h} largos {b.largo.tolist()}")
    pr(f"     colores UR270 {a.color.tolist()} | UR278 {b.color.tolist()}")
    pr(f"     nudos UR278: {b.nudos.str.replace(r'\(([\d.]+),\w\)', r'@\1', regex=True).tolist()[:4]}")

# ---------- (c) valores frecuentes o redondos
pr("\n(c) ¿Las coincidencias se concentran en valores frecuentes o redondos?")
inca = set(q[q.procedencia == "Incahuasi"].kfg)
todos = c[c.pres]
fa = Counter(todos[todos.kfg.isin(inca)].valor)
ft = Counter(todos.valor)
for v in SUMAS_47 + SUMAS_25:
    pr(f"  {v}: en el archivo {fa[v]} veces, en todo KFG {ft[v]} (fuera de Incahuasi {ft[v] - fa[v]}); "
       f"múltiplo de 10: {v % 10 == 0}, de 100: {v % 100 == 0}")
S = L.diana(c, L.RES)
rango = S[(S >= 1000) & (S <= 3000)]
pr(f"  Diana (unión 266/275/269) en 1000-3000: {len(rango)} valores distintos de 2001 posibles "
   f"(densidad {len(rango) / 2001:.3f}); múltiplos de 10 entre ellos {np.mean(rango % 10 == 0):.2f}")
pr(f"  Aciertos A+B (UR273): múltiplos de 10: {sum(v % 10 == 0 for v in SUMAS_47)}/{len(SUMAS_47)}; "
   f"frecuencia media en KFG fuera de Incahuasi {np.mean([ft[v] - fa[v] for v in SUMAS_47]):.2f}; "
   f"en la diana, frecuencia media de valores 1000-3000 en KFG fuera de Incahuasi "
   f"{np.mean([ft[v] - fa[v] for v in rango]):.2f}")
out.close()
