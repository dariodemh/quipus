"""Tarea 1: entropía, entropía condicional (orden 1-3), información mutua por desfase, Zipf/Heaps.
Compara quipus con nulos: (a) barajado dentro del quipu, (b) barajado de grupos, (c) tabla sintética
con columnas periódicas, (d) texto natural silabeado (DUDH quechua boliviano y español).

Salida: resultados/t1_metricas.csv (una fila por documento x nivel de token) y t1_resumen.csv.
"""
import time

import numpy as np
import pandas as pd

import comun as C

P = 200            # permutaciones por documento (nulo a)
PB = 100           # permutaciones de grupos (nulo b)
LAGS = list(range(1, 21))
NIVELES = {"color": "tok_color", "patron": "tok_patron", "tupla": "tok_full"}


def _h_rows(X, k, V):
    """Entropía condicional plug-in de orden k para cada fila de X (P x n), vectorizada."""
    X = np.asarray(X, dtype=np.int64)
    Pn, n = X.shape

    def hgram(m):
        L = n - m + 1
        code = np.zeros((Pn, L), dtype=np.int64)
        for j in range(m):
            code = code * V + X[:, j:j + L]
        code = np.sort(code, axis=1)
        nuevo = np.ones_like(code, dtype=bool)
        nuevo[:, 1:] = code[:, 1:] != code[:, :-1]
        # longitudes de corrida por fila
        idx = np.flatnonzero(nuevo.ravel())
        fin = np.append(idx[1:], Pn * L)
        cnt = (fin - idx).astype(float)
        fila = idx // L
        s = np.bincount(fila, weights=cnt * np.log2(cnt), minlength=Pn)
        return np.log2(L) - s / L

    if k == 0:
        return hgram(1)
    return hgram(k + 1) - hgram(k)


def metricas(tok, grp, rng):
    x = C.codificar(tok)
    n, V = len(x), int(x.max()) + 1
    out = {"n": n, "V": V}
    H0 = C.h_cond(x, 0)
    out["H0"] = H0
    out["H0_norm"] = H0 / np.log2(V) if V > 1 else np.nan
    Xa = C.barajar(x, P, rng)
    ng = len(np.unique(grp))
    Xb = C.barajar_grupos(x, grp, PB, rng) if ng > 2 else None
    for k in (1, 2, 3):
        h = float(_h_rows(x[None, :], k, V)[0])
        ha = _h_rows(Xa, k, V)
        out[f"H{k}"] = h
        out[f"H{k}_a"] = ha.mean()
        # reducción de entropía respecto del nulo, en fracción de H0 (robusto a vocabulario grande)
        out[f"D{k}_a"] = (ha.mean() - h) / H0 if H0 > 0 else np.nan
        out[f"zD{k}_a"] = (ha.mean() - h) / (ha.std() + 1e-12)
        out[f"p{k}_a"] = (1 + (ha <= h).sum()) / (P + 1)
        if Xb is not None:
            hb = _h_rows(Xb, k, V)
            out[f"H{k}_b"] = hb.mean()
            out[f"D{k}_b"] = (hb.mean() - h) / H0 if H0 > 0 else np.nan
    lags = [d for d in LAGS if d < n - 5]
    I = C.mi_lags(x[None, :], lags, V)[0]
    Ia = C.mi_lags(Xa, lags, V)
    exc = I - Ia.mean(0)
    z = exc / (Ia.std(0) + 1e-12)
    for d, e, zz in zip(lags, exc, z):
        out[f"Iexc_{d}"] = e
        out[f"z_{d}"] = zz
    # perfil: ¿domina el desfase 1 (texto/bandas) o un desfase periódico >1 (tabla)?
    if len(lags) >= 3:
        z2 = z[1:]
        out["z1"] = z[0]
        out["zmax_d>1"] = z2.max()
        out["dmax"] = lags[1 + int(np.argmax(z2))]
        out["Iexc1_rel"] = exc[0] / H0 if H0 > 0 else np.nan
        out["Iexcmax_rel"] = exc[1:].max() / H0 if H0 > 0 else np.nan
    same = (x[1:] == x[:-1]).mean()
    same_a = (Xa[:, 1:] == Xa[:, :-1]).mean()
    out["auto_rep"] = same / same_a if same_a > 0 else np.nan
    out["zipf"] = C.zipf_exponente(tok)
    v, beta = C.heaps(tok)
    out["heaps_beta"] = beta
    vs = np.mean([C.heaps(tok[rng.permutation(n)])[0].mean() for _ in range(20)])
    out["heaps_ratio"] = v.mean() / vs
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(C.SEMILLA)
    c, q = C.cargar()
    refs = {nm: C.texto_referencia(nm) for nm in ("Quechua", "Spanish")}
    refs["Quechua_letras"] = C.texto_referencia("Quechua", "letra")
    filas = []
    for nivel, col in NIVELES.items():
        seqs = C.secuencias(c, col, min_len=10)
        for i, (k, (tok, grp)) in enumerate(seqs.items()):
            n = len(tok)
            # quipu real
            m = metricas(tok, grp, rng)
            filas.append({"doc": k, "clase": "quipu", "nivel": nivel, **m})
            # (c) tabla sintética emparejada: misma longitud y frecuencias de token
            vals, frec = np.unique(tok, return_counts=True)
            gs = pd.Series(grp).value_counts()
            kk = int(gs.mode().iloc[0]) if 2 <= gs.mode().iloc[0] <= 30 else int(rng.integers(3, 9))
            kk = min(kk, max(2, n // 3))
            fid = rng.uniform(0.5, 0.9)
            ts, tg = C.tabla_sintetica(n, frec.astype(float), kk, fid, rng)
            filas.append({"doc": f"tabla_{k}", "clase": "tabla", "nivel": nivel, "k_sint": kk,
                          "fid_sint": fid, **metricas(ts, tg, rng)})
            # (a) referencia aleatoria: el propio quipu barajado (una realización)
            perm = rng.permutation(n)
            filas.append({"doc": f"azar_{k}", "clase": "azar", "nivel": nivel,
                          **metricas(tok[perm], grp, rng)})
            # (d) texto: ventana aleatoria de la misma longitud (solo una vez por quipu: nivel color)
            if nivel == "color":
                for nm, (tt, tgp) in refs.items():
                    L = min(n, len(tt))
                    s = int(rng.integers(0, len(tt) - L + 1))
                    filas.append({"doc": f"{nm}_{k}", "clase": f"texto_{nm}", "nivel": "texto",
                                  **metricas(tt[s:s + L], tgp[s:s + L], rng)})
            if i % 100 == 0:
                print(nivel, i, len(seqs), f"{time.time() - t0:.0f}s", flush=True)
    df = pd.DataFrame(filas)
    df.to_csv(C.RES / "t1_metricas.csv", index=False)
    cols = ["n", "V", "H0", "H0_norm", "D1_a", "D2_a", "D3_a", "zD1_a", "D1_b", "p1_a", "z1", "zmax_d>1", "Iexc1_rel",
            "Iexcmax_rel", "auto_rep", "zipf", "heaps_beta", "heaps_ratio"]
    res = df.groupby(["clase", "nivel"])[cols].median().round(3)
    res.to_csv(C.RES / "t1_resumen.csv")
    print(res.to_string())
    print(f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
