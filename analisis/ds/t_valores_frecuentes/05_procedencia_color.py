# -*- coding: utf-8 -*-
"""Concentracion por procedencia (unidad = quipu) y asociacion con color
(estratificada por quipu, para no confundir color global del quipu con valor).
"""
import pandas as pd, numpy as np, os, re
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))

c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)

cand = [1, 2, 3, 5, 10, 11, 12, 15, 20, 22, 30, 33, 40, 47, 50, 100, 110, 200]
f = pd.Series(k.valor.values).value_counts()
cand = [v for v in cand if f.get(v, 0) >= 100]

# ================= A) PROCEDENCIA =================
meta = q.set_index("kfg")
todas = sorted(k.kfg.unique())
prov = meta.reindex(todas).procedencia.fillna("Unknown").astype(str)
prov = prov.replace({"unknown": "Unknown", "nan": "Unknown"})
conteo_prov = prov.value_counts()
sitios = [s for s in conteo_prov.index if conteo_prov[s] >= 15 and s != "Unknown"]
print("sitios con >=15 quipus:", {s: int(conteo_prov[s]) for s in sitios})

pres = k.groupby(["kfg", "valor"]).size().unstack(fill_value=0)
pres = (pres > 0).reindex(todas, fill_value=False)
rows = []
for s in sitios:
    en = prov[prov == s].index
    fuera = prov[prov != s].index
    for v in cand:
        a = int(pres.loc[en, v].sum()); b = len(en) - a
        cc = int(pres.loc[fuera, v].sum()); dd = len(fuera) - cc
        OR, p = stats.fisher_exact([[a, b], [cc, dd]])
        rows.append({"sitio": s, "valor": v, "quipus_sitio": len(en), "con_valor": a,
                     "pct_sitio": 100 * a / len(en), "pct_resto": 100 * cc / len(fuera),
                     "odds_ratio": OR, "p": p})
P = pd.DataFrame(rows)

def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); qq = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, p[o[i]] * m / (i + 1)); qq[o[i]] = prev
    return qq
P["q"] = bh(P.p.values)
P.to_csv(OUT + r"\tabla_procedencia.csv", index=False)
pd.set_option("display.width", 260)
print("\n=== A) asociaciones valor-sitio (Fisher, BH sobre %d pruebas) ===" % len(P))
print(P.sort_values("p").head(16).to_string(index=False, float_format=lambda x: f"{x:.3g}"))
print("sobreviven q<0.05:", (P.q < .05).sum(), "de", len(P))

# ================= B) COLOR =================
def color_prim(x):
    if not isinstance(x, str): return None
    return re.split(r"[\(:/,\-]", x.strip())[0].strip()
k["col"] = k.color.map(color_prim)
print("\ncolores primarios (cuerdas):", k.col.value_counts().head(10).to_dict())
top_col = k.col.value_counts().head(6).index.tolist()
print("colores probados:", top_col)

qids = sorted(k.kfg.unique()); qidx = {x: i for i, x in enumerate(qids)}
k["qi"] = k.kfg.map(qidx)
nq = len(qids)
n_i = k.groupby("qi").size().reindex(range(nq), fill_value=0).values

rows = []
for v in cand:
    n_iv = k[k.valor == v].groupby("qi").size().reindex(range(nq), fill_value=0).values
    p_i = n_iv / n_i
    for col in top_col:
        n_ic = k[k.col == col].groupby("qi").size().reindex(range(nq), fill_value=0).values
        obs = int(((k.valor == v) & (k.col == col)).sum())
        exp = float((n_ic * p_i).sum())
        var = float((n_ic * p_i * (1 - p_i) * (n_i - n_ic) / np.maximum(n_i - 1, 1)).sum())
        z = (obs - exp) / np.sqrt(var) if var > 0 else np.nan
        rows.append({"valor": v, "color": col, "obs": obs, "esp": round(exp, 1),
                     "ratio": obs / exp if exp > 0 else np.nan, "z": z,
                     "p": 2 * stats.norm.sf(abs(z)) if np.isfinite(z) else 1.0})
C = pd.DataFrame(rows)
C["q"] = bh(C.p.values)
C.to_csv(OUT + r"\tabla_color.csv", index=False)
print("\n=== B) valor x color, estratificado por quipu (BH sobre %d pruebas) ===" % len(C))
print(C.reindex(C.z.abs().sort_values(ascending=False).index).head(18)
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))
print("sobreviven q<0.05:", (C.q < .05).sum(), "de", len(C))
print("\ncolor mas asociado por valor (solo q<0.05):")
for v in cand:
    s = C[(C.valor == v) & (C.q < .05)]
    if len(s):
        print(f"  v={v:>4}: " + ", ".join(f"{r.color} {r.ratio:.2f}x" for r in s.itertuples()))
