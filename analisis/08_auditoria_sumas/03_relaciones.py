"""Lista de relaciones PPS observadas (definición KFG) con su coste: global (cualquier distancia) y local (adyacente).
Coste = P(un valor aleatorio del quipu con el mismo nº de dígitos caiga en alguna suma de tramo disponible), modelo de
dígitos independientes por posición (Laplace 0,5). Salida: relaciones_pps.csv y resumen en consola."""
import numpy as np, pandas as pd
from kfg import *

Qs = cargar()
rows = []
for k, Q in Qs.items():
    F = digit_model(Q["v"][Q["pres"]])
    a = Q["v"][Q["P"]]
    R = rel_pps(a, F)
    nm = Q["names"][Q["P"]]
    for r in R:
        i, s, e = int(r[0]), int(r[1]), int(r[2])
        rows.append(dict(kfg=k, cuerda=nm[i], valor=int(a[i]), n_sumandos=e - s, sumandos=" ".join(map(str, a[s:e])),
                         lado="der" if s > i else "izq", distancia=(s - i - 1) if s > i else (i - e),
                         adyacente=bool(r[3]), cadena=bool(r[4]), coste_global=r[5], coste_local=r[6]))
d = pd.DataFrame(rows)
d.to_csv("relaciones_pps.csv", index=False)
n = len(d)
L = [f"relaciones PPS: {n} en {d.kfg.nunique()} quipus",
     f"valor <=20: {(d.valor<=20).mean():.3f}; <=50: {(d.valor<=50).mean():.3f}; >=100: {(d.valor>=100).mean():.3f}; >=1000: {(d.valor>=1000).mean():.3f}",
     f"adyacentes (saltando huecos): {d.adyacente.mean():.3f}; distancia mediana {d.distancia.median():.0f}, p90 {d.distancia.quantile(.9):.0f}",
     f"nº sumandos: mediana {d.n_sumandos.median():.0f}; >=10: {(d.n_sumandos>=10).mean():.3f}",
     f"coste global: mediana {d.coste_global.median():.3f}; <0.05: {(d.coste_global<0.05).sum()}; <0.01: {(d.coste_global<0.01).sum()}",
     f"coste local (solo adyacentes): mediana {d[d.adyacente].coste_local.median():.4f}; <0.01: {(d.coste_local<0.01).sum()} en {d[d.coste_local<0.01].kfg.nunique()} quipus; <0.001: {(d.coste_local<0.001).sum()} en {d[d.coste_local<0.001].kfg.nunique()} quipus"]
print("\n".join(L))
top = d[d.coste_local < 0.001].groupby("kfg").size().sort_values(ascending=False)
print(top.head(25).to_string())
open("salida_03_relaciones.txt", "w", encoding="utf8").write("\n".join(L) + "\n\nquipus con relaciones de coste local <0.001:\n" + top.to_string() + "\n")
