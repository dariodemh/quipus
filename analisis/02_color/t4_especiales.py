"""Tarea 4 (y variante natural de la 5): colores raros, mezclas, luminosidad y cordon principal frente a cuerdas 'especiales':
primera/ultima del grupo, cuerda superior (union T), colgante = suma de sus subsidiarias, primera/ultima del grupo = suma del resto.
Las sumas se calculan aqui (valor > 0, >= 2 cuerdas con nudos sumando) y se compara con su frecuencia por azar
(permutando los valores dentro del quipu). Unidad = quipu; nulos Nq (permuta atributo de color en el quipu) y Ng (dentro de grupo).
Salida: resultados_t4_*.csv"""
import numpy as np, pandas as pd
import comun as m

B = 1000; BS = 300


def banderas_suma(d, rng, bs=BS):
    """d: filas del quipu ordenadas. Devuelve flags por cuerda y recuento observado/nulo de sumas."""
    n = len(d); name = {c: i for i, c in enumerate(d.cuerda)}
    v = d.val.values.copy(); hv = ~np.isnan(v)
    par = np.array([name.get(p, -1) if isinstance(p, str) else -1 for p in d.padre])
    ch = np.where((par >= 0) & hv)[0]                       # hijos con valor
    cand_idx = np.unique(par[ch]) if len(ch) else np.array([], int)
    # candidatos: padres con valor y >= 2 hijos con valor
    cnt_h = np.bincount(par[ch], minlength=n) if len(ch) else np.zeros(n, int)
    cand = (cnt_h >= 2) & hv
    # grupo: colgantes en grupos de >=3 cuerdas
    pe = (d.nivel.values == 0)
    gk = pd.factorize(d.grupo.where(pe))[0]; gk = np.where(pe, gk, -1)
    first = np.zeros(n, bool); last = np.zeros(n, bool)
    for g in np.unique(gk[gk >= 0]):
        ii = np.where(gk == g)[0]
        if len(ii) >= 3: first[ii[0]] = True; last[ii[-1]] = True
    cnt_g = np.bincount(gk[(gk >= 0) & hv], minlength=gk.max() + 2) if (gk >= 0).any() else np.zeros(1, int)

    def calc(vv):
        h = ~np.isnan(vv); w = np.where(h, vv, 0.0)
        s = np.bincount(par[ch], weights=w[ch], minlength=n) if len(ch) else np.zeros(n)
        sp = cand & (vv > 0) & np.isclose(vv, s)
        ok = (gk >= 0)
        sg = np.bincount(gk[ok & h], weights=w[ok & h], minlength=gk.max() + 2) if ok.any() else np.zeros(1)
        gsz_h = np.bincount(gk[ok & h], minlength=gk.max() + 2) if ok.any() else np.zeros(1)
        rest = np.where(ok, sg[np.maximum(gk, 0)] - w, 0)
        edge = (first | last) & h & (vv > 0) & (gsz_h[np.maximum(gk, 0)] >= 3) & np.isclose(vv, rest)
        return sp, edge
    sp, edge = calc(v)
    # nulo: permutar los valores entre cuerdas con valor del mismo quipu (misma clase: colgantes con colgantes, subs con subs)
    nsp = np.zeros(bs); ned = np.zeros(bs)
    cls = (d.nivel.values == 0)
    for b in range(bs):
        vv = v.copy()
        for msk in (cls, ~cls):
            ix = np.where(msk & hv)[0]; vv[ix] = v[rng.permutation(ix)]
        a, e = calc(vv); nsp[b] = a.sum(); ned[b] = e.sum()
    return dict(cand=cand, sp=sp, first=first, last=last, edge=edge, n_cand=int(cand.sum()), n_sp=int(sp.sum()), n_sp_nulo=nsp.mean(), var_sp=nsp.var(),
                n_edge=int(edge.sum()), n_edge_nulo=ned.mean(), var_edge=ned.var(), n_edge_cand=int((first | last).sum()))


def contraste(sp_mask, attr, strata, rng, extra_pop=None, vbin=None):
    """diferencia media de attr entre especiales y resto; nulos Nq/Ng permutando attr."""
    ok = ~np.isnan(attr)
    if extra_pop is not None: ok &= extra_pop
    sp = sp_mask[ok]; a = attr[ok]; st = strata[ok]; vb = vbin[ok] if vbin is not None else None
    if sp.sum() < 3 or (~sp).sum() < 3 or np.ptp(a) == 0: return None
    o = np.argsort(st, kind="stable"); sp, a, st = sp[o], a[o], st[o]; vb = vb[o] if vb is not None else None
    stat = lambda A: A[:, sp].mean(1) - A[:, ~sp].mean(1)
    obs = stat(a[None])[0]; out = dict(n=len(a), n_esp=int(sp.sum()), eff=obs)
    ixs = [("Nq", m.idx_perm(len(a), None, B, rng))]
    if 1 < len(set(st)) < len(a): ixs.append(("Ng", m.idx_perm(len(a), st, B, rng)))
    if vb is not None and len(set(vb)) > 1:   # Nv: permuta atributo dentro de terciles de magnitud del valor (controla 'W <-> valor grande')
        o2 = np.argsort(vb, kind="stable"); inv = np.argsort(o2)
        # trabajamos en el orden por tercil y devolvemos al orden original
        pp = m.idx_perm(len(a), vb[o2], B, rng); idv = np.empty_like(pp); idv[:, o2] = o2[pp]
        ixs.append(("Nv", idv))
    for nm, idx in ixs:
        nu = stat(a[idx]); sd = nu.std()
        out[nm + "_z"] = (obs - nu.mean()) / sd if sd > 0 else np.nan
        out[nm + "_p"] = min(1, 2 * min(m.mid_p(obs, nu, "ge"), m.mid_p(obs, nu, "le")))
    return out


def main():
    c, q = m.cargar(); c = c[c.ckey.notna() | True]
    glob = c.ckey.value_counts(normalize=True)
    rows, sums = [], []
    for ik, (kfg, d) in enumerate(c.groupby("kfg")):
        d = d.sort_values("orden").reset_index(drop=True); col = d.col.iloc[0]
        rng = np.random.default_rng([m.SEED, 6, ik])
        F = banderas_suma(d, rng)
        sums.append(dict(kfg=kfg, col=col, **{k: F[k] for k in ("n_cand", "n_sp", "n_sp_nulo", "var_sp", "n_edge_cand", "n_edge", "n_edge_nulo", "var_edge")}))
        valid = d.ckey.notna().values
        # atributos de color (numericos 0/1 salvo luminosidad)
        pe = (d.nivel.values == 0)
        attrs = {}
        for cl, cm in (("colgantes", pe), ("subsidiarias", ~pe)):
            sub = d[cm & valid]
            if len(sub) < 20 or sub.ckey.nunique() < 2: continue
            freq = sub.ckey.map(sub.ckey.value_counts(normalize=True))
            a = {k: np.full(len(d), np.nan) for k in ("rara_en_quipu", "rara_global", "mixta", "blanca", "luminosidad", "tinte")}
            idx = np.where(cm & valid)[0]
            a["rara_en_quipu"][idx] = (freq.values <= 0.10); a["rara_global"][idx] = (sub.ckey.map(glob).values < 0.005)
            a["mixta"][idx] = (sub.ctipo.values != "simple"); a["blanca"][idx] = (sub.ckey.values == "W")
            a["luminosidad"][idx] = sub.inten.values; a["tinte"][idx] = (sub.nd.values == "tinte")
            attrs[cl] = (cm & valid, a)
        specials = {
            "primera_del_grupo": ("colgantes", F["first"]), "ultima_del_grupo": ("colgantes", F["last"]),
            "cuerda_superior_T": ("colgantes", (d.union == "T").values & pe),
            "colgante_suma_de_subs": ("colgantes", F["sp"]),
            "borde_de_grupo_suma_del_resto": ("colgantes", F["edge"]),
        }
        estr = pd.factorize(d.grupo.astype(str) + "|" + d.nivel.astype(str))[0]
        vbin = np.full(len(d), -1)
        for cm_ in (pe, ~pe):
            ii = np.where(cm_ & d.tiene_valor.values)[0]
            if len(ii) >= 6: vbin[ii] = (3 * (pd.Series(d.val.values[ii]).rank(method="first").values - 1) / len(ii)).astype(int) + (0 if cm_ is pe else 10)
        for sn, (cl, mk) in specials.items():
            if cl not in attrs or mk.sum() < 3: continue
            pop_cm, a = attrs[cl]
            for an, arr in a.items():
                # poblacion: para sumas, candidatos (colgantes con >=2 subs con valor) / bordes de grupo; resto: todos los colgantes
                if sn == "colgante_suma_de_subs": pops = {"candidatos": F["cand"]}
                elif sn == "borde_de_grupo_suma_del_resto": pops = {"bordes_de_grupo": F["first"] | F["last"]}
                else: pops = {"todos": np.ones(len(d), bool)}
                for pn, pm in pops.items():
                    for fondo in ("todos", "natural"):
                        if an == "tinte" and fondo == "natural": continue
                        ex = pm & (d.nd == "nat").values if fondo == "natural" else pm
                        r = contraste(mk, arr, estr, rng, ex, vbin)
                        if r: rows.append(dict(kfg=kfg, col=col, especial=sn, atributo=an, poblacion=pn, fondo=fondo, **r))
        if ik % 100 == 0: print("t4", ik, flush=True)
    R = pd.DataFrame(rows); S = pd.DataFrame(sums)
    R.to_csv(m.OUT + "/resultados_t4_quipu.csv", index=False); S.to_csv(m.OUT + "/resultados_t4_sumas_quipu.csv", index=False)
    # metaanalisis
    M = []
    for (sn, an, pn, fo), d in R.groupby(["especial", "atributo", "poblacion", "fondo"]):
        for nm in ("Nq", "Ng", "Nv"):
            if nm + "_z" not in d: continue
            x = d.rename(columns={nm + "_p": "p", nm + "_z": "z"})[["kfg", "eff", "z", "p"]].dropna()
            if len(x) < 8: continue
            M.append(dict(especial=sn, atributo=an, poblacion=pn, fondo=fo, nulo=nm, **m.meta(x)))
    M = pd.DataFrame(M); M["q_bh"] = np.nan
    for nm in ("Nq", "Ng", "Nv"):
        ix = M.index[M.nulo == nm]; M.loc[ix, "q_bh"] = m.bh(M.loc[ix, "p_stouffer"].fillna(1).values)
    M.to_csv(m.OUT + "/resultados_t4_meta.csv", index=False)
    pd.set_option("display.width", 250)
    tot = dict(quipus=len(S), cand=S.n_cand.sum(), sumas_obs=S.n_sp.sum(), sumas_nulo=S.n_sp_nulo.sum(), z=(S.n_sp.sum() - S.n_sp_nulo.sum()) / np.sqrt(S.var_sp.sum()),
               quipus_con_suma=int((S.n_sp > 0).sum()), borde_cand=S.n_edge_cand.sum(), borde_obs=S.n_edge.sum(), borde_nulo=S.n_edge_nulo.sum(), zb=(S.n_edge.sum() - S.n_edge_nulo.sum()) / np.sqrt(max(S.var_edge.sum(), 1e-9)))
    print(tot)
    print(M[M.nulo == "Nq"].sort_values("p_stouffer").head(30)[["especial", "atributo", "poblacion", "fondo", "n", "eff_med", "frac_pos", "z_stouffer", "p_signo", "q_bh"]].round(4).to_string())


if __name__ == "__main__":
    main()
