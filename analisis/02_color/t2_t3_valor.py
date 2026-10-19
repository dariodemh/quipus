"""Tareas 2, 3 y 5: color <-> valor dentro de cada quipu y vocabulario entre quipus (metaanalisis por quipu).
Estadisticos por quipu: Kruskal-Wallis (epsilon^2) color~valor; AUC de cada color vs resto sobre valor y sobre 'cuerda vacia'; rho(luminosidad, valor).
Nulos: Nq = permutar color entre cuerdas del mismo quipu y clase (colgantes / subsidiarias);
       Ng = permutar dentro de grupo (colgantes) o dentro de madre (subsidiarias).
Salida: resultados_t2_*.csv, resultados_t3_*.csv"""
import re, numpy as np, pandas as pd
from scipy.stats import rankdata
import comun as m

B = 1000
SINGLES = ["W", "AB", "MB", "KB", "YB", "B", "LB", "NB", "DB", "HB", "RB", "GG"]
ROJOS = {"RM", "SR", "VR"}; AZULES = {"PB", "VB", "BG", "BL", "GL", "LC", "TG"}
VERDES = {"GG", "PG", "DG", "VG", "YG", "GR", "G", "0G", "G0", "0D"}; AMARILLOS = {"YY", "SY", "0Y"}


def anade_cats(c):
    tk = c.ckey.map(lambda s: set(t for t in re.split(r"[:/%*_\-]+", s) if t) if isinstance(s, str) else set())
    cat = {}
    for s in SINGLES:
        cat[s] = (c.ckey == s)
    cat["MIX_moteado"] = c.ctipo == "moteado"; cat["MIX_barber"] = c.ctipo == "barber"; cat["MIX_segm"] = c.ctipo == "segmentado"
    cat["MIX_cualquiera"] = c.ctipo.isin(["moteado", "barber", "segmentado", "otro"])
    cat["MIX_con_W"] = tk.map(lambda t: "W" in t and len(t) > 1)
    cat["rojo"] = tk.map(lambda t: bool(t & ROJOS)); cat["azul"] = tk.map(lambda t: bool(t & AZULES))
    cat["verde"] = tk.map(lambda t: bool(t & VERDES)); cat["amarillo"] = tk.map(lambda t: bool(t & AMARILLOS))
    cat["TINTE_amplio"] = c.nd == "tinte"; cat["TINTE_estricto"] = c.nd2 == "tinte"; cat["NATURAL"] = c.nd == "nat"
    return pd.DataFrame(cat)


NATCATS = (set(SINGLES) - {"GG"}) | {"MIX_moteado", "MIX_barber", "MIX_segm", "MIX_cualquiera", "MIX_con_W"}


def prep(d, estr_col):
    """Ordena por estrato (necesario para permutar dentro de estratos)."""
    code = pd.factorize(d[estr_col].astype(str))[0]
    o = np.argsort(code, kind="stable")
    return d.iloc[o], code[o]


def auc_stats(mask, r, idxs):
    n = len(r); mm = mask.sum(); den = mm * (n - mm)
    f = lambda sr: (sr - mm * (mm + 1) / 2) / den
    obs = f(r[mask].sum()); out = dict(auc=obs)
    for nm, idx in idxs:
        nu = f((mask[idx] * r[None]).sum(1)); sd = nu.std()
        out[nm + "_z"] = (obs - nu.mean()) / sd if sd > 0 else np.nan
        p1, p2 = m.mid_p(obs, nu, "ge"), m.mid_p(obs, nu, "le")
        out[nm + "_p"] = min(1, 2 * min(p1, p2))
    return out


def kw_stats(L, r, idxs):
    n = len(L); K = L.max() + 1; nj = np.bincount(L, minlength=K).astype(float); k = (nj > 0).sum()

    def H(Lp):
        S = np.stack([np.bincount(l, weights=r, minlength=K) for l in Lp])
        return 12 / (n * (n + 1)) * ((S ** 2) / np.where(nj > 0, nj, 1)).sum(1) - 3 * (n + 1)
    obs = H(L[None])[0]; out = dict(H=obs, eps2=(obs - (k - 1)) / (n - k), k=k)
    for nm, idx in idxs:
        nu = H(L[idx]); sd = nu.std()
        out[nm + "_z"] = (obs - nu.mean()) / sd if sd > 0 else np.nan
        out[nm + "_p"] = m.mid_p(obs, nu, "ge")
    return out


def merge_rare(lab, minc=3):
    s = pd.Series(lab); vc = s.value_counts(); s = s.where(s.map(vc) >= minc, "otro")
    return pd.factorize(s)[0], s.nunique()


def perm_set(n, s_, rng):
    ix = [("Nq", m.idx_perm(n, None, B, rng))]
    if 1 < len(set(s_)) < n:
        ix.append(("Ng", m.idx_perm(n, s_, B, rng)))
    # Nc: desplazamiento circular del color a lo largo del quipu (conserva rachas/autocorrelacion de color)
    sh = rng.integers(1, n, B); ix.append(("Nc", (np.arange(n)[None, :] + sh[:, None]) % n))
    return ix


def main():
    c, q = m.cargar(); C = anade_cats(c); c = pd.concat([c, C.add_prefix("cat_")], axis=1)
    c = c[c.ckey.notna()]
    T2, T3 = [], []
    for ik, (kfg, d0) in enumerate(c.groupby("kfg")):
        col = d0.col.iloc[0]
        for clase, estr in (("colgantes", "grupo"), ("subsidiarias", "padre")):
            d = d0[d0.nivel == 0] if clase == "colgantes" else d0[d0.nivel >= 1]
            if len(d) < 20:
                continue
            d, st = prep(d, estr)
            rng = np.random.default_rng([m.SEED, 5, ik, len(clase)])
            for outc in ("valor", "vacia"):
                sel = d.tiene_valor.values if outc == "valor" else np.ones(len(d), bool)
                dd = d[sel]; s_ = st[sel]; n = len(dd)
                if n < 20:
                    continue
                y = dd.val.values if outc == "valor" else (~dd.tiene_valor.values).astype(float)
                if np.ptp(y) == 0:
                    continue
                r = rankdata(y); idxs = perm_set(n, s_, rng)
                # ---- T2: Kruskal-Wallis, variantes por origen del color ----
                if outc == "valor":
                    for vn, msk in (("todos", np.ones(n, bool)), ("natural", (dd.nd == "nat").values), ("tinte", (dd.nd == "tinte").values)):
                        if msk.sum() < 15:
                            continue
                        sub = dd[msk]; ss = s_[msk]; rs = rankdata(sub.val.values)
                        L, k = merge_rare(sub.ckey.tolist())
                        if k < 2 or np.ptp(rs) == 0:
                            continue
                        T2.append(dict(kfg=kfg, col=col, clase=clase, variante=vn, n=len(sub), **kw_stats(L, rs, perm_set(len(sub), ss, rng))))
                    # luminosidad (intensidad Ascher) vs valor
                    ok = dd.inten.notna().values
                    if ok.sum() >= 20 and dd.inten[ok].nunique() > 1:
                        sub = dd[ok]; ss = s_[ok]; rs = rankdata(sub.val.values); li = rankdata(sub.inten.values)
                        if rs.std() > 0:
                            zr = (rs - rs.mean()) / rs.std(); zl = (li - li.mean()) / li.std()
                            obs = (zr * zl).mean()
                            row = dict(kfg=kfg, col=col, clase=clase, outcome="valor", color="LUMINOSIDAD(rho)", fondo="todos", n=len(sub), m=len(sub), eff=obs)
                            for nm, idx in perm_set(len(sub), ss, rng):
                                nu = (zr[None] * zl[idx]).mean(1); sd = nu.std()
                                row[nm + "_z"] = (obs - nu.mean()) / sd if sd > 0 else np.nan
                                row[nm + "_p"] = min(1, 2 * min(m.mid_p(obs, nu, "ge"), m.mid_p(obs, nu, "le")))
                            T3.append(row)
                # ---- T3: AUC por color ----
                nat = (dd.nd == "nat").values
                ix_nat = None
                for cn in C.columns:
                    mk = dd["cat_" + cn].values.astype(bool)
                    for fondo in (("todos", "natural") if cn in NATCATS else ("todos",)):
                        if fondo == "natural":
                            if nat.sum() < 20:
                                continue
                            mk2 = mk[nat]; ss = s_[nat]
                            if mk2.sum() < 5 or (~mk2).sum() < 5:
                                continue
                            if np.ptp(y[nat]) == 0:
                                continue
                            if ix_nat is None:
                                ix_nat = perm_set(nat.sum(), ss, rng)
                            res = auc_stats(mk2, rankdata(y[nat]), ix_nat); mm = mk2.sum(); nn = nat.sum()
                        else:
                            if mk.sum() < 5 or (~mk).sum() < 5:
                                continue
                            res = auc_stats(mk, r, idxs); mm = mk.sum(); nn = n
                        res["eff"] = res.pop("auc") - 0.5
                        T3.append(dict(kfg=kfg, col=col, clase=clase, outcome=outc, color=cn, fondo=fondo, n=nn, m=mm, **res))
        if ik % 100 == 0:
            print("t2/t3", ik, flush=True)
    T2 = pd.DataFrame(T2); T3 = pd.DataFrame(T3)
    T2.to_csv(m.OUT + "/resultados_t2_quipu.csv", index=False); T3.to_csv(m.OUT + "/resultados_t3_quipu.csv", index=False)

    def consist(d):
        g = d.groupby("col").eff.agg(lambda x: ((x > 0).sum() / max((x != 0).sum(), 1), len(x)))
        g = g[g.map(lambda t: t[1] >= 8)]
        return "; ".join("%s:%.2f(n=%d)" % (k, v[0], v[1]) for k, v in g.items())
    M2 = []
    for (cl, vn), d in T2.groupby(["clase", "variante"]):
        for nm in ("Nq", "Ng", "Nc"):
            if nm + "_z" not in d:
                continue
            x = d.rename(columns={nm + "_p": "p", nm + "_z": "z", "eps2": "eff"})[["kfg", "eff", "z", "p"]].dropna()
            M2.append(dict(clase=cl, variante=vn, nulo=nm, **m.meta(x, dos_colas=False)))
    M2 = pd.DataFrame(M2); M2["q_bh"] = np.nan
    for nm in ("Nq", "Ng", "Nc"):
        ix = M2.index[M2.nulo == nm]; M2.loc[ix, "q_bh"] = m.bh(M2.loc[ix, "p_stouffer"].fillna(1).values)
    M2.to_csv(m.OUT + "/resultados_t2_meta.csv", index=False)
    M3 = []
    for (cl, oc, cn, fo), d in T3.groupby(["clase", "outcome", "color", "fondo"]):
        for nm in ("Nq", "Ng", "Nc"):
            if nm + "_z" not in d:
                continue
            x = d.rename(columns={nm + "_p": "p", nm + "_z": "z"})[["kfg", "eff", "z", "p"]].dropna()
            if len(x) < 8:
                continue
            M3.append(dict(clase=cl, outcome=oc, color=cn, fondo=fo, nulo=nm, **m.meta(x), por_coleccion=consist(d)))
    M3 = pd.DataFrame(M3); M3["q_bh"] = np.nan
    for nm in ("Nq", "Ng", "Nc"):
        ix = M3.index[M3.nulo == nm]; M3.loc[ix, "q_bh"] = m.bh(M3.loc[ix, "p_stouffer"].fillna(1).values)
    M3.to_csv(m.OUT + "/resultados_t3_meta.csv", index=False)
    pd.set_option("display.width", 250)
    print(M2.round(4).to_string())
    print(M3[M3.nulo == "Nq"].sort_values("p_stouffer").head(25)[["clase", "outcome", "color", "fondo", "n", "eff_med", "frac_pos", "z_stouffer", "p_signo", "p_stouffer", "q_bh"]].round(4).to_string())


if __name__ == "__main__":
    main()
