# -*- coding: utf-8 -*-
"""Grupos de 9 cuerdas en todo el corpus KFG: cuantos tienen 9 valores iguales
o casi iguales, y contraste con un nulo que baraja las cuerdas dentro de cada
quipu (conserva la distribucion de valores del quipu y los tamanos de grupo).

Salida: grupos9.csv, pruebas_grupos9.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import false_discovery_control

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SEED = 20261018
NPERM = 10000
rng = np.random.default_rng(SEED)

c = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
c["pres"] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != "") & c.valor.notna()
c0 = c[(c.nivel == 0) & c.pres].copy()
c0["valor"] = c0.valor.astype(float)

# grupos de exactamente 9 colgantes, todos anudados, valores > 0
rows = []
for (k, g), x in c0.groupby(["kfg", "grupo"]):
    if len(x) != 9:
        continue
    v = x.sort_values("orden").valor.values.astype(float)
    if not (v > 0).all():
        continue
    rows.append((k, int(g), v))
print("grupos de 9 con 9 valores > 0:", len(rows))


def metricas(v):
    m = v.mean()
    cv = v.std() / m if m else np.nan
    return dict(
        media=m, cv=cv, rango=v.max() - v.min(), distintos=len(set(v)),
        eq_all=int(len(set(v)) == 1), range1=int(v.max() - v.min() <= 1),
        cv05=int(cv <= 0.05), cv10=int(cv <= 0.10),
        ties=sum(v[i] == v[j] for i in range(9) for j in range(i + 1, 9)),
    )

D = []
for k, g, v in rows:
    D.append(dict(kfg=k, grupo=g, **metricas(v), vector=" ".join(str(int(z)) for z in v)))
D = pd.DataFrame(D)
D.to_csv(AQUI / "grupos9.csv", index=False)

print("\nResumen observado (237 grupos):")
for col in ["eq_all", "range1", "cv05", "cv10", "ties"]:
    print(f"  {col}: {int(D[col].sum())} grupos / {D[col].mean():.4f} por grupo")
print(f"  CV medio: {D.cv.mean():.3f}; mediana: {D.cv.median():.3f}")
print("\nGrupos mas planos:")
print(D.nsmallest(12, "cv")[["kfg", "grupo", "media", "cv", "rango", "distintos", "ties", "vector"]].to_string(index=False))

# ---------------- Nulo: barajar cuerdas dentro de cada quipu ----------------
# Para cada quipu, pool de valores de nivel 0; cada grupo de 9 toma 9 sin reemplazo.
pools = {k: x.valor.values.astype(float) for k, x in c0.groupby("kfg")}
porq = D.groupby("kfg")
obs_q = {k: d[["eq_all", "range1", "cv05", "cv10", "ties"]].sum().to_dict() for k, d in porq}
obs_cv_q = {k: d.cv.mean() for k, d in porq}

sim_eq = {k: np.zeros(NPERM, int) for k in obs_q}
sim_r1 = {k: np.zeros(NPERM, int) for k in obs_q}
sim_c5 = {k: np.zeros(NPERM, int) for k in obs_q}
sim_c10 = {k: np.zeros(NPERM, int) for k in obs_q}
sim_ties = {k: np.zeros(NPERM, int) for k in obs_q}
sim_cv = {k: np.zeros(NPERM) for k in obs_q}
tam = {k: len(d) for k, d in porq}

for b in range(NPERM):
    for k, pool in pools.items():
        if k not in obs_q:
            continue
        n = tam[k]
        draw = rng.choice(pool, size=(n, 9), replace=len(pool) < 9)
        for i in range(n):
            v = draw[i]
            sim_eq[k][b] += int(len(set(v)) == 1)
            sim_r1[k][b] += int(v.max() - v.min() <= 1)
            cv = v.std() / v.mean()
            sim_c5[k][b] += int(cv <= 0.05)
            sim_c10[k][b] += int(cv <= 0.10)
            sim_ties[k][b] += sum(v[a] == v[z] for a in range(9) for z in range(a + 1, 9))
        sim_cv[k][b] = np.mean([draw[i].std() / draw[i].mean() for i in range(n)])

# p por quipu (una cola, exceso) y Holm
P = []
for k in sorted(obs_q):
    for nombre, sim, obs in [
        ("eq_all", sim_eq[k], obs_q[k]["eq_all"]),
        ("range1", sim_r1[k], obs_q[k]["range1"]),
        ("cv05", sim_c5[k], obs_q[k]["cv05"]),
        ("cv10", sim_c10[k], obs_q[k]["cv10"]),
        ("ties", sim_ties[k], obs_q[k]["ties"]),
    ]:
        p = (1 + np.sum(sim >= obs)) / (NPERM + 1)
        P.append(dict(kfg=k, prueba=nombre, observado=obs, nulo_medio=sim.mean(), p=p))
    p = (1 + np.sum(sim_cv[k] <= obs_cv_q[k])) / (NPERM + 1)
    P.append(dict(kfg=k, prueba="cv_medio", observado=obs_cv_q[k], nulo_medio=sim_cv[k].mean(), p=p))
P = pd.DataFrame(P)
# Holm dentro de cada prueba, sobre los quipus con observado > 0 (los demas no pueden rechazar)
P["p_holm"] = 1.0
for nombre, sub in P.groupby("prueba"):
    idx = sub.index
    pv = sub.p.values
    orden = np.argsort(pv)
    m = len(pv)
    adj = np.empty(m)
    prev = 0.0
    for rank, j in enumerate(orden):
        val = min(1.0, (m - rank) * pv[j])
        prev = max(prev, val)
        adj[j] = prev
    P.loc[idx, "p_holm"] = adj
P.to_csv(AQUI / "pruebas_grupos9.csv", index=False)

print("\nQuipus con algun grupo plano (observado > 0):")
sel = P[(P.observado > 0) & (P.prueba.isin(["eq_all", "range1", "cv05", "ties"]))]
print(sel.sort_values(["prueba", "p"]).head(30).to_string(index=False))

print("\nPruebas globales (suma sobre los 237 grupos):")
glob = []
for nombre, obs_col in [("eq_all", "eq_all"), ("range1", "range1"), ("cv05", "cv05"), ("cv10", "cv10"), ("ties", "ties")]:
    obs = int(D[obs_col].sum())
    # nulo global = suma de los nulos por quipu
    sim = sum(sim_eq[k] if nombre == "eq_all" else sim_r1[k] if nombre == "range1"
              else sim_c5[k] if nombre == "cv05" else sim_c10[k] if nombre == "cv10" else sim_ties[k]
              for k in obs_q)
    p = (1 + np.sum(sim >= obs)) / (NPERM + 1)
    glob.append(dict(prueba=nombre, observado=obs, nulo_medio=sim.mean(), p=p))
G = pd.DataFrame(glob)
print(G.to_string(index=False))
print("\nCV medio global: %.3f" % D.cv.mean())
