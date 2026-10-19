"""Tarea 1a. Enlaces entre los 52 quipus del archivo por cifras compartidas EN ORDEN.

Secuencia de un quipu = valores >=100 de todas sus cuerdas anudadas (colgantes y subsidiarias), en orden.
Estadístico = LCS tolerante (exacto o ±1 en un dígito) entre A y B.
Nulo (preserva magnitud y orden de magnitudes de B): cada valor de B se sustituye por uno de los 40 valores
del resto del archivo (sin A ni B) más cercanos en escala log. 200 réplicas; 5000 si p<0,05. BH-FDR sobre 1326 pares.
Versión robusta (columna lcs_r): solo valores no múltiplos de 100 y coincidencia exacta (los números
redondos 1000, 2000, 5000... coinciden con tolerancia ±1 dígito por pura convención de redondeo).
Salida: enlaces_valores.csv
"""
import itertools
import numpy as np
import pandas as pd
import comun13 as C
from numba import njit


@njit(cache=True)
def lcs_exacto(x, y):
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            H[i + 1, j + 1] = H[i, j] + 1 if x[i] == y[j] else max(H[i, j + 1], H[i + 1, j])
    return H[n, m]


def prueba(xa, xb, pool, rng, fun):
    obs = fun(xa, xb)
    if len(xa) < 3 or len(xb) < 3:
        return obs, np.nan, 0, 1.0
    f = C.vecinos_magnitud(pool, rng)
    nul = np.array([fun(xa, f(xb)) for _ in range(200)])
    p = (np.sum(nul >= obs) + 1) / 201
    if p < 0.05:
        nul = np.array([fun(xa, f(xb)) for _ in range(5000)])
        p = (np.sum(nul >= obs) + 1) / 5001
    return obs, nul.mean(), nul.max(), p

SEED = 13001
c, q = C.archivo()
pres = c[c.pres & (c.valor >= 100)].sort_values(["kfg", "orden"])
seqs = {k: pres[pres.kfg == k].valor.to_numpy(np.int64) for k in C.ARCHIVO}
ids = [k for k in C.ARCHIVO if len(seqs[k]) >= 3]
rng = np.random.default_rng(SEED)
filas = []
for a, b in itertools.combinations(ids, 2):
    xa, xb = seqs[a], seqs[b]
    pool = np.concatenate([seqs[k] for k in ids if k not in (a, b)])
    obs, nm, nx, p = prueba(xa, xb, pool, rng, C.lcs)
    ra, rb, rp = xa[xa % 100 != 0], xb[xb % 100 != 0], pool[pool % 100 != 0]
    obs_r, nm_r, nx_r, p_r = prueba(ra, rb, rp, rng, lcs_exacto)
    filas.append(dict(A=a, B=b, nA=len(xa), nB=len(xb), exactos_distintos=len(set(xa) & set(xb)),
                      lcs=int(obs), nulo_media=nm, nulo_max=nx, p=p,
                      lcs_r=int(obs_r), nulo_media_r=nm_r, nulo_max_r=nx_r, p_r=p_r))
df = pd.DataFrame(filas)
df["q"] = C.bh(df.p)
df["q_r"] = C.bh(df.p_r)
df = df.sort_values(["p_r", "p"])
df.to_csv(C.AQUI / "enlaces_valores.csv", index=False, float_format="%.4g")
print(f"pares probados: {len(df)}; q<0,05 tolerante: {(df.q < 0.05).sum()}; robusto: {(df.q_r < 0.05).sum()}; "
      f"p_r<0,05: {(df.p_r < 0.05).sum()} (esperados {0.05*len(df):.0f})")
print(df[(df.q < 0.1) | (df.q_r < 0.1)].to_string(index=False))
