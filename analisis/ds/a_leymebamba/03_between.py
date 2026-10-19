# -*- coding: utf-8 -*-
"""03: relaciones ENTRE quipus UR001-UR022 con nulo de permutacion (semilla 0).
Estadisticos:
 (a) subsecuencias contiguas de valores compartidas (L=3,4,5) entre pares -> nulo: barajar valores dentro de cada quipu.
 (b) totales de un quipu presentes como valor en otro -> nulo: permutar valores entre quipus.
 (c) patrones de color compartidos (seq>=4) -> nulo: barajar colores dentro de cada quipu.
 (d) firmas de grupos iguales -> nulo: permutar etiquetas de grupo dentro de cada quipu.
Holm sobre la familia de tests.
"""
import pandas as pd, numpy as np, os

RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]
rng = np.random.default_rng(0)
NPERM = 500

c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
c = c[c.kfg.isin(LE)].copy()
c["sin_nudos"] = c.nudos.isna() | (c.nudos.astype(str).str.strip().isin(["", "nan"]))
c["valor_real"] = np.where(c.sin_nudos, np.nan, c.valor)

# secuencias de colgantes (nivel 0) en orden, y colores
seqv, seqc, grp = {}, {}, {}
for kfg, sub in c.groupby("kfg"):
    sub = sub.sort_values("orden")
    col = sub[sub.nivel == 0]
    seqv[kfg] = col.valor_real.tolist()
    seqc[kfg] = col.color.fillna("?").astype(str).tolist()
    grp[kfg] = col.grupo.fillna(-1).astype(int).tolist()
K = sorted(seqv)
print("n quipus:", len(K), " nulos:", NPERM, " semilla 0")

def shared_subseq_count(seqs, L):
    """pares (A,B) A<B con >=1 subsecuencia contigua de longitud L compartida.
    Eficiente: diccionario L-grama -> n. de quipus que lo contienen."""
    from collections import defaultdict
    d = defaultdict(set)
    for i, a in enumerate(seqs):
        for t in range(len(a) - L + 1):
            g = a[t:t + L]
            if any(np.isnan(x) for x in g):
                continue
            d[tuple(g)].add(i)
    return sum(len(s) * (len(s) - 1) // 2 for s in d.values())

def total_match_count(seqs):
    """pares (A,B) donde sum(A) aparece como valor en B"""
    tots = {k: int(round(np.nansum(v))) for k, v in seqs.items()}
    vals = {k: set(int(x) for x in v if not np.isnan(x)) for k, v in seqs.items()}
    n = 0
    for a in seqs:
        for b in seqs:
            if a != b and tots[a] in vals[b]:
                n += 1
    return n

# ---------- (a) subsecuencias ----------
res = {}
for L in (3, 4, 5):
    obs = shared_subseq_count([seqv[k] for k in K], L)
    null = np.empty(NPERM)
    for p in range(NPERM):
        sh = {k: list(rng.permutation(seqv[k])) for k in K}
        null[p] = shared_subseq_count([sh[k] for k in K], L)
    pval = (1 + np.sum(null >= obs)) / (1 + NPERM)
    res[f"subseq_L{L}"] = (obs, null.mean(), null.std(), pval)
    print(f"(a) L={L}: obs={obs} nulo={null.mean():.2f}+-{null.std():.2f} p={pval:.4f}")

# ---------- (b) totales (nulo: permutar valores entre quipus) ----------
obs_tot = total_match_count(seqv)
tot_pairs = sum(1 for a in K for b in K if a != b)
pool = [x for k in K for x in seqv[k]]
sizes = {k: len(seqv[k]) for k in K}
null = np.empty(NPERM)
for p in range(NPERM):
    perm = rng.permutation(pool)
    sh, idx = {}, 0
    for k in K:
        sh[k] = list(perm[idx:idx + sizes[k]]); idx += sizes[k]
    null[p] = total_match_count(sh)
pval_tot = (1 + np.sum(null >= obs_tot)) / (1 + NPERM)
res["totales"] = (obs_tot, null.mean(), null.std(), pval_tot)
print(f"(b) totales en otro quipu: obs={obs_tot}/{tot_pairs} nulo={null.mean():.2f}+-{null.std():.2f} p={pval_tot:.4f}")

# ---------- (c) patrones de color ----------
def shared_color(seqs, L):
    from collections import defaultdict
    d = defaultdict(set)
    for i, a in enumerate(seqs):
        for t in range(len(a) - L + 1):
            d[tuple(a[t:t + L])].add(i)
    return sum(len(s) * (len(s) - 1) // 2 for s in d.values())
for L in (4, 8):
    obs = shared_color([seqc[k] for k in K], L)
    null = np.empty(NPERM)
    for p in range(NPERM):
        sh = {k: list(rng.permutation(seqc[k])) for k in K}
        null[p] = shared_color([sh[k] for k in K], L)
    pval = (1 + np.sum(null >= obs)) / (1 + NPERM)
    res[f"color_L{L}"] = (obs, null.mean(), null.std(), pval)
    print(f"(c) color L={L}: obs={obs} nulo={null.mean():.2f}+-{null.std():.2f} p={pval:.4f}")

# ---------- (d) firmas de grupos iguales ----------
sigs = {k: tuple(sorted(pd.Series(grp[k]).value_counts().tolist(), reverse=True)) for k in K}
obs_sig = sum(1 for i in range(len(K)) for j in range(i + 1, len(K)) if sigs[K[i]] == sigs[K[j]])
null = np.empty(NPERM)
for p in range(NPERM):
    sh = {}
    for k in K:
        g = grp[k]
        sh[k] = tuple(sorted(pd.Series(rng.permutation(g)).value_counts().tolist(), reverse=True))
    null[p] = sum(1 for i in range(len(K)) for j in range(i + 1, len(K)) if sh[K[i]] == sh[K[j]])
pval_sig = (1 + np.sum(null >= obs_sig)) / (1 + NPERM)
res["firmas_grupo"] = (obs_sig, null.mean(), null.std(), pval_sig)
print(f"(d) firmas de grupo identicas: obs={obs_sig} nulo={null.mean():.2f}+-{null.std():.2f} p={pval_sig:.4f}")

# ---------- Holm ----------
ps = sorted([(v[3], k) for k, v in res.items()])
m = len(ps); holm = {}
prev = 0
for i, (p, k) in enumerate(ps):
    adj = min(1.0, (m - i) * p); adj = max(prev, adj); prev = adj
    holm[k] = adj
print("\nHolm (familia de", m, "tests):", {k: round(v, 4) for k, v in holm.items()})

# ---------- detalle de coincidencias ----------
print("\nDetalle (para informe):")
seqs = [seqv[k] for k in K]
for i in range(len(K)):
    for j in range(i + 1, len(K)):
        a, b = seqs[i], seqs[j]
        for L in (3, 4, 5):
            sa = {tuple(round(x, 6) for x in a[t:t + L]) for t in range(len(a) - L + 1)}
            sb = {tuple(round(x, 6) for x in b[t:t + L]) for t in range(len(b) - L + 1)}
            sa = {s for s in sa if not any(np.isnan(x) for x in s)}
            sb = {s for s in sb if not any(np.isnan(x) for x in s)}
            if sa & sb:
                print(f"  subseq L{L} {K[i]}-{K[j]}:", sorted(sa & sb)[:3])
                break
# totales
tots = {k: int(round(np.nansum(seqv[k]))) for k in K}
for a in K:
    hits = [b for b in K if b != a and tots[a] in [int(x) for x in seqv[b] if not np.isnan(x)]]
    print(f"  total({a})={tots[a]} aparece en {hits}")
