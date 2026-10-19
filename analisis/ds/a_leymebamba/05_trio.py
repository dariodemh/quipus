# -*- coding: utf-8 -*-
"""05 (v2): test dirigido a las relaciones citadas en la literatura.
Urton 2005: UR6/UR9/UR21 cuentas duplicadas; UR9 y UR21 replican un segmento
de 4 meses de UR6 (~1/6). Familias CMA-628 y CMA-480.
Estadistico: L* = mayor L con una subsecuencia contigua de L valores compartida.
p-valor: fraccion de permutaciones (valores no nulos barajados dentro de cada
quipu, 500, semilla 0) con alguna subsecuencia compartida de longitud L*.
Eficiente: conjuntos de L-gramas.
"""
import pandas as pd, numpy as np, os
RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]
rng = np.random.default_rng(0); NPERM = 500

c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
c = c[c.kfg.isin(LE)].copy()
c["sn"] = c.nudos.isna() | (c.nudos.astype(str).str.strip().isin(["", "nan"]))
c["v"] = np.where(c.sn, np.nan, c.valor)
seq = {}
for k, s in c.groupby("kfg"):
    s = s.sort_values("orden"); col = s[s.nivel == 0]
    seq[k] = col.v.tolist()

def grams(a, L):
    out = set()
    for t in range(len(a) - L + 1):
        g = a[t:t + L]
        if any(np.isnan(x) for x in g):
            continue
        out.add(tuple(g))
    return out

def shares(a, b, L):
    return len(grams(a, L) & grams(b, L)) > 0

def lmax(a, b, cap=25):
    L = 1
    while L <= cap and shares(a, b, L):
        L += 1
    return L - 1

def perm_within(seqk):
    idx = [i for i, x in enumerate(seqk) if not np.isnan(x)]
    vals = [seqk[i] for i in idx]
    p = rng.permutation(vals)
    out = list(seqk)
    for i, v in zip(idx, p):
        out[i] = v
    return out

def test_pair(an, bn):
    a, b = seq[an], seq[bn]
    L = lmax(a, b)
    if L < 2:
        return L, a.index(a[-1]) if False else None, None, 1.0
    # localizar run
    ga = grams(a, L); gb = grams(b, L); common = ga & gb
    run = sorted(common)[0] if L <= 6 else None
    null = 0
    for p in range(NPERM):
        if shares(perm_within(a), perm_within(b), L):
            null += 1
    pval = (1 + null) / (1 + NPERM)
    return L, run, null, pval

pairs = [("UR006", "UR009"), ("UR006", "UR021"), ("UR009", "UR021"),
         ("UR001", "UR003"), ("UR004", "UR006"), ("UR011", "UR012"),
         ("UR002", "UR011"), ("UR012", "UR013"), ("UR005", "UR010"),
         ("UR017", "UR019"), ("UR016", "UR022"), ("UR010", "UR021")]
print("L*=subsecuencia contigua compartida mas larga; p = P(L*>=obs) bajo permutacion dentro de quipu (500):")
res = []
for a, b in pairs:
    L, run, null, p = test_pair(a, b)
    res.append((a, b, L, p))
    print(f"  {a}-{b}: L*={L} run={run} nulo_con_L*={null} p={p:.4f}")
ps = sorted([(r[3], (r[0], r[1])) for r in res]); m = len(ps); prev = 0; holm = {}
for i, (p, ko) in enumerate(ps):
    adj = max(prev, min(1.0, (m - i) * p)); prev = adj; holm[ko] = adj
print("Holm:", {k: round(v, 4) for k, v in holm.items()})
