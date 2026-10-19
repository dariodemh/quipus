"""Tarea 4 (cordon principal): el color del cordon principal, ¿se repite en los colgantes del mismo quipu mas que por azar?
Estadistico: media entre quipus de la fraccion de colgantes cuyo color comparte algun hilo con el del cordon principal.
Nulo: permutar el color del cordon principal entre quipus de la misma coleccion (UR, AS, ...) (semilla fija); conserva la distribucion de colores de cordon principal y de colgantes.
Se repite sin cordones 'W' (blanco omnipresente) y con tokens naturales vs teñidos."""
import re, numpy as np, pandas as pd
import comun as m

B = 5000
tok = lambda s: set(t for t in re.split(r"[:/%*_\-]+", re.sub(r"\([^)]*\)", "", s)) if t) if isinstance(s, str) else set()

c, q = m.cargar(); pe = c[(c.nivel == 0) & c.ckey.notna()]
q = q[q.pc_color.notna()].copy(); q["pct"] = q.pc_color.map(tok)
q["col"] = q.kfg.str.extract(r"^([A-Z]+)")[0]
pend = {k: [tok(s) for s in d.ckey] for k, d in pe.groupby("kfg")}
q = q[q.kfg.isin(pend) & (q.pct.map(len) > 0)].reset_index(drop=True)
rng = np.random.default_rng([m.SEED, 7])


def corre(filtro, nombre, quitaW=False):
    ks = list(q.kfg); n = len(ks)
    pct = [(t - {"W"}) if quitaW else t for t in q.pct]
    S = np.full((n, n), np.nan)
    for i, k in enumerate(ks):
        P = [(t - {"W"}) if quitaW else t for t in pend[k]]
        if len(P) < 5: continue
        for j in range(n):
            if pct[j]: S[i, j] = np.mean([bool(t & pct[j]) for t in P])
    ok = np.where(~np.isnan(np.diag(S)) & np.array([bool(p) for p in pct]) & np.array([filtro(x) for x in q.pct]))[0]
    if len(ok) < 10: return None
    obs = np.nanmean(S[ok, ok]); nul = np.zeros(B)
    colv = q.col.values
    for b in range(B):
        perm = np.arange(n)
        for cc in set(colv[ok]):
            ii = np.array([i for i in ok if colv[i] == cc]); perm[ii] = rng.permutation(ii)
        nul[b] = np.nanmean(S[ok, perm[ok]])
    # tambien por quipu: diferencia obs - media nula (efecto) para prueba de signo
    d = np.array([S[i, i] - np.nanmean([S[i, j] for j in ok if colv[j] == colv[i]]) for i in ok])
    from scipy import stats
    pos = (d > 0).sum(); neg = (d < 0).sum()
    return dict(analisis=nombre, n_quipus=len(ok), media_obs=obs, media_nulo=nul.mean(), p_perm=(1 + (nul >= obs).sum()) / (B + 1),
                frac_quipus_mayor_que_azar=pos / max(pos + neg, 1), p_signo=stats.binomtest(pos, pos + neg, .5).pvalue if pos + neg else np.nan)


R = [corre(lambda t: True, "todos"),
     corre(lambda t: True, "sin contar W (se quita W de ambos lados)", quitaW=True),
     corre(lambda t: t != {"W"}, "solo quipus cuyo cordon principal no es solo W"),
     ]
R = pd.DataFrame([r for r in R if r]); R.to_csv(m.OUT + "/resultados_t4_cordon_principal.csv", index=False)
print(R.round(4).to_string())
