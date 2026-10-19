"""01: jerarquia de Puruchuco (Urton & Brezine 2005) con las reglas (a)-(d).

Estructura contrastada (Urton 2017, cap. 5):
  nivel I   UR063 (y UR073, roto)  -> 6 secciones de grupos de 4 cuerdas
  nivel II  UR068 y UR064 (copias) -> 3 secciones de 20 cuerdas + intro
  nivel III UR067 y UR066 (copias) -> 20 cuerdas de datos + intro

Pruebas:
  P1  UR068 -> UR067 : suma columna a columna de las 3 secciones (20 columnas).
  P2  UR063 -> UR068 : las 6 secciones, alineadas por el final, suman la seccion
      central de UR068 (20 columnas).
  P3  UR064 ~ UR068 : copia del mismo nivel (LCS de valores).
  P4  nulos: permutar cuerdas de UR067 / permutar los grupos de 4 dentro de
      cada seccion (rompe solo la alineacion).
"""
import itertools
import json
import numpy as np
import pandas as pd
import comun_np as L

rng = np.random.default_rng(L.SEED + 1)
c, q = L.cargar_kfg()
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def vals(k):
    d = c[c.kfg == k].sort_values("orden")
    return [int(v) for v in d.valor]


def colores(k):
    d = c[c.kfg == k].sort_values("orden")
    return list(d.col3)


V68, V67, V66, V64, V63, V73 = (vals(k) for k in
                                ["UR068", "UR067", "UR066", "UR064", "UR063", "UR073"])

# ---------------------------------------------------------------- P1
# secciones de UR068 por el ritmo de color W,AB,GG,W:KB (verificado en 00):
# intro 1-13 (13 cuerdas), luego 3 bloques de 20: 14-33, 34-53, 54-73.
SEC68 = [V68[13:33], V68[33:53], V68[53:73]]
assert all(len(s) == 20 for s in SEC68), [len(s) for s in SEC68]
sumas68 = [sum(x) for x in zip(*SEC68)]           # 20 columnas
pr("P1. Sumas de las 3 secciones de UR068 (20 columnas):")
pr("   ", sumas68)

# cuerdas de datos de UR067: 12 de intro; se excluye la cuerda 30 (valor 1),
# que es la "broken string" que el propio Urton aparta.
d67 = V67[12:33]                                   # cuerdas 13-33 (21 valores)
d67_sin = d67[:17] + d67[18:]                      # quita la cuerda 30 -> 20 columnas
pr("UR067 datos (13-32):", d67)
pr("UR067 sin la cuerda 30 (rota):", d67_sin)


def matches(a, b, tol=False):
    return sum(L.coincide(x, y, tol) for x, y in zip(a, b))


obs_ex = matches(sumas68, d67_sin)
obs_tol = matches(sumas68, d67_sin, tol=True)
pr(f"P1 observado: {obs_ex}/20 exactas, {obs_tol}/20 con tolerancia +-1 digito")
for i, (s, v) in enumerate(zip(sumas68, d67_sin)):
    if s != v:
        pr(f"    col {i+1}: suma={s} UR067={v} dif={v-s}")

# nulo 1: permutar las 20 cuerdas de datos de UR067
nulo1 = np.array([matches(sumas68, rng.permutation(d67_sin)) for _ in range(5000)])
p1 = L.p_emp(obs_ex, nulo1)
pr(f"   nulo (permutar cuerdas UR067, 5000 rep): media={nulo1.mean():.2f} max={nulo1.max()} p={p1:.5f}")

# nulo 2: permutar los 5 grupos de 4 dentro de cada seccion de UR068
quads = [[s[j:j + 4] for j in range(0, 20, 4)] for s in SEC68]
nulo2 = []
for _ in range(2000):
    ss = []
    for qq in quads:
        orden = rng.permutation(5)
        ss.append([x for j in orden for x in qq[j]])
    sumas = [sum(x) for x in zip(*ss)]
    nulo2.append(matches(sumas, d67_sin))
nulo2 = np.array(nulo2)
p2 = L.p_emp(obs_ex, nulo2)
pr(f"   nulo (permutar grupos de 4 por seccion, 2000 rep): media={nulo2.mean():.2f} max={nulo2.max()} p={p2:.5f}")

# ---------------------------------------------------------------- P2
# Seis secciones de UR063: los grupos KFG 0 | 1+2+3 | 4 | 5 | 6 | 7.
# (tamanos 20,21,15,20,20,15 = 111; el corte 1/21/42/57/77/97 reproduce los
#  seis bloques de color del quipu).
cortes = [0, 20, 41, 56, 76, 96, 111]
SEC63 = [V63[a:b] for a, b in zip(cortes[:-1], cortes[1:])]
pr("\nP2. Secciones de UR063 (tamanos):", [len(s) for s in SEC63])
C63 = [colores("UR063")[a:b] for a, b in zip(cortes[:-1], cortes[1:])]

# Cada seccion se parte en "grupos de 4" que empiezan en una cuerda blanca (W)
# que sigue a GG o W:KB. Es la seriacion de color que describe Urton.
def quads_de(cols, vals):
    """Indices (i,j) de los grupos de 4: empiezan en cada W que no es mixta.
    Se descarta un grupo final de menos de 4 cuerdas y suma 0 (resto de color)."""
    idx = [i for i, col in enumerate(cols) if col.startswith("W") and ":" not in col]
    out = []
    for j, i in enumerate(idx):
        fin = idx[j + 1] if j + 1 < len(idx) else len(cols)
        out.append((i, fin))
    if out and out[-1][1] - out[-1][0] < 4 and sum(vals[out[-1][0]:out[-1][1]]) == 0:
        out.pop()
    return out


Q63 = [quads_de(cc, s) for cc, s in zip(C63, SEC63)]
pr("   grupos de 4 por seccion:", [len(x) for x in Q63])


def vec_por_color(qq):
    """Suma las cuerdas del grupo por su posicion de color: W, AB/MB, GG, W:KB."""
    v = [0, 0, 0, 0]
    for val, col in qq:
        if ":" in col:
            k = 3
        elif col.startswith("W"):
            k = 0
        elif "AB" in col or "MB" in col or "KB" in col:
            k = 1
        elif "GG" in col:
            k = 2
        else:
            k = 3
        v[k] += val
    return v


Q63v = [[vec_por_color(list(zip(s[i:j], cc[i:j]))) for (i, j) in qq]
        for qq, s, cc in zip(Q63, SEC63, C63)]

# alineacion por el final: los ultimos 5 grupos de cada seccion ocupan las
# columnas 1..5 (los grupos que faltan quedan a la izquierda, a cero).
def sumas_alineadas(secs_vec, desplazamientos):
    M = np.zeros((5, 4), dtype=int)
    for vecs, sh in zip(secs_vec, desplazamientos):
        take = vecs[-5:] if len(vecs) >= 5 else vecs
        for k, v in enumerate(take):
            col = 5 - len(take) + k
            M[col] += v
    return M.ravel().tolist()

DESP = [max(0, 5 - len(v)) for v in Q63v]
sumas63 = sumas_alineadas(Q63v, DESP)
central68 = SEC68[1]
pr("   sumas de UR063 alineadas:", sumas63)
pr("   seccion central UR068   :", central68)
obs2 = matches(sumas63, central68)
obs2t = matches(sumas63, central68, tol=True)
pr(f"   observado: {obs2}/20 exactas, {obs2t}/20 con tolerancia")
for i, (s, v) in enumerate(zip(sumas63, central68)):
    if s != v:
        pr(f"    col {i+1}: UR063={s} UR068={v} dif={v-s}")

# nulo: permutar los grupos de 4 dentro de cada seccion (conserva sus vectores)
Q63flat = [[v for v in qq] for qq in Q63v]
nulo3 = []
for _ in range(5000):
    secs = [list(rng.permutation(np.array(qq, dtype=object), axis=0)) if len(qq) else [] for qq in Q63flat]
    secs = [[list(map(int, v)) for v in qq] for qq in secs]
    nulo3.append(matches(sumas_alineadas(secs, DESP), central68))
nulo3 = np.array(nulo3)
p3 = L.p_emp(obs2, nulo3)
pr(f"   nulo (permutar grupos dentro de seccion, 5000 rep): media={nulo3.mean():.2f} max={nulo3.max()} p={p3:.5f}")

# ---------------------------------------------------------------- P3
lcs_6468 = L.lcs(V64, V68)
pr(f"\nP3. UR064 vs UR068: LCS={lcs_6468} de {min(len(V64),len(V68))} cuerdas "
   f"(pares identicos por posicion: {matches(V64,V68)}/{min(len(V64),len(V68))})")
nulo4 = np.array([L.lcs(V64, list(rng.permutation(V68))) for _ in range(2000)])
pr(f"   nulo (barajar UR068): media={nulo4.mean():.1f} max={nulo4.max()} p={L.p_emp(lcs_6468,nulo4):.5f}")

# suma de secciones nivel II (comprobacion de copia)
SEC64 = [V64[17:36], V64[36:52], V64[52:71]]
pr("   sumas por seccion UR064:", [sum(x) for x in SEC64], " UR068:", [sum(x) for x in SEC68])

json.dump(dict(sumas68=sumas68, d67=d67_sin, obs_p1=obs_ex, p1=float(p1), p2=float(p2),
               sumas63=sumas63, central68=central68, obs_p2=obs2, p3=float(p3),
               lcs_6468=lcs_6468),
          open(L.AQUI / "puruchuco_jerarquia.json", "w"), indent=1)
with open(L.AQUI / "salida_01_puruchuco.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
