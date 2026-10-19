"""D3. Cadenas de cabeceras: los totales de grupo de A aparecen como cabeceras de grupo de B
en el mismo orden (LCS ordenada).

Secuencia A = total de colgantes (nivel 0) de cada grupo/registro, en orden.
Secuencia B = cabecera (primer colgante anudado) de cada grupo/registro de B, en orden.
Coincidencia exacta o +-1 digito. Estadistico = longitud de la subsecuencia comun mas larga.

Se prueban todos los pares ordenados (A,B) de quipus con >=3 registros (A != B, sin copias).
Nulo: barajar la secuencia de cabeceras de B (conserva multiconjunto y magnitudes; rompe el orden),
1000 replicas. Solo se prueba en pares con LCS>=3; el resto p=1 (conservador).
BH por detector sobre todos los pares ordenados probados.

Control positivo: UR278 -> UR266 y UR278 -> UR275 (totales de fila de UR278 = cabeceras).
Salida: d3_cadenas.csv
"""
import numpy as np
import pandas as pd
from numba import njit
import comun as C

NPERM = 1000
SEED = C.SEMILLA + 3
rng = np.random.default_rng(SEED)


@njit(cache=True)
def _tol(d):
    d = abs(d)
    return d == 0 or d == 1 or d == 10 or d == 100 or d == 1000 or d == 10000


@njit(cache=True)
def lcs(x, y):
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            if _tol(x[i] - y[j]):
                H[i + 1, j + 1] = H[i, j] + 1
            else:
                H[i + 1, j + 1] = max(H[i, j + 1], H[i + 1, j])
    return H[n, m]


@njit(cache=True)
def lcs_nulo(x, y, R, seed):
    np.random.seed(seed)
    out = np.zeros(R, dtype=np.int32)
    yy = y.copy()
    for r in range(R):
        np.random.shuffle(yy)
        out[r] = lcs(x, yy)
    return out


def main():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    tot, cab = {}, {}
    for k, recs in R.items():
        if len(recs) < 3:
            continue
        t = [int(np.sum(r["pend"])) for r in recs if len(r["pend"]) > 0]
        h = [r["x"] for r in recs if r["x"] > 0]
        if len(t) >= 3 or len(h) >= 3:
            tot[k] = np.array(t, dtype=np.int64)
            cab[k] = np.array(h, dtype=np.int64)
    ks = sorted(tot)
    fp, fm = C.familias(q)

    def familia(a, b):
        if a in fp and b in fp and fp[a] == fp[b]:
            return "proc:" + str(fp[a][1])
        if a in fm and b in fm and fm[a] == fm[b]:
            return "museo:" + str(fm[a][1])
        return "global"

    print(f"quipus {len(ks)}")
    pares = [(a, b) for a in ks for b in ks if a != b and not C.excluido(a, b)]
    print(f"pares ordenados: {len(pares)}")
    filas = []
    for n, (a, b) in enumerate(pares):
        x, y = tot[a], cab[b]
        if len(x) < 3 or len(y) < 3:
            continue
        obs = int(lcs(x, y))
        filas.append((a, b, len(x), len(y), obs, familia(a, b)))
        if (n + 1) % 50000 == 0:
            print(" ", n + 1)
    D = pd.DataFrame(filas, columns=["A", "B", "nA", "nB", "lcs", "familia"])
    D.to_csv(C.AQUI / "d3_observado.csv", index=False)
    print(D.lcs.value_counts().sort_index().head(12).to_string())
    print(f"pares lcs>=3: {(D.lcs >= 3).sum()}; lcs>=4: {(D.lcs >= 4).sum()}; lcs>=5: {(D.lcs >= 5).sum()}")

    cand = D[D.lcs >= 3].copy()
    print(f"candidatos a nulo: {len(cand)}")
    pv = np.ones(len(cand)); nm = np.zeros(len(cand)); nx = np.zeros(len(cand))
    for pos, (ix, r) in enumerate(cand.iterrows()):
        nul = lcs_nulo(tot[r.A], cab[r.B], NPERM, int(SEED + pos))
        nm[pos], nx[pos] = nul.mean(), nul.max()
        pv[pos] = (np.sum(nul >= r.lcs) + 1) / (NPERM + 1)
        if (pos + 1) % 5000 == 0:
            print("  nulo", pos + 1)
    cand["nulo_media"] = nm; cand["nulo_max"] = nx; cand["p"] = pv
    D["p"] = 1.0
    D.loc[cand.index, "p"] = cand.p
    D["q"] = C.bh(D.p)
    D["q_familia"] = np.nan
    for fam, idx in D.groupby("familia").groups.items():
        D.loc[idx, "q_familia"] = C.bh(D.loc[idx, "p"])
    D.to_csv(C.AQUI / "d3_cadenas.csv", index=False, float_format="%.4g")
    cand["q"] = D.loc[cand.index, "q"]
    cand["q_familia"] = D.loc[cand.index, "q_familia"]
    cand = cand.sort_values(["p", "lcs"], ascending=[True, False])
    cand.to_csv(C.AQUI / "d3_candidatos.csv", index=False, float_format="%.4g")
    print(cand.head(25).to_string(index=False))
    print("\nCONTROLES:")
    print(cand[((cand.A == "UR278") & (cand.B.isin(["UR266", "UR275"]))) |
               ((cand.A == "UR273A") & (cand.B.isin(["UR266", "UR275"])))].to_string(index=False))


if __name__ == "__main__":
    main()
