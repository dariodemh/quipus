"""Afirmaciones 1 y 2: cabecera(i, A) + cabecera(i, B) = cabecera de algun registro de un quipu destino.
Nulo: barajar el orden de los registros de B (lista completa, incluidos ausentes), 10 000 replicas, semilla 16."""
import numpy as np
from lib import load, cabeceras, SEED

c = load()
N_REP = 10000
rng = np.random.default_rng(SEED)


def run(qa, qb, destinos, sep):
    A = cabeceras(c, qa, sep)
    B = cabeceras(c, qb, sep)
    pool = set()
    for d in destinos:
        pool |= {int(x) for x in cabeceras(c, d, sep) if x == x}
    pairs = [(i, a, b) for i, (a, b) in enumerate(zip(A, B)) if a == a and b == b]
    obs_ex = sum(int(a + b) in pool for _, a, b in pairs)
    obs_pm1 = sum(any((int(a + b) + d) in pool for d in (-1, 0, 1)) for _, a, b in pairs)
    # nulo: barajar orden de B
    Bl = np.array([np.nan if x != x else x for x in B], dtype=float)
    null_ex = np.empty(N_REP)
    null_pm1 = np.empty(N_REP)
    for r in range(N_REP):
        perm = rng.permutation(len(Bl))
        Bp = Bl[perm]
        ex = pm = 0
        for i in range(min(len(A), len(Bp))):
            a, b = A[i], Bp[i]
            if a == a and b == b:
                s = int(a + b)
                ex += s in pool
                pm += any((s + d) in pool for d in (-1, 0, 1))
        null_ex[r] = ex
        null_pm1[r] = pm
    p_ex = (np.sum(null_ex >= obs_ex) + 1) / (N_REP + 1)
    p_pm1 = (np.sum(null_pm1 >= obs_pm1) + 1) / (N_REP + 1)
    print(f"== {qa}+{qb} -> {destinos} (sep={sep})")
    print(f"   pares validos={len(pairs)}  exactos={obs_ex}  (+-1: {obs_pm1})  |  nulo exacto media={null_ex.mean():.2f}  p={p_ex:.4f}  |  nulo +-1 media={null_pm1.mean():.2f} p={p_pm1:.4f}")
    print("   pares:", [(int(a), int(b), int(a + b), (int(a + b) in pool)) for _, a, b in pairs][:40])
    return obs_ex, p_ex


if __name__ == "__main__":
    for sep in "ABC":
        run("UR273A", "UR273B", ["UR266", "UR275", "UR269"], sep)
    for sep in "ABC":
        run("UR267A", "UR267B", ["UR269"], sep)
