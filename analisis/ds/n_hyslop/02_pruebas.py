# -*- coding: utf-8 -*-
"""
Controles estadisticos para la hipotesis "las 9 partes de UR278/UR270
corresponden a divisiones del sitio de Inkawasi".

Pruebas:
  T1  4+5 (Sector E, subdivision 2) vs columnas c1-c4 / c5-c9
  T2  3x3 (los tres suyu con 9 ceques en grupos de 3) vs 3 bloques de 3
  T3  gradiente monotono a lo largo de las 9 columnas (fila de 9 depositos)
  T4  control de ubicuidad: cuantos conteos arquitectonicos son multiplos de 9
  T5  concentracion espacial de los dos unicos quipus de 9 partes (UR270, UR278)
  T6  tamano (cuerdas) del grupo de 14 del mani frente al resto

Semilla fija. Nulo explicito en cada prueba. Holm para T1-T3.
"""
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parent
SEED = 20261018
rng = np.random.default_rng(SEED)
NPERM = 20000

# ---------------------------------------------------------------------------
# Datos: UR278, tabla canonica de 13_sistema_incahuasi (26 filas completas)
# ---------------------------------------------------------------------------
cols = [f"c{i}" for i in range(1, 10)]
t = pd.read_csv(BASE.parent.parent / "13_sistema_incahuasi" / "ur278_tabla.csv")
U278 = t.set_index("grupo")[cols].astype(float)
U278 = U278[U278.notna().all(axis=1)]
P = U278.div(U278.sum(axis=1), axis=0).to_numpy()
n = len(P)
col_mean = P.mean(0)


def holm(pvals):
    """Holm-Bonferroni; devuelve p ajustados en el orden original."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    m = len(p)
    prev = 0.0
    for rank, i in enumerate(order):
        val = min(1.0, (m - rank) * p[i])
        prev = max(prev, val)
        adj[i] = prev
    return adj


# ---------------------------------------------------------------------------
# T1: 4 + 5
# ---------------------------------------------------------------------------
obs45 = P[:, :4].mean(1).mean() - P[:, 4:].mean(1).mean()
count = 0
for _ in range(NPERM):
    idx = rng.permutation(9)
    d = P[:, idx[:4]].mean(1).mean() - P[:, idx[4:]].mean(1).mean()
    if abs(d) >= abs(obs45):
        count += 1
p45 = (count + 1) / (NPERM + 1)

# ---------------------------------------------------------------------------
# T2: 3 bloques de 3 vs 9 columnas libres (F anidada sobre log-proporciones)
# ---------------------------------------------------------------------------
Y = np.log(P + 1e-4)
y = Y.ravel()
row = np.repeat(np.eye(n), 9, axis=0)
col = np.tile(np.eye(9), (n, 1))
blk = np.tile(np.repeat(np.eye(3), 3, axis=0), (n, 1))


def rss(D):
    b, _, _, _ = np.linalg.lstsq(D, y, rcond=None)
    e = y - D @ b
    return e @ e, np.linalg.matrix_rank(D)


r_row, k_row = rss(row)
r_col, k_col = rss(np.hstack([row, col]))
r_blk, k_blk = rss(np.hstack([row, blk]))
df1 = len(y) - k_col
F = ((r_blk - r_col) / (k_col - k_blk)) / (r_col / df1)
p33 = stats.f.sf(F, k_col - k_blk, df1)
r2_col = 1 - r_col / r_row
r2_blk = 1 - r_blk / r_row

# ---------------------------------------------------------------------------
# T3: gradiente monotono (Spearman) con permutacion dentro de fila
# ---------------------------------------------------------------------------
pos = np.arange(1, 10)
rho_obs = stats.spearmanr(pos, col_mean).statistic
count = 0
for _ in range(NPERM):
    Pp = np.vstack([row_vals[rng.permutation(9)] for row_vals in P])
    rho = stats.spearmanr(pos, Pp.mean(0)).statistic
    if abs(rho) >= abs(rho_obs):
        count += 1
p_grad = (count + 1) / (NPERM + 1)

p_adj = holm([p45, p33, p_grad])

# ---------------------------------------------------------------------------
# T1b: escaneo de los 8 puntos de corte contiguos (familia aparte, Holm 8)
# ---------------------------------------------------------------------------
scan = []
for k in range(1, 9):
    obs = P[:, :k].mean(1).mean() - P[:, k:].mean(1).mean()
    count = 0
    for _ in range(NPERM):
        idx = rng.permutation(9)
        d = P[:, idx[:k]].mean(1).mean() - P[:, idx[k:]].mean(1).mean()
        if abs(d) >= abs(obs):
            count += 1
    scan.append((k, obs, (count + 1) / (NPERM + 1)))
scan_adj = holm([x[2] for x in scan])
scan_rows = [dict(corte=k, diferencia=d, p_perm=p, p_holm=pa)
             for (k, d, p), pa in zip(scan, scan_adj)]
with open(BASE / "control_cortes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(scan_rows[0].keys()))
    w.writeheader()
    w.writerows(scan_rows)

# Mejor particion posible en 3 bloques de 3 (exploratorio, no prueba)
import itertools
best = None
for tri in itertools.combinations(range(9), 3):
    rem = [i for i in range(9) if i not in tri]
    for tri2 in itertools.combinations(rem, 3):
        tri3 = tuple(i for i in rem if i not in tri2)
        B = np.zeros((n * 9, 3))
        for j, g in enumerate([tri, tri2, tri3]):
            for i in g:
                B[np.arange(n) * 9 + i, j] = 1
        val_tmp, _ = rss(np.hstack([row, B]))
        if best is None or val_tmp < best[0]:
            best = (val_tmp, [tuple(i + 1 for i in g) for g in [tri, tri2, tri3]])
r2_best3 = 1 - best[0] / r_row


# ---------------------------------------------------------------------------
# T4: control de ubicuidad del 9
# ---------------------------------------------------------------------------
# Conteos independientes tomados de Hyslop 1985 y Urton & Chu 2015.
# Se excluyen los derivados (36 = 2x18; 245 = 209+36; 9+9 = 18) para no
# contar dos veces la misma decision de diseno.
conteos = {
    "kallankas_A1": 4,
    "secaderos_A1": 2,
    "camaras_grandes_por_lado_A2": 18,
    "bins_pequenos_A3": 209,
    "cubiculos_E1": 96,
    "cuartos_E2": 9,
    "cuartos_G": 63,
    "recintos_rectangulares_A": 30,
    "unidades_F1": 14,
    "cuartos_H": 7,
    "cuartos_C": 25,
    "cuartos_B": 120,
    "cuartos_D": 120,
}
vals = np.array(list(conteos.values()))
rows_mult = []
for k in range(2, 13):
    obs = int(np.sum(vals % k == 0))
    pbin = stats.binom.sf(obs - 1, len(vals), 1 / k)  # P(X >= obs)
    # Monte Carlo uniforme 1..250 (mismo rango que los conteos)
    sims = rng.integers(1, 251, size=(NPERM, len(vals)))
    pmc = (np.sum(np.sum(sims % k == 0, axis=1) >= obs) + 1) / (NPERM + 1)
    rows_mult.append(dict(k=k, observados=obs, esperados=round(len(vals) / k, 2),
                          p_binomial=pbin, p_montecarlo=pmc,
                          cuales=", ".join(nm for nm, v in conteos.items() if v % k == 0)))
with open(BASE / "control_multiplos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_mult[0].keys()))
    w.writeheader()
    w.writerows(rows_mult)

# ---------------------------------------------------------------------------
# T5: los dos unicos quipus de 9 partes, ambos en U.A.4
# ---------------------------------------------------------------------------
struct_sizes = {"U.A.4": 15, "corredor": 7, "U.A.2": 5, "U.A.7": 2}
N = sum(struct_sizes.values())
p_same = sum(s * (s - 1) for s in struct_sizes.values()) / (N * (N - 1))
p_both_UA4 = (15 / N) * (14 / (N - 1))

# ---------------------------------------------------------------------------
# T6: tamano del grupo de 14 del mani
# ---------------------------------------------------------------------------
# cuerdas del suplemento 2015
cuerdas = {
    "255": 85, "256": 118, "257": 10, "258": 41, "259": 13, "260": 24, "261": 12,
    "262": 138, "263": 236, "264": 226, "265": 14,
    "266": 129, "267A": 79, "267B": 103, "268": 128, "269": 273, "270": 158,
    "271": 32, "272": 173, "273A": 78, "273B": 109, "274A": 88, "274B": 95,
    "275": 112, "276": 5, "277": 150, "278": 297, "279": 12, "280": 37,
}
grupo14 = {"266", "268", "269", "270", "272", "273A", "273B", "274A", "274B",
           "275", "276", "277", "278", "279"}
a = np.array([cuerdas[k] for k in grupo14])
b = np.array([v for k, v in cuerdas.items() if k not in grupo14])
obs_diff = a.mean() - b.mean()
pool = np.concatenate([a, b])
count = 0
for _ in range(NPERM):
    perm = rng.permutation(pool)
    if abs(perm[:len(a)].mean() - perm[len(a):].mean()) >= abs(obs_diff):
        count += 1
p_size = (count + 1) / (NPERM + 1)

# ---------------------------------------------------------------------------
# T1c: réplica descriptiva en UR270 (6 filas completas; no independiente)
# ---------------------------------------------------------------------------
r270 = pd.read_csv(BASE.parent / "n_rejilla" / "rejilla.csv")
r270 = r270[r270.quipu == "UR270"].dropna(subset=cols)
P270 = r270[cols].to_numpy(float)
P270 = P270 / P270.sum(1, keepdims=True)
obs270 = P270[:, :4].mean(1).mean() - P270[:, 4:].mean(1).mean()
count = 0
for _ in range(NPERM):
    idx = rng.permutation(9)
    d = P270[:, idx[:4]].mean(1).mean() - P270[:, idx[4:]].mean(1).mean()
    if abs(d) >= abs(obs270):
        count += 1
p270 = (count + 1) / (NPERM + 1)

# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
lines = []
lines.append("T1 4+5 (c1-c4 vs c5-c9): dif = %.4f; p_perm = %.4f; p_Holm = %.4f" % (obs45, p45, p_adj[0]))
lines.append("T2 3x3 vs 9 libres: R2_col = %.3f, R2_bloque = %.3f, F = %.2f, p = %.2e; p_Holm = %.2e" % (
    r2_col, r2_blk, F, p33, p_adj[1]))
lines.append("T3 gradiente Spearman: rho = %.3f; p_perm = %.4f; p_Holm = %.4f" % (rho_obs, p_grad, p_adj[2]))
lines.append("T1b puntos de corte contiguos (Holm sobre 8):")
for x in scan_rows:
    lines.append("   corte tras c%d: dif = %.4f, p = %.4f, p_Holm = %.3f" % (
        x["corte"], x["diferencia"], x["p_perm"], x["p_holm"]))
lines.append("Mejor 3+3+3 posible (exploratorio): R2 = %.3f; grupos = %s" % (r2_best3, best[1]))
lines.append("T4 multiplos de k (13 conteos independientes):")
for row in rows_mult:
    lines.append("   k=%2d: %d observados (%.2f esperados), p_bin = %.3f, p_MC = %.3f" % (
        row["k"], row["observados"], row["esperados"], row["p_binomial"], row["p_montecarlo"]))
lines.append("T1c UR270 (6 filas completas): 4+5 dif = %.4f; p_perm = %.3f (replica de direccion, no independiente)" % (
    obs270, p270))
lines.append("T5 los 2 quipus de 9 partes: P(misma estructura) = %.3f; P(ambos en U.A.4) = %.3f" % (
    p_same, p_both_UA4))
lines.append("T6 grupo de 14: media %.1f cuerdas vs %.1f resto; dif %.1f; p_perm = %.4f" % (
    a.mean(), b.mean(), obs_diff, p_size))
lines.append("")
lines.append("Medias por columna: " + ", ".join("%.4f" % v for v in col_mean))
lines.append("Totales por columna: " + ", ".join("%.0f" % v for v in U278.sum(0).to_numpy()))
lines.append("CV de los totales por columna: %.3f" % (U278.sum(0).std(ddof=1) / U278.sum(0).mean()))

(BASE / "salida_02.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
