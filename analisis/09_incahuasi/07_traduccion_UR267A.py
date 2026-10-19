"""Tarea 5: lectura registro a registro de UR267A (29 grupos) con estado de cierre y contraparte en UR255. Salida: traduccion_UR267A.csv"""
import numpy as np, pandas as pd
from comun import *
c, q = cargar()
a = c[(c.kfg == "UR267A")].sort_values("orden"); b = c[(c.kfg == "UR255") & (c.nivel == 0) & c.pres & (c.valor > 0)]
Bx = {}  # x en UR255 -> lista de grupos
for g, gg in b.groupby("grupo"): Bx[g] = gg.valor.tolist()
rows = []
for g, gg in a.groupby("grupo", sort=False):
    l0 = gg[(gg.nivel == 0)]; pres = l0[l0.pres & (l0.valor > 0)]; v = pres.valor.tolist(); col = pres.color.tolist()
    subs = gg[(gg.nivel > 0) & gg.pres & (gg.valor > 0)].valor.tolist(); ausentes = int((~l0.pres | (l0.valor == 0)).sum())
    if not v: est = "separador (solo cuerda ausente PK)"; x = cc = n = None
    else:
        x = v[0]; cc = 15 if 15 in v[1:] else (v[1] if len(v) > 1 else None); resto = [w for w in v[1:] if w != cc]
        n = resto[0] if resto else None
        if n is not None and abs(x-cc-n) == 0: est = "cierra exacto"
        elif n is not None: est = f"no cierra (x-c-n={x-cc-n})"
        else: est = "sin cuerda neta (cuerda de resultado ausente o rota)"
    pa = [gk for gk, vv in Bx.items() if x is not None and x in vv]
    rows.append(dict(grupo=g, valores=v, colores=col, subsidiarias=subs, cuerdas_ausentes=ausentes, estado=est, en_UR255_grupo=pa))
T = pd.DataFrame(rows); T.to_csv(OUT/"traduccion_UR267A.csv", index=False); pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70); print(T.to_string())
print(T.estado.str.split(" \(").str[0].value_counts())
