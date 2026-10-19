"""Tests de independencia/co-variación entre rasgos binarios del quipu.
Unidad de análisis: quipu (estratificación); nulo: permutación dentro de cada quipu
(equivalente a hipergeométrico por estrato). Estadístico CMH.
"""
import numpy as np
import pandas as pd
import prep

d, q = prep.load()
d0 = d[d.nivel == 0].copy()
d0["grupo"] = pd.to_numeric(d0["grupo"], errors="coerce")
d0["valor_n"] = pd.to_numeric(d0["valor_n"], errors="coerce")


def cmh(df, a, b, min_n=6):
    """df con columnas binarias a,b y kfg. Devuelve (chi2, OR_pooled, n_quipus, detalle)."""
    sub = df.dropna(subset=[a, b])
    rows = []
    for k, x in sub.groupby("kfg"):
        n = len(x)
        if n < min_n or x[a].nunique() < 2 or x[b].nunique() < 2:
            continue
        o11 = int(((x[a] == 1) & (x[b] == 1)).sum())
        r1 = int((x[a] == 1).sum())
        c1 = int((x[b] == 1).sum())
        rows.append((k, n, o11, r1, c1))
    t = pd.DataFrame(rows, columns=["kfg", "n", "o11", "r1", "c1"])
    if len(t) == 0:
        return np.nan, np.nan, 0, t
    t["e11"] = t.r1 * t.c1 / t.n
    t["v"] = t.r1 * (t.n - t.r1) * t.c1 * (t.n - t.c1) / (t.n ** 2 * (t.n - 1))
    num = (t.o11 - t.e11).sum()
    chi2 = num ** 2 / t["v"].sum()
    # OR ponderado (Mantel-Haenszel)
    t["a"] = t.o11
    t["b"] = t.r1 - t.o11
    t["c"] = t.c1 - t.o11
    t["dd"] = t.n - t.r1 - t.c1 + t.o11
    or_mh = (t.a * t.dd / t.n).sum() / (t.b * t.c / t.n).sum()
    return chi2, or_mh, len(t), t


def cmh_perm(t, n_perm=5000, seed=20261018):
    rng = np.random.default_rng(seed)
    obs = ((t.o11 - t.e11).sum()) ** 2 / t["v"].sum()
    null = np.empty(n_perm)
    n = t.n.values.astype(int)
    r1 = t.r1.values.astype(int)
    c1 = t.c1.values.astype(int)
    for i in range(n_perm):
        o = rng.hypergeometric(c1, n - c1, r1)
        e = r1 * c1 / n
        rng_var = r1 * (n - r1) * c1 * (n - c1) / (n ** 2 * (n - 1))
        null[i] = ((o - e).sum()) ** 2 / rng_var.sum()
    p = (1 + (null >= obs).sum()) / (n_perm + 1)
    return obs, null, p


if __name__ == "__main__":
    pairs = [("torsion2", "union2"), ("torsion2", "cromatico"), ("union2", "cromatico"),
             ("kdir", "torsion2"), ("kdir", "union2"), ("kdir", "cromatico")]
    # binarias auxiliares
    d0["torZ"] = (d0.torsion2 == "Z").astype(float).where(d0.torsion2.notna())
    d0["uniV"] = (d0.union2 == "V").astype(float).where(d0.union2.notna())
    d0["kdS"] = (d0.kdir == "S").astype(float).where(d0.kdir.isin(["S", "Z"]))
    d0["kdZ"] = (d0.kdir == "Z").astype(float).where(d0.kdir.isin(["S", "Z"]))
    d0["crom"] = d0.cromatico
    tests = [("torZ", "uniV"), ("torZ", "crom"), ("uniV", "crom"),
             ("kdS", "torZ"), ("kdS", "uniV"), ("kdS", "crom")]
    out = []
    for a, b in tests:
        chi2, ormh, nq, t = cmh(d0, a, b)
        obs, null, p = cmh_perm(t)
        signs = np.sign(t.o11 - t.e11)
        out.append(dict(a=a, b=b, chi2=chi2, OR=ormh, nq=nq,
                        pos=int((signs > 0).sum()), neg=int((signs < 0).sum()),
                        null_mean=float(null.mean()), p=p))
        print(out[-1])
    pd.DataFrame(out).to_csv("resultados_cmh.csv", index=False)
