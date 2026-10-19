"""Tarea 2: ¿estructura de tabla? Por quipu, variables color y magnitud (nº de dígitos; 0 = sin nudos):
 A) Periodo implícito k=2..15: filas = trozos consecutivos de k colgantes, columnas = posición en el trozo.
    I(variable; columna) con nulo = permutar DENTRO de cada fila (conserva la composición de las filas).
    p por k (P=3000) y combinación de Simes sobre k.
 B) Grupos explícitos (espacios en el cordón): grupos del tamaño más frecuente (>=2, >=3 grupos);
    ¿la posición dentro del grupo predice la variable? Nulo: permutar dentro de cada grupo (P=2000).
Referencias emparejadas por quipu (misma prueba, misma longitud y mismos grupos):
    markov1 = sustituto de Markov de orden 1 del propio quipu; texto_quechua = ventana de la DUDH;
    tabla_fid0.3/0.6 = tablas sintéticas (potencia).
Fracción tabular estimada = (tasa quipus - tasa referencia) / (1 - tasa referencia).
Salidas: resultados/t2_por_quipu.csv, t2_resumen.txt
"""
import numpy as np
import pandas as pd

import comun as C

P = 3000
KMAX = 15
VARS = {"color": "tok_color", "magn": "magn"}


def simes(p):
    p = np.sort(np.asarray(p))
    return float(min(1.0, (len(p) * p / np.arange(1, len(p) + 1)).min()))


def barrido(x, rng, P=P):
    """x codificado. Para cada k: filas = trozos consecutivos de k (se descarta la fila incompleta).
    Columna: I(token; i mod k) con nulo = permutar DENTRO de cada fila (conserva la composición de las
    filas, por tanto el bandeado y la dependencia local). p por k; combinación Simes sobre k.
    Filas (descriptivo): exceso de I(token; fila) frente a barajado global."""
    n, V = len(x), int(x.max()) + 1
    ks = [k for k in range(2, min(KMAX, n // 3) + 1)]
    if not ks or V < 2:
        return None
    H0 = C.entropia(x)
    pk, ec, er = [], [], []
    for k in ks:
        m = (n // k) * k
        xr = x[:m].reshape(-1, k)
        X = np.vstack([xr.ravel()[None, :],
                       rng.permuted(np.broadcast_to(xr, (P,) + xr.shape), axis=2).reshape(P, m)])
        col = np.tile(np.arange(k), m // k)
        row = np.repeat(np.arange(m // k), k)
        mc = C.mi_etiqueta(X, col, V, k)
        pk.append((1 + (mc[1:] >= mc[0]).sum()) / (P + 1))
        ec.append((mc[0] - mc[1:].mean()) / H0 if H0 else np.nan)
        G = C.barajar(xr.ravel(), 100, rng)
        mr = C.mi_etiqueta(np.vstack([xr.ravel()[None, :], G]), row, V, m // k)
        er.append((mr[0] - mr[1:].mean()) / H0 if H0 else np.nan)
    j = int(np.argmin(pk))
    return {"k_best": ks[j], "p_kbest": pk[j], "exc_col": ec[j], "exc_row": er[j],
            "p_col": simes(pk), "exc_row_max": float(np.nanmax(er))}


def grupos_explicitos(x, grp, rng, P=P):
    s = pd.Series(grp)
    tam = s.map(s.value_counts())
    # tamaño de grupo más frecuente entre los >=2
    vc = s.value_counts().value_counts()
    vc = vc[vc.index >= 2]
    if vc.empty:
        return None
    modal = int(vc.idxmax())
    sel = (tam == modal).to_numpy()
    ngr = len(np.unique(grp[sel]))
    if ngr < 3:
        return None
    xs, gs = x[sel], grp[sel]
    pos = np.concatenate([np.arange(modal)] * ngr)
    V = int(xs.max()) + 1
    if V < 2:
        return None
    # permutación dentro de grupo: orden aleatorio por bloques
    perms = np.empty((P, len(xs)), dtype=np.int64)
    base = np.arange(len(xs)).reshape(ngr, modal)
    for i in range(P):
        perms[i] = xs[rng.permuted(base, axis=1).ravel()]
    m = C.mi_etiqueta(np.vstack([xs[None, :], perms]), pos, V, modal)
    H0 = C.entropia(xs)
    return {"g_tam": modal, "g_n": ngr, "g_exc": (m[0] - m[1:].mean()) / H0 if H0 else np.nan,
            "g_p": (1 + (m[1:] >= m[0]).sum()) / (P + 1)}


def markov1(x, rng):
    """Sustituto de Markov de orden 1 con las transiciones observadas del propio quipu (conserva bandeado
    y dependencia de desfase 1; destruye la periodicidad fija salvo ciclos deterministas)."""
    V = int(x.max()) + 1
    T = np.zeros((V, V))
    np.add.at(T, (x[:-1], x[1:]), 1)
    marg = np.bincount(x, minlength=V) / len(x)
    y = np.empty(len(x), dtype=np.int64)
    y[0] = x[0]
    for i in range(1, len(x)):
        r = T[y[i - 1]]
        y[i] = rng.choice(V, p=r / r.sum()) if r.sum() > 0 else rng.choice(V, p=marg)
    return y


def evaluar(x, grp, rng, P1, P2):
    return {**(barrido(x, rng, P=P1) or {}), **(grupos_explicitos(x, grp, rng, P=P2) or {})}


def main():
    rng = np.random.default_rng(C.SEMILLA + 2)
    c, q = C.cargar()
    tt, _ = C.texto_referencia("Quechua")
    filas = []
    for var, colname in VARS.items():
        seqs = C.secuencias(c, colname, min_len=12)
        for k, (tok, grp) in seqs.items():
            x = C.codificar(tok)
            n = len(x)
            filas.append({"kfg": k, "var": var, "clase": "quipu", "n": n, **evaluar(x, grp, rng, P, 2000)})
            filas.append({"kfg": k, "var": var, "clase": "markov1", "n": n,
                          **evaluar(C.codificar(markov1(x, rng)), grp, rng, 1000, 1000)})
            if var == "color" and n <= len(tt):
                s0 = int(rng.integers(0, len(tt) - n + 1))
                filas.append({"kfg": k, "var": var, "clase": "texto_quechua", "n": n,
                              **evaluar(C.codificar(tt[s0:s0 + n]), grp, rng, 1000, 1000)})
            if var == "color" and n % 5 == 0:   # ~1/5 de los quipus: tablas sintéticas (potencia)
                _, frec = np.unique(tok, return_counts=True)
                kk = int(rng.integers(3, 9))
                for fid in (0.3, 0.6):
                    ts, tg = C.tabla_sintetica(n, frec.astype(float), kk, fid, rng)
                    filas.append({"kfg": k, "var": var, "clase": f"tabla_fid{fid}", "n": n,
                                  **evaluar(ts, tg, rng, 1000, 1000)})
    df = pd.DataFrame(filas)
    df["q_p_col"] = np.nan
    df["q_g_p"] = np.nan
    for (var, cl), idx in df.groupby(["var", "clase"]).groups.items():
        df.loc[idx, "q_p_col"] = C.bh(df.loc[idx, "p_col"].to_numpy())
        df.loc[idx, "q_g_p"] = C.bh(df.loc[idx, "g_p"].to_numpy())
    df.to_csv(C.RES / "t2_por_quipu.csv", index=False)

    lin = ["Tasas de significación (p<0.05 sin corregir / q<0.05 BH) por clase de secuencia:"]
    tabla = []
    for (var, cl), d in df.groupby(["var", "clase"]):
        a, b = d.dropna(subset=["p_col"]), d.dropna(subset=["g_p"])
        tabla.append({"var": var, "clase": cl, "n_impl": len(a), "impl_p<.05": (a.p_col < .05).mean(),
                      "impl_q<.05": (a.q_p_col < .05).mean(), "n_grupos": len(b),
                      "grupos_p<.05": (b.g_p < .05).mean(), "grupos_q<.05": (b.q_g_p < .05).mean(),
                      "exc_col_med": a.exc_col.median(), "g_exc_med": b.g_exc.median(),
                      "exc_row_max_med": a.exc_row_max.median()})
    tabla = pd.DataFrame(tabla)
    lin.append(tabla.round(3).to_string(index=False))
    # fracción tabular estimada = exceso de la tasa de los quipus sobre la de su referencia emparejada
    for var in VARS:
        t = tabla[tabla["var"] == var].set_index("clase")
        for test in ("impl_p<.05", "grupos_p<.05"):
            r_q = t.loc["quipu", test]
            for ref in ("markov1", "texto_quechua"):
                if ref in t.index:
                    r0 = t.loc[ref, test]
                    lin.append(f"[{var}] {test}: quipus {r_q:.1%} vs {ref} {r0:.1%} -> fracción tabular "
                               f"estimada (r-r0)/(1-r0) = {(r_q - r0) / (1 - r0):.1%}")
    qd = df[df.clase == "quipu"]
    w = qd.pivot_table(index="kfg", columns="var", values="q_g_p")
    tabg = (w < 0.05).any(axis=1)
    lin.append(f"Quipus con columnas significativas en sus grupos explícitos (q<0.05, color o magnitud): "
               f"{int(tabg.sum())}/{len(tabg)} = {tabg.mean():.1%} (de los que tienen grupos repetidos >=2)")
    sig = qd[(qd.q_p_col < .05)]
    lin.append(f"Periodo implícito q<0.05: {sig.kfg.nunique()} quipus; entre ellos columnas > filas "
               f"(exc_col > exc_row) = {(sig.exc_col > sig.exc_row).mean():.1%}; k mediano = {sig.k_best.median()}")
    txt = "\n".join(lin)
    (C.RES / "t2_resumen.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
