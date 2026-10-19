"""05. Control positivo: ¿la maquinaria detecta las parejas ya demostradas?

Se usan las sumas registro a registro que el equipo 13 calculó en
`13_sistema_incahuasi/componentes_filas.csv` (parte_A + parte_B, emparejando por
número de grupo) y se comprueba si aparecen en los objetivos de UR269 definidos
por cuota. Esto valida (a) que los conjuntos de objetivos 47 y 25 son los correctos
y (b) que el estadístico tiene potencia para detectar un flujo real.
Nulo: barajar parte_B dentro de la pareja y recalcular las sumas.
"""
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4606
NPERM = 2000
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()
F, _ = C.registros_ur269(c[c.kfg == "UR269"])
OBJ = {f"cuota_{int(cu)}": F[F.cuota == cu].sort_values(["bloque", "fila"]).cab.to_numpy(int)
       for cu in (47, 46, 44, 25)}
for k, v in OBJ.items():
    print(k, len(v), v.tolist())


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


CF = pd.read_csv(C.RAIZ / "analisis/13_sistema_incahuasi/componentes_filas.csv")
filas = []
for fuente in ["UR273A+UR273B", "UR274A+UR273B", "UR267A+UR267B", "UR267A+UR256"]:
    x = CF[CF.fuente == fuente].sort_values("registro")
    if not len(x):
        continue
    A = x.parte_A.to_numpy(int); B = x.parte_B.to_numpy(int)
    S = A + B
    for nom, T in OBJ.items():
        o = match1(S, T); o1 = match1(S, T, 1)
        nul = np.array([match1(A + rng.permutation(B), T) for _ in range(NPERM)])
        filas.append(dict(pareja=fuente, n=len(S), objetivos=nom, obs0=o, obs1=o1,
                          lcs=lcs(S, T), nulo_medio=nul.mean(), nulo_max=nul.max(),
                          p=(np.sum(nul >= o) + 1) / (NPERM + 1)))
        print(f"{fuente} ({len(S)}) vs {nom} (n={len(T)}): obs0={o} obs1={o1} "
              f"LCS={lcs(S, T)}/{len(T)} nulo {nul.mean():.2f} (máx {nul.max()}) "
              f"p={(np.sum(nul >= o) + 1) / (NPERM + 1):.4f}")
D = pd.DataFrame(filas)
D.to_csv(C.AQUI / "control_positivo.csv", index=False, float_format="%.4g")
print("\nresumen (obs0):")
print(D.pivot(index="pareja", columns="objetivos", values="obs0").to_string())
