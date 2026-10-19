# -*- coding: utf-8 -*-
"""Estabilidad del desciframiento: split-half. Si la asignacion recuperada no
coincide entre dos mitades independientes del mismo quipu, no hay lectura.
"""
import os, sys, re, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_descifrado.py"),
          encoding="utf-8").read().split("rows = []")[0])

CASOS = [("UR203", "A5_nudo"), ("UR203", "A6_color_nudo"), ("UR215", "A6_color_nudo"),
         ("UR050", "A6_micro"), ("AS076", "A5_nudo"), ("UR179", "A5_nudo"),
         ("UR052", "A5_nudo"), ("UR278", "A5_nudo")]

def descifra(seq):
    C, st, inv = D.counts_seq(seq)
    f, v = D.anneal(C[None], st[None], L, restarts=6, iters=3000, seed=SEED)
    return {inv[i]: TOP[f[0][i]] for i in range(len(inv))}, v[0] / len(seq)

rows = []
for k, a in CASOS:
    seq = micro(k) if a == "A6_micro" else [SIGS[a](r) for _, r in
            df[(df.kfg == k) & (df.nivel == 0)].sort_values("orden").iterrows()]
    mitad = len(seq) // 2
    m1, l1 = descifra(seq[:mitad])
    m2, l2 = descifra(seq[mitad:])
    comunes = set(m1) & set(m2)
    ac = np.mean([m1[s] == m2[s] for s in comunes]) if comunes else np.nan
    azar = 1.0 / max(1, len(comunes))   # azar relevante: cuantas silabas usa el optimo
    rows.append(dict(quipu=k, alfabeto=a, n=len(seq), n_comunes=len(comunes),
                     acuerdo=ac, azar=azar, logL1=l1, logL2=l2))
    print(k, a, "n=%d comunes=%d acuerdo=%.2f (azar 1/V=%.3f)" %
          (len(seq), len(comunes), ac, azar))
pd.DataFrame(rows).to_csv(os.path.join(BASE, "estabilidad.csv"), index=False)
