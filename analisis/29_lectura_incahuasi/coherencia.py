# Coherencia de la lectura integral de Incahuasi: recalcula desde los datos las cifras que usa lectura.md.
# Implementación propia (no importa scripts de 13/16/19/ds). Base: KFG (analisis/datos/cuerdas.csv);
# cotejo directo con OKR (khipu.db en solo lectura).
# Uso, desde la raíz del repo:  python analisis/29_lectura_incahuasi/coherencia.py
import sqlite3
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.stdout.reconfigure(encoding="utf-8")
c = pd.read_csv("analisis/datos/cuerdas.csv", low_memory=False, keep_default_na=False)
c["valor"] = pd.to_numeric(c.valor, errors="coerce").fillna(0).round().astype(int)
c["grupo"] = c.grupo.astype(int)
c["orden"] = c.orden.astype(int)
c = c.sort_values(["kfg", "orden"])
q = lambda k: c[c.kfg == k]
col0 = lambda k: q(k)[q(k).nivel == 0]
res = []


def check(nombre, cond, detalle):
    res.append(bool(cond))
    print(f"[{'OK' if cond else 'FALLA'}] {nombre}\n       {detalle}")


def cabeceras(k):
    """Primer colgante anudado de cada grupo no separador (definición de 13/18)."""
    out = {}
    for g, x in col0(k).groupby("grupo"):
        p = x[(x.valor > 0) | (x.nudos != "")]
        if len(p):
            out[g] = int(p.valor.iloc[0])
    return out


def ps1(k, g):
    """Lista (P, S1) de los colgantes de un grupo: colgante y su primera subsidiaria (0 si falta)."""
    x = q(k)[q(k).grupo == g]
    return [(int(r.valor), int(x[(x.padre == r.cuerda) & (x.cuerda == r.cuerda + "s1")].valor.sum()))
            for r in x[x.nivel == 0].itertuples()]


def lcs(a, b):
    D = np.zeros((len(a) + 1, len(b) + 1), int)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            D[i + 1, j + 1] = D[i, j] + 1 if x == y else max(D[i, j + 1], D[i + 1, j])
    return int(D[-1, -1])


# ---------------------------------------------------------------- UR278: filas de 9
u278 = col0("UR278")
filas = {g: x.valor.tolist() for g, x in u278.groupby("grupo") if len(x) == 9}
tot = {g: sum(v) for g, v in filas.items()}

# 1. UR270 -> UR278: celda = P + S1, columna a columna (±1)
mejores = {}
for g in sorted(q("UR270").grupo.unique()):
    v = ps1("UR270", g)
    if len(v) != 9:
        continue
    s = [p + s1 for p, s1 in v]
    soloP = [p for p, _ in v]
    best = max(filas, key=lambda h: sum(abs(a - b) <= 1 for a, b in zip(s, filas[h])))
    n = sum(abs(a - b) <= 1 for a, b in zip(s, filas[best]))
    nP = max(sum(abs(a - b) <= 1 for a, b in zip(soloP, filas[h])) for h in filas)
    mejores[g] = (best, n, nP)
g6 = {g: v for g, v in mejores.items() if v[1] >= 6}
check("UR270 (P+S1) -> UR278: 5 grupos con >=6/9 columnas; solo colgantes: ninguno",
      len(g6) == 5 and max(v[2] for v in mejores.values()) < 6,
      "; ".join(f"g{g}->g{b} {n}/9 (solo P {nP}/9)" for g, (b, n, nP) in mejores.items()))
s0 = [p + s1 for p, s1 in ps1("UR270", 0)]
check("UR270 g0 = UR278 g21 (8 exactas, la 1.ª +1)",
      sum(a == b for a, b in zip(s0, filas[21])) == 8 and filas[21][0] - s0[0] == 1,
      f"P+S1 {s0} | UR278 g21 {filas[21]}")

# 2. Totales de fila de UR278 en orden en UR266 (colgantes) y en UR275 (cabeceras)
orden_tot = [tot[g] for g in sorted(tot)]
d266 = col0("UR266").valor.tolist()
cab275 = [cabeceras("UR275")[g] for g in sorted(cabeceras("UR275"))]
n266, n275 = lcs(orden_tot, d266), lcs(orden_tot, cab275)
check("Totales de UR278 en orden: 11 en UR266 y 7 en UR275",
      n266 == 11 and n275 == 7, f"LCS UR266 = {n266}; LCS UR275 = {n275}; fila g0 = {orden_tot[0]}")

# 3. UR273A + UR273B por número de grupo -> cabeceras de UR266/UR275/UR269
A, B = cabeceras("UR273A"), cabeceras("UR273B")
comunes = sorted(set(A) & set(B))
pool = set(pd.concat([col0(k).valor for k in ["UR266", "UR275", "UR269"]]))
ab = {g: A[g] + B[g] for g in comunes}
ex = {g: s for g, s in ab.items() if s in pool}
check("UR273A+B: 8 de 18 sumas exactas en los libros", len(comunes) == 18 and len(ex) == 8,
      f"{len(ex)}/{len(comunes)}: " + ", ".join(f"g{g} {A[g]}+{B[g]}={s}" for g, s in ex.items()))

# 4. Doble vía: cifras alcanzadas a la vez por una fila de UR278 y por una suma A+B (±1)
#    A = UR273A; donde UR273A está en blanco, su copia UR274A, alineada por índice de registro
#    (grupos no separadores en orden: UR274A tiene los separadores en otras posiciones que UR273A/B).
def por_registro(k):
    out = []
    for g, x in col0(k).groupby("grupo"):
        if x.color.str.startswith("PK").all() and not (x.valor > 0).any():
            continue
        p = x[x.valor > 0]
        out.append((g, int(p.valor.iloc[0]) if len(p) else None))
    return out


rB, rA4 = por_registro("UR273B"), por_registro("UR274A")
sust = {}
for i, (gB, b) in enumerate(rB):
    if b and gB not in A and i < len(rA4) and rA4[i][1]:
        sust[gB] = (rA4[i][1], b, rA4[i][1] + b)
ab2 = list(ab.values()) + [v[2] for v in sust.values()]
doble = sorted({s for s in ab2 for t in tot.values() if abs(s - t) <= 1})
check("Doble vía (fila UR278 = suma A+B, ±1): 3 con UR273A; 5 con UR274A como sustituto",
      len({s for s in ab.values() for t in tot.values() if abs(s - t) <= 1}) == 3 and len(doble) == 5,
      f"{doble}; sustituciones UR274A+UR273B: {sust}")


# 5. P de UR270 (Σ colgantes del grupo g) = cabecera de UR273B en el grupo g+9; S1 = UR273A
pe, se = [], []
for g in mejores:
    v = ps1("UR270", g)
    P, S = sum(p for p, _ in v), sum(s for _, s in v)
    if g + 9 in B:
        pe.append((g, P, B[g + 9]))
    if g + 9 in A:
        se.append((g, S, A[g + 9]))
nP = sum(P == b for _, P, b in pe)
nS = sum(abs(S - a) <= 1 for _, S, a in se)
check("Σ colgantes de UR270 = componente B (UR273B, grupo +9): 4 exactas",
      nP == 4, f"P: {pe} -> {nP} exactas; S1 vs UR273A (±1): {se} -> {nS}")

# 6. Cuotas fijas por quipu (cuerdas con ese valor exacto)
cnt = {(k, v): int((q(k).valor == v).sum()) for k, v in
       [("UR275", 47), ("UR266", 47), ("UR269", 47), ("UR268", 208), ("UR274A", 30), ("UR274B", 17), ("UR274B", 10),
        ("UR267A", 15), ("UR267B", 10)]}
check("Cuotas: 24 cuerdas de 47 en UR275, 12 de 17 en UR274B",
      cnt[("UR275", 47)] == 24 and cnt[("UR274B", 17)] == 12, cnt)

# 7. La cuota es absoluta: 47 / cabecera en UR275 (registros que llevan 47 en 2.ª posición)
tasas = []
for g, x in col0("UR275").groupby("grupo"):
    v = x[x.valor > 0].valor.tolist()
    if len(v) >= 2 and v[1] == 47:
        tasas.append(47 / v[0])
check("UR275: 47/cabecera entre 1,1 % y 3,7 % (no un 2 % fijo)",
      abs(min(tasas) - 0.0110) < 0.0005 and abs(max(tasas) - 0.0368) < 0.0005,
      f"n={len(tasas)}; min {min(tasas):.4f}; max {max(tasas):.4f}; media {np.mean(tasas):.4f}")

# 8. UR275: cabecera = 47 + destinos (colgantes; registros con >= 3 cuerdas tras la cabecera; error < 5 %)
ok = {}
for g, x in col0("UR275").groupby("grupo"):
    v = x[x.valor > 0].valor.tolist()
    if len(v) - 1 >= 3:
        ok[g] = abs(sum(v[1:]) - v[0]) / v[0] < 0.05
check("UR275: reparto cerrado (±5 %) en 15 de 16 registros complejos; falla g8 (2633)",
      sum(ok.values()) == 15 and len(ok) == 16 and not ok[8], f"{sum(ok.values())}/{len(ok)}")


# 9. Perfil de las 9 columnas de UR278 (filas completas)
M = np.array([v for v in filas.values() if all(x > 0 for x in v)], float)
med = M.mean(0)
cv = med.std(ddof=1) / med.mean()
prop = (M / M.sum(1, keepdims=True)).mean(0)
rho, p = spearmanr(range(9), prop)
check("UR278: CV entre medias de columna 0,173; perfil descendente rho ≈ -0,73",
      abs(cv - 0.173) < 0.002 and abs(rho + 0.73) < 0.02,
      f"{len(M)} filas; CV={cv:.3f}; rho={rho:.2f} (p={p:.3f}); medias {np.round(med).astype(int).tolist()}; "
      f"% {np.round(100 * prop, 1).tolist()}")

# 10. Escala: unidades de UR278 y su conversión con el bulto propuesto (82 L ≈ 23,5 kg; n_agronomia)
tot278 = int(u278.valor.sum())
tot_filas = int(sum(tot.values()))
check("Escala UR278: 1 300-1 700 t con 23,5 kg/unidad (n_agronomia: 61 790 u. = 1 449 t)",
      1300 <= tot_filas * 23.5 / 1000 and tot278 * 23.5 / 1000 <= 1700,
      f"Σ 26 filas de 9 = {tot_filas} u. ({tot_filas * 23.5 / 1000:.0f} t; {tot_filas * 82 / 1000:.0f} m³); "
      f"Σ colgantes = {tot278} u. ({tot278 * 23.5 / 1000:.0f} t); Σ cabeceras UR275 = {sum(cab275)} "
      f"(Urton y Chu 2018: 56 446)")


# 11. Cotejo directo con OKR (khipu.db en solo lectura): valores de UR278 y UR270 iguales a KFG
db = sqlite3.connect("file:data/external/open-khipu-repository/data/khipu.db?mode=ro", uri=True)


def okr_colgantes(inv):
    kid = db.execute("select KHIPU_ID from khipu_main where INVESTIGATOR_NUM=?", (inv,)).fetchone()[0]
    rows = db.execute("""select c.CORD_ID, coalesce(sum(k.knot_value_type),0) from cord c
                         left join knot k on k.CORD_ID=c.CORD_ID
                         where c.KHIPU_ID=? and c.CORD_LEVEL=1 group by c.CORD_ID order by c.CORD_ORDINAL""",
                      (kid,)).fetchall()
    return [int(round(v)) for _, v in rows]


iguales = {k: okr_colgantes(k) == col0(k).valor.tolist() for k in ["UR278", "UR270", "UR275", "UR266"]}
check("OKR = KFG en los colgantes de UR278, UR270, UR275 y UR266", all(iguales.values()), iguales)

print(f"\n{sum(res)}/{len(res)} comprobaciones correctas")
