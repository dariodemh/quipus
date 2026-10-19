"""Tarea 4: direccion de nudo (S/Z) dentro de cuerda. Unidad = quipu; nulos por permutacion dentro de quipu (y de tipo de nudo).
1. cuantifica cuerdas mixtas y cuanto explica el tipo de nudo.
2. mixtas dentro del mismo tipo: direccion vs posicion (arriba/abajo, decenas/centenas).
3. direccion de cuerda vs union R/V y color (nulo: permutar etiquetas de direccion dentro de quipu x conjunto de tipos).
4. estructura en bloques a lo largo del quipu (cambios de direccion entre cuerdas vecinas) por quipu.
"""
import numpy as np, pandas as pd
from scipy import stats
from util import *

rng = np.random.default_rng(SEED)
c = pd.read_csv(AQUI / "racimos.csv", keep_default_na=False)
for x in ("n", "pos", "ap", "niv"): c[x] = pd.to_numeric(c[x], errors="coerce")
cc = c[c.dir.isin(["S", "Z"])].copy()
cc["Z"] = (cc.dir == "Z").astype(int)

# ---------------- 1. cuerdas mixtas
cord = cc.groupby("i").agg(kfg=("kfg", "first"), orden=("orden", "first"), n=("Z", "size"), z=("Z", "sum"), tipos=("tipo", lambda s: "+".join(sorted(set(s)))),
                           union=("union", "first"), color=("color", "first"))
cord["mixta"] = (cord.z > 0) & (cord.z < cord.n)
# direccion modal por (kfg, tipo): un racimo es "sorpresa" si difiere de la moda de su (quipu,tipo)
mode = cc.groupby(["kfg", "tipo"]).Z.transform(lambda s: int(s.mean() >= .5))
cc["sorpresa"] = cc.Z != mode
cc["nb"] = cc.groupby(["kfg", "tipo"]).Z.transform("size")
mx = cord[cord.mixta]
print(f"Cuerdas con >=1 racimo S/Z conocido: {len(cord)}; con >=2: {(cord.n>=2).sum()}; mixtas S+Z: {len(mx)} ({100*len(mx)/(cord.n>=2).sum():.1f}% de las de >=2) en {mx.kfg.nunique()} quipus")
unif_tipo = cc[cc.i.isin(mx.index)].groupby(["i", "tipo"]).Z.agg(lambda s: s.nunique() == 1).groupby("i").all()
print(f"  de las mixtas, {unif_tipo.sum()} ({100*unif_tipo.mean():.1f}%) son uniformes dentro de cada tipo: la mezcla = diferencia de direccion entre tipos distintos")
print(f"  mixtas DENTRO de un mismo tipo: {(~unif_tipo).sum()} cuerdas en {cc[cc.i.isin(unif_tipo[~unif_tipo].index)].kfg.nunique()} quipus")
qq = cc.groupby("kfg").agg(n=("Z", "size"), sorp=("sorpresa", "mean"))
print(f"racimos que difieren de la direccion modal de su quipu x tipo: {100*cc.sorpresa.mean():.2f}%  (quipus con >=20 racimos: mediana {100*qq[qq.n>=20].sorp.median():.2f}%)")
print("direccion por tipo y prefijo (Z%):"); print((cc.assign(p=cc.kfg.str[:2]).groupby(["p", "tipo"]).Z.agg(["mean", "size"]).query("size>=100")).round(2).T.to_string())

# ---------------- 2. mixtas dentro del mismo tipo: posicion
print("\n2. cuerdas mixtas dentro del mismo tipo (direccion vs posicion arriba/abajo y vs nivel decimal)")
rows = []
for t in ("S", "L", "E"):
    sub = cc[cc.tipo == t]; g = sub.groupby("i")
    ids = [i for i, h in g if len(h) >= 2 and h.Z.nunique() == 2]
    S_ = sub[sub.i.isin(ids)].sort_values(["i", "j"])
    if len(ids) < 5: rows.append(dict(tipo=t, cuerdas=len(ids), quipus=S_.kfg.nunique())); continue
    # estadistico: Z en el racimo superior - fraccion Z de la cuerda (nulo: permutar direcciones dentro de la cuerda)
    arr = [h.Z.values for _, h in S_.groupby("i")]; kq = np.array([h.kfg.iloc[0] for _, h in S_.groupby("i")])
    def st(perm):
        v = np.array([(rng.permutation(a)[0] if perm else a[0]) - a.mean() for a in arr])
        return np.mean([v[kq == k].mean() for k in np.unique(kq)])
    obs = st(False); null = [st(True) for _ in range(5000)]
    row = dict(tipo=t, cuerdas=len(ids), quipus=len(np.unique(kq)), efecto_Z_arriba=obs, p=pemp(obs, null, "dos"))
    if t == "S":  # nivel decimal: correlacion direccion~nivel dentro de cuerda
        lv = [h.niv.values for _, h in S_.groupby("i")]
        ok = [(a, l) for a, l in zip(arr, lv) if np.isfinite(l).all() and len(set(l)) > 1]
        def st2(perm):
            v = [np.corrcoef(rng.permutation(a) if perm else a, l)[0, 1] for a, l in ok]
            return np.nanmean(v)
        o2 = st2(False); n2 = [st2(True) for _ in range(3000)]
        row.update(cuerdas_niv=len(ok), corr_dir_nivel=o2, p_nivel=pemp(o2, n2, "dos"))
    rows.append(row)
R2 = pd.DataFrame(rows); print(R2.round(4).to_string()); R2.to_csv(AQUI / "tabla_dir_posicion.csv", index=False)

# ---------------- 3. direccion de cuerda vs union y color
print("\n3. direccion de cuerda (modal) vs union R/V y color; nulo: permutar etiquetas dentro de quipu x conjunto de tipos")
cd = cord[cord.z * 2 != cord.n].copy(); cd["Zc"] = (cd.z * 2 > cd.n).astype(int)
cd["W"] = cd.color.str.match(r"^W(?![A-Za-z])").astype(int)
cd["mix"] = cd.color.str.contains(":").astype(int)
cd["R"] = cd.union.map({"R": 1, "V": 0})
cd["strata"] = cd.kfg + "|" + cd.tipos
def test(var, sub):
    s = sub.dropna(subset=[var]).copy(); s[var] = s[var].astype(int)
    keep = []
    for k, h in s.groupby("kfg"):
        a, b = h[h[var] == 1], h[h[var] == 0]
        if len(a) >= 5 and len(b) >= 5 and 0 < h.Zc.mean() < 1: keep.append(k)
    s = s[s.kfg.isin(keep)].reset_index(drop=True)
    if not keep: return None
    qi = pd.Series(s.kfg).astype("category").cat.codes.values; nq = qi.max() + 1
    X = s[var].values; strata = [v for v in s.groupby("strata").indices.values()]
    def stat(y):
        d = []
        for k in range(nq):
            m = qi == k; d.append(y[m & (X == 1)].mean() - y[m & (X == 0)].mean())
        return np.mean(d)
    y0 = s.Zc.values.astype(float); obs = stat(y0); null = []
    for _ in range(3000):
        y = y0.copy()
        for v in strata:
            if len(v) > 1: y[v] = rng.permutation(y0[v])
        null.append(stat(y))
    return dict(variable=var, n_quipus=nq, n_cuerdas=len(s), efecto_medio_PZ=obs, p=pemp(obs, null, "dos"))
rows = [test(v, cd) for v in ("R", "W", "mix")]
# por prefijo de fuente (sensibilidad)
for pf in ("UR", "HP", "KH", "QU"):
    for v in ("R", "W"):
        r = test(v, cd[cd.kfg.str.startswith(pf)])
        if r: r["variable"] += "_" + pf; rows.append(r)
R3 = pd.DataFrame([r for r in rows if r]); R3["p_holm"] = holm(R3.p); print(R3.round(4).to_string()); R3.to_csv(AQUI / "tabla_dir_union_color.csv", index=False)

# ---------------- 4. bloques a lo largo del quipu
print("\n4. bloques de direccion a lo largo del quipu (cuerdas del mismo conjunto de tipos; cambios entre vecinas)")
rows = []
for (k), h in cd.groupby("kfg"):
    best = None
    for tp, g in h.groupby("tipos"):
        g = g.sort_values("orden")
        if len(g) < 12 or g.Zc.nunique() < 2 or min(g.Zc.mean(), 1 - g.Zc.mean()) < .1: continue
        y = g.Zc.values; sw = (y[1:] != y[:-1]).sum()
        null = [(lambda z: (z[1:] != z[:-1]).sum())(rng.permutation(y)) for _ in range(2000)]
        rows.append(dict(kfg=k, tipos=tp, n=len(g), pZ=y.mean(), cambios=sw, esperados=np.mean(null), p=pemp(sw, null, "menor")))
R4 = pd.DataFrame(rows); R4["q_bh"] = bh(R4.p)
print(f"strata evaluadas {len(R4)} en {R4.kfg.nunique()} quipus; con q<0.05: {(R4.q_bh<.05).sum()} en {R4[R4.q_bh<.05].kfg.nunique()} quipus; p<0.05 sin corregir: {(R4.p<.05).sum()} (esperado ~{0.05*len(R4):.0f})")
R4.sort_values("p").to_csv(AQUI / "tabla_dir_bloques.csv", index=False); print(R4.sort_values("p").head(12).round(4).to_string())
