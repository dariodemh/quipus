"""Reglas ENTRE quipus de la misma procedencia: copia (quipu completo o grupo) y suma de dos registros.

Se abandona el alineamiento LCS con ancla en la propia cuerda: se comprobo que la pareja del
alineamiento completo desaparece al enmascarar el valor en 238/300 casos, es decir, la ancla se
eligio mirando el valor oculto (fuga). En su lugar se usa un modelo de OFFSET, que no mira el
valor objetivo:

  copia_quipu   la secuencia de colgantes de X es la de Y desplazada un offset d constante.
                d y su recuento se estiman leave-one-out (>=K aciertos con las demas cuerdas).
  copia_grupo   dentro de un grupo, X[g,k] = Y[h,k+e] con offset local e estimado leave-one-out
                (>=3 posiciones comparadas y >=60 % de acuerdo, sin contar la cuerda objetivo).
  suma_dos      X[i] = A[i+dA] + B[i+dB] con offsets globales y >=2 posiciones vecinas que ya
                cumplen la suma (>=60 %); la puerta se recalcula en cada permutacion.

Salida: inter_pred.csv, inter_resumen.csv, inter_estructura.pkl
"""
import pickle, time
from pathlib import Path
import numpy as np
import pandas as pd
from motor import cargar

AQUI = Path(__file__).resolve().parent
SEED = 20261018
NPERM = 300
MIN_PAR = 3
FR = 0.6


def main():
    c, q = cargar()
    proc = q.set_index("kfg").procedencia.fillna("Unknown").to_dict()
    l0 = c[c.nivel == 0]
    seq, name, grupos = {}, {}, {}
    for k, d in l0.groupby("kfg", sort=True):
        sub = d.reset_index(drop=True)
        seq[k] = sub.vi.to_numpy(float)
        name[k] = sub.cuerda.to_numpy()
        G = []
        for g, dd in sub.groupby("grupo", sort=True):
            G.append((dd.index.to_numpy(), dd.vi.to_numpy(float)))
        grupos[k] = G
    byp = {}
    for k in seq:
        byp.setdefault(proc.get(k, "Unknown"), []).append(k)
    pares = []
    for p, L in byp.items():
        if p == "Unknown" or p.startswith("Unknown"):
            continue
        for x in sorted(L):
            for y in sorted(L):
                if x < y and len(seq[x]) >= 8 and len(seq[y]) >= 8 and 0.5 <= len(seq[x]) / len(seq[y]) <= 2.5:
                    pares.append((x, y))
    print("pares:", len(pares))

    # valores con centinela -1 para ausentes (nunca iguales entre si)
    SV = {k: np.where(np.isnan(v), -1.0, v) for k, v in seq.items()}

    def cuentas(X, Y):
        """dict d -> nº de posiciones i con X[i]==Y[i+d] (ambas presentes)."""
        n, m = len(X), len(Y)
        out = {}
        for d in range(-(min(n, m) - 5), min(n, m) - 4):
            if d >= 0:
                L = min(n - d, m - d)
                a, b = X[:L], Y[d:d + L]
            else:
                L = min(n + d, m)
                a, b = X[-d:-d + L], Y[:L]
            s = int(np.sum((a == b) & (a >= 0)))
            out[d] = s
        return out

    # ---------------------------------------------------------------- copia de quipu completo
    t0 = time.time()
    pred = []
    off = {}
    for a, b in pares:
        X, Y = SV[a], SV[b]
        n, m = len(X), len(Y)
        K = max(5, int(0.4 * min(n, m)))
        ca = cuentas(X, Y)
        cb = cuentas(Y, X)
        orden = sorted(ca.items(), key=lambda z: -z[1])
        off[(a, b)] = orden[0] if orden else (0, 0)
        if orden and orden[0][1] >= K and (len(orden) == 1 or orden[1][1] < orden[0][1]):
            d0, s0 = orden[0]
            for i in range(n):
                j = i + d0
                if 0 <= j < m and X[i] >= 0 and Y[j] >= 0 and s0 - (X[i] == Y[j]) >= K:
                    pred.append((a, i, "copia_quipu", b, j, abs(d0), s0 - (X[i] == Y[j])))
        orden = sorted(cb.items(), key=lambda z: -z[1])
        off[(b, a)] = orden[0] if orden else (0, 0)
        if orden and orden[0][1] >= K and (len(orden) == 1 or orden[1][1] < orden[0][1]):
            d0, s0 = orden[0]
            for j in range(m):
                i = j + d0
                if 0 <= i < n and Y[j] >= 0 and X[i] >= 0 and s0 - (Y[j] == X[i]) >= K:
                    pred.append((b, j, "copia_quipu", a, i, abs(d0), s0 - (Y[j] == X[i])))
    print("copia_quipu: %d predicciones (%.0f s)" % (len(pred), time.time() - t0))

    # ---------------------------------------------------------------- copia de grupo
    t0 = time.time()
    ng = 0
    for a, b in pares:
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
                        n2 = len(idx) - 1
                        if s >= MIN_PAR and s / n2 >= FR:
                            pred.append((a, pa[k], "copia_grupo", b, pb[l], len(idx), s))
                            ng += 1
    print("copia_grupo: %d predicciones (%.0f s)" % (ng, time.time() - t0))

    P = pd.DataFrame(pred, columns=["kfg", "i", "regla", "otro", "j", "gap", "ev"])
    P = P.drop_duplicates(["kfg", "i", "regla", "otro", "j"]).reset_index(drop=True)
    print("predicciones de copia:", len(P), " quipus:", P.kfg.nunique())
    print(P.groupby("regla").size().to_dict())

    # ---------------------------------------------------------------- suma de dos registros
    t0 = time.time()
    # A y B son un par de copia (offset relativo dAB conocido); se busca X tal que X = A + B
    pares_copia = [(r.kfg, r.otro, r.gap) for r in P[P.regla == "copia_quipu"].itertuples()
                   if r.kfg < r.otro]
    sum2, sum2_ev = [], []
    for A, B, dAB in pares_copia:
        if dAB > 60:
            continue
        pa = proc.get(A)
        for X in [k for k in seq if proc.get(k) == pa and k not in (A, B) and len(seq[k]) >= 8]:
            n, na, nb = len(SV[X]), len(SV[A]), len(SV[B])
            best = None
            for d in range(-(min(n, na) - 5), min(n, na) - 4):
                L = min(n - max(d, 0), na - max(d, 0))
                # X[i] = A[i+d] + B[i+d+dAB]
                cnt = 0; nev = 0
                for i in range(max(0, -d), n):
                    j = i + d
                    if j < 0 or j >= na or j + dAB < 0 or j + dAB >= nb:
                        continue
                    if SV[X][i] < 0 or SV[A][j] < 0 or SV[B][j + dAB] < 0:
                        continue
                    nev += 1
                    cnt += abs(SV[X][i] - (SV[A][j] + SV[B][j + dAB])) <= 1
                if nev >= 5 and cnt >= 2 and cnt / nev >= FR:
                    if best is None or cnt / nev > best[1]:
                        best = (d, cnt / nev, cnt, nev)
            if best is None:
                continue
            d, fr, cnt, nev = best
            pos = [i for i in range(max(0, -d), n) if 0 <= i + d < na and 0 <= i + d + dAB < nb
                   and SV[X][i] >= 0 and SV[A][i + d] >= 0 and SV[B][i + d + dAB] >= 0]
            for i in pos:
                e2 = [k for k in pos if k != i]
                ok2 = sum(1 for k in e2 if abs(SV[X][k] - (SV[A][k + d] + SV[B][k + d + dAB])) <= 1)
                if len(e2) >= 3 and ok2 >= 2 and ok2 / len(e2) >= FR:
                    sum2.append((X, i, A, i + d, B, i + d + dAB, len(e2), ok2))
                    sum2_ev.append(e2)
    S2 = pd.DataFrame(sum2, columns=["kfg", "i", "A", "ja", "B", "jb", "nev", "nok"])
    S2 = S2.drop_duplicates(["kfg", "i", "A", "B"]).reset_index(drop=True)
    evmap = {}
    for t, r in enumerate(pd.DataFrame(sum2, columns=["kfg", "i", "A", "ja", "B", "jb", "nev", "nok"]).itertuples()):
        evmap.setdefault((r.kfg, r.i, r.A, r.B), sum2_ev[t])
    sum2_ev = [evmap[(r.kfg, r.i, r.A, r.B)] for r in S2.itertuples()]
    print("suma_dos: %d predicciones (%.0f s)" % (len(S2), time.time() - t0))

    # ---------------------------------------------------------------- evaluacion
    def evalua(vv, P, S2, gate=True):
        h = np.zeros(len(P) + len(S2), bool)
        for t, r in enumerate(P.itertuples()):
            h[t] = abs(vv[r.kfg][r.i] - vv[r.otro][r.j]) < 0.5
        for t, r in enumerate(S2.itertuples()):
            dA, dB = r.ja - r.i, r.jb - r.i
            if gate:
                ev = sum2_ev[t]
                ok = sum(1 for k in ev if abs(vv[r.kfg][k] - (vv[r.A][k + dA] + vv[r.B][k + dB])) <= 1)
                if not (ok >= 2 and ok / len(ev) >= FR):
                    continue
            h[len(P) + t] = abs(vv[r.kfg][r.i] - (vv[r.A][r.ja] + vv[r.B][r.jb])) < 0.5
        return h

    vv = {k: np.where(np.isnan(v), 0.0, v) for k, v in seq.items()}
    hob = evalua(vv, P, S2)
    print("acierto copia: %d/%d = %.3f" % (hob[:len(P)].sum(), len(P), hob[:len(P)].mean()))
    if len(S2):
        print("acierto suma_dos: %d/%d = %.3f" % (hob[len(P):].sum(), len(S2), hob[len(P):].mean()))
    P = P.assign(hit=hob[:len(P)])
    print(P.groupby("regla").hit.agg(["size", "mean"]).round(3).to_string())

    rng = np.random.default_rng(SEED)
    Hn = []
    for _ in range(NPERM):
        vp = {}
        for k, v in seq.items():
            w = v.copy(); m = ~np.isnan(w); w[m] = rng.permutation(w[m]); vp[k] = np.where(np.isnan(w), 0.0, w)
        Hn.append(evalua(vp, P, S2))
    Hn = np.array(Hn)
    print("nulo copia: %.4f ; nulo suma_dos: %.4f" % (Hn[:, :len(P)].mean(),
          Hn[:, len(P):].mean() if len(S2) else np.nan))

    # ---------------------------------------------------------------- salida
    out = []
    for t, r in enumerate(P.itertuples()):
        out.append(dict(kfg=r.kfg, i=r.i, cuerda=name[r.kfg][r.i], regla=r.regla, otro=r.otro,
                        j=r.j, pred=vv[r.otro][r.j], real=vv[r.kfg][r.i], hit=bool(hob[t]), gap=int(r.gap)))
    for t, r in enumerate(S2.itertuples()):
        out.append(dict(kfg=r.kfg, i=r.i, cuerda=name[r.kfg][r.i], regla="suma_dos",
                        otro=f"{r.A}+{r.B}", j=f"{r.ja},{r.jb}",
                        pred=vv[r.A][r.ja] + vv[r.B][r.jb], real=vv[r.kfg][r.i],
                        hit=bool(hob[len(P) + t]), gap=-1))
    O = pd.DataFrame(out)
    O["procedencia"] = O.kfg.map(proc)
    O.to_csv(AQUI / "inter_pred.csv", index=False)
    O.groupby(["kfg", "regla"]).agg(n=("hit", "size"), hit=("hit", "sum")).reset_index() \
        .to_csv(AQUI / "inter_resumen.csv", index=False)
    print("\npor procedencia:")
    print(O.groupby("procedencia").hit.agg(["size", "mean"]).sort_values("size", ascending=False).head(8).round(3).to_string())
    np.save(AQUI / "inter_hits_nulo.npy", Hn)
    with open(AQUI / "inter_estructura.pkl", "wb") as f:
        pickle.dump(dict(P=P, S2=S2, sum2_ev=sum2_ev, seq=seq, name=name, proc=proc, off=off), f)
    print("\nOK -> inter_pred.csv")


if __name__ == "__main__":
    main()
