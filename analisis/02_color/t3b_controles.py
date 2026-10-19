"""Controles de T3 para los colores 'robustos': ¿se mantienen (a) quitando primera y ultima cuerda de cada grupo (donde viven las sumas/encabezados)
y (b) quitando los quipus de la coleccion mayoritaria (UR)? Colgantes, nulos Nq/Ng/Nc como en t2_t3_valor.py. Salida: resultados_t3_controles.csv"""
import numpy as np, pandas as pd
from scipy.stats import rankdata
import comun as m
from t2_t3_valor import anade_cats, auc_stats, perm_set, prep

c, q = m.cargar(); C = anade_cats(c); c = pd.concat([c, C.add_prefix("cat_")], axis=1); c = c[c.ckey.notna() & (c.nivel == 0)]
COLORES = ["W", "KB", "MIX_cualquiera", "MIX_moteado", "MB", "YB", "NATURAL"]
rows = []
for ik, (kfg, d0) in enumerate(c.groupby("kfg")):
    for ctl in ("interior_de_grupo", "solo_grupos>=3_con_bordes"):
        d = d0[d0.gsize >= 3]
        if ctl == "interior_de_grupo": d = d[(d.pos > 1) & (d.pos < d.gsize)]
        if len(d) < 20: continue
        d, st = prep(d, "grupo"); rng = np.random.default_rng([m.SEED, 9, ik, len(ctl)])
        for outc in ("valor", "vacia"):
            sel = d.tiene_valor.values if outc == "valor" else np.ones(len(d), bool)
            dd = d[sel]; s_ = st[sel]; n = len(dd)
            if n < 20: continue
            y = dd.val.values if outc == "valor" else (~dd.tiene_valor.values).astype(float)
            if np.ptp(y) == 0: continue
            r = rankdata(y); idxs = perm_set(n, s_, rng)
            for cn in COLORES:
                mk = dd["cat_" + cn].values.astype(bool)
                if mk.sum() < 5 or (~mk).sum() < 5: continue
                res = auc_stats(mk, r, idxs); res["eff"] = res.pop("auc") - .5
                rows.append(dict(kfg=kfg, col=d0.col.iloc[0], control=ctl, outcome=outc, color=cn, n=n, m=int(mk.sum()), **res))
R = pd.DataFrame(rows); R.to_csv(m.OUT + "/resultados_t3_controles_quipu.csv", index=False)
M = []
for (ctl, oc, cn), d in R.groupby(["control", "outcome", "color"]):
    for sub, dd in (("todas las colecciones", d), ("sin UR", d[d.col != "UR"])):
        for nm in ("Nq", "Ng", "Nc"):
            if nm + "_z" not in dd: continue
            x = dd.rename(columns={nm + "_p": "p", nm + "_z": "z"})[["kfg", "eff", "z", "p"]].dropna()
            if len(x) >= 8: M.append(dict(control=ctl, outcome=oc, color=cn, subconjunto=sub, nulo=nm, **m.meta(x)))
M = pd.DataFrame(M); M["q_bh"] = m.bh(M.p_stouffer.fillna(1).values); M.to_csv(m.OUT + "/resultados_t3_controles_meta.csv", index=False)
pd.set_option("display.width", 250)
print(M[M.nulo == "Ng"][["control", "outcome", "color", "subconjunto", "n", "eff_med", "frac_pos", "p_signo", "z_stouffer", "q_bh"]].round(4).to_string())
