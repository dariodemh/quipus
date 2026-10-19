"""T3. Filas: ¿qué distingue una fila de otra? ¿hay filas/cuerdas resumen? ¿el nº de filas es "típico"?

(a) Nº de filas R (grupos del tamaño modal) en las tablas, nº total de grupos y tamaño modal K en todo el corpus.
    Exceso en valores preregistrados (4, 5, 6, 10, 12) frente a la vecindad (x±2): binomial con p0 = 1/5; Holm.
(b) Cuerdas resumen fuera de la tabla (colgantes de grupos de otro tamaño y cuerdas superiores T):
    ¿= total de una columna (Σ filas), total de una fila o suma de un tramo contiguo (≥2 filas) de una columna?
    Nulo: barajar los valores anudados entre las celdas anudadas de la tabla (B=999).
(c) Filas resumen dentro de la tabla: fila r tal que, en varias columnas, su celda = suma de las demás filas
    (o de las filas anteriores); estadístico = máx. nº de columnas que cumple una misma fila. Nulo N_col.
    Fila = fila_i + fila_j (celda a celda en ≥2/3 de las columnas anudadas). Nulo N_fila.
(d) Filas duplicadas (pares de filas idénticas con ≥2 celdas anudadas), totales y contiguas. Nulo N_col.
(e) Color: ¿lo explica más la fila (bloque) o la columna? MI normalizada.
"""
import numpy as np
import pandas as pd
from scipy.stats import binomtest
import comun as C

B = 999


def exceso(serie, valores, nombre):
    vc = serie.value_counts()
    out = []
    for x in valores:
        win = [vc.get(y, 0) for y in range(x - 2, x + 3)]
        n = sum(win)
        r = binomtest(vc.get(x, 0), n, 1 / 5, alternative="greater") if n else None
        out.append({"variable": nombre, "valor": x, "n_x": vc.get(x, 0), "n_ventana": n,
                    "esperado": n / 5, "p": r.pvalue if r else np.nan})
    return out


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    h = np.empty_like(p)
    h[o] = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    return h


# ------------------------------------------------------------------ (b) cuerdas resumen fuera de tabla
def objetivos(V):
    W = np.nan_to_num(V)
    col = set(W.sum(0)[W.sum(0) > 0])
    fil = set(W.sum(1)[(~np.isnan(V)).sum(1) >= 2])
    cs = np.vstack([np.zeros(W.shape[1]), np.cumsum(W, 0)])
    tramo = set()
    R = W.shape[0]
    for a in range(R):
        for b in range(a + 2, R + 1):
            if b - a < R:
                tramo.update(cs[b] - cs[a])
    tramo.discard(0.0)
    return col, fil, tramo - col


def coincidencias(fuera, V):
    col, fil, tramo = objetivos(V)
    return (sum(x in col for x in fuera), sum(x in fil for x in fuera), sum(x in tramo for x in fuera))


def perm_anudadas(V, rng):
    P = V.copy()
    ok = ~np.isnan(V)
    P[ok] = rng.permutation(V[ok])
    return P


# ------------------------------------------------------------------ (c) filas resumen
def fila_resumen(V):
    W = np.nan_to_num(V)
    resto = W.sum(0, keepdims=True) - W
    ant = np.vstack([np.zeros((1, W.shape[1])), np.cumsum(W, 0)[:-1]])
    a = ((W > 0) & np.isclose(W, resto)).sum(1)
    b = ((W > 0) & np.isclose(W, ant) & (np.arange(len(W))[:, None] >= 2)).sum(1)
    return a.max(), b.max()


def fila_suma(V):
    """nº de filas k que son suma celda a celda de otras dos filas i<j (≥2/3 de las celdas anudadas de k, ≥2)."""
    R = V.shape[0]
    if R > 60:
        return np.nan
    W = np.where(V > 0, V, np.nan)
    S = W[:, None, :] + W[None, :, :]                     # R x R x K
    eq = np.isclose(W[:, None, None, :], S[None])         # k x i x j x K
    n = (~np.isnan(W)).sum(1)
    c = eq.sum(-1)
    ok = c >= np.maximum(2, np.ceil(2 * n[:, None, None] / 3))
    idx = np.arange(R)
    ok &= (idx[None, :, None] < idx[None, None, :])
    ok &= (idx[:, None, None] != idx[None, :, None]) & (idx[:, None, None] != idx[None, None, :])
    return ok.any((1, 2)).sum()


# ------------------------------------------------------------------ (d) duplicados
def duplicados(V):
    W = np.nan_to_num(V, nan=-1)
    ok = (~np.isnan(V)).sum(1) >= 2
    eq = (W[:, None, :] == W[None, :, :]).all(-1) & ok[:, None] & ok[None, :]
    iu = np.triu_indices(len(V), 1)
    adj = np.array([eq[i, i + 1] for i in range(len(V) - 1)])
    return eq[iu].sum(), adj.sum()


def mi_norm(x, lab):
    x = pd.Series(x).astype(str)
    t = pd.crosstab(x, lab).to_numpy().astype(float)
    p = t / t.sum()
    px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
    with np.errstate(all="ignore"):
        mi = np.nansum(p * np.log2(p / (px * py)))
        h = -np.nansum(px * np.log2(px))
    return mi / h if h > 0 else np.nan


def main():
    M, c, s = C.matrices()
    lin = []
    # ---------------- (a)
    g = pd.read_csv(C.RAIZ / "datos" / "grupos.csv")
    p0 = c[(c.nivel == 0) & (c.union != "T")]
    tam = p0.groupby(["kfg", "grupo"]).size()
    ng = tam.groupby("kfg").size()
    modal = tam[tam >= 2].groupby("kfg").agg(lambda x: x.value_counts().idxmax())
    R = pd.Series({k: m["R"] for k, m in M.items()})
    K = pd.Series({k: m["K"] for k, m in M.items()})
    vals = [4, 5, 6, 10, 12]
    ex = (exceso(R, vals, "R tablas (n=%d)" % len(R)) + exceso(K, vals, "K tablas (n=%d)" % len(K)) +
          exceso(ng[ng >= 2], vals, "nº grupos corpus (n=%d)" % (ng >= 2).sum()) +
          exceso(modal, vals, "tamaño modal de grupo corpus (n=%d)" % len(modal)))
    ex = pd.DataFrame(ex)
    ex["holm"] = holm(ex.p.fillna(1))
    ex.to_csv(C.OUT / "t3_numero_filas.csv", index=False)
    lin.append("(a) Exceso de valores 'típicos' frente a la vecindad x±2 (binomial p0=1/5, Holm sobre 20 pruebas)")
    lin.append(ex.round(4).to_string(index=False))
    lin.append("distribución R (tablas): " + R.value_counts().sort_index().head(25).to_dict().__str__())
    lin.append("distribución K (tablas): " + K.value_counts().sort_index().to_dict().__str__())
    lin.append("distribución nº de grupos (corpus, 1-30): " + ng.value_counts().sort_index().head(30).to_dict().__str__())
    lin.append("distribución tamaño modal de grupo (corpus): " + modal.value_counts().sort_index().head(20).to_dict().__str__())
    lin.append(f"R múltiplo de 10: {(R % 10 == 0).sum()} de {len(R)}; múltiplo de 5: {(R % 5 == 0).sum()}")

    # ---------------- (b)-(e) por quipu
    filas = []
    for i, k in enumerate(sorted(M)):
        rng = np.random.default_rng([C.SEED, 3, i])
        m = M[k]
        V = m["V"]
        cq = c[c.kfg == k]
        en_tabla = set(m["O"].ravel())
        fu = cq[(cq.nivel == 0) & ~cq.orden.isin(en_tabla) & (cq.v > 0)]
        fuera = fu.v.to_numpy()
        o = {"kfg": k, "R": m["R"], "K": m["K"], "n_fuera": len(fuera), "n_T": (fu.union == "T").sum()}
        if len(fuera):
            o["fuera_col"], o["fuera_fila"], o["fuera_tramo"] = coincidencias(fuera, V)
            tot = np.nansum(V)
            o["fuera_gran_total"] = int((fuera == tot).sum())
            nb = np.array([coincidencias(fuera, perm_anudadas(V, rng)) for _ in range(B)])
            for j, x in enumerate(("fuera_col", "fuera_fila", "fuera_tramo")):
                o["e_" + x] = nb[:, j].mean()
                o["p_" + x] = C.pemp(o[x], nb[:, j]) if o[x] > 0 else np.nan
        o["fres_resto"], o["fres_acum"] = fila_resumen(V)
        o["fila_suma"] = fila_suma(V)
        o["dup"], o["dup_contig"] = duplicados(V)
        nr, ns, nd = [], [], []
        for _ in range(B):
            Q = C.perm_col(V, rng)
            nr.append(fila_resumen(Q)); nd.append(duplicados(Q))
            if _ < 199:
                ns.append(fila_suma(C.perm_fila(V, rng)))
        nr, nd = np.array(nr), np.array(nd)
        o["p_fres_resto"] = C.pemp(o["fres_resto"], nr[:, 0]) if o["fres_resto"] >= 2 else np.nan
        o["p_fres_acum"] = C.pemp(o["fres_acum"], nr[:, 1]) if o["fres_acum"] >= 2 else np.nan
        o["e_fila_suma"] = np.nanmean(ns) if len(ns) else np.nan
        o["p_fila_suma"] = C.pemp(o["fila_suma"], ns) if o["fila_suma"] and o["fila_suma"] > 0 else np.nan
        o["e_dup"], o["e_dup_contig"] = nd.mean(0)
        o["p_dup"] = C.pemp(o["dup"], nd[:, 0]) if o["dup"] > 0 else np.nan
        o["p_dup_contig"] = C.pemp(o["dup_contig"], nd[:, 1]) if o["dup_contig"] > 0 else np.nan
        Cm = m["C"]
        o["mi_color_fila"] = mi_norm(Cm.ravel(), np.repeat(np.arange(m["R"]), m["K"]))
        o["mi_color_col"] = mi_norm(Cm.ravel(), np.tile(np.arange(m["K"]), m["R"]))
        filas.append(o)
    d = pd.DataFrame(filas)
    # Las pruebas con estadístico 0 no se evalúan (p = NaN): BH sobre los quipus evaluables, se reporta n.
    pr = ["fuera_col", "fuera_fila", "fuera_tramo", "fres_resto", "fres_acum", "fila_suma", "dup", "dup_contig"]
    for t in pr:
        d["q_" + t] = C.bh(d["p_" + t])
    d.to_csv(C.OUT / "t3_por_quipu.csv", index=False)
    lin.append("\n(b-d) prueba | quipus con estadístico>0 | suma obs | suma esperada nulo | q<0,05 (BH) | quipus")
    for t in pr:
        e = d.get("e_" + t)
        sig = d[d["q_" + t] < .05]
        lin.append(f"{t} | {(d[t] > 0).sum()} | {d[t].sum():.0f} | {e.sum() if e is not None else float('nan'):.1f} | {len(sig)} | "
                   + ", ".join(f"{r.kfg}({getattr(r, t):.0f})" for r in sig.itertuples()))
    lin.append(f"Cuerdas fuera de tabla con valor: {d.n_fuera.sum()} en {(d.n_fuera > 0).sum()} quipus; cuerdas superiores T: {d.n_T.sum()} en {(d.n_T > 0).sum()} quipus")
    lin.append(f"Coincidencias con el gran total de la tabla: {d.fuera_gran_total.sum():.0f} en quipus " +
               ", ".join(d[d.fuera_gran_total > 0].kfg))
    lin.append(f"\n(e) MI normalizada color~fila vs color~columna: mediana fila {d.mi_color_fila.median():.3f}, "
               f"columna {d.mi_color_col.median():.3f}; quipus donde fila > columna: {(d.mi_color_fila > d.mi_color_col).sum()} de {d.mi_color_col.notna().sum()}")
    lin.append("(MI con fila está inflada por tener R categorías con K celdas cada una; comparar solo como orden de magnitud)")
    open(C.OUT / "t3_resumen.txt", "w", encoding="utf-8").write("\n".join(lin))
    print("\n".join(lin))


if __name__ == "__main__":
    main()
