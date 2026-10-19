# -*- coding: utf-8 -*-
"""Control por tamano del efecto 'mismo sitio'. Nulo: barajar valores dentro de
cada quipu para obtener exceso por par (obs - media nula), luego permutar etiquetas
de sitio. Corrige por comparaciones multiples (BH)."""
import pandas as pd, numpy as np, itertools
from scipy.stats import false_discovery_control as fdr
BASE = r"."
rng = np.random.default_rng(0); NC = 500
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
site = dict(zip(sel["kfg"], sel["sitio"]))
solo = [k for k in sel["kfg"] if k != "UR1124_Detail_1"]
VALS = {}
for k in solo:
    d0 = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    VALS[k] = list(d0["valor"].fillna(0).astype(int))
def bg(v): return set(zip(v[:-1], v[1:]))
bg0 = {k: bg(VALS[k]) for k in solo}
pairs = list(itertools.combinations(solo, 2))
obs = {(a, b): len(bg0[a] & bg0[b]) for a, b in pairs}
perm = {k: list(VALS[k]) for k in solo}
nullsum = {kk: 0.0 for kk in obs}
for it in range(NC):
    for k in solo:
        rng.shuffle(perm[k])
    pb = {k: bg(perm[k]) for k in solo}
    for a, b in pairs:
        nullsum[(a, b)] += len(pb[a] & pb[b])
nmean = {kk: nullsum[kk] / NC for kk in obs}
excess = {kk: obs[kk] - nmean[kk] for kk in obs}   # exceso por par, controla tamano
print("Exceso global medio:", round(np.mean(list(excess.values())), 3))

# por sitio: exceso medio dentro vs permutacion de etiquetas
arr_site = np.array([site[k] for k in solo])
obs_res = {}
for s in sorted(set(site.values())):
    ks = set(k for k in solo if site[k] == s)
    val = [excess[(a, b)] for a, b in pairs if a in ks and b in ks]
    obs_res[s] = (len(ks), np.mean(val) if val else np.nan, len(val))
nulls = {s: np.zeros(NC) for s in obs_res}
for it in range(NC):
    perm_lab = dict(zip(solo, rng.permutation(arr_site)))
    for s in obs_res:
        ks = set(k for k in solo if perm_lab[k] == s)
        val = [excess[(a, b)] for a, b in pairs if a in ks and b in ks]
        nulls[s][it] = np.mean(val) if val else 0
print("\nExceso medio por sitio (controlado por tamano), nulo por permutacion de etiquetas:")
ps = []
for s, (n, me, np_) in obs_res.items():
    p = (np.sum(nulls[s] >= me) + 1) / (NC + 1)
    ps.append(p)
    print(f"  {s:12s} n={n:2d} exceso={me:+.3f} nulo={nulls[s].mean():+.3f} sd={nulls[s].std():.3f} p={p:.3f}")
q = fdr(np.array(ps), method="bh")
print("q BH:", dict(zip(obs_res.keys(), np.round(q, 3))))

# Top pares por exceso
E = pd.DataFrame([(a, b, site[a], site[b], obs[(a, b)], round(nmean[(a, b)], 2),
                   round(excess[(a, b)], 2)) for a, b in pairs],
                 columns=["A", "B", "sitioA", "sitioB", "obs", "nulo", "exceso"])
E.to_csv(BASE + r"\analisis\ds\a_lima\test1_exceso_por_par.csv", index=False)
print("\nTop 12 pares por exceso (positivo):")
print(E.sort_values("exceso", ascending=False).head(12).to_string(index=False))
print("\nTop 6 pares por exceso negativo:")
print(E.sort_values("exceso").head(6).to_string(index=False))
