# -*- coding: utf-8 -*-
"""Cuantifica el par duplicado UR066/UR067 y el cluster {UR062,UR064,UR066,UR067}.
Estadisticos: bigramas compartidos, coincidencias posicionales, valor raro compartido.
Nulo: barajar valores dentro de cada quipu, 5000 iteraciones, semilla 0."""
import pandas as pd, numpy as np, itertools
BASE = r"."
rng = np.random.default_rng(0); NC = 5000
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
V = {}
for k in sel["kfg"]:
    d = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    V[k] = list(d["valor"].fillna(0).astype(int))

def stats(a, b):
    va, vb = V[a], V[b]
    n = min(len(va), len(vb))
    pos_eq = sum(1 for i in range(n) if va[i] == vb[i] and va[i] > 0)
    ba = set(zip(va[:-1], va[1:])); bb = set(zip(vb[:-1], vb[1:]))
    return pos_eq, len(ba & bb)

for (a, b) in [("UR066", "UR067"), ("UR062", "UR064"), ("UR062", "UR066"), ("UR062", "UR067"),
               ("UR064", "UR066"), ("UR064", "UR067")]:
    o_pe, o_bg = stats(a, b)
    na, nb = V[a][:], V[b][:]
    null_pe = np.zeros(NC); null_bg = np.zeros(NC)
    for it in range(NC):
        rng.shuffle(na); rng.shuffle(nb)
        n = min(len(na), len(nb))
        null_pe[it] = sum(1 for i in range(n) if na[i] == nb[i] and na[i] > 0)
        ba = set(zip(na[:-1], na[1:])); bb = set(zip(nb[:-1], nb[1:]))
        null_bg[it] = len(ba & bb)
    p_pe = (np.sum(null_pe >= o_pe) + 1) / (NC + 1)
    p_bg = (np.sum(null_bg >= o_bg) + 1) / (NC + 1)
    print(f"{a:6s} x {b:6s}: pos_eq={o_pe} (nulo {null_pe.mean():.2f}, p={p_pe:.4f}) | "
          f"bigramas={o_bg} (nulo {null_bg.mean():.1f}, p={p_bg:.4f})")

# fuerza del match: % de cuerdas alineadas (nivel0) y longitud del sufijo comun
print("\nAlineacion nivel0 UR066 vs UR067:")
for i, (x, y) in enumerate(zip(V["UR066"], V["UR067"])):
    print(f"  {i:2d}: UR066={x:5d}  UR067={y:5d}  {'=' if x==y else ''}")
# subsecuencia contigua comun mas larga (igualdad estricta)
def lcs_contig(a, b):
    n = min(len(a), len(b)); best = 0; bl = 0
    for i in range(n):
        if a[i] == b[i]:
            bl += 1; best = max(best, bl)
        else:
            bl = 0
    return best
print("\nSubsecuencia contigua comun mas larga UR066-UR067:", lcs_contig(V["UR066"], V["UR067"]))
print("valor 2904 aparece en quipus:", [k for k in sel["kfg"] if 2904 in V[k]])
print("valor 1236 aparece en:", [k for k in sel["kfg"] if 1236 in V[k]])
print("valor 1212 aparece en:", [k for k in sel["kfg"] if 1212 in V[k]])
