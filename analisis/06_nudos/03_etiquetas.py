"""Tarea 3: hipotesis de 'etiqueta' (Saez-Rodriguez).
(a) la primera cuerda de cada grupo / del quipu tiene un perfil de nudos distinto? Nulo: permutar el orden de los colgantes
    dentro de cada grupo (o dentro del quipu); estadistico agregado por quipu; Holm. Control: ultima cuerda.
(b) valores/firmas 'etiqueta' repetidos en la misma posicion entre quipus de igual procedencia. Nulo: permutar procedencia
    entre quipus dentro de prefijo; y comparar con posiciones control (colgantes 11..30).
"""
import numpy as np, pandas as pd, re
from scipy import stats
from util import *

rng = np.random.default_rng(SEED)
d = pd.read_csv(AQUI.parents[0] / "datos/cuerdas.csv", keep_default_na=False, low_memory=False)
qm = pd.read_csv(AQUI.parents[0] / "datos/quipus.csv", keep_default_na=False)
cf = pd.read_csv(AQUI / "cuerdas_flags2.csv", keep_default_na=False, low_memory=False)
c = pd.read_csv(AQUI / "racimos.csv")
d["valor"] = pd.to_numeric(d.valor, errors="coerce")
sig = c.sort_values(["i", "j"]).groupby("i").apply(lambda g: "|".join(f"{t}{n:.0f}" for t, n in zip(g.tipo, g.n)))
d["firma"] = sig.reindex(d.index).fillna("")
d["ncl"] = c.groupby("i").size().reindex(d.index).fillna(0)
d["hasE"] = c[c.tipo == "E"].groupby("i").size().reindex(d.index).fillna(0) > 0
d["hasL"] = c[c.tipo == "L"].groupby("i").size().reindex(d.index).fillna(0) > 0
d["nether"] = cf.nether.values
d["sin_nudos"] = d.nudos == ""
subs = d[d.nivel == 1].groupby(["kfg", "padre"]).size()
p = d[d.nivel == 0].copy()
p["nsub"] = [subs.get((k, n), 0) for k, n in zip(p.kfg, p.cuerda)]
p["tiene_sub"] = p.nsub > 0
p["ord"] = p.groupby("kfg").cumcount() + 1
p = p[p.valor.notna()]
FEAT = {"sin_nudos": "sin nudos", "val_rango": "rango (percentil) del valor", "ncl": "n racimos", "hasE": "tiene figura 8",
        "hasL": "tiene largo", "nether": "nudo inferior", "tiene_sub": "tiene subsidiarias", "firma_unica": "firma unica en el grupo"}

def mk_units(kind):
    """lista de (kfg, indices ordenados) = unidades de permutacion"""
    out = []
    for k, g in p.groupby("kfg"):
        if kind == "quipu":
            if len(g) >= 5: out.append((k, g.index.values))
        else:
            for gi, h in g.groupby("grupo"):
                if gi != "" and len(h) >= 3: out.append((k, h.index.values))
    return out

def feats(ix, perm):
    """valores de cada rasgo para el primero y el ultimo del orden permutado (ix[perm])"""
    h = p.loc[ix]; v = h.valor.values
    r = stats.rankdata(v) - .5; r = r / len(v)  # percentil medio
    sg = h.firma.values; cnt = pd.Series(sg).value_counts()
    cols = {"sin_nudos": h.sin_nudos.values.astype(float), "val_rango": r, "ncl": h.ncl.values.astype(float), "hasE": h.hasE.values.astype(float),
            "hasL": h.hasL.values.astype(float), "nether": h.nether.values.astype(float), "tiene_sub": h.tiene_sub.values.astype(float),
            "firma_unica": np.array([cnt[s] == 1 for s in sg], float)}
    return cols

def run(kind, B=5000):
    U = mk_units(kind)
    pre = [(k, ix, feats(ix, None)) for k, ix in U]
    fl = list(FEAT)
    lens = np.array([len(ix) for _, ix, _ in pre]); starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
    M = np.vstack([np.column_stack([F[f] - F[f].mean() for f in fl]) for _, _, F in pre])  # desviaciones por cuerda
    qn = np.array([k for k, *_ in pre]); qu, qid = np.unique(qn, return_inverse=True); nq = len(qu)
    cnt = np.bincount(qid)
    def estad(j):
        D = M[starts + j]; return np.vstack([np.bincount(qid, D[:, c]) / cnt for c in range(len(fl))]).mean(axis=1)
    res = []
    nulls = np.array([estad((rng.random(len(lens)) * lens).astype(int)) for _ in range(B)])
    for pos, jf in (("primero", lambda: np.zeros(len(lens), int)), ("ultimo", lambda: lens - 1)):
        obs = estad(jf())
        for c, f in enumerate(fl):
            res.append(dict(unidad=kind, posicion=pos, rasgo=f, n_quipus=nq, n_unidades=len(pre), efecto=obs[c],
                            sd_nulo=nulls[:, c].std(), p=pemp(obs[c], nulls[:, c], "dos")))
    R = pd.DataFrame(res); R["p_holm"] = holm(R.p); return R

# NB: permutar el orden dentro de la unidad equivale a elegir al azar la cuerda 'primera': se muestrea un indice uniforme
A = run("grupo"); B_ = run("quipu")
T = pd.concat([A, B_]); T["p_holm_global"] = holm(T.p); T.to_csv(AQUI / "tabla_etiquetas_perfil.csv", index=False)
print(T.round(4).to_string())

# ---------- (b) etiquetas repetidas entre quipus de igual procedencia
print("\n(b) misma posicion, misma procedencia")
P = p.merge(qm[["kfg", "procedencia"]], on="kfg")
P["pref"] = P.kfg.str.extract(r"^([A-Z]+)")[0]
qmeta = qm.set_index("kfg")
def etiqueta_en(posf, campo):
    out = {}
    for k, g in P.groupby("kfg"):
        g = g.sort_values("ord"); r = posf(g)
        if r is None: continue
        v = r[campo]
        if campo == "valor" and (v != v or v == 0): continue
        if campo == "firma" and v == "": continue
        out[k] = v
    return out
POS = {f"pend{j}": (lambda g, j=j: g.iloc[j - 1] if len(g) >= j else None) for j in range(1, 6)}
POS["ultimo"] = lambda g: g.iloc[-1]
POS["penult"] = lambda g: g.iloc[-2] if len(g) >= 2 else None
POS["grupo2_primero"] = lambda g: (g[g.grupo == 1].iloc[0] if (g.grupo == 1).any() else None)
POS["grupo3_primero"] = lambda g: (g[g.grupo == 2].iloc[0] if (g.grupo == 2).any() else None)
CTRL = {f"pend{j}": (lambda g, j=j: g.iloc[j - 1] if len(g) >= j else None) for j in range(11, 31)}

prov = qmeta.procedencia.copy()
bad = prov.isin(["Unknown", ""]) | prov.str.lower().str.contains("unknown")
def estad(lab, provs, prefs, perm=False, cache={}):
    ks = tuple(lab)
    if ks not in cache:
        v = np.array([lab[k] for k in ks], dtype=object); eq = (v[:, None] == v[None, :])
        pr = np.array(pd.factorize(provs.reindex(list(ks)).values)[0]); pf = prefs.reindex(list(ks)).values
        cache[ks] = (eq, pr, pf, np.triu(np.ones(eq.shape, bool), 1))
    eq, pr, pf, iu = cache[ks]
    pr = pr.copy()
    if perm:
        for u in np.unique(pf):
            m = np.where(pf == u)[0]; pr[m] = rng.permutation(pr[m])
    same = (pr[:, None] == pr[None, :]) & iu; diff = (~(pr[:, None] == pr[None, :])) & iu
    return (eq & same).sum() / same.sum() - (eq & diff).sum() / diff.sum(), int(same.sum())
res = []
prefs = P.groupby("kfg").pref.first()
provs = prov.where(~bad, None)
for campo in ("valor", "firma"):
    ctrl_stats = []
    for nm, f in CTRL.items():
        lab = etiqueta_en(f, campo); lab = {k: v for k, v in lab.items() if provs.get(k) is not None}
        if len(lab) > 30: ctrl_stats.append(estad(lab, provs, prefs)[0])
    for nm, f in POS.items():
        lab = etiqueta_en(f, campo); lab = {k: v for k, v in lab.items() if provs.get(k) is not None}
        obs, npar = estad(lab, provs, prefs)
        null = [estad(lab, provs, prefs, True)[0] for _ in range(1000)]
        res.append(dict(campo=campo, posicion=nm, n_quipus=len(lab), pares_misma_proc=npar, exceso_eq=obs, media_nulo=np.mean(null), p_perm=pemp(obs, null),
                        ctrl_media=np.mean(ctrl_stats), ctrl_max=np.max(ctrl_stats), p_vs_ctrl=(1 + sum(c_ >= obs for c_ in ctrl_stats)) / (1 + len(ctrl_stats))))
Rb = pd.DataFrame(res); Rb["p_holm"] = holm(Rb.p_perm); Rb.to_csv(AQUI / "tabla_etiquetas_procedencia.csv", index=False)
print(Rb.round(4).to_string())

# ---------- (c) control de tendencia: el efecto 'primero' ya esta explicado por el orden decreciente dentro del grupo?
# Residuo leave-one-out: ajuste lineal (rasgo ~ posicion) sin la cuerda i, prediccion en i. Nulo: residuo medio 0 (signo aleatorio por quipu).
print("\n(c) residuo respecto de la tendencia lineal dentro del grupo (grupos con >=5 colgantes)")
def loo(y, i):
    x = np.arange(len(y)); m = np.arange(len(y)) != i
    b, a = np.polyfit(x[m], y[m], 1); return y[i] - (a + b * x[i])
rows = []
for feat in ("val_rango", "ncl", "sin_nudos"):
    acc = {}
    for k, ix in [(k, ix) for k, ix in mk_units("grupo") if len(ix) >= 5]:
        F = feats(ix, None)[feat]
        for lab, i in (("pos1", 0), ("pos2", 1), ("pos3", 2), ("penult", len(ix) - 2), ("ultimo", len(ix) - 1)):
            acc.setdefault(lab, {}).setdefault(k, []).append(loo(F, i))
    for lab, dct in acc.items():
        qm_ = np.array([np.mean(v) for v in dct.values()]); obs = qm_.mean()
        null = np.array([(qm_ * rng.choice([-1, 1], len(qm_))).mean() for _ in range(5000)])
        rows.append(dict(rasgo=feat, posicion=lab, n_quipus=len(qm_), residuo_medio=obs, se=qm_.std() / np.sqrt(len(qm_)), p=pemp(obs, null, "dos")))
Rc = pd.DataFrame(rows); Rc["p_holm"] = holm(Rc.p); Rc.to_csv(AQUI / "tabla_etiquetas_tendencia.csv", index=False); print(Rc.round(4).to_string())

# ---------- (d) primer colgante del quipu: vacio? comparado con primeros de otros grupos
print("\n(d) fraccion de primeros colgantes sin nudos")
pp = p.copy(); pp["g"] = pd.to_numeric(pp.grupo, errors="coerce")
first_q = pp.groupby("kfg").head(1)
first_g = pp[pp.g.notna()].groupby(["kfg", "g"]).head(1)
print("primer colgante del quipu: %.3f (n=%d); primero de grupos>=1: %.3f (n=%d); todos: %.3f" % (
    first_q.sin_nudos.mean(), len(first_q), first_g[first_g.g >= 1].sin_nudos.mean(), (first_g.g >= 1).sum(), pp.sin_nudos.mean()))
print("por prefijo (primer colgante vacio / base):")
print(first_q.groupby(first_q.kfg.str[:2]).sin_nudos.agg(["mean", "size"]).join(pp.groupby(pp.kfg.str[:2]).sin_nudos.mean().rename("base")).round(3))
