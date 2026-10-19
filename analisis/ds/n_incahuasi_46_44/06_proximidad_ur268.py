"""06. ¿Están las sumas de bloque de UR269 'cerca' de UR268 aunque no coincidan?

El equipo 13 señaló dos casi-coincidencias (9335 vs 9332; 10379 vs 10385). Aquí se
mide la proximidad de cada suma de bloque (definición PK) a la cabecera más cercana
de UR268 y se compara con un nulo que baraja las cabeceras de UR268. El nulo mide
lo aburrido: con 29 cabeceras repartidas en ~8000 unidades, la distancia al más
cercano es ~140 por puro espaciado.
"""
import numpy as np
import pandas as pd
import comun_n as C

SEED = 4608
NPERM = 5000
rng = np.random.default_rng(SEED)

c, q = C.cargar_todo()
F, B = C.registros_ur269(c[c.kfg == "UR269"])
T = np.array([r["cab"] for r in C.registros(c[c.kfg == "UR268"])])
idx = [list(x.index) for _, x in F.sort_values(["bloque", "fila"]).groupby("bloque")]
S = np.array([F.sort_values(["bloque", "fila"]).loc[i, "cab"].sum() for i in idx])
d = np.array([np.min(np.abs(T - s)) for s in S])
print("sumas de bloque:", S.tolist())
print("distancias a la cabecera UR268 más cercana:", d.tolist())
for umbral in (1, 10, 25, 50, 100, 200):
    obs = int((d <= umbral).sum())
    sims = np.array([(np.min(np.abs(rng.permutation(T)[None, :] - S[:, None]), axis=1) <= umbral).sum()
                     for _ in range(NPERM)])
    print(f"  <= {umbral:3d}: obs {obs}/{len(S)}; nulo medio {sims.mean():.2f} "
          f"(máx {sims.max()}); p={(np.sum(sims >= obs) + 1) / (NPERM + 1):.3f}")
