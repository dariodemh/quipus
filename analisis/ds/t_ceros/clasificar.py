"""Clasificación final de quipus: alineación global/local y registros no decimales."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from collections import Counter
from explorar import load


def per_quipu(d):
    rows = []
    for k, g in d[d.nivel == 0].groupby("kfg"):
        multi = g[g.nap >= 2]
        pur, dup, inv = [], [], []
        for _, r in multi.iterrows():
            es = [e for e, v, p in r.ap]
            c = Counter(es)
            pur.append(max(c.values()) / len(es))
            dup.append(len(es) != len(set(es)))
        es_all = [e for _, r in g.iterrows() for e, v, p in r.ap]
        rows.append(dict(
            kfg=k, ncords=len(g), n_una=int((g.nap == 1).sum()),
            nmulti=len(multi), purity=np.mean(pur) if pur else np.nan,
            fdup=np.mean(dup) if dup else np.nan,
            nbands_all=len(set(es_all)) if es_all else 0))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    d = load()
    P = per_quipu(d)

    B = pd.read_csv(os.path.join(os.path.dirname(__file__), "bandas_quipu2.csv"))
    B["ratio"] = B.relmad / B.relmad_startperm
    B["rel_q"] = B.relmad / B.spacing.abs()
    B = B[["kfg", "nbands", "relmad", "spacing", "rel_q", "tight", "ratio", "p_startperm"]]

    G = pd.read_csv(os.path.join(os.path.dirname(__file__), "grupos_bandas.csv"))
    G = G.groupby("kfg").agg(rel_g=("rel", "median"), ngrupos=("grupo", "size"),
                              rel_g_max=("rel", "max")).reset_index()

    T = P.merge(B, on="kfg", how="left").merge(G, on="kfg", how="left")
    T["rel_q"] = T.rel_q.replace([np.inf, -np.inf], np.nan)

    def cat(r):
        if r.nmulti < 5:
            return "pocos_datos"
        if r.purity >= .8:
            return "secuencia_no_decimal"
        if pd.notna(r.rel_g) and r.rel_g > .3:
            return "sin_alineacion_local"
        if pd.isna(r.rel_g) and pd.notna(r.rel_q) and r.rel_q > .4:
            return "sin_alineacion_local"
        if pd.notna(r.rel_q) and r.rel_q > .4 and pd.notna(r.rel_g) and r.rel_g <= .15:
            return "alineacion_local_solamente"
        if pd.notna(r.ratio) and r.ratio <= .8:
            return "alineado"
        return "debil"

    T["clase"] = T.apply(cat, axis=1)
    T.to_csv(os.path.join(os.path.dirname(__file__), "clasificacion.csv"), index=False)
    print(T.clase.value_counts().to_string())
    print("\nResumen por clase:")
    print(T.groupby("clase").agg(n=("kfg", "size"), nmulti=("nmulti", "median"),
                                  nbands=("nbands", "median"), rel_q=("rel_q", "median"),
                                  rel_g=("rel_g", "median"), purity=("purity", "median"),
                                  fdup=("fdup", "median")).round(2).to_string())
    for c in ["secuencia_no_decimal", "sin_alineacion_local", "alineacion_local_solamente"]:
        print("\n==", c)
        print(T[T.clase == c].sort_values("nmulti", ascending=False)[
            ["kfg", "nmulti", "nbands_all", "nbands", "rel_q", "rel_g", "ratio", "purity", "fdup"]
        ].head(20).round(2).to_string())
