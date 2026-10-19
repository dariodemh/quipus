# -*- coding: utf-8 -*-
"""Controles adicionales UR262:
  D1 duplicados exactos de valor (nulo de digitos, preserva estructura decimal)
  D2 similitud entre pendientes adyacentes (|dif|) vs nulo
  D3 color: AB al inicio de bloque / periodicidad (nulo: permutar colores)
  D4 color y nivel (tabla + chi2)
  D5 largo vs valor (Spearman vs nulo)
  D6 primer pendiente del grupo es el mayor
  D7 razon ~6.8: estadistico maximo sobre ventanas (corrige eleccion post hoc)
"""
import os
import numpy as np
import pandas as pd
from scipy import stats as st

OUT = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)
NPERM = 1000
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0).astype(int)
q["grupo"] = q["grupo"].astype(int)
q["largo"] = q["largo"].fillna(0)
n = len(q)
val = q.valor.values.astype(float)
nivel = q.nivel.values.astype(int)
grupo = q.grupo.values
orden = q.orden.values

# ---------- D1 duplicados ----------
pos = val[val > 0]
def n_dup(v):
    v = v[v > 0]
    u, c = np.unique(v, return_counts=True)
    return int((c[c > 1] - 1).sum())   # cuerdas "sobrantes" en grupos de valores repetidos

obs_dup = n_dup(val)
print("D1 duplicados: cuerdas sobrantes =", obs_dup, "| valores distintos:", len(np.unique(pos)), "de", len(pos))

# nulo de digitos: se conserva el multiconjunto de digitos de cada posicion decimal
digits = {}
maxdec = 4
for d in range(maxdec):
    digits[d] = ((val // 10**d) % 10).astype(int)
null_dup = []
for _ in range(NPERM):
    v = np.zeros(n)
    for d in range(maxdec):
        v += RNG.permutation(digits[d]) * 10**d
    null_dup.append(n_dup(v))
null_dup = np.array(null_dup)
p_dup = (1 + int((null_dup >= obs_dup).sum())) / (1 + NPERM)
print("   nulo digitos: media %.2f p95 %.1f  p=%.4f" % (null_dup.mean(), np.percentile(null_dup, 95), p_dup))

# ---------- D2 adyacentes ----------
p = q[q.nivel == 0].copy()
p["pos"] = p.groupby("grupo").cumcount() + 1
seqs = {g: s.sort_values("orden").valor.values.astype(float) for g, s in p.groupby("grupo") if len(s) > 2}
def adj_diff(vals_by_group):
    d = []
    for g, v in vals_by_group.items():
        if len(v) > 1:
            d += list(np.abs(np.diff(v)))
    return float(np.median(d)), float(np.mean(d))
obs_med, obs_mean = adj_diff(seqs)
print("\nD2 adyacentes: mediana |dif| = %.1f  media = %.1f" % (obs_med, obs_mean))
null_med = []
for _ in range(NPERM):
    vv = RNG.permutation(val)
    d = {g: vv[np.where((nivel == 0) & (grupo == g))[0]] for g in seqs}
    # respetar orden interno
    d = {g: np.array([vv[i] for i in np.where((nivel == 0) & (grupo == g))[0]]) for g in seqs}
    null_med.append(adj_diff(d)[0])
null_med = np.array(null_med)
print("   nulo: mediana %.1f p5 %.1f  p(menor)=%.4f" % (null_med.mean(), np.percentile(null_med, 5),
      (1 + int((null_med <= obs_med).sum())) / (1 + NPERM)))

# ---------- D3 color ----------
print("\nD3 color en pendientes:")
p["es_ab"] = p.color.isin(["AB", "W:NB", "MB", "W:AB", "W:KB", "AB:MB"])
p["ab"] = (p.color == "AB").astype(int)
print("   AB en posicion 1 de grupo:", int(p[p.pos == 1].ab.sum()), "de", int((p.pos == 1).sum()))
print("   AB en otras posiciones:", int(p[p.pos > 1].ab.sum()), "de", int((p.pos > 1).sum()))
tab = [[int(p[p.pos == 1].ab.sum()), int((p.pos == 1).sum() - p[p.pos == 1].ab.sum())],
       [int(p[p.pos > 1].ab.sum()), int((p.pos > 1).sum() - p[p.pos > 1].ab.sum())]]
print("   Fisher exacto:", st.fisher_exact(tab))
print("   posiciones AB por grupo:", {int(g): sorted(s.pos[s.ab == 1].tolist()) for g, s in p.groupby("grupo")})

# periodicidad: mejor lag 2..15, fraccion de AB que caen en posiciones congruentes
def period_score(seq_pos, L):
    if len(seq_pos) < 2:
        return 0
    r = [x % L for x in seq_pos]
    return max(r.count(k) for k in set(r)) / len(r)
def stat_period(abpos):
    best = 0
    for L in range(2, 16):
        fr = [period_score(v, L) for v in abpos.values() if len(v) >= 2]
        if fr:
            best = max(best, np.mean(fr))
    return best
abpos = {int(g): sorted(s.pos[s.ab == 1].tolist()) for g, s in p.groupby("grupo")}
obs_per = stat_period(abpos)
print("   score de periodicidad observado: %.3f" % obs_per)
pr = p.reset_index(drop=True)
base_ab = pr.ab.values
posarr = pr.pos.values
grparr = pr.grupo.values
null_per = []
for _ in range(NPERM):
    sh = RNG.permutation(base_ab)
    ap = {}
    for g in np.unique(grparr):
        m = (grparr == g) & (sh == 1)
        ap[int(g)] = sorted(posarr[m].tolist())
    null_per.append(stat_period(ap))
null_per = np.array(null_per)
print("   nulo: media %.3f p95 %.3f  p=%.4f" % (null_per.mean(), np.percentile(null_per, 95),
      (1 + int((null_per >= obs_per).sum())) / (1 + NPERM)))

# ---------- D4 color-nivel ----------
ct = pd.crosstab(q.nivel, q.color.isin(["NB", "AB"]))
print("\nD4 color (NB/AB) x nivel:\n", ct.to_string())
sub = q[q.color.isin(["NB", "AB"])]
chi2, pchi, dof, _ = st.chi2_contingency(pd.crosstab(sub.nivel, sub.color))
print("   chi2=%.1f dof=%d p=%.2e" % (chi2, dof, pchi))

# ---------- D5 largo-valor ----------
r, pr = st.spearmanr(q.valor, q.largo)
print("\nD5 Spearman largo-valor: rho=%.3f p=%.2e (n=%d)" % (r, pr, n))
null_rho = []
for _ in range(NPERM):
    null_rho.append(st.spearmanr(RNG.permutation(val), q.largo.values)[0])
null_rho = np.array(null_rho)
print("   nulo: media %.3f p95 %.3f  p=%.4f" % (null_rho.mean(), np.percentile(null_rho, 95),
      (1 + int((null_rho >= r).sum())) / (1 + NPERM)))

# ---------- D6 primer pendiente mayor ----------
first_big = sum(1 for g, s in p.groupby("grupo") if len(s) > 1 and s.sort_values("orden").valor.iloc[0] == s.valor.max())
print("\nD6 primer pendiente es el maximo: %d de %d grupos" % (first_big, len(seqs)))
null_fb = []
for _ in range(NPERM):
    vv = RNG.permutation(val)
    k = 0
    for g, s in p.groupby("grupo"):
        if len(s) > 1:
            vs = np.array([vv[i] for i in s.sort_values("orden").index])
            k += int(vs[0] == vs.max())
    null_fb.append(k)
null_fb = np.array(null_fb)
print("   nulo: media %.2f p95 %.0f p=%.4f" % (null_fb.mean(), np.percentile(null_fb, 95),
      (1 + int((null_fb >= first_big).sum())) / (1 + NPERM)))

# ---------- D7 razon ~6.8 con estadistico maximo ----------
ch = {c: g for c, g in q.groupby("padre")}
ratios = []
for i, r_ in q[q.nivel == 0].iterrows():
    if r_.cuerda in ch and r_.valor > 0:
        s = ch[r_.cuerda].valor.sum()
        if s > 0:
            ratios.append(s / r_.valor)
ratios = np.array(ratios)
centers = np.arange(1.5, 12.0, 1.0)
def maxbin(rs):
    c = [int(((rs >= x - .5) & (rs < x + .5)).sum()) for x in centers]
    return max(c), centers[int(np.argmax(c))]
obs_max, obs_center = maxbin(ratios)
print("\nD7 razon: maximo en ventana de ancho 1 = %d en centro %.1f (n=%d ratios)" % (obs_max, obs_center, len(ratios)))
print("   ratios en 6.5-7.5:", int(((ratios >= 6.5) & (ratios <= 7.5)).sum()))
null_max = []
for _ in range(NPERM):
    vv = RNG.permutation(val)
    rr = []
    for i, r_ in q[q.nivel == 0].iterrows():
        if r_.cuerda in ch and vv[i] > 0:
            s = sum(vv[j] for j in q.index[q.padre == r_.cuerda])
            if s > 0:
                rr.append(s / vv[i])
    null_max.append(maxbin(np.array(rr))[0])
null_max = np.array(null_max)
print("   nulo max-ventana: media %.2f p95 %.0f  p=%.4f" % (null_max.mean(), np.percentile(null_max, 95),
      (1 + int((null_max >= obs_max).sum())) / (1 + NPERM)))
