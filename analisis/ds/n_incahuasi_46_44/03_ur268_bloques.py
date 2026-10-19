"""03. ¿Es UR268 (cuota 208) la suma de los bloques de UR269?

Tres definiciones de bloque, todas con las cabeceras de las filas de UR269:
  (a) separadores rosas (PK): 15 bloques de tamaños [5,5,5,5,4,8,5,4,5,5,5,2,4,2,4].
  (b) patrón de cuotas: un bloque empieza en una fila con cuota 47 y acaba antes de
      la siguiente; si no hay 47, se corta en la fila con cuota 25.
  (c) ventanas deslizantes de 5 filas consecutivas (54 ventanas).
Estadístico: nº de cabeceras de UR268 explicadas por el multiconjunto de sumas de
bloque (emparejamiento uno a uno, exacto y ±1), y LCS en el orden de UR268.
Nulo: barajar el orden de las filas de UR269 y recalcular las mismas sumas (conserva
los valores de fila y los tamaños de bloque, rompe la adyacencia real). 2000 réplicas.
BH sobre las 3 definiciones x 2 tolerancias. Se prueba también la suma de netos
(cabecera - cuota) como variante.
"""
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4603
NPERM = 2000
rng = np.random.default_rng(SEED)


def match1(S, T, tol=0):
    S = np.sort(np.asarray(S))
    T = np.sort(np.asarray(T))
    i = j = k = 0
    while i < len(S) and j < len(T):
        if S[i] < T[j] - tol:
            i += 1
        elif S[i] > T[j] + tol:
            j += 1
        else:
            k += 1
            i += 1
            j += 1
    return k


def lcs(S, T, tol=0):
    n, m = len(S), len(T)
    H = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n):
        for j in range(m):
            if abs(int(S[i]) - int(T[j])) <= tol:
                H[i + 1, j + 1] = H[i, j] + 1
            else:
                H[i + 1, j + 1] = max(H[i, j + 1], H[i + 1, j])
    return int(H[n, m])


c, q = C.cargar_todo()
F, Bloques = C.registros_ur269(c[c.kfg == "UR269"])
F = F.sort_values(["bloque", "fila"]).reset_index(drop=True)
U = C.registros(c[c.kfg == "UR268"])
T = np.array([r["cab"] for r in U])
print("UR268:", len(T), "registros; cabeceras", T.tolist())

# índices de fila por bloque: (a) PK
idx_pk = [list(x.index) for _, x in F.groupby("bloque")]
# (b) patrón de cuotas
idx_cu, act = [], []
for i, r in F.iterrows():
    if not np.isnan(r.cuota) and r.cuota == 47 and act:
        idx_cu.append(act)
        act = []
    act.append(i)
    if not np.isnan(r.cuota) and r.cuota == 25:
        idx_cu.append(act)
        act = []
if act:
    idx_cu.append(act)
# (c) ventanas de 5
idx_5 = [list(range(i, i + 5)) for i in range(len(F) - 4)]
print("bloques PK:", [len(b) for b in idx_pk])
print("bloques por cuota:", [len(b) for b in idx_cu])

# valores de fila: cabecera y neto (cab - cuota)
cab = F.cab.to_numpy(int)
cuota = F.cuota.fillna(0).to_numpy(float)
neto = cab - cuota

DEF = {"PK": idx_pk, "cuota": idx_cu, "ventana5": idx_5}


def sumas(idx, v):
    return np.array([v[i].sum() for i in idx])


res = []
for nombre, idx in DEF.items():
    for var, v in (("cabecera", cab), ("neto", neto)):
        S = sumas(idx, v)
        for tol in (0, 1):
            obs = match1(S, T, tol)
            filas = []
            for _ in range(NPERM):
                perm = rng.permutation(len(F))
                vp = v[perm]
                Sp = sumas(idx, vp)
                filas.append(match1(Sp, T, tol))
            filas = np.array(filas)
            res.append(dict(definicion=nombre, valores=var, tol=tol, nbloques=len(idx),
                            obs=obs, nulo_media=filas.mean(), nulo_max=filas.max(),
                            p=(np.sum(filas >= obs) + 1) / (NPERM + 1),
                            lcs=lcs(S, T, tol)))
R = pd.DataFrame(res)
R["q"] = C.bh(R.p)
R.to_csv(C.AQUI / "ur268_bloques.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 220)
print("\n== UR268 frente a sumas de bloque de UR269")
print(R.to_string(index=False))

print("\nsumas de bloque (cabeceras, PK) y UR268 más cercana:")
S = sumas(idx_pk, cab)
for b, s in enumerate(S):
    j = int(np.abs(T - s).argmin())
    print(f"  bloque {b:2d} suma {s:6d} | UR268 más cercana {T[j]:6d} (dif {s - T[j]:+5d})")

# potencia: si UR268 fuese exactamente las sumas de bloque, ¿se detectaría?
print("\npotencia (alternativa perfecta): con 15 bloques y 29 registros el máximo "
      f"emparejamiento es {min(15, 29)}; P(nulo >= {min(15, 29)}) = "
      f"{(np.sum(np.array([match1(sumas(idx_pk, cab[rng.permutation(len(F))]), T, 0) for _ in range(200)]) >= min(15, 29)) + 1) / 201:.4f}")
