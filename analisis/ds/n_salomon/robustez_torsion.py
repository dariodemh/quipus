"""Robustez de T2 (torsion): restringir a quipus con minoria >=20%."""
import numpy as np, pandas as pd
from scipy.stats import norm
RNG = np.random.default_rng(7)
d = pd.read_csv("analisis/datos/cuerdas.csv", low_memory=False)
d["tors"] = d.torsion.where(d.torsion.isin(["S", "Z"]))
lv0 = d[d.nivel == 0].sort_values(["kfg", "orden"])

def runs(x):
    x = np.asarray(x)
    return 1 + int(np.sum(x[1:] != x[:-1]))

for thresh in (0.0, 0.2, 0.3):
    zr, zh, rat, dif, n = [], [], [], [], 0
    for kfg, g in lv0.groupby("kfg"):
        t = g.tors.dropna().values
        if len(t) < 8 or len(set(t)) < 2:
            continue
        pmin = min((t == "S").mean(), (t == "Z").mean())
        if pmin < thresh or pmin == 0:
            continue
        n += 1
        obs = runs(t); perm = np.empty(1000); v = t.copy()
        for i in range(1000):
            RNG.shuffle(v); perm[i] = runs(v)
        if perm.std() > 0:
            zr.append((obs - perm.mean()) / perm.std()); rat.append(obs / perm.mean())
        h = len(t) // 2
        o = abs((t[:h] == "S").mean() - (t[h:] == "S").mean())
        pp = np.empty(1000); v = t.copy()
        for i in range(1000):
            RNG.shuffle(v); pp[i] = abs((v[:h] == "S").mean() - (v[h:] == "S").mean())
        if pp.std() > 0:
            zh.append((o - pp.mean()) / pp.std()); dif.append(o)
    zr, zh = np.array(zr), np.array(zh)
    print(f"minoria>={thresh}: n={n} | rachas: Z={zr.sum()/np.sqrt(len(zr)):.2f} "
          f"ratio_med={np.median(rat):.3f} frac_z<-2={np.mean(zr<-2):.2f} | "
          f"mitades: Z={zh.sum()/np.sqrt(len(zh)):.2f} dif_med={np.median(dif):.3f} "
          f"frac_z>2={np.mean(zh>2):.2f}")
