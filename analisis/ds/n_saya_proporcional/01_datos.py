# -*- coding: utf-8 -*-
"""
01_datos.py -- construye las tablas de trabajo para las dos pruebas.

A) UR278: 24 filas completas de 9 columnas (las 4 filas con 7, 8, 10 y 12
   columnas se excluyen del modelo principal; se usan solo como control).
   Reconstruye tambien UR270 (detalle) como replicacion: grupos de 9 colgantes
   de nivel 0, cada uno sumado con su primera subsidiaria (parte A + parte B).
B) Constantes de capacidad de Inkawasi (LeVine 1992 / Hyslop 1985 / Snead).

Salidas: datos_ur278.csv, datos_ur270.csv, resumen_datos.txt
"""
import json
import numpy as np
import pandas as pd

SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)

RAIZ = "."
TAB = f"{RAIZ}/analisis/13_sistema_incahuasi/ur278_tabla.csv"
CUERDAS = f"{RAIZ}/analisis/datos/cuerdas.csv"
OUT = f"{RAIZ}/analisis/ds/n_saya_proporcional"

COLS = [f"c{i}" for i in range(1, 10)]

# ---------------------------------------------------------------- A. UR278
df = pd.read_csv(TAB)
completas = df[(df["n"] == 9) & df[COLS].notna().all(axis=1)].copy()
completas = completas.sort_values("grupo").reset_index(drop=True)
X = completas[COLS].to_numpy(float)
N = X.sum(axis=1)
P = X / N[:, None]

out = pd.DataFrame({"fila": np.arange(1, len(completas) + 1),
                    "grupo": completas["grupo"].astype(int).values,
                    "N": N})
for j, c in enumerate(COLS):
    out[c] = X[:, j]
    out["p" + c[1:]] = P[:, j]
out.to_csv(f"{OUT}/datos_ur278.csv", index=False)

# filas incompletas: solo descriptivo
incompletas = df[~df.index.isin(completas.index)]
# cuidado: el indice de completas es el original; recalculo por posicion
mask = (df["n"] == 9) & df[COLS].notna().all(axis=1)
incompletas = df[~mask].copy()

# ---------------------------------------------------------------- UR270
cu = pd.read_csv(CUERDAS)
u = cu[cu["kfg"] == "UR270"].copy()
p0 = u[u["nivel"] == 0].sort_values("orden")
s1 = u[u["nivel"] == 1]
filas270 = []
for g, grp in p0.groupby("grupo"):
    grp = grp.sort_values("orden")
    if len(grp) != 9:
        continue
    vals, nudos_vacios = [], 0
    for _, r in grp.iterrows():
        sub = s1[s1["padre"] == r["cuerda"]]
        v = r["valor"] + (sub["valor"].sum() if len(sub) else np.nan)
        # 0 con nudos vacio = ausente
        if (r["valor"] == 0) and (pd.isna(r["nudos"]) or str(r["nudos"]).strip() == ""):
            v = np.nan
            nudos_vacios += 1
        vals.append(v)
    if np.isnan(vals).any():
        continue
    filas270.append([int(g)] + vals)

ur270 = pd.DataFrame(filas270, columns=["grupo"] + COLS)
if len(ur270):
    X270 = ur270[COLS].to_numpy(float)
    N270 = X270.sum(axis=1)
    P270 = X270 / N270[:, None]
    ur270.insert(1, "N", N270)
    for j, c in enumerate(COLS):
        ur270["p" + c[1:]] = P270[:, j]
    ur270.to_csv(f"{OUT}/datos_ur270.csv", index=False)

# ---------------------------------------------------------------- resumen
lineas = []
lineas.append("=== UR278 ===")
lineas.append(f"filas en la tabla: {len(df)}; completas (9 col, sin huecos): {len(completas)}")
lineas.append(f"unidades en filas completas: {int(N.sum())}")
lineas.append(f"unidades en toda la tabla (suma de c1..c9): {int(df[COLS].sum().sum())}")
lineas.append(f"suma de la columna total (incluye cuerdas 10/12): {int(df['total'].sum())}")
lineas.append(f"rango de totales de fila: {int(N.min())}-{int(N.max())}")
lineas.append(f"medias de columna: {np.round(P.mean(0), 4).tolist()}")
lineas.append(f"CV entre medias de columna: {P.mean(0).std(ddof=1)/P.mean(0).mean():.4f}")
lineas.append(f"CV intra-columna: {np.round(P.std(0, ddof=1)/P.mean(0), 4).tolist()}")
esp = np.sqrt(P.mean(0) * (1 - P.mean(0)) / N.mean()) / P.mean(0)
lineas.append(f"CV multinomial esperado: {np.round(esp, 4).tolist()}")
lineas.append(f"razon CV obs/esp: {np.round((P.std(0, ddof=1)/P.mean(0))/esp, 3).tolist()}")
lineas.append(f"filas incompletas excluidas: grupos {incompletas['grupo'].astype(int).tolist()}")
lineas.append("")
lineas.append("=== UR270 (replicacion) ===")
lineas.append(f"grupos de 9 colgantes completos: {len(ur270)}")
if len(ur270):
    lineas.append(f"unidades: {int(ur270['N'].sum())}; rango {int(ur270['N'].min())}-{int(ur270['N'].max())}")
    lineas.append(f"CV intra-columna: {np.round(ur270[[f'p{i}' for i in range(1,10)]].std(ddof=1).values/ur270[[f'p{i}' for i in range(1,10)]].mean().values, 4).tolist()}")

txt = "\n".join(lineas)
open(f"{OUT}/resumen_datos.txt", "w", encoding="utf-8").write(txt + "\n")
print(txt)
