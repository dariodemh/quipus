# -*- coding: utf-8 -*-
"""07 - Resumen estadistico: familia de pruebas y correccion de Holm."""
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

AQUI = Path(__file__).parent

# (nombre, p, familia)  -- p-valores empíricos ya calculados en 03,04,06
pruebas = [
    ("k-mer valor k=3 (tipos) [todos]",         0.002, "sec-val"),
    ("k-mer valor k=3 (pares) [todos]",         0.002, "sec-val"),
    ("k-mer valor k=4 (tipos) [todos]",         0.002, "sec-val"),
    ("k-mer valor k=4 (pares) [todos]",         0.028, "sec-val"),
    ("k-mer valor k=5 (tipos) [todos]",         0.002, "sec-val"),
    ("k-mer valor k=3 (tipos) [sin dup]",       0.002, "sec-val"),
    ("k-mer valor k=4 (tipos) [sin dup]",       0.136, "sec-val"),
    ("k-mer valor k=5 (tipos) [sin dup]",       1.000, "sec-val"),
    ("total(A)=bloque contiguo en B",           0.373, "otros"),
    ("total(A)=valor en B (nulo cross-quipu)",  1.000, "otros"),
    ("estructuras de grupo identicas",          1.000, "otros"),
    ("k-mer color k=4 (pares) [todos]",         0.002, "color"),
    ("k-mer color k=4 (pares) [sin dup]",       0.002, "color"),
    ("k-mer color k=3 (tipos) [todos]",         1.000, "color"),
    ("direccion de nudo Z>S (sign test)",       0.00686, "direccion"),
]
df = pd.DataFrame(pruebas, columns=["prueba", "p", "familia"])

def holm(ps):
    ps = list(ps); m = len(ps)
    order = np.argsort(ps)
    adj = [None] * m
    prev = 0.0
    for rank, i in enumerate(order):
        val = ps[i] * (m - rank)
        val = max(val, prev)   # monotono
        val = min(val, 1.0)
        adj[i] = val
        prev = val
    return adj

df["p_holm_global"] = holm(df["p"].tolist())
for fam, grp in df.groupby("familia"):
    sub = grp.copy()
    sub["p_holm_fam"] = holm(sub["p"].tolist())
    print(f"--- familia {fam} (Holm dentro de familia) ---")
    print(sub[["prueba", "p", "p_holm_fam"]].to_string(index=False))

print("\n--- Holm global (familia amplia de 15 pruebas) ---")
print(df[["prueba", "p", "p_holm_global"]].sort_values("p").to_string(index=False))
df.to_csv(AQUI / "salida" / "pruebas_holm.csv", index=False)

# tamano de efecto direccion a nivel de quipu
print("\nDireccion: 30 quipus Z>S vs 13 S>Z (1 empate); sign test p=0.0069")
