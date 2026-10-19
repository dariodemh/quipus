# -*- coding: utf-8 -*-
"""Paso 3: relaciones ENTRE quipus de Incahuasi.
Tests: (A) k-gramas de valores compartidos, (B) totales/sumas de grupo cruzados,
(C) firmas de estructura de grupos, (D) k-gramas de color.
Nulo: barajar valores (o colores) DENTRO de cada quipu, 500 veces, semilla 0.
"""
import pandas as pd, numpy as np, itertools
from collections import Counter, defaultdict

RAIZ = "./"
rng = np.random.default_rng(0)
NPERM = 500

q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]
ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
ci = ci.sort_values(["kfg", "orden"])

# secuencias
seqval, seqcol, gsizes, gsums = {}, {}, {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]
    rv = d.loc[~d["sin_nudos"], "valor"].astype(int).tolist()
    seqval[k] = rv
    seqcol[k] = d.loc[d["nivel"] == 0, "color"].fillna("?").str.split("-").str[0].str.split(":").str[0].tolist()
    gr = d.groupby("grupo")
    gsizes[k] = [int(len(x)) for _, x in gr]
    gsums[k] = [int(x.loc[~x["sin_nudos"], "valor"].sum()) for _, x in gr]

pairs = [tuple(sorted(p)) for p in itertools.combinations(ids, 2)]

def kgram_pairs(seqs, k):
    """devuelve (S total incidencias, dict pair->count) para k-gramas compartidos."""
    d = defaultdict(list)
    for kk, s in seqs.items():
        for i in range(len(s) - k + 1):
            d[tuple(s[i:i + k])].append(kk)
    S = 0
    pc = Counter()
    for kg, ks in d.items():
        if len(ks) >= 2:
            for a, b in itertools.combinations(sorted(set(ks)), 2):
                pc[(a, b)] += 1
    S = sum(pc.values())
    return S, pc

def perm_test(seqs, k, label):
    obs_S, obs_pc = kgram_pairs(seqs, k)
    tested = {p: o for p, o in obs_pc.items() if o > 0}
    ge = Counter()
    nullS = []
    keys = list(seqs.keys())
    base = {kk: np.array(seqs[kk]) if len(seqs[kk]) else np.array([], dtype=int) for kk in keys}
    for _ in range(NPERM):
        ps = {kk: (rng.permutation(base[kk]).tolist() if len(base[kk]) else []) for kk in keys}
        s, pc = kgram_pairs(ps, k)
        nullS.append(s)
        for p, o in tested.items():
            if pc.get(p, 0) >= o:
                ge[p] += 1
    nullS = np.array(nullS)
    pS = (1 + (nullS >= obs_S).sum()) / (1 + NPERM)
    print(f"[{label} k={k}] obs_S={obs_S}  nulo_media={nullS.mean():.1f}  p_S={pS:.4f}  "
          f"pares_con>=1_compartido={len(tested)}")
    # p-valores por par + BH
    pv = {p: (1 + ge[p]) / (1 + NPERM) for p in tested}
    if pv:
        items = sorted(pv.items(), key=lambda x: x[1])
        m = len(items)
        sig = []
        for rank, (p, pv_) in enumerate(items, 1):
            qv = pv_ * m / rank  # BH
            if pv_ <= 0.05 * rank / m:
                sig.append((p, obs_pc[p], pv_))
        print(f"    pares significativos BH 0.05: {len(sig)}")
        for p, o, pv_ in sig[:12]:
            print(f"      {p} n_gk={o} p={pv_:.4f}")
    return obs_pc, pv

print("=== A) k-gramas de VALORES compartidos entre quipus ===")
for k in (3, 4, 5):
    perm_test(seqval, k, "valores")

print("\n=== C) FIRMA de estructura de grupos (n cuerdas por grupo) ===")
sig = {k: tuple(gsizes[k]) for k in ids}
cnt = Counter(s for s in sig.values() if len(s) >= 2)
obs_pairs = sum(v * (v - 1) // 2 for v in cnt.values())
print("firmas repetidas (>=2 quipus):", {s: n for s, n in cnt.items() if n >= 2})
print("n pares con firma identica:", obs_pairs)
# nulo: repartir cuerdas al azar en n_grupos grupos
nullC = []
for _ in range(NPERM):
    cc = Counter()
    for k in ids:
        n = len(ci[ci["kfg"] == k]); ng = len(gsizes[k])
        if ng == 0: continue
        sizes = np.bincount(rng.integers(0, ng, n), minlength=ng)
        t = tuple(sizes)
        if len(t) >= 2: cc[t] += 1
    nullC.append(sum(v * (v - 1) // 2 for v in cc.values()))
nullC = np.array(nullC)
print("nulo firma: media", round(nullC.mean(), 1), "p=", (1 + (nullC >= obs_pairs).sum()) / (1 + NPERM))

print("\n=== B) SUMAS de grupo de un quipu == valor de cuerda de otro ===")
# indices
val_by_quipu = {k: set(seqval[k]) for k in ids}
def cross_matches():
    # cuenta pares (grupo de i, cord de j), i!=j, con suma de grupo == valor
    tot = 0
    hit = Counter()
    for i in ids:
        for g in gsums[i]:
            if g == 0: continue
            for j in ids:
                if j == i: continue
                if g in val_by_quipu[j]:
                    tot += 1; hit[(i, j)] += 1
    return tot, hit
obs_m, obs_hit = cross_matches()
nullm = []
for _ in range(NPERM):
    sv = {k: set(rng.permutation(seqval[k]).tolist()) if seqval[k] else set() for k in ids}
    t = 0
    for i in ids:
        for g in gsums[i]:
            if g == 0: continue
            for j in ids:
                if j != i and g in sv[j]:
                    t += 1
    nullm.append(t)
nullm = np.array(nullm)
print(f"obs={obs_m}  nulo_media={nullm.mean():.1f}  p={(1+(nullm>=obs_m).sum())/(1+NPERM):.4f}")
print("top pares (i=gsuma de i, j=cord de j):", obs_hit.most_common(8))

print("\n=== D) k-gramas de COLOR compartidos (cuerdas nivel 0) ===")
for k in (3, 4):
    perm_test(seqcol, k, "color")
