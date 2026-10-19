"""Alineación de bandas decimales con tres modelos nulos."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load
from alineacion import quipu_points

RNG = np.random.default_rng(20261018)


def band_table(P, C, E):
    out = []
    for e in np.unique(E):
        m = E == e
        if m.sum() < 2 or len(np.unique(C[m])) < 2:
            continue
        p = P[m]
        med = np.median(p)
        out.append(dict(e=int(e), n=int(m.sum()), med=float(med),
                        mad=float(np.median(np.abs(p - med)))))
    return out


def metrics(P, C, E):
    bt = band_table(P, C, E)
    if len(bt) < 2:
        return None
    n = np.array([b["n"] for b in bt], float)
    mad = np.array([b["mad"] for b in bt], float)
    relmad = float(np.average(mad, weights=n))
    # fraccion de racimos a <=1 cm de la mediana de su banda
    tight = []
    for b in bt:
        p = P[E == b["e"]]
        tight.append(np.mean(np.abs(p - b["med"]) <= 1.0))
    tight = float(np.average(tight, weights=n))
    # espaciado entre bandas consecutivas (por lugar)
    e = np.array([b["e"] for b in bt], float)
    med = np.array([b["med"] for b in bt], float)
    o = np.argsort(e)
    e, med = e[o], med[o]
    if len(e) >= 2:
        sp = (med[:-1] - med[1:]) / (e[1:] - e[:-1])
        spacing = float(np.median(sp))
    else:
        spacing = np.nan
    return dict(relmad=relmad, tight=tight, spacing=spacing, nbands=len(bt))


def shift_positions(P, C, L, kind, rng=RNG):
    cords = np.unique(C)
    span = {c: P[C == c].max() - P[C == c].min() for c in cords}
    starts = {c: P[C == c].min() for c in cords}
    largo = {c: float(np.nanmax(L[C == c])) for c in cords}
    # inicios observados factibles para cada cuerda
    feasible = {}
    for c in cords:
        feasible[c] = [s for s in starts.values()
                       if 0 <= s <= max(0.0, largo[c] - span[c]) + 1e-9]
    delta = {}
    for c in cords:
        m = starts[c]
        if kind.startswith("jitter"):
            s = float(kind.split("_")[1])
            lo = max(-s, -m)
            hi = min(s, max(0.0, largo[c] - span[c]) - m)
            delta[c] = rng.uniform(lo, hi) if hi > lo else 0.0
        elif kind == "startperm":
            cand = feasible[c]
            if cand:
                target = rng.choice(cand)
                delta[c] = target - m
            else:
                delta[c] = 0.0
        elif kind == "free":
            lo = -m
            hi = max(0.0, largo[c] - span[c] - m)
            delta[c] = rng.uniform(lo, hi) if hi > lo else 0.0
    return P + np.array([delta[c] for c in C])


def null_metrics(P, C, E, L, kind, B=199):
    out = []
    for _ in range(B):
        Pn = shift_positions(P, C, L, kind)
        m = metrics(Pn, C, E)
        if m is not None:
            out.append(m)
    if not out:
        return None
    return pd.DataFrame(out)


if __name__ == "__main__":
    d = load()
    rows = []
    for k, g in d[d.nivel == 0].groupby("kfg"):
        r = quipu_points(d, k, unique=True)
        if r is None:
            continue
        P, C, E, L = r
        if len(P) < 8 or len(np.unique(C)) < 5 or len(np.unique(E)) < 2:
            continue
        m = metrics(P, C, E)
        if m is None:
            continue
        row = dict(kfg=k, ncl=len(P), nc=len(np.unique(C)), **m)
        for kind in ["jitter_2.0", "startperm"]:
            nm = null_metrics(P, C, E, L, kind, B=99)
            if nm is None:
                continue
            row["relmad_" + kind] = nm.relmad.median()
            row["tight_" + kind] = nm.tight.median()
            # p unilateral: observado mas tight / menor mad
            row["p_" + kind] = (1 + np.sum(nm.relmad <= m["relmad"])) / (len(nm) + 1)
        rows.append(row)
    R = pd.DataFrame(rows)
    print("quipus", len(R))
    cols = ["relmad", "tight", "spacing", "nbands",
            "relmad_jitter_2.0", "relmad_startperm",
            "tight_jitter_2.0", "tight_startperm"]
    print(R[cols].describe().round(3).to_string())
    for kind in ["jitter_2.0", "startperm"]:
        print("\n--", kind, "p<0.05:", (R["p_" + kind] < 0.05).mean(),
              "n=", (R["p_" + kind] < 0.05).sum())
    print("\nmejores (relmad bajo):")
    print(R.sort_values("relmad").head(12)[["kfg", "ncl", "nc", "nbands", "relmad",
                                             "tight", "spacing", "relmad_startperm", "p_startperm"]].to_string())
    print("\npeores:")
    print(R.sort_values("relmad", ascending=False).head(12)[["kfg", "ncl", "nc", "nbands", "relmad",
                                                              "tight", "spacing", "relmad_startperm", "p_startperm"]].to_string())
    R.to_csv(os.path.join(os.path.dirname(__file__), "bandas_quipu2.csv"), index=False)
