# -*- coding: utf-8 -*-
"""Busqueda intensiva (20 reinicios x 15000 iteraciones) en los mejores
candidatos, para descartar que el resultado negativo se deba solo al
presupuesto de busqueda."""
import os, sys, re, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_descifrado.py"),
          encoding="utf-8").read().split("rows = []")[0])

CASOS = [("UR203", "A5_nudo"), ("UR203", "A6_color_nudo"), ("UR203", "A6_micro"),
         ("UR215", "A6_color_nudo"), ("UR215", "A5_nudo"), ("UR052", "A5_nudo")]
rows = []
for k, a in CASOS:
    seq = micro(k) if a == "A6_micro" else [SIGS[a](r) for _, r in
            df[(df.kfg == k) & (df.nivel == 0)].sort_values("orden").iterrows()]
    C, st, inv = D.counts_seq(seq); V = len(inv)
    f, v = D.anneal(C[None], st[None], L, restarts=20, iters=15000, seed=SEED)
    # nulo con el mismo presupuesto (10 barajados)
    Cs, sts = [], []
    for i in range(10):
        cc, ss, _ = D.counts_seq(list(np.random.default_rng(SEED + i).permutation(seq)))
        Cs.append(cc); sts.append(ss)
    _, vn = D.anneal(np.array(Cs), np.array(sts), L, restarts=4, iters=15000, seed=SEED + 3)
    rows.append(dict(quipu=k, alfabeto=a, n=len(seq), V=V, logL_int=v[0] / len(seq),
                     logL_nulo=vn.mean() / len(seq), p=float((vn >= v[0]).mean())))
    print(k, a, "V=%d logL/s=%.2f nulo=%.2f p=%.3f" %
          (V, v[0] / len(seq), vn.mean() / len(seq), rows[-1]["p"]))
pd.DataFrame(rows).to_csv(os.path.join(BASE, "busqueda_intensa.csv"), index=False)
