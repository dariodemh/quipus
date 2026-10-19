"""Tarea 2. UR278 como tabla: ¿qué son sus filas y columnas?

Filas = grupos con >=7 colgantes anudados (los 33 «registros» de 04). Columnas = posición del colgante en el grupo.
(a) Efecto de fila: correlación media de Spearman entre columnas a través de filas (filas «grandes» en todas las
    columnas); nulo = barajar cada columna entre filas por separado (rompe solo la covariación de fila). 5000 réplicas.
(b) Efecto de columna: estadístico de Friedman sobre rangos dentro de fila; nulo = permutar dentro de cada fila.
(c) Columnas gemelas: nº de filas con |col_i - col_j| <= 1 para cada par (i,j); nulo = permutar dentro de fila.
    BH sobre los 36 pares.
(d) Dispersión dentro de fila: CV dentro de fila frente al nulo que reparte las cuerdas al azar entre filas.
(e) Bloques de color: secuencia de color dominante por fila.
Salida: salida_05_ur278.txt (impresa), ur278_tabla.csv
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, friedmanchisquare
import comun13 as C

SEED = 13005
rng = np.random.default_rng(SEED)
c, q = C.archivo()
s = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
filas = []
for g, x in s.groupby("grupo"):
    if x.pres.sum() >= 7:
        v = x.valor.astype(float).where(x.pres, np.nan).to_numpy()[:9]
        col = x.color.str.split(r"[(\s]", regex=True).str[0].mode().iloc[0]
        filas.append([g, col, x.pres.sum(), x[x.pres].valor.sum()] + list(np.pad(v, (0, 9 - len(v)), constant_values=np.nan)))
T = pd.DataFrame(filas, columns=["grupo", "color", "n", "total"] + [f"c{i+1}" for i in range(9)])
T.to_csv(C.AQUI / "ur278_tabla.csv", index=False)
M = T[[f"c{i+1}" for i in range(9)]].to_numpy(float)
print(f"UR278: {len(T)} filas con >=7 colgantes anudados; filas completas (9): {np.isfinite(M).all(1).sum()}")
print(T.to_string(index=False))

full = M[np.isfinite(M).all(1)]


def rho_medio(X):
    r = spearmanr(X).correlation
    return r[np.triu_indices(9, 1)].mean()


obs = rho_medio(full)
nul = np.array([rho_medio(np.column_stack([rng.permutation(full[:, j]) for j in range(9)])) for _ in range(5000)])
print(f"\n(a) efecto de fila: rho medio entre columnas = {obs:.3f}; nulo {nul.mean():.3f} (máx {nul.max():.3f}); p = {(np.sum(nul >= obs)+1)/5001:.4g}")

fr = friedmanchisquare(*full.T).statistic
nulf = np.array([friedmanchisquare(*np.array([rng.permutation(r) for r in full]).T).statistic for _ in range(5000)])
print(f"(b) efecto de columna: Friedman = {fr:.1f}; nulo {nulf.mean():.1f}; p = {(np.sum(nulf >= fr)+1)/5001:.4g}")
rk = np.argsort(np.argsort(-full, axis=1), axis=1) + 1
print("    rango medio por columna (1 = mayor de la fila):", np.round(rk.mean(0), 2))
print("    mediana por columna:", np.median(full, 0))
print("    columna que es mínima de la fila (frecuencia):", np.bincount(np.argmin(full, 1), minlength=9) )

pares = []
for i in range(9):
    for j in range(i + 1, 9):
        o = int(np.sum(np.abs(full[:, i] - full[:, j]) <= 1))
        nn = []
        for _ in range(2000):
            P = np.array([rng.permutation(r) for r in full])
            nn.append(np.sum(np.abs(P[:, i] - P[:, j]) <= 1))
        nn = np.array(nn)
        pares.append((i + 1, j + 1, o, nn.mean(), (np.sum(nn >= o) + 1) / 2001))
P = pd.DataFrame(pares, columns=["col_i", "col_j", "filas_casi_iguales", "nulo", "p"])
P["q"] = C.bh(P.p)
print("\n(c) columnas gemelas (|ci-cj|<=1) con q<0,05:")
print(P[P.q < 0.05].sort_values("p").to_string(index=False))
print(f"    total de pares casi iguales: {P.filas_casi_iguales.sum()} frente a {P.nulo.sum():.1f} bajo permutación dentro de fila")

cv = np.std(full, 1) / np.mean(full, 1)
flat = full.ravel()
nulcv = np.array([np.mean([np.std(r) / np.mean(r) for r in rng.permutation(flat).reshape(full.shape)]) for _ in range(2000)])
print(f"\n(d) CV medio dentro de fila = {cv.mean():.3f}; nulo (cuerdas repartidas al azar) {nulcv.mean():.3f}; p = {(np.sum(nulcv <= cv.mean())+1)/2001:.4g}")
print("\n(e) color dominante por fila:", " ".join(f"g{g}:{col}" for g, col in zip(T.grupo, T.color)))
