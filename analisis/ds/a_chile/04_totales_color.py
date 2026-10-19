# -*- coding: utf-8 -*-
"""04: Totales cruzados, patrones de color, y runs entre quipus con valores raros."""
import pandas as pd, numpy as np, os, itertools
from collections import Counter

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]
c["v"] = pd.to_numeric(c.valor, errors="coerce")
sub = c[c.kfg.isin(CHILE)].copy()
rng = np.random.default_rng(0)

# --- totales ---
print("=== Totales y suma de grupos ===")
tot = sub.groupby("kfg")["v"].sum()
gsum = sub.groupby(["kfg", "grupo"])["v"].sum()
for kfg in CHILE:
    print(f"{kfg}: total={int(tot[kfg])}  suma-grupos(min/med/max)="
          f"{gsum[kfg].min():.0f}/{gsum[kfg].median():.0f}/{gsum[kfg].max():.0f}")

# valores de cuerdas por quipu (multiset)
vals = {k: sorted(sub[(sub.kfg == k) & (sub.v > 0)].v.astype(int).tolist()) for k in CHILE}
print("\n=== ¿el total o suma de grupo de A aparece como valor de cuerda en B? ===")
rows = []
for A in CHILE:
    cand = set(pd.to_numeric(gsum[A], errors="coerce").dropna().astype(int).tolist())
    cand.add(int(tot[A]))
    for B in CHILE:
        if A == B:
            continue
        vb = set(vals[B])
        hits = sorted(x for x in cand if x in vb and x > 0)
        if hits:
            rows.append(dict(A=A, B=B, hits=hits[:10], n=len(hits)))
for r in rows:
    print(r)

# --- Patrones de color ---
print("\n=== Patrones de color ===")
cseq = {}
for kfg in CHILE:
    g = sub[sub.kfg == kfg].sort_values("orden")
    base = g.color.astype(str).str.split(r"[:/\-]").str[0]
    cseq[kfg] = base.tolist()
print("colores base distintos por quipu:")
for k in CHILE:
    print(" ", k, Counter(cseq[k]).most_common(5))

def run_matches(a, b, L):
    sb = set(tuple(b[i:i + L]) for i in range(len(b) - L + 1))
    return sum(1 for i in range(len(a) - L + 1) if tuple(a[i:i + L]) in sb)

rows = []
for A, B in itertools.combinations(CHILE, 2):
    obs = {L: run_matches(cseq[A], cseq[B], L) + run_matches(cseq[B], cseq[A], L)
           for L in (2, 3, 4)}
    Lmax = 0
    for L in range(2, 10):
        if run_matches(cseq[A], cseq[B], L) > 0:
            Lmax = L
        else:
            break
    rows.append(dict(A=A, B=B, c2=obs[2], c3=obs[3], c4=obs[4], Lmax=Lmax))
R = pd.DataFrame(rows).sort_values("Lmax", ascending=False)
print("\ncolor runs top:")
print(R.head(12).to_string(index=False))

# --- Runs con valores raros (<=3 apariciones en la union de ambos) ---
print("\n=== Runs de valores 'raros' (freq<=2 en la union de ambos quipus) ===")

def rare_seq(v):
    cnt = Counter(v)
    return [x if (x > 0 and cnt[x] <= 2) else 0 for x in v]

rows = []
for A, B in itertools.combinations(CHILE, 2):
    ra, rb = rare_seq(vals[A]), rare_seq(vals[B])
    best = 0
    for L in range(2, 12):
        m = run_matches(ra, rb, L)
        if m:
            best = L
        else:
            break
    n2 = run_matches(ra, rb, 2) + run_matches(rb, ra, 2)
    rows.append(dict(A=A, B=B, rare_runs2=n2, rareLmax=best))
RR = pd.DataFrame(rows).sort_values(["rareLmax", "rare_runs2"], ascending=False)
print(RR.head(12).to_string(index=False))
