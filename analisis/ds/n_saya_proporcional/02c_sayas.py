# -*- coding: utf-8 -*-
"""
02c_sayas.py -- ?hay dos sayas? La regla wanka predice proporcionalidad entre
dos grupos, no necesariamente entre las 9 columnas.

Para cada biparticion de las 9 columnas se calcula la sobredispersion (rho) de
la cuota del grupo. Si las dos sayas entregaran en proporcion fija a su
poblacion, la cuota del grupo correcto tendria rho ~ 0 aunque las columnas
individuales varien. Se compara el minimo observado sobre las 126 biparticiones
con el nulo de M2 (que no tiene estructura de grupo) y con M1.

Salidas: sayas_ur278.csv, salida_02c.txt
"""
import json
import itertools
import numpy as np
import pandas as pd

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)
OUT = "analisis/ds/n_saya_proporcional"
COLS = [f"c{i}" for i in range(1, 10)]

d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[COLS].to_numpy(float)
N = d["N"].to_numpy(float)
n, k = X.shape
res02 = json.load(open(f"{OUT}/resultados_02.json", encoding="utf-8"))
p2 = np.array(res02["p2"])
alpha2 = res02["alpha2"]
p1 = np.array(res02["p1"])

# biparticiones: subconjuntos de tamano 4 (el complemento de 5 es la misma)
subsets = [np.array(s) for s in itertools.combinations(range(k), 4)]
M = np.zeros((k, len(subsets)))
for i, s in enumerate(subsets):
    M[s, i] = 1.0

A = np.column_stack([np.ones(n), 1.0 / N])
Ainv = np.linalg.pinv(A.T @ A) @ A.T


def rho_mom(Xm):
    """rho por metodo de momentos para cada columna de M (biparticiones)."""
    Y = Xm @ M                      # n x nsub
    Q = Y / N[:, None]
    ps = Y.sum(0) / N.sum()
    D = (Q - ps) ** 2
    coef = Ainv @ D                 # 2 x nsub
    b0, b1 = coef[0], coef[1]
    rho = b0 / (b0 + b1)
    return rho, ps


rho_obs, ps_obs = rho_mom(X)
i_best = int(np.argmin(rho_obs))
best = subsets[i_best]
comp = np.array([j for j in range(k) if j not in best])
rho_best = float(rho_obs[i_best])
share_best = float(ps_obs[i_best])

# particiones contiguas (orden fisico)
cont = []
for a in range(1, k):
    S = np.arange(a)
    Y = X[:, S].sum(1)
    Q = Y / N
    p = Y.sum() / N.sum()
    D = (Q - p) ** 2
    coef = Ainv @ D
    r = coef[0] / (coef[0] + coef[1])
    cont.append({"corte": a, "grupo_A": f"c1-c{a}", "grupo_B": f"c{a+1}-c9",
                 "cuota_A": p, "rho": float(r)})
cont = pd.DataFrame(cont)

# nulos por simulacion (minimo sobre las 126 y rho de cada particion contigua)
B = 1000
subs_cont = [np.arange(a) for a in range(1, k)]
Mc = np.zeros((k, len(subs_cont)))
for i, s in enumerate(subs_cont):
    Mc[s, i] = 1.0


def rho_mom_mat(Xm, Mm):
    Y = Xm @ Mm
    Q = Y / N[:, None]
    ps = Y.sum(0) / N.sum()
    D = (Q - ps) ** 2
    coef = Ainv @ D
    return coef[0] / (coef[0] + coef[1])


def sims_rho(modelo):
    mins = np.empty(B)
    conts = np.empty((B, len(subs_cont)))
    for b in range(B):
        if modelo == "M1":
            Xs = rng.multinomial(N.astype(int), p1)
        else:
            pi = rng.dirichlet(alpha2 * p2, size=n)
            Xs = np.array([rng.multinomial(int(N[i]), pi[i]) for i in range(n)])
        mins[b] = rho_mom(Xs)[0].min()
        conts[b] = rho_mom_mat(Xs, Mc)
    return mins, conts


sim_M1, cont_M1 = sims_rho("M1")
sim_M2, cont_M2 = sims_rho("M2")
p_M1 = (1 + np.sum(sim_M1 <= rho_best)) / (B + 1)
p_M2 = (1 + np.sum(sim_M2 <= rho_best)) / (B + 1)

# p por particion contigua (cola inferior), BH sobre 8
cont["p_M2"] = [(1 + np.sum(cont_M2[:, i] <= cont.rho.iloc[i])) / (B + 1)
                for i in range(len(cont))]
cont["p_M1"] = [(1 + np.sum(cont_M1[:, i] <= cont.rho.iloc[i])) / (B + 1)
                for i in range(len(cont))]


def bh(p):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    q = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        i = o[rank]
        val = min(prev, p[i] * m / (rank + 1))
        q[i] = val
        prev = val
    return q


cont["q_M2_BH"] = bh(cont.p_M2.values)

# cuota del mejor grupo frente a la media
detalle = pd.DataFrame({"columna": COLS,
                        "en_grupo_A": [j in best for j in range(k)],
                        "media_p": X.mean(0) / N.mean()})
detalle.to_csv(f"{OUT}/sayas_detalle.csv", index=False)

tab = pd.DataFrame({"subset": [",".join(COLS[j] for j in s) for s in subsets],
                    "rho": rho_obs, "cuota": ps_obs})
tab = tab.sort_values("rho").head(15)
tab.to_csv(f"{OUT}/sayas_ur278.csv", index=False)
cont.to_csv(f"{OUT}/sayas_contiguas.csv", index=False)

L = []
L.append("=== Biparticiones de las 9 columnas: ?hay un grupo con cuota fija? ===")
L.append(f"Mejor biparticion (menor rho): A = {', '.join(COLS[j] for j in best)} | B = {', '.join(COLS[j] for j in comp)}")
L.append(f"rho del grupo A = {rho_best:.5f}; cuota media = {share_best:.3f}")
L.append(f"15 biparticiones mas estables:")
L.append(tab.to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== Particiones contiguas (orden fisico) ===")
L.append(cont.to_string(index=False, float_format=lambda z: f"{z:.4g}"))
L.append("")
L.append("=== Nulo del minimo sobre las 126 biparticiones ===")
L.append(f"M1: media {sim_M1.mean():.5f}, p05 {np.quantile(sim_M1,.05):.5f}, min {sim_M1.min():.5f}")
L.append(f"M2: media {sim_M2.mean():.5f}, p05 {np.quantile(sim_M2,.05):.5f}, min {sim_M2.min():.5f}")
L.append(f"Observado: {rho_best:.5f}")
L.append(f"p (cola inferior) frente a M1 = {p_M1:.4f}; frente a M2 = {p_M2:.4f}")

txt = "\n".join(L)
open(f"{OUT}/salida_02c.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
