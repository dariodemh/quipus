"""Tarea 1 (cont.): seriacion (periodicidad), banding (rachas), homogeneidad intragrupo (color = etiqueta de bloque) y potencia.
Nulo: permutacion del color entre las cuerdas colgantes del quipu (semilla fija)."""
import numpy as np, pandas as pd
import comun as m
from t1_posicion import t1, codifica

B = 1000

def seriacion(lab, rng, B=B):
    lab = [x for x in lab if x is not None]; n = len(lab)
    if n < 20: return None
    c = pd.factorize(pd.Series(lab))[0]
    if c.max() < 1: return None
    K = min(12, n // 4)
    def a(M):  # M (b,n) -> (b,K) agreement a(k), k=1..K
        return np.stack([(M[:, :-k] == M[:, k:]).mean(1) for k in range(1, K + 1)], 1)
    ao = a(c[None])[0]; Mp = c[m.idx_perm(n, None, B, rng)]; an = a(Mp)
    S = lambda A: A[..., 1:].max(-1) - A[..., 0]
    kstar = 2 + ao[1:].argmax()
    return dict(n=n, K=int(c.max() + 1), a1=ao[0], a1_nulo=an[:, 0].mean(), p_banding=m.mid_p(ao[0], an[:, 0]),
                S=S(ao), S_nulo=S(an).mean(), p_periodico=m.mid_p(S(ao), S(an)), k_mejor=int(kstar), a_k=ao[kstar - 1],
                z_banding=(ao[0] - an[:, 0].mean()) / max(an[:, 0].std(), 1e-9), z_per=(S(ao) - S(an).mean()) / max(S(an).std(), 1e-9))

def homogeneidad(codes, gid, rng, B=B):
    """Fraccion de pares de cuerdas del mismo grupo con igual color. Nulo: permutar colores en el quipu."""
    k = (codes >= 0); c = codes[k]; g = pd.factorize(gid[k])[0]
    sz = np.bincount(g)
    if len(c) < 12 or c.max() < 1 or (sz >= 2).sum() < 3: return None
    K = c.max() + 1; G = g.max() + 1
    def h(Cm):
        Bn = Cm.shape[0]; ids = g[None] * K + Cm + (np.arange(Bn) * G * K)[:, None]
        cnt = np.bincount(ids.ravel(), minlength=Bn * G * K).reshape(Bn, G, K)
        return (cnt * (cnt - 1) / 2).sum((1, 2)) / max((sz * (sz - 1) / 2).sum(), 1)
    ho = h(c[None])[0]; hn = h(c[m.idx_perm(len(c), None, B, rng)])
    return dict(n=len(c), h=ho, h_nulo=hn.mean(), p_homog=m.mid_p(ho, hn), z_homog=(ho - hn.mean()) / max(hn.std(), 1e-9))

def main():
    c, q = m.cargar(); pe = c[c.nivel == 0]
    S, Hh = [], []
    for ik, (kfg, d) in enumerate(pe.groupby("kfg")):
        d = d.sort_values("orden")
        V = {"full": d.ckey.tolist(),
             "natural(sin tintes, comprimida)": [k if nd == "nat" else None for k, nd in zip(d.ckey, d.nd)],
             "binaria nat/tinte": [{"nat": "N", "tinte": "T"}.get(nd) for nd in d.nd]}
        for vn, lab in V.items():
            r = seriacion(lab, np.random.default_rng([m.SEED, 2, ik, len(vn)]))
            if r: S.append(dict(kfg=kfg, col=d.col.iloc[0], variante=vn, **r))
        codes, _ = codifica([x if x else None for x in d.ckey])
        r = homogeneidad(codes, d.grupo.values, np.random.default_rng([m.SEED, 3, ik]))
        if r: Hh.append(dict(kfg=kfg, col=d.col.iloc[0], **r))
    S = pd.DataFrame(S); Hh = pd.DataFrame(Hh)
    for nm in ("p_banding", "p_periodico"):
        S[nm[2:] + "_q"] = np.nan
        for vn in S.variante.unique():
            ix = S.index[S.variante == vn]; S.loc[ix, nm[2:] + "_q"] = m.bh(S.loc[ix, nm].values)
    Hh["homog_q"] = m.bh(Hh.p_homog.values)
    S["clase"] = np.select([(S.banding_q < .05) & (S.periodico_q < .05), S.banding_q < .05, S.periodico_q < .05], ["bandas+periodico", "bandas", "periodico"], "ninguno")
    S.to_csv(m.OUT + "/resultados_t1_seriacion.csv", index=False); Hh.to_csv(m.OUT + "/resultados_t1_homogeneidad.csv", index=False)
    print(S.groupby("variante").clase.value_counts().unstack(fill_value=0))
    print(S.groupby("variante").agg(n=("kfg", "size"), p05_band=("p_banding", lambda x: (x < .05).mean()), p05_per=("p_periodico", lambda x: (x < .05).mean())).round(3))
    print("homogeneidad intragrupo: n=%d, BH<.05: %d (%.1f%%), p<.05 crudo %.1f%%, h medio %.3f vs nulo %.3f" % (len(Hh), (Hh.homog_q < .05).sum(), 100 * (Hh.homog_q < .05).mean(), 100 * (Hh.p_homog < .05).mean(), Hh.h.mean(), Hh.h_nulo.mean()))
    # combinacion homogeneidad x columna
    R = pd.read_csv(m.OUT + "/resultados_t1_mi.csv"); R = R[R.variante == "full"][["kfg", "N2_q", "N2_nMI", "columna_fuerte"]]
    X = Hh.merge(R, on="kfg"); X["bloque"] = X.homog_q < .05; X["columna"] = X.N2_q < .05
    print(pd.crosstab(X.bloque, X.columna, margins=True))
    # --- potencia (simulacion) del test N2: se inyecta estructura de columna con intensidad lam ---
    rows = []
    P0 = pe.groupby("kfg")
    for ik, (kfg, d) in enumerate(P0):
        if kfg not in set(R.kfg): continue
        d = d.sort_values("orden"); rng = np.random.default_rng([m.SEED, 4, ik])
        codes, _ = codifica(d.ckey.where(d.ckey.notna(), None).tolist()); v = codes >= 0
        pos0 = (d.pos.values - 1).astype(int); pcap = np.minimum(pos0, 7)
        sizes = d.groupby("grupo", sort=False).size().tolist()
        for lam in (0.0, 0.1, 0.2, 0.3, 0.5):
            cols = rng.integers(0, 4, 8); sim = codes.copy()
            idx = np.where(v)[0]; emp = codes[v]
            follow = rng.random(len(idx)) < lam
            sim[idx] = np.where(follow, cols[pcap[idx]], rng.permutation(emp))
            r = t1(sim, pos0, d.gsize.values, d.grupo.values, sizes, rng, B1=2, B2=300, B3=2)
            if r: rows.append(dict(kfg=kfg, lam=lam, p=r["N2_p"], nMI=r["N2_nMI"]))
    Pw = pd.DataFrame(rows)
    Pw["q"] = Pw.groupby("lam").p.transform(lambda x: m.bh(x.values))
    pot = Pw.groupby("lam").agg(n=("kfg", "size"), potencia_p05=("p", lambda x: (x < .05).mean()), potencia_bh=("q", lambda x: (x < .05).mean()), nMI_med=("nMI", "median")).round(3)
    pot.to_csv(m.OUT + "/resultados_t1_potencia.csv"); print(pot)

if __name__ == "__main__":
    main()
