"""Tarea 3: "frases" compartidas. n-gramas (n=2,3,4) de tokens color+patrón de nudos (sin dígitos) sobre
la secuencia de colgantes, presentes en >=3 quipus distintos.
Nulos (por quipu, semilla fija):
  A) barajado de las cuerdas dentro de cada quipu (conserva la composición de cada quipu);
  R) barajado de corridas (runs) de tokens idénticos dentro del quipu (conserva además el bandeado);
  Cfijo) secuencia de COLORES intacta, patrones de nudos barajados dentro del quipu;
  Pfijo) secuencia de PATRONES intacta, colores barajados dentro del quipu.
Un n-grama "robusto" supera los cuatro nulos (q BH < 0.05 en todos).
Por n-grama: nº de quipus observado vs nulo, p empírico, BH. Concentración por sitio con permutación de
etiquetas de sitio entre quipus. Salidas: resultados/t3_*.csv, t3_resumen.txt
"""
import numpy as np
import pandas as pd

import comun as C

P = 400
NULOS = ("A", "R", "Cfijo", "Pfijo")
NS = (2, 3, 4)
MINQ = 3


def runs(x):
    cortes = np.flatnonzero(np.diff(x)) + 1
    return np.split(x, cortes)


def ngram_codes(x, n, V):
    L = len(x) - n + 1
    if L <= 0:
        return np.empty(0, dtype=np.int64)
    code = np.zeros(L, dtype=np.int64)
    for j in range(n):
        code = code * V + x[j:j + L]
    return code


def homog(code, n, V):
    """True si el n-grama tiene un solo token distinto."""
    toks = []
    for _ in range(n):
        toks.append(code % V)
        code = code // V
    toks = np.array(toks)
    return (toks == toks[0]).all(0)


def contiene(code, n, V, t):
    """True si el n-grama contiene el token t."""
    out = np.zeros(len(code), dtype=bool)
    for _ in range(n):
        out |= (code % V) == t
        code = code // V
    return out


def doc_counts(seqs, n, V):
    """n-gramas distintos por quipu -> (codes únicos, nº de quipus)."""
    allc = np.concatenate([np.unique(ngram_codes(x, n, V)) for x in seqs])
    return np.unique(allc, return_counts=True)


def main():
    rng = np.random.default_rng(C.SEMILLA + 3)
    c, q = C.cargar()
    d = c[c["nivel"] == 0]
    vocab = {t: i for i, t in enumerate(sorted(d["tok_colpat"].unique()))}
    V = len(vocab) + 1   # +1: código para combinaciones color|patrón inexistentes creadas por los nulos
    kfgs, seqs, cols, pats = [], [], [], []
    for k, g in d.groupby("kfg"):
        if len(g) >= 5:
            kfgs.append(k)
            seqs.append(g["tok_colpat"].map(vocab).to_numpy(dtype=np.int64))
            cols.append(g["tok_color"].to_numpy())
            pats.append(g["tok_patron"].to_numpy())
    def recod(cc, pp):
        return np.array([vocab.get(f"{a}|{b}", V - 1) for a, b in zip(cc, pp)], dtype=np.int64)

    sitio = q.set_index("kfg")["sitio"].reindex(kfgs).to_numpy()
    inv = {i: t for t, i in vocab.items()}
    filas, lin = [], []
    for n in NS:
        codes, nq = doc_counts(seqs, n, V)
        cand = codes[nq >= MINQ]
        nobs = nq[nq >= MINQ]
        es_h = homog(cand.copy(), n, V)
        nulos = {}
        for nombre in NULOS:
            M = np.zeros((P, len(cand)), dtype=np.int32)
            tot = np.zeros(P)
            tot_nh = np.zeros(P)
            for p in range(P):
                if nombre == "A":
                    ss = [rng.permutation(x) for x in seqs]
                elif nombre == "R":
                    ss = []
                    for x in seqs:
                        r = runs(x)
                        ss.append(np.concatenate([r[i] for i in rng.permutation(len(r))]))
                elif nombre == "Cfijo":   # secuencia de colores intacta; patrones barajados en el quipu
                    ss = [recod(cc, rng.permutation(pp)) for cc, pp in zip(cols, pats)]
                else:                      # Pfijo: secuencia de patrones intacta; colores barajados
                    ss = [recod(rng.permutation(cc), pp) for cc, pp in zip(cols, pats)]
                cc, cn = doc_counts(ss, n, V)
                sh = cc[cn >= MINQ]
                sh = sh[~contiene(sh.copy(), n, V, V - 1)]   # sin combinaciones inexistentes
                tot[p] = len(sh)
                tot_nh[p] = (~homog(sh.copy(), n, V)).sum()
                pos = np.searchsorted(cc, cand)
                pos = np.clip(pos, 0, len(cc) - 1)
                M[p] = np.where(cc[pos] == cand, cn[pos], 0)
            nulos[nombre] = (M, tot, tot_nh)
            s_obs, s_obs_nh = len(cand), int((~es_h).sum())
            lin.append(f"n={n} nulo {nombre}: n-gramas en >={MINQ} quipus: obs={s_obs} vs nulo media={tot.mean():.1f} "
                       f"(p={(1 + (tot >= s_obs).sum()) / (P + 1):.4f}); no homogéneos: obs={s_obs_nh} vs "
                       f"{tot_nh.mean():.1f} (p={(1 + (tot_nh >= s_obs_nh).sum()) / (P + 1):.4f})")
        pv = {nm: (1 + (nulos[nm][0] >= nobs).sum(0)) / (P + 1) for nm in NULOS}
        esp = {nm: nulos[nm][0].mean(0) for nm in NULOS}
        # quipus que contienen cada candidato
        sets = {cd: [] for cd in cand}
        for k, x in zip(range(len(seqs)), seqs):
            for cd in np.intersect1d(np.unique(ngram_codes(x, n, V)), cand):
                sets[cd].append(k)
        for j, cd in enumerate(cand):
            toks, z = [], cd
            for _ in range(n):
                toks.append(inv[int(z % V)])
                z //= V
            ks = sets[cd]
            sit = [sitio[i] for i in ks if sitio[i] is not None]
            filas.append({"n": n, "ngrama": " > ".join(toks[::-1]), "homog": bool(es_h[j]),
                          "n_quipus": int(nobs[j]), **{f"esp_{nm}": esp[nm][j] for nm in NULOS},
                          **{f"p_{nm}": pv[nm][j] for nm in NULOS}, "quipus": " ".join(kfgs[i] for i in ks),
                          "sitios": "; ".join(sorted(set(sit))), "n_sitio_conocido": len(sit),
                          "pureza": (pd.Series(sit).value_counts().iloc[0] / len(sit)) if sit else np.nan})
    df = pd.DataFrame(filas)
    for nm in NULOS:
        df[f"q_{nm}"] = C.bh(df[f"p_{nm}"].to_numpy())
    df["q_todos"] = df[[f"q_{nm}" for nm in NULOS]].max(axis=1)
    df.sort_values(["q_R", "n_quipus"], ascending=[True, False]).to_csv(C.RES / "t3_ngramas.csv", index=False)
    sig = df[(df.q_R < 0.05) & (~df.homog)]
    lin.append(f"n-gramas no homogéneos con exceso de quipus (q_R<0.05, BH sobre {len(df)} candidatos): {len(sig)} "
               f"(por n: {sig.groupby('n').size().to_dict()})")
    for nm in NULOS:
        lin.append(f"  no homogéneos con q_{nm}<0.05: {int(((df[f'q_{nm}'] < 0.05) & ~df.homog).sum())}")
    fuerte = df[(df.q_todos < 0.05) & (~df.homog)]
    lin.append(f"  que superan LOS CUATRO nulos (q<0.05 en todos): {len(fuerte)} (por n: {fuerte.groupby('n').size().to_dict()})")
    fuerte.to_csv(C.RES / "t3_ngramas_robustos.csv", index=False)

    # concentración por sitio: pureza media observada vs permutación de etiquetas de sitio entre quipus
    conoc = np.array([s is not None for s in sitio])
    lab = sitio[conoc]
    idx_conoc = np.flatnonzero(conoc)
    pos_en_conoc = {k: i for i, k in enumerate(idx_conoc)}
    kidx = {k: i for i, k in enumerate(kfgs)}

    def pureza_media(labels, conjuntos):
        v = []
        for cj in conjuntos:
            s = pd.Series(labels[cj]).value_counts()
            v.append(s.iloc[0] / s.sum())
        return np.mean(v)

    for nombre, sub in (("significativos_R", sig), ("robustos_4nulos", fuerte), ("todos_no_homog", df[~df.homog])):
        conj = []
        for qs in sub["quipus"]:
            ii = [pos_en_conoc[kidx[k]] for k in qs.split() if kidx[k] in pos_en_conoc]
            if len(ii) >= 3:
                conj.append(np.array(ii))
        if not conj:
            continue
        obs = pureza_media(lab, conj)
        null = np.array([pureza_media(rng.permutation(lab), conj) for _ in range(500)])
        lin.append(f"pureza de sitio ({nombre}, {len(conj)} n-gramas con >=3 quipus de sitio conocido): "
                   f"obs={obs:.3f} vs nulo={null.mean():.3f} (p={(1 + (null >= obs).sum()) / 501:.4f})")
    sitio_top = sig.assign(s=sig["sitios"]).query("n_sitio_conocido>=3 and pureza>=0.99")
    lin.append(f"significativos con todos sus quipus de sitio conocido en un único sitio: {len(sitio_top)}; "
               f"sitios: {sitio_top['sitios'].value_counts().to_dict()}")
    txt = "\n".join(lin)
    (C.RES / "t3_resumen.txt").write_text(txt, encoding="utf-8")
    print(txt)
    print(sig.sort_values("n_quipus", ascending=False).head(25)[
        ["n", "ngrama", "n_quipus", "esp_A", "esp_R", "q_R", "sitios", "pureza"]].to_string())
    print(fuerte.sort_values("n_quipus", ascending=False).head(40)[
        ["n", "ngrama", "n_quipus", "esp_R", "esp_Cfijo", "esp_Pfijo", "q_todos", "sitios", "pureza", "quipus"]].to_string())


if __name__ == "__main__":
    main()
