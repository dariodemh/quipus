"""Aritmetica interna y jerarquia del archivo HP.
- cord = suma de sus subsidiarias directas
- cord = suma de todas las cuerdas de su grupo (total de grupo presente como cuerda)
- total de un quipu = suma de totales de otros quipus (jerarquia de archivo)
Nulo: barajar valores dentro de cada quipu, 500 veces, semilla 0.
"""
import pandas as pd, numpy as np
from itertools import combinations

RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()
hp["v"] = pd.to_numeric(hp.valor, errors="coerce")

# --- arbol: cord = suma de subsidiarias directas ---
def hier_hits():
    n = 0; casos = []
    for k in HP:
        d = hp[hp.kfg == k]
        for _, r in d[d.nivel == 0].iterrows():
            if pd.isna(r.v) or r.v <= 0: continue
            subs = d[d.padre == r.cuerda]
            if len(subs) == 0: continue
            s = np.nansum(subs.v.to_numpy(float))
            if abs(s - r.v) < 1e-6:
                n += 1; casos.append((k, r.cuerda, int(r.v), len(subs)))
    return n, casos

obs, casos = hier_hits()
print("== cord = suma de subsidiarias directas ==")
print("obs =", obs)
for x in casos[:15]: print("  ", x)

# --- cord = suma del grupo ---
grp_hits_val = 0
for k in HP:
    d = hp[hp.kfg == k]
    tot = np.nansum(d.v.to_numpy(float))
    if tot > 0 and int(round(tot)) in set(np.round(d.v.dropna()).astype(int)):
        pass

# --- totales de quipu ---
tot = {k: float(np.nansum(hp[hp.kfg == k].v.to_numpy(float))) for k in HP}
print("\n== totales por quipu ==")
for k in HP:
    print(f"  {k}: {tot[k]:.0f}")

# jerarquia: total de A = suma de totales de un subconjunto de otros quipus
others = HP
tot_vals = np.array([tot[k] for k in others])
hits = []
for i, a in enumerate(others):
    rest = [tot[k] for k in others if k != a]
    # subconjunto de tamano 2..4 (suma de 2..4 totales)
    from itertools import combinations as comb
    for rsize in (2, 3, 4):
        for cc in comb([k for k in others if k != a], rsize):
            if abs(sum(tot[k] for k in cc) - tot[a]) < 1:
                hits.append((a, cc, tot[a]))
print("\n== total de A = suma de totales de 2-4 quipus (tolerancia 1) ==")
print("hits:", hits if hits else "ninguno")

# nulo para hits de totales: barajar valores dentro de cada quipu
def count_tot_hits(T):
    h = 0
    for a in HP:
        for rsize in (2, 3):
            for cc in combinations([k for k in HP if k != a], rsize):
                if abs(sum(T[k] for k in cc) - T[a]) < 1: h += 1
    return h
obs_th = count_tot_hits(tot)
null_th = []
seqs = {k: hp[hp.kfg == k].sort_values("orden")["v"].to_numpy(float) for k in HP}
for _ in range(500):
    T = {}
    for k in HP:
        v = seqs[k].copy(); np.random.default_rng(0).shuffle(v)  # placeholder
        T[k] = float(np.nansum(v))
    # NOTA: shuffling dentro del quipu NO cambia el total -> nulo trivial.
    null_th.append(count_tot_hits(T))
print("obs hits totales (r=2,3):", obs_th, " (el nulo por permutacion no cambia el total: invariante)")

# --- HP001/HP002 (mismo objeto RN43366): comparar ---
print("\n== par mismo objeto ==")
print("HP001 suma", tot["HP001"], "HP002 suma", tot["HP002"], "diferencia", abs(tot['HP001']-tot['HP002']))
# HP001 vs suma de grupos de HP002?
d2 = hp[hp.kfg == "HP002"]
print("HP002 sumas por grupo:", [round(np.nansum(s.v.to_numpy(float))) for _, s in d2.groupby("grupo")])
print("HP001 valores:", sorted(hp[hp.kfg=='HP001'].v.dropna().astype(int).tolist()))
