# -*- coding: utf-8 -*-
"""04 - Diagnostico: LCCS entre pares y k-mers de valor SIN el duplicado AS125/UR247."""
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"
NPERM = 500

q = pd.read_csv(DAT / "quipus.csv")
c = pd.read_csv(DAT / "cuerdas.csv")
m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
ids = sorted(q[m & q["kfg"].str.startswith(("AS", "UR"))]["kfg"].tolist())
cc = c[c["kfg"].isin(ids)]

def vr(v, n):
    if pd.isna(v): return None
    if v == 0 and (pd.isna(n) or str(n).strip() == ""): return None
    return float(v)

seq = {}
for k in ids:
    rows = cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")
    seq[k] = [vr(r["valor"], r["nudos"]) for _, r in rows.iterrows()]

def lccs(a, b):
    """longitud del mayor bloque de valores consecutivos (sin huecos) comunes a ambos."""
    A = [x for x in a if x is not None]
    B = [x for x in b if x is not None]
    # cuidado: quitamos None => puede unir rachas a traves de huecos; para diagnosticar es aceptable
    prev = [0] * (len(B) + 1)
    best = 0
    for i in range(1, len(A) + 1):
        cur = [0] * (len(B) + 1)
        for j in range(1, len(B) + 1):
            if A[i - 1] == B[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best

pares = []
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        L = lccs(seq[ids[i]], seq[ids[j]])
        if L >= 3:
            pares.append((ids[i], ids[j], L))
pares.sort(key=lambda x: -x[2])
print("== Pares con mayor bloque contiguo de valores comunes (>=3) ==")
for a, b, L in pares[:20]:
    print(f"   {a:>14} - {b:<14} LCCS={L}")
pd.DataFrame(pares, columns=["A", "B", "LCCS"]).to_csv(OUT / "lccs_pares.csv", index=False)

# --- k-mers de valor, excluyendo el duplicado AS125/UR247 ---
def kmers(s, klen):
    out = set(); run = []
    for x in s:
        if x is None:
            run = []
        else:
            run.append(x)
            if len(run) >= klen:
                out.add(tuple(run[-klen:]))
    return out

def stat(seqs, klen):
    prop = defaultdict(set)
    for k, s in seqs.items():
        for km in kmers(s, klen):
            prop[km].add(k)
    tipos = sum(1 for v in prop.values() if len(v) >= 2)
    pares = set()
    for v in prop.values():
        if len(v) >= 2:
            vl = sorted(v)
            for i in range(len(vl)):
                for j in range(i + 1, len(vl)):
                    pares.add((vl[i], vl[j]))
    return tipos, len(pares)

rng = np.random.default_rng(0)
def shuf(s):
    idx = [i for i, x in enumerate(s) if x is not None]
    v = [s[i] for i in idx]; rng.shuffle(v)
    s2 = list(s)
    for i, x in zip(idx, v): s2[i] = x
    return s2

sin = {k: s for k, s in seq.items() if k not in ("AS125", "UR247")}
print("\n== k-mers de valor SIN AS125/UR247 ==")
for klen in (3, 4, 5):
    ot, op = stat(sin, klen)
    nt = []; npr = []
    for _ in range(NPERM):
        sh = {k: shuf(s) for k, s in sin.items()}
        t, p = stat(sh, klen); nt.append(t); npr.append(p)
    nt = np.array(nt); npr = np.array(npr)
    pt = (1 + np.sum(nt >= ot)) / (1 + NPERM)
    pp = (1 + np.sum(npr >= op)) / (1 + NPERM)
    print(f"k={klen}: obs tipos={ot} pares={op} | nulo tipos={nt.mean():.1f}+-{nt.std():.1f} pares={npr.mean():.1f} | p_t={pt:.3f} p_p={pp:.3f}")
