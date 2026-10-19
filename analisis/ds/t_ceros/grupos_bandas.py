"""Dispersión de bandas decimales dentro de cada grupo de colgantes (observada)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load


def stats(P, E, C):
    vals = []
    for e in sorted(set(E)):
        p = P[E == e]
        if len(p) < 3 or len(set(C[E == e])) < 2:
            continue
        med = np.median(p)
        vals.append((len(p), float(np.median(np.abs(p - med))), int(e), float(med)))
    if len(vals) < 2:
        return None
    n = np.array([v[0] for v in vals], float)
    mad = np.array([v[1] for v in vals], float)
    e = np.array([v[2] for v in vals])
    med = np.array([v[3] for v in vals])
    o = np.argsort(e)
    e, med = e[o], med[o]
    sp = np.median((med[:-1] - med[1:]) / (e[1:] - e[:-1]))
    if sp == 0:
        return None
    return float(np.average(mad, weights=n)), float(sp), float(np.average(mad, weights=n) / abs(sp))


if __name__ == "__main__":
    d = load()
    rows = []
    for (k, g), gg in d[(d.nivel == 0) & (d.nap >= 1)].groupby(["kfg", "grupo"]):
        pts = [(p, e, c) for _, r in gg.iterrows() for e, v, p in r.ap for c in [r.cuerda]]
        if len(pts) < 8 or gg.cuerda.nunique() < 5:
            continue
        P = np.array([p for p, e, c in pts])
        E = np.array([e for p, e, c in pts])
        C = np.array([c for p, e, c in pts])
        s = stats(P, E, C)
        if s is None:
            continue
        rows.append((k, g, gg.cuerda.nunique(), len(pts), s[0], s[1], s[2]))
    G = pd.DataFrame(rows, columns=["kfg", "grupo", "nc", "ncl", "mad", "sp", "rel"])
    G.to_csv(os.path.join(os.path.dirname(__file__), "grupos_bandas.csv"), index=False)
    print("grupos", len(G), "quipus", G.kfg.nunique())
    print(G[["nc", "ncl", "mad", "sp", "rel"]].describe(percentiles=[.25, .5, .75, .9]).round(3).to_string())
    print("rel<=0.2", (G.rel <= .2).mean(), "<=0.3", (G.rel <= .3).mean())
