"""Controles de las reglas entre quipus:
   1) placebo: la MISMA maquinaria de offset sobre parejas de procedencia distinta y tamano similar;
   2) duplicados/copias literales: parejas con >=8 predicciones y >=75 % de valores identicos;
   3) suma_dos por quipu.
"""
import pickle
import numpy as np, pandas as pd
from pathlib import Path
from motor import cargar

A = Path(__file__).resolve().parent
rng = np.random.default_rng(20261018)
MIN_PAR, FR = 3, 0.6

c, q = cargar()
proc = q.set_index("kfg").procedencia.fillna("Unknown").to_dict()
l0 = c[c.nivel == 0]
seq, grupos = {}, {}
for k, d in l0.groupby("kfg", sort=True):
    sub = d.reset_index(drop=True)
    seq[k] = sub.vi.to_numpy(float)
    grupos[k] = [(dd.index.to_numpy(), dd.vi.to_numpy(float)) for _, dd in sub.groupby("grupo", sort=True)]
SV = {k: np.where(np.isnan(v), -1.0, v) for k, v in seq.items()}


def cuentas(X, Y):
    n, m = len(X), len(Y)
    out = {}
    for d in range(-(min(n, m) - 5), min(n, m) - 4):
        if d >= 0:
            L = min(n - d, m - d); a, b = X[:L], Y[d:d + L]
        else:
            L = min(n + d, m); a, b = X[-d:-d + L], Y[:L]
        out[d] = int(np.sum((a == b) & (a >= 0)))
    return out


def copia_quipu(a, b):
    X, Y = SV[a], SV[b]
    n, m = len(X), len(Y)
    K = max(5, int(0.4 * min(n, m)))
    out = []
    for (P, Q, d0, s0) in ((X, Y, None, None),):
        pass
    ca = cuentas(X, Y)
    o = sorted(ca.items(), key=lambda z: -z[1])
    if o and o[0][1] >= K and (len(o) == 1 or o[1][1] < o[0][1]):
        d0, s0 = o[0]
        for i in range(n):
            j = i + d0
            if 0 <= j < m and X[i] >= 0 and Y[j] >= 0 and s0 - (X[i] == Y[j]) >= K:
                out.append((i, j, abs(int(X[i] - Y[j])) < 0.5))
    cb = cuentas(Y, X)
    o = sorted(cb.items(), key=lambda z: -z[1])
    if o and o[0][1] >= K and (len(o) == 1 or o[1][1] < o[0][1]):
        d0, s0 = o[0]
        for j in range(m):
            i = j + d0
            if 0 <= i < n and Y[j] >= 0 and X[i] >= 0 and s0 - (Y[j] == X[i]) >= K:
                out.append((j, i, abs(int(Y[j] - X[i])) < 0.5))
    return out


def copia_grupo(a, b):
    out = []
    for pa, va in grupos[a]:
        if len(va) < 3:
            continue
        for pb, vb in grupos[b]:
            if len(vb) < 3 or abs(len(va) - len(vb)) > 1:
                continue
            for e in range(-2, 3):
                idx = [(k, k + e) for k in range(len(va)) if 0 <= k + e < len(vb)]
                if len(idx) < MIN_PAR:
                    continue
                ok = sum(1 for k, l in idx if va[k] == vb[l] and not np.isnan(va[k]))
                if ok < MIN_PAR or ok / len(idx) < FR:
                    continue
                for k, l in idx:
                    if np.isnan(va[k]) or np.isnan(vb[l]):
                        continue
                    s = ok - (1 if va[k] == vb[l] else 0)
                    if s >= MIN_PAR and s / (len(idx) - 1) >= FR:
                        out.append((pa[k], pb[l], bool(va[k] == vb[l])))
    return out


O = pd.read_csv(A / "inter_pred.csv")
usados = sorted(set(O[O.regla != "suma_dos"].kfg) | set(O[O.regla != "suma_dos"].otro))
print("placebo para %d quipus con predicciones entre quipus" % len(usados))
filas = []
for k in usados:
    otros = [o for o in seq if proc.get(o) != proc.get(k) and not proc.get(o, "Unknown").startswith("Unknown")
             and 0.7 <= len(seq[o]) / len(seq[k]) <= 1.4]
    if not otros:
        continue
    for o in rng.choice(otros, min(4, len(otros)), replace=False):
        for i, j, h in copia_quipu(k, o):
            filas.append(dict(kfg=k, otro=o, regla="copia_quipu", hit=h))
        for i, j, h in copia_grupo(k, o):
            filas.append(dict(kfg=k, otro=o, regla="copia_grupo", hit=h))
P = pd.DataFrame(filas)
print("\n=== PLACEBO entre procedencias distintas (mismos umbrales) ===")
if len(P):
    print(P.groupby("regla").hit.agg(["size", "mean"]).round(3).to_string())
    print("total %d predicciones, %.3f exactas (real: 323, 0.656)" % (len(P), P.hit.mean()))
else:
    print("0 predicciones: la regla no dispara entre quipus no emparentados")

# ---------------------------------------------------------------- duplicados
pares = []
for (a, b), d in O[O.regla == "copia_quipu"].groupby(["kfg", "otro"]):
    if a < b:
        pares.append(dict(a=a, b=b, n=len(d), hit=int(d.hit.sum()), fr=d.hit.mean()))
P2 = pd.DataFrame(pares)
P2["duplicado"] = (P2.n >= 8) & (P2.fr >= 0.75)
print("\n=== parejas de copia de quipu completo ===")
print(P2.round(3).to_string(index=False))
print("quipus implicados en copias literales:", len(set(P2[P2.duplicado].a) | set(P2[P2.duplicado].b)))
P2.to_csv(A / "pares_copia.csv", index=False)

# ---------------------------------------------------------------- suma_dos
S = O[O.regla == "suma_dos"]
print("\n=== suma_dos ===")
if len(S):
    print(S.groupby("kfg").agg(n=("hit", "size"), hit=("hit", "sum")).round(3).to_string())
    print("total %d predicciones, %d exactas (%.3f)" % (len(S), S.hit.sum(), S.hit.mean()))
