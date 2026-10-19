"""05 · Cuantas vias independientes sostienen cada celda de la rejilla (19_prediccion)."""
import sys
import pandas as pd
sys.path.insert(0, ".")
from comun_rejilla import RAIZ, cargar_cuerdas

c, q = cargar_cuerdas()
I = pd.read_csv(f"{RAIZ}/19_prediccion/inventario_redundancia.csv")
L = pd.read_csv(f"{RAIZ}/19_prediccion/loo_consenso.csv")[["quipu", "cuerda", "exacta", "n_vias"]]


def celdas(k, grupos):
    s = c[(c.kfg == k) & (c.nivel == 0) & (c.grupo.isin(grupos))].sort_values(["grupo", "orden"])
    s["pos"] = s.groupby("grupo").cumcount() + 1
    return s[s.pos <= 9][["kfg", "cuerda"]]


for k, gs, nombre in [("UR278", [21, 25, 26, 27, 28], "UR278"),
                      ("UR270", [0, 4, 5, 8, 9], "UR270")]:
    u = celdas(k, gs)
    m = u.merge(I, left_on=["kfg", "cuerda"], right_on=["quipu", "cuerda"], how="left")
    m = m.merge(L, on=["quipu", "cuerda"], how="left", suffixes=("_inv", "_loo"))
    print(f"{nombre}: {len(m)} cuerdas")
    print("  reglas:", m.reglas.fillna("(sin prediccion)").value_counts().to_dict())
    print("  n_vias_indep:", m.n_vias_indep.value_counts(dropna=False).to_dict())
    print("  exactas (LOO):", int(m.exacta.sum()), "/", int(m.exacta.notna().sum()))
    if k == "UR278":
        # ±1: comparar el valor con la prediccion del LOO no siempre esta; usar la tabla de 13
        pass
