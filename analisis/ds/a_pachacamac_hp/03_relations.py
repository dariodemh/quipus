"""Relaciones ENTRE los quipus HP001-HP032 con nulos de permutacion.
Metricas:
  A) alineacion posicional de VALORES (mismo valor en la misma posicion ordinal entre dos quipus)
  B) suma de grupo de un quipu que aparece como valor en otro quipu
  C) estructura de grupos identica (vector cuerdas-por-grupo)
  D) alineacion posicional de COLOR base
Nulo: barajar valores (o colores) dentro de cada quipu, 500 veces, semilla 0.
"""
import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter

rng = np.random.default_rng(0)
RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()

def has_knot(s):
    return s.notna() & (s != "") & (s != "[]")

hp["tiene"] = has_knot(hp.nudos)
hp["v"] = pd.to_numeric(hp.valor, errors="coerce")

# secuencias ordenadas por 'orden'
seqs, groupsz, colseq = {}, {}, {}
for k in HP:
    d = hp[hp.kfg == k].sort_values("orden")
    seqs[k] = d["v"].to_numpy(dtype=float)  # NaN donde sin nudo
    gs = d.groupby("grupo", sort=True).size().to_numpy()
    groupsz[k] = gs
    colseq[k] = d["color"].fillna("").astype(str).to_numpy()

def col_base(s):
    import re
    m = re.findall(r"[A-Z]{1,3}", str(s))
    return m[0] if m else ""
colseq = {k: np.array([col_base(x) for x in v]) for k, v in colseq.items()}

pairs = list(combinations(HP, 2))

def aligned_matches(seqA, seqB):
    n = min(len(seqA), len(seqB))
    a, b = seqA[:n], seqB[:n]
    m = ~np.isnan(a) & ~np.isnan(b) & (a == b) & (a > 0)
    return int(m.sum())

# ===== Metrica A: alineacion de valores =====
obs_A = sum(aligned_matches(seqs[a], seqs[b]) for a, b in pairs)
# por par
per_pair_A = {p: aligned_matches(seqs[p[0]], seqs[p[1]]) for p in pairs}
# nulo
null_A = []
perm_seqs = {k: seqs[k].copy() for k in HP}
for _ in range(500):
    for k in HP:
        rng.shuffle(perm_seqs[k])
    null_A.append(sum(aligned_matches(perm_seqs[a], perm_seqs[b]) for a, b in pairs))
null_A = np.array(null_A)
p_A = (np.sum(null_A >= obs_A) + 1) / (len(null_A) + 1)
print("== Metrica A: alineacion posicional de VALORES ==")
print(f"obs total={obs_A}  nulo media={null_A.mean():.1f} sd={null_A.std():.1f} max={null_A.max()}  p={p_A:.4f}")
top = sorted(per_pair_A.items(), key=lambda x: -x[1])[:8]
print("top pares:", [(f"{a}-{b}", v) for (a, b), v in top if v > 0])

# ===== Metrica B: suma de grupo que aparece en otro quipu =====
def group_sums(k):
    d = hp[hp.kfg == k]
    out = []
    for gg, sub in d.groupby("grupo"):
        s = pd.to_numeric(sub.valor, errors="coerce").sum()
        out.append(s)
    return np.array(out, dtype=float)

gsums = {k: group_sums(k) for k in HP}
valset = {k: set(np.round(seqs[k][~np.isnan(seqs[k])]).astype(int)) for k in HP}

def count_hits(gs, vs):
    return sum(1 for x in gs if not np.isnan(x) and int(round(x)) in vs and x > 0)

pairs_B = [(a, b) for a in HP for b in HP if a != b]
per_pair_B = {(a, b): count_hits(gsums[a], valset[b]) for a, b in pairs_B}
obs_B = sum(per_pair_B.values())  # suma de grupo de A aparece como valor en B, a!=b

def betw_hits(gsums_d, valset_d):
    return sum(1 for a in HP for b in HP if a != b
               for x in gsums_d[a] if not np.isnan(x) and x > 0 and int(round(x)) in valset_d[b])

# nulo: barajar valores dentro de cada quipu (recomputa gsums Y valset de cada quipu)
null_B = []
for _ in range(500):
    gs_d, vs_d = {}, {}
    for k in HP:
        vv = seqs[k].copy(); rng.shuffle(vv)
        d = hp[hp.kfg == k].sort_values("orden").copy(); d["vs"] = vv
        gs_d[k] = np.array([np.nansum(sub["vs"].to_numpy(dtype=float))
                            for _, sub in d.groupby("grupo")], dtype=float)
        vs_d[k] = set(np.round(vv[~np.isnan(vv)]).astype(int))
    null_B.append(betw_hits(gs_d, vs_d))
null_B = np.array(null_B)
p_B = (np.sum(null_B >= obs_B) + 1) / (len(null_B) + 1)
print("\n== Metrica B: suma de grupo de A que aparece como valor en OTRO quipu B ==")
print(f"obs={obs_B} nulo media={null_B.mean():.1f} sd={null_B.std():.1f} p={p_B:.4f}")
topB = sorted(per_pair_B.items(), key=lambda x: -x[1])[:8]
print("top pares A->B:", [(f"{a}->{b}", v) for (a, b), v in topB if v > 0])

# ===== Metrica B2 (interna): alguna cuerda = suma de un grupo contiguo de colgantes =====
def subset_sum_hits(k):
    d = hp[hp.kfg == k].sort_values("orden")
    vals = d["v"].to_numpy(dtype=float)
    V = set(np.round(vals[~np.isnan(vals) & (vals > 0)]).astype(int))
    n = len(vals); found = 0
    for i in range(n):
        s = 0.0
        for j in range(i, min(i + 12, n)):
            if not np.isnan(vals[j]):
                s += vals[j]
            if j > i and s > 0 and int(round(s)) in V:
                found += 1
    return found
obsB2 = sum(subset_sum_hits(k) for k in HP)
nullB2 = []
for _ in range(500):
    tot = 0
    for k in HP:
        vv = seqs[k].copy(); rng.shuffle(vv)
        V = set(np.round(vv[~np.isnan(vv) & (vv > 0)]).astype(int))
        n = len(vv)
        for i in range(n):
            s = 0.0
            for j in range(i, min(i + 12, n)):
                if not np.isnan(vv[j]):
                    s += vv[j]
                if j > i and s > 0 and int(round(s)) in V:
                    tot += 1
    nullB2.append(tot)
nullB2 = np.array(nullB2)
p_B2 = (np.sum(nullB2 >= obsB2) + 1) / (len(nullB2) + 1)
print("\n== Metrica B2: cuerda contigua = suma de otra cuerda (interna, ventana<=12) ==")
print(f"obs={obsB2} nulo media={nullB2.mean():.1f} sd={nullB2.std():.1f} p={p_B2:.4f}")

# ===== Metrica C: estructura de grupos identica =====
vec = {k: tuple(groupsz[k].tolist()) for k in HP}
combo_C = Counter(vec.values())
same = {v: n for v, n in combo_C.items() if n > 1}
print("\n== Metrica C: estructura de grupos IDENTICA ==")
print("combinaciones repetidas:", same if same else "ninguna")
# pares con misma estructura
ident = [(a, b) for a, b in pairs if vec[a] == vec[b]]
print("pares identicos:", ident if ident else "ninguno")

# ===== Metrica D: alineacion de COLOR base =====
def aligned_col(A, B):
    n = min(len(A), len(B))
    return int(np.sum(A[:n] == B[:n]))
obs_D = sum(aligned_col(colseq[a], colseq[b]) for a, b in pairs)
per_pair_D = {p: aligned_col(colseq[p[0]], colseq[p[1]]) for p in pairs}
null_D = []
pc = {k: colseq[k].copy() for k in HP}
for _ in range(500):
    for k in HP:
        rng.shuffle(pc[k])
    null_D.append(sum(aligned_col(pc[a], pc[b]) for a, b in pairs))
null_D = np.array(null_D)
p_D = (np.sum(null_D >= obs_D) + 1) / (len(null_D) + 1)
print("\n== Metrica D: alineacion posicional de COLOR base ==")
print(f"obs={obs_D} nulo media={null_D.mean():.1f} sd={null_D.std():.1f} p={p_D:.4f}")
topD = sorted(per_pair_D.items(), key=lambda x: -x[1])[:8]
print("top pares:", [(f"{a}-{b}", v) for (a, b), v in topD if v > 0])

# guardar pares con mas coincidencias de valor
res = pd.DataFrame([dict(a=a, b=b, val_match=per_pair_A[(a, b)],
                         col_match=per_pair_D[(a, b)],
                         sumaAB=per_pair_B.get((a, b), 0),
                         sumaBA=per_pair_B.get((b, a), 0)) for a, b in pairs])
res.sort_values(["val_match", "col_match"], ascending=False).to_csv("pares.csv", index=False)
print("\nGuardado pares.csv")
