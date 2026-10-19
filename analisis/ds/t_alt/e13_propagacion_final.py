"""Propagacion corregida: denominador = numero de simulaciones VALIDAS
(grupos con >=k cuerdas y suma>0). Reporta P(suma cambia) y, condicionado a
que cambie, la magnitud del cambio.
"""
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
W = pd.read_csv(AQUI/"desacuerdos_alineados.csv")
rat = (W.v_okr/W.v_kfg.replace(0, np.nan)).dropna()
rat = rat[(rat > 0) & np.isfinite(rat)]
logr = np.concatenate([np.log(rat.values), -np.log(rat.values)])

d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
d["v"] = pd.to_numeric(d.valor, errors="coerce").fillna(0)
g = pd.read_csv(RAIZ/"analisis/datos/grupos.csv", dtype=str, keep_default_na=False)
g["desde"] = pd.to_numeric(g.desde, errors="coerce"); g["hasta"] = pd.to_numeric(g.hasta, errors="coerce")
d["pnum"] = d.cuerda.str.extract(r"^p(\d+)$")[0]
raiz = d[d.pnum.notna()].copy(); raiz["pnum"] = raiz.pnum.astype(int)
Vq = {k: {int(i): float(x) for i, x in zip(gr.pnum, gr.v)} for k, gr in raiz.groupby("kfg")}
grupos = []
for _, r in g.iterrows():
    vals = Vq.get(r.kfg, {})
    idx = [i for i in range(int(r.desde), int(r.hasta)+1) if i in vals]
    if len(idx) >= 2:
        grupos.append(np.array([vals[i] for i in idx]))
print("grupos:", len(grupos), " suma mediana:", np.median([x.sum() for x in grupos]))

rng = np.random.default_rng(20261018)
NS = 30000
for p in [0.00225, 0.00047]:
    print(f"\n=== p = {p} ===")
    print("k   validas   P(cambia)   |   si cambia: rel med  p90   | abs med  p90")
    for k in [2, 3, 5, 8, 10]:
        val = 0; rel = []; ab = []
        for _ in range(NS):
            gr = grupos[rng.integers(len(grupos))]
            if len(gr) < k:
                continue
            pick = rng.choice(len(gr), k, replace=False)
            vals = gr[pick].astype(float); s0 = vals.sum()
            if s0 <= 0:
                continue
            val += 1
            m = rng.random(k) < p
            if not m.any():
                continue
            v2 = vals * np.where(m, np.exp(rng.choice(logr, k)), 1.0)
            rel.append(abs(v2.sum()-s0)/s0); ab.append(abs(v2.sum()-s0))
        rel = np.array(rel); ab = np.array(ab)
        print(f"{k:<3} {val:7d}   {100*len(rel)/val:7.2f}%    |  {100*np.median(rel):6.1f}%  {100*np.percentile(rel,90):6.0f}%  | {np.median(ab):5.0f}  {np.percentile(ab,90):6.0f}")
