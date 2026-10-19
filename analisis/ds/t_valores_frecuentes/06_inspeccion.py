# -*- coding: utf-8 -*-
"""Inspeccion de los quipus que sostienen los excesos y controles de copia/duplicado."""
import pandas as pd, numpy as np, os

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False).set_index("kfg")
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0]

def perfil(quipu, n=12):
    s = k[k.kfg == quipu]
    prov = q.procedencia.get(quipu, "?")
    print(f"\n--- {quipu} ({prov}) | cuerdas={len(s)} | nivel0={int((s.nivel==0).sum())} ---")
    print("top valores:", s.valor.value_counts().head(n).to_dict())
    for v in [100, 200, 110, 47, 33, 22, 15, 10, 1]:
        m = s[s.valor == v]
        if len(m):
            print(f"  v={v:>4}: {len(m):>3} | nivel {m.nivel.value_counts().to_dict()} | "
                  f"madre {int(m.nivel.notna().sum() and 0)} | color {m.color.value_counts().head(3).to_dict()}")

for x in ["UR1109", "UR1084", "HP055", "UR275", "UR266", "UR270"]:
    if x in set(k.kfg): perfil(x)

# comparar multiconjuntos de valores entre pares
def jaccard(a, b):
    A = pd.Series(k[k.kfg == a].valor.values).value_counts()
    B = pd.Series(k[k.kfg == b].valor.values).value_counts()
    inter = sum(min(A.get(v, 0), B.get(v, 0)) for v in set(A.index) | set(B.index))
    uni = sum(max(A.get(v, 0), B.get(v, 0)) for v in set(A.index) | set(B.index))
    return inter / uni if uni else np.nan, inter, uni

for a, b in [("UR1084", "HP055"), ("UR275", "UR266"), ("UR270", "UR271")]:
    if a in set(k.kfg) and b in set(k.kfg):
        j, i, u = jaccard(a, b)
        print(f"\nJaccard valores {a}/{b}: {j:.3f} (interseccion {i}, union {u})")
        print(f"  n cuerdas {a}={len(k[k.kfg==a])}, {b}={len(k[k.kfg==b])}")

# ---- efecto de quitar duplicados en el heaping global ----
print("\n=== control: heaping de 100/200/47/33/22 quitando un miembro de cada par ===")
base = pd.Series(k.valor.values).value_counts()
drop = [x for x in ["UR1084", "UR266"] if x in set(k.kfg)]
sub = k[~k.kfg.isin(drop)]
fs = pd.Series(sub.valor.values).value_counts()
for v in [100, 200, 110, 47, 33, 22, 15]:
    print(f"v={v:>4}: total {base.get(v,0):>4} -> {fs.get(v,0):>4} tras quitar {drop}")

# ---- 100, 200, ..., 900: es un fenomeno de centenas redondas? ----
print("\n=== centenas y valores redondos ===")
ft = pd.Series(k.valor.values).value_counts()
for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 150, 250, 120, 110, 101, 105]:
    print(f"{v:>5}: {ft.get(v,0):>4}")
