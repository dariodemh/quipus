"""T4. Lecturas concretas con predicción comprobable, y una prueba de corpus que surgió de T1 (columnas gemelas).

Gemelas (exploratorio, post hoc tras ver T1): por quipu, máx. sobre pares de columnas de la fracción de filas
(con ambas celdas >0) en que |vi − vj| <= max(1, 2 % del mayor) y vi != vj o vi == vj. Se reportan dos versiones:
casi-iguales (incluye iguales) y estrictamente casi-iguales (diferencia 1..2 %, excluye idénticos, para separar
copias exactas de dos conteos independientes). Nulo N_col (B=999), BH entre quipus.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import comun as C
from t1_columnas import modas

B = 9999


def cerca(a, b, estricto=False):
    ok = (a > 0) & (b > 0)
    d = np.abs(a - b)
    tol = np.maximum(1, 0.02 * np.maximum(a, b))
    m = ok & (d <= tol)
    if estricto:
        m &= d > 0
    return m, ok


def gemelas(V, estricto=False):
    K = V.shape[1]
    best, arg = 0.0, None
    for i in range(K):
        for j in range(i + 1, K):
            m, ok = cerca(V[:, i], V[:, j], estricto)
            if ok.sum() >= 4 and m.sum() / ok.sum() > best:
                best, arg = m.sum() / ok.sum(), (i, j, int(m.sum()), int(ok.sum()))
    return best, arg


def p_ncol(V, f, rng, B=B, mayor=True):
    obs = f(V)
    nul = [f(C.perm_col(V, rng)) for _ in range(B)]
    return obs, np.nanmean(nul), C.pemp(obs, nul, mayor)


def main():
    M, c, s = C.matrices()
    lin = []
    # ------------------------------------------------ corpus: columnas gemelas
    filas = []
    for i, k in enumerate(sorted(M)):
        V = M[k]["V"]
        if V.shape[1] < 2:
            continue
        rng = np.random.default_rng([C.SEED, 4, i])
        o = {"kfg": k, "R": M[k]["R"], "K": M[k]["K"]}
        for est, nom in ((False, "gem"), (True, "gem_estr")):
            g, arg = gemelas(V, est)
            o[nom], o[nom + "_par"] = g, arg
            if arg is None or g == 0:
                continue
            nul = [gemelas(C.perm_col(V, rng), est)[0] for _ in range(999)]
            o["e_" + nom], o["p_" + nom] = np.mean(nul), C.pemp(g, nul)
        filas.append(o)
    d = pd.DataFrame(filas)
    for nom in ("gem", "gem_estr"):
        d["q_" + nom] = C.bh(d["p_" + nom])
    d.to_csv(C.OUT / "t4_gemelas.csv", index=False)
    for nom, txt in (("gem", "casi iguales (incluye idénticas)"), ("gem_estr", "casi iguales pero no idénticas (dif. 1..2 %)")):
        x = d[d["q_" + nom] < .05]
        lin.append(f"Columnas gemelas, {txt}: evaluables {d['p_' + nom].notna().sum()}, p<0,05 {(d['p_' + nom] < .05).sum()}, "
                   f"q<0,05 {len(x)}: " + ", ".join(f"{r.kfg}{getattr(r, nom + '_par')}" for r in x.itertuples()))
    lin.append("(par = (col i, col j, filas casi iguales, filas con ambas >0))")

    # ------------------------------------------------ L1 Incahuasi: [bruto, c, neto]
    lin.append("\nL1 Incahuasi: fila = lote; col0 = bruto, col1 = cuota fija c, col2 = neto (bruto − c)")
    for k in ["UR255", "UR256", "UR267A", "UR267B", "UR269", "UR275", "UR274B"]:
        if k not in M:
            continue
        V0 = M[k]["V"]
        # columna de la cuota = la de mayor cuota de moda entre las columnas 1 y 2; se reordena a [bruto, c, neto]
        jc = max((1, 2), key=lambda j: modas(V0)[j, 0] if np.isfinite(modas(V0)[j, 0]) else -1)
        orden = [0, jc, 3 - jc]
        V = V0[:, orden]
        W = np.nan_to_num(V)
        comp = (~np.isnan(V)).all(1)
        ok = comp & (np.isclose(W[:, 0], W[:, 1] + W[:, 2]))
        vals, cnt = np.unique(V[:, 1][~np.isnan(V[:, 1])], return_counts=True)
        cc = vals[cnt.argmax()] if len(vals) else np.nan
        # predicción nueva A: filas sin cuota (columna c vacía) -> ¿bruto == neto?
        sin = np.isnan(V[:, 1]) & ~np.isnan(V[:, 0]) & ~np.isnan(V[:, 2])
        # B: filas donde c aparece en otra columna (intercambio de posición)
        c_otra = [(r, orden[int(np.where(V[r] == cc)[0][0])]) for r in range(len(V))
                  if (np.isnan(V[r, 1]) or V[r, 1] != cc) and (V[r] == cc).any()]
        # C: ¿cuota fija o proporcional? CV de c vs CV de c/bruto
        okc = ~np.isnan(V[:, 1]) & ~np.isnan(V[:, 0])
        x1, x0 = V[okc, 1], V[okc, 0]
        cv1, cvr = x1.std() / x1.mean(), (x1 / x0).std() / (x1 / x0).mean()
        # D: ¿bruto > c siempre?
        menor = (V[:, 0] <= cc).sum()
        cols = [pd.Series(M[k]["C"][:, j]).value_counts().head(2).to_dict() for j in orden]
        lin.append(f"  {k}: columna de la cuota = {jc}")
        lin.append(f"  {k}: R={len(V)}, filas completas {comp.sum()}, bruto=c+neto en {ok.sum()} ({ok.sum() / max(comp.sum(), 1):.0%}); "
                   f"c modal={cc:g} ({cnt.max() if len(cnt) else 0} filas); filas sin c con bruto y neto: {sin.sum()} "
                   f"(bruto==neto en {int((V[sin, 0] == V[sin, 2]).sum())}); c en otra columna: {c_otra}; "
                   f"CV(c)={cv1:.2f} vs CV(c/bruto)={cvr:.2f}; filas con bruto<=c: {menor}; colores {cols}")

    # ------------------------------------------------ L2 KH0197: dos columnas casi iguales
    k = "KH0197"
    V = M[k]["V"]
    rng = np.random.default_rng([C.SEED, 41])
    f = lambda X: cerca(X[:, 0], X[:, 1])[0].sum()
    o, e, p = p_ncol(V, f, rng)
    dif = (V[:, 1] - V[:, 0])[~np.isnan(V).any(1)]
    lin.append(f"\nL2 {k}: fila = partida; col0 (W) y col1 (AB) = dos registros de la misma cantidad (asignado/entregado o copia)."
               f"\n  Predicción: |col0−col1| <= max(1, 2 %) en muchas más filas que al azar -> obs {o}, esperado {e:.2f}, p={p:.4f}."
               f"\n  Diferencias col1−col0 por fila: {dif.astype(int).tolist()}")
    d2 = dif[np.abs(dif) <= 2]
    lin.append(f"  Entre casi iguales, signo de la diferencia: {np.sign(d2).astype(int).tolist()}")
    rho = spearmanr(V[:, 0], V[:, 1], nan_policy="omit")[0]
    lin.append(f"  Spearman col0~col1 = {rho:.2f}")

    # ------------------------------------------------ L3 UR011 Leymebamba
    k = "UR011"
    V = M[k]["V"]
    rng = np.random.default_rng([C.SEED, 42])
    L = np.log10(np.where(V > 0, V, np.nan))
    f_sd = lambda X: np.nanstd(np.log10(np.where(X > 0, X, np.nan))[:, 3] - np.log10(np.where(X > 0, X, np.nan))[:, 4])
    o, e, p = p_ncol(V, f_sd, rng, mayor=False)
    r34 = (V[:, 3] / V[:, 4])
    lin.append(f"\nL3 {k} (Leymebamba): fila = unidad (ayllu/pachaca); col3 y col4 = dos conteos grandes del mismo universo"
               f" (p. ej. dos fechas, o dos categorías de tamaño similar)."
               f"\n  P3a razón col3/col4 cercana a 1: mediana {np.nanmedian(r34):.3f}; DE(log10) obs {o:.3f}, nulo {e:.3f}, p={p:.4f}")
    lin.append(f"     razones por fila: {np.round(r34, 2).tolist()}")
    for j in (0, 1, 2):
        f_r = lambda X, j=j: spearmanr(X[:, j], X[:, 3], nan_policy="omit")[0]
        o, e, p = p_ncol(V, f_r, rng, B=1999)
        lin.append(f"  P3b col{j} proporcional al tamaño de la fila (Spearman con col3): {o:.2f} (nulo {e:.2f}), p={p:.4f}")
    # P3c: grupos fuera de tabla = totales por bloque de filas
    cq = c[(c.kfg == k) & (c.nivel == 0)]
    W = np.nan_to_num(V)
    blo = {"filas 0-8": W[:9].sum(0), "filas 9-": W[9:].sum(0), "todas": W.sum(0)}
    fuera = cq[~cq.orden.isin(set(M[k]["O"].ravel())) & (cq.v > 0)]
    lin.append("  P3c totales de columna por bloque: " + "; ".join(f"{n}: {v.astype(int).tolist()}" for n, v in blo.items()))
    hits = [(int(x), n, j) for x in fuera.v for n, v in blo.items() for j in range(V.shape[1]) if x == v[j]]
    cerc = [(int(x), n, j, int(v[j])) for x in fuera.v for n, v in blo.items() for j in range(V.shape[1])
            if v[j] > 100 and abs(x - v[j]) / v[j] < .02 and x != v[j]]
    lin.append(f"     cuerdas fuera de tabla con valor: {len(fuera)}; coincidencias exactas con totales de bloque: {hits}; a <2 %: {cerc}")

    # ------------------------------------------------ L4 UR1144 Pachacamac
    k = "UR1144"
    V = M[k]["V"]
    rng = np.random.default_rng([C.SEED, 43])
    f_r = lambda X: spearmanr(X[:, 0], np.nansum(X[:, 1:], 1), nan_policy="omit")[0]
    o, e, p = p_ncol(V, f_r, rng)
    lin.append(f"\nL4 {k} (Pachacamac): fila = unidad; col0 = bien principal (centenas), col1-3 = bienes menores; "
               f"predicción: el tamaño de la fila arrastra a todas las columnas.\n  Spearman(col0, col1+col2+col3) = {o:.2f} "
               f"(nulo {e:.2f}), p={p:.4f}")
    rat = V[:, 0] / np.nansum(V[:, 1:], 1)
    f_cv = lambda X: np.nanstd(np.log10(X[:, 0] / np.nansum(X[:, 1:], 1)))
    o, e, p = p_ncol(V, f_cv, rng, mayor=False)
    lin.append(f"  ¿col0 = múltiplo fijo del resto? razón mediana {np.nanmedian(rat):.2f}, DE(log10) {o:.3f} vs nulo {e:.3f}, p={p:.4f}")
    lin.append(f"  ¿col0 = suma del resto? filas: {int(np.isclose(V[:, 0], np.nansum(V[:, 1:], 1)).sum())}")

    # ------------------------------------------------ L5 AS178: columnas 1 y 2 gemelas, col0 ≈ 2·col3
    k = "AS178"
    V = M[k]["V"]
    rng = np.random.default_rng([C.SEED, 44])
    f12 = lambda X: cerca(X[:, 1], X[:, 2])[0].sum()
    o, e, p = p_ncol(V, f12, rng)
    lin.append(f"\nL5 {k} (cerca de Lima): fila = unidad; col1 (B) y col2 (LB) = dos mitades iguales de una partida; "
               f"col0 (W) = total/doble de col3 (KB).\n  P5a col1≈col2: obs {o}, esperado {e:.2f}, p={p:.4f}")
    f03 = lambda X: (cerca(X[:, 0], 2 * X[:, 3])[0]).sum()
    o, e, p = p_ncol(V, f03, rng)
    lin.append(f"  P5b col0 ≈ 2·col3: obs {o}, esperado {e:.2f}, p={p:.4f}")
    f0s = lambda X: np.isclose(X[:, 0], X[:, 1] + X[:, 2] + X[:, 3]).sum()
    o, e, p = p_ncol(V, f0s, rng)
    lin.append(f"  P5c col0 = col1+col2+col3: obs {o}, esperado {e:.2f}, p={p:.4f}")
    lin.append("  matriz: " + str(V.tolist()))

    open(C.OUT / "t4_resumen.txt", "w", encoding="utf-8").write("\n".join(lin))
    print("\n".join(lin))


if __name__ == "__main__":
    main()
