# -*- coding: utf-8 -*-
"""Chequeos finales: robustez de Incahuasi, indice de repeticion por quipu,
robustez de las asociaciones de color y del '1' en posicion de etiqueta."""
import pandas as pd, numpy as np, os, re
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261018)
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False).set_index("kfg")
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)
prov = q.reindex(sorted(k.kfg.unique())).procedencia.fillna("Unknown").astype(str)

# ---------- 1) Incahuasi sin los quipus emparejados ----------
print("=== 1) Incahuasi: efecto de quitar UR267A/UR255 (15) y UR275/UR266 (47) ===")
for v, lo, hi, pares in [(15, 10, 19, ["UR267A", "UR255"]), (47, 40, 49, ["UR275", "UR266"])]:
    for excl in [False, True]:
        kk = k[~k.kfg.isin(pares)] if excl else k
        inc = set(prov[prov == "Incahuasi"].index) - (set(pares) if excl else set())
        a = kk[(kk.kfg.isin(inc)) & (kk.valor.between(lo, hi))].valor.eq(v).sum()
        n1 = kk[(kk.kfg.isin(inc)) & (kk.valor.between(lo, hi))].shape[0]
        rest = set(kk.kfg.unique()) - inc
        b = kk[(kk.kfg.isin(rest)) & (kk.valor.between(lo, hi))].valor.eq(v).sum()
        n2 = kk[(kk.kfg.isin(rest)) & (kk.valor.between(lo, hi))].shape[0]
        OR, p = stats.fisher_exact([[a, n1 - a], [b, n2 - b]])
        print(f" v={v} {'sin pares' if excl else 'con pares '}: Incahuasi {a}/{n1}={100*a/n1:.1f}%  "
              f"resto {b}/{n2}={100*b/n2:.1f}%  OR={OR:.2f} p={p:.2g}")

# ---------- 2) repeticion dentro de cada quipu (HHI) vs nulo ----------
print("\n=== 2) indice de repeticion (HHI) por quipu: observado vs nulo de decadas ===")
k["L"] = k.valor.map(lambda v: len(str(v)))
k["d1"] = k.valor.map(lambda v: int(str(v)[0]))
k["est"] = np.where(k.L == 1, 0, k.L * 10 + k.d1)
qi = k.groupby("kfg").ngroup().values
val = k.valor.values; E = k.est.values
nq = k.kfg.nunique()

def hhi_por_quipu(vals):
    df = pd.DataFrame({"qi": qi, "v": vals})
    g = df.groupby(["qi", "v"]).size().rename("n").reset_index()
    tot = g.groupby("qi").n.sum()
    g["p"] = g.n / g.qi.map(tot)
    return g.groupby("qi").apply(lambda s: (s.p ** 2).sum()).reindex(range(nq), fill_value=np.nan)

obs_hhi = hhi_por_quipu(val)
est_vals = sorted(set(E))
null_hhi = []
for it in range(200):
    vp = val.copy()
    for e in est_vals:
        m = np.where(E == e)[0]
        if len(m) > 1: vp[m] = rng.permutation(val[m])
    null_hhi.append(hhi_por_quipu(vp).values)
null_hhi = np.array(null_hhi)
print(f"HHI medio obs={np.nanmean(obs_hhi):.4f}  nulo={np.nanmean(null_hhi):.4f}  "
      f"p={(1+(null_hhi.mean(1)>=np.nanmean(obs_hhi)).sum())/(1+len(null_hhi))}")
print(f"quipus con HHI superior a la mediana nula: {(obs_hhi > np.nanmedian(null_hhi)).sum()}/{nq}")

# ---------- 3) color: robustez de las asociaciones significativas ----------
print("\n=== 3) color: consistencia por quipu de los pares significativos ===")
def color_prim(x):
    if not isinstance(x, str): return None
    return re.split(r"[\(:/,\-]", x.strip())[0].strip()
k["col"] = k.color.map(color_prim)
k["solido"] = k.color.map(lambda x: isinstance(x, str) and not re.search(r"[\(:/,\-]", x))
qmap = {x: i for i, x in enumerate(sorted(k.kfg.unique()))}
k["qi"] = k.kfg.map(qmap)
for v, col in [(1, "B"), (3, "B"), (30, "KB"), (47, "YB")]:
    out = []
    for solid in [False, True]:
        kk = k[k.solido] if solid else k
        n_i = kk.groupby("qi").size().reindex(range(nq), fill_value=0).values
        n_iv = kk[kk.valor == v].groupby("qi").size().reindex(range(nq), fill_value=0).values
        p_i = n_iv / n_i
        n_ic = kk[kk.col == col].groupby("qi").size().reindex(range(nq), fill_value=0).values
        obs = int(((kk.valor == v) & (kk.col == col)).sum()); exp = float((n_ic * p_i).sum())
        var = float((n_ic * p_i * (1 - p_i) * (n_i - n_ic) / np.maximum(n_i - 1, 1)).sum())
        z = (obs - exp) / np.sqrt(var)
        out.append(f"{'solo solidos' if solid else 'todos'}: {obs}/{exp:.0f}={obs/exp:.2f}x z={z:.2f}")
        if not solid:
            # contribucion por quipu y prueba de signos
            contrib = n_ic * (n_iv / n_i) - (n_ic * n_iv / n_i)  # siempre 0; usamos direccion por quipu
            sub = kk[(kk.valor == v) | (kk.col == col)]
            pos = neg = 0
            for i in range(nq):
                s = kk[kk.qi == i]
                if len(s) == 0: continue
                a = ((s.valor == v) & (s.col == col)).sum()
                e = (s.col == col).sum() * (s.valor == v).mean()
                if a > e: pos += 1
                elif a < e: neg += 1
            out.append(f"quipus +{pos}/-{neg} (signo p={stats.binomtest(pos,pos+neg,0.5).pvalue:.2g})")
    print(f" v={v} color={col}: " + " | ".join(out))

# ---------- 4) '1' en primera cuerda: sin quipus dominados por 1 ----------
print("\n=== 4) '1' en primera cuerda del grupo, excluyendo quipus con >30% de unos ===")
k0 = k[k.nivel == 0].copy()
prim = k0.groupby(["kfg", "grupo"]).orden.transform("min")
k0["primero"] = k0.orden == prim
frac1 = k0.groupby("kfg").valor.apply(lambda s: (s == 1).mean())
ok = set(frac1[frac1 <= 0.30].index)
for nom, kk in [("todos", k0), ("sin dominados por 1", k0[k0.kfg.isin(ok)])]:
    obs = int(((kk.valor == 1) & kk.primero).sum())
    esp = kk.groupby("kfg").apply(lambda s: s.grupo.nunique() * (s.valor == 1).mean(), include_groups=False).sum()
    # p por permutacion
    rng2 = np.random.default_rng(7); cnt = 0; B = 500
    vals = kk.valor.values; qs = kk.kfg.values; pr = kk.primero.values
    for it in range(B):
        pp = pr.copy()
        for g in np.unique(qs):
            m = np.where(qs == g)[0]
            if len(m) > 1: pp[m] = rng2.permutation(pr[m])
        c2 = int(((vals == 1) & pp).sum())
        if c2 >= obs: cnt += 1
    print(f" {nom:<22} obs={obs} esp={esp:.0f} ratio={obs/esp:.2f} p={(1+cnt)/(1+B):.4f}")
