# -*- coding: utf-8 -*-
"""03b: repeticion de los tests entre-quipus restringiendo a patrones DISTINTIVOS
(valores >=5) y a runs de color NO monocromos, para descartar la explicacion
aburrida (1s ubicuos / bloques de un solo color). Nulo: barajar dentro de cada quipu.
"""
import pandas as pd, numpy as np, os
from collections import defaultdict
RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]
rng = np.random.default_rng(0); NPERM = 500
c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
c = c[c.kfg.isin(LE)].copy()
c["sn"] = c.nudos.isna() | (c.nudos.astype(str).str.strip().isin(["", "nan"]))
c["v"] = np.where(c.sn, np.nan, c.valor)
seqv, seqc = {}, {}
for k, s in c.groupby("kfg"):
    s = s.sort_values("orden"); col = s[s.nivel == 0]
    seqv[k] = col.v.tolist(); seqc[k] = col.color.fillna("?").astype(str).tolist()
K = sorted(seqv)

def count_val(seqs, L, minval):
    d = defaultdict(set)
    for i, a in enumerate(seqs):
        for t in range(len(a) - L + 1):
            g = a[t:t + L]
            if any(np.isnan(x) for x in g) or max(g) < minval:
                continue
            d[tuple(g)].add(i)
    return sum(len(s) * (len(s) - 1) // 2 for s in d.values())

def count_col(seqs, L, nonmono):
    d = defaultdict(set)
    for i, a in enumerate(seqs):
        for t in range(len(a) - L + 1):
            g = a[t:t + L]
            if nonmono and len(set(g)) < 2:
                continue
            d[tuple(g)].add(i)
    return sum(len(s) * (len(s) - 1) // 2 for s in d.values())

def test(fn, seqs, args):
    obs = fn(seqs, *args)
    null = np.empty(NPERM)
    for p in range(NPERM):
        sh = [list(rng.permutation(x)) for x in seqs]
        null[p] = fn(sh, *args)
    pval = (1 + np.sum(null >= obs)) / (1 + NPERM)
    return obs, null.mean(), null.std(), pval

tests = {
    "val_L3_min5": (count_val, [seqv[k] for k in K], (3, 5)),
    "val_L4_min5": (count_val, [seqv[k] for k in K], (4, 5)),
    "val_L3_min10": (count_val, [seqv[k] for k in K], (3, 10)),
    "col_L8_nonmono": (count_col, [seqc[k] for k in K], (8, True)),
    "col_L6_nonmono": (count_col, [seqc[k] for k in K], (6, True)),
}
rows = []
for name, (fn, seqs, args) in tests.items():
    o, m, sd, p = test(fn, seqs, args)
    rows.append((name, o, m, sd, p))
    print(f"{name}: obs={o} nulo={m:.2f}+-{sd:.2f} p={p:.4f}")
# Holm
ps = sorted([(r[4], r[0]) for r in rows]); m = len(ps); prev = 0; holm = {}
for i, (p, k) in enumerate(ps):
    adj = max(prev, min(1.0, (m - i) * p)); prev = adj; holm[k] = adj
print("Holm:", {k: round(v, 4) for k, v in holm.items()})
