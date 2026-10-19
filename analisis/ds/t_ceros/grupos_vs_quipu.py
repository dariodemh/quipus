"""¿La alineación decimal es local a los grupos de colgantes?

Estadístico: dispersión relativa media de las bandas decimales dentro de
cada grupo (MAD / espaciado entre bandas). Nulo: se permutan las etiquetas
de grupo entre las cuerdas del quipu, preservando tamaños de grupo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load

RNG = np.random.default_rng(20261020)


def rel_grupo(P, E, C, min_cl=3):
    vals = []
    for e in sorted(set(E)):
        p = P[E == e]
        if len(p) < min_cl or len(set(C[E == e])) < 2:
            continue
        vals.append((int(e), len(p), float(np.median(p)),
                     float(np.median(np.abs(p - np.median(p))))))
    if len(vals) < 2:
        return np.nan
    n = np.array([v[1] for v in vals], float)
    mad = np.array([v[3] for v in vals], float)
    e = np.array([v[0] for v in vals])
    med = np.array([v[2] for v in vals])
    o = np.argsort(e)
    e, med = e[o], med[o]
    sp = np.median((med[:-1] - med[1:]) / (e[1:] - e[:-1]))
    if sp == 0:
        return np.nan
    return float(np.average(mad, weights=n)) / abs(sp)


def stat_grupos(cords, labels):
    """cords: lista de (P,E). labels: asignación de grupo."""
    s, w = 0.0, 0.0
    for g in np.unique(labels):
        idx = np.where(labels == g)[0]
        P = np.concatenate([cords[i][0] for i in idx])
        E = np.concatenate([cords[i][1] for i in idx])
        if len(P) < 8 or len(idx) < 3:
            continue
        C = np.concatenate([cords[i][2] for i in idx])
        r = rel_grupo(P, E, C)
        if np.isfinite(r):
            s += r * len(P)
            w += len(P)
    return s / w if w else np.nan


def stat_quipu(cords):
    P = np.concatenate([c[0] for c in cords])
    E = np.concatenate([c[1] for c in cords])
    C = np.concatenate([c[2] for c in cords])
    return rel_grupo(P, E, C)


if __name__ == "__main__":
    d = load()
    rows = []
    for k, gg in d[(d.nivel == 0) & (d.nap >= 1)].groupby("kfg"):
        # cuerdas con >=1 racimo
        cords, groups = [], []
        for (g, c), sub in gg.groupby(["grupo", "cuerda"]):
            pts = [(p, e) for _, r in sub.iterrows() for e, v, p in r.ap]
            if not pts:
                continue
            cords.append((np.array([p for p, e in pts]), np.array([e for p, e in pts]), np.array([c] * len(pts))))
            groups.append(g)
        if len(cords) < 10 or len(set(groups)) < 2:
            continue
        # solo grupos con >=5 cuerdas
        groups = np.array(groups)
        ok = [g for g in np.unique(groups) if np.sum(groups == g) >= 5]
        if len(ok) < 2:
            continue
        sel = np.isin(groups, ok)
        cords = [c for c, s in zip(cords, sel) if s]
        groups = groups[sel]
        labels = groups.copy()
        obs = stat_grupos(cords, labels)
        q = stat_quipu(cords)
        if not np.isfinite(obs):
            continue
        null = []
        for _ in range(499):
            RNG.shuffle(labels)
            v = stat_grupos(cords, labels)
            if np.isfinite(v):
                null.append(v)
        null = np.array(null)
        p = (1 + np.sum(null <= obs)) / (len(null) + 1)
        rows.append(dict(kfg=k, nc=len(cords), ngrupos=len(ok),
                         S_grupo=obs, S_quipu=q,
                         S_null=float(np.median(null)), p=p,
                         ratio=obs / np.median(null)))
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(os.path.dirname(__file__), "grupos_vs_quipu.csv"), index=False)
    print("quipus", len(R))
    print(R[["nc", "ngrupos", "S_grupo", "S_quipu", "S_null", "ratio"]].describe(
        percentiles=[.25, .5, .75]).round(3).to_string())
    print("S_grupo < S_quipu:", (R.S_grupo < R.S_quipu).mean())
    print("p<0.05:", (R.p < 0.05).mean(), (R.p < 0.05).sum())
    print("\nmejores:")
    print(R.sort_values("ratio").head(10).round(3).to_string())
    print("\npeores:")
    print(R.sort_values("ratio", ascending=False).head(10).round(3).to_string())
