# -*- coding: utf-8 -*-
"""Heaping global de valores frente a nulos explicitos.
   A) log-uniforme P(v) prop 1/v (el nulo que pide el encargo)
   B1) digitos uniformes dentro de cada longitud (1-9 / 0-9): "ningun numero favorito"
   B2) digitos independientes con marginales ajustadas DENTRO de cada longitud (>=2 digitos):
       conserva el sesgo de cada digito en cada posicion; aisla combinaciones favoritas
   C) uniforme dentro de (longitud, suma de digitos): control grueso del coste de nudos
Salida: tabla_heaping_global.csv + resumen por pantalla.
"""
import pandas as pd, numpy as np, os
from scipy import stats
from math import log10

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0]
N = len(k)
f = k.valor.value_counts()
vmax = int(k.valor.max())


def dig(v):
    return [int(x) for x in str(v)]


k["nd"] = k.valor.map(lambda v: len(str(v)))
n_len = k.nd.value_counts().to_dict()

# ---- A) log-uniforme ----
H = sum(1.0 / v for v in range(1, vmax + 1))
expA = {v: N * (1.0 / v) / H for v in f.index}

# ---- B1) digitos uniformes por longitud ----
expB1 = {v: n_len[len(str(v))] / (9 * 10 ** (len(str(v)) - 1)) for v in f.index}

# ---- B2) marginales ajustadas dentro de longitud ----
marg = {}
for L in sorted(k.nd.unique()):
    sub = k[k.nd == L]
    marg[L] = {pos: sub.valor.map(lambda v: dig(v)[pos]).value_counts(normalize=True).to_dict()
               for pos in range(L)}

def prob_B2(v):
    L = len(str(v))
    if L == 1:                       # 9 categorias: uniforme (B1)
        return 1.0 / 9
    p = 1.0
    for pos, d in enumerate(dig(v)):
        p *= marg[L][pos].get(d, 1e-12)
    return p

expB2 = {v: n_len[len(str(v))] * prob_B2(v) for v in f.index}

# ---- C) uniforme por (longitud, suma digitos) ----
from collections import defaultdict, Counter
estratos = defaultdict(list)
for v in range(1, vmax + 1):
    estratos[(len(str(v)), sum(dig(v)))].append(v)
tot_est = Counter()
for v in f.index:
    tot_est[(len(str(v)), sum(dig(v)))] += f[v]
expC = {v: tot_est[(len(str(v)), sum(dig(v)))] / len(estratos[(len(str(v)), sum(dig(v)))])
        for v in f.index}

# ---- tabla ----
res = []
for v, n in f.items():
    row = {"valor": int(v), "n": int(n), "quipus": int(k.loc[k.valor == v, "kfg"].nunique())}
    for nom, e in [("A", expA[v]), ("B1", expB1[v]), ("B2", expB2[v]), ("C", expC[v])]:
        row["exp_" + nom] = e
        row["ratio_" + nom] = n / e if e > 0 else np.nan
        row["p_" + nom] = stats.poisson.sf(n - 1, e) if e > 0 else 1.0
    row["n_estrato"] = len(estratos[(len(str(v)), sum(dig(v)))])
    res.append(row)
R = pd.DataFrame(res).sort_values("n", ascending=False)


def bh(p):
    p = np.asarray(p, float); m = len(p)
    o = np.argsort(p); q = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, p[o[i]] * m / (i + 1)); q[o[i]] = prev
    return q

for nom in ["A", "B1", "B2", "C"]:
    R["q" + nom] = bh(R["p_" + nom].values)
R.to_csv(OUT + r"\tabla_heaping_global.csv", index=False)

pd.set_option("display.width", 260)
print("N =", N, "| valores distintos =", len(f), "| quipus =", k.kfg.nunique())
print("\n=== TOP 30 por frecuencia ===")
print(R[["valor", "n", "quipus", "ratio_A", "ratio_B1", "ratio_B2", "ratio_C", "qB1", "qB2"]]
      .head(30).to_string(index=False, float_format=lambda x: f"{x:.3g}"))

print("\n=== mayores excesos sobre B1 (digitos uniformes), n>=100 ===")
S = R[R.n >= 100].sort_values("ratio_B1", ascending=False)
print(S[["valor", "n", "ratio_A", "ratio_B1", "ratio_B2", "ratio_C", "qB1"]].head(20)
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))

print("\n=== mayores excesos sobre B2 (marginales de digito), n>=100, >=2 digitos ===")
S2 = R[(R.n >= 100) & (R.valor >= 10)].sort_values("ratio_B2", ascending=False)
print(S2[["valor", "n", "ratio_B1", "ratio_B2", "ratio_C", "qB2"]].head(22)
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))

print("\n=== mayores DEFICITS sobre B1 (n>=100) ===")
S3 = R[R.n >= 100].sort_values("ratio_B1").head(12)
print(S3[["valor", "n", "ratio_B1", "ratio_B2", "qB1"]].to_string(index=False, float_format=lambda x: f"{x:.3g}"))

print("\nSobreviven BH q<0.05 y n>=100: A", ((R.qA < .05) & (R.n >= 100)).sum(),
      "| B1", ((R.qB1 < .05) & (R.n >= 100)).sum(),
      "| B2", ((R.qB2 < .05) & (R.n >= 100)).sum(),
      "| C", ((R.qC < .05) & (R.n >= 100)).sum())

# ---- Benford primer digito (v>=10) ----
kk = k[k.valor >= 10]
d1 = kk.valor.map(lambda v: int(str(v)[0]))
obs = d1.value_counts().reindex(range(1, 10), fill_value=0).values
exp = len(kk) * np.array([log10(1 + 1 / d) for d in range(1, 10)])
chi, p = stats.chisquare(obs, exp)
print("\n=== Benford primer digito (v>=10, n=%d) ===" % len(kk))
print("digito :", list(range(1, 10)))
print("obs    :", obs.tolist())
print("exp    :", np.round(exp, 0).astype(int).tolist())
print("chi2=%.1f df=8 p=%.3g" % (chi, p))
print("ratio obs/exp:", np.round(obs / exp, 2).tolist())

# ---- digitos por posicion ----
print("\ndigito de unidades, valores de 2 digitos (n=%d):" % (k.nd == 2).sum())
print(k[k.nd == 2].valor.map(lambda v: v % 10).value_counts().reindex(range(10), fill_value=0).to_string())
print("\ndigito de decenas, valores de 2 digitos:")
print(k[k.nd == 2].valor.map(lambda v: v // 10).value_counts().reindex(range(1, 10), fill_value=0).to_string())
print("\nlongitudes:", n_len, "| max =", vmax)
