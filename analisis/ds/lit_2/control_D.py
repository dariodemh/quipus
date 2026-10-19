# -*- coding: utf-8 -*-
"""Control adicional de D: direccion del efecto (¿S antes o despues?) y
medias nulas de los tres estadisticos. Semilla fija."""
import pandas as pd, numpy as np, re

D = r"./analisis/datos"
rng = np.random.default_rng(20261017)
c = pd.read_csv(D + r"\cuerdas.csv", low_memory=False)


def cd(s):
    ds = [d for _, d in re.findall(r"\(([\d.]+),([SZU])\)", str(s)) if d in ("S", "Z")]
    if not ds:
        return None
    return ds[0] if len(set(ds)) == 1 else "M"


c["cdir"] = c.nudos.apply(cd)
p = c[(c.nivel == 0) & c.cdir.isin(["S", "Z"])]
g = p.groupby("kfg").filter(lambda d: len(d) >= 6 and d.cdir.nunique() == 2)

data = []
signed = 0.0
s_later = 0
for k, d in g.groupby("kfg"):
    d = d.sort_values("orden")
    x = (d.cdir.values == "S").astype(float)
    _, gi = np.unique(d.grupo.values, return_inverse=True)
    data.append((x, gi, gi.max() + 1, np.arange(1, len(x) + 1)))
    n = len(x)
    dev = (np.arange(1, n + 1)[x == 1].mean() - (n + 1) / 2)
    signed += dev
    s_later += dev > 0


def st(x, gi, ng, r):
    runs_ = 1 + int(np.sum(x[1:] != x[:-1]))
    rk = abs(r[x == 1].mean() - (len(x) + 1) / 2) if x.sum() else 0.0
    s_g = np.bincount(gi, weights=x, minlength=ng)
    n_g = np.bincount(gi, minlength=ng)
    pbar = x.mean()
    return runs_, rk, float(np.sum(n_g * (s_g / n_g - pbar) ** 2))


obs = np.array([st(*d) for d in data]).sum(axis=0)
B = 3000
null = np.zeros((B, 3))
for b in range(B):
    acc = np.zeros(3)
    for x, gi, ng, r in data:
        acc += st(rng.permutation(x), gi, ng, r)
    null[b] = acc

print("quipus:", len(data))
print("obs: runs=%.0f  sum|dev|=%.1f  het_grupos=%.1f" % tuple(obs))
print("nulo (media): runs=%.0f  sum|dev|=%.1f  het_grupos=%.1f" % tuple(null.mean(axis=0)))
print("desviacion firmada (suma): %.1f  (media por quipu %.2f rangos)" % (signed, signed / len(data)))
print("quipus con S mas tarde que Z: %d/%d" % (s_later, len(data)))
print("p: runs=%.5f  |dev|=%.5f  het=%.5f" % (
    (np.sum(null[:, 0] <= obs[0]) + 1) / (B + 1),
    (np.sum(null[:, 1] >= obs[1]) + 1) / (B + 1),
    (np.sum(null[:, 2] >= obs[2]) + 1) / (B + 1)))
