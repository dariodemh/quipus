# -*- coding: utf-8 -*-
"""Nulo: frecuencia con que una edicion de UNA operacion con el mismo delta
aparece por azar en cuerdas de quipus no relacionados.

q(tipo, delta, n_racimos) = fraccion de cuerdas aleatorias (con la misma
exposicion: tener nudo largo, figura de ocho, etc.) que admiten una edicion de
ese tipo con Delta = delta exacto.

p_nulo(relacion) = 1 - (1-q)^k, k = cuerdas de la relacion.
"""
import os, sys
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")
sys.path.insert(0, OUT)
from importlib import import_module
eng = import_module("03_reparaciones") if False else None   # (no reimportar: usa funciones copiadas)

RE = None
import re
RE = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")

def parse(chain):
    if not isinstance(chain, str):
        return []
    cl = []
    for m in RE.finditer(chain):
        n, tipo, pos, d, val = int(m.group(1)), m.group(2), float(m.group(3)), m.group(4), float(m.group(5))
        cl.append(dict(n=n, tipo=tipo, pos=pos, d=d, val=val, power=None))
    for c in cl:
        if c["tipo"].startswith("S") and c["val"] > 0 and c["n"] > 0:
            r = c["val"] / c["n"]
            p = round(np.log10(r)) if r > 0 else 0
            c["power"] = int(p) if abs(r - 10 ** p) < 1e-6 else 0
    for i, c in enumerate(cl):
        if c["power"] is None:
            below = [x["power"] for x in cl[i + 1:] if x["power"] is not None]
            c["power"] = int(max(below) + 1) if below and max(below) >= 0 else 0
    return cl

def deltas(cl):
    """Conjunto de (tipo, delta) alcanzables con una edicion."""
    out = set()
    n_L = sum(1 for c in cl if c["tipo"].startswith("L"))
    n_E = sum(1 for c in cl if c["tipo"].startswith("E"))
    n_S = sum(1 for c in cl if c["tipo"].startswith("S"))
    for c in cl:
        v, p = c["val"], c["power"]
        out.add(("factor10", 9 * v)); out.add(("factor10", -9 * v))
        out.add(("racimo_omitido", -v)); out.add(("racimo_duplicado", +v))
        if c["tipo"].startswith("L"):
            out.add(("vueltas", 10 ** p)); out.add(("vueltas", -10 ** p))
            out.add(("S_vs_L", 10 ** p - v))
            for k in range(2, 10):
                out.add(("ocho_vs_largo", 1 - k))
        if c["tipo"].startswith("S"):
            out.add(("conteo_simple", 10 ** p)); out.add(("conteo_simple", -10 ** p))
            out.add(("S_vs_L", 1 - v)); out.add(("ocho_vs_largo", 1 - v))
        if c["tipo"].startswith("E"):
            for k in range(2, 10):
                out.add(("ocho_vs_largo", k - 1))
    for p in range(0, 5):
        for m in range(1, 10):
            out.add(("insercion", m * 10 ** p))
    for k in range(1, 10):
        out.add(("insercion", k))
    return out

# ---------- universo de cuerdas no relacionadas ----------
d = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"), dtype={"valor": float})
SIS = {"UR270", "UR273A", "UR273B", "UR274A", "UR274B", "UR278", "UR266", "UR275",
       "UR269", "UR267A", "UR267B", "UR255", "UR256"}
pool = d[(~d.kfg.isin(SIS)) & (d.valor > 0) & d.nudos.notna()].copy()
pool["nrac"] = pool.nudos.str.count(";") + 1
print("pool de cuerdas no relacionadas:", len(pool), "quipus:", pool.kfg.nunique())

rng = np.random.default_rng(20261018)
DELTAS = [1, -1, 2, -2, 5, -5, 6, -6, 7, -7, 10, -10, 24, -24, 25, -25, 29, -29, 36, -36,
          44, -44, 46, -46, 70, -70, 94, -94, 100, -100, 125, -125, 1000, -1000]
filas = []
for nrac in [1, 2, 3, 4, 5, 6]:
    sub = pool[pool.nrac == nrac]
    if len(sub) > 6000:
        sub = sub.sample(6000, random_state=20261018)
    hab = [deltas(parse(x)) for x in sub.nudos]
    hab_any = [set(x[1] for x in h) for h in hab]
    for delta in DELTAS:
        q_any = np.mean([delta in h for h in hab_any]) if hab else np.nan
        por_tipo = {}
        for t in ["factor10", "vueltas", "racimo_omitido", "racimo_duplicado", "S_vs_L",
                  "ocho_vs_largo", "conteo_simple", "insercion"]:
            por_tipo[t] = np.mean([any(tt == t and dd == delta for tt, dd in h) for h in hab]) if hab else np.nan
        filas.append(dict(n_racimos=nrac, delta=delta, n=len(sub), q_any=q_any, **por_tipo))
Q = pd.DataFrame(filas)
Q.to_csv(os.path.join(OUT, "nulo_ediciones.csv"), index=False)
print(Q[Q.n_racimos.isin([2, 3])].pivot(index="delta", columns="n_racimos", values="q_any").round(3).to_string())
