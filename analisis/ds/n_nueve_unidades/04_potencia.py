"""04. Potencia: ¿la ausencia de estructura es informativa o es falta de datos?

(a) Potencia del test de emparejamiento (máx. sobre 945, nulo C) para una estructura de 4 pares
    con correlación intra-par r = 0,3 / 0,4 / 0,5 / 0,6, con el mismo n (24 filas) y las mismas
    desviaciones por columna que UR278. Umbral: percentil 95 del nulo observado (0,291).
(b) Potencia del test de estacionalidad (R2 de cos+sin de periodo 9) y del de extremos para un
    perfil estacional de amplitud creciente. Umbral: p95 del nulo de etiquetas (0,646) y p05 (3).
(c) Estabilidad del perfil entre fases: r(perfil 14 filas, perfil 10 filas) frente a 10 000
    particiones aleatorias de las 24 filas.
Salida: potencia.csv y salida_04.txt.
"""
import itertools
import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
rng = np.random.default_rng(20261020)
COLS = [f"c{i}" for i in range(1, 10)]
LOG = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _emp():
    seen, E = set(), []
    for f in range(9):
        idx = [i for i in range(9) if i != f]
        for a in itertools.combinations(idx, 2):
            r1 = [i for i in idx if i not in a]
            for b in itertools.combinations(r1, 2):
                r2 = [i for i in r1 if i not in b]
                for c in itertools.combinations(r2, 2):
                    d = tuple(i for i in r2 if i not in c)
                    k = tuple(sorted([a, b, c, d]))
                    if k not in seen:
                        seen.add(k)
                        E.append((a, b, c, d))
    return E


EMP = _emp()
E0 = np.array([[m[k][0] for m in EMP] for k in range(4)]).T
E1 = np.array([[m[k][1] for m in EMP] for k in range(4)]).T


def best_pair_r(Z):
    R = np.corrcoef(Z.T)
    return float(R[E0, E1].mean(1).max())


def r2_season(p):
    j = np.arange(9)
    D = np.column_stack([np.ones(9), np.cos(2 * np.pi * j / 9), np.sin(2 * np.pi * j / 9)])
    b, *_ = np.linalg.lstsq(D, p, rcond=None)
    r = p - D @ b
    return 1 - (r @ r) / ((p - p.mean()) @ (p - p.mean()))


def n_extr(p):
    s = np.sign(np.diff(p))
    s = s[s != 0]
    return int((s[1:] != s[:-1]).sum())


def main():
    T = pd.read_csv(AQUI / "ur278_24.csv")
    X = T[COLS].to_numpy(float)
    Z = np.log(X)
    Z = Z - Z.mean(1, keepdims=True)
    sd = Z.std(0, ddof=1)
    med = Z.mean(0)
    n = len(X)
    out(f"n = {n}; SD por columna (clr): {np.round(sd,3).tolist()}")
    out(f"SD media = {sd.mean():.3f}")

    UMBRAL_PAR = 0.2909   # p95 del nulo C de C1 (pruebas.csv, 20 000 réplicas)

    # calibración del umbral en el mismo diseño (H0: sin estructura de pares)
    def simula(r):
        F = rng.normal(size=(n, 4))
        Eps = rng.normal(size=(n, 9))
        Zs = np.empty((n, 9))
        for k, (i, j) in enumerate([(0, 1), (2, 3), (4, 5), (6, 7)]):
            Zs[:, i] = r * F[:, k] + np.sqrt(1 - r ** 2) * Eps[:, i]
            Zs[:, j] = r * F[:, k] + np.sqrt(1 - r ** 2) * Eps[:, j]
        Zs[:, 8] = Eps[:, 8]
        Zs = Zs - Zs.mean(1, keepdims=True)
        return Zs * sd + med

    h0 = np.array([best_pair_r(simula(0.0)) for _ in range(1000)])
    UMBRAL_PAR = float(np.percentile(h0, 95))
    out(f"umbral calibrado (p95 de 1 000 réplicas H0 en el mismo diseño) = {UMBRAL_PAR:.3f}")

    filas = []
    for r in [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        aciertos = 0
        NS = 400
        for s in range(NS):
            aciertos += best_pair_r(simula(r)) > UMBRAL_PAR
        filas.append({"tipo": "pares", "parametro": r, "potencia": aciertos / NS})
        out(f"(a) 4 pares con r intra-par = {r:.1f}: potencia = {aciertos/NS:.3f}")

    # (b) perfil estacional: coseno de periodo 9 con amplitud A (rango pico-valle 2A)
    j = np.arange(9)

    def simula_perfil(A):
        base = A * np.cos(2 * np.pi * (j - 0.5) / 9)
        Zs = base[None, :] + rng.normal(size=(n, 9)) * sd
        Zs = Zs - Zs.mean(1, keepdims=True)
        return Zs.mean(0)

    h0r = np.array([r2_season(simula_perfil(0.0)) for _ in range(1000)])
    h0e = np.array([n_extr(simula_perfil(0.0)) for _ in range(1000)])
    u_r2, u_ex = float(np.percentile(h0r, 95)), float(np.percentile(h0e, 5))
    out(f"umbrales calibrados: R2 p95 = {u_r2:.3f}; extremos p05 = {u_ex:.0f}")
    for A in [0.1, 0.2, 0.4, 0.6, 0.8]:
        acierta_r2 = acierta_ex = 0
        NS = 400
        for s in range(NS):
            p = simula_perfil(A)
            acierta_r2 += r2_season(p) > u_r2
            acierta_ex += n_extr(p) <= u_ex
        filas.append({"tipo": "estacional_R2", "parametro": A, "potencia": acierta_r2 / NS})
        filas.append({"tipo": "estacional_extremos", "parametro": A, "potencia": acierta_ex / NS})
        out(f"(b) perfil coseno amplitud {A:.1f} (rango {2*A:.1f} en log): potencia R2 = {acierta_r2/NS:.3f}; "
            f"potencia extremos<=3 = {acierta_ex/NS:.3f}")

    # (c) estabilidad del perfil entre fases
    g = T.grupo.to_numpy()
    p1, p2 = Z[g < 15].mean(0), Z[g > 15].mean(0)
    robs = np.corrcoef(p1, p2)[0, 1]
    nn = np.empty(10000)
    for b in range(10000):
        i = rng.permutation(n)
        nn[b] = np.corrcoef(Z[i[:14]].mean(0), Z[i[14:]].mean(0))[0, 1]
    pval = (np.sum(nn >= robs) + 1) / 10001
    out(f"(c) r(perfil fase1, fase2) = {robs:.3f}; nulo de particiones {nn.mean():.3f}"
        f" (sd {nn.std():.3f}); p = {pval:.4g}")

    pd.DataFrame(filas).to_csv(AQUI / "potencia.csv", index=False)
    with open(AQUI / "salida_04.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
