"""Tarea 5. Validacion cruzada por registros y controles nulos.
CV por mitades: para cada quipu los registros se parten en 2 mitades contiguas (y en 4 bloques); al predecir una cuerda de un
bloque se ocultan TODAS las cuerdas de los demas registros de ese bloque (las cuotas, anclas de alineacion y tasas de cierre
se formulan solo con el resto del quipu). Se compara con el LOO. Controles: (a) pares de copia sin relacion;
(b) sumas con los registros B desplazados una posicion. Salidas: cv_resultados.csv, cv_resumen.csv."""
import numpy as np
import pandas as pd
import comun19 as M

def corre(nb):
    filas = []
    for t in M.presentes():
        if t not in M.REC_DE:
            continue
        k, i = M.REC_DE[t]
        n = len(M.REC[k])
        b = min(nb - 1, i * nb // n)
        mate = [x for j, r in enumerate(M.REC[k]) if j != i and min(nb - 1, j * nb // n) == b for x in r["cords"]]
        hide = set(mate) | {t}
        for p in M.predecir(t, hide):
            filas.append(dict(quipu=k, cuerda=t[1], real=M.VAL[t], regla=p["rule"], pred=p["pred"], bloques=nb, **M.metricas(p["pred"], M.VAL[t])))
    return pd.DataFrame(filas)

CV = pd.concat([corre(2), corre(4)])
CV.to_csv(M.AQUI / "cv_resultados.csv", index=False)
L = pd.read_csv(M.AQUI / "loo_resultados.csv")
res = {"LOO": L.groupby("regla").agg(n=("exacta", "size"), exacta=("exacta", "mean"), tol=("tol", "mean"), r5=("r5", "mean"))}
for nb in (4, 2):
    res[f"CV{nb}"] = CV[CV.bloques == nb].groupby("regla").agg(n=("exacta", "size"), exacta=("exacta", "mean"), tol=("tol", "mean"), r5=("r5", "mean"))
T = pd.concat(res, axis=1).round(3)
T.to_csv(M.AQUI / "cv_resumen.csv")
print(T.to_string())
for nb in (4, 2):
    c = CV[CV.bloques == nb]
    g = c.groupby(["quipu", "cuerda"]).apply(lambda x: x.iloc[0]).exacta.mean()
    print(f"CV{nb}: predicciones {len(c)}, exacta global {c.exacta.mean():.3f}")
print(f"LOO: predicciones {len(L)}, exacta global {L.exacta.mean():.3f}")

# controles nulos: la misma maquinaria de alineacion ciega sobre pares sin relacion
M.PARES_COPIA[:] = [("UR255", "UR275"), ("UR256", "UR266"), ("UR267A", "UR269"), ("UR273B", "UR255"), ("UR267B", "UR275"), ("UR270", "UR256")]
nul = []
for t in M.presentes():
    for p in M.r_copia(t, {t}):
        nul.append(M.metricas(p["pred"], M.VAL[t]))
nul = pd.DataFrame(nul)
print(f"\nControl copia con pares SIN relacion: {len(nul)} predicciones, exacta {nul.exacta.mean():.3f}, tol {nul.tol.mean():.3f}")
