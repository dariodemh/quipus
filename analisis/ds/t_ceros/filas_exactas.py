"""Prueba libre de etiquetas: coincidencia exacta de alturas entre cuerdas.

No usa exponentes ni valores: solo posiciones en cm. Si los racimos se
talan en filas horizontales, muchos racimos comparten la misma altura
(redondeada a 0.5 cm) con racimos de otras cuerdas.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load

RNG = np.random.default_rng(20261021)


def exact_frac(P, C):
    """Fracción de racimos cuya altura exacta aparece en otra cuerda."""
    n = len(P)
    if n == 0:
        return np.nan
    # para cada altura, cuerdas distintas que la ocupan
    d = {}
    for p, c in zip(P, C):
        d.setdefault(round(p * 2) / 2, set()).add(c)
    ok = sum(1 for p, c in zip(P, C) if len(d[round(p * 2) / 2]) >= 2)
    return ok / n


def shift_grid(P, C, L, rng=RNG, s=2.0):
    cords = np.unique(C)
    delta = {}
    for c in cords:
        m = P[C == c]
        span = m.max() - m.min()
        lim = max(0.0, float(np.nanmax(L[C == c])) - span)
        vals = np.arange(-s, s + 0.25, 0.5)
        vals = vals[(m.min() + vals >= 0) & (m.min() + vals <= lim)]
        delta[c] = rng.choice(vals) if len(vals) else 0.0
    return P + np.array([delta[c] for c in C])


if __name__ == "__main__":
    d = load()
    rows = []
    for k, gg in d[(d.nivel == 0) & (d.nap >= 1)].groupby("kfg"):
        P = np.array([p for _, r in gg.iterrows() for e, v, p in r.ap], float)
        C = np.array([r.cuerda for _, r in gg.iterrows() for e, v, p in r.ap])
        L = np.array([r.largo for _, r in gg.iterrows() for e, v, p in r.ap], float)
        if len(P) < 8 or len(np.unique(C)) < 5:
            continue
        obs = exact_frac(P, C)
        null = np.array([exact_frac(shift_grid(P, C, L), C) for _ in range(199)])
        p = (1 + np.sum(null >= obs)) / (len(null) + 1)
        rows.append(dict(kfg=k, ncl=len(P), nc=len(np.unique(C)),
                         obs=obs, null=np.median(null), p=p,
                         excess=obs - np.median(null)))
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(os.path.dirname(__file__), "filas_exactas.csv"), index=False)
    print("quipus", len(R))
    print(R[["obs", "null", "excess", "p"]].describe(percentiles=[.25, .5, .75]).round(3).to_string())
    print("p<0.05:", (R.p < 0.05).mean(), (R.p < 0.05).sum())
    print("excess>0.1:", (R.excess > .1).mean(), "excess>0.2:", (R.excess > .2).mean())
    print("\ntop:")
    print(R.sort_values("excess", ascending=False).head(8).round(3).to_string())
    print("\nbottom:")
    print(R.sort_values("excess").head(8).round(3).to_string())
