# -*- coding: utf-8 -*-
"""V0: codificación decimal posicional (Locke 1912; Ascher & Ascher 1981).
Comprueba en los 64.464 racimos de nudos que:
  - nudo simple aporta n * 10^k (k entero >=0)
  - nudo largo aporta n (unidades), nunca >=10
  - figura de ocho / otros aportan n
"""
import pandas as pd, numpy as np, re, os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
rows = []
for s in D.nudos.dropna():
    for m in re.finditer(r"(\d+)([A-Z]+)\(([-0-9.]+),([SZU])\)(?:,(\d+))?", s):
        rows.append((int(m.group(1)), m.group(2), int(m.group(5)) if m.group(5) else 0))
r = pd.DataFrame(rows, columns=["n", "tipo", "val"])
print("clusters:", len(r), "| con valor>0:", int((r.val > 0).sum()))

for t in ["S", "L", "E", "EE", "LL", "BL", "SP", "TF"]:
    x = r[r.tipo == t]
    if len(x) == 0:
        continue
    print(f"{t}: n={len(x)} max_n={x.n.max()} max_val={x.val.max()} val==n={x.val.eq(x.n).mean():.3f}")

s = r[(r.tipo == "S") & (r.n <= 9) & (r.val > 0)]
k = np.log10(s.val / s.n)
print("S (n<=9): clusters", len(s), "| val/n = 10^entero:", f"{(abs(k-k.round())<1e-9).mean():.4f}")
print("posiciones decimales k:", pd.Series(np.round(k).astype(int)).value_counts().sort_index().to_dict())
print("S con k no entero:", int((abs(k - k.round()) > 1e-9).sum()))

l = r[r.tipo == "L"]
print("L: con n<=9 y val>=10:", int(((l.n <= 9) & (l.val >= 10)).sum()),
      "| con n>9 (notación valor):", int((l.n > 9).sum()))
print("todos los clusters con n>9:", int((r.n > 9).sum()), f"({100*(r.n>9).mean():.2f}%)")
