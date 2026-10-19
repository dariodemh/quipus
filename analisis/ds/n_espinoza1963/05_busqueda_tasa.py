# -*- coding: utf-8 -*-
"""Busca en el corpus KFG un quipu con la forma de la tasa de Guancayo:
9 productos x 9 pachacas.

Formas previstas:
  A) grupos de 9 colgantes constantes (una pachaca, 9 productos iguales)
  B) un grupo de 9 con los totales x9 [45,234,18,27,36,180,90,27,9]
  C) cualquier ventana de 9 valores proporcional al vector de 9 productos.

Salida: busqueda_tasa.csv, busqueda_tasa_ventanas.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path
from numpy.lib.stride_tricks import sliding_window_view

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SEED = 20261018
NPERM = 1000
rng = np.random.default_rng(SEED)

T = np.array([5, 26, 2, 3, 4, 20, 10, 3, 1], float)
T9 = T * 9
c = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
c["pres"] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != "") & c.valor.notna()
c0 = c[(c.nivel == 0) & c.pres].copy()
c0["valor"] = c0.valor.astype(float)
c0 = c0[c0.valor > 0].sort_values(["kfg", "orden"])

# --- A/B: grupos de exactamente 9 colgantes ---
grupos = []
for (k, g), x in c0.groupby(["kfg", "grupo"]):
    v = x.sort_values("orden").valor.values.astype(float)
    if len(v) == 9:
        grupos.append((k, int(g), v))
print("grupos de 9:", len(grupos))

res = []
for k, g, v in grupos:
    if len(set(v)) == 1:
        res.append(dict(kfg=k, grupo=g, forma="constante", valor=int(v[0]),
                        en_productos=int(v[0] in T), en_totales_x9=int(v[0] in T9),
                        vector=" ".join(map(str, v.astype(int)))))
    if sorted(v.astype(int)) == sorted(T.astype(int)):
        res.append(dict(kfg=k, grupo=g, forma="multiset_productos", valor=0, en_productos=1,
                        en_totales_x9=0, vector=" ".join(map(str, v.astype(int)))))
    if sorted(v.astype(int)) == sorted(T9.astype(int)):
        res.append(dict(kfg=k, grupo=g, forma="multiset_totales_x9", valor=0, en_productos=0,
                        en_totales_x9=1, vector=" ".join(map(str, v.astype(int)))))
R = pd.DataFrame(res)
R.to_csv(AQUI / "busqueda_tasa.csv", index=False)
print("\nGrupos de 9 constantes:")
print(R[R.forma == "constante"].to_string(index=False))
print("Coincidencias exactas con las listas de la Visita:",
      len(R[R.forma.isin(["multiset_productos", "multiset_totales_x9"])]))

# --- C: ventanas de 9 colgantes consecutivos dentro de cada quipu ---
vals = c0.valor.values.astype(float)
kfg = c0.kfg.values
# bloques por quipu
cambios = np.r_[0, np.where(kfg[1:] != kfg[:-1])[0] + 1, len(vals)]
bloques = [(a, b) for a, b in zip(cambios[:-1], cambios[1:])]
starts = np.concatenate([np.arange(a, b - 8) for a, b in bloques if b - a >= 9])
print("ventanas de 9 dentro de un mismo quipu:", len(starts))

W = sliding_window_view(vals, 9)[starts]
V = pd.DataFrame(dict(kfg=kfg[starts], pos=starts,
                      escala=np.nan, error_rel=np.nan,
                      vector=[" ".join(map(str, w.astype(int))) for w in W]))


def errores(M, obj):
    esc = (M @ obj) / (obj @ obj)
    num = np.linalg.norm(M - esc[:, None] * obj[None, :], axis=1)
    den = np.maximum(1e-9, np.linalg.norm(M, axis=1))
    return esc, num / den


esc, err = errores(W, T)
V["escala"] = np.round(esc, 3)
V["error_rel"] = err
V = V.sort_values("error_rel")
V.to_csv(AQUI / "busqueda_tasa_ventanas.csv", index=False)
print("\nVentanas de 9 mas parecidas al vector de productos (error relativo L2):")
print(V.head(12).to_string(index=False))

esc9, err9 = errores(W, T9)
obs_min = err
obs_min9 = err9
# escala 9: solo interesan las que tengan escala global ~9
print("\nVentanas mas parecidas a los totales x9 (mejor escala global):")
print(pd.DataFrame(dict(kfg=kfg[starts], pos=starts, escala=np.round(esc9, 2), error_rel=err9,
                        vector=[" ".join(map(str, w.astype(int))) for w in W]))
      .sort_values("error_rel").head(6).to_string(index=False))

# --- nulo: barajar valores dentro de cada quipu, mismas ventanas ---
def barajar():
    key = rng.random(len(vals))
    for a, b in bloques:
        key[a:b] += np.arange(1)  # nada: el offset por bloque se hace abajo
    # offset grande por bloque para que argsort no mezcle bloques
    off = np.zeros(len(vals))
    for j, (a, b) in enumerate(bloques):
        off[a:b] = j * 10.0
    return vals[np.argsort(key + off)]


nul = np.empty(NPERM)
nul9 = np.empty(NPERM)
for b in range(NPERM):
    Wp = sliding_window_view(barajar(), 9)[starts]
    nul[b] = errores(Wp, T)[1].min()
    nul9[b] = errores(Wp, T9)[1].min()
print("\nMinimo error relativo observado vs nulo (barajar dentro de cada quipu):")
print("  productos : obs %.4f; nulo medio %.4f (min %.4f); p = %.4f" %
      (obs_min.min(), nul.mean(), nul.min(), (1 + np.sum(nul <= obs_min.min())) / (NPERM + 1)))
print("  totales_x9: obs %.4f; nulo medio %.4f (min %.4f); p = %.4f" %
      (obs_min9.min(), nul9.mean(), nul9.min(), (1 + np.sum(nul9 <= obs_min9.min())) / (NPERM + 1)))

# --- quipus con 9 grupos de 9, grupos constantes, vectores repetidos ---
porq = {}
for k, g, v in grupos:
    porq.setdefault(k, []).append((g, v))
print("\nQuipus con >=9 grupos de 9:")
for k, L in sorted(porq.items(), key=lambda z: -len(z[1])):
    if len(L) >= 9:
        const = sum(len(set(v)) == 1 for g, v in L)
        print(f"  {k}: {len(L)} grupos, {const} constantes")
print("\nGrupos de 9 con el mismo vector (repetido en el mismo quipu):")
for k, L in porq.items():
    seen = {}
    for g, v in L:
        t = tuple(v.astype(int))
        if t in seen:
            print(f"  {k}: g{seen[t]} = g{g} = {t}")
        seen[t] = g
