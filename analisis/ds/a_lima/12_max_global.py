# -*- coding: utf-8 -*-
"""Test GLOBAL de duplicados: max por-pares de coincidencias posicionales y de
bigramas, sobre TODO el cohorte, comparado con la distribucion nula del maximo.
Nulo: barajar valores dentro de cada quipu (500 iter, semilla 0), recalculando el
maximo entre TODOS los pares -> controla la seleccion post-hoc."""
import pandas as pd, numpy as np, itertools
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]
V = {}
for k in solo:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V[k] = list(d["valor"].fillna(0).astype(int))
pairs = list(itertools.combinations(solo, 2))
print("Pares:", len(pairs))

def all_stats(VV):
    posm = {}; bgm = {}
    bg = {k: set(zip(VV[k][:-1], VV[k][1:])) for k in solo}
    for a, b in pairs:
        n = min(len(VV[a]), len(VV[b]))
        posm[(a, b)] = sum(1 for i in range(n) if VV[a][i] == VV[b][i] and VV[a][i] > 0)
        bgm[(a, b)] = len(bg[a] & bg[b])
    return posm, bgm

obs_pos, obs_bg = all_stats(V)
maxpos_obs = max(obs_pos.values()); maxbg_obs = max(obs_bg.values())
apa = max(obs_pos.items(), key=lambda x: x[1]); apb = max(obs_bg.items(), key=lambda x: x[1])
print("obs max posicion:", maxpos_obs, apa, "| obs max bigramas:", maxbg_obs, apb)

null_maxpos = np.zeros(NC); null_maxbg = np.zeros(NC)
perm = {k: list(V[k]) for k in solo}
for it in range(NC):
    for k in solo:
        rng.shuffle(perm[k])
    p, b = all_stats(perm)
    null_maxpos[it] = max(p.values()); null_maxbg[it] = max(b.values())
print(f"Nulo max posicion: media={null_maxpos.mean():.2f} sd={null_maxpos.std():.2f} p95={np.percentile(null_maxpos,95):.1f} "
      f"p={(np.sum(null_maxpos>=maxpos_obs)+1)/(NC+1):.4f}")
print(f"Nulo max bigramas: media={null_maxbg.mean():.1f} sd={null_maxbg.std():.1f} p95={np.percentile(null_maxbg,95):.1f} "
      f"p={(np.sum(null_maxbg>=maxbg_obs)+1)/(NC+1):.4f}")

# top pares por pos_eq
print("\nTop 10 pares por coincidencias posicionales:")
for (a, b), v in sorted(obs_pos.items(), key=lambda x: -x[1])[:10]:
    print(f"  {a:8s} x {b:8s} pos_eq={v:2d}  bigr={obs_bg[(a,b)]}")
