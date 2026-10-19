"""Paso 3: ¿las relaciones UR270->UR278 y UR278->UR275->UR266 pasan con P, S1 o P+S1?

A) UR270 -> UR278 (celda a celda, columna a columna). Se replica el diseño de
   analisis/13_sistema_incahuasi/07_ur270_ur278.py para tres candidatos: P, S1 y P+S1.
   Estadístico: nº de grupos de UR270 cuya mejor fila de UR278 acierta >=6 de 9 columnas
   (+/-1) y suma de aciertos. Nulo: permutar el vector candidato dentro de cada grupo.
B) UR278 -> UR275/UR266: se reconstruye el total de cada fila de UR278 a partir de UR270
   con cada candidato y se compara con las cabeceras de UR275 y UR266 (y con el total
   observado de la fila de UR278).
C) UR270 -> UR273A/UR273B: ¿P suma la parte B y S1 la parte A? Alineación g -> fila g+9
   (la documentada en 13). Nulo: permutar las cabeceras.
Salida: salida_03.txt, relaciones.csv
"""
import numpy as np
import pandas as pd
from scipy import stats

import lib_cuota as L
from pathlib import Path
import sys

# reutilizar el lector de registros del equipo 16 (solo lectura de su código)
sys.path.insert(0, str(L.RAIZ / "analisis" / "16_verificacion_incahuasi"))
import lib as L16  # noqa: E402

RNG = np.random.default_rng(L.SEED)
NP = 5000

c, q = L.cargar()
c16 = L16.load()

# ---------------- A) UR270 -> UR278 ----------------
m = L.celdas(c, "UR270")
G = {}
for g, x in m.groupby("grupo"):
    x = x.sort_values("j")
    if len(x) < 7:
        continue
    G[g] = dict(P=np.where(x.presP, x.P, 0).astype(int),
                S1=np.where(x.presS1, x.S1, 0).astype(int))
for g in G:
    G[g]["P+S1"] = G[g]["P"] + G[g]["S1"]

t = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values(["grupo", "orden"])
H = {}
for h, x in t.groupby("grupo"):
    if len(x) >= 7:
        H[h] = np.where((x.nudos != "") | (x.valor > 0), x.valor, 0).astype(int)[:9]


def aciertos(v, w):
    n = min(len(v), len(w))
    ok = (v[:n] > 0) & (w[:n] > 0)
    return int(np.sum(ok & (np.abs(v[:n] - w[:n]) <= 1)))


def best(v):
    sc = [(aciertos(v, w), h) for h, w in H.items()]
    return max(sc)


def estad(cols):
    b = {g: best(v) for g, v in cols.items()}
    return sum(a >= 6 for a, _ in b.values()), sum(a for a, _ in b.values()), b


rel = []
for nombre in ["P", "S1", "P+S1"]:
    cols = {g: G[g][nombre] for g in G}
    o6, osum, b = estad(cols)
    keys = list(cols)
    n6 = np.zeros(NP, dtype=int)
    nsum = np.zeros(NP, dtype=int)
    for r in range(NP):
        perm = {g: RNG.permutation(cols[g]) for g in keys}
        a, s, _ = estad(perm)
        n6[r], nsum[r] = a, s
    rel.append(dict(relacion="UR270->UR278", candidato=nombre, n_grupos=len(cols),
                    grupos_6mas=o6, aciertos_total=osum,
                    p_6mas=(np.sum(n6 >= o6) + 1) / (NP + 1),
                    p_total=(np.sum(nsum >= osum) + 1) / (NP + 1),
                    detalle="; ".join(f"g{g}->g{h}:{a}" for g, (a, h) in b.items())))

# ---------------- B) totales reconstruidos -> cabeceras UR275 / UR266 ----------------
cab275 = [x for x in L16.cabeceras(c16, "UR275") if x == x]
cab266 = [x for x in L16.cabeceras(c16, "UR266") if x == x]
cab = np.array(sorted(set(cab275) | set(cab266)), dtype=float)
tot278 = {h: int(w[:9].sum()) for h, w in H.items()}

filasB = []
for g, (a, h) in estad({g: G[g]["P+S1"] for g in G})[2].items():
    if a < 5:
        continue
    for nombre in ["P", "S1", "P+S1"]:
        tot = int(G[g][nombre][:9].sum())
        mch = int(np.sum(np.abs(cab - tot) <= 1))
        exact = int(np.sum(cab == tot))
        filasB.append(dict(grupo=g, ur278=h, candidato=nombre, total=tot,
                           total_ur278=tot278.get(h), cabeceras_pm1=mch, cabeceras_exactas=exact))
B = pd.DataFrame(filasB)

# ---------------- C) UR270 -> UR273B (P) y UR273A (S1) ----------------
cabB = {int(r["grupo"]): r["cab"] for r in L16.registros(c16, "UR273B")}
cabA = {int(r["grupo"]): r["cab"] for r in L16.registros(c16, "UR273A")}


def alineado(g):
    return g + 9


filasC = []
for g in sorted(G):
    i = alineado(g)
    if i not in cabB or i not in cabA:
        continue
    Psum = int(G[g]["P"].sum())
    Ssum = int(G[g]["S1"].sum())
    filasC.append(dict(grupo=g, fila=i, Psum=Psum, B=cabB[i], dP=(Psum - cabB[i]),
                       Ssum=Ssum, A=cabA[i], dS=(Ssum - cabA[i]),
                       PmasS=Psum + Ssum))
C = pd.DataFrame(filasC)


def cuenta(d, tol=0):
    d = np.asarray(d, float)
    d = d[~np.isnan(d)]
    return int(np.sum(np.abs(d) <= tol))


obsP = cuenta(C.dP, 0)
obsS = cuenta(C.dS, 0)
obsP1 = cuenta(C.dP, 1)
obsS1 = cuenta(C.dS, 1)
# nulo: permutar las cabeceras B (y A) entre filas
Bv = C.B.to_numpy(float)
Av = C.A.to_numpy(float)
nPdist, nSdist = [], []
for _ in range(NP):
    bp = RNG.permutation(Bv)
    ap = RNG.permutation(Av)
    nPdist.append(cuenta(C.Psum.to_numpy() - bp, 0))
    nSdist.append(cuenta(C.Ssum.to_numpy() - ap, 0))
nPdist = np.array(nPdist)
nSdist = np.array(nSdist)
pP = (np.sum(nPdist >= obsP) + 1) / (NP + 1)
pS = (np.sum(nSdist >= obsS) + 1) / (NP + 1)

with open("salida_03.txt", "w", encoding="utf-8") as f:
    f.write("== A) UR270 -> UR278 (mejor fila por grupo; +/-1) ==\n")
    f.write(pd.DataFrame(rel).round(5).to_string(index=False) + "\n\n")
    f.write("== B) totales reconstruidos vs cabeceras UR275/UR266 ==\n")
    f.write(B.round(3).to_string(index=False) + "\n\n")
    f.write(f"cabeceras UR275: {cab275}\ncabeceras UR266: {cab266}\n\n")
    f.write("== C) UR270 -> UR273B (P) / UR273A (S1), alineación g->fila g+9 ==\n")
    f.write(C.round(1).to_string(index=False) + "\n")
    f.write(f"\nP = B exactas: {obsP}/{len(C)} (nulo medio {nPdist.mean():.2f}, p={pP:.4f})\n")
    f.write(f"S1 = A exactas: {obsS}/{len(C)} (nulo medio {nSdist.mean():.2f}, p={pS:.4f})\n")
    f.write(f"P = B +/-1: {obsP1}/{len(C)}; S1 = A +/-1: {obsS1}/{len(C)}\n")

pd.DataFrame(rel).to_csv("relaciones.csv", index=False)
print(pd.DataFrame(rel)[["candidato", "n_grupos", "grupos_6mas", "aciertos_total", "p_6mas", "p_total"]].to_string(index=False))
print(B.to_string(index=False))
print(C.to_string(index=False))
print(f"P=B exactas {obsP}/{len(C)} p={pP:.4f}; S1=A exactas {obsS}/{len(C)} p={pS:.4f}")
