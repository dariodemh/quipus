"""Tabla integrada por quipu: estructura decimal, alineación y ceros posicionales."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load
from alineacion import quipu_points


def annotate(d):
    x = d[d.nap >= 1].copy()

    def cat(r):
        es = [e for e, v, p in r.ap]
        if len(es) < 2:
            return "una"
        if len(es) != len(set(es)):
            return "dup"
        a = sorted(r.ap, key=lambda t: t[2])
        es = [e for e, v, p in a]
        if any(es[i] < es[i + 1] for i in range(len(es) - 1)):
            return "inv"
        return "reg"

    def gaps(r):
        es = sorted({e for e, v, p in r.ap})
        if len(es) < 2:
            return []
        return [e for e in range(min(es), max(es) + 1) if e not in es]

    x["cat"] = x.apply(cat, axis=1)
    x["gaps"] = x.apply(gaps, axis=1)
    x["ng"] = x.gaps.map(len)
    return x


def gap_details(d):
    rows = []
    for k, g in d[d.nivel == 0].groupby("kfg"):
        r = quipu_points(d, k, unique=True)
        if r is None:
            continue
        P, C, E, L = r
        for c in sorted(set(C)):
            m = C == c
            if m.sum() < 2:
                continue
            pc, ec = P[m], E[m]
            o = np.argsort(pc)
            pc, ec = pc[o], ec[o]
            es = list(ec)
            if len(es) != len(set(es)):
                continue
            for i in range(len(es) - 1):
                ehi, elo = es[i], es[i + 1]
                for em in range(elo + 1, ehi):
                    phat = pc[i] + (pc[i + 1] - pc[i]) * (ehi - em) / (ehi - elo)
                    om = C != c
                    pos_e = P[om & (E == em)]
                    de = np.min(np.abs(pos_e - phat)) if len(pos_e) else np.nan
                    rows.append(dict(kfg=k, cuerda=c, ehi=ehi, em=em, elo=elo,
                                     p_hi=pc[i], p_lo=pc[i + 1], p_hat=phat,
                                     d_banda=de))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    d = load()
    x = annotate(d)
    x.to_csv(os.path.join(os.path.dirname(__file__), "cuerdas_anotadas.csv"),
             index=False, columns=["kfg", "cuerda", "nivel", "grupo", "valor", "alt",
                                    "nudos", "largo", "cat", "ng"])

    ag = x[x.nivel == 0].groupby("kfg").agg(
        nc=("cuerda", "size"), n_una=("cat", lambda s: (s == "una").sum()),
        nreg=("cat", lambda s: (s == "reg").sum()),
        ndup=("cat", lambda s: (s == "dup").sum()),
        ninv=("cat", lambda s: (s == "inv").sum()),
        ngaps=("ng", "sum")).reset_index()
    ag = ag.rename(columns={"nc": "ncords"})
    ag["n_multi"] = ag.nreg + ag.ndup + ag.ninv
    ag["fdup"] = ag.ndup / ag.n_multi.replace(0, np.nan)
    ag["finv"] = ag.ninv / ag.n_multi.replace(0, np.nan)

    gd = gap_details(d)
    gq = gd.groupby("kfg").agg(nceros=("em", "size"), n_cuerdas_cero=("cuerda", "nunique"),
                                loc=("d_banda", lambda s: np.mean(s <= 1.0)),
                                d_banda_med=("d_banda", "median")).reset_index()

    b = pd.read_csv(os.path.join(os.path.dirname(__file__), "bandas_quipu2.csv"))
    b["ratio"] = b.relmad / b.relmad_startperm
    b["rel"] = b.relmad / b.spacing.abs()

    T = ag.merge(b, on="kfg", how="outer").merge(gq, on="kfg", how="left")
    T = T.merge(pd.read_csv("analisis/datos/quipus.csv")[
        ["kfg", "region", "procedencia", "museo", "pc_largo"]], on="kfg", how="left")
    T.to_csv(os.path.join(os.path.dirname(__file__), "quipus_alineacion.csv"), index=False)
    gd.to_csv(os.path.join(os.path.dirname(__file__), "ceros_detalle.csv"), index=False)

    print("quipus", len(T), "con gap", T.ngaps.gt(0).sum(), "con banda", T.nbands.notna().sum())
    print(T[["ncords", "n_una", "nreg", "ndup", "ninv", "ngaps", "nbands",
             "ratio", "tight", "loc"]].describe().round(2).to_string())
    print("\ncorrelaciones (Spearman):")
    cols = ["ngaps", "nbands", "ratio", "rel", "tight", "loc", "fdup", "ncords"]
    print(T[cols].corr(method="spearman").round(2).to_string())
