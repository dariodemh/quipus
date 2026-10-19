# -*- coding: utf-8 -*-
"""Bootstrap por quipu del exceso global (ratio obs/esperado bajo B2).
Reestima el nulo de digitos en cada muestra para no tratar las cuerdas como independientes."""
import pandas as pd, numpy as np, os
from scipy import stats

RUTA = r"./analisis/datos"
rng = np.random.default_rng(20261018)
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)


def dig(v): return [int(x) for x in str(v)]


def ratio_B2(df, v):
    f = pd.Series(df.valor.values).value_counts()
    if v not in f.index: return np.nan
    L = df.valor.map(lambda x: len(str(x)))
    nL = L.value_counts().to_dict()
    l = len(str(v))
    if l == 1:
        e = nL.get(1, 0) / 9
    else:
        pr = 1.0
        sub = df[L == l]
        for p, d in enumerate(dig(v)):
            pr *= (sub.valor.map(lambda x: dig(x)[p]) == d).mean()
        e = nL.get(l, 0) * pr
    return f[v] / e if e > 0 else np.nan


qids = sorted(k.kfg.unique())
grupos = {q: g for q, g in k.groupby("kfg")}
objetivo = [1, 2, 5, 10, 12, 15, 20, 30, 50, 100, 110, 200, 47, 33, 22]
obs = {v: ratio_B2(k, v) for v in objetivo}
B = 300
res = {v: [] for v in objetivo}
for b in range(B):
    m = rng.choice(qids, size=len(qids), replace=True)
    df = pd.concat([grupos[q] for q in m], ignore_index=True)
    for v in objetivo:
        res[v].append(ratio_B2(df, v))

print("valor   ratio   IC95% bootstrap (por quipu)")
out = []
for v in objetivo:
    a = np.array(res[v], float)
    out.append({"valor": v, "ratio": obs[v], "lo": np.nanpercentile(a, 2.5), "hi": np.nanpercentile(a, 97.5)})
    print(f"{v:>5} {obs[v]:>6.2f}   [{np.nanpercentile(a,2.5):.2f}, {np.nanpercentile(a,97.5):.2f}]")
pd.DataFrame(out).to_csv(os.path.dirname(os.path.abspath(__file__)) + r"\tabla_bootstrap.csv", index=False)
