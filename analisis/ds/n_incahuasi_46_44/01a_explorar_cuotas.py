"""01a. Exploración: ¿cuántos quipus del corpus tienen una constante por grupo?

Estadístico observado (sin nulo todavía): para cada quipu con >=5 registros,
para cada d candidato (1..min(300,x//2)), apoyo(d) = nº de registros con una
cuerda no cabecera de valor x-d. Se guarda el mejor d y su apoyo.
"""
import numpy as np
import pandas as pd
import comun_n as C

pd.set_option("display.width", 200)
c, q = C.cargar_todo()
filas = []
for k, s in c.groupby("kfg", sort=True):
    R = C.registros(s)
    if len(R) < 5:
        continue
    cnt = {}
    for r in R:
        x = r["cab"]
        ds = {x - v for v in r["resto"] if 0 < x - v <= min(300, x // 2)}
        for d in ds:
            cnt[d] = cnt.get(d, 0) + 1
    if not cnt:
        continue
    best = max(cnt.values())
    cand = sorted([d for d, v in cnt.items() if v == best])
    filas.append(dict(kfg=k, n=len(R), apoyo=best, d=cand[:4], nd=len(cnt)))
D = pd.DataFrame(filas)
print("quipus con >=5 registros:", len(D))
print(D.apoyo.value_counts().sort_index().to_string())
print("\nquipus con apoyo >= 0,6n y >=4:")
E = D[(D.apoyo >= 4) & (D.apoyo >= 0.6 * D.n)].sort_values(["apoyo", "n"], ascending=False)
print(len(E))
print(E.head(30).to_string(index=False))
D.to_csv(C.AQUI / "cuotas_observadas.csv", index=False)
