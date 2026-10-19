"""03: archivos de los mejores candidatos del mapa de legibilidad (sin informe)
y tabla-resumen de candidatos. Usa el mismo pipeline que 02."""
import numpy as np
import pandas as pd
import comun_np as L
from importlib import import_module

g = import_module("02_general")
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


res = {}
for proc in ["Ica", "Huaquerones"]:
    res[proc] = g.analizar(proc)

# --- tabla de los mejores candidatos de n_legibilidad (fuera de Incahuasi)
leg = pd.read_csv(L.RAIZ / "analisis/ds/n_legibilidad/quipus_legibles.csv")
top = leg[(leg.procedencia != "Incahuasi")].sort_values("q").head(15)
c, q = L.cargar_kfg()
filas = []
for r in top.itertuples():
    regs = L.registros_kfg(c, r.kfg)
    n = sum(1 for x in regs if not x["vacio"])
    filas.append(dict(kfg=r.kfg, procedencia=r.procedencia, n_reg=n,
                      genero=str(getattr(r, "genero", "")), q_leg=r.q))
tab = pd.DataFrame(filas)
tab.to_csv(L.AQUI / "candidatos_legibilidad.csv", index=False)
pr("\nMejores candidatos del mapa de legibilidad (fuera de Incahuasi):")
pr(tab.to_string(index=False))

with open(L.AQUI / "salida_03_candidatos.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
