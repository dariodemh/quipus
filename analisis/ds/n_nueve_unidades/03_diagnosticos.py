"""03. Diagnósticos, estabilidad y replicación en UR270.

Contenido:
  (1) Perfil de las 9 columnas: ¿ordenado por tamaño? tendencia con signo, índice de monotonía.
  (2) Pares: las 36 correlaciones con nulo C y BH; ¿hay 4 pares o un solo par fuerte?
  (3) Estabilidad del "mejor emparejamiento": bootstrap de filas y fases antes/después del grupo 15.
  (4) Igualdades: por par; ¿la adyacencia explica los empates más allá del tamaño de columna?
  (5) UR270: replicación del perfil (nulo de etiquetas), cociente A/(A+B) por columna.
  (6) PCA/clr y explicación aburrida (largo de cuerda).
  (7) Fases y robustez con 26 filas.
Salida: salida_03.txt, pares_36.csv, bootstrap_pares.csv, fases.csv, ur270_pruebas.csv.
"""
import itertools
import json
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import rankdata, spearmanr, pearsonr
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
rng = np.random.default_rng(20261019)
COLS = [f"c{i}" for i in range(1, 10)]
PAIRS = [(i, j) for i in range(9) for j in range(i + 1, 9)]
LOG = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def clr(X):
    Y = np.log(X)
    return Y - Y.mean(1, keepdims=True)


def perfil(X):
    return clr(X).mean(0)


# ---------- emparejamientos únicos (945)
def _emp():
    seen, E = set(), []
    for f in range(9):
        idx = [i for i in range(9) if i != f]
        for a in itertools.combinations(idx, 2):
            r1 = [i for i in idx if i not in a]
            for b in itertools.combinations(r1, 2):
                r2 = [i for i in r1 if i not in b]
                for c in itertools.combinations(r2, 2):
                    d = tuple(i for i in r2 if i not in c)
                    k = tuple(sorted([a, b, c, d]))
                    if k not in seen:
                        seen.add(k)
                        E.append((f, a, b, c, d))
    return E


EMP = _emp()
assert len(EMP) == 945
E0 = np.array([[m[k][0] for m in EMP] for k in range(1, 5)]).T
E1 = np.array([[m[k][1] for m in EMP] for k in range(1, 5)]).T
PAIR_SUM = {frozenset(p): i for i, p in enumerate(PAIRS)}


def corr(X):
    Z = clr(X)
    return np.corrcoef(Z.T)


def best_pair(R, modo="signed"):
    q = R[E0, E1]                     # (945,4)
    v = np.abs(q).mean(1) if modo == "abs" else q.mean(1)
    k = int(v.argmax())
    return float(v[k]), EMP[k], v


def nulo_etiquetas_perfil(p, stat, B=362880):
    """Nulo de etiquetas exacto para estadísticos del perfil (9 columnas)."""
    perms = np.array(list(itertools.permutations(range(9))), dtype=np.int8)
    vals = np.empty(len(perms))
    CH = 40000
    for s in range(0, len(perms), CH):
        Q = perms[s:s + CH]
        pq = p[Q]
        if stat == "monotonia":
            vals[s:s + CH] = _mono_vec(pq)
        elif stat == "extrema":
            S = np.sign(np.diff(pq, axis=1))
            vals[s:s + CH] = (S[:, 1:] != S[:, :-1]).sum(1)
    return vals


def _mono_vec(P):
    n = P.shape[1]
    idx = np.triu_indices(n, 1)
    return (P[:, idx[0]] > P[:, idx[1]]).mean(1)


def main():
    T = pd.read_csv(AQUI / "ur278_24.csv")
    X = T[COLS].to_numpy(float)
    g = T.grupo.to_numpy()
    p = perfil(X)
    Y = np.log(X)

    # ---------- (1) perfil
    rho, prho = spearmanr(p, np.arange(1, 10))
    mono = (p[[i for i, j in PAIRS]] > p[[j for i, j in PAIRS]]).mean()
    nulm = nulo_etiquetas_perfil(p, "monotonia")
    pm = (np.sum(nulm >= mono) + 1) / (len(nulm) + 1)
    out("== (1) PERFIL DE LAS 9 COLUMNAS (medias de log-razón, clr)")
    out("  perfil:", np.round(p, 3).tolist())
    out(f"  Spearman(perfil, posición) = {rho:.3f} (p dos colas {prho:.4f})")
    out(f"  monotonía (pares i<j con p_i>p_j) = {mono:.3f}; nulo etiquetas {nulm.mean():.3f}; p = {pm:.4g}")
    out("  interpretación: valores decrecientes de la 1-2 a la 8-9, con repuntes locales.")

    # ---------- (2) pares
    R = corr(X)
    obs = np.array([R[i, j] for i, j in PAIRS])
    B = 20000
    nul = np.empty((B, 36))
    for b in range(B):
        Yp = np.column_stack([rng.permutation(Y[:, j]) for j in range(9)])
        Rp = np.corrcoef((Yp - Yp.mean(1, keepdims=True)).T)
        nul[b] = [Rp[i, j] for i, j in PAIRS]
    # p a dos colas (nos interesan también los emparejamientos por compensación, r negativa)
    pv = np.array([min(1.0, 2 * min((np.sum(nul[:, k] >= obs[k]) + 1) / (B + 1),
                                    (np.sum(nul[:, k] <= obs[k]) + 1) / (B + 1))) for k in range(36)])
    P = pd.DataFrame({"i": [a + 1 for a, b in PAIRS], "j": [b + 1 for a, b in PAIRS],
                      "r": obs, "p": pv})
    o = np.argsort(P.p.values)
    q = np.empty(36)
    q[o] = np.minimum(1, np.minimum.accumulate((P.p.values[o] * 36 / np.arange(1, 37))[::-1])[::-1])
    P["q_bh"] = q
    P["adyacente"] = [abs(a - b) == 1 for a, b in PAIRS]
    P.sort_values("r", ascending=False).to_csv(AQUI / "pares_36.csv", index=False)
    out("\n== (2) PARES: 36 correlaciones de residuos clr (nulo C, 20 000)")
    out(P.reindex(P.r.abs().sort_values(ascending=False).index).head(10)
        .to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    out("  pares con q<0,05 (dos colas):", int((P.q_bh < 0.05).sum()), "->",
        P[P.q_bh < 0.05].sort_values("r", ascending=False)[["i", "j", "r", "q_bh"]].round(3).values.tolist())

    # ---------- (3) estabilidad del mejor emparejamiento
    vb, mb, _ = best_pair(R, "signed")
    vabs, mabs, _ = best_pair(R, "abs")
    # nulo C del mejor emparejamiento con signo y con |r|
    Bc = 5000
    nuls, nula = np.empty(Bc), np.empty(Bc)
    for b in range(Bc):
        Yp = np.column_stack([rng.permutation(Y[:, j]) for j in range(9)])
        Rp = np.corrcoef((Yp - Yp.mean(1, keepdims=True)).T)
        nuls[b] = best_pair(Rp, "signed")[0]
        nula[b] = best_pair(Rp, "abs")[0]
    ps = (np.sum(nuls >= vb) + 1) / (Bc + 1)
    pa = (np.sum(nula >= vabs) + 1) / (Bc + 1)
    out("\n== (3) MEJOR EMPAREJAMIENTO (máx. sobre 945; nulo C, 5 000)")
    out(f"  con signo: obs {vb:.3f} = {[(a+1,b+1) for a,b in mb[1:]]} (suelta c{mb[0]+1}); "
        f"nulo {nuls.mean():.3f}±{nuls.std():.3f}; p = {ps:.4g}")
    out(f"  con |r|  : obs {vabs:.3f} = {[(a+1,b+1) for a,b in mabs[1:]]} (suelta c{mabs[0]+1}); "
        f"nulo {nula.mean():.3f}±{nula.std():.3f}; p = {pa:.4g}")
    # bootstrap de filas
    cb, cbabs = Counter(), Counter()
    for _ in range(3000):
        i = rng.integers(0, len(X), len(X))
        if len(np.unique(i)) < 6:
            continue
        Rb = corr(X[i])
        cb[tuple(sorted(best_pair(Rb, "signed")[1][1:]))] += 1
        cbabs[tuple(sorted(best_pair(Rb, "abs")[1][1:]))] += 1
    Bp = pd.DataFrame([{"tipo": "signed", "pares": str([(a + 1, b + 1) for a, b in k]), "n": v}
                       for k, v in cb.most_common(8)] +
                      [{"tipo": "abs", "pares": str([(a + 1, b + 1) for a, b in k]), "n": v}
                       for k, v in cbabs.most_common(8)])
    Bp.to_csv(AQUI / "bootstrap_pares.csv", index=False)
    out("  bootstrap (3 000): emparejamientos más frecuentes")
    out(Bp.to_string(index=False))
    out("  frecuencia con que (1,2) aparece en el mejor emparejamiento: %.3f"
        % np.mean([(0, 1) in k for k in cb.elements()]))

    # ---------- (4) igualdades
    ties = np.abs(X[:, :, None] - X[:, None, :]) <= 1
    cnt = np.array([ties[:, i, j].sum() for i, j in PAIRS])
    adj = np.array([abs(i - j) == 1 for i, j in PAIRS])
    out("\n== (4) IGUALDADES |x_i - x_j| <= 1")
    out(f"  total celdas-cola: {cnt.sum()} (adyacentes {cnt[adj].sum()} en {24*8} oportunidades; "
        f"no adyacentes {cnt[~adj].sum()} en {24*28})")
    out("  por par:", [(a + 1, b + 1, int(c)) for (a, b), c in zip(PAIRS, cnt) if c > 0])
    # ¿la adyacencia añade algo tras controlar |Δperfil|?
    dp = np.array([abs(p[i] - p[j]) for i, j in PAIRS])
    Xd = np.column_stack([np.ones(36), dp, adj.astype(float)])
    beta, *_ = np.linalg.lstsq(Xd, cnt.astype(float), rcond=None)
    resid = cnt - Xd @ beta
    se = np.sqrt((resid @ resid) / (36 - 3) * np.diag(np.linalg.pinv(Xd.T @ Xd)))
    out(f"  regresión Poisson-aprox. cnt ~ |Δperfil| + adyacente: beta_ady = {beta[2]:.2f} (SE {se[2]:.2f})")
    # nulo de etiquetas para "adyacentes" (exacto, ya calculado en 02): se recalcula aquí para las fases
    # filas planas
    cvf = X.std(1) / X.mean(1)
    out("  CV por fila (las 6 más planas):", np.round(np.sort(cvf)[:6], 3).tolist(),
        "grupos", T.grupo.to_numpy()[np.argsort(cvf)[:6]].tolist())
    out("  empates por fila:", np.bincount(np.array([np.sum(np.abs(np.diff(r)) <= 1) for r in X]), minlength=9).tolist())

    # ---------- (5) UR270
    U = pd.read_csv(AQUI / "ur270_9.csv")
    XU = U[COLS].to_numpy(float)
    pu = perfil(XU)
    r_rep = np.corrcoef(pu, p)[0, 1]
    # nulo: permutar etiquetas de UR270 (9! exacto, vectorizado)
    perms = np.array(list(itertools.permutations(range(9))), dtype=np.int8)
    PQ = pu[perms]
    PQc = PQ - PQ.mean(1, keepdims=True)
    pc = p - p.mean()
    rr = (PQc @ pc) / np.sqrt((PQc ** 2).sum(1) * (pc @ pc))
    p_rep = (np.sum(rr >= r_rep) + 1) / (len(rr) + 1)
    out("\n== (5) UR270 (6 grupos de 9; 5 de ellos son filas de UR278, no es muestra independiente)")
    out("  perfil UR270:", np.round(pu, 3).tolist())
    out(f"  r(perfil UR270, perfil UR278) = {r_rep:.3f}; nulo de etiquetas {rr.mean():.3f}; p = {p_rep:.4g}")
    RU = corr(XU)
    vu, mu, _ = best_pair(RU, "signed")
    out(f"  mejor emparejamiento UR270: {vu:.3f} = {[(a+1,b+1) for a,b in mu[1:]]} (suelta c{mu[0]+1})")
    out(f"  ¿coincide con UR278? {set(map(frozenset, mu[1:])) == set(map(frozenset, mb[1:]))}")
    # cociente A/(A+B) por columna: estadístico máximo sobre columnas, nulo = permutar columnas dentro de grupo
    A = pd.read_csv(AQUI / "ur270_parts.csv")
    rat = A[[f"ratio_c{j}" for j in range(1, 10)]].to_numpy(float)
    med = rat.mean(0)
    stat_obs = np.max(np.abs(med - med.mean()))
    jmax = int(np.argmax(np.abs(med - med.mean()))) + 1
    Bq = 20000
    nuloq = np.empty(Bq)
    for b in range(Bq):
        Rp = np.array([rng.permutation(r) for r in rat])
        m = Rp.mean(0)
        nuloq[b] = np.max(np.abs(m - m.mean()))
    pq = (np.sum(nuloq >= stat_obs) + 1) / (Bq + 1)
    out(f"  cociente A/(A+B) por columna: {np.round(med,3).tolist()}")
    out(f"  columna más distinta: c{jmax}; estadístico max|media_j - media| = {stat_obs:.3f}; "
        f"nulo {nuloq.mean():.3f}; p = {pq:.4g}")
    pd.DataFrame({"columna": range(1, 10), "ratio_A_sobre_A_mas_B": med,
                  "sd": rat.std(0, ddof=1)}).to_csv(AQUI / "ur270_ratio.csv", index=False)

    # ---------- (6) PCA y largo
    Z = clr(X)
    C = np.cov(Z.T)
    w, v = np.linalg.eigh(C)
    o = np.argsort(w)[::-1]
    w, v = w[o], v[:, o]
    out("\n== (6) PCA de log-razones (clr)")
    out("  varianza explicada:", np.round(w / w.sum(), 3).tolist())
    for k in range(2):
        vv = v[:, k] * np.sign(v[0, k])
        out(f"  PC{k+1}:", np.round(vv, 2).tolist())
    # largo de cuerda por columna (alineado por grupo con las 24 filas)
    import pandas as _pd
    c = _pd.read_csv(AQUI.parents[2] / "analisis" / "datos" / "cuerdas.csv", low_memory=False, keep_default_na=False)
    c["valor"] = _pd.to_numeric(c.valor, errors="coerce").fillna(0).round().astype(int)
    u = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
    Lg = {}
    for gg, x in u.groupby("grupo"):
        if len(x) == 9:
            Lg[gg] = x.largo.to_numpy(float)
    L = np.array([Lg[gg] for gg in g])
    out("  largo medio por columna:", np.round(L.mean(0), 1).tolist(),
        "; r(largo, valor) =", round(spearmanr(L.ravel(), X.ravel()).statistic, 3),
        "; r(largo medio, perfil) =", round(pearsonr(L.mean(0), p).statistic, 3),
        f" (n={len(L)})")

    # ---------- (7) fases y robustez
    filas = []
    for nom, mask in [("fase1_grupos<15", g < 15), ("fase2_grupos>15", g > 15), ("todas_24", np.ones(24, bool))]:
        Xs = X[mask]
        ps_ = perfil(Xs)
        Rs = corr(Xs)
        vs, ms, _ = best_pair(Rs, "signed")
        # nulo C 3000 para el mejor emparejamiento
        nn = np.empty(3000)
        for b in range(3000):
            Yp = np.column_stack([rng.permutation(np.log(Xs)[:, j]) for j in range(9)])
            Rp = np.corrcoef((Yp - Yp.mean(1, keepdims=True)).T)
            nn[b] = best_pair(Rp, "signed")[0]
        pp = (np.sum(nn >= vs) + 1) / 3001
        rho_, _ = spearmanr(ps_, np.arange(1, 10))
        # adyacencia de perfiles
        aa = np.abs(np.diff(ps_)).sum()
        # ties adyacentes
        tt = int(np.sum(np.abs(np.diff(Xs, axis=1)) <= 1))
        filas.append({"conjunto": nom, "n": int(mask.sum()), "rho_perfil_pos": rho_,
                      "adj_abs": aa, "ties_ady": tt,
                      "mejor_par": str([(a + 1, b + 1) for a, b in ms[1:]]) + f"|c{ms[0]+1}",
                      "mejor_par_r": vs, "p_mejor_par": pp})
    # robustez 26 filas
    T26 = pd.read_csv(AQUI / "ur278_26.csv")
    X26 = T26[COLS].to_numpy(float)
    v26, m26, _ = best_pair(corr(X26), "signed")
    filas.append({"conjunto": "robustez_26", "n": 26, "rho_perfil_pos": spearmanr(perfil(X26), np.arange(1, 10)).statistic,
                  "adj_abs": np.abs(np.diff(perfil(X26))).sum(),
                  "ties_ady": int(np.sum(np.abs(np.diff(X26, axis=1)) <= 1)),
                  "mejor_par": str([(a + 1, b + 1) for a, b in m26[1:]]) + f"|c{m26[0]+1}",
                  "mejor_par_r": v26, "p_mejor_par": np.nan})
    F = pd.DataFrame(filas)
    F.to_csv(AQUI / "fases.csv", index=False)
    out("\n== (7) FASES Y ROBUSTEZ")
    out(F.to_string(index=False, float_format=lambda v: f"{v:.3g}"))

    with open(AQUI / "salida_03.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
