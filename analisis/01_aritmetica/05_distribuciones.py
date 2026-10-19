"""Tarea 2: Benford (primer dígito, por magnitud), redondeo (dígito de unidades 0/5, múltiplos de 100), repetición de valores pequeños.
Unidad = quipu; nulos explícitos y semilla fija; BH-FDR entre quipus."""
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
from nucleo import cargar, bh
OUT = Path(__file__).parent
rng = np.random.default_rng(2026)
Qs, q = cargar(); q = q.set_index("kfg")
BEN = np.log10(1 + 1 / np.arange(1, 10))
def fd(x):  # primer dígito
    return (x // 10 ** np.floor(np.log10(x)).astype(int)).astype(int)
rows = []
B = 4000
for k, Q in Qs.items():
    v = Q["v"][Q["pres"] & (Q["v"] > 0)]
    r = dict(kfg=k, n_val=len(v), mediana=np.median(v) if len(v) else np.nan, p90=np.percentile(v, 90) if len(v) else np.nan,
             maximo=v.max() if len(v) else np.nan, frac_le9=(v <= 9).mean() if len(v) else np.nan, frac_le20=(v <= 20).mean() if len(v) else np.nan)
    # ---- Benford (n>=50) con nulo Monte Carlo multinomial
    if len(v) >= 50:
        c = np.bincount(fd(v), minlength=10)[1:]; n = c.sum(); f = c / n
        mad = np.abs(f - BEN).mean(); chi = (((c - n * BEN) ** 2) / (n * BEN)).sum()
        sim = rng.multinomial(n, BEN, size=B)
        chis = (((sim - n * BEN) ** 2) / (n * BEN)).sum(1)
        r.update(ben_mad=mad, ben_chi2=chi, ben_p=(1 + (chis >= chi).sum()) / (B + 1), f1=f[0], f2=f[1], f9=f[8])
    # ---- redondeo en dígito de unidades, valores >=20
    w = v[v >= 20]
    if len(w) >= 40:
        u = np.bincount(w % 10, minlength=10) / len(w)
        ref = u[[2, 3, 4, 6, 7, 8, 9]].mean()
        r.update(n20=len(w), u0=u[0], u5=u[5], ref=ref, r0=u[0] / ref if ref > 0 else np.nan, r5=u[5] / ref if ref > 0 else np.nan,
                 p0=stats.binomtest(int(round(u[0] * len(w))), len(w), ref, alternative="greater").pvalue,
                 p5=stats.binomtest(int(round(u[5] * len(w))), len(w), ref, alternative="greater").pvalue)
    # ---- repetición: Simpson vs lognormal discretizada ajustada al quipu
    if len(v) >= 20:
        _, cnt = np.unique(v, return_counts=True)
        simp = ((cnt / len(v)) ** 2).sum(); top = cnt.max() / len(v)
        lv = np.log(v); mu, sg = lv.mean(), max(lv.std(), 1e-6)
        sims = np.maximum(1, np.rint(np.exp(rng.normal(mu, sg, size=(1000, len(v)))))).astype(int)
        ss = np.array([(np.unique(s, return_counts=True)[1] ** 2).sum() / len(v) ** 2 for s in sims])
        # nulo 2: barajar los dígitos de cada posición decimal entre cuerdas (estratos: cuerdas cuyo dígito es el más significativo / no)
        K = int(np.floor(np.log10(v.max()))) + 1; L = np.floor(np.log10(v)).astype(int)
        Dg = np.stack([(v // 10 ** j) % 10 for j in range(K)], 1)
        sd_ = []
        for _b in range(500):
            Dn = Dg.copy()
            for j in range(K):
                for m_ in (L == j, L > j):
                    ix = np.where(m_)[0]
                    if len(ix) > 1: Dn[ix, j] = rng.permutation(Dn[ix, j])
            w2 = (Dn * 10 ** np.arange(K)).sum(1)
            sd_.append((np.unique(w2, return_counts=True)[1] ** 2).sum() / len(v) ** 2)
        sd_ = np.array(sd_)
        r.update(simpsonD_E=sd_.mean(), simpsonD_p=(1 + (sd_ >= simp).sum()) / 501)
        r.update(simpson=simp, simpson_E=ss.mean(), simpson_p=(1 + (ss >= simp).sum()) / 1001, top_valor=top, valor_top=int(_[cnt.argmax()]),
                 distintos=len(cnt) / len(v), n_distintos=len(cnt))
    rows.append(r)
d = pd.DataFrame(rows)
for col in ["ben_p", "p0", "p5", "simpson_p"]:
    t = d[col].notna(); d[col.replace("_p", "_q") if col.endswith("_p") else col.replace("p", "q")] = np.nan
d["simpsonD_q"] = np.nan; d["ben_q"] = np.nan; d["q0"] = np.nan; d["q5"] = np.nan; d["simpson_q"] = np.nan
for p_, q_ in [("ben_p", "ben_q"), ("p0", "q0"), ("p5", "q5"), ("simpson_p", "simpson_q"), ("simpsonD_p", "simpsonD_q")]:
    t = d[p_].notna(); d.loc[t, q_] = bh(d.loc[t, p_])
d["procedencia"] = q.loc[d.kfg, "procedencia"].values
d.to_csv(OUT / "distribuciones_por_quipu.csv", index=False)
print("== Benford por quipu (n>=50)")
t = d.ben_p.notna(); print("testables", t.sum(), "p<.05", (d.ben_p < .05).sum(), "q<.05 (rechaza Benford)", (d.ben_q < .05).sum(), "MAD mediano", d.ben_mad.median().round(4))
print("conforme (MAD<.015 Nigrini):", (d.ben_mad < .015).sum(), " MAD>=.015:", (d.ben_mad >= .015).sum())
# agregado por magnitud, bootstrap de quipus
vals = {k: Q["v"][Q["pres"] & (Q["v"] > 0)] for k, Q in Qs.items()}
ks = list(vals)
def pooled(sel):
    out = {}
    for nd in [1, 2, 3, 4]:
        c = np.zeros(10)
        for k in sel:
            v = vals[k]; v = v[(v >= 10 ** (nd - 1)) & (v < 10 ** nd)] if nd < 4 else v[v >= 1000]
            if len(v): c += np.bincount(fd(v), minlength=10)
        out[nd] = c[1:] / max(c.sum(), 1)
    return out
obs = pooled(ks)
bs = [pooled(rng.choice(ks, len(ks))) for _ in range(300)]
print("== primer dígito pooled por magnitud (n dígitos), IC95% bootstrap de quipus; Benford =", BEN.round(3))
tab = []
for nd in obs:
    lo = np.percentile([b[nd] for b in bs], 2.5, axis=0); hi = np.percentile([b[nd] for b in bs], 97.5, axis=0)
    for dg in range(9): tab.append(dict(digitos=nd, primer=dg + 1, obs=obs[nd][dg], lo=lo[dg], hi=hi[dg], benford=BEN[dg]))
    print(nd, "dig:", np.round(obs[nd], 3), " MAD vs Benford:", np.abs(obs[nd] - BEN).mean().round(4))
pd.DataFrame(tab).to_csv(OUT / "benford_pooled.csv", index=False)
print("== Redondeo (unidades, valores >=20, n>=40)")
t = d.p0.notna(); print("quipus", t.sum(), "mediana r0", d.r0.median().round(2), "mediana r5", d.r5.median().round(2))
print("digito 0 en exceso: p<.05", (d.p0 < .05).sum(), "q<.05", (d.q0 < .05).sum(), "esperados por azar", round(.05 * t.sum(), 1))
print("digito 5 en exceso: p<.05", (d.p5 < .05).sum(), "q<.05", (d.q5 < .05).sum())
bsr = [np.median(d.r0.dropna().sample(frac=1, replace=True, random_state=i)) for i in range(500)]
print("IC95 mediana r0 (quipus):", np.percentile(bsr, [2.5, 97.5]).round(2))
# múltiplos de 100 en valores >=1000: observado vs independencia de dígitos (decenas, unidades) por quipu, agregado
o = e = 0; porq = []
for k, v in vals.items():
    w = v[v >= 1000]
    if len(w) >= 20:
        a_ = (w % 10 == 0).mean(); b_ = ((w // 10) % 10 == 0).mean(); ob = (w % 100 == 0).sum(); ex = len(w) * a_ * b_
        o += ob; e += ex; porq.append((k, len(w), ob, ex, stats.poisson.sf(ob - 1, ex) if ex > 0 else np.nan))
pq = pd.DataFrame(porq, columns=["kfg", "n", "obs", "esp", "p"]); pq["q"] = bh(pq.p.fillna(1))
print("mult. de 100 en >=1000: quipus", len(pq), "obs", o, "esperado indep.", round(e, 1), "razon", round(o / e, 2), " p<.05", (pq.p < .05).sum(), "q<.05", (pq.q < .05).sum())
pq.to_csv(OUT / "mult100.csv", index=False)
print("== Repetición (lognormal discretizada) n>=20")
t = d.simpson_p.notna(); print("quipus", t.sum(), "p<.05", (d.simpson_p < .05).sum(), "q<.05", (d.simpson_q < .05).sum(), "esperados", round(.05 * t.sum(), 1))
print("Simpson obs vs E mediano:", d.simpson.median().round(3), d.simpson_E.median().round(3))
print(d[d.simpson_q < .05].groupby(pd.cut(d.mediana, [0, 5, 10, 20, 50, 1e9]), observed=True).size())
print("valor mas repetido (quipus con q<.05):", d[d.simpson_q < .05].valor_top.value_counts().head(8).to_dict())
print("distribución de la mediana de valores:", d.mediana.describe().round(1).to_dict())
print("quipus con mediana<=9:", (d.mediana <= 9).sum(), " frac_le9>0.5:", (d.frac_le9 > .5).sum())

t = d.simpsonD_p.notna(); print("nulo dígitos por posición: quipus", t.sum(), "p<.05", (d.simpsonD_p < .05).sum(), "q<.05", (d.simpsonD_q < .05).sum(), "esperados", round(.05 * t.sum(), 1))
print("Simpson mediano obs / E(lognormal) / E(dígitos):", d.simpson.median().round(3), d.simpson_E.median().round(3), d.simpsonD_E.median().round(3))
print("quipus con q<.05 en ambos nulos:", ((d.simpson_q < .05) & (d.simpsonD_q < .05)).sum())
print("u0 (frac. unidades=0 en valores>=20) cuantiles:", d.u0.quantile([.1, .25, .5, .75, .9]).round(2).to_dict(), " u0>0.5:", (d.u0 > .5).sum(), "de", d.u0.notna().sum())
