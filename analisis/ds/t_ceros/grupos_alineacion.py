"""Alineación de bandas decimales dentro de grupos de colgantes."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load

RNG = np.random.default_rng(20261019)


def band_metrics(P, E, C):
    vals = []
    for e in sorted(set(E)):
        p = P[E == e]
        if len(p) < 3 or len(set(C[E == e])) < 2:
            continue
        med = np.median(p)
        vals.append((int(e), len(p), float(med), float(np.median(np.abs(p - med)))))
    if len(vals) < 2:
        return None
    n = np.array([v[1] for v in vals], float)
    mad = np.array([v[3] for v in vals], float)
    e = np.array([v[0] for v in vals])
    med = np.array([v[2] for v in vals])
    o = np.argsort(e)
    e, med = e[o], med[o]
    sp = np.median((med[:-1] - med[1:]) / (e[1:] - e[:-1]))
    rel = float(np.average(mad, weights=n)) / abs(sp) if sp != 0 else np.nan
    return float(np.average(mad, weights=n)), float(sp), rel


def shift_group(P, C, spans, starts, L):
    delta = {}
    for c in np.unique(C):
        span = spans[c]
        cand = [s for s in starts.values() if 0 <= s <= max(0.0, L[c] - span) + 1e-9]
        if cand:
            delta[c] = RNG.choice(cand) - starts[c]
        else:
            delta[c] = 0.0
    return P + np.array([delta[c] for c in C])


if __name__ == "__main__":
    d = load()
    rows = []
    for (k, g), gg in d[(d.nivel == 0) & (d.nap >= 1)].groupby(["kfg", "grupo"]):
        pts = [(p, c, e) for _, r in gg.iterrows() for e, v, p in r.ap for c in [r.cuerda]]
        if len(pts) < 8 or gg.cuerda.nunique() < 5:
            continue
        P = np.array([p for p, c, e in pts])
        C = np.array([c for p, c, e in pts])
        E = np.array([e for p, c, e in pts])
        m = band_metrics(P, E, C)
        if m is None or not np.isfinite(m[2]):
            continue
        cords = np.unique(C)
        starts = {c: P[C == c].min() for c in cords}
        spans = {c: P[C == c].max() - P[C == c].min() for c in cords}
        L = {c: float(np.nanmax(gg[gg.cuerda == c].largo)) for c in cords}
        null = []
        for _ in range(49):
            Pn = shift_group(P, C, spans, starts, L)
            m2 = band_metrics(Pn, E, C)
            if m2 is not None and np.isfinite(m2[2]):
                null.append(m2[2])
        if not null:
            continue
        null = np.array(null)
        p = (1 + np.sum(null <= m[2])) / (len(null) + 1)
        rows.append(dict(kfg=k, grupo=g, nc=len(cords), ncl=len(P),
                         mad=m[0], sp=m[1], rel=m[2],
                         rel_null=float(np.median(null)),
                         ratio=m[2] / np.median(null), p=p))
    G = pd.DataFrame(rows)
    G.to_csv(os.path.join(os.path.dirname(__file__), "grupos_bandas_null.csv"), index=False)
    print("grupos", len(G), "quipus", G.kfg.nunique())
    print(G[["nc", "ncl", "mad", "sp", "rel", "rel_null", "ratio"]].describe(
        percentiles=[.25, .5, .75, .9]).round(3).to_string())
    print("p<0.05", (G.p < 0.05).mean(), (G.p < 0.05).sum())
    print("ratio<=0.5", (G.ratio <= .5).mean(), "<=0.8", (G.ratio <= .8).mean())
    print(G.sort_values("ratio").head(5).round(3).to_string())
    print(G.sort_values("ratio", ascending=False).head(10).round(3).to_string())
