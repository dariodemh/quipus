# -*- coding: utf-8 -*-
"""Referencia NUMERICA: 20 quipus claramente decimales (6 de Incahuasi + 14
aleatorios de la clase no-anomala). Para cada alfabeto se calcula su exceso de
verosimilitud sobre el barajado (z). p_vs_numerico = fraccion de quipus
numericos con z >= z del candidato (misma alfabeto).
"""
import os, sys, re, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_descifrado.py"),
          encoding="utf-8").read().split("rows = []")[0])

# candidatos numericos
inc = ["UR278", "UR266", "UR272", "UR267A", "UR255", "UR270"]
cl = pd.read_csv(r"./analisis/ds/n_no_numericos/quipus_clase.csv")
pool = cl[(cl.clase_limpia == 0) & (cl.ncuerdas >= 20)].kfg.tolist()
rng = np.random.default_rng(SEED)
extra = list(rng.choice([x for x in pool if x not in inc], 14, replace=False))
NUMQ = [x for x in inc if x in set(df.kfg)] + extra
print("referencia numerica:", len(NUMQ), NUMQ)

rows = []
for k in NUMQ:
    for name, fn in SIGS.items():
        seq = [fn(r) for _, r in df[(df.kfg == k) & (df.nivel == 0)].sort_values("orden").iterrows()]
        if len(seq) < 10:
            continue
        C, st, inv = D.counts_seq(seq)
        f, v = D.anneal(C[None], st[None], L, restarts=2, iters=2000, seed=SEED)
        Cs, sts = [], []
        for i in range(20):
            cc, ss, _ = D.counts_seq(list(np.random.default_rng(SEED + i).permutation(seq)))
            Cs.append(cc); sts.append(ss)
        _, vn = D.anneal(np.array(Cs), np.array(sts), L, restarts=1, iters=2000, seed=SEED + 5)
        z = (v[0] - vn.mean()) / (vn.std() + 1e-9)
        rows.append(dict(quipu=k, alfabeto=name, n=len(seq), V=len(inv), z=z,
                         logL=v[0] / len(seq)))
    print(k, "ok")

t = pd.DataFrame(rows)
t.to_csv(os.path.join(BASE, "referencia_numerica.csv"), index=False)
print(t.groupby("alfabeto")["z"].describe()[["count", "mean", "50%", "max"]].round(2).to_string())

# fusionar p_vs_numerico en resultados.csv
r = pd.read_csv(os.path.join(BASE, "resultados.csv"))
pnum = []
for _, x in r.iterrows():
    zz = t[t.alfabeto == x.alfabeto].z.values
    pnum.append(float((zz >= x.z_obs).mean()) if len(zz) else np.nan)
r["p_vs_numerico"] = pnum
r["logL_por_signo"] = r["logL_obs"]
r.to_csv(os.path.join(BASE, "resultados.csv"), index=False)
print("p_vs_numerico añadido; mediana", np.nanmedian(pnum))
