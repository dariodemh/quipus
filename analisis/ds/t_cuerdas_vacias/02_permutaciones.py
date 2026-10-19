# -*- coding: utf-8 -*-
"""
02_permutaciones.py -- pruebas con permutación dentro de quipu (o dentro de madre)
para posición, color, unión y largo de las cuerdas sin nudos.

Motor rápido: las permutaciones se hacen por bloques (argsort de claves aleatorias
con offset de grupo) y los estadísticos por grupo con np.add.reduceat.
Unidad de inferencia: el quipu. Semilla fija.
"""
import os, re, json
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
os.makedirs(OUT, exist_ok=True)
NPERM = 5000
BATCH = 250
SEED = 20261017


# ---------------------------------------------------------------- datos
def load():
    df = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str, keep_default_na=False)
    df["sin"] = df.nudos.str.strip() == ""
    df["nivel"] = df.nivel.astype(int)
    df["orden"] = df.orden.astype(int)
    df["grupo"] = df.grupo.astype(int)
    df["L"] = pd.to_numeric(df.largo, errors="coerce")
    df["rota"] = df.terminacion.isin(["B", "C"])
    df["completa"] = df.terminacion.isin(["K", "U", "R", "D"])

    def prim(c):
        c = c.strip()
        if c == "":
            return "NA"
        m = re.match(r"^([A-Z]{1,2})", c)
        return m.group(1) if m else "OTRO"
    df["pc"] = df.color.map(prim)
    df["mezcla"] = df.color.str.contains(r"[:/\-%]", regex=True) & (df.color.str.strip() != "")
    df["un"] = df.union.replace({"Unknown": "DESCONOCIDA", "U": "DESCONOCIDA",
                                 "?": "DESCONOCIDA", "": "SIN_DATO"})
    return df


def add_position(df):
    d0 = df[df.nivel == 0].copy().sort_values(["kfg", "grupo", "orden"])
    d0["rank"] = d0.groupby(["kfg", "grupo"]).cumcount() + 1
    d0["gsize"] = d0.groupby(["kfg", "grupo"]).orden.transform("size")
    d0["first"] = d0["rank"] == 1
    d0["last"] = d0["rank"] == d0.gsize
    d0["single"] = d0.gsize == 1
    gr = d0[["kfg", "grupo"]].drop_duplicates().sort_values(["kfg", "grupo"])
    gr["gidx"] = gr.groupby("kfg").cumcount() + 1
    gr["ngroups"] = gr.groupby("kfg").grupo.transform("size")
    d0 = d0.merge(gr, on=["kfg", "grupo"], how="left")
    d0["gfirst"] = d0.gidx == 1
    d0["glast"] = d0.gidx == d0.ngroups
    return d0


def add_siblings(df):
    ds = df[df.nivel >= 1].copy().sort_values(["kfg", "padre", "orden"])
    ds["srank"] = ds.groupby(["kfg", "padre"]).cumcount() + 1
    ds["ssize"] = ds.groupby(["kfg", "padre"]).orden.transform("size")
    ds["sfirst"] = ds.srank == 1
    ds["slast"] = ds.srank == ds.ssize
    return ds


# ---------------------------------------------------------------- motor
class Groups:
    """Bloques contiguos definidos por una o más columnas, en orden de filas."""
    def __init__(self, sub, cols):
        if isinstance(cols, str):
            cols = [cols]
        self.sub = sub.reset_index(drop=True)
        keys = list(zip(*[self.sub[c].values for c in cols]))
        # ya viene ordenado; bloques contiguos
        same = np.array([keys[i] == keys[i - 1] for i in range(1, len(keys))], dtype=bool)
        starts = np.r_[0, np.where(~same)[0] + 1].astype(int)
        ends = np.r_[starts[1:], len(keys)].astype(int)
        self.starts = starts
        self.ends = ends
        self.sizes = ends - starts
        self.G = len(starts)
        self.group_id = np.repeat(np.arange(self.G), self.sizes)
        self.keys = [keys[s] for s in starts]

    def permute(self, y, rng, B):
        """y (n,) -> yp (n,B) permutado dentro de cada bloque."""
        n = len(y)
        keys = rng.random((n, B)) + self.group_id[:, None] * 1e6
        order = np.argsort(keys, axis=0)
        return y[order]


def _stats_from(yp, g, flag, y):
    """Estadísticos por grupo y por permutación para y continuo/binario y flag fijo."""
    flag = flag.astype(float)
    S_all = np.add.reduceat(yp, g.starts, axis=0)                 # G,B
    S_flag = np.add.reduceat(yp * flag[:, None], g.starts, axis=0)
    n_flag = np.add.reduceat(flag[:, None] * np.ones((1, yp.shape[1])), g.starts, axis=0)
    n_all = g.sizes[:, None]
    n1 = n_flag
    n0 = n_all - n_flag
    with np.errstate(invalid="ignore", divide="ignore"):
        d = S_flag / n1 - (S_all - S_flag) / n0
        w = n1 * n0 / n_all
    mix = (n1[:, 0] > 0) & (n0[:, 0] > 0)
    d = d[mix]; w = w[mix]
    if d.size:
        stat_eq = np.nanmean(d, axis=0)
        stat_w = np.nansum(w * d, axis=0) / np.nansum(w, axis=0)
    else:
        stat_eq = np.full(yp.shape[1], np.nan)
        stat_w = np.full(yp.shape[1], np.nan)
    fb = flag.astype(bool)
    if fb.any() and (~fb).any():
        pooled = yp[fb].mean(axis=0) - yp[~fb].mean(axis=0)
    else:
        pooled = np.full(yp.shape[1], np.nan)
    return stat_eq, stat_w, pooled, int(mix.sum()), int(flag.sum())


def perm_diff(sub, groupcols, ycol, flagcol, nperm=NPERM, seed=7, label=""):
    sub = sub.dropna(subset=[ycol]).copy()
    if len(sub) == 0:
        return None
    sub = sub.sort_values(groupcols if isinstance(groupcols, list) else [groupcols], kind="stable")
    g = Groups(sub, groupcols)
    y = sub[ycol].values.astype(float)
    flag = sub[flagcol].values.astype(bool)
    if not (flag.any() and (~flag).any()):
        return None
    rng = np.random.default_rng(seed)
    obs_eq, obs_w, obs_pool, nmix, nflag = _stats_from(y[:, None], g, flag, y)
    null_eq, null_w, null_pool = [], [], []
    left = nperm
    while left > 0:
        B = min(BATCH, left)
        yp = g.permute(y, rng, B)
        s_eq, s_w, s_pool, _, _ = _stats_from(yp, g, flag, y)
        null_eq.append(s_eq); null_w.append(s_w); null_pool.append(s_pool)
        left -= B
    null_eq = np.concatenate(null_eq); null_w = np.concatenate(null_w); null_pool = np.concatenate(null_pool)
    def pv(null, obs):
        return float((1 + np.sum(np.abs(null) >= abs(obs) - 1e-12)) / (nperm + 1))
    return dict(test=label, obs=float(obs_eq[0]), obs_w=float(obs_w[0]), obs_pool=float(obs_pool[0]),
                null_mean=float(np.nanmean(null_eq)), null_sd=float(np.nanstd(null_eq)),
                p=pv(null_eq, obs_eq[0]), p_w=pv(null_w, obs_w[0]), p_pool=pv(null_pool, obs_pool[0]),
                n=len(sub), n_groups=nmix, n_flag=nflag)


def strat_test(sub, catcol, nperm=NPERM, seed=11, label="", min_count=50, stratcols="kfg"):
    sub = sub.copy()
    vc = sub[catcol].value_counts()
    keep = vc[vc >= min_count].index.tolist()
    if len(keep) == 0:
        return None
    sub["cat"] = np.where(sub[catcol].isin(keep), sub[catcol], "OTRO")
    cats = list(keep)
    if "OTRO" in sub.cat.values and "OTRO" not in cats:
        cats.append("OTRO")
    if isinstance(stratcols, str):
        stratcols = [stratcols]
    sub = sub.sort_values(stratcols, kind="stable").reset_index(drop=True)
    g = Groups(sub, stratcols)
    y = sub.sin.values.astype(bool)
    c = pd.Categorical(sub.cat, categories=cats).codes
    C = len(cats)

    O = np.bincount(c[y], minlength=C).astype(float)
    E = np.zeros(C)
    V = np.zeros(C)
    for s, e in zip(g.starts, g.ends):
        n = e - s
        m = y[s:e].sum()
        if n < 2:
            continue
        kc = np.bincount(c[s:e], minlength=C).astype(float)
        E += m * kc / n
        V += m * (kc / n) * (1 - kc / n) * (n - m) / (n - 1)
    z = (O - E) / np.sqrt(np.maximum(V, 1e-12))
    ok = V > 0
    g_obs = float(np.sum((O[ok] - E[ok]) ** 2 / V[ok]))

    onehot = np.zeros((len(sub), C))
    onehot[np.arange(len(sub)), c] = 1.0
    rng = np.random.default_rng(seed)
    Ostar = []
    left = nperm
    while left > 0:
        B = min(BATCH, left)
        yp = g.permute(y.astype(float), rng, B)
        # O* por categoría = suma de yp en filas de cada categoría
        this = np.empty((B, C))
        for j in range(C):
            this[:, j] = np.add.reduceat(yp * onehot[:, j][:, None], g.starts, axis=0).sum(axis=0)
        Ostar.append(this)
        left -= B
    Ostar = np.vstack(Ostar)
    dev_obs = np.abs(O - E)
    dev_null = np.abs(Ostar - E)
    p_cat = (1 + (dev_null >= dev_obs - 1e-12).sum(axis=0)) / (nperm + 1)
    g_null = np.sum((Ostar[:, ok] - E[ok]) ** 2 / V[ok], axis=1)
    p_global = (1 + np.sum(g_null >= g_obs - 1e-12)) / (nperm + 1)
    # BH
    n = len(p_cat)
    o = np.argsort(p_cat)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p_cat[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    q = np.minimum(q, 1.0)
    rows = []
    for j, cat in enumerate(cats):
        mj = c == j
        nq = sub.loc[mj, "kfg"].nunique()
        both = sub.loc[mj].groupby("kfg").sin.agg(["min", "max"])
        nqc = int(((both["min"] == 0) & (both["max"] == 1)).sum())
        rows.append(dict(test=label, categoria=cat, n=int(mj.sum()),
                         n_quipus=nq, n_quipus_contraste=nqc,
                         obs=int(O[j]), esperado=round(float(E[j]), 1),
                         z=round(float(z[j]), 2), p=float(p_cat[j]), q=float(q[j])))
    glob = dict(test=label, stat=round(g_obs, 1), p=float(p_global), n=len(sub),
                n_groups=g.G, ncats=C)
    return glob, pd.DataFrame(rows)


def summarize(res, title):
    if res is None:
        print(f"{title}: sin datos", flush=True)
        return
    print(f"{title}: w={res['obs_w']:+.4f} (p={res['p_w']:.4f}) | eq={res['obs']:+.4f} (p={res['p']:.4f}) | "
          f"pooled={res['obs_pool']:+.4f} (p={res['p_pool']:.4f}); n={res['n']}, grupos={res['n_groups']}", flush=True)


# ---------------------------------------------------------------- main
def main():
    df = load()
    d0 = add_position(df)
    ds = add_siblings(df)
    k0 = d0[d0.terminacion == "K"].copy()
    ks = ds[ds.terminacion == "K"].copy()
    allres = []

    print("== 1. POSICIÓN (nivel 0, terminación K) ==", flush=True)
    for flag, lab in [("first", "primera del grupo"), ("last", "última del grupo"),
                      ("gfirst", "primer grupo del quipu"), ("glast", "último grupo"),
                      ("single", "grupo de 1")]:
        r = perm_diff(k0, "kfg", "sin", flag, label=lab)
        summarize(r, lab)
        if r: allres.append(dict(seccion="posicion", **r))
    r = perm_diff(k0, "kfg", "gsize", "sin", label="tamaño de grupo ~ sin")
    summarize(r, "tamaño de grupo (y=gsize, flag=sin)")
    if r: allres.append(dict(seccion="posicion", **r))

    # ---------- 2. concentración en grupos / adyacencia
    print("\n== 2. AGRUPAMIENTO (nivel 0, K) ==", flush=True)
    k0 = k0.sort_values(["kfg", "grupo", "orden"], kind="stable").reset_index(drop=True)
    gsub = Groups(k0, ["kfg", "grupo"])   # sub-grupos para el estadístico
    gk = Groups(k0, "kfg")                # bloques de permutación (dentro del quipu)
    y = k0.sin.values.astype(bool)
    qn = k0.groupby("kfg").size()
    qm = k0.groupby("kfg").sin.sum()
    pq_g = np.array([qm[k[0]] / qn[k[0]] for k in gsub.keys])
    n_g = gsub.sizes
    m_g = np.array([int(y[s:e].sum()) for s, e in zip(gsub.starts, gsub.ends)])
    idx3 = n_g >= 3
    obs_conc = float(np.sum((m_g[idx3] - n_g[idx3] * pq_g[idx3]) ** 2))
    obs_all = int(np.sum(m_g[n_g >= 2] == n_g[n_g >= 2]))
    # adyacencia dentro de grupo
    same = np.zeros(len(k0) - 1, dtype=bool)
    for s, e in zip(gsub.starts, gsub.ends):
        same[s:e - 1] = True
    obs_adj = int(np.sum(y[:-1] & y[1:] & same))
    rng = np.random.default_rng(31)
    null_conc, null_all, null_adj = [], [], []
    left = NPERM
    while left > 0:
        B = min(BATCH, left)
        yp = gk.permute(y.astype(float), rng, B)
        S = np.add.reduceat(yp, gsub.starts, axis=0)
        null_conc.append(np.sum((S[idx3] - n_g[idx3, None] * pq_g[idx3, None]) ** 2, axis=0))
        null_all.append(np.sum(S[n_g >= 2] == n_g[n_g >= 2, None], axis=0))
        null_adj.append(np.sum(yp[:-1] * yp[1:] * same[:, None], axis=0))
        left -= B
    null_conc = np.concatenate(null_conc); null_all = np.concatenate(null_all); null_adj = np.concatenate(null_adj)
    p_conc = (1 + np.sum(null_conc >= obs_conc - 1e-9)) / (NPERM + 1)
    p_all = (1 + np.sum(null_all >= obs_all)) / (NPERM + 1)
    p_adj = (1 + np.sum(null_adj >= obs_adj)) / (NPERM + 1)
    print(f"concentración por grupo (n>=3): stat={obs_conc:.1f}, nulo={null_conc.mean():.1f}±{null_conc.std():.1f}, p={p_conc:.4f}", flush=True)
    print(f"grupos 100% vacíos (n>=2): obs={obs_all}, nulo={null_all.mean():.1f}±{null_all.std():.1f}, p={p_all:.4f}", flush=True)
    print(f"pares adyacentes vacíos: obs={obs_adj}, nulo={null_adj.mean():.1f}±{null_adj.std():.1f}, p={p_adj:.4f}", flush=True)
    allres += [dict(seccion="agrupamiento", test="concentracion_grupo", obs=obs_conc,
                    null_mean=float(null_conc.mean()), null_sd=float(null_conc.std()), p=float(p_conc)),
               dict(seccion="agrupamiento", test="grupos_100_vacios", obs=obs_all,
                    null_mean=float(null_all.mean()), null_sd=float(null_all.std()), p=float(p_all)),
               dict(seccion="agrupamiento", test="adyacencia", obs=obs_adj,
                    null_mean=float(null_adj.mean()), null_sd=float(null_adj.std()), p=float(p_adj))]

    # ---------- 3. color
    print("\n== 3. COLOR (nivel 0, K) ==", flush=True)
    glob, tab = strat_test(k0, "pc", label="color_primario_K0", min_count=50)
    print(f"global color: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}, n={glob['n']}", flush=True)
    tab.to_csv(os.path.join(OUT, "color_perm.csv"), index=False, encoding="utf-8-sig")
    print(tab.sort_values("p").head(14).to_string(index=False), flush=True)
    allres.append(dict(seccion="color", **glob))
    r = perm_diff(k0, "kfg", "sin", "mezcla", label="color mezclado")
    summarize(r, "color mezclado (y=sin, flag=mezcla)")
    if r: allres.append(dict(seccion="color", **r))

    # ---------- 4. unión
    print("\n== 4. UNIÓN (nivel 0, K) ==", flush=True)
    glob, tab = strat_test(k0, "un", label="union_K0", min_count=30)
    print(f"global unión: stat={glob['stat']}, p={glob['p']}, cats={glob['ncats']}", flush=True)
    tab.to_csv(os.path.join(OUT, "union_perm.csv"), index=False, encoding="utf-8-sig")
    print(tab.sort_values("p").to_string(index=False), flush=True)
    allres.append(dict(seccion="union", **glob))

    # ---------- 5. largo
    print("\n== 5. LARGO (nivel 0, K) ==", flush=True)
    r = perm_diff(k0, "kfg", "L", "sin", label="largo K0")
    summarize(r, "largo (y=L, flag=sin)")
    if r: allres.append(dict(seccion="largo", **r))
    d0b = d0[d0.rota].copy()
    r = perm_diff(d0b, "kfg", "L", "sin", label="largo rotas")
    summarize(r, "largo rotas (B/C)")
    if r: allres.append(dict(seccion="largo", **r))

    # ---------- 6. subsidiarias
    print("\n== 6. SUBSIDIARIAS (terminación K) ==", flush=True)
    for flag, lab in [("sfirst", "primera hermana"), ("slast", "última hermana")]:
        r = perm_diff(ks, ["kfg", "padre"], "sin", flag, label=lab)
        summarize(r, lab)
        if r: allres.append(dict(seccion="subsidiarias", **r))
    mp = df.set_index(["kfg", "cuerda"]).pc.to_dict()
    ks2 = ks.copy()
    ks2["mother_pc"] = [mp.get((k, p), "NA") for k, p in zip(ks2.kfg, ks2.padre)]
    ks2 = ks2[ks2.mother_pc != "NA"].copy()
    ks2["match"] = (ks2.pc == ks2.mother_pc).astype(float)
    r = perm_diff(ks2, ["kfg", "padre"], "match", "sin", label="color hija=madre")
    summarize(r, "color hija == madre (y=match, flag=sin)")
    if r: allres.append(dict(seccion="subsidiarias", **r))

    res = pd.DataFrame(allres)
    res.to_csv(os.path.join(OUT, "resultados_perm.csv"), index=False, encoding="utf-8-sig")
    print("\nguardado resultados_perm.csv", flush=True)


if __name__ == "__main__":
    main()
