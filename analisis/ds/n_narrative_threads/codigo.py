# -*- coding: utf-8 -*-
"""Estructura del codigo: combinaciones de rasgos, bits efectivos, regularidad decimal,
color del cordon principal y tamanos de grupo.
"""
import re
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng = np.random.default_rng(SEED)
d, q = prep.load()
q = q.set_index("kfg")
d0 = d[d.nivel == 0].copy()
d0["valor_n"] = pd.to_numeric(d0["valor_n"], errors="coerce")
d0["uniV"] = (d0.union2 == "V").astype(float).where(d0.union2.notna())
d0["torZ"] = (d0.torsion2 == "Z").astype(float).where(d0.torsion2.notna())
d0["kdS"] = (d0.kdir == "S").astype(float).where(d0.kdir.isin(["S", "Z"]))
d0["crom"] = d0.cromatico

print("=== 1. Combinaciones de 4 rasgos por quipu ===")
rows = []
for k, x in d0.groupby("kfg"):
    y = x.dropna(subset=["uniV", "torZ", "kdS", "crom"])
    if len(y) < 5:
        continue
    comb = (y.uniV.astype(int).astype(str) + y.torZ.astype(int).astype(str)
            + y.kdS.astype(int).astype(str) + y.crom.astype(int).astype(str))
    vc = comb.value_counts(normalize=True)
    ent = -(vc * np.log2(vc)).sum()
    # entropia marginal suma
    marg = 0
    for c in ["uniV", "torZ", "kdS", "crom"]:
        p = y[c].mean()
        if 0 < p < 1:
            marg += -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    rows.append((k, len(y), comb.nunique(), ent, marg, marg - ent))
cc = pd.DataFrame(rows, columns=["kfg", "n", "combos", "H", "H_marg", "MI"])
print(cc[["n", "combos", "H", "H_marg", "MI"]].describe().round(2).to_string())
print("quipus con >=5 cuerdas y 4 rasgos:", len(cc))
print("combinaciones observadas: mediana", cc.combos.median(), "| max", cc.combos.max(),
      "| quipus con 1 sola combinacion:", int((cc.combos == 1).sum()),
      "| con >=6:", int((cc.combos >= 6).sum()))
print("MI mediana:", round(cc.MI.median(), 3), "| MI>0.5:", int((cc.MI > .5).sum()))
cc.to_csv("codigo_combinaciones.csv", index=False)

print("\n=== 2. Regularidad decimal de las cuerdas ===")


def decimal_valid(nudos):
    if not isinstance(nudos, str) or not nudos.strip():
        return np.nan
    places = []
    for m in re.finditer(r"(\d+)([A-Z]+)\(([\d.]+),([A-Z]+)\),([\d.]+)", nudos):
        v = float(m.group(5))
        if v <= 0:
            continue
        p = int(np.floor(np.log10(v)))
        dig = v / (10 ** p)
        if abs(dig - round(dig)) > 1e-9 or not (1 <= round(dig) <= 9):
            return 0
        places.append(p)
    if len(places) < 1:
        return np.nan
    # places deben ser estrictamente decrecientes (de arriba a abajo)
    return int(all(places[i] > places[i + 1] for i in range(len(places) - 1)))


d0["dec_ok"] = d0.nudos.map(decimal_valid)
print("cuerdas evaluables:", int(d0.dec_ok.notna().sum()),
      "| validas:", int((d0.dec_ok == 1).sum()),
      f"({(d0.dec_ok == 1).mean():.3f})")
kk = d0.dropna(subset=["dec_ok"]).groupby("kfg").agg(dec=("dec_ok", "mean"), n=("dec_ok", "size"),
                                                     maxL=("maxL", "max"))
kk = kk[kk.n >= 5]
# nudo largo "narrativo": 10-20 vueltas (Urton 2002: hasta 16); se excluyen
# los valores 100+ que KFG usa para codificar centenas/millares en un nudo.
long10 = d0.nudos.map(lambda s: isinstance(s, str) and any(10 <= int(x) <= 20 for x in re.findall(r"(\d+)L\(", s)))
kk["L10"] = long10.groupby(d0.kfg).any().reindex(kk.index).fillna(False)
print("por quipu: mediana regularidad", round(kk.dec.median(), 3))
print(kk.groupby("L10").dec.agg(["mean", "median", "size"]).round(3).to_string())
obs = kk[kk.L10].dec.mean() - kk[~kk.L10].dec.mean()
null = np.empty(2000)
for i in range(2000):
    lab = rng.permutation(kk.L10.values)
    null[i] = kk.dec.values[lab].mean() - kk.dec.values[~lab].mean()
p = (1 + (np.abs(null) >= abs(obs)).sum()) / 2001
print(f"diferencia (L>=10 - resto) = {obs:.3f}; nulo={null.mean():.3f}; p={p:.4f}")
# correlacion continua
obs2 = kk.dec.corr(kk.maxL, method="spearman")
null2 = np.empty(2000)
for i in range(2000):
    null2[i] = pd.Series(kk.dec.values).corr(pd.Series(rng.permutation(kk.maxL.values)), method="spearman")
p2 = (1 + (np.abs(null2) >= abs(obs2)).sum()) / 2001
print(f"Spearman regularidad vs maxL = {obs2:.3f}; p={p2:.4f}")

print("\n=== 3. Color del cordon principal y paleta de colgantes ===")
pc = q.pc_color.fillna("").map(prep.color_family)
prof = d0.groupby("kfg").agg(crom=("crom", "mean"), n=("crom", "size"))
prof["pc"] = pc.reindex(prof.index).values
prof = prof.dropna(subset=["pc"])
prof = prof[prof.pc != ""]
prof["pc_crom"] = ~prof.pc.isin(["W", "AB", "MB", "KB", "LB", "NB", "DB", "HB", "YB", "B"])
print("quipus con color de cordon principal:", len(prof))
print(prof.groupby("pc_crom").crom.agg(["mean", "size"]).round(3).to_string())
obs = prof[prof.pc_crom].crom.mean() - prof[~prof.pc_crom].crom.mean()
null = np.empty(2000)
for i in range(2000):
    lab = rng.permutation(prof.pc_crom.values)
    null[i] = prof.crom.values[lab].mean() - prof.crom.values[~lab].mean()
p = (1 + (np.abs(null) >= abs(obs)).sum()) / 2001
print(f"diferencia color PC cromatico vs neutro = {obs:.3f}; p={p:.4f}")

print("\n=== 4. Tamanos de grupo ===")
gs = d0.groupby(["kfg", "grupo"]).size().values
vc = pd.Series(gs).value_counts().sort_index()
print(vc.head(16).to_string())
print("total grupos", len(gs), "| media", round(gs.mean(), 2))
