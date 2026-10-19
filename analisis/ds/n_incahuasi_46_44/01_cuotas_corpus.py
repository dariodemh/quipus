"""01. Descubrimiento de cuotas constantes en TODO el corpus (651 quipus KFG).

Para cada quipu con >=5 registros (definición del equipo 13: grupo con cabecera
nivel 0 >=100 y >=1 cuerda anudada más) se busca d tal que muchas cabeceras x
tengan una cuerda no cabecera de valor x-d (el "neto"). Es la misma definición
de cuota que 13_sistema_incahuasi/03_constantes.py, aplicada a todo el corpus.

Estadístico: apoyo(d) = nº de registros con una cuerda = x-d, para
d en D = {2..60} U {208} (rango de las cuotas conocidas del archivo y la de UR268).
Nulo: barajar las cuerdas no cabecera entre registros del mismo quipu (conserva
x, tamaños de grupo y multiconjunto de valores). 2000 réplicas. BH-FDR sobre quipus.
"""
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4644
NPERM = 2000
D = np.array([*range(2, 61), 208])
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()


def apoyo(X, rest, D):
    """Matriz booleana (registros x |D|): el registro i tiene x_i - D[j] en rest[i]."""
    H = np.zeros((len(X), len(D)), dtype=bool)
    for i, (x, r) in enumerate(zip(X, rest)):
        v = x - r
        H[i] = np.isin(D, v)
    return H.sum(0)


filas = []
for k, s in c.groupby("kfg", sort=True):
    R = C.registros(s)
    if len(R) < 5:
        continue
    X = np.array([r["cab"] for r in R])
    rest = [np.array(r["resto"], dtype=int) for r in R]
    sizes = [len(r) for r in rest]
    flat = np.concatenate(rest) if sizes else np.array([], dtype=int)
    H = apoyo(X, rest, D)
    obs = int(H.max())
    dbest = int(D[int(H.argmax())])
    nul = np.empty(NPERM, dtype=int)
    for b in range(NPERM):
        rp = np.split(rng.permutation(flat), np.cumsum(sizes)[:-1])
        nul[b] = apoyo(X, rp, D).max()
    p = (np.sum(nul >= obs) + 1) / (NPERM + 1)
    # apoyo dirigido para las cuotas de interés
    dir_ = {f"ap_{d}": int(H[list(D).index(d)]) for d in (44, 46, 47, 25, 30, 15, 10, 17) if d in D}
    filas.append(dict(kfg=k, n=len(R), mejor_d=dbest, apoyo=obs, nulo_media=nul.mean(),
                      nulo_max=nul.max(), p=p, **dir_))
Df = pd.DataFrame(filas).sort_values(["p", "apoyo"], ascending=[True, False])
Df["q"] = C.bh(Df.p)
Df = Df.sort_values(["q", "apoyo"], ascending=[True, False])
Df.to_csv(C.AQUI / "cuotas_corpus.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 250)
print(f"quipus con >=5 registros: {len(Df)}; permutaciones: {NPERM}; p mínimo = {1/(NPERM+1):.5f}")
print(Df.head(20).to_string(index=False))
print("\nquipus con q<0,05 y apoyo>=max(3, 0.5n):")
E = Df[(Df.q < 0.05) & (Df.apoyo >= np.maximum(3, 0.5 * Df.n))]
print(E.to_string(index=False))
print("\nresumen del corpus: apoyo máximo por quipu")
print(Df.apoyo.value_counts().sort_index().to_string())
