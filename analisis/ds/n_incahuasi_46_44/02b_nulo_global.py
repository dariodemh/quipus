"""02b. Nulo global del barrido exhaustivo de parejas.

El barrido de 02 prueba 10153 parejas; con B=2000 el p mínimo es 0,0005 y BH nunca
puede dar q<0,05 (q mínimo = 5,07). Para que la búsqueda tenga una prueba global
válida se usa el estadístico máximo: ¿cuántas parejas alcanzan obs>=2, y cuál es el
máximo de coincidencias exactas, cuando se baraja el orden de B en TODAS las parejas?
Ese máximo ya incorpora la multiplicidad (es una sola prueba).
100 réplicas globales (cada réplica baraja el orden de los registros de cada quipu),
para los dos conjuntos de objetivos (A posición, B cuota).
"""
import itertools
from collections import Counter
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4605
NREP = 100
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()
O = pd.read_csv(C.AQUI / "ur269_objetivos.csv")
T = {"A_posicion": O[O.definicion == "A_posicion"].sort_values("orden").cab.to_numpy(int),
     "B_cuota": O[O.definicion == "B_cuota"].sort_values("orden").cab.to_numpy(int)}
R = {k: X for k, s in c.groupby("kfg", sort=True)
     if len(X := C.registros_lax(s)) >= 3}
claves = sorted(R)
pares = list(itertools.combinations(claves, 2))
print("quipus:", len(claves), "parejas:", len(pares))


def m(S, cT):
    cs = Counter(S.tolist())
    return sum(min(cs[v], n) for v, n in cT.items())


for nombre, Tv in T.items():
    cT = Counter(Tv.tolist())
    obs = np.array([m(R[a][:min(len(R[a]), len(R[b]))] + R[b][:min(len(R[a]), len(R[b]))], cT)
                    for a, b in pares])
    print(f"\n{nombre}: observado máximo={obs.max()}, parejas con >=2: {(obs >= 2).sum()}, "
          f"con >=3: {(obs >= 3).sum()}")
    mx, n2 = [], []
    for rep in range(NREP):
        P = {k: rng.permutation(v) for k, v in R.items()}
        v = np.array([m(R[a][:min(len(R[a]), len(P[b]))] + P[b][:min(len(R[a]), len(P[b]))], cT)
                      for a, b in pares])
        mx.append(v.max()); n2.append((v >= 2).sum())
    mx, n2 = np.array(mx), np.array(n2)
    print(f"  nulo global ({NREP} réplicas): máximo medio={mx.mean():.2f} (máx {mx.max()}); "
          f"parejas con >=2 medio={n2.mean():.2f} (máx {n2.max()})")
    print(f"  p(máximo >= {obs.max()}) = {(np.sum(mx >= obs.max()) + 1) / (NREP + 1):.3f}; "
          f"p(nº con >=2 >= {(obs >= 2).sum()}) = {(np.sum(n2 >= (obs >= 2).sum()) + 1) / (NREP + 1):.3f}")
    print(f"  potencia: el nulo nunca superó {mx.max()} coincidencias exactas; "
          f"una pareja con >= {mx.max()+1} daría p <= {(np.sum(mx >= mx.max()+1) + 1) / (NREP + 1):.3f}")
