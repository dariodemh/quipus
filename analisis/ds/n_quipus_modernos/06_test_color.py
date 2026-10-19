# -*- coding: utf-8 -*-
"""Convencion 'el color forma un orden fijo de categorias, compartido entre
quipus de la misma procedencia' (Anchucaya: 6 colores x 10 tareas; Collata:
color+fibra+ply como nombres). Se prueba en el corpus antiguo.

C1 similitud de bigramas de color entre quipus de la misma procedencia.
   Nulo: barajar los colores DENTRO de cada quipu (preserva la paleta y el
   numero de cuerdas; destruye solo el orden).
C2 concordancia de orden entre pares de colores (A antes que B).
C3 seriacion: bigramas de color repetidos >=3 veces dentro del quipu.
"""
import numpy as np
import pandas as pd
from itertools import combinations
from utils import load, describe, SEMILLA

rng = np.random.default_rng(SEMILLA)
B = 1000

c = load()
q = pd.read_csv(r"..\..\datos\quipus.csv")[["kfg", "procedencia"]]
p = c[(c.nivel == 0) & c.colfam.notna()].merge(q, on="kfg", how="left")
nq = p.groupby("kfg").size()
p = p[p.kfg.isin(nq[nq >= 8].index)]
prov_counts = p.groupby("procedencia").kfg.nunique()
provs = [x for x in prov_counts[prov_counts >= 5].index if x != "Unknown"]

blocks = {}
for k, d in p.groupby("kfg"):
    prov = d.procedencia.iloc[0]
    if prov not in provs:
        continue
    d = d.sort_values("orden")
    blocks[k] = dict(prov=prov, seq=d.colfam.values.copy())

by_prov = {pr: [k for k in blocks if blocks[k]["prov"] == pr] for pr in provs}


def bigrams(seq):
    return set(zip(seq[:-1], seq[1:]))


def jacc(a, b):
    if not a and not b:
        return np.nan
    return len(a & b) / len(a | b)


def runs(seq):
    out = []
    for x in seq:
        if not out or out[-1] != x:
            out.append(x)
    return out


def stats(seqs):
    """seqs: dict k -> secuencia (posiblemente barajada)."""
    c1 = {}
    for pr in provs:
        ks = by_prov[pr]
        vals = []
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                vals.append(jacc(bigrams(seqs[ks[i]]), bigrams(seqs[ks[j]])))
        c1[pr] = np.nanmean(vals) if vals else np.nan
    # C2: concordancia de orden de pares de colores
    c2 = {}
    for pr in provs:
        ks = by_prov[pr]
        # posicion media normalizada de cada color en cada quipu
        pos = {}
        for k in ks:
            s = seqs[k]
            for i, x in enumerate(s):
                pos.setdefault(x, []).append((k, i / max(1, len(s) - 1)))
        conc = []
        for a, b in combinations(sorted(pos), 2):
            ka = {k: v for k, v in pos[a]}
            kb = {k: v for k, v in pos[b]}
            common = set(ka) & set(kb)
            if len(common) < 3:
                continue
            wins = sum(1 for k in common if ka[k] < kb[k])
            n = len(common)
            conc.append(max(wins, n - wins) / n)
        c2[pr] = np.mean(conc) if conc else np.nan
    # C3: bigramas repetidos a nivel de cuerdas
    c3 = 0.0
    # C3b: bigramas repetidos a nivel de RUNS de color (seriacion real)
    c3b = 0.0
    for k, s in seqs.items():
        from collections import Counter
        cnt = Counter(zip(s[:-1], s[1:]))
        c3 += sum(1 for (a, b), n in cnt.items() if a != b and n >= 3)
        r = runs(list(s))
        cnt2 = Counter(zip(r[:-1], r[1:]))
        c3b += sum(1 for (a, b), n in cnt2.items() if a != b and n >= 3)
    return c1, c2, c3, c3b


seqs0 = {k: v["seq"] for k, v in blocks.items()}
c1_obs, c2_obs, c3_obs, c3b_obs = stats(seqs0)
# global: media de C1 sobre procedencias, media de C2, suma de C3
C1_obs = np.nanmean(list(c1_obs.values()))
C2_obs = np.nanmean(list(c2_obs.values()))

null = {"C1": [], "C2": [], "C3": [], "C3b": [], "C1_prov": {pr: [] for pr in provs},
        "C2_prov": {pr: [] for pr in provs}}
for it in range(B):
    seqs = {}
    for k, v in blocks.items():
        s = v["seq"].copy()
        rng.shuffle(s)
        seqs[k] = s
    c1, c2, c3, c3b = stats(seqs)
    null["C1"].append(np.nanmean(list(c1.values())))
    null["C2"].append(np.nanmean(list(c2.values())))
    null["C3"].append(c3)
    null["C3b"].append(c3b)
    for pr in provs:
        null["C1_prov"][pr].append(c1[pr])
        null["C2_prov"][pr].append(c2[pr])

rows = []
rows.append(dict(test="C1", descripcion="Jaccard de bigramas de color intra-procedencia",
                 obs=C1_obs, null_mean=np.mean(null["C1"]),
                 null_sd=np.std(null["C1"], ddof=1),
                 efecto_z=(C1_obs - np.mean(null["C1"])) / np.std(null["C1"], ddof=1),
                 p=(1 + np.sum(np.array(null["C1"]) >= C1_obs)) / (1 + B),
                 n_quipus=len(blocks), lado="greater"))
rows.append(dict(test="C2", descripcion="concordancia de orden entre pares de colores",
                 obs=C2_obs, null_mean=np.mean(null["C2"]),
                 null_sd=np.std(null["C2"], ddof=1),
                 efecto_z=(C2_obs - np.mean(null["C2"])) / np.std(null["C2"], ddof=1),
                 p=(1 + np.sum(np.array(null["C2"]) >= C2_obs)) / (1 + B),
                 n_quipus=len(blocks), lado="greater"))
rows.append(dict(test="C3b", descripcion="bigramas de RUNS de color repetidos >=3 (seriacion)", obs=c3b_obs, null_mean=np.mean(null["C3b"]), null_sd=np.std(null["C3b"], ddof=1), efecto_z=(c3b_obs - np.mean(null["C3b"])) / np.std(null["C3b"], ddof=1), p=(1 + np.sum(np.array(null["C3b"]) >= c3b_obs)) / (1 + B), n_quipus=len(blocks), lado="greater"))
rows.append(dict(test="C3", descripcion="bigramas de color repetidos >=3 (seriacion)",
                 obs=c3_obs, null_mean=np.mean(null["C3"]),
                 null_sd=np.std(null["C3"], ddof=1),
                 efecto_z=(c3_obs - np.mean(null["C3"])) / np.std(null["C3"], ddof=1),
                 p=(1 + np.sum(np.array(null["C3"]) >= c3_obs)) / (1 + B),
                 n_quipus=len(blocks), lado="greater"))
res = pd.DataFrame(rows)
res.to_csv("res_color_global.csv", index=False, encoding="utf-8-sig")

# por procedencia
pr_rows = []
for pr in provs:
    for test, obs, nk in [("C1", c1_obs[pr], null["C1_prov"][pr]),
                          ("C2", c2_obs[pr], null["C2_prov"][pr])]:
        pr_rows.append(dict(procedencia=pr, test=test, n_quipus=len(by_prov[pr]),
                            obs=obs, null_mean=np.mean(nk),
                            efecto_z=(obs - np.mean(nk)) / (np.std(nk, ddof=1) + 1e-12),
                            p=(1 + np.sum(np.array(nk) >= obs)) / (1 + B)))
pd.DataFrame(pr_rows).to_csv("res_color_procedencia.csv", index=False, encoding="utf-8-sig")

print(res.round(4).to_string())
print("\nPor procedencia:")
print(pd.DataFrame(pr_rows).round(4).to_string())
print("\nprocedencias", provs)
print("quipus", len(blocks))


# --- C3c: seriacion real = trigramas de RUNS repetidos, nulo barajando RUNS ---
from collections import Counter

def run_trigrams(seq):
    r = runs(list(seq))
    cnt = Counter(zip(r[:-1], r[1:], r[2:]))
    return sum(n - 1 for tri, n in cnt.items() if n >= 2)

obs_c3c = sum(run_trigrams(v["seq"]) for v in blocks.values())
null_c3c = []
for it in range(B):
    tot = 0
    for k, v in blocks.items():
        r = runs(list(v["seq"]))
        rng.shuffle(r)
        cnt = Counter(zip(r[:-1], r[1:], r[2:]))
        tot += sum(n - 1 for tri, n in cnt.items() if n >= 2)
    null_c3c.append(tot)
rows.append(dict(test="C3c", descripcion="trigramas de RUNS repetidos (seriacion vs orden aleatorio de bandas)",
                 obs=obs_c3c, null_mean=np.mean(null_c3c), null_sd=np.std(null_c3c, ddof=1),
                 efecto_z=(obs_c3c - np.mean(null_c3c)) / (np.std(null_c3c, ddof=1) + 1e-12),
                 p=(1 + np.sum(np.array(null_c3c) >= obs_c3c)) / (1 + B),
                 n_quipus=len(blocks), lado="greater"))
res = pd.DataFrame(rows)
res.to_csv("res_color_global.csv", index=False, encoding="utf-8-sig")
print("C3c obs", obs_c3c, "nulo", round(np.mean(null_c3c), 1), "p", round(rows[-1]["p"], 4))
