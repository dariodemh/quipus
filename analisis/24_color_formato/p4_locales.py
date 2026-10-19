"""P4: qué distingue el color en los 8 quipus con código local fuerte (diseno.md §5).

Salidas: p4_colores.csv (una fila por quipu x color), p4_medidas.csv (η² por variante y clasificación)
"""
from collections import Counter

import numpy as np
import pandas as pd

import comun24 as C

rng = np.random.default_rng(C.SEED)
NREP = 4999
LISTA = ["UR123", "HP017", "QU013", "UR208", "AS128", "UR231", "UR1152", "UR1140"]
c = C.cargar().sort_values(["kfg", "orden"])


def eta2(y, g):
    y = np.asarray(y, float)
    g = np.asarray(g)
    m = y.mean()
    sst = ((y - m) ** 2).sum()
    if sst == 0:
        return 0.0
    ssb = sum(len(y[g == u]) * (y[g == u].mean() - m) ** 2 for u in np.unique(g))
    return ssb / sst


def perm_p(y, g, strata=None):
    o = eta2(y, g)
    g = np.asarray(g)
    nul = []
    for _ in range(NREP):
        if strata is None:
            gp = rng.permutation(g)
        else:
            gp = g.copy()
            for s in np.unique(strata):
                ii = np.where(strata == s)[0]
                gp[ii] = g[rng.permutation(ii)]
        nul.append(eta2(y, gp))
    return o, C.p_emp(o, np.array(nul))


def cramer(a, b):
    t = pd.crosstab(a, b).values
    if min(t.shape) < 2:
        return 0.0
    from scipy.stats import chi2_contingency
    chi2 = chi2_contingency(t, correction=False)[0]
    return np.sqrt(chi2 / (t.sum() * (min(t.shape) - 1)))


COL, MED = [], []
for k in LISTA:
    x = c[c.kfg == k].copy()
    x0 = x[(x.nivel == 0) & x.pres & (x.col != "")].copy()
    x0["pos"] = x0.groupby("grupo").cumcount()
    x0["k"] = x0.groupby("grupo").pos.transform("size")
    x0["posrel"] = np.where(x0.k > 1, x0.pos / (x0.k - 1).clip(lower=1), 0)
    gs = x0.groupby("grupo").valor
    x0["total"] = x0.valor.eq(gs.transform("sum") - x0.valor) & (x0.valor > 0)
    x0["maxg"] = x0.valor.eq(gs.transform("max")) & (x0.k > 1)
    subs = x[(x.nivel == 1) & x.pres].groupby("padre").valor.agg(["sum", "size"])
    x0["total_subs"] = [r.cuerda in subs.index and subs.loc[r.cuerda, "size"] >= 2 and r.valor == subs.loc[r.cuerda, "sum"]
                        for r in x0.itertuples()]
    keep = x0.col.map(Counter(x0.col)) >= 3
    x0 = x0[keep]
    x0["y"] = np.log1p(x0.valor)
    for col, z in x0.groupby("col"):
        tz = Counter(z.torsion)
        COL.append(dict(kfg=k, color=col, base=C.base(col), compuesto=C.compuesto(col), n=len(z),
                        valor_mediana=z.valor.median(), log_media=round(z.y.mean(), 2),
                        posrel_media=round(z.posrel.mean(), 2), grupos=z.grupo.nunique(),
                        frac_total=round((z.total | z.total_subs).mean(), 2), frac_max=round(z.maxg.mean(), 2),
                        torsion=" ".join(f"{a}:{b}" for a, b in tz.most_common()),
                        terminacion=" ".join(f"{a}:{b}" for a, b in Counter(z.terminacion).most_common(2))))
    y, g = x0.y.values, x0.col.values
    a, pa = perm_p(y, g)
    b, pb = perm_p(y, x0.base.values)
    yr = y - x0.groupby("grupo").y.transform("mean").values
    cc_, pc = perm_p(yr, g, strata=x0.grupo.values) if x0.grupo.nunique() > 1 else (np.nan, np.nan)
    ypos = y - x0.groupby("pos").y.transform("mean").values
    d, pd_ = perm_p(ypos, g, strata=x0.pos.values)
    e_mask = ~(x0.total | x0.total_subs | x0.maxg).values
    if len(set(g[e_mask])) > 1:
        e, pe = perm_p(y[e_mask], g[e_mask])
    else:
        e, pe = np.nan, np.nan
    f, pf = perm_p(y, x0.torsion.values) if x0.torsion.nunique() > 1 else (0.0, 1.0)
    V = cramer(x0.col, x0.torsion)
    Vg = cramer(x0.col, x0.grupo)
    MED.append(dict(kfg=k, n=len(x0), colores=x0.col.nunique(), frac_comp=round(x0.comp.mean(), 2),
                    eta_a_crudo=round(a, 3), p_a=pa, eta_b_base=round(b, 3), p_b=pb,
                    eta_c_resid_grupo=round(cc_, 3), p_c=pc, eta_d_resid_pos=round(d, 3), p_d=pd_,
                    eta_e_sin_tot_max=round(e, 3), p_e=pe, n_e=int(e_mask.sum()),
                    eta_f_torsion=round(f, 3), p_f=pf, V_color_torsion=round(V, 2), V_color_grupo=round(Vg, 2)))

M = pd.DataFrame(MED)
M["holm_e"] = C.holm(M.p_e.fillna(1).values)


def clasif(r):
    out = []
    a = r.eta_a_crudo
    if r.eta_b_base < 0.5 * a:
        out.append("ARTEFACTO compuesto/ply")
    if not (r.eta_e_sin_tot_max >= 0.5 * a):
        out.append("MARCA total/encabezado")
    if (r.eta_c_resid_grupo < 0.5 * a) or (r.eta_d_resid_pos < 0.5 * a):
        out.append("MARCA grupo/columna")
    if r.V_color_torsion > 0.5:
        out.append("TORSION")
    if not out and r.p_e < 0.05:
        out.append("CATEGORIA LOCAL")
    return "; ".join(out) or "sin efecto claro"


M["clasificacion"] = M.apply(clasif, axis=1)
M.to_csv(C.AQUI / "p4_medidas.csv", index=False)
pd.DataFrame(COL).to_csv(C.AQUI / "p4_colores.csv", index=False)
pd.set_option("display.width", 300)
print(M.to_string())
print(pd.DataFrame(COL).to_string())
