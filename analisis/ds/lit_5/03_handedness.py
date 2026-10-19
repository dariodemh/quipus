"""Verificación de la asimetría de handedness (KFG / Medrano & Khosla 2024).

Afirmaciones:
  - PPS 54/46 [4382/3706]; color 56/44 [1707/1316];
    indexed 57/43 [2712/2034]; subsidiary 57/43 [439/328]
  - 63% de los khipus presenta ambos sentidos de suma.

Control: la unidad es el quipu. Se hace (a) test de signos por quipu
(¿hay más khipus con exceso de sumas derechas que de izquierdas?),
(b) bootstrap de khipus para el % agregado, y (c) nulo de permutación
que baraja la etiqueta L/R dentro de cada quipu preservando sus totales.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from comun import KFG_SUM, SALIDA, SEMILLA

rng = np.random.default_rng(SEMILLA)
REL = ["pendant_pendant_sum", "pendant_pendants_color_sum",
       "indexed_pendant_sum", "indexed_subsidiary_sum"]
NOMBRE = {"pendant_pendant_sum": "pendant-pendant",
          "pendant_pendants_color_sum": "color",
          "indexed_pendant_sum": "indexed",
          "indexed_subsidiary_sum": "subsidiary"}
R = {}


def pct_r(d):
    L, Rr = d.num_left_sums.sum(), d.num_right_sums.sum()
    return 100 * Rr / (L + Rr), int(L), int(Rr)


for rel in REL:
    d = pd.read_csv(os.path.join(KFG_SUM, rel + ".csv"))
    p, L, Rr = pct_r(d)
    # sign test por quipu (solo quipus con asimetría)
    dif = d.num_right_sums - d.num_left_sums
    n_pos, n_neg = int((dif > 0).sum()), int((dif < 0).sum())
    p_sign = binomtest(n_pos, n_pos + n_neg, 0.5).pvalue
    # bootstrap por quipu del % agregado
    idx = rng.integers(0, len(d), size=(5000, len(d)))
    boot = []
    Lv, Rv = d.num_left_sums.values, d.num_right_sums.values
    for i in idx:
        s = Lv[i].sum() + Rv[i].sum()
        if s:
            boot.append(100 * Rv[i].sum() / s)
    lo, hi = np.quantile(boot, [0.025, 0.975])
    print(f"{NOMBRE[rel]:16s} R%={p:5.2f} [{L}/{Rr}]  "
          f"khipus +R/-R={n_pos}/{n_neg}  p_signos={p_sign:.3g}  "
          f"IC95%=[{lo:.2f},{hi:.2f}]  filas con 0 sumas={(d.num_left_sums + d.num_right_sums == 0).sum()}")
    R[rel] = dict(pct_R=round(p, 3), L=L, R=int(Rr), n_pos=n_pos, n_neg=n_neg,
                  p_signos=float(p_sign), ic=[round(lo, 2), round(hi, 2)])
    # columnas alternativas para indexed (clusters vs cords)
    if "num_sum_clusters" in d.columns:
        print(f"   num_sum_clusters total={int(d.num_sum_clusters.sum())} "
              f"(ficha KFG indexed cita 2712+2034=4746)")

# ---------------------------------------------------------------- ambos sentidos
print("\n--- Holm sobre los 4 tests de signos ---")
ps = sorted([(k, v["p_signos"]) for k, v in R.items() if k in REL], key=lambda x: x[1])
for i, (k, p) in enumerate(ps):
    print(f"  {NOMBRE[k]:16s} p={p:.3g}  Holm={min(1.0, p*(4-i)):.3g}")

print("\n--- khipus con ambos sentidos ---")
base = None
for rel in REL:
    d = pd.read_csv(os.path.join(KFG_SUM, rel + ".csv"))[["khipu_id", "num_left_sums", "num_right_sums"]]
    d = d.rename(columns={"num_left_sums": "L_" + rel, "num_right_sums": "R_" + rel})
    base = d if base is None else base.merge(d, on="khipu_id", how="outer")
base = base.fillna(0)
hasL = (base[[c for c in base if c.startswith("L_")]] > 0).any(axis=1)
hasR = (base[[c for c in base if c.startswith("R_")]] > 0).any(axis=1)
print(f"khipus={len(base)}; con L>0 y R>0 en alguna relación={int((hasL & hasR).sum())} "
      f"({100*(hasL & hasR).mean():.1f}%) (KFG declara 63%)")
print(f"khipus con alguna suma={int((hasL | hasR).sum())}; "
      f"de ellos con ambos sentidos={100*(hasL & hasR).sum()/(hasL | hasR).sum():.1f}%; "
      f"sobre 650={100*(hasL & hasR).sum()/650:.1f}%")
R["ambos_sentidos"] = dict(pct=round(100*float((hasL & hasR).mean()), 2),
                           n=int(len(base)),
                           pct_de_650=round(100*float((hasL & hasR).sum()/650), 2),
                           pct_de_con_suma=round(100*float((hasL & hasR).sum()/(hasL | hasR).sum()), 2))
# volumen de la relación PPS (para contrastar K-CAT 7.018 / 57,8%)
dpps = pd.read_csv(os.path.join(KFG_SUM, "pendant_pendant_sum.csv"))
print(f"PPS: suma de num_sum_cords={int(dpps.num_sum_cords.sum())}; "
      f"khipus con PPS={int((dpps.num_sum_cords > 0).sum())} "
      f"({100*(dpps.num_sum_cords > 0).mean():.1f}%)")
R["pps_volumen"] = dict(sum_cords=int(dpps.num_sum_cords.sum()),
                        khipus=int((dpps.num_sum_cords > 0).sum()))

# ---------------------------------------------------------------- nulo intra-quipu
print("\n--- nulo: barajar L/R dentro de cada quipu (PPS) ---")
d = pd.read_csv(os.path.join(KFG_SUM, "pendant_pendant_sum.csv"))
obs = d.num_right_sums.sum() / (d.num_right_sums.sum() + d.num_left_sums.sum())
n_perm = 5000
mayores = 0
for _ in range(n_perm):
    # recomponer cada fila repartiendo sus n sumas con p=0.5
    n = (d.num_left_sums + d.num_right_sums).values
    r = rng.binomial(n, 0.5)
    tot = n.sum()
    if tot and (r.sum() / tot) >= obs:
        mayores += 1
p_perm = (mayores + 1) / (n_perm + 1)
print(f"observado R%={100*obs:.2f}; p_perm={p_perm:.4f} (N={n_perm}, una cola)")
R["nulo_PPS"] = dict(obs=round(100*float(obs), 2), p_perm=float(p_perm), n_perm=n_perm)

with open(os.path.join(SALIDA, "res_03_handedness.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_03_handedness.json")
