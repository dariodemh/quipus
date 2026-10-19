"""Refinamiento de D2 y D3: segunda etapa con 5000 replicas para los pares con p<=0.01.

Motivo: con 1000 replicas el p minimo es 0,001 y, tras BH sobre decenas de miles de pares,
ningun q puede bajar de 0,05. Se aplica la misma estrategia que 13_sistema_incahuasi:
criba con 1000 y refinamiento a 5000 en los candidatos.

Salidas: enlaces_d2.csv, enlaces_d3.csv (con q global, q por familia y top3 de destinos).
"""
import numpy as np
import pandas as pd
from numba import njit
import comun as C
import d2_parejas_suma as D2
import d3_cadenas as D3

NP = 5000
SEED = C.SEMILLA + 22
rng = np.random.default_rng(SEED)


def d2():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    X = {k: np.array([r["x"] for r in v], dtype=np.int64)
         for k, v in R.items() if len(v) >= 3 and sum(r["x"] > 0 for r in v) >= 3}
    ks = sorted(X)
    kid = {k: i for i, k in enumerate(ks)}
    fp, fm = C.familias(q)

    def familia(a, b):
        if a in fp and b in fp and fp[a] == fp[b]:
            return "proc:" + str(fp[a][1])
        if a in fm and b in fm and fm[a] == fm[b]:
            return "museo:" + str(fm[a][1])
        return "global"

    grupos = {}
    for k in ks:
        if k in fp:
            grupos.setdefault("proc:" + str(fp[k][1]), []).append(k)
        if k in fm:
            grupos.setdefault("museo:" + str(fm[k][1]), []).append(k)
    tablas = {fam: D2.tabla_cod(X, mem, kid) for fam, mem in grupos.items()}
    Hall, qall, rall = D2.tabla_cod(X, ks, kid)
    excl = {}
    for a, b in C.EXCLUIDOS:
        if a in X and b in X:
            excl.setdefault(a, set()).add(b); excl.setdefault(b, set()).add(a)
    D = pd.read_csv(C.AQUI / "d2_observado.csv")
    cand = D[D.p <= 0.01].copy()
    print(f"D2 candidatos a refinar: {len(cand)}")
    pv = np.ones(len(cand)); nm = np.zeros(len(cand)); nx = np.zeros(len(cand)); top = []
    for pos, (ix, r) in enumerate(cand.iterrows()):
        fam = r.familia
        H, qs, rH = tablas[fam] if fam in tablas else (Hall, qall, rall)
        malos = np.array([kid[x] for x in {r.A, r.B} | excl.get(r.A, set()) | excl.get(r.B, set())], dtype=np.int64)
        keep = ~np.isin(qs, malos)
        H, qs, rH = H[keep], qs[keep], rH[keep]
        xa, xb = X[r.A], X[r.B]
        m = min(len(xa), len(xb))
        va, vb = xa[:m] > 0, xb[:m] > 0
        ok = va & vb
        posb = np.where(vb)[0]
        perm = np.array([rng.permutation(xb[posb]) for _ in range(NP)])
        Smat = np.zeros((NP, m), dtype=np.int64)
        for j, i in enumerate(posb):
            Smat[:, i] = xa[i] + perm[:, j]
        mask = np.zeros_like(Smat, dtype=bool)
        for t in C.TOL:
            w = Smat + t
            j = np.minimum(np.searchsorted(H, w), len(H) - 1)
            mask |= (H[j] == w)
        mask &= ok[None, :]
        nul = mask.sum(1)
        nm[pos], nx[pos] = nul.mean(), nul.max()
        pv[pos] = C.p_emp(r.obs, nul)
        # top3 destinos observados
        s = (xa[:m] + xb[:m])[ok]
        ii2 = np.where(ok)[0]
        fi, cc, rr = D2.match_detalle(s, H, qs, rH)
        if len(cc):
            nq = len(ks)
            key, uidx = np.unique(fi.astype(np.int64) * nq + cc, return_index=True)
            f2, c2 = key // nq, key % nq
            rru = rr[uidx]
            cnt = np.bincount(c2, minlength=nq)
            o = np.argsort(cnt)[::-1][:3]
            top.append("|".join(f"{ks[k]}:{int(cnt[k])}" for k in o))
            best = int(o[0])
            cand.loc[ix, "C"] = ks[best]
            cand.loc[ix, "matches"] = int(cnt[best])
            sel = ii2[f2[c2 == best]]
            rsel = rru[c2 == best]
            orden = np.argsort(sel, kind="stable")
            sel, rsel = sel[orden], rsel[orden]
            _, uix = np.unique(sel, return_index=True)
            cand.loc[ix, "nC"] = len(uix)
            if len(uix) >= 4:
                from scipy.stats import kendalltau
                cand.loc[ix, "tau"] = float(kendalltau(sel[uix], rsel[uix]).statistic)
        else:
            top.append("")
        if (pos + 1) % 200 == 0:
            print("  ", pos + 1)
    cand["nulo_media"] = nm; cand["nulo_max"] = nx; cand["p"] = pv; cand["top3_nombres"] = top
    D["p"] = D.p.fillna(1.0)
    D.loc[cand.index, "p"] = cand.p
    D.loc[cand.index, "nulo_media"] = cand.nulo_media
    D.loc[cand.index, "nulo_max"] = cand.nulo_max
    D["q_global"] = C.bh(D.p)
    D["q_familia"] = np.nan
    for fam, idx in D.groupby("familia").groups.items():
        D.loc[idx, "q_familia"] = C.bh(D.loc[idx, "p"])
    D["exceso"] = D.obs - D.nulo_media
    D.to_csv(C.AQUI / "d2_observado.csv", index=False, float_format="%.4g")
    cand["q_global"] = D.loc[cand.index, "q_global"]
    cand["q_familia"] = D.loc[cand.index, "q_familia"]
    cand["exceso"] = cand.obs - cand.nulo_media
    cand = cand.sort_values(["exceso", "p"], ascending=[False, True])
    cand.to_csv(C.AQUI / "enlaces_d2.csv", index=False, float_format="%.4g")
    cols = ["A", "B", "n", "obs", "obs_exacto", "C", "top3_nombres", "nC", "tau", "nulo_media", "exceso", "p", "q_global", "q_familia", "familia"]
    print(cand.head(30)[cols].to_string(index=False))
    print("\nCONTROL:")
    print(cand[(cand.A.isin(["UR273A", "UR273B"])) & (cand.B.isin(["UR273A", "UR273B"]))][cols].to_string(index=False))


def d3():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    tot, cab = {}, {}
    for k, recs in R.items():
        if len(recs) < 3:
            continue
        t = [int(np.sum(r["pend"])) for r in recs if len(r["pend"]) > 0]
        h = [r["x"] for r in recs if r["x"] > 0]
        if len(t) >= 3 and len(h) >= 3:
            tot[k] = np.array(t, dtype=np.int64); cab[k] = np.array(h, dtype=np.int64)
    D = pd.read_csv(C.AQUI / "d3_cadenas.csv")
    cand = D[D.p <= 0.01].copy()
    print(f"\nD3 candidatos a refinar: {len(cand)}")
    pv = np.ones(len(cand)); nm = np.zeros(len(cand)); nx = np.zeros(len(cand))
    for pos, (ix, r) in enumerate(cand.iterrows()):
        nul = D3.lcs_nulo(tot[r.A], cab[r.B], NP, int(SEED + pos))
        nm[pos], nx[pos] = nul.mean(), nul.max()
        pv[pos] = (np.sum(nul >= r.lcs) + 1) / (NP + 1)
    cand["nulo_media"] = nm; cand["nulo_max"] = nx; cand["p"] = pv
    D["p"] = D.p.fillna(1.0)
    D.loc[cand.index, "p"] = cand.p
    D.loc[cand.index, "nulo_media"] = cand.nulo_media
    D.loc[cand.index, "nulo_max"] = cand.nulo_max
    D["q"] = C.bh(D.p)
    D["q_familia"] = np.nan
    for fam, idx in D.groupby("familia").groups.items():
        D.loc[idx, "q_familia"] = C.bh(D.loc[idx, "p"])
    D["exceso"] = D.lcs - D.nulo_media
    D.to_csv(C.AQUI / "d3_cadenas.csv", index=False, float_format="%.4g")
    cand["q"] = D.loc[cand.index, "q"]
    cand["q_familia"] = D.loc[cand.index, "q_familia"]
    cand["exceso"] = cand.lcs - cand.nulo_media
    cand = cand.sort_values(["exceso", "p"], ascending=[False, True])
    cand.to_csv(C.AQUI / "enlaces_d3.csv", index=False, float_format="%.4g")
    print(cand.head(25).to_string(index=False))
    print("\nCONTROLES:")
    print(cand[(cand.A == "UR278") & (cand.B.isin(["UR266", "UR275"]))].to_string(index=False))


if __name__ == "__main__":
    d2()
    d3()
