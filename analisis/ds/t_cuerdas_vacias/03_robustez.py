# -*- coding: utf-8 -*-
"""
03_robustez.py -- separa marcadores de longitud 0, repite las pruebas principales
sin ellos, analiza rotas por separado y añade controles cruzados color <-> unión
y sensibilidad a quipus grandes.

Reutiliza el motor de 02_permutaciones.py.
"""
import os, sys, importlib.util
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
spec = importlib.util.spec_from_file_location("p02", os.path.join(OUT, "02_permutaciones.py"))
p02 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p02)

df = p02.load()
d0 = p02.add_position(df)
ds = p02.add_siblings(df)

def reposition(sub):
    drop = [c for c in ["rank", "gsize", "first", "last", "single", "gidx", "ngroups", "gfirst", "glast"] if c in sub.columns]
    sub = sub.drop(columns=drop).sort_values(["kfg", "grupo", "orden"], kind="stable").copy()
    sub["rank"] = sub.groupby(["kfg", "grupo"]).cumcount() + 1
    sub["gsize"] = sub.groupby(["kfg", "grupo"]).orden.transform("size")
    sub["first"] = sub["rank"] == 1
    sub["last"] = sub["rank"] == sub.gsize
    sub["single"] = sub.gsize == 1
    gr = sub[["kfg", "grupo"]].drop_duplicates().sort_values(["kfg", "grupo"])
    gr["gidx"] = gr.groupby("kfg").cumcount() + 1
    gr["ngroups"] = gr.groupby("kfg").grupo.transform("size")
    sub = sub.merge(gr, on=["kfg", "grupo"], how="left")
    sub["gfirst"] = sub.gidx == 1
    sub["glast"] = sub.gidx == sub.ngroups
    return sub

k_all = d0[d0.terminacion == "K"].copy()
k = reposition(k_all[k_all.L > 0])
kmark = k_all[k_all.L == 0].copy()
b = reposition(d0[(d0.terminacion == "B") & (d0.L > 0)].copy())

rows = []
def rec(seccion=None, grupo=None, test=None, **kw):
    rows.append(dict(seccion=seccion, grupo=grupo, test=test, **kw))

print("== 0. TAXONOMÍA DE VACÍAS: longitud 0 vs >0 ==", flush=True)
for name, sub in [("K nivel0", k_all), ("B nivel0", d0[(d0.terminacion == "B") & (d0.nivel == 0)]),
                  ("U nivel0", d0[(d0.terminacion == "U") & (d0.nivel == 0)])]:
    for lab, s in [("todas", sub), ("L=0", sub[sub.L == 0]), ("L>0", sub[sub.L > 0])]:
        rec(seccion="taxonomia", grupo=name, sub=lab, n=len(s), vacias=int(s.sin.sum()),
            pct=round(100 * s.sin.mean(), 1) if len(s) else np.nan)
        if len(s):
            print(f"{name} {lab}: n={len(s)}, vacías={int(s.sin.sum())} ({100*s.sin.mean():.1f}%)", flush=True)

# ---------------------------------------------------------------- posición
def pos_tests(sub, label):
    print(f"\n== POSICIÓN: {label} (n={len(sub)}, vacías={int(sub.sin.sum())}) ==", flush=True)
    for flag, lab in [("first", "primera"), ("last", "última"), ("single", "grupo de 1"),
                      ("gfirst", "primer grupo"), ("glast", "último grupo")]:
        r = p02.perm_diff(sub, "kfg", "sin", flag, label=f"{label}:{lab}")
        if r:
            p02.summarize(r, lab)
            rec(seccion="posicion", grupo=label, **r)
    r = p02.perm_diff(sub, "kfg", "gsize", "sin", label=f"{label}:gsize")
    if r:
        p02.summarize(r, "tamaño de grupo")
        rec(seccion="posicion", grupo=label, **r)

pos_tests(k, "K L>0")
pos_tests(b, "B L>0")

# ---------------------------------------------------------------- agrupamiento
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
    rng = np.random.default_rng(77)
    nc, na, nj = [], [], []
    left = p02.NPERM
    while left > 0:
        B = min(p02.BATCH, left)
        yp = gk.permute(y.astype(float), rng, B)
        S = np.add.reduceat(yp, gsub.starts, axis=0)
        nc.append(np.sum((S[idx3] - n_g[idx3, None] * pq[idx3, None]) ** 2, axis=0))
        na.append(np.sum(S[n_g >= 2] == n_g[n_g >= 2, None], axis=0))
        nj.append(np.sum(yp[:-1] * yp[1:] * same[:, None], axis=0))
        left -= B
    nc = np.concatenate(nc); na = np.concatenate(na); nj = np.concatenate(nj)
    for name, obs, null in [("concentracion", obs_conc, nc), ("grupos_100_vacios", obs_all, na), ("adyacencia", obs_adj, nj)]:
        p = (1 + np.sum(null >= obs - 1e-9)) / (p02.NPERM + 1)
        print(f"{label} {name}: obs={obs:.1f}, nulo={null.mean():.1f}±{null.std():.1f}, p={p:.4f}", flush=True)
        rec(seccion="agrupamiento", grupo=label, test=name, obs=float(obs),
            null_mean=float(null.mean()), null_sd=float(null.std()), p=float(p))

print("\n== AGRUPAMIENTO ==", flush=True)
cluster_tests(k, "K L>0")

# ---------------------------------------------------------------- color / unión
print("\n== COLOR (K nivel0, L>0) ==", flush=True)
glob, tab = p02.strat_test(k, "pc", label="color_K_Lpositivo", min_count=40)
print(f"global: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}, n={glob['n']}", flush=True)
tab.to_csv(os.path.join(OUT, "color_perm_Lpositivo.csv"), index=False, encoding="utf-8-sig")
print(tab.sort_values("p").head(12).to_string(index=False), flush=True)
rec(seccion="color", grupo="K L>0", **glob)

print("\n== UNIÓN (K nivel0, L>0) ==", flush=True)
glob, tabu = p02.strat_test(k, "un", label="union_K_Lpositivo", min_count=30)
print(f"global: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}", flush=True)
tabu.to_csv(os.path.join(OUT, "union_perm_Lpositivo.csv"), index=False, encoding="utf-8-sig")
print(tabu.sort_values("p").to_string(index=False), flush=True)
rec(seccion="union", grupo="K L>0", **glob)

# controles cruzados
print("\n== COLOR controlando unión (sólo R/V) ==", flush=True)
krv = k[k.un.isin(["R", "V"])].copy()
glob, tab = p02.strat_test(krv, "pc", label="color_control_union", min_count=30, stratcols=["kfg", "un"])
print(f"global: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}, n={glob['n']}", flush=True)
print(tab.sort_values("p").head(8).to_string(index=False), flush=True)
rec(seccion="color_control", grupo="R/V", **glob)

print("\n== UNIÓN controlando color (colores frecuentes) ==", flush=True)
topc = k.pc.value_counts(); topc = topc[topc >= 100].index.tolist()
kc = k[k.pc.isin(topc)].copy()
glob, tab = p02.strat_test(kc, "un", label="union_control_color", min_count=30, stratcols=["kfg", "pc"])
print(f"global: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}, n={glob['n']}", flush=True)
print(tab.sort_values("p").to_string(index=False), flush=True)
rec(seccion="union_control", grupo="colores frecuentes", **glob)

# ---------------------------------------------------------------- largo
print("\n== LARGO (K nivel0, L>0) ==", flush=True)
r = p02.perm_diff(k, "kfg", "L", "sin", label="largo_K_Lpositivo")
p02.summarize(r, "largo K L>0")
rec(seccion="largo", grupo="K L>0", **r)
print("\n== LARGO rotas (B nivel0, L>0) ==", flush=True)
r = p02.perm_diff(b, "kfg", "L", "sin", label="largo_B_Lpositivo")
p02.summarize(r, "largo B L>0")
rec(seccion="largo", grupo="B L>0", **r)

# ---------------------------------------------------------------- sensibilidad
print("\n== SENSIBILIDAD: excluir 5 quipus con más vacías ==", flush=True)
top5 = df.groupby("kfg").sin.sum().sort_values(ascending=False).head(5).index.tolist()
print("excluidos:", top5, flush=True)
k_s = reposition(k[~k.kfg.isin(top5)])
r = p02.perm_diff(k_s, "kfg", "sin", "last", label="last_sin_top5")
p02.summarize(r, "última (sin top5)")
rec(seccion="sensibilidad", grupo="sin_top5", **r)
glob, _ = p02.strat_test(k_s, "pc", label="color_sin_top5", min_count=40)
print(f"color global sin top5: stat={glob['stat']}, p={glob['p']}", flush=True)
rec(seccion="sensibilidad", grupo="sin_top5", **glob)

print("\n== SENSIBILIDAD: excluir quipus >500 cuerdas ==", flush=True)
big = df.groupby("kfg").size(); big = big[big > 500].index.tolist()
print("excluidos:", big, flush=True)
k_s2 = reposition(k[~k.kfg.isin(big)])
r = p02.perm_diff(k_s2, "kfg", "sin", "last", label="last_sin_grandes")
p02.summarize(r, "última (sin grandes)")
rec(seccion="sensibilidad", grupo="sin_grandes", **r)
glob, _ = p02.strat_test(k_s2, "pc", label="color_sin_grandes", min_count=40)
print(f"color global sin grandes: stat={glob['stat']}, p={glob['p']}", flush=True)
rec(seccion="sensibilidad", grupo="sin_grandes", **glob)

pd.DataFrame(rows).to_csv(os.path.join(OUT, "resultados_robustez.csv"), index=False, encoding="utf-8-sig")
print("\nguardado resultados_robustez.csv", flush=True)
