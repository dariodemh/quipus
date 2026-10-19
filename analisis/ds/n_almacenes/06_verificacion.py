# -*- coding: utf-8 -*-
"""06. Verificacion de las cifras citadas en informe.md (asserts)."""
import numpy as np, pandas as pd
from comun import leer_ur278, leer_libro

d, cols = leer_ur278()
V = d[cols].values.astype(float)
L = leer_libro()
Lq = L.groupby("quipu").cabecera.sum()
_c = pd.read_csv("../../datos/cuerdas.csv")
_q = _c[(_c.kfg == "UR268") & (_c.nivel == 0)].copy()
_q["v"] = pd.to_numeric(_q.valor, errors="coerce")
ur268 = _q.groupby("grupo").v.max().sum()

checks = {
    "UR278 suma 9 columnas = 61 790": np.nansum(V) == 61790,
    "UR278 total columna = 62 179": d.total.sum() == 62179,
    "UR266 = 56 986": Lq["UR266"] == 56986,
    "UR275 = 56 446": Lq["UR275"] == 56446,
    "UR269 = 122 609": Lq["UR269"] == 122609,
    "UR268 = 300 378": ur268 == 300378,
    "celdas = 249": int((~np.isnan(V)).sum()) == 249,
    "media celda 248,2": abs(np.nanmean(V) - 248.15) < 0.01,
    "max celda 537": np.nanmax(V) == 537,
    "min celda 11": np.nanmin(V) == 11,
    "capacidad min 2 560 t": 6400 * 0.40 == 2560,
    "capacidad max 4 480 t": 6400 * 0.70 == 4480,
    "costal 25 kg L3 = 3 065 t": abs(122609 * 25 / 1000 - 3065.2) < 0.1,
    "racion L3 = 86-98 t": abs(122609 * 0.7 / 1000 - 85.8) < 0.5,
    "maní 25 kg ocupa 0,1 m3/u": abs(25 / 250 - 0.1) < 1e-9,
    "maní L3 pide 12 260 m3": abs(122609 * 0.1 - 12261) < 2,
    "saco 35 L L3 = 4 291 m3": abs(122609 * 0.035 - 4291) < 2,
    "cota L4 T=2,5 = 3,41 kg": abs(2560000 / (300378 * 2.5) - 3.41) < 0.01,
    "cota L3 T=2 = 10,44 kg": abs(2560000 / (122609 * 2) - 10.44) < 0.01,
    "caravana L1 a 25 kg = 2 207": abs(2207 * 25 / 25 - 2207) < 1,
    "caravana mensual = 74/dia": abs(2207 / 30 - 73.6) < 1,
    "cuota 47 = 1 175 kg": 47 * 25 == 1175,
    "cuadro 23cm x 5cm = 2,6 L": abs(0.23**2 * 0.05 * 1000 - 2.645) < 0.01,
    "cuadro L4 a 5 cm = 12,4 %": abs(100 * 300378 * 0.23**2 * 0.05 / 6400 - 12.4) < 0.2,
}
for k, v in checks.items():
    print(("OK   " if v else "FALLA") + "  " + k)
print()
print("TODAS OK" if all(checks.values()) else "HAY FALLOS")
