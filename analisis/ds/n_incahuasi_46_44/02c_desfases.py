"""02c. Robustez del barrido a desfases entre los registros de A y B.

En 02 se alinea A_i con B_i. El equipo 13 empareja por número de grupo, que puede
introducir un desfase si un quipu tiene grupos sin contraparte. Aquí se repite la
pantalla con desfases d = -3..+3 (S_i = A_i + B_{i+d}) y se calcula el máximo de
coincidencias exactas observado y su nulo global (30 réplicas por desfase).
"""
import itertools
from collections import Counter
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4607
NREP = 30
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()
O = pd.read_csv(C.AQUI / "ur269_objetivos.csv")
T = {"A_posicion": O[O.definicion == "A_posicion"].sort_values("orden").cab.to_numpy(int),
     "B_cuota": O[O.definicion == "B_cuota"].sort_values("orden").cab.to_numpy(int)}
R = {k: X for k, s in c.groupby("kfg", sort=True) if len(X := C.registros_lax(s)) >= 3}
pares = list(itertools.combinations(sorted(R), 2))
print("parejas:", len(pares))


def suma_desfase(A, B, d):
    if d >= 0:
        m = min(len(A), len(B) - d)
        return A[:m] + B[d:d + m]
    m = min(len(A) + d, len(B))
    return A[-d:-d + m] + B[:m]


def m(S, cT):
    cs = Counter(S.tolist())
    return sum(min(cs[v], n) for v, n in cT.items())


filas = []
for nombre, Tv in T.items():
    cT = Counter(Tv.tolist())
    for d in range(-3, 4):
        obs = max(m(suma_desfase(R[a], R[b], d), cT) for a, b in pares)
        nul = []
        for rep in range(NREP):
            P = {k: rng.permutation(v) for k, v in R.items()}
            nul.append(max(m(suma_desfase(R[a], P[b], d), cT) for a, b in pares))
        nul = np.array(nul)
        filas.append(dict(objetivos=nombre, desfase=d, obs_max=obs, nulo_medio=nul.mean(),
                          nulo_max=nul.max(),
                          p=(np.sum(nul >= obs) + 1) / (NREP + 1)))
        print(f"{nombre} d={d:+d}: obs_max={obs}, nulo={nul.mean():.2f} (máx {nul.max()}), "
              f"p={(np.sum(nul >= obs) + 1) / (NREP + 1):.2f}")
pd.DataFrame(filas).to_csv(C.AQUI / "parejas_desfases.csv", index=False, float_format="%.4g")
