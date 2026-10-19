# -*- coding: utf-8 -*-
"""Subconjuntos: ?se ve la convencion de cria/proporcion en los khipus de
fibra de camelido (los mas parecidos a los de pastores modernos) y en la
clase tally de n_no_numericos? ?Y la seriacion de color solo en quipus con
paleta rica (>=4 colores)?"""
import numpy as np
import pandas as pd
from utils import load, describe, SEMILLA

rng = np.random.default_rng(SEMILLA)
B = 1000
c = load()

# --- subconjunto fibra camelido ---
p0 = c[(c.nivel == 0) & c.fibra.isin(["CL", "CN"])]
g = p0.groupby("kfg").fibra.agg(n="size", cl=lambda s: (s == "CL").sum())
clq = set(g[(g.n >= 5) & (g.cl / g.n >= 0.5)].index)
clase = pd.read_csv(r"..\n_no_numericos\quipus_clase.csv")
tally = set(clase.loc[clase["clase_limpia"] == 1, "kfg"])

print("quipus CL:", len(clq), "| tally:", len(tally), "| interseccion:", len(clq & tally))

# --- subsidiarias en subconjuntos ---
sub = c[(c.nivel > 0) & c.padre.notna()].copy()
mv = dict(zip(zip(c.kfg, c.cuerda), c.valor))
sub["mv"] = [mv.get((k, p), np.nan) for k, p in zip(sub.kfg, sub.padre)]
sub = sub.dropna(subset=["mv"])


def sub_test(qset, name):
    blocks = []
    for k, d in sub[sub.kfg.isin(qset)].groupby("kfg"):
        moms = []
        for p, dd in d.groupby("padre"):
            m = mv.get((k, p), np.nan)
            if np.isfinite(m):
                moms.append((float(m), dd.valor.fillna(0).values.astype(float)))
        if moms:
            blocks.append(moms)

    def stat(mvals_list):
        s1n = s1d = sn = sd = an = ad = 0.0
        for moms, mvals in zip(blocks, mvals_list):
            for (m0, kids), m in zip(moms, mvals):
                for kid in kids:
                    s1d += 1
                    s1n += kid < m
                    if m > 0:
                        for kk in range(2, 11):
                            sd += 1
                            sn += abs(kid - m / kk) < 1e-6
                ad += 1
                an += abs(np.sum(kids) - m) < 1e-6
        return dict(S1=s1n / s1d if s1d else np.nan, S3=sn / sd if sd else np.nan,
                    S4=an / ad if ad else np.nan)

    obs = stat([[m for m, _ in b] for b in blocks])
    null = {k: [] for k in ["S1", "S3", "S4"]}
    for it in range(B):
        mvls = []
        for b in blocks:
            v = np.array([m for m, _ in b], float)
            rng.shuffle(v)
            mvls.append(v)
        st = stat(mvls)
        for k in null:
            null[k].append(st[k])
    rows = []
    for k in ["S1", "S3", "S4"]:
        d = describe(obs[k], null[k], "greater")
        d.update(test=f"{k}_{name}", n_quipus=len(blocks))
        rows.append(d)
    return rows


rows = []
rows += sub_test(clq, "CL")
rows += sub_test(tally, "tally")
rows += sub_test(clq & tally, "CL_tally")

# --- torsion en CL: bloques ---
p = c[(c.nivel == 0) & c.twist.isin(["S", "Z"]) & c.kfg.isin(clq)]
blocks = []
for k, dd in p.groupby("kfg"):
    if len(dd) >= 5:
        blocks.append(dd.sort_values("orden").twist.values.copy())
if blocks:
    obs_t = sum(np.sum(x[1:] != x[:-1]) for x in blocks)
    null_t = []
    for it in range(B):
        tot = 0
        for x in blocks:
            y = x.copy()
            rng.shuffle(y)
            tot += np.sum(y[1:] != y[:-1])
        null_t.append(tot)
    d = describe(obs_t, null_t, "less")
    d.update(test="T1_CL", n_quipus=len(blocks))
    rows.append(d)

# --- seriacion de color en quipus con >=4 colores distintos ---
q = pd.read_csv(r"..\..\datos\quipus.csv")[["kfg", "procedencia"]]
pp = c[(c.nivel == 0) & c.colfam.notna()].merge(q, on="kfg", how="left")
rich = pp.groupby("kfg").colfam.nunique()
rich = set(rich[rich >= 4].index)
seqs = {}
for k, dd in pp[pp.kfg.isin(rich)].groupby("kfg"):
    if len(dd) >= 8:
        seqs[k] = dd.sort_values("orden").colfam.values.copy()


def run_tris(seq):
    r = []
    for x in seq:
        if not r or r[-1] != x:
            r.append(x)
    from collections import Counter
    cnt = Counter(zip(r[:-1], r[1:], r[2:]))
    return sum(n - 1 for n in cnt.values() if n >= 2)


obs_c = sum(run_tris(s) for s in seqs.values())
null_c = []
for it in range(B):
    tot = 0
    for s in seqs.values():
        r = []
        for x in s:
            if not r or r[-1] != x:
                r.append(x)
        rng.shuffle(r)
        from collections import Counter
        cnt = Counter(zip(r[:-1], r[1:], r[2:]))
        tot += sum(n - 1 for n in cnt.values() if n >= 2)
    null_c.append(tot)
d = describe(obs_c, null_c, "greater")
d.update(test="C3c_paleta_rica", n_quipus=len(seqs))
rows.append(d)

R = pd.DataFrame(rows)
R.to_csv("res_subconjuntos.csv", index=False, encoding="utf-8-sig")
print(R.round(4).to_string(index=False))
