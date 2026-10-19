# -*- coding: utf-8 -*-
"""Rol estructural de los valores: posicion de etiqueta (primera cuerda del grupo),
papel aritmetico (madre que suma hijas, cuerda superior) y repeticion por grupo.
Nulos: permutacion DENTRO de cada quipu (conserva valores y estructura del quipu).
"""
import pandas as pd, numpy as np, os
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261018)
NPERM = 1000

c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)
qids = sorted(k.kfg.unique()); qidx = {q: i for i, q in enumerate(qids)}
k["qi"] = k.kfg.map(qidx)

# --- primera cuerda de cada grupo (solo colgantes nivel 0) ---
k0 = k[k.nivel == 0].copy()
prim = k0.groupby(["kfg", "grupo"]).orden.transform("min")
k0["primero"] = k0.orden == prim
print("grupos:", k0.groupby(['kfg', 'grupo']).ngroups, "| primeras cuerdas:", int(k0.primero.sum()),
      "| colgantes nivel0:", len(k0))

# --- papel aritmetico ---
hijos = k.groupby(["kfg", "padre"]).valor.sum().rename("suma_hijos")
hijos_n = k.groupby(["kfg", "padre"]).size().rename("n_hijos")
k = k.merge(hijos, left_on=["kfg", "cuerda"], right_index=True, how="left")
k = k.merge(hijos_n, left_on=["kfg", "cuerda"], right_index=True, how="left")
k["es_madre"] = k.n_hijos.notna()
k["suma_ok"] = k.es_madre & (k.valor == k.suma_hijos.fillna(-1))
k["es_superior"] = k.union == "T"
print("madres:", int(k.es_madre.sum()), "| madres que suman exacto:", int(k.suma_ok.sum()),
      "| cuerdas superiores:", int(k.es_superior.sum()))

f = pd.Series(k.valor.values).value_counts()
cand = [1, 2, 3, 4, 5, 10, 11, 12, 15, 20, 22, 30, 33, 40, 47, 50, 100, 110, 200]

# ================= A) posicion de etiqueta =================
vals0 = k0.valor.values; qi0 = k0.qi.values; prim0 = k0.primero.values
nq = len(qids)
obs_prim = {v: int(((vals0 == v) & prim0).sum()) for v in cand}
obs_tot0 = {v: int((vals0 == v).sum()) for v in cand}

# permutacion dentro de quipu: barajar etiqueta 'primero' entre colgantes del quipu
perm_prim = {v: [] for v in cand}
idx_by_q = [np.where(qi0 == i)[0] for i in range(nq)]
for it in range(NPERM):
    p = prim0.copy()
    for idx in idx_by_q:
        if len(idx) > 1:
            p[idx] = rng.permutation(prim0[idx])
    for v in cand:
        perm_prim[v].append(int(((vals0 == v) & p).sum()))

rows = []
for v in cand:
    o = obs_prim[v]; P = np.array(perm_prim[v])
    n = obs_tot0[v]
    rows.append({"valor": v, "n_nivel0": n, "primero_obs": o,
                 "primero_esp": round(P.mean(), 2), "ratio_primero": o / P.mean() if P.mean() > 0 else np.nan,
                 "p_primero": (1 + (P >= o).sum()) / (1 + NPERM)})

# ================= B) papel aritmetico =================
arq = {}
for v in cand:
    s = k[k.valor == v]
    arq[v] = {"pct_madre": round(100 * s.es_madre.mean(), 1),
              "pct_suma_ok": round(100 * s.suma_ok.mean(), 1),
              "pct_superior": round(100 * s.es_superior.mean(), 1),
              "pct_nivel0": round(100 * (s.nivel == 0).mean(), 1)}

T = pd.DataFrame(rows)
T = T.merge(pd.DataFrame(arq).T.rename_axis("valor").reset_index(), on="valor", how="left")
for col in ["pct_madre", "pct_suma_ok", "pct_superior", "pct_nivel0"]:
    T[col] = pd.to_numeric(T[col])


def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); q = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, p[o[i]] * m / (i + 1)); q[o[i]] = prev
    return q
T["q_primero"] = bh(T.p_primero.values)
T.to_csv(OUT + r"\tabla_codigos.csv", index=False)

pd.set_option("display.width", 260)
print("\n=== A) valores en la PRIMERA cuerda de su grupo (posicion de etiqueta) ===")
print(T.sort_values("ratio_primero", ascending=False)
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))

# ================= C) repeticion dentro del grupo =================
# para cada (quipu,grupo): cuantas veces aparece cada valor; se compara con n del grupo
g = k.groupby(["kfg", "grupo", "valor"]).size().rename("rep").reset_index()
gtot = k.groupby(["kfg", "grupo"]).size().rename("n_grupo").reset_index()
g = g.merge(gtot, on=["kfg", "grupo"])
print("\n=== C) repeticion del mismo valor dentro del mismo grupo (n_grupo>=3) ===")
for v in [1, 2, 10, 15, 20, 100, 200]:
    gg = g[(g.valor == v) & (g.n_grupo >= 3)]
    if len(gg):
        print(f"v={v:>4}: grupos={len(gg):>4}  rep media={gg.rep.mean():.2f}  "
              f"grupos con rep>=2: {(gg.rep>=2).sum():>3} ({(gg.rep>=2).mean()*100:.0f}%)")

# ================= D) papel de 1: marcador vs cantidad =================
print("\n=== D) estructura de las cuerdas con valor 1 ===")
s1 = k[k.valor == 1]
print("nivel:", s1.nivel.value_counts().head(4).to_dict())
print("madre:", round(100 * s1.es_madre.mean(), 1), "% | suma_ok:", round(100 * s1.suma_ok.mean(), 1),
      "% | superior:", round(100 * s1.es_superior.mean(), 1), "%")
print("quipus con >=5 cuerdas de valor 1:", int((s1.groupby('kfg').size() >= 5).sum()))

# ================= E) control: sin cuerdas superiores =================
print("\n=== E) control sin cuerdas superiores (union=T) ===")
kk = k[~k.es_superior]
print("cuerdas:", len(kk), "| valores distintos:", kk.valor.nunique())
top = pd.Series(kk.valor.values).value_counts().head(8)
print("top:", top.to_dict())
