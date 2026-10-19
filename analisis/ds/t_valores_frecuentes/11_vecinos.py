# -*- coding: utf-8 -*-
"""Control libre de modelo: peso de cada valor redondo dentro de su propia decena.
No depende de la independencia de digitos de B2."""
import pandas as pd, numpy as np, os

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0]
f = k.valor.value_counts()

rows = []
for v in [10, 40, 100, 110, 200, 300]:
    s = [int(f.get(x, 0)) for x in range(v, v + 10)]
    rows.append({"valor": v, "n": s[0], "total_decena": sum(s), "pct_decena": 100 * s[0] / sum(s),
                 "media_vecinos": round(np.mean(s[1:]), 1),
                 "veces_media": round(s[0] / np.mean(s[1:]), 2)})
T = pd.DataFrame(rows)
T.to_csv(OUT + r"\tabla_vecinos.csv", index=False)
print(T.to_string(index=False))
