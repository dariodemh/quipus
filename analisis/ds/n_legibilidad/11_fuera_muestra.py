"""Prueba fuera de muestra (mitad par / mitad impar) de las reglas entre quipus.

El offset (o el par de grupos y su offset) se estima SOLO con las posiciones pares y se evalua
solo en las impares. Si el acierto se mantiene, la regla no es un artefacto de haber elegido el
offset sobre los mismos datos que luego se evaluan.
"""
import numpy as np, pandas as pd
from pathlib import Path
from motor import cargar

A = Path(__file__).resolve().parent
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

pares = []
L = {}
for p in set(proc.values()):
    K = sorted([k for k in seq if proc.get(k) == p])
    for i, x in enumerate(K):
        for y in K[i + 1:]:
            if len(seq[x]) >= 8 and len(seq[y]) >= 8 and 0.5 <= len(seq[x]) / len(seq[y]) <= 2.5:
                pares.append((x, y))


def cuentas(X, Y, par):
    n, m = len(X), len(Y)
    out = {}
    for d in range(-(min(n, m) - 5), min(n, m) - 4):
        if d >= 0:
            L = min(n - d, m - d); a, b = X[:L], Y[d:d + L]
        else:
            L = min(n + d, m); a, b = X[-d:-d + L], Y[:L]
        idx = np.arange(len(a))
        sel = (idx % 2 == 0) if par else (idx % 2 == 1)
        out[d] = int(np.sum((a[sel] == b[sel]) & (a[sel] >= 0)))
    return out

# ---------------------------------------------------------------- copia_quipu fuera de muestra
res = []
for a, b in pares:
    X, Y = SV[a], SV[b]
    n, m = len(X), len(Y)
    K = max(3, int(0.4 * min(n, m) / 2))  # umbral sobre la mitad de las posiciones
    for (P, Q, flip) in ((X, Y, False), (Y, X, True)):
        ce = cuentas(P, Q, par=True)
        o = sorted(ce.items(), key=lambda z: -z[1])
        if not o or o[0][1] < max(3, int(0.4 * min(len(P), len(Q)) / 2)):
            continue
        if len(o) > 1 and o[1][1] == o[0][1]:
            continue
        d0 = o[0][0]
        nn, mm = len(P), len(Q)
        test = []
        for i in range(nn):
            j = i + d0
            if 0 <= j < mm and P[i] >= 0 and Q[j] >= 0 and i % 2 == 1:
                test.append(abs(P[i] - Q[j]) < 0.5)
        if test:
            res.append((a if not flip else b, b if not flip else a, len(test), sum(test)))
R = pd.DataFrame(res, columns=["kfg", "otro", "n", "hit"])
print("=== copia_quipu: offset estimado en pares, evaluado en impares ===")
if len(R):
    print("predicciones %d ; exactas %d (%.3f) ; quipus %d" % (R.n.sum(), R.hit.sum(), R.hit.sum() / R.n.sum(), R.kfg.nunique()))
    print(R.groupby(["kfg", "otro"]).agg(n=("n", "sum"), hit=("hit", "sum")).round(2).to_string())
else:
    print("sin predicciones fuera de muestra")

# ---------------------------------------------------------------- copia_grupo fuera de muestra
res = []
for a, b in pares:
    for pa, va in grupos[a]:
        if len(va) < 4:
            continue
        for pb, vb in grupos[b]:
            if len(vb) < 3 or abs(len(va) - len(vb)) > 1:
                continue
            for e in range(-2, 3):
                idx = [(k, k + e) for k in range(len(va)) if 0 <= k + e < len(vb)]
                if len(idx) < MIN_PAR + 1:
                    continue
                par = [(k, l) for t, (k, l) in enumerate(idx) if t % 2 == 0]
                imp = [(k, l) for t, (k, l) in enumerate(idx) if t % 2 == 1]
                if not par or not imp:
                    continue
                ok = sum(1 for k, l in par if va[k] == vb[l] and not np.isnan(va[k]))
                if ok / len(par) < FR or ok < 2:
                    continue
                for k, l in imp:
                    if np.isnan(va[k]) or np.isnan(vb[l]):
                        continue
                    res.append((a, b, bool(va[k] == vb[l])))
Rg = pd.DataFrame(res, columns=["kfg", "otro", "hit"])
print("\n=== copia_grupo: grupo y offset elegidos con posiciones pares, evaluados en impares ===")
if len(Rg):
    print("predicciones %d ; exactas %d (%.3f) ; quipus %d" % (len(Rg), Rg.hit.sum(), Rg.hit.mean(), Rg.kfg.nunique()))

# ---------------------------------------------------------------- suma_dos fuera de muestra
# El offset se estima SOLO con posiciones pares y se evalua SOLO en las impares.
O0 = pd.read_csv(A / "inter_pred.csv")
pares_copia = sorted({(r.kfg, r.otro, r.gap) for r in O0[O0.regla == "copia_quipu"].itertuples() if r.kfg < r.otro})
res = []
for A_, B_, dAB in pares_copia:
    if dAB > 60:
        continue
    pa = proc.get(A_)
    for X in [k for k in seq if proc.get(k) == pa and k not in (A_, B_) and len(seq[k]) >= 8]:
        n, na, nb = len(SV[X]), len(SV[A_]), len(SV[B_])
        best = None
        for d in range(-(min(n, na) - 5), min(n, na) - 4):
            cnt = nev = 0
            for i in range(max(0, -d), n):
                j = i + d
                if j < 0 or j >= na or j + dAB < 0 or j + dAB >= nb or i % 2 == 1:
                    continue
                if SV[X][i] < 0 or SV[A_][j] < 0 or SV[B_][j + dAB] < 0:
                    continue
                nev += 1; cnt += abs(SV[X][i] - (SV[A_][j] + SV[B_][j + dAB])) <= 1
            if nev >= 3 and cnt >= 2 and cnt / nev >= FR:
                if best is None or cnt / nev > best[1]:
                    best = (d, cnt / nev)
        if best is None:
            continue
        d = best[0]
        test = [i for i in range(max(0, -d), n) if 0 <= i + d < na and 0 <= i + d + dAB < nb and i % 2 == 1
                and SV[X][i] >= 0 and SV[A_][i + d] >= 0 and SV[B_][i + d + dAB] >= 0]
        if test:
            ok = sum(1 for i in test if abs(SV[X][i] - (SV[A_][i + d] + SV[B_][i + d + dAB])) <= 1)
            res.append((X, len(test), ok))
Rs = pd.DataFrame(res, columns=["kfg", "n", "hit"])
print("\n=== suma_dos: offset elegido con posiciones PARES, evaluado en IMPARES ===")
if len(Rs):
    print("predicciones %d ; exactas %d (%.3f) ; quipus %d"
          % (Rs.n.sum(), Rs.hit.sum(), Rs.hit.sum() / Rs.n.sum(), Rs.kfg.nunique()))
    print(Rs.groupby("kfg").agg(n=("n", "sum"), hit=("hit", "sum")).round(2).to_string())
    print("(en muestra, con el offset elegido sobre todas las posiciones: 12/50 = 0.240)")
else:
    print("0 predicciones fuera de muestra")
