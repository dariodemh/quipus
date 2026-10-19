"""Prototipo de alineación: ¿se alinean los racimos entre cuerdas?"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load

rng = np.random.default_rng(20261017)


def quipu_points(d, k, nivel=0, unique=False):
    x = d[(d.kfg == k) & (d.nivel == nivel) & (d.nap >= 1)]
    pts = []
    for _, r in x.iterrows():
        ap = r.ap
        if unique:
            es = [e for e, v, p in ap]
            if len(es) != len(set(es)):
                continue
        for e, v, p in ap:
            pts.append((p, r.cuerda, e, r.largo))
    if not pts:
        return None
    P = np.array([p for p, c, e, L in pts], float)
    C = np.array([c for p, c, e, L in pts])
    E = np.array([e for p, c, e, L in pts])
    L = np.array([L for p, c, e, L in pts], float)
    return P, C, E, L


def rowscore(P, C, tol=1.0):
    """Media de vecinos de otra cuerda dentro de tol cm (por racimo)."""
    n = len(P)
    if n < 2:
        return np.nan
    order = np.argsort(P)
    Ps, Cs = P[order], C[order]
    # ventana
    lo = np.searchsorted(Ps, Ps - tol, side="left")
    hi = np.searchsorted(Ps, Ps + tol, side="right")
    total = hi - lo - 1  # excluye el propio punto
    # mismos cordones dentro de la ventana: pequeño, contar por cuerda
    same = np.zeros(n, int)
    # como cada cuerda tiene pocos puntos, contar directo
    for i in range(n):
        same[i] = np.sum((Cs[lo[i]:hi[i]] == Cs[i])) - 1
    other = total - same
    return float(np.mean(other))


def shift_null(P, C, L, B=199, s=2.0, tol=1.0):
    """Nulo: desplaza el bloque de nudos de cada cuerda U(-s,s)."""
    cords = np.unique(C)
    out = []
    for _ in range(B):
        delta = rng.uniform(-s, s, size=len(cords))
        dd = dict(zip(cords, delta))
        dvec = np.array([dd[c] for c in C])
        Pn = P + dvec
        out.append(rowscore(Pn, C, tol))
    return np.array(out)


if __name__ == "__main__":
    d = load()
    rows = []
    for k, g in d[d.nivel == 0].groupby("kfg"):
        r = quipu_points(d, k, unique=True)
        if r is None:
            continue
        P, C, E, L = r
        if len(P) < 8 or len(np.unique(C)) < 5:
            continue
        obs = rowscore(P, C, 1.0)
        null = shift_null(P, C, L, B=199, s=2.0, tol=1.0)
        z = (obs - null.mean()) / (null.std() + 1e-9)
        p = (1 + np.sum(null >= obs)) / (len(null) + 1)
        rows.append(dict(kfg=k, ncl=len(P), nc=len(np.unique(C)), obs=obs,
                         nullmed=np.median(null), z=z, p=p))
    R = pd.DataFrame(rows)
    print("quipus analizados", len(R))
    print(R[["obs", "nullmed", "z", "p"]].describe().round(3).to_string())
    print("p<0.05:", (R.p < 0.05).mean(), "n=", (R.p < 0.05).sum())
    print("\nmas alineados:")
    print(R.sort_values("z", ascending=False).head(10).to_string())
    print("\nmenos alineados:")
    print(R.sort_values("z").head(10).to_string())
