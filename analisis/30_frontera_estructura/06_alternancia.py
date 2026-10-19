"""Seguimiento (fuera de la frontera) de la alternancia de color de desfase 2 (T2) en todo el corpus KFG.
Pregunta: la alternancia A/B/A/B hallada en UR040, UR167 y UR1033F ¿existe en quipus ya clasificados? ¿se concentra
por museo o lote? Mismo estadistico T2 y mismo nulo (permutacion de colores), 9 999 replicas, BH sobre el corpus.
Uso: python 06_alternancia.py"""
import importlib.util
import numpy as np, pandas as pd
from comun import *

s = importlib.util.spec_from_file_location("i1", AQUI / "01_internas.py"); I1 = importlib.util.module_from_spec(s); s.loader.exec_module(I1)

filas = []
for k in sorted(set(C.kfg)):
    q = quipu(k); c = q.col
    pr = I1.t2(c)
    if pr is None: continue
    base, f = pr
    u, ci = np.unique(c, return_inverse=True); n = len(ci); K = n // 3; b0 = ((np.bincount(ci) / n) ** 2).sum()
    A = [(ci[:-kk] == ci[kk:]).mean() - b0 for kk in range(1, K + 2)]
    prom = [(A[kk - 1] - (A[kk - 2] + A[kk]) / 2) if A[kk - 1] > 0 else -1 for kk in range(2, K + 1)]
    lag = int(np.argmax(prom) + 2)
    obs = float(f(base[None, :])[0])
    p, N, b = p_escalada(obs, lambda m, rng: f(I1.perm_filas(base, m, rng)), [9999], 0)
    alt = np.mean([c[i] == c[i + 2] and c[i] != c[i + 1] for i in range(len(c) - 2)]) if len(c) > 2 else 0
    filas.append(dict(kfg=k, lag=lag, estadistico=obs, p=p, frac_alterna=round(alt, 3), colores=len(u), n=len(c),
                      genero=ATLAS.loc[k, "genero"], museo=MUSEO[k], sitio=ATLAS.loc[k, "procedencia"], frontera=k in FRONTERA))
D = pd.DataFrame(filas); D["q"] = bh(D.p)
D.to_csv(AQUI / "alternancia_corpus.csv", index=False)
sig = D[(D.q < 0.05) & (D.lag == 2)].sort_values("p")
pd.set_option("display.width", 220)
print("quipus evaluados:", len(D), "| lag 2 con q < 0.05:", len(sig))
print(sig[["kfg", "p", "q", "frac_alterna", "colores", "n", "genero", "museo", "sitio", "frontera"]].to_string())
print("\npor museo (lag2 q<0.05 / evaluados):")
t = D.groupby("museo").agg(n=("kfg", "size"), alt=("kfg", lambda s: int(((D.loc[s.index, "q"] < 0.05) & (D.loc[s.index, "lag"] == 2)).sum())))
print(t[t.alt > 0].sort_values("alt", ascending=False).to_string())
print("\nfraccion de quipus con alternancia lag 2 (q<0.05): frontera", round(sig.frontera.mean() if len(sig) else 0, 2))
