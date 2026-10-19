# -*- coding: utf-8 -*-
"""UR006: patron de color periodico en los 24 grupos grandes + nulo."""
import pandas as pd, numpy as np, os
from collections import Counter
BASE = r"."; OUT = os.path.join(BASE, "analisis", "ds", "k_UR006")
u = pd.read_csv(os.path.join(OUT, "cuerdas_ur006.csv"))
big = sorted(u[u.nivel == 0].groupby("grupo_g").size().pipe(lambda s: s[s >= 20]).index.tolist())

# matriz colores por posicion
cols = [u[(u.grupo_g == g) & (u.nivel == 0)].sort_values("orden").color.tolist() for g in big]
maxn = max(len(c) for c in cols)
print("posiciones 1..%d : color modal y %acuerdo" % (maxn, 0))
for pos in range(maxn):
    vals = [c[pos] for c in cols if len(c) > pos]
    if vals:
        mc, n = Counter(vals).most_common(1)[0]
        print(f"pos{pos+1:2d} (mod4={ (pos)%4 }): n={len(vals):2d} modal={mc:7s} {n}/{len(vals)}  {dict(Counter(vals).most_common(3))}")

# test nulo: mide regularidad = fraccion de posiciones con >=80% de acuerdo en su modal
def score(color_lists):
    tot = 0; agree = 0
    for pos in range(maxn):
        vals = [c[pos] for c in color_lists if len(c) > pos]
        if vals:
            _, n = Counter(vals).most_common(1)[0]
            tot += 1; agree += n / len(vals)
    return agree / tot
obs = score(cols)
rng = np.random.default_rng(0)
allcol = [c for col in cols for c in col]
N = 1000; null = np.zeros(N)
for i in range(N):
    sh = list(rng.permutation(allcol))
    k = 0; cl = []
    for col in cols:
        cl.append(sh[k:k+len(col)]); k += len(col)
    null[i] = score(cl)
p = (1 + (null >= obs).sum()) / (N + 1)
print(f"\nscore regularidad color posicional: obs={obs:.3f} nulo_media={null.mean():.3f} sd={null.std():.3f} p={p:.4f}")

# residuo mod4: color modal por clase
print("\n-- color modal por clase mod 4 --")
for r in range(4):
    vals = [c[pos] for c in cols for pos in range(len(c)) if pos % 4 == r]
    print(f"mod4={r}: n={len(vals)} {dict(Counter(vals).most_common(5))}")
