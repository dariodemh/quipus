# -*- coding: utf-8 -*-
"""03 - Relaciones ENTRE los quipus AS+UR de Pachacamac.
Nulos: barajar valores/colores DENTRO de cada quipu, 500x, seed(0)."""
import random
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"
OUT.mkdir(exist_ok=True)
NPERM = 500

q = pd.read_csv(DAT / "quipus.csv")
c = pd.read_csv(DAT / "cuerdas.csv")
g = pd.read_csv(DAT / "grupos.csv")
m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
sub = q[m & q["kfg"].str.startswith(("AS", "UR"))].copy()
ids = sorted(sub["kfg"].tolist())
cc = c[c["kfg"].isin(ids)].copy()
gg = g[g["kfg"].isin(ids)].copy()

def valor_real(v, nudos):
    if pd.isna(v):
        return np.nan
    if v == 0 and (pd.isna(nudos) or str(nudos).strip() == ""):
        return np.nan
    return float(v)

# --- secuencias de colgantes (nivel 0) por quipu, en orden ---
seq_val = {}   # list con NaN donde ausente
seq_col = {}
for k in ids:
    rows = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    vals = [valor_real(r["valor"], r["nudos"]) for _, r in rows.iterrows()]
    cols = [r["color"] if isinstance(r["color"], str) else None for _, r in rows.iterrows()]
    seq_val[k] = vals
    seq_col[k] = cols

# --- k-mers de valores reales consecutivos (NaN corta la racha) ---
def kmers(seq, klen):
    out = set()
    run = []
    for x in seq:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            run = []
        else:
            run.append(x)
            if len(run) >= klen:
                out.add(tuple(run[-klen:]))
    return out

def shared_kmer_stat(seqs, klen, type_="val"):
    """n tipos de k-mer presentes en >=2 quipus; y n de pares que comparten >=1."""
    prop = defaultdict(set)  # kmer -> set quipus
    for k, s in seqs.items():
        for km in kmers(s, klen):
            prop[km].add(k)
    tipos = sum(1 for km, qs in prop.items() if len(qs) >= 2)
    pares = set()
    for km, qs in prop.items():
        if len(qs) >= 2:
            ql = sorted(qs)
            for i in range(len(ql)):
                for j in range(i + 1, len(ql)):
                    pares.add((ql[i], ql[j]))
    return tipos, len(pares), prop

for klen in (3, 4, 5):
    t_v, p_v, _ = shared_kmer_stat(seq_val, klen)
    t_c, p_c, _ = shared_kmer_stat(seq_col, klen)
    print(f"k={klen}: valores -> {t_v} k-mers compartidos, {p_v} pares;  colores -> {t_c} k-mers, {p_c} pares")

# --- Nulo: barajar valores/colores dentro de cada quipu ---
rng = np.random.default_rng(0)
def shuffle_seq(seq):
    idx = [i for i, x in enumerate(seq) if x is not None and not (isinstance(x, float) and np.isnan(x))]
    vals = [seq[i] for i in idx]
    rng.shuffle(vals)
    s = list(seq)
    for i, v in zip(idx, vals):
        s[i] = v
    return s

def null_dist(seqs, klen, which):
    out = []
    for _ in range(NPERM):
        sh = {k: shuffle_seq(s) for k, s in seqs.items()}
        t, p, _ = shared_kmer_stat(sh, klen, which)
        out.append((t, p))
    return np.array(out)

print("\n== Nulo (500) para k-mers compartidos ==")
res = {}
for which, seqs in (("val", seq_val), ("col", seq_col)):
    for klen in (3, 4, 5):
        obs_t, obs_p, _ = shared_kmer_stat(seqs, klen, which)
        nd = null_dist(seqs, klen, which)
        p_t = (1 + np.sum(nd[:, 0] >= obs_t)) / (1 + NPERM)
        p_p = (1 + np.sum(nd[:, 1] >= obs_p)) / (1 + NPERM)
        res[(which, klen)] = (obs_t, obs_p, nd[:, 0].mean(), nd[:, 0].std(), p_t, p_p)
        print(f"{which} k={klen}: obs tipos={obs_t} pares={obs_p} | nulo tipos={nd[:,0].mean():.1f}+-{nd[:,0].std():.1f} pares={nd[:,1].mean():.1f} | p_tipos={p_t:.3f} p_pares={p_p:.3f}")

# guardar los k-mers de valor compartidos (k=4, excl sin contar AS101 redundante)
_, _, prop4 = shared_kmer_stat(seq_val, 4)
compartidos = {km: sorted(qs) for km, qs in prop4.items() if len(qs) >= 2}
print(f"\nTipos de k-mer (k=4, valores) compartidos por >=2 quipus: {len(compartidos)}")
for km, qs in sorted(compartidos.items(), key=lambda x: -len(x[1]))[:15]:
    print("  ", km, "->", qs)
with open(OUT / "kmer_val_k4.csv", "w", encoding="utf-8") as f:
    f.write("kmer,quipus\n")
    for km, qs in sorted(compartidos.items()):
        f.write(",".join(str(x) for x in km) + ";" + "|".join(qs) + "\n")

# --- Test 2: el TOTAL de A aparece como suma de un bloque contiguo en B ---
# total real por quipu (suma de colgantes reales) y tambien suma de todas las cuerdas
tot_pen = {k: float(np.nansum([x for x in seq_val[k] if not (isinstance(x, float) and np.isnan(x))])) for k in ids}
allval = cc.groupby("kfg")["valor"]
def suma_total(k):
    rows = cc[cc["kfg"] == k]
    vs = [valor_real(r["valor"], r["nudos"]) for _, r in rows.iterrows()]
    return float(np.nansum(vs))
tot_all = {k: suma_total(k) for k in ids}

def bloques_hit(seq, target, tol=1e-9, minlen=2):
    """hay un bloque contiguo de valores reales (len>=minlen) que sume target?"""
    if target <= 0:
        return False
    n = len(seq)
    for i in range(n):
        s = 0.0
        for j in range(i, n):
            x = seq[j]
            if isinstance(x, float) and np.isnan(x):
                break
            s += x
            if j - i + 1 >= minlen and abs(s - target) < tol:
                return True
            if s > target + tol:
                break
    return False

print("\n== Totales de A que reaparecen como BLOQUE CONTIGUO (>=2 cuerdas) en B ==")
hit_all_obs = 0
detalle = []
for A in ids:
    ta = tot_pen[A]
    if ta <= 0:
        continue
    for B in ids:
        if A == B:
            continue
        if bloques_hit(seq_val[B], ta):
            hit_all_obs += 1
            detalle.append((A, B, ta))
print("Pares ordenados (A,B) con total(A) = bloque contiguo en B:", hit_all_obs)

# Nulo: barajar valores dentro de B (el total de A no cambia)
def null_total_hits(rep=NPERM):
    hits = []
    for _ in range(rep):
        sh = {k: shuffle_seq(s) for k, s in seq_val.items()}
        h = 0
        for A in ids:
            ta = tot_pen[A]
            if ta <= 0:
                continue
            for B in ids:
                if A == B:
                    continue
                if bloques_hit(sh[B], ta):
                    h += 1
        hits.append(h)
    return np.array(hits)

nd = null_total_hits()
p = (1 + np.sum(nd >= hit_all_obs)) / (1 + NPERM)
print(f"Nulo bloques: media={nd.mean():.1f} sd={nd.std():.1f} max={nd.max()} | p={p:.3f}")
print("Detalle observado (primeros 25):")
for A, B, ta in detalle[:25]:
    print(f"   total({A})={ta:.0f} aparece como bloque contiguo en {B}")
pd.DataFrame(detalle, columns=["A", "B", "total_A"]).to_csv(OUT / "totales_bloques.csv", index=False)

# --- Test 3 (multiset): total de A aparece como VALOR o como suma de grupo en B ---
valset = {k: set(np.round([x for x in seq_val[k] if not (isinstance(x, float) and np.isnan(x))], 6)) for k in ids}
gsum = {}
for k in ids:
    s = []
    for gr, rows in cc[cc["kfg"] == k].groupby("grupo"):
        vs = [valor_real(r["valor"], r["nudos"]) for _, r in rows.iterrows()]
        vs = [v for v in vs if not np.isnan(v)]
        if vs:
            s.append(round(float(sum(vs)), 6))
    gsum[k] = set(s)
hit_val = sum(1 for A in ids for B in ids if A != B and round(tot_pen[A], 6) in valset[B])
hit_gsum = sum(1 for A in ids for B in ids if A != B and round(tot_pen[A], 6) in gsum[B])
print(f"\n[multiset] total(A) aparece como VALOR en B: {hit_val} pares ordenados (nulo trivial, ver informe)")
print(f"[multiset] total(A) aparece como SUMA DE GRUPO en B: {hit_gsum} pares")

# --- Test 4: estructuras de grupo identicas ---
firma = {}
for k in ids:
    sizes = gg[gg["kfg"] == k].sort_values("grupo").apply(lambda r: int(r["hasta"] - r["desde"] + 1), axis=1).tolist()
    firma[k] = tuple(sizes)
sig = defaultdict(list)
for k, s in firma.items():
    sig[s].append(k)
rep = {s: ks for s, ks in sig.items() if len(ks) >= 2}
print(f"\n== Estructuras de grupo identicas (misma secuencia exacta de tamanos) ==")
print("n firmas repetidas:", len(rep))
for s, ks in sorted(rep.items(), key=lambda x: -len(x[1]))[:15]:
    print("  ", list(s), "->", ks)
# nulo: barajar los tamanos de grupo dentro de cada quipu
def null_sig(rep_n=NPERM):
    c = []
    for _ in range(rep_n):
        d = defaultdict(list)
        for k, s in firma.items():
            l = list(s)
            rng.shuffle(l)
            d[tuple(l)].append(k)
        c.append(sum(1 for s2, ks2 in d.items() if len(ks2) >= 2))
    return np.array(c)
nds = null_sig()
p4 = (1 + np.sum(nds >= len(rep))) / (1 + NPERM)
print(f"Nulo firmas repetidas: media={nds.mean():.1f} sd={nds.std():.1f} | obs={len(rep)} | p={p4:.3f}")

# --- Test 5: patrones de color a nivel de grupo ---
# firma de color = colores de los colgantes en orden, dentro de quipu
sigcol = defaultdict(list)
for k in ids:
    sigcol[tuple("x" if (x is None or (isinstance(x, float) and np.isnan(x))) else str(x) for x in seq_col[k])].append(k)
repc = {s: ks for s, ks in sigcol.items() if len(ks) >= 2}
print(f"\n== Secuencias de color de colgantes identicas ==")
print("n repetidas:", len(repc), " (ejemplos):")
for s, ks in list(repc.items())[:5]:
    print("   largo", len(s), "->", ks)
