# -*- coding: utf-8 -*-
"""
02d_novenos.py -- prueba exploratoria de las fracciones wanka 2/9, 3/9, 4/9.

Chirinos (2010, citado en la ficha 2013-Curatola) documenta para Hatun Xauxa
fracciones de 2/9, 3/9 y 4/9. Si las 9 columnas de UR278 fueran 9 unidades
iguales y se agruparan en 2+3+4 (en el orden fisico), las cuotas de los tres
grupos deberian ser 2/9, 3/9 y 4/9. Se contrasta con bootstrap de filas.

Salida: salida_02d.txt
"""
import numpy as np
import pandas as pd

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)
OUT = "analisis/ds/n_saya_proporcional"

d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[[f"c{i}" for i in range(1, 10)]].to_numpy(float)
N = d["N"].to_numpy(float)
P = X / N[:, None]
n = len(d)

grupos = {"c1-c2": [0, 1], "c3-c5": [2, 3, 4], "c6-c9": [5, 6, 7, 8]}
G = np.column_stack([P[:, idx].sum(1) for idx in grupos.values()])
obs = G.mean(0)
null = np.array([2, 3, 4]) / 9

B = 20000
bs = np.array([G[rng.integers(0, n, n)].mean(0) for _ in range(B)])
mu = bs.mean(0)
S = np.cov(bs.T)
d0 = obs - null
T = float(d0 @ np.linalg.inv(S) @ d0)
Ts = np.array([(bs[i] - mu) @ np.linalg.inv(S) @ (bs[i] - mu) for i in range(B)])
p_joint = (1 + np.sum(Ts >= T)) / (B + 1)

filas = []
for i, (nombre, idx) in enumerate(grupos.items()):
    p_un = 2 * min((bs[:, i] <= null[i]).mean(), (bs[:, i] >= null[i]).mean())
    filas.append({"grupo": nombre, "columnas": len(idx),
                  "cuota_obs": obs[i], "cuota_nula": null[i],
                  "dif": obs[i] - null[i],
                  "IC95_inf": np.quantile(bs[:, i], 0.025),
                  "IC95_sup": np.quantile(bs[:, i], 0.975),
                  "p_univ": min(1.0, p_un)})
tab = pd.DataFrame(filas)

L = []
L.append("=== Fracciones 2/9, 3/9, 4/9 (agrupacion contigua 2+3+4) ===")
L.append("Si las 9 columnas son 9 unidades iguales, las cuotas de los grupos deberian ser 0,222 / 0,333 / 0,444.")
L.append(tab.to_string(index=False, float_format=lambda z: f"{z:.4f}"))
L.append(f"Contraste conjunto (Mahalanobis, bootstrap de filas): T = {T:.2f}; p = {p_joint:.5f}")
L.append("Lectura: la agrupacion 2+3+4 NO reproduce los novenos documentados; el grupo c1-c2 es ~27 % mayor de lo previsto.")
L.append("Supuesto fuerte: las 9 columnas son unidades iguales y el orden fisico refleja el orden de los grupos. Si las columnas tienen poblaciones desiguales, el test no aplica.")

txt = "\n".join(L)
open(f"{OUT}/salida_02d.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
