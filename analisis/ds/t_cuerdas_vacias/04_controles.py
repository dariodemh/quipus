# -*- coding: utf-8 -*-
"""
04_controles.py -- controles adicionales:
  (a) prueba exacta de posición final en grupos con UNA sola cuerda vacía;
  (b) efecto "última" controlando color y unión;
  (c) ¿son las vacías finales distintas en color/largo?
  (d) agrupamiento tras excluir quipus totalmente vacíos y los 5 mayores;
  (e) efecto por tamaño de grupo.
"""
import os, importlib.util
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
spec = importlib.util.spec_from_file_location("p02", os.path.join(OUT, "02_permutaciones.py"))
p02 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p02)

df = p02.load()
d0 = p02.add_position(df)
k = d0[(d0.terminacion == "K") & (d0.nivel == 0) & (d0.L > 0)].copy()
k = k.sort_values(["kfg", "grupo", "orden"], kind="stable").reset_index(drop=True)
k["rank"] = k.groupby(["kfg", "grupo"]).cumcount() + 1
k["gsize"] = k.groupby(["kfg", "grupo"]).orden.transform("size")
k["is_last"] = k["rank"] == k.gsize
k["is_first"] = k["rank"] == 1

rows = []
def rec(**kw): rows.append(kw)

print("== (a) GRUPOS CON UNA SOLA CUERDA VACÍA ==", flush=True)
g = k.groupby(["kfg", "grupo"])
z = g.apply(lambda s: pd.Series({
    "n": len(s), "m": int(s.sin.sum()),
    "last_empty": bool(s.sort_values("orden").iloc[-1].sin),
    "first_empty": bool(s.sort_values("orden").iloc[0].sin)}), include_groups=False).reset_index()
one = z[(z.m == 1) & (z.n >= 2)].copy()
for col in ["last_empty", "first_empty"]:
    obs = int(one[col].sum()); n = len(one)
    exp = float((1 / one.n).sum()); var = float(((1 / one.n) * (1 - 1 / one.n)).sum())
    zz = (obs - exp) / np.sqrt(var)
    from math import erfc, sqrt
    p = erfc(abs(zz) / sqrt(2))
    print(f"{col}: obs={obs}/{n} ({100*obs/n:.1f}%), esperado={exp:.1f} ({100*exp/n:.1f}%), z={zz:.2f}, p={p:.2e}", flush=True)
    rec(seccion="posicion_exacta", test=col, obs=obs, n=n, esperado=exp, z=zz, p=p)

print("\n== (b) EFECTO ÚLTIMA controlando COLOR / UNIÓN ==", flush=True)
r = p02.perm_diff(k, ["kfg", "pc"], "sin", "is_last", label="last_control_color")
p02.summarize(r, "última | color (estratos quipu×color)"); rec(seccion="control_posicion", **r)
r = p02.perm_diff(k, ["kfg", "un"], "sin", "is_last", label="last_control_union")
p02.summarize(r, "última | unión (estratos quipu×unión)"); rec(seccion="control_posicion", **r)
# por tamaño de grupo
print("por tamaño de grupo (proporción vacía en última vs resto):", flush=True)
for lo, hi in [(2, 2), (3, 3), (4, 4), (5, 9), (10, 19), (20, 100)]:
    s = k[(k.gsize >= lo) & (k.gsize <= hi)]
    d = s.loc[s.is_last, "sin"].mean() - s.loc[~s.is_last, "sin"].mean()
    print(f"  gsize {lo}-{hi}: dif={d:+.3f} (n={len(s)})", flush=True)
    rec(seccion="posicion_tamano", test=f"{lo}-{hi}", obs=float(d), n=len(s))

print("\n== (c) ¿VACÍAS FINALES DISTINTAS? ==", flush=True)
ke = k[k.sin].copy()
# color de las vacías finales vs otras vacías (controlando quipu)
ke["is_last_num"] = ke.is_last.astype(int)
glob, tab = p02.strat_test(ke.assign(sin=ke.is_last.astype(bool)), "pc", label="color_last_vs_other_empty", min_count=30)
print(f"color de vacías finales vs otras: stat={glob['stat']}, p={glob['p']}", flush=True)
print(tab.sort_values("p").head(5).to_string(index=False), flush=True)
rec(seccion="comparacion_vacias", **glob)
r = p02.perm_diff(ke, "kfg", "L", "is_last", label="largo_last_vs_other_empty")
p02.summarize(r, "largo de vacías finales vs otras"); rec(seccion="comparacion_vacias", **r)

print("\n== (d) AGRUPAMIENTO SIN QUIPUS TOTALMENTE VACÍOS / SIN TOP5 ==", flush=True)
def cluster_tests(sub, label):
    sub = sub.sort_values(["kfg", "grupo", "orden"], kind="stable").reset_index(drop=True)
    gsub = p02.Groups(sub, ["kfg", "grupo"]); gk = p02.Groups(sub, "kfg")
    y = sub.sin.values.astype(bool)
    qn = sub.groupby("kfg").size(); qm = sub.groupby("kfg").sin.sum()
    pq = np.array([qm[kk[0]] / qn[kk[0]] for kk in gsub.keys])
    n_g = gsub.sizes
    m_g = np.array([int(y[s:e].sum()) for s, e in zip(gsub.starts, gsub.ends)])
    idx3 = n_g >= 3
    obs_conc = float(np.sum((m_g[idx3] - n_g[idx3] * pq[idx3]) ** 2))
    obs_all = int(np.sum(m_g[n_g >= 2] == n_g[n_g >= 2]))
    same = np.zeros(len(sub) - 1, dtype=bool)
    for s, e in zip(gsub.starts, gsub.ends):
        same[s:e - 1] = True
    obs_adj = int(np.sum(y[:-1] & y[1:] & same))
    rng = np.random.default_rng(99); nc, na, nj = [], [], []
    left = p02.NPERM
    while left > 0:
        B = min(p02.BATCH, left)
        yp = gk.permute(y.astype(float), rng, B)
        S = np.add.reduceat(yp, gsub.starts, axis=0)
        nc.append(np.sum((S[idx3] - n_g[idx3, None] * pq[idx3, None]) ** 2, axis=0))
        na.append(np.sum(S[n_g >= 2] == n_g[n_g >= 2, None], axis=0))
        nj.append(np.sum(yp[:-1] * yp[1:] * same[:, None], axis=0))
        left -= B
    for name, obs, null in [("concentracion", obs_conc, np.concatenate(nc)),
                            ("grupos_100_vacios", obs_all, np.concatenate(na)),
                            ("adyacencia", obs_adj, np.concatenate(nj))]:
        p = (1 + np.sum(null >= obs - 1e-9)) / (p02.NPERM + 1)
        print(f"{label} {name}: obs={obs:.1f}, nulo={null.mean():.1f}±{null.std():.1f}, p={p:.4f}", flush=True)
        rec(seccion="agrupamiento_control", grupo=label, test=name, obs=float(obs),
            null_mean=float(null.mean()), null_sd=float(null.std()), p=float(p))

allblank = df.groupby("kfg").sin.agg(["size", "sum"]); allblank = allblank[allblank["size"] == allblank["sum"]].index.tolist()
print("quipus 100% vacíos:", allblank, flush=True)
cluster_tests(k[~k.kfg.isin(allblank)], "sin_quipus_100_vacios")
top5 = df.groupby("kfg").sin.sum().sort_values(ascending=False).head(5).index.tolist()
cluster_tests(k[~k.kfg.isin(top5)], "sin_top5")

pd.DataFrame(rows).to_csv(os.path.join(OUT, "resultados_controles.csv"), index=False, encoding="utf-8-sig")
print("\nguardado resultados_controles.csv", flush=True)
