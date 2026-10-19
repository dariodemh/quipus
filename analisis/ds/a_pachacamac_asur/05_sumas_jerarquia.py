# -*- coding: utf-8 -*-
"""05 - Sumas y jerarquia: totales cruzados con nulo cross-quipu; auto-sumas; grupos."""
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

RAIZ = Path(r".")
DAT = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).parent
OUT = AQUI / "salida"
NPERM = 2000

q = pd.read_csv(DAT / "quipus.csv")
c = pd.read_csv(DAT / "cuerdas.csv")
g = pd.read_csv(DAT / "grupos.csv")
m = q["procedencia"].astype(str).str.lower().str.contains("pachacamac")
ids = sorted(q[m & q["kfg"].str.startswith(("AS", "UR"))]["kfg"].tolist())
cc = c[c["kfg"].isin(ids)].copy()
gg = g[g["kfg"].isin(ids)].copy()

def vr(v, n):
    if pd.isna(v): return np.nan
    if v == 0 and (pd.isna(n) or str(n).strip() == ""): return np.nan
    return float(v)

cc["vreal"] = [vr(r["valor"], r["nudos"]) for _, r in cc.iterrows()]
pen = {k: cc[(cc["kfg"] == k) & (cc["nivel"] == 0)].sort_values("orden")["vreal"].tolist() for k in ids}
tot = {k: float(np.nansum(pen[k])) for k in ids}
valset = {k: set(np.round([x for x in pen[k] if not np.isnan(x)], 6)) for k in ids}

# sumas de grupo (suma de vreal de las cuerdas del grupo)
gsum = {}
for k in ids:
    s = {}
    for gr, rows in cc[cc["kfg"] == k].groupby("grupo"):
        v = [x for x in rows["vreal"] if not np.isnan(x)]
        if v:
            s[gr] = round(float(sum(v)), 6)
    gsum[k] = set(s.values())

# --- Observado: total(A) en valset(B) y en gsum(B); excluir duplicado ---
def cuenta(Vset):
    hits = []
    for A in ids:
        for B in ids:
            if A == B: continue
            if round(tot[A], 6) in Vset[B]:
                hits.append((A, B, tot[A]))
    return hits

h_val = cuenta(valset)
h_gs = cuenta(gsum)
print("Total(A) aparece como VALOR en B (obs):", len(h_val))
print("Total(A) aparece como SUMA DE GRUPO en B (obs):", len(h_gs))
# sin duplicado
h_val2 = [x for x in h_val if "AS125" not in x[:2] and "UR247" not in x[:2]]
h_gs2 = [x for x in h_gs if "AS125" not in x[:2] and "UR247" not in x[:2]]
print("  sin AS125/UR247:", len(h_val2), "y", len(h_gs2))

# --- Nulo cross-quipu: reasignar valores entre quipus preservando tamanos ---
rng = np.random.default_rng(0)
pool = [x for k in ids for x in pen[k] if not np.isnan(x)]
sizes = {k: int(np.sum(~np.isnan(pen[k]))) for k in ids}
# tambien necesito el patron de huecos para reconstruir gsum: simplifico -> cada quipu recibe
# 'size[k]' valores del pool, en orden arbitrario (equivalente para valset)
def null_val(rep=NPERM):
    out = []
    for _ in range(rep):
        rng.shuffle(pool)
        # reasignar
        i = 0; newval = {}
        for k in ids:
            newval[k] = set(np.round(pool[i:i + sizes[k]], 6)); i += sizes[k]
        o = 0
        for A in ids:
            if A in ('AS125', 'UR247'): continue
            ta = tot[A]
            for B in ids:
                if A == B or B in ('AS125', 'UR247'): continue
                if round(ta, 6) in newval[B]:
                    o += 1
        out.append(o)
    return np.array(out)

# total(A) no cambia (depende de pen[A]); el valset de B si cambia. Uso obs sin duplicado como referencia.
# Pero el nulo tambien reasigna los valores que forman los totales de A -> inconsistente.
# Alternativa correcta: fijar pen[A] (totales) y reasignar SOLO los valores de B.
def null_val_fijoB(rep=NPERM):
    out = []
    for _ in range(rep):
        sh = {k: rng.permutation([x for x in pen[k] if not np.isnan(x)]) for k in ids}
        newset = {k: set(np.round(sh[k], 6)) for k in ids}
        o = 0
        for A in ids:
            if A in ('AS125','UR247'): continue
            ta = tot[A]
            for B in ids:
                if A == B or B in ('AS125','UR247'): continue
                if round(ta, 6) in newset[B]:
                    o += 1
        out.append(o)
    return np.array(out)

# permutation within B preserves B's value multiset -> valset unchanged -> test trivial!
print("\nNota: permutar valores dentro de B NO cambia el conjunto de valores de B,")
print("por lo que 'total(A) como valor de B' es invariante al nulo prescrito (no testable asi).")
print("Uso un nulo de reasignacion de valores ENTRE quipus (destruye que valor va en que quipu):")
nv = null_val(rep=500)
p = (1 + np.sum(nv >= len(h_val2))) / (1 + 500)
print(f"  nulo cross-quipu valset: media={nv.mean():.1f} sd={nv.std():.1f} max={nv.max()} | obs={len(h_val2)} p={p:.3f}")

# --- Auto-sumas: hay una cuerda cuyo valor = total del quipu? y grupo: 1a cuerda = suma del grupo ---
print("\n== Auto-sumas intra-quipu ==")
auto_tot = []
for k in ids:
    t = tot[k]
    if t <= 0: continue
    if any(abs(x - t) < 1e-9 for x in pen[k] if not np.isnan(x)):
        auto_tot.append(k)
print("Quipus con un colgante = suma total de colgantes:", auto_tot)

autog = 0; gdet = []
for k in ids:
    for gr, rows in cc[cc["kfg"] == k].groupby("grupo"):
        r = rows.sort_values("orden")
        v = [x for x in r["vreal"] if not np.isnan(x)]
        if len(v) >= 2 and abs(v[0] - sum(v[1:])) < 1e-9:
            autog += 1; gdet.append((k, gr))
print("Grupos donde la 1a cuerda = suma de las demas:", autog, gdet[:12])

# madre = suma de hijas (ya en 01), aqui recontamos global
hijas = defaultdict(list)
for _, r in cc.iterrows():
    if isinstance(r["padre"], str) and r["padre"] == r["padre"]:
        hijas[(r["kfg"], r["padre"])].append(r["vreal"])
sm = 0
for (k, madre), vs in hijas.items():
    vs = [x for x in vs if not np.isnan(x)]
    mr = cc[(cc["kfg"] == k) & (cc["cuerda"] == madre)]["vreal"]
    if len(mr) == 0 or np.isnan(mr.iloc[0]) or not vs: continue
    if abs(sum(vs) - mr.iloc[0]) < 1e-9:
        sm += 1
print("Cuerdas madre = suma de hijas directas (todo el conjunto):", sm)

pd.DataFrame(h_val, columns=["A", "B", "total_A"]).to_csv(OUT / "total_como_valor.csv", index=False)
pd.DataFrame(h_gs, columns=["A", "B", "total_A"]).to_csv(OUT / "total_como_grupo.csv", index=False)
print("\nEjemplos total(A) como SUMA DE GRUPO en B:")
for A, B, t in h_gs[:15]:
    print(f"   tot({A})={t:.0f} = suma de un grupo de {B}")
