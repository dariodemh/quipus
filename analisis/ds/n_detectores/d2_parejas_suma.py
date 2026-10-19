"""D2. Parejas que se suman registro a registro.

A_i + B_i = cabecera de algun registro de un tercer quipu C (exacto y +-1 digito).
Alineacion por indice de registro; los registros sin cabecera (x=0) se conservan como hueco.

Diseno dirigido (leccion Incahuasi): el destino C se busca en el MISMO archivo/coleccion que A y B
(misma procedencia; si no, mismo museo), no en los 466 quipus. Si la pareja no comparte familia,
se usa el corpus entero y se marca 'global' (exploratorio). El estadistico es de union -numero de
registros i cuya suma cae en la cabecera de algun quipu del destino-, que es la lectura literal de
'algun tercer quipu C' y el mismo estadistico que uso 13_sistema_incahuasi (UR266 U UR275 U UR269).
Se anade la atribucion al mejor C, la union de los 3 mejores y tau de Kendall.

Nulo: se permutan las cabeceras no nulas de B entre sus posiciones no nulas (conserva huecos,
magnitudes y multiconjunto; rompe solo el emparejamiento). 1000 replicas.
Solo se prueba en pares con obs>=3; el resto queda p=1 (conservador).
BH por detector sobre TODOS los pares y, ademas, BH dentro de la familia dirigida.

Salidas: d2_observado.csv, enlaces_d2.csv.
"""
import sys
from collections import defaultdict
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
import comun as C

NPERM = 1000
SEED = C.SEMILLA + 2
rng = np.random.default_rng(SEED)


def tabla(X, ks):
    vals, qs, ranks = [], [], []
    for k in ks:
        for i, x in enumerate(X[k]):
            if x > 0:
                vals.append(int(x)); qs.append(k); ranks.append(i)
    vals = np.array(vals, dtype=np.int64)
    o = np.argsort(vals, kind="stable")
    return vals[o], np.array(qs)[o], np.array(ranks)[o]


def tabla_cod(X, ks, kid):
    H, qs, rH = tabla(X, ks)
    return H, np.array([kid[k] for k in qs], dtype=np.int64), rH


def match_union(s, H):
    mask = np.zeros(len(s), dtype=bool)
    for t in C.TOL:
        w = s + t
        j = np.minimum(np.searchsorted(H, w), len(H) - 1)
        mask |= H[j] == w
    return mask


def match_detalle(s, H, qs, rH):
    ii, cc, rr = [], [], []
    for t in C.TOL:
        w = s + t
        lo = np.searchsorted(H, w, "left")
        hi = np.searchsorted(H, w, "right")
        for i in np.where(hi > lo)[0]:
            a, b = lo[i], hi[i]
            ii.append(np.full(b - a, int(i)))
            cc.append(qs[a:b])
            rr.append(rH[a:b])
    if not ii:
        return np.array([], int), np.array([], str), np.array([], int)
    return np.concatenate(ii), np.concatenate(cc), np.concatenate(rr)


def main():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    X = {k: np.array([r["x"] for r in v], dtype=np.int64)
         for k, v in R.items() if len(v) >= 3 and sum(r["x"] > 0 for r in v) >= 3}
    ks = sorted(X)
    fp, fm = C.familias(q)

    def familia(a, b):
        if a in fp and b in fp and fp[a] == fp[b]:
            return "proc:" + str(fp[a][1])
        if a in fm and b in fm and fm[a] == fm[b]:
            return "museo:" + str(fm[a][1])
        return "global"

    # destinos por familia
    grupos = defaultdict(list)
    for k in ks:
        if k in fp:
            grupos["proc:" + str(fp[k][1])].append(k)
        if k in fm:
            grupos["museo:" + str(fm[k][1])].append(k)
    kid = {k: i for i, k in enumerate(ks)}
    tablas = {}
    for fam, members in grupos.items():
        tablas[fam] = tabla_cod(X, members, kid)
    Hall, qall, rall = tabla_cod(X, ks, kid)
    print(f"quipus {len(ks)}; cabeceras {len(Hall)}; familias {len(grupos)}")

    excl = defaultdict(set)
    for a, b in C.EXCLUIDOS:
        if a in X and b in X:
            excl[a].add(b); excl[b].add(a)

    pares = [p for p in C.parejas(X) if not C.excluido(*p)]
    print(f"pares a barrer: {len(pares)}")
    filas = []
    for n, (a, b) in enumerate(pares):
        fam = familia(a, b)
        if fam != "global" and fam in tablas:
            H, qs, rH = tablas[fam]
        else:
            H, qs, rH = Hall, qall, rall
        malos = np.array([kid[x] for x in {a, b} | excl[a] | excl[b]], dtype=np.int64)
        keep = ~np.isin(qs, malos)
        H, qs, rH = H[keep], qs[keep], rH[keep]
        xa, xb = X[a], X[b]
        m = min(len(xa), len(xb))
        va, vb = xa[:m] > 0, xb[:m] > 0
        ok = va & vb
        s = (xa[:m] + xb[:m])[ok]
        ii = np.where(ok)[0]
        if len(H) == 0:
            union = np.zeros(len(s), dtype=bool)
        else:
            union = match_union(s, H)
        obs = int(union.sum())
        ex = int(np.isin(s, H).sum()) if len(H) else 0
        Cb, mt, nC, tau, top3, seg, mt2 = "", 0, 0, np.nan, 0, "", 0
        if obs:
            fi, cc, rr = match_detalle(s, H, qs, rH)
            if len(cc):
                uq, inv = np.unique(cc, return_inverse=True)
                cnt = np.bincount(inv)
                best = int(np.argmax(cnt))
                Cb, mt = ks[uq[best]], int(cnt[best])
                top3 = int(np.sort(cnt)[::-1][:3].sum())
                if len(cnt) > 1:
                    cnt2 = cnt.copy(); cnt2[best] = -1
                    mt2, seg = int(cnt2.max()), ks[uq[int(np.argmax(cnt2))]]
                sel = ii[fi[inv == best]]
                rsel = rr[inv == best]
                o = np.argsort(sel, kind="stable")
                sel, rsel = sel[o], rsel[o]
                _, uix = np.unique(sel, return_index=True)
                sel, rsel = sel[uix], rsel[uix]
                nC = len(sel)
                if nC >= 4:
                    try:
                        tau = float(kendalltau(sel, rsel).statistic)
                    except Exception:
                        tau = np.nan
        filas.append(dict(A=a, B=b, n=int(ok.sum()), obs=obs, obs_exacto=ex, C=Cb, matches=mt,
                          nC=nC, tau=tau, top3=top3, segundo=seg, matches2=mt2, familia=fam))
        if (n + 1) % 20000 == 0:
            print(" ", n + 1, file=sys.stderr)
    D = pd.DataFrame(filas)
    D.to_csv(C.AQUI / "d2_observado.csv", index=False, float_format="%.4g")
    print(D.obs.value_counts().sort_index().head(15).to_string())
    print(f"pares obs>=3: {(D.obs >= 3).sum()}; obs>=4: {(D.obs >= 4).sum()}; obs>=5: {(D.obs >= 5).sum()}")
    print(f"pares con tau=1 y nC>=4: {((D.tau == 1) & (D.nC >= 4)).sum()}")

    cand = D[D.obs >= 3].copy()
    print(f"candidatos a nulo: {len(cand)}")
    pv = np.ones(len(cand)); nm = np.zeros(len(cand)); nx = np.zeros(len(cand))
    for pos, (ix, r) in enumerate(cand.iterrows()):
        fam = r.familia
        if fam != "global" and fam in tablas:
            H, qs, rH = tablas[fam]
        else:
            H, qs, rH = Hall, qall, rall
        malos = np.array([kid[x] for x in {r.A, r.B} | excl[r.A] | excl[r.B]], dtype=np.int64)
        keep = ~np.isin(qs, malos)
        H = H[keep]
        xa, xb = X[r.A], X[r.B]
        m = min(len(xa), len(xb))
        va, vb = xa[:m] > 0, xb[:m] > 0
        ok = va & vb
        posb = np.where(vb)[0]
        perm = np.array([rng.permutation(xb[posb]) for _ in range(NPERM)])
        Smat = np.zeros((NPERM, m), dtype=np.int64)
        for j2, i in enumerate(posb):
            Smat[:, i] = xa[i] + perm[:, j2]
        mask = np.zeros_like(Smat, dtype=bool)
        for t in C.TOL:
            w = Smat + t
            j = np.minimum(np.searchsorted(H, w), len(H) - 1)
            mask |= (H[j] == w)
        mask &= ok[None, :]
        nul = mask.sum(1)
        nm[pos], nx[pos] = nul.mean(), nul.max()
        pv[pos] = C.p_emp(r.obs, nul)
        if (pos + 1) % 5000 == 0:
            print("  nulo", pos + 1, file=sys.stderr)
    cand["nulo_media"] = nm; cand["nulo_max"] = nx; cand["p"] = pv
    D["p"] = 1.0
    D.loc[cand.index, "p"] = cand.p
    D["q_global"] = C.bh(D.p)
    D["q_familia"] = np.nan
    for fam, idx in D.groupby("familia").groups.items():
        D.loc[idx, "q_familia"] = C.bh(D.loc[idx, "p"])
    D.to_csv(C.AQUI / "d2_observado.csv", index=False, float_format="%.4g")
    cand["q_global"] = D.loc[cand.index, "q_global"]
    cand["q_familia"] = D.loc[cand.index, "q_familia"]
    cand = cand.sort_values(["p", "obs"], ascending=[True, False])
    cand.to_csv(C.AQUI / "enlaces_d2.csv", index=False, float_format="%.4g")
    cols = ["A", "B", "n", "obs", "obs_exacto", "C", "matches", "top3", "nC", "tau", "nulo_media", "p", "q_global", "q_familia", "familia"]
    print(cand.head(30)[cols].to_string(index=False))
    ctrl = cand[(cand.A == "UR273A") & (cand.B == "UR273B")]
    print("\nCONTROL UR273A+UR273B:")
    print(ctrl[cols].to_string(index=False))


if __name__ == "__main__":
    main()
