"""T1. ¿Qué hay en las columnas? Pruebas por quipu sobre la matriz filas x columnas.

Estadísticos y nulos (B permutaciones, semilla fija; p empírico; BH entre quipus por prueba):
  orden     columna sistemáticamente mayor/menor: Σ n_k (rango medio normalizado_k − 0,5)²     N_fila
  vacias    concentración de cuerdas sin nudos en columnas: var(fracción vacía por columna)      N_fila
  constante columna casi constante: máx. cuota de la moda (columnas con ≥3 anudadas)           N_fila
  total_col ¿el "total de fila" cae siempre en la misma columna?: máx. nº de filas por columna
            con celda = suma del resto de la fila                                              N_fila
  total_ex  ¿hay más filas con total interno que por azar?: nº de filas con alguna celda = suma
            del resto                                                                          N_col
  par       columna k = i + j (o i = k − j, "saldo"): máx. nº de filas por terna (k,i,j)       N_col
  corr      tamaño de fila común: correlación de Spearman media entre columnas (filas completas)  N_col
  razon     proporción fija: mín. DE(log10 v_i/v_j) entre pares de columnas (≥4 filas)          N_col (menor = extremo)
  tend      seriación de filas: |Spearman(total de fila, índice de fila)|                        orden de filas
N_fila = baraja celdas dentro de cada fila; N_col = baraja cada columna entre filas; orden de filas = permuta filas.
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr
import comun as C

B = 999


def rangos(V):
    r = rankdata(V, axis=1, nan_policy="omit")
    n = (~np.isnan(V)).sum(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = (r - 1) / (n - 1)
    r[np.broadcast_to(n < 2, r.shape)] = np.nan
    return r


def s_orden(V):
    r = rangos(V)
    n = (~np.isnan(r)).sum(0)
    with np.errstate(invalid="ignore"):
        m = np.nanmean(r, 0)
    return np.nansum(n * (m - .5) ** 2), m


def s_vacias(V):
    f = np.isnan(V).mean(0)
    return f.var(), f


def modas(V):
    out = []
    for k in range(V.shape[1]):
        x = V[:, k][~np.isnan(V[:, k])]
        if len(x) < 3:
            out.append((np.nan, np.nan))
            continue
        u, c = np.unique(x, return_counts=True)
        out.append((c.max() / len(x), u[c.argmax()]))
    return np.array(out)


def s_const(V):
    m = modas(V)
    return (np.nanmax(m[:, 0]) if np.isfinite(m[:, 0]).any() else np.nan), m


def totales(V):
    """T[r,k] = True si la celda (r,k) = suma de las otras celdas anudadas de la fila (≥2 otras >0)."""
    W = np.nan_to_num(V)
    s = W.sum(1, keepdims=True)
    otras = (W > 0).sum(1, keepdims=True) - (W > 0)
    return (~np.isnan(V)) & (W > 0) & (otras >= 2) & np.isclose(W, s - W)


def s_total_col(V):
    t = totales(V).sum(0)
    return t.max(), t


def s_total_ex(V):
    return totales(V).any(1).sum()


def ternas(V):
    """cnt[k,i,j] = nº de filas con V[k] = V[i] + V[j], i<j, todos >0, k∉{i,j}."""
    W = np.where(V > 0, V, np.nan)
    S = W[:, :, None] + W[:, None, :]                       # R x K x K
    eq = np.isclose(W[:, :, None, None], S[:, None, :, :])  # R x K(k) x K(i) x K(j)
    cnt = eq.sum(0).astype(float)
    K = V.shape[1]
    i, j = np.meshgrid(np.arange(K), np.arange(K), indexing="ij")
    malo = (i >= j)
    cnt[:, malo] = 0
    for k in range(K):
        cnt[k, k, :] = 0
        cnt[k, :, k] = 0
    return cnt


def s_par(V):
    if V.shape[1] < 3:
        return np.nan, None
    c = ternas(V)
    return c.max(), np.unravel_index(c.argmax(), c.shape)


def s_corr(V):
    if V.shape[1] < 2:
        return np.nan
    d = pd.DataFrame(np.where(V > 0, V, np.nan))
    m = d.corr(method="spearman", min_periods=4).to_numpy()
    iu = np.triu_indices(V.shape[1], 1)
    return np.nanmean(m[iu]) if np.isfinite(m[iu]).any() else np.nan


def s_razon(V):
    L = np.log10(np.where(V > 0, V, np.nan))
    best, arg = np.nan, None
    K = V.shape[1]
    for i in range(K):
        for j in range(i + 1, K):
            d = L[:, i] - L[:, j]
            d = d[~np.isnan(d)]
            if len(d) >= 4:
                sd = d.std()
                if np.isnan(best) or sd < best:
                    best, arg = sd, (i, j, 10 ** np.median(d))
    return best, arg


def s_tend(V):
    t = np.where((~np.isnan(V)).any(1), np.nansum(V, 1), np.nan)
    ok = ~np.isnan(t)
    if ok.sum() < 4 or np.nanstd(t) == 0:
        return np.nan, np.nan
    rho = spearmanr(np.arange(len(t))[ok], t[ok])[0]
    return abs(rho), rho


def analiza(k, m, rng):
    V = m["V"]
    R, K = V.shape
    o = {"kfg": k, "R": R, "K": K, "frac_anudada": np.mean(~np.isnan(V))}
    obs = {"orden": s_orden(V), "vacias": s_vacias(V), "constante": s_const(V),
           "total_col": s_total_col(V)}
    o["orden"], mr = obs["orden"]
    o["col_mayor"], o["col_menor"] = (int(np.nanargmax(mr)), int(np.nanargmin(mr))) if np.isfinite(mr).any() else (-1, -1)
    o["rango_mayor"] = np.nanmax(mr) if np.isfinite(mr).any() else np.nan
    o["vacias"], fv = obs["vacias"]
    o["cols_vacias"] = ",".join(str(i) for i in np.where(fv >= .8)[0])
    o["frac_vacia_por_col"] = ",".join(f"{x:.2f}" for x in fv)
    o["constante"], md = obs["constante"]
    if np.isfinite(md[:, 0]).any():
        kc = int(np.nanargmax(md[:, 0]))
        o["col_const"], o["val_const"] = kc, md[kc, 1]
    o["total_col"], tc = obs["total_col"]
    o["col_total"] = int(tc.argmax()) if tc.max() > 0 else -1
    o["total_ex"] = s_total_ex(V)
    o["par"], arg = s_par(V)
    if arg is not None:
        o["terna_k_i_j"] = "%d=%d+%d" % arg
    o["corr"] = s_corr(V)
    o["razon"], arg = s_razon(V)
    if arg is not None:
        o["razon_par"] = "%d/%d=%.3g" % arg
    o["tend"], o["rho_tend"] = s_tend(V)
    # nulos
    nf = {x: [] for x in ("orden", "vacias", "constante", "total_col")}
    nc = {x: [] for x in ("total_ex", "par", "corr", "razon")}
    nt = []
    hacer_par = K >= 3 and K <= 40
    for _ in range(B):
        P = C.perm_fila(V, rng)
        nf["orden"].append(s_orden(P)[0]); nf["vacias"].append(s_vacias(P)[0])
        nf["constante"].append(s_const(P)[0]); nf["total_col"].append(s_total_col(P)[0])
        Q = C.perm_col(V, rng)
        nc["total_ex"].append(s_total_ex(Q))
        nc["par"].append(s_par(Q)[0] if hacer_par else np.nan)
        nc["corr"].append(s_corr(Q)); nc["razon"].append(s_razon(Q)[0])
        nt.append(s_tend(V[rng.permutation(R)])[0])
    for x, v in nf.items():
        o["p_" + x] = C.pemp(o[x], v)
        o["e_" + x] = np.nanmean(v)
    for x, v in nc.items():
        o["p_" + x] = C.pemp(o[x], v, mayor=(x != "razon"))
        o["e_" + x] = np.nanmean(v)
    # total_col solo tiene sentido si hay totales
    if o["total_col"] == 0:
        o["p_total_col"] = np.nan
    o["p_tend"] = C.pemp(o["tend"], nt)
    return o


def main():
    if "resumen" in sys.argv:   # solo rehace el resumen a partir del CSV
        return resumen(pd.read_csv(C.OUT / "t1_por_quipu.csv"))
    M, c, s = C.matrices()
    filas = []
    for i, (k, m) in enumerate(sorted(M.items())):
        filas.append(analiza(k, m, np.random.default_rng([C.SEED, 1, i])))
    d = pd.DataFrame(filas)
    resumen(d)


def resumen(d):
    tests = ["orden", "vacias", "constante", "total_col", "total_ex", "par", "corr", "razon", "tend"]
    for t in tests:
        d["q_" + t] = C.bh(d["p_" + t])
    if "resumen" not in sys.argv:
        d.to_csv(C.OUT / "t1_por_quipu.csv", index=False)
    lin = [f"Quipus analizados: {len(d)}; R mediana {d.R.median():.0f} (RIC {d.R.quantile(.25):.0f}-{d.R.quantile(.75):.0f}), "
           f"K mediana {d.K.median():.0f} (RIC {d.K.quantile(.25):.0f}-{d.K.quantile(.75):.0f}); fracción anudada mediana {d.frac_anudada.median():.2f}",
           "prueba | n evaluables | p<0,05 | q<0,05 (BH) | mediana obs | mediana esperado nulo"]
    for t in tests:
        p = d["p_" + t].dropna()
        lin.append(f"{t} | {len(p)} | {(p < .05).sum()} | {(d['q_' + t] < .05).sum()} | "
                   f"{d[t].median():.3g} | {d.get('e_' + t, pd.Series([np.nan])).median():.3g}")
    # posición de la columna mayor/menor entre quipus con orden significativo
    so = d[d.q_orden < .05]
    pos = lambda col, K: "primera" if col == 0 else ("ultima" if col == K - 1 else "interior")
    lin.append(f"\nOrden significativo (q<0,05): {len(so)} quipus")
    lin.append("columna mayor: " + str(pd.Series([pos(a, b) for a, b in zip(so.col_mayor, so.K)]).value_counts().to_dict()))
    lin.append("columna menor: " + str(pd.Series([pos(a, b) for a, b in zip(so.col_menor, so.K)]).value_counts().to_dict()))
    lin.append("esperado si posición uniforme: primera=%.1f ultima=%.1f interior=%.1f" %
               ((1 / so.K).sum(), (1 / so.K).sum(), ((so.K - 2) / so.K).sum()))
    st = d[d.q_total_col < .05]
    lin.append(f"\nColumna-total consistente (q<0,05): {len(st)}: " +
               ", ".join(f"{r.kfg}(col {r.col_total}/{r.K}, {r.total_col:.0f} de {r.R} filas)" for r in st.itertuples()))
    sv = d[d.q_vacias < .05]
    lin.append(f"\nVacías concentradas (q<0,05): {len(sv)}; con alguna columna ≥80 % vacía: {(sv.cols_vacias.fillna('') != '').sum()}")
    lin.append("posición de columnas ≥80 % vacías (todas las seleccionadas): " + str(pd.Series(
        [pos(int(x), r.K) for r in d.itertuples() for x in str(r.cols_vacias).split(",") if x not in ("", "nan")]).value_counts().to_dict()))
    sc = d[d.q_constante < .05]
    lin.append(f"\nColumna casi constante (q<0,05): {len(sc)}: " + ", ".join(
        f"{r.kfg}(col {r.col_const:.0f}={r.val_const:g}, cuota {r.constante:.2f})" for r in sc.itertuples()))
    for t, nom in (("par", "terna k=i+j"), ("razon", "proporción fija"), ("total_ex", "filas con total interno"), ("corr", "correlación entre columnas")):
        x = d[d["q_" + t] < .05]
        col = {"par": "terna_k_i_j", "razon": "razon_par", "total_ex": "total_ex", "corr": "corr"}[t]
        lin.append(f"\n{nom} (q<0,05): {len(x)}: " + ", ".join(f"{r.kfg}({getattr(r, col)})" for r in x.itertuples()))
    x = d[d.q_tend < .05]
    lin.append(f"\nTendencia del total de fila (q<0,05): {len(x)}; crecientes {(x.rho_tend > 0).sum()}, decrecientes {(x.rho_tend < 0).sum()}: "
               + ", ".join(f"{r.kfg}({r.rho_tend:+.2f})" for r in x.itertuples()))
    lin.append(f"Correlación media entre columnas: mediana {d["corr"].median():.3f}; >0 en {(d["corr"] > 0).mean():.0%} de quipus")
    open(C.OUT / "t1_resumen.txt", "w", encoding="utf-8").write("\n".join(lin))
    print("\n".join(lin))


if __name__ == "__main__":
    main()
