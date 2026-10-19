# -*- coding: utf-8 -*-
"""Relaciones ENTRE quipus de la cohorte de Lima + controles nulos.
Estadisticos: (1) bigramas de valor compartidos; (2) total de A en B;
(3) estructura de grupos; (4) bigramas de color. Nulo: barajar dentro de cada quipu,
500 iteraciones, semilla 0. Se anaden nulos alternativos donde el nulo prescrito es degenerado.
"""
import pandas as pd, numpy as np, re, itertools
from collections import Counter
BASE = r"."
rng = np.random.default_rng(0)
NC = 500

sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
cc["nudos"] = cc["nudos"].fillna("")

# Secuencia de valores por quipu: solo nivel 0, valor != 0, en orden de cuerda
seqs, colseqs, totals, vals_by_q = {}, {}, {}, {}
for kfg, d in cc.groupby("kfg"):
    d = d.sort_values("orden")
    d0 = d[d["nivel"] == 0]
    v = d0["valor"].fillna(0).astype(int).values
    seqs[kfg] = list(v)
    cbase = d0["color"].astype(str).str.extract(r"^([A-Za-z0-9]+)")[0].fillna("?").values
    colseqs[kfg] = list(cbase)
    vals_by_q[kfg] = set(x for x in v if x > 0)
    totals[kfg] = int(v[v > 0].sum())

# Grupos (tamanos en orden)
g = pd.read_csv(BASE + r"\analisis\datos\grupos.csv")
grp = {}
for kfg, d in g[g["kfg"].isin(sel["kfg"])].groupby("kfg"):
    d = d.sort_values("grupo")
    grp[kfg] = [int(r["hasta"]) - int(r["desde"]) + 1 for _, r in d.iterrows()]

# Detalle del mismo objeto: excluir de pares
solo_kfg = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]
site = dict(zip(sel["kfg"], sel["sitio"]))

def bigrams(seq):
    return set(zip(seq[:-1], seq[1:]))

def shared_bigram_pairs(seqmap):
    bg = {k: bigrams(v) for k, v in seqmap.items()}
    tot = 0
    for a, b in itertools.combinations(solo_kfg, 2):
        tot += len(bg[a] & bg[b])
    return tot, bg

# ---- Test 1: bigramas de valor ----
bg = {k: bigrams(seqs[k]) for k in solo_kfg}
obs_pairs_mean = np.mean([len(bg[a] & bg[b]) for a, b in itertools.combinations(solo_kfg, 2)])
obs_total = sum(len(bg[a] & bg[b]) for a, b in itertools.combinations(solo_kfg, 2))
# per-pair observed
obs_pp = {}
for a, b in itertools.combinations(solo_kfg, 2):
    obs_pp[(a, b)] = len(bg[a] & bg[b])
null_total = np.zeros(NC)
null_pp = {kk: 0 for kk in obs_pp}
perm_seqs = {k: list(v) for k, v in seqs.items()}
for it in range(NC):
    for k in solo_kfg:
        rng.shuffle(perm_seqs[k])
    pbg = {k: bigrams(perm_seqs[k]) for k in solo_kfg}
    for a, b in itertools.combinations(solo_kfg, 2):
        s = len(pbg[a] & pbg[b])
        null_total[it] += s
        if s >= obs_pp[(a, b)]:
            null_pp[(a, b)] += 1
pval_bg = {k: (v + 1) / (NC + 1) for k, v in null_pp.items()}
pv = np.array(list(pval_bg.values()))
from scipy.stats import false_discovery_control as fdr
q_bg = fdr(pv, method="bh")
print("=== Test 1: bigramas de valor compartidos (nulo: barajar dentro de cada quipu) ===")
print(f"Observado total={obs_total}  nulo medio={null_total.mean():.1f} sd={null_total.std():.1f}  "
      f"z={(obs_total-null_total.mean())/null_total.std():.2f}")
print(f"p-valor global (proporcion de nulos >= obs): {(np.sum(null_total>=obs_total)+1)/(NC+1):.4f}")
print(f"Pares obs>=1: {sum(1 for v in obs_pp.values() if v>0)}; pares con q<0.05 (BH): {(q_bg<0.05).sum()}")
# top pares
items = sorted(obs_pp.items(), key=lambda x: -x[1])[:12]
for (a, b), v in items:
    print(f"  {a:16s} x {b:16s} obs={v} q={[q for (kk,q) in zip(obs_pp,pv)][list(obs_pp).index((a,b))]:.3f}" if (a,b) in obs_pp else f"  {a} x {b} obs={v}")
np.save(BASE + r"\analisis\ds\a_lima\null_total_bg.npy", null_total)
pd.DataFrame({"pair": [f"{a}|{b}" for a, b in obs_pp], "obs_bg": list(obs_pp.values()),
              "p_emp": list(pval_bg.values()), "q_bh": q_bg}).to_csv(
    BASE + r"\analisis\ds\a_lima\test1_bigramas.csv", index=False)

# ---- Test 2: total de A aparece como valor en B (estadistico de conjunto -> nulo de pool) ----
print("\n=== Test 2: total de un quipu como valor en otro ===")
coinc = []
for a in solo_kfg:
    for b in solo_kfg:
        if a != b and totals[a] in vals_by_q[b]:
            coinc.append((a, b, totals[a]))
print(f"Coincidencias observadas total(A) in valores(B): {len(coinc)} (pares ordenados unicos: {len(set((a,b) for a,b,_,_ in [(x[0],x[1],x[2],0) for x in coinc]))})")
# nulo de pool: reasignar valores globalmente conservando n cuerdas por quipu
allvals = cc[cc["nivel"] == 0]["valor"].fillna(0).astype(int).values.copy()
sizes = {k: len(seqs[k]) for k in solo_kfg}
null2 = np.zeros(NC)
for it in range(NC):
    rng.shuffle(allvals)
    idx = 0
    sets = {}
    tot = {}
    for k in solo_kfg:
        seg = allvals[idx:idx + sizes[k]]; idx += sizes[k]
        sets[k] = set(x for x in seg if x > 0); tot[k] = int(seg[seg > 0].sum())
    cnt = 0
    for a in solo_kfg:
        for b in solo_kfg:
            if a != b and tot[a] in sets[b]:
                cnt += 1
    null2[it] = cnt
print(f"Nulo pool medio={null2.mean():.1f} sd={null2.std():.1f}  p={ (np.sum(null2>=len(coinc))+1)/(NC+1):.4f}")
for a, b, t in coinc[:20]:
    print(f"  total({a})={t} dentro de {b}")
pd.DataFrame(coinc, columns=["A","B","total"]).to_csv(BASE + r"\analisis\ds\a_lima\test2_totales.csv", index=False)

# ---- Test 3: estructura de grupos ----
print("\n=== Test 3: estructura de grupos ===")
obs_same_multiset = 0
for a, b in itertools.combinations(solo_kfg, 2):
    if a in grp and b in grp and grp[a] and Counter(grp[a]) == Counter(grp[b]):
        obs_same_multiset += 1
print(f"Pares con multiconjunto de tamanos de grupo identico: {obs_same_multiset}")
# nulo pooled: reasignar tamanos de grupo entre quipus
allg = [s for k in solo_kfg if k in grp for s in grp[k]]
glens = {k: len(grp.get(k, [])) for k in solo_kfg}
null3 = np.zeros(NC)
for it in range(NC):
    rng.shuffle(allg); idx = 0; cnt = 0; gh = {}
    for k in solo_kfg:
        gh[k] = allg[idx:idx + glens[k]]; idx += glens[k]
    for a, b in itertools.combinations(solo_kfg, 2):
        if gh[a] and Counter(gh[a]) == Counter(gh[b]):
            cnt += 1
    null3[it] = cnt
print(f"Nulo pooled medio={null3.mean():.1f} sd={null3.std():.1f}  p={(np.sum(null3>=obs_same_multiset)+1)/(NC+1):.4f}")
print("Ejemplos:", [(a,b,grp[a],grp[b]) for a,b in itertools.combinations(solo_kfg,2)
                    if a in grp and b in grp and grp[a] and Counter(grp[a])==Counter(grp[b])][:8])

# ---- Test 4: bigramas de color (nulo: barajar colores dentro de cada quipu) ----
print("\n=== Test 4: bigramas de color ===")
cbg = {k: bigrams(colseqs[k]) for k in solo_kfg}
obs_c = sum(len(cbg[a] & cbg[b]) for a, b in itertools.combinations(solo_kfg, 2))
perm_c = {k: list(v) for k, v in colseqs.items()}
nullc = np.zeros(NC)
for it in range(NC):
    for k in solo_kfg:
        rng.shuffle(perm_c[k])
    pcbg = {k: bigrams(perm_c[k]) for k in solo_kfg}
    for a, b in itertools.combinations(solo_kfg, 2):
        nullc[it] += len(pcbg[a] & pcbg[b])
print(f"Observado={obs_c} nulo medio={nullc.mean():.1f} sd={nullc.std():.1f} z={(obs_c-nullc.mean())/nullc.std():.2f} "
      f"p={(np.sum(nullc>=obs_c)+1)/(NC+1):.4f}")

# ---- Test 5: coherencia por sitio (dentro vs entre sitios) ----
print("\n=== Test 5: los quipus del mismo sitio se parecen mas? ===")
def within_mean(obs_pp, groupmap):
    same, diff = [], []
    for (a, b), v in obs_pp.items():
        if groupmap[a] == groupmap[b]:
            same.append(v)
        else:
            diff.append(v)
    return np.mean(same), np.mean(diff), len(same)
same_o, diff_o, ns = within_mean(obs_pp, site)
print(f"media dentro del sitio={same_o:.3f} (n={ns}) vs entre sitios={diff_o:.3f}")
obs_delta = same_o - diff_o
null_delta = np.zeros(NC)
sites_arr = np.array([site[k] for k in solo_kfg])
for it in range(NC):
    perm = rng.permutation(sites_arr)
    gm = dict(zip(solo_kfg, perm))
    s, d, _ = within_mean(obs_pp, gm)
    null_delta[it] = s - d
print(f"delta obs={obs_delta:.3f}  nulo medio={null_delta.mean():.4f} sd={null_delta.std():.3f}  "
      f"p={(np.sum(null_delta>=obs_delta)+1)/(NC+1):.4f}")
