# -*- coding: utf-8 -*-
"""Paridad 'neta': excluye unidades 0 (que son notación decimal, no pares).
Busca quipus y colores con exceso de unidades 2,4,6,8."""
import json
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, bh_holm

RNG = np.random.default_rng(99)
RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_salas2025"
c, q = cargar()
net = c[c.valida & (c.u != 0)].sort_values(["kfg", "orden"]).reset_index(drop=True)
net["par_net"] = net.u.isin([2, 4, 6, 8])
p0 = float(net.par_net.mean())
print("cuerdas netas", len(net), "p0", p0)

# ---------------------------------------------- quipus con exceso de pares
filas = []
for kfg, d in net.groupby("kfg"):
    n = len(d); k = int(d.par_net.sum())
    if n < 10:
        continue
    p = stats.binomtest(k, n, p0, alternative="two-sided").pvalue
    filas.append((kfg, n, k, k / n, p))
f = pd.DataFrame(filas, columns=["kfg", "n", "pares", "tasa", "p"])
f["p_bh"], _ = bh_holm(f.p.values)
f = f.sort_values("p")
print(f.head(15).to_string(index=False))
print("quipus n>=10:", len(f), "p<0.05:", int((f.p < 0.05).sum()),
      "BH<0.05:", int((f.p_bh < 0.05).sum()))
# exceso (una cola) para los candidatos
f["p_exc"] = [stats.binomtest(int(r.pares), int(r.n), p0, alternative="greater").pvalue
              for r in f.itertuples()]
f["p_exc_bh"], _ = bh_holm(f.p_exc.values)
cand = f[(f.p_exc_bh < 0.05)].copy()
for kfg in cand.kfg.head(12):
    d = net[net.kfg == kfg]
    print("\n", kfg, "n", len(d), "tasa", round(d.par_net.mean(), 3),
          "proc", q.loc[q.kfg == kfg, "procedencia"].values,
          "valores", d.v.value_counts().head(8).to_dict())
    print("  colores", d.color_base.value_counts().head(6).to_dict())

# ---------------------------------------------- color y paridad neta
codes, uniques = pd.factorize(net.color_base.astype(str).values)
K = len(uniques)
mask = np.bincount(codes, minlength=K)
colores = [uniques[k] for k in range(K) if mask[k] >= 200]
gid = pd.factorize(net.kfg)[0]
n = len(net)
flag = net.par_net.values.astype(float)
obs = np.bincount(codes, weights=flag, minlength=K)
B = 4000
perm = np.empty((B, K))
for b in range(B):
    fp = flag[np.lexsort((RNG.random(n), gid))]
    perm[b] = np.bincount(codes, weights=fp, minlength=K)
res = []
for color in colores:
    k = list(uniques).index(color)
    o = obs[k]; nn = mask[k]
    p_exc = (1 + int((perm[:, k] >= o).sum())) / (B + 1)
    res.append({"color": color, "n": int(nn), "tasa": float(o / nn),
                "nulo": float(perm[:, k].mean() / nn),
                "z": float((o - perm[:, k].mean()) / (perm[:, k].std(ddof=1) + 1e-9)),
                "p_exceso": float(p_exc)})
r = pd.DataFrame(res).sort_values("p_exceso")
r["p_bh"], _ = bh_holm(r.p_exceso.values)
print("\ncolor y paridad neta:")
print(r.head(10).to_string(index=False))

out = {"p0": p0, "n_cuerdas": int(len(net)), "quipus": f.head(30).to_dict("records"),
       "colores": r.to_dict("records")}
with open(OUT + r"\pares_neto.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
