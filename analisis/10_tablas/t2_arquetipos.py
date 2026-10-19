"""T2. Arquetipos de columna entre quipus.

(a) Rasgos por columna (normalizados dentro del quipu): posición relativa, rango medio en la fila, magnitud
    relativa (log10 mediana de la columna − log10 mediana de la tabla), % vacías, cuota de la moda,
    fracción de filas en que es total del resto, fracción blanca (W principal), consistencia de color.
(b) Indicadores por quipu definidos de antemano (unidad = quipu) y su recuento en el corpus frente al nulo
    conjunto (cada iteración baraja todas las matrices a la vez):
      A1 primera columna = mayor (máx. rango medio)     A2 última = menor     A3 última = mayor   A4 primera = menor
      A0 media entre quipus de Spearman(posición, rango medio)  (¿decrecen las columnas de izquierda a derecha?)
      A5 la columna mayor es la más blanca   (nulo: valores barajados dentro de fila, colores fijos)
      A6 la primera columna es la más blanca (nulo: colores barajados dentro de fila)
      A7 la columna más vacía es la última / la primera
    Nulo para A0-A4, A7: filas barajadas entre sí + celdas barajadas dentro de fila (conservando valores).
(c) Agrupamiento (k-medias sobre rasgos sin posición, k por silueta) y asociación grupo-de-columna x posición
    (primera/interior/última) con χ² ponderado por quipu (peso 1/K); nulo: mismas matrices barajadas,
    columnas asignadas a los centroides observados.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import comun as C
from t1_columnas import rangos, totales, modas

B = 999
BC = 200  # iteraciones del nulo del agrupamiento


def rasgos(V, Cm):
    R, K = V.shape
    with np.errstate(all="ignore"):
        mr = np.nanmean(rangos(V), 0)
        L = np.log10(np.where(V > 0, V, np.nan))
        med = np.nanmedian(L) if np.isfinite(L).any() else np.nan
        mag = np.nanmedian(L, 0) - med
    md = modas(V)[:, 0]
    tot = totales(V).mean(0)
    w = (Cm == "W").mean(0)
    cons = np.array([pd.Series(Cm[:, k]).value_counts().iloc[0] / R for k in range(K)])
    return pd.DataFrame({"relpos": np.arange(K) / (K - 1), "pos": np.arange(K), "K": K,
                         "rango": mr, "mag": mag, "vacia": np.isnan(V).mean(0), "moda": md,
                         "total": tot, "blanca": w, "cons_color": cons})


def indicadores(V, Cm, Vv=None, Cc=None):
    """Indicadores por quipu. Vv/Cc: versiones barajadas de valores y colores (si None, observados)."""
    Vv = V if Vv is None else Vv
    Cc = Cm if Cc is None else Cc
    K = V.shape[1]
    with np.errstate(all="ignore"):
        mr = np.nanmean(rangos(Vv), 0)
    o = {}
    if np.isfinite(mr).sum() >= 2:
        top, bot = np.nanargmax(mr), np.nanargmin(mr)
        o.update(A1=top == 0, A2=bot == K - 1, A3=top == K - 1, A4=bot == 0)
        ok = np.isfinite(mr)
        o["A0"] = spearmanr(np.arange(K)[ok], mr[ok])[0] if ok.sum() >= 3 and np.nanstd(mr) > 0 else np.nan
        w = (Cm == "W").mean(0)   # colores fijos para A5
        if w.max() > 0 and (w < w.max()).any():
            o["A5"] = w[top] == w.max() and (w == w.max()).sum() == 1
    wc = (Cc == "W").mean(0)
    if wc.max() > 0 and (wc < wc.max()).any():
        o["A6"] = wc[0] == wc.max() and (wc == wc.max()).sum() == 1
    f = np.isnan(Vv).mean(0)
    if f.max() > f.min():
        o["A7u"] = f.argmax() == K - 1 and (f == f.max()).sum() == 1
        o["A7p"] = f.argmax() == 0 and (f == f.max()).sum() == 1
    return o


def main():
    M, c, s = C.matrices()
    ks = sorted(M)
    # ---------------- (b) indicadores
    obs = pd.DataFrame({k: indicadores(M[k]["V"], M[k]["Cm"]) for k in ks}).T
    rng = np.random.default_rng([C.SEED, 2])
    nul = {x: [] for x in obs.columns}
    for b in range(B):
        filas = []
        for k in ks:
            V, Cm = M[k]["V"], M[k]["Cm"]
            P = C.perm_ambos(V, rng)
            o = indicadores(V, Cm, Vv=P)
            o["A5"] = indicadores(V, Cm, Vv=C.perm_fila(V, rng)).get("A5", np.nan)
            o["A6"] = indicadores(V, Cm, Cc=C.perm_fila(Cm, rng)).get("A6", np.nan)
            filas.append(o)
        d = pd.DataFrame(filas)
        for x in nul:
            if x in d:
                nul[x].append(d[x].astype(float).sum() if x != "A0" else d[x].astype(float).mean())
    lin = ["Indicadores de arquetipo (unidad = quipu) frente al nulo conjunto",
           "ind | n quipus | observado | esperado nulo | p (una cola, sup.) | p (inf.)"]
    res = []
    for x in sorted(obs.columns):
        v = obs[x].dropna().astype(float)
        o = v.mean() if x == "A0" else v.sum()
        n = np.array(nul[x])
        res.append({"ind": x, "n": len(v), "obs": o, "esp": n.mean(), "p_sup": C.pemp(o, n), "p_inf": C.pemp(o, n, False)})
    r = pd.DataFrame(res)
    r["p2"] = 2 * r[["p_sup", "p_inf"]].min(1).clip(upper=.5)
    r["holm"] = np.minimum(1, r.p2 * (len(r) - r.p2.rank(method="first") + 1))
    r["holm"] = r.sort_values("p2").holm.cummax().reindex(r.index)
    r.to_csv(C.OUT / "t2_indicadores.csv", index=False)
    for t in r.itertuples():
        lin.append(f"{t.ind} | {t.n} | {t.obs:.3g} | {t.esp:.3g} | {t.p_sup:.4f} | {t.p_inf:.4f}   (bilateral {t.p2:.4f}, Holm {t.holm:.4f})")
    # ---------------- (a) rasgos y (c) agrupamiento
    F = pd.concat([rasgos(M[k]["V"], M[k]["Cm"]).assign(kfg=k) for k in ks], ignore_index=True)
    F.to_csv(C.OUT / "t2_rasgos_columnas.csv", index=False)
    cols = ["rango", "mag", "vacia", "moda", "total", "blanca", "cons_color"]
    X = F[cols].fillna({"rango": .5, "mag": 0, "moda": 0})
    mu, sd = X.mean(), X.std()
    Z = ((X - mu) / sd).to_numpy()
    sil = {}
    for k in range(2, 9):
        km = KMeans(k, n_init=20, random_state=0).fit(Z)
        sil[k] = silhouette_score(Z, km.labels_, random_state=0, sample_size=min(3000, len(Z)))
    kbest = max(sil, key=sil.get)
    km = KMeans(kbest, n_init=50, random_state=0).fit(Z)
    F["arq"] = km.labels_
    F["clase_pos"] = np.where(F.pos == 0, "primera", np.where(F.pos == F.K - 1, "ultima", "interior"))
    F["w"] = 1 / F.K
    lin.append(f"\nAgrupamiento de {len(F)} columnas de {len(ks)} quipus; silueta por k: " +
               ", ".join(f"{k}:{v:.3f}" for k, v in sil.items()) + f" -> k={kbest}")
    cen = F.groupby("arq")[cols].mean()
    cen["n_col"] = F.groupby("arq").size()
    cen["n_quipus"] = F.groupby("arq").kfg.nunique()
    pt = F.pivot_table(index="arq", columns="clase_pos", values="w", aggfunc="sum").fillna(0)
    cen = cen.join(pt.div(pt.sum(1), axis=0).add_prefix("pos_"))
    cen.to_csv(C.OUT / "t2_arquetipos.csv")
    lin.append(cen.round(2).to_string())
    esp_pos = F.groupby("clase_pos").w.sum() / F.w.sum()
    lin.append("reparto global de posiciones (ponderado 1/K): " + esp_pos.round(3).to_dict().__str__())

    def chi2(df):
        t = df.pivot_table(index="arq", columns="clase_pos", values="w", aggfunc="sum").fillna(0)
        e = np.outer(t.sum(1), t.sum(0)) / t.to_numpy().sum()
        return ((t.to_numpy() - e) ** 2 / np.where(e > 0, e, 1)).sum()

    ch_obs = chi2(F)
    ch_n, sil_n = [], []
    rng = np.random.default_rng([C.SEED, 22])
    for b in range(BC):
        G = []
        for k in ks:
            V, Cm = M[k]["V"], M[k]["Cm"]
            # celdas (valor, color) barajadas juntas: filas entre sí y dentro de fila
            R, K = V.shape
            ir = rng.permutation(R)
            ic = np.argsort(rng.random((R, K)), 1)
            G.append(rasgos(V[ir][np.arange(R)[:, None], ic], Cm[ir][np.arange(R)[:, None], ic]).assign(kfg=k))
        G = pd.concat(G, ignore_index=True)
        Zg = ((G[cols].fillna({"rango": .5, "mag": 0, "moda": 0}) - mu) / sd).to_numpy()
        G["arq"] = km.predict(Zg)
        G["clase_pos"] = np.where(G.pos == 0, "primera", np.where(G.pos == G.K - 1, "ultima", "interior"))
        G["w"] = 1 / G.K
        ch_n.append(chi2(G))
        if b < 30:
            kmn = KMeans(kbest, n_init=10, random_state=0).fit(Zg)
            sil_n.append(silhouette_score(Zg, kmn.labels_, random_state=0, sample_size=min(3000, len(Zg))))
    lin.append(f"χ²(arquetipo x posición) observado {ch_obs:.2f}; nulo media {np.mean(ch_n):.2f}, p = {C.pemp(ch_obs, ch_n):.4f}")
    lin.append(f"silueta k={kbest}: observada {sil[kbest]:.3f}; nulo (30 iter.) media {np.mean(sil_n):.3f} (máx {np.max(sil_n):.3f})")
    # residuos por celda arquetipo x posición
    t = F.pivot_table(index="arq", columns="clase_pos", values="w", aggfunc="sum").fillna(0)
    e = np.outer(t.sum(1), t.sum(0)) / t.to_numpy().sum()
    lin.append("observado/esperado (independencia) por arquetipo x posición:\n" + (t / e).round(2).to_string())
    open(C.OUT / "t2_resumen.txt", "w", encoding="utf-8").write("\n".join(lin))
    print("\n".join(lin))


if __name__ == "__main__":
    main()
