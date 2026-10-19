"""Cifras canónicas del análisis de ceros posicionales."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from collections import Counter
from explorar import load


def main():
    d = load()
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
    x["vint"] = x.valor.astype("Int64")

    out = {}
    out["quipus_total"] = int(d.kfg.nunique())
    out["cuerdas_total"] = int(len(d))
    out["quipus_con_racimos"] = int(x.kfg.nunique())
    out["cuerdas_con_racimos"] = int(len(x))
    out["cat"] = x.cat.value_counts().to_dict()
    out["quipus_por_cat"] = {c: int(x[x.cat == c].kfg.nunique()) for c in ["reg", "dup", "inv"]}
    reg = x[x.cat == "reg"]
    out["reg_multi"] = int(len(reg))
    out["reg_con_cero"] = int((reg.ng > 0).sum())
    out["reg_frac_cero"] = float((reg.ng > 0).mean())
    out["ceros_posiciones"] = int(reg.ng.sum())
    out["quipus_con_cero"] = int(reg[reg.ng > 0].kfg.nunique())
    out["gaps_por_quipu"] = reg[reg.ng > 0].groupby("kfg").ng.sum().describe().round(2).to_dict()
    c = Counter()
    for g in reg.gaps:
        for e in g:
            c[e] += 1
    out["exponente_faltante"] = dict(sorted(c.items()))
    # digitos
    out["cero_interno_por_digitos"] = {}
    for L in [3, 4, 5]:
        m = (reg.valor >= 10 ** (L - 1)) & (reg.valor < 10 ** L)
        sub = reg[m]
        if len(sub):
            out["cero_interno_por_digitos"][L] = dict(
                n=int(len(sub)), frac=float((sub.ng > 0).mean()),
                esperado=float(1 - .9 ** (L - 2)))
    # una cuerda, ceros finales
    one = x[x.cat == "una"]
    v = one.valor.astype(int)
    out["una_cuerdas"] = int(len(one))
    out["una_1a9"] = int(((v >= 1) & (v <= 9)).sum())
    out["una_multiplo10"] = int(((v >= 10) & (v % 10 == 0)).sum())
    out["una_potencia10"] = int(one[v.isin([10 ** k for k in range(1, 6)])].shape[0])
    # duplicados
    multi = x[x.cat.isin(["reg", "dup", "inv"])]
    out["quipus_multi"] = int(multi.kfg.nunique())
    dupq = multi.groupby("kfg").cat.apply(lambda s: (s == "dup").any())
    out["quipus_con_dup"] = int(dupq.sum())
    udup = 0
    pure = []
    for k, g in multi.groupby("kfg"):
        has_u = False
        purs = []
        for _, r in g.iterrows():
            es = [e for e, v, p in r.ap]
            cnt = Counter(es)
            purs.append(max(cnt.values()) / len(es))
            if max(cnt.values()) > 1 and set(es) == {0}:
                has_u = True
        udup += int(has_u)
        pure.append((k, len(g), float(np.mean(purs))))
    out["quipus_con_unidades_dup"] = int(udup)
    P = pd.DataFrame(pure, columns=["kfg", "nmulti", "purity"])
    out["quipus_secuencia"] = int(((P.purity >= .8) & (P.nmulti >= 5)).sum())
    # gaps ratio
    w = {}
    gs = []
    for _, r in reg.iterrows():
        a = sorted(r.ap, key=lambda t: t[2])
        es = [e for e, v, p in a]
        for i in range(len(a) - 1):
            de = es[i] - es[i + 1]
            dp = a[i + 1][2] - a[i][2]
            if de == 1:
                w.setdefault(r.kfg, []).append(dp)
            elif de >= 2:
                gs.append((r.kfg, de, dp))
    G = pd.DataFrame(gs, columns=["kfg", "de", "dp"])
    G["w"] = G.kfg.map(lambda k: np.median(w.get(k, [np.nan])))
    G["ratio"] = G.dp / (G.de * G.w)
    out["gap_ratio_n"] = int(G.ratio.notna().sum())
    out["gap_ratio_mediana"] = float(G.ratio.median())
    out["gap_ratio_iqr"] = [float(v) for v in G.ratio.quantile([.25, .75])]
    out["gap_ratio_dentro_08_12"] = float(((G.ratio >= .8) & (G.ratio <= 1.2)).mean())
    q = G.dropna(subset=["ratio"]).groupby("kfg").agg(
        n=("ratio", "size"), med=("ratio", "median"),
        cv=("ratio", lambda s: s.std() / s.mean() if len(s) > 1 else np.nan))
    out["quipus_3mas_gaps"] = int((q.n >= 3).sum())
    out["cv_ratio_mediana"] = float(q[q.n >= 3].cv.median())

    print(json.dumps(out, indent=2, ensure_ascii=False))
    with open(os.path.join(os.path.dirname(__file__), "cifras.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
