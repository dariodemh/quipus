# -*- coding: utf-8 -*-
"""06 - Diseno "swap": mismos colores, distinto orden entre dos grupos.

Para cada par de grupos del mismo k con la MISMA multitud de colores pero
distinto orden, y cada par de posiciones (x,z) donde los colores se
intercambian, se compara:
  d_pos = (y_Ax-y_Bx)^2 + (y_Az-y_Bz)^2   -> el valor sigue a la posicion
  d_col = (y_Ax-y_Bz)^2 + (y_Az-y_Bx)^2   -> el valor sigue al color
Delta = d_pos - d_col > 0 favorece al color.
Nulo: permutar colores dentro de (quipu,k,pos) y re-identificar swaps.
Salida: swaps_test.csv, swaps_quipu.csv
"""
import sys
import warnings
from itertools import combinations
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)
NPERM = 299

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[(B.k >= 2) & (~B.ausente) & (~B.es_total)].copy()
vc = B.groupby(["kfg", "col3"]).size().rename("nc").reset_index()
B = B.merge(vc, on=["kfg", "col3"], how="left")
B["col3"] = np.where(B.nc >= 3, B.col3, "OTRO")
B["colcode"] = B.col3.astype("category").cat.codes

# preparar matrices por estrato
EST = []
for (kfg, k), g in B.groupby(["kfg", "k"]):
    us = sorted(g.grupo.unique())
    if len(us) < 2:
        continue
    pos = sorted(g.pos.unique())
    if pos != list(range(k)):
        continue
    m = len(us)
    seq = np.full((m, k), -1, int)
    yy = np.full((m, k), np.nan)
    aus = np.ones((m, k), bool)
    for i, u in enumerate(us):
        h = g[g.grupo == u]
        for _, r in h.iterrows():
            seq[i, r.pos] = r.colcode
            yy[i, r.pos] = r.y
            aus[i, r.pos] = r.ausente
    EST.append(dict(kfg=kfg, k=k, us=us, seq=seq, y=yy, aus=aus))


def deltas(seq, yy, aus):
    out = []
    m, k = seq.shape
    # buckets por multiset
    buck = {}
    for i in range(m):
        key = tuple(sorted(seq[i]))
        buck.setdefault(key, []).append(i)
    for key, ix in buck.items():
        if len(ix) < 2 or len(set(key)) < 2:
            continue
        for a, b in combinations(ix, 2):
            if np.array_equal(seq[a], seq[b]):
                continue
            for x in range(k):
                for z in range(x + 1, k):
                    if (seq[a, x] == seq[b, z] and seq[a, z] == seq[b, x]
                            and seq[a, x] != seq[a, z]
                            and not aus[a, x] and not aus[b, x]
                            and not aus[a, z] and not aus[b, z]):
                        d_pos = (yy[a, x] - yy[b, x]) ** 2 + (yy[a, z] - yy[b, z]) ** 2
                        d_col = (yy[a, x] - yy[b, z]) ** 2 + (yy[a, z] - yy[b, x]) ** 2
                        out.append((d_pos - d_col, seq[a, x], seq[a, z]))
    return out


def todos(permutar=False):
    res = []
    for e in EST:
        seq = e["seq"]
        if permutar:
            seq = seq.copy()
            for j in range(seq.shape[1]):
                seq[:, j] = rng.permutation(seq[:, j])
        for d, c1, c2 in deltas(seq, e["y"], e["aus"]):
            res.append((e["kfg"], d, c1, c2))
    return pd.DataFrame(res, columns=["kfg", "delta", "c1", "c2"])


obs = todos(False)
obs_mean = obs.delta.mean()
print("swaps observados:", len(obs), "quipus:", obs.kfg.nunique())
print("gana color: %d (%.3f) | delta medio %.4f (mediana %.4f)" %
      ((obs.delta > 0).sum(), (obs.delta > 0).mean(), obs_mean, obs.delta.median()),
      flush=True)

nul = []
for _ in range(NPERM):
    s = todos(True)
    nul.append(s.delta.mean() if len(s) else np.nan)
nul = np.array(nul, float)
nul = nul[np.isfinite(nul)]
p_color = (1 + np.sum(nul >= obs_mean)) / (len(nul) + 1)
print("nulo: delta medio %.4f (sd %.4f) | p(color mejor que posicion) = %.4f" %
      (nul.mean(), nul.std(), p_color), flush=True)

pq = obs.groupby("kfg").agg(n=("delta", "size"), delta=("delta", "mean"),
                            win=("delta", lambda s: (s > 0).mean())).reset_index()
pq = pq.sort_values("delta", ascending=False)
pq.to_csv(OUT + r"\swaps_quipu.csv", index=False)
pd.DataFrame([dict(n_swaps=len(obs), quipus=obs.kfg.nunique(),
                   win_color=float((obs.delta > 0).mean()), delta_medio=obs_mean,
                   nulo_media=nul.mean(), nulo_sd=nul.std(), p=p_color,
                   nperm=len(nul))]).to_csv(OUT + r"\swaps_test.csv", index=False)
print(pq.head(10).round(3).to_string(index=False))
