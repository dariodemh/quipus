# -*- coding: utf-8 -*-
"""02: Relaciones ENTRE los quipus del norte de Chile.
- secuencias de valores compartidas (runs contiguos)
- totales de un quipu presentes en otro
- estructuras de grupo identicas
- patrones de color
Nulo: barajar valores dentro de cada quipu, 500 veces, semilla 0.
"""
import pandas as pd, numpy as np, os, re, json, itertools

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "a_chile")
c = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "cuerdas.csv"))
g = pd.read_csv(os.path.join(ROOT, "analisis", "datos", "grupos.csv"))
rng = np.random.default_rng(0)

CHILE = ["AS069", "KH0083", "KH0267", "UR058A", "UR084", "UR130",
         "UR131A", "UR131B", "UR131C", "UR132"]

# --- secuencias de valores (colgantes, nivel 0, en orden) ---
seqs = {}
for kfg, grp in c[c.kfg.isin(CHILE)].groupby("kfg"):
    p = grp[grp.nivel == 0].sort_values("orden")
    v = pd.to_numeric(p.valor, errors="coerce")
    # ausentes (0 sin nudos) -> 0 marcador; mantener posiciones
    knots_empty = p.nudos.isna() | (p.nudos.astype(str).str.strip() == "")
    vv = v.copy()
    vv[(vv == 0) & knots_empty] = 0
    vv = vv.fillna(0).astype(int).tolist()
    seqs[kfg] = vv

print("=== longitudes de secuencia de colgantes ===")
for k in CHILE:
    print(f"{k}: {len(seqs[k])} colgantes, valores distintos={len(set(seqs[k]))}")

# --- runs comunes max por par ---
def max_common_run(a, b, minlen=2):
    """longitud del run contiguo comun mas largo (>=minlen), y #runs>=minlen."""
    if not a or not b:
        return 0, 0
    sb = set()
    for L in range(minlen, min(len(b), 12) + 1):
        for i in range(len(b) - L + 1):
            sb.add(tuple(b[i:i + L]))
    best = 0
    count = 0
    # recorre ventanas de a
    for L in range(minlen, min(len(a), 12) + 1):
        for i in range(len(a) - L + 1):
            if tuple(a[i:i + L]) in sb:
                if L > best:
                    best = L
                if L == min(len(a), 12) and i == 0:
                    pass
                count += 1
        # continuar
    return best, count

# mas eficiente: contar ventanas de a que aparecen en b, por longitud
def window_matches(a, b, L):
    if len(a) < L or len(b) < L or L < 2:
        return 0, 0
    sb = {}
    for i in range(len(b) - L + 1):
        sb[tuple(b[i:i + L])] = 1
    hit = sum(1 for i in range(len(a) - L + 1) if tuple(a[i:i + L]) in sb)
    return hit, len(sb)

pairs = list(itertools.combinations(CHILE, 2))
obs = {}
for A, B in pairs:
    d = {}
    for L in (2, 3, 4, 5):
        h, _ = window_matches(seqs[A], seqs[B], L)
        h2, _ = window_matches(seqs[B], seqs[A], L)
        d[L] = h + h2
    # longitud maxima real compartida
    Lmax = 0
    for L in range(2, 13):
        h, _ = window_matches(seqs[A], seqs[B], L)
        if h > 0:
            Lmax = L
        else:
            break
    d["Lmax"] = Lmax
    obs[(A, B)] = d

# --- nulo: barajar valores dentro de cada quipu ---
NITER = 500
null_runs = {p: {2: [], 3: [], 4: [], 5: [], "Lmax": []} for p in pairs}
shuf = {}
for it in range(NITER):
    for k in CHILE:
        arr = seqs[k].copy()
        # barajar solo posiciones no-cero y cero por separado (preserva patron de ausencia)
        nz = [i for i, x in enumerate(arr) if x != 0]
        z = [i for i, x in enumerate(arr) if x == 0]
        vals = [arr[i] for i in nz]
        rng.shuffle(vals)
        new = arr.copy()
        for i, v in zip(nz, vals):
            new[i] = v
        shuf[k] = new
    for (A, B) in pairs:
        for L in (2, 3, 4, 5):
            h, _ = window_matches(shuf[A], shuf[B], L)
            h2, _ = window_matches(shuf[B], shuf[A], L)
            null_runs[(A, B)][L].append(h + h2)
        Lm = 0
        for L in range(2, 13):
            h, _ = window_matches(shuf[A], shuf[B], L)
            if h > 0:
                Lm = L
            else:
                break
        null_runs[(A, B)]["Lmax"].append(Lm)

# p-valores para L=4 y Lmax
rows = []
for (A, B) in pairs:
    o = obs[(A, B)]
    row = dict(A=A, B=B, L2=o[2], L3=o[3], L4=o[4], Lmax=o["Lmax"])
    for L in (3, 4, 5):
        nl = np.array(null_runs[(A, B)][L])
        row[f"p_L{L}"] = (np.sum(nl >= o[L]) + 1) / (NITER + 1)
    nl = np.array(null_runs[(A, B)]["Lmax"])
    row["p_Lmax"] = (np.sum(nl >= o["Lmax"]) + 1) / (NITER + 1)
    row["null_Lmax_mean"] = round(float(nl.mean()), 2)
    rows.append(row)
R = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.max_columns", 40)
print("\n=== runs compartidos por par (top por L3/L4) ===")
print(R.sort_values(["L4", "L3"], ascending=False).head(45).to_string(index=False))
R.to_csv(os.path.join(OUT, "pares_runs.csv"), index=False)

# correccion Holm sobre p_Lmax y p_L4
def holm(p):
    p = np.asarray(p, float)
    n = len(p)
    order = np.argsort(p)
    adj = np.empty(n)
    prev = 0.0
    for rank, idx in enumerate(order):
        val = min(1.0, (n - rank) * p[idx])
        prev = max(prev, val)
        adj[idx] = prev
    return adj

R["p_Lmax_holm"] = holm(R["p_Lmax"].values)
R["p_L4_holm"] = holm(R["p_L4"].values)
print("\n=== significativos tras Holm (p<0.05) ===")
sig = R[(R.p_Lmax_holm < 0.05) | (R.p_L4_holm < 0.05)]
print(sig[["A", "B", "L3", "L4", "Lmax", "p_L4", "p_L4_holm", "p_Lmax", "p_Lmax_holm", "null_Lmax_mean"]].to_string(index=False))
R.to_csv(os.path.join(OUT, "pares_runs.csv"), index=False)
