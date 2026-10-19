# -*- coding: utf-8 -*-
"""Cifras de cobertura y defectos internos de cada fuente."""
import os, sqlite3
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")
DB = os.path.join(ROOT, "data", "external", "open-khipu-repository", "data", "khipu.db")

kfg = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
qu = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "quipus.csv"))
mp = pd.read_csv(os.path.join(SAL, "mapa_quipus.csv"))
con = sqlite3.connect(DB)
cord = pd.read_sql("select KHIPU_ID,CORD_ID,CORD_LEVEL,CORD_LENGTH from cord", con)
kn = pd.read_sql("select CORD_ID,TYPE_CODE,knot_value_type,NUM_TURNS from knot", con)
kc = pd.read_sql("select CORD_ID,CLUSTER_ID,TOTAL_VALUE,NUM_KNOTS from knot_cluster", con)
con.close()

print("=== cobertura ===")
print("quipus KFG:", len(qu), "| mapeados a OKR:", mp.KHIPU_ID.notna().sum(),
      "| sin mapear:", mp.KHIPU_ID.isna().sum())
print("cuerdas KFG:", len(kfg))
sinq = set(mp[mp.KHIPU_ID.isna()].kfg)
print("cuerdas en quipus sin mapear:", kfg.kfg.isin(sinq).sum())
j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
print("cuerdas KFG emparejadas por nombre:", len(j),
      "| en quipus mapeados pero sin pareja:", len(kfg[~kfg.kfg.isin(sinq)]) - len(j))
print("cuerdas OKR con nombre asignado:", len(pd.read_csv(os.path.join(SAL, "mapa_cuerdas_okr.csv"))),
      "| total OKR:", len(cord), "| quipus OKR:", cord.KHIPU_ID.nunique())

print("\n=== OKR: campos de valor ===")
print("knots:", len(kn), "| knot_value_type=0:", (kn.knot_value_type == 0).sum())
print("nudos L/LL con NUM_TURNS>0 y vt=0 (recuperados con vueltas):",
      ((kn.knot_value_type <= 0) & kn.TYPE_CODE.isin(["L", "LL"]) & (kn.NUM_TURNS > 0)).sum())
print("knot_value_type=0 por tipo:")
print(kn[kn.knot_value_type == 0].TYPE_CODE.fillna("(vacio)").value_counts().head(8).to_string())
print("knot_cluster:", len(kc), "| TOTAL_VALUE != 0:", (kc.TOTAL_VALUE.fillna(0) != 0).sum())

print("\n=== KFG: consistencia interna ===")
import re
RE = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")
def suma(s):
    if not isinstance(s, str):
        return np.nan
    return sum(float(m.group(5)) for m in RE.finditer(s))
v = kfg.nudos.apply(suma)
mal = (kfg.nudos.notna()) & (~np.isclose(kfg.valor.fillna(0), v.fillna(0)))
print("cuerdas con nudos:", kfg.nudos.notna().sum(),
      "| cadenas sin valor explicito tras la coma:", mal.sum())
print(kfg[mal][["kfg", "cuerda", "valor", "nudos"]].head(5).to_string())

print("\n=== KFG: duplicados ===")
dup = kfg[kfg.duplicated(["kfg", "cuerda"], False)]
print("filas con (kfg,cuerda) repetido:", len(dup), "| quipus:", dup.kfg.nunique(),
      list(dup.kfg.unique()))

print("\n=== largos: magnitud de la diferencia (solo diferencias >0) ===")
jx = j[~j.kfg.isin({"KH0197", "KH0227", "KH0267", "KH0350", "UR196", "MM007_AN002"})]
d = jx.dlargo.dropna()
print("cuerdas con largo identico:", (d == 0).sum(), "de", len(d))
dd = d[d > 0]
print(pd.cut(dd, [0, 0.51, 2, 10, 1e9], labels=["<=0.5", "0.5-2", "2-10", ">10"]).value_counts().sort_index().to_string())

print("\n=== multiset de valores por quipu (solo largos que coinciden) ===")
g = pd.read_csv(os.path.join(SAL, "por_quipu_final.csv"), index_col=0)
g = g[~g.index.isin({"KH0197", "KH0227", "KH0267", "KH0350",
                     "UR196", "MM007_AN002"})]
jj = jx[jx.dlargo <= 0.51]
equal = []
for k, x in jj.groupby("kfg"):
    if len(x) >= 5:
        equal.append((k, sorted(x.valor.fillna(0)) == sorted(x.valor_okr.fillna(0))))
eq = pd.DataFrame(equal, columns=["kfg", "multiset_igual"])
print("quipus con >=5 cuerdas comparables:", len(eq),
      "| multiset igual:", eq.multiset_igual.sum())

print("\n=== nulo: cuantos quipus con >5% se esperan por azar ===")
rng = np.random.default_rng(20261018)
g2 = g[g.n_valor > 0]
n = g2.n_valor.values
p0 = g2.disc_valor.sum() / g2.n_valor.sum()
obs = ((g2.disc_valor / g2.n_valor > 0.05)).sum()
sims = []
for _ in range(5000):
    x = rng.binomial(n, p0)
    sims.append(((x / n) > 0.05).sum())
sims = np.array(sims)
print("tasa global de referencia:", round(p0, 5))
print("quipus con denominador>0:", len(g2), "| observados >5%:", obs,
      "| esperados (media simulada):", round(sims.mean(), 2),
      "| p(sim >= obs):", (1 + (sims >= obs).sum()) / 5001)
