# -*- coding: utf-8 -*-
"""Platt (cap. 10): el significado del color varia por provincia.
Test de interaccion color x sitio sobre el rango percentil del valor, centrado por sitio.
"""
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng = np.random.default_rng(SEED)
d, q = prep.load()
q = q.set_index("kfg")
d0 = d[d.nivel == 0].copy()
d0["valor_n"] = pd.to_numeric(d0.valor_n, errors="coerce")

c = d0.dropna(subset=["color_f", "valor_n"]).copy()
c["procedencia"] = c.kfg.map(q.procedencia)
c = c[(c.valor_n > 0) & c.procedencia.notna()]
top_sites = c.procedencia.value_counts()[lambda s: s >= 100].index
c = c[c.procedencia.isin(top_sites)]
top_colors = c.color_f.value_counts()[lambda s: s >= 100].index
c = c[c.color_f.isin(top_colors)]
print("cuerdas:", len(c), "| sitios:", c.procedencia.nunique(), "| colores:", c.color_f.nunique())
print(c.groupby("procedencia").size().sort_values(ascending=False).to_string())
c["rank"] = c.groupby("procedencia").valor_n.rank(pct=True)


def stat(df, minn=5):
    cell = df.groupby(["procedencia", "color_f"]).agg(m=("rank", "mean"), n=("rank", "size"))
    cell = cell[cell.n >= minn].reset_index()
    cell["dev"] = cell.m - cell.groupby("procedencia").m.transform("mean")
    return (cell.n * cell.dev ** 2).sum() / cell.n.sum(), len(cell)


obs, ncell = stat(c)
print("observado:", round(obs, 4), "celdas:", ncell)
null = np.empty(2000)
for i in range(2000):
    cc = c.copy()
    cc["procedencia"] = rng.permutation(cc.procedencia.values)
    cc["rank"] = cc.groupby("procedencia").valor_n.rank(pct=True)
    null[i] = stat(cc)[0]
p = (1 + (null >= obs).sum()) / 2001
print(f"nulo={null.mean():.4f} (DE {null.std():.4f}); p={p:.5f}")

# control: solo colores con >=300 cuerdas para evitar celdas pequenas
big = c.color_f.value_counts()[lambda s: s >= 300].index
c2 = c[c.color_f.isin(big)]
obs2, nc2 = stat(c2)
null2 = np.empty(2000)
for i in range(2000):
    cc = c2.copy()
    cc["procedencia"] = rng.permutation(cc.procedencia.values)
    cc["rank"] = cc.groupby("procedencia").valor_n.rank(pct=True)
    null2[i] = stat(cc)[0]
p2 = (1 + (null2 >= obs2).sum()) / 2001
print(f"colores grandes: obs={obs2:.4f} ({nc2} celdas), nulo={null2.mean():.4f}, p={p2:.5f}")

# actualizar la fila correspondiente en resultados_principales.csv
try:
    r = pd.read_csv("resultados_principales.csv")
    m = r.test.str.contains("Interacci", na=False)
    r.loc[m, "observado"] = obs
    r.loc[m, "nulo"] = float(null.mean())
    r.loc[m, "p"] = p
    r.loc[m, "n"] = len(c)
    r.loc[m, "extra"] = f"{c.procedencia.nunique()} sitios, {c.color_f.nunique()} colores"
    r.to_csv("resultados_principales.csv", index=False)
    print("resultados_principales.csv actualizado")
except Exception as e:
    print("no se pudo actualizar:", e)
