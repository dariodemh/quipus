# -*- coding: utf-8 -*-
"""Controles para los dos efectos positivos del test de co-variacion:
 (1) torsion Z x color marcado: cuantos quipus y de que sitios;
 (2) nudo S x union V: estratificado por tipo de nudo y posicion decimal.
"""
import re
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng = np.random.default_rng(SEED)
d, q = prep.load()
q = q.set_index("kfg")
d0 = d[d.nivel == 0].copy()
d0["uniV"] = (d0.union2 == "V").astype(float).where(d0.union2.notna())
d0["torZ"] = (d0.torsion2 == "Z").astype(float).where(d0.torsion2.notna())
d0["crom"] = d0.cromatico
d0["site"] = d0.kfg.map(q.procedencia)


def cmh(df, a, b, strata=("kfg",), min_n=4):
    sub = df.dropna(subset=[a, b])
    rows = []
    for key, x in sub.groupby(list(strata)):
        n = len(x)
        if n < min_n or x[a].nunique() < 2 or x[b].nunique() < 2:
            continue
        rows.append((n, int(((x[a] == 1) & (x[b] == 1)).sum()),
                     int((x[a] == 1).sum()), int((x[b] == 1).sum())))
    t = pd.DataFrame(rows, columns=["n", "o11", "r1", "c1"])
    if len(t) == 0:
        return None
    t["e"] = t.r1 * t.c1 / t.n
    t["v"] = t.r1 * (t.n - t.r1) * t.c1 * (t.n - t.c1) / (t.n ** 2 * (t.n - 1))
    obs = ((t.o11 - t.e).sum()) ** 2 / t["v"].sum()
    null = np.empty(5000)
    n = t.n.values.astype(int); r1 = t.r1.values.astype(int); c1 = t.c1.values.astype(int)
    for i in range(5000):
        o = rng.hypergeometric(c1, n - c1, r1)
        e = r1 * c1 / n
        v = r1 * (n - r1) * c1 * (n - c1) / (n ** 2 * (n - 1))
        null[i] = ((o - e).sum()) ** 2 / v.sum()
    p = (1 + (null >= obs).sum()) / 5001
    return obs, null.mean(), p, len(t), int((np.sign(t.o11 - t.e) > 0).sum()), int((np.sign(t.o11 - t.e) < 0).sum())


print("=== Control 1: torsion Z x color marcado ===")
t = cmh(d0, "torZ", "crom")
print("global:", t)
sub = d0.dropna(subset=["torZ", "crom"])
quipus = sub.groupby("kfg").filter(lambda x: x.torZ.nunique() > 1 and x.crom.nunique() > 1)
print("quipus con variacion en ambos:", quipus.kfg.nunique())
print(quipus.groupby(["kfg", "site"]).size().to_string())
for excl in [["Playa Miller #6, Arica, Chile"], ["Playa Miller #6, Arica, Chile", "Chachapoyas", "Leymebamba"]]:
    s2 = quipus[~quipus.site.isin(excl)]
    print("excluyendo", excl, "->", cmh(s2, "torZ", "crom"))

print("\n=== Control 2: nudo S x union V, estratificado por tipo y posicion ===")
rows = []
for k, u, nudos in zip(d.kfg, d.union, d.nudos):
    if not isinstance(nudos, str):
        continue
    for m in re.finditer(r"(\d+)([A-Z]+)\(([\d.]+),([SZ])\),([\d.]+)", nudos):
        val = float(m.group(5))
        place = 0 if val < 10 else (1 if val < 100 else 2)
        rows.append((k, u, m.group(2), m.group(4), val, place))
kn = pd.DataFrame(rows, columns=["kfg", "union", "type", "dir", "val", "place"])
kn["S"] = (kn.dir == "S").astype(int)
kn["V"] = (kn.union == "V").astype(int)
kn = kn[kn.union.isin(["R", "V"])]
print("nudos:", len(kn), "| S:", kn.S.mean().round(3))
print(kn.groupby("type").S.agg(["mean", "size"]).round(3).to_string())
for strata in [("kfg",), ("kfg", "type"), ("kfg", "type", "place")]:
    print(strata, cmh(kn, "S", "V", strata=strata, min_n=6))
# solo nudos simples y largos
for tp in ["S", "L", "E"]:
    print("tipo", tp, cmh(kn[kn.type == tp], "S", "V", strata=("kfg",), min_n=6))
