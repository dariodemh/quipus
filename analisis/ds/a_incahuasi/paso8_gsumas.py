# -*- coding: utf-8 -*-
"""Paso 8: k-gramas de SUMAS DE GRUPO entre quipus (nulo: barajar valores dentro del quipu);
firmas de tamano de grupo como multiconjunto; contraste JC vs UR."""
import pandas as pd, numpy as np, itertools
from collections import Counter, defaultdict
RAIZ = "./"
rng = np.random.default_rng(0); NPERM = 500
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]; ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
ci = ci.sort_values(["kfg", "orden"])
gvals, gsizes, gsums = {}, {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]; gr = list(d.groupby("grupo"))
    gvals[k] = [x.loc[~x["sin_nudos"], "valor"].astype(int).tolist() for _, x in gr]
    gsizes[k] = [int(len(x)) for _, x in gr]
    gsums[k] = [int(sum(v)) for v in gvals[k]]

def kpair(seqs, k):
    d = defaultdict(list)
    for kk, s in seqs.items():
        for i in range(len(s) - k + 1): d[tuple(s[i:i + k])].append(kk)
    pc = Counter()
    for kg, ks in d.items():
        if len(ks) >= 2:
            for a, b in itertools.combinations(sorted(set(ks)), 2): pc[(a, b)] += 1
    return sum(pc.values()), pc

print("k-gramas de SUMAS DE GRUPO compartidas:")
for k in (2, 3, 4):
    obs, opc = kpair(gsums, k)
    nulls = []
    for _ in range(NPERM):
        gs = {}
        for i in ids:
            flat = [v for x in gvals[i] for v in x]
            if not flat: gs[i] = []; continue
            pv = rng.permutation(flat); idx = 0; o = []
            for sz in gsizes[i]:
                o.append(int(pv[idx:idx + sz].sum())); idx += sz
            gs[i] = o
        s, _ = kpair(gs, k); nulls.append(s)
    nulls = np.array(nulls)
    print(f"  k={k}: obs={obs} nulo={nulls.mean():.1f} p={(1+(nulls>=obs).sum())/(1+NPERM):.4f}")

print("\nfirmas de tamanos de grupo como MULTICONJUNTO:")
sig = {k: tuple(sorted(gsizes[k])) for k in ids}
cnt = Counter(v for v in sig.values() if len(v) >= 2)
pairs = sum(v * (v - 1) // 2 for v in cnt.values())
print("  multiconjuntos repetidos:", {s: n for s, n in cnt.items() if n >= 2})
print("  n pares con mismo multiconjunto de tamanos:", pairs, "(de", len(ids) * (len(ids) - 1) // 2, ")")
# n de grupos identico
ng = Counter(len(gsizes[k]) for k in ids)
print("  quipus con mismo n de grupos:", {n: c for n, c in ng.items() if c >= 3})

print("\ncontraste JC vs UR:")
jc = [k for k in ids if k.startswith("JC")]; ur = [k for k in ids if k.startswith("UR")]
def summ(ks):
    n = sum(len(ci[ci.kfg == k]) for k in ks)
    sv = sum(len([1 for _ in [0]]) for k in ks)
    allv = [v for k in ks for v in ci[(ci.kfg == k) & ~ci.sin_nudos]["valor"].astype(int)]
    v = np.array(allv)
    tor = ci[ci.kfg.isin(ks)]["torsion"]
    un = ci[ci.kfg.isin(ks)]["union"]
    return (len(ks), n, round(float(v.mean()), 1) if len(v) else 0, int(v.max()) if len(v) else 0,
            round((tor == "Z").mean(), 2), round((un == "V").mean(), 2), round(float(ci[ci.kfg.isin(ks)]["sin_nudos"].mean()), 2))
print("  JC: n_quipus,cuerdas,valor_medio,valor_max,frac_Z,frac_V,frac_sin_nudos =", summ(jc))
print("  UR: n_quipus,cuerdas,valor_medio,valor_max,frac_Z,frac_V,frac_sin_nudos =", summ(ur))
