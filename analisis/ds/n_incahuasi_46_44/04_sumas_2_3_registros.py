"""04. ¿Es alguna fila 2-4 de UR269 la suma de dos o tres registros de un quipu
del archivo de Incahuasi (UR255-UR280, UR267A/B, UR273A/B, UR274A/B, JC001-JC023)?

Para cada objetivo t (conjuntos A y B de 00_objetivos.py) se cuentan las
representaciones t = a+b y t = a+b+c con registros distintos del MISMO quipu
(cabeceras). Estadístico: nº total de representaciones y nº de objetivos con >=1.

Nulo de densidad local (preserva la magnitud): para cada objetivo se sortean enteros
en su ventana [0,9t, 1,1t] y se cuenta cuántas representaciones tienen. Así el nulo
mide "¿es t más representable que un número cualquiera de su tamaño?".
5000 réplicas para el estadístico global (una extracción por objetivo y réplica);
2000 por objetivo para el p individual, con BH sobre objetivos.
Sensibilidad: tolerancia ±1 y variante con todos los valores de nivel 0.
"""
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4604
NPERM = 5000
B_IND = 2000
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()
O = pd.read_csv(C.AQUI / "ur269_objetivos.csv")
TA = O[O.definicion == "A_posicion"].sort_values("orden").cab.to_numpy(int)
TB = O[O.definicion == "B_cuota"].sort_values("orden").cab.to_numpy(int)
F, _ = C.registros_ur269(c[c.kfg == "UR269"])
pool_cab = F.cab.to_numpy(int)

V, V0 = {}, {}
for k in C.ARCHIVO:
    s = c[c.kfg == k]
    if not len(s):
        continue
    R = C.registros(s)
    if len(R) >= 2:
        V[k] = np.array([r["cab"] for r in R])
    x0 = s[(s.nivel == 0) & s.pres].valor.to_numpy(int)
    if len(x0) >= 2:
        V0[k] = x0
print("quipus con >=2 registros:", len(V), "| con >=2 valores nivel 0:", len(V0))


def sumas(V, orden):
    porq = {}
    for k, v in V.items():
        if orden == 2:
            s = [int(v[i] + v[j]) for i in range(len(v)) for j in range(i + 1, len(v))]
        else:
            s = [int(v[i] + v[j] + v[l]) for i in range(len(v)) for j in range(i + 1, len(v))
                 for l in range(j + 1, len(v))]
        porq[k] = np.sort(np.array(s))
    todo = np.sort(np.concatenate([x for x in porq.values() if len(x)]))
    return porq, todo


def cuenta(todo, T, tol=0):
    T = np.atleast_1d(np.asarray(T))
    lo = np.searchsorted(todo, T - tol, "left")
    hi = np.searchsorted(todo, T + tol, "right")
    return (hi - lo).astype(int)


def ventana(t, rng, n):
    return rng.integers(max(100, int(0.9 * t)), int(1.1 * t) + 1, n)


filas = []
for nombre, T in (("A_posicion", TA), ("B_cuota", TB)):
    print(f"\n== objetivos {nombre} ({len(T)})")
    for orden in (2, 3):
        porq, todo = sumas(V, orden)
        for tol in (0, 1):
            o = cuenta(todo, T, tol)
            obs = int(o.sum())
            # nulo global: un valor de la ventana de cada objetivo por réplica
            sims = np.array([sum(cuenta(todo, ventana(t, rng, 1), tol)[0] for t in T)
                             for _ in range(NPERM)])
            p = (np.sum(sims >= obs) + 1) / (NPERM + 1)
            pj = np.array([(np.sum(cuenta(todo, ventana(t, rng, B_IND), tol) >= o[j]) + 1) / (B_IND + 1)
                           for j, t in enumerate(T)])
            qj = C.bh(pj)
            det = [(int(T[j]), k, int(cuenta(porq[k], [T[j]], tol)[0]))
                   for j in range(len(T)) for k in porq if cuenta(porq[k], [T[j]], tol)[0] > 0]
            filas.append(dict(objetivos=nombre, orden=orden, tol=tol, obs=obs,
                              objetivos_con_algo=int((o > 0).sum()), nulo_media=sims.mean(),
                              nulo_max=sims.max(), p=p, q_min=float(np.nanmin(qj)),
                              n_q05=int((qj < 0.05).sum())))
            print(f"  orden {orden} tol {tol}: obs={obs} en {(o>0).sum()}/{len(T)} objetivos; "
                  f"nulo local {sims.mean():.2f} (máx {sims.max()}); p={p:.4f}; "
                  f"q mínimo por objetivo={np.nanmin(qj):.3f}; con q<0,05: {(qj<0.05).sum()}")
            print(f"    detalle: {det[:10]}")

print("\n== control de densidad: todos los valores de nivel 0")
for nombre, T in (("A_posicion", TA), ("B_cuota", TB)):
    _, todo = sumas(V0, 2)
    o = cuenta(todo, T)
    sims = np.array([sum(cuenta(todo, ventana(t, rng, 1))[0] for t in T) for _ in range(NPERM)])
    print(f"  {nombre}: pares obs={o.sum()} en {(o>0).sum()} objetivos, nulo local {sims.mean():.2f}, "
          f"p={(np.sum(sims >= o.sum()) + 1) / (NPERM + 1):.4f}")

# ---- variante clave: excluir UR269 (evita la aritmética interna del propio libro)
print("\n== excluyendo UR269 del pool (sumas de registros de OTROS quipus)")
Vx = {k: v for k, v in V.items() if k != "UR269"}
V0x = {k: v for k, v in V0.items() if k != "UR269"}
for nombre, T in (("A_posicion", TA), ("B_cuota", TB)):
    for orden in (2, 3):
        porq, todo = sumas(Vx, orden)
        o = cuenta(todo, T)
        sims = np.array([sum(cuenta(todo, ventana(t, rng, 1))[0] for t in T) for _ in range(NPERM)])
        print(f"  {nombre} orden {orden}: obs={o.sum()} en {(o>0).sum()}/{len(T)}, "
              f"nulo local {sims.mean():.2f} (máx {sims.max()}), "
              f"p={(np.sum(sims >= o.sum()) + 1) / (NPERM + 1):.4f}")
    _, todo = sumas(V0x, 2)
    o = cuenta(todo, T)
    sims = np.array([sum(cuenta(todo, ventana(t, rng, 1))[0] for t in T) for _ in range(NPERM)])
    print(f"  {nombre} nivel0 sin UR269: obs={o.sum()} en {(o>0).sum()}, nulo {sims.mean():.2f}, "
          f"p={(np.sum(sims >= o.sum()) + 1) / (NPERM + 1):.4f}")

# ---- reparto por quipu de las representaciones observadas (pares, nivel 0)
print("\n== reparto por quipu de las representaciones con nivel 0 (pares, objetivos A)")
porq0, _ = sumas(V0, 2)
for k, s in sorted(porq0.items()):
    c_ = int(cuenta(s, TA).sum()) if len(s) else 0
    if c_:
        print(f"  {k}: {c_}")


pd.DataFrame(filas).to_csv(C.AQUI / "sumas_23_registros.csv", index=False, float_format="%.4g")
