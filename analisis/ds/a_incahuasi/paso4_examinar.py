# -*- coding: utf-8 -*-
"""Paso 4: (a) inspecciona los pares con k-gramas de valor compartidos;
(b) control 'colapso de runs' (elimina artefacto de valores repetidos consecutivos);
(c) test B corregido (sumas de grupo bajo permutacion)."""
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
seqval, gsizes, gvals = {}, {}, {}
for k in ids:
    d = ci[ci["kfg"] == k]
    seqval[k] = d.loc[~d["sin_nudos"], "valor"].astype(int).tolist()
    gr = d.groupby("grupo")
    gsizes[k] = [int(len(x)) for _, x in gr]
    gvals[k] = [x.loc[~x["sin_nudos"], "valor"].astype(int).tolist() for _, x in gr]

def lcs(a, b):
    """longest common contiguous substring (valores)."""
    m = len(b); best = 0; bi = 0; bj = 0
    prev = [0] * (m + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]; bi = i - best; bj = j - best
        prev = cur
    return best, a[bi:bi + best] if best else []

def collapse(s):
    out = []
    for x in s:
        if not out or out[-1] != x:
            out.append(x)
    return out

# --- (a) pares significativos, su run comun mas largo ---
cand = [("UR260","UR272"),("UR263","UR267B"),("UR265","UR267B"),("JC009","UR262"),
        ("JC013","UR272"),("UR263","UR271"),("JC005","JC010"),("JC005","JC022"),
        ("JC012","UR260"),("JC013","UR260"),("JC011","UR260"),("JC005","JC011")]
print("pares candidatos: run comun mas largo (valores originales) y con runs colapsados")
for a, b in cand:
    n1, r1 = lcs(seqval[a], seqval[b])
    n2, r2 = lcs(collapse(seqval[a]), collapse(seqval[b]))
    print(f"{a:7s}-{b:7s} LCS={n1} {str(r1)[:60]:60s} | colapsado={n2} {str(r2)[:60]}")

# --- (b) test global con runs colapsados ---
def kgram_pairs(seqs, k):
    d = defaultdict(list)
    for kk, s in seqs.items():
        for i in range(len(s) - k + 1):
            d[tuple(s[i:i + k])].append(kk)
    pc = Counter()
    for kg, ks in d.items():
        if len(ks) >= 2:
            for a, b in itertools.combinations(sorted(set(ks)), 2):
                pc[(a, b)] += 1
    return sum(pc.values()), pc

def perm_test(seqs, k, label, collapse_runs=True):
    base0 = {k: (collapse(v) if collapse_runs else v) for k, v in seqs.items()}
    obs_S, obs_pc = kgram_pairs(base0, k)
    nullS = []
    for _ in range(NPERM):
        ps = {}
        for kk, v in seqs.items():
            pv = rng.permutation(v).tolist()
            ps[kk] = collapse(pv) if collapse_runs else pv
        s, _ = kgram_pairs(ps, k)
        nullS.append(s)
    nullS = np.array(nullS)
    print(f"[{label} k={k} colapso={collapse_runs}] obs_S={obs_S} nulo={nullS.mean():.1f} "
          f"p={(1+(nullS>=obs_S).sum())/(1+NPERM):.4f}")

print("\ntest A con runs COLAPSADOS (control del artefacto de repeticiones):")
for k in (3, 4, 5):
    perm_test(seqval, k, "valor", collapse_runs=True)
print("test A SIN colapsar (recordatorio):")
for k in (3, 4, 5):
    perm_test(seqval, k, "valor", collapse_runs=False)

# --- (c) test B corregido: suma de grupo vs valor de cuerda ---
val_by_quipu = {k: set(seqval[k]) for k in ids}
def cross_hits(gsums_now):
    tot = 0; hit = Counter()
    for i in ids:
        for g in gsums_now[i]:
            if g == 0: continue
            for j in ids:
                if j != i and g in val_by_quipu[j]:
                    tot += 1; hit[(i, j)] += 1
    return tot, hit
obs_g = {k: [sum(x) for x in gvals[k]] for k in ids}
obs_m, obs_hit = cross_hits(obs_g)
nullm = []
for _ in range(NPERM):
    ng = {}
    for k in ids:
        flat = list(np.concatenate([np.array(x) for x in gvals[k]])) if gvals[k] else []
        if not flat: ng[k] = gsizes[k] and [0]*len(gsizes[k]) or []; continue
        pv = rng.permutation(flat)
        out = []; idx = 0
        for sz in gsizes[k]:
            out.append(int(pv[idx:idx+sz].sum())); idx += sz
        ng[k] = out
    t, _ = cross_hits(ng); nullm.append(t)
nullm = np.array(nullm)
print(f"\nB) suma_grupo(i)==valor_cuerda(j): obs={obs_m} nulo={nullm.mean():.1f} "
      f"p={(1+(nullm>=obs_m).sum())/(1+NPERM):.4f}")
print("top pares:", obs_hit.most_common(6))
