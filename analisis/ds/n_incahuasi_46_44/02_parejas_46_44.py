"""02. ¿Alguna pareja de quipus da, registro a registro, las filas 2-4 de UR269?

(a) Familia dirigida: parejas con cuotas detectadas que sumen 46 o 44 (según 01).
(b) Pantalla exhaustiva: TODAS las parejas de quipus con >=3 registros (definición
    laxa, que recupera componentes fragmentarios como UR273A, 21 registros).
    S_i = A_i + B_i (alineación por índice de registro, sin desfase).
    Objetivos: A = filas 2-4 por posición en bloques de 5; B = registros con cuota
    explícita 46/44. Estadístico: nº de objetivos explicados por el multiconjunto
    de sumas (emparejamiento uno a uno, exacto y ±1).
    Nulo: barajar el orden de los registros de B (2000 réplicas). BH por familia.
(c) Mejores parejas: nulo de magnitud (objetivos sorteados de la distribución de
    cabeceras de UR269) y LCS con las filas en orden.
"""
import itertools
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4602
NPERM = 2000
rng = np.random.default_rng(SEED)


def match1(S, T, tol=0):
    S = np.sort(np.asarray(S)); T = np.sort(np.asarray(T))
    i = j = k = 0
    while i < len(S) and j < len(T):
        if S[i] < T[j] - tol:
            i += 1
        elif S[i] > T[j] + tol:
            j += 1
        else:
            k += 1; i += 1; j += 1
    return k


def lcs(S, T, tol=0):
    n, m = len(S), len(T)
    H = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n):
        for j in range(m):
            H[i + 1, j + 1] = H[i, j] + 1 if abs(int(S[i]) - int(T[j])) <= tol else max(H[i, j + 1], H[i + 1, j])
    return int(H[n, m])


c, q = C.cargar_todo()
O = pd.read_csv(C.AQUI / "ur269_objetivos.csv")
TA = O[O.definicion == "A_posicion"].sort_values("orden").cab.to_numpy(int)
TB = O[O.definicion == "B_cuota"].sort_values("orden").cab.to_numpy(int)
print("objetivos A (posición):", len(TA), TA.tolist())
print("objetivos B (cuota):   ", len(TB), TB.tolist())

R = {}
for k, s in c.groupby("kfg", sort=True):
    X = C.registros_lax(s)
    if len(X) >= 3:
        R[k] = X
print("quipus con >=3 registros:", len(R))

# ---------------------------------------------------------------- (a) dirigida
Q = pd.read_csv(C.AQUI / "cuotas_corpus.csv")
cuotas = {r.kfg: r.mejor_d for r in Q[(Q.q < 0.05) & (Q.apoyo >= 3)].itertuples()}
print("\n(a) cuotas detectadas:", cuotas)
dirigidas = [(a, b, cuotas[a] + cuotas[b]) for a, b in itertools.combinations(sorted(cuotas), 2)
             if cuotas[a] + cuotas[b] in (44, 46)]
print("parejas dirigidas con cuota 44/46:", len(dirigidas), dirigidas)

# ---------------------------------------------------------------- (b) exhaustiva
claves = sorted(R)
filas = []
for a, b in itertools.combinations(claves, 2):
    A, B = R[a], R[b]
    m = min(len(A), len(B))
    S = A[:m] + B[:m]
    r = dict(A=a, B=b, npar=m, obs0=match1(S, TA), obs1=match1(S, TA, 1),
             obs0B=match1(S, TB), obs1B=match1(S, TB, 1))
    if r["obs0"] >= 1 or r["obs1"] >= 2 or r["obs0B"] >= 1 or r["obs1B"] >= 2:
        filas.append(r)
P = pd.DataFrame(filas)
claves_arr = P[["A", "B"]].to_numpy()
print(f"\n(b) parejas totales: {len(claves)*(len(claves)-1)//2}; con señal: {len(P)}")

nul = {k: np.empty((len(P), NPERM), dtype=int) for k in ("n0", "n1", "n0B", "n1B")}
for i, r in enumerate(P.itertuples()):
    A, B = R[r.A], R[r.B]
    m = r.npar
    for j in range(NPERM):
        S = A[:m] + rng.permutation(B)[:m]
        nul["n0"][i, j] = match1(S, TA)
        nul["n1"][i, j] = match1(S, TA, 1)
        nul["n0B"][i, j] = match1(S, TB)
        nul["n1B"][i, j] = match1(S, TB, 1)
mpares = len(claves) * (len(claves) - 1) // 2
for k, obs, tol in (("n0", "obs0", 0), ("n1", "obs1", 1), ("n0B", "obs0B", 0), ("n1B", "obs1B", 1)):
    P[f"p_{k[1:]}"] = [(np.sum(nul[k][i] >= P[obs].iloc[i]) + 1) / (NPERM + 1) for i in range(len(P))]
    P[f"nulo_{k[1:]}"] = nul[k].mean(1)
    # BH sobre la familia COMPLETA: las parejas no preseleccionadas cuentan con p=1
    pfull = np.concatenate([P[f"p_{k[1:]}"].to_numpy(), np.ones(mpares - len(P))])
    P[f"q_{k[1:]}"] = C.bh(pfull)[:len(P)]
P.to_csv(C.AQUI / "parejas_screen.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 260)
cols = ["A", "B", "npar", "obs0", "obs1", "obs0B", "obs1B", "p_0", "p_1", "p_0B", "p_1B",
        "q_0", "q_1", "q_0B", "q_1B"]
print(P.sort_values(["obs0", "obs1", "obs0B", "obs1B"], ascending=False)[cols].head(15).to_string(index=False))
print(f"\npotencia: {mpares} parejas; BH exige p < 0,05/m = {0.05/mpares:.2e}; "
      f"p mínimo con B={NPERM} es {1/(NPERM+1):.5f} -> q mínimo posible = {mpares/(NPERM+1):.2f}")

# ---------------------------------------------------------------- (c) mejores
print("\n(c) control de magnitud y orden en las 5 mejores parejas")
for r in P.sort_values(["obs0", "obs1", "obs0B", "obs1B"], ascending=False).head(5).itertuples():
    A, B = R[r.A], R[r.B]
    m = r.npar
    S = A[:m] + B[:m]
    pool = O.cab.to_numpy(int)
    sims = np.array([match1(S, rng.choice(pool, size=len(TA))) for _ in range(NPERM)])
    pm = (np.sum(sims >= match1(S, TA)) + 1) / (NPERM + 1)
    print(f"{r.A}+{r.B}: S={list(S)}")
    print(f"   obs0={r.obs0} obs1={r.obs1} obs0B={r.obs0B} obs1B={r.obs1B} | "
          f"LCS0={lcs(S, TA)}/{len(TA)} LCS1={lcs(S, TA, 1)} | nulo magnitud p={pm:.4g} "
          f"(medio {sims.mean():.2f})")
