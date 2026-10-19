"""Tarea 1: color como 'encabezado de columna' (MI color<->posicion-en-grupo) + seriacion/banding.
Salida: resultados_t1_mi.csv, resultados_t1_meta.csv, resultados_t1_seriacion.csv, resultados_t1_potencia.csv"""
import sys, numpy as np, pandas as pd
from scipy import stats
import comun as m

P = 8; KMAX = 8
B_N1, B_N2, B_N3 = 500, 1000, 300

def codifica(lab):
    s = pd.Series(lab); vc = s.value_counts()
    mp = {k: min(i, KMAX) for i, k in enumerate(vc.index)}
    return np.array([mp.get(x, -1) if x is not None else -1 for x in lab]), len(vc)

def mi_batch(cols, poss, w, K):
    cols = np.broadcast_to(cols, w.shape); poss = np.broadcast_to(poss, w.shape)
    B, n = w.shape; KP = K * P
    ids = cols * P + poss + (np.arange(B) * KP)[:, None]
    cnt = np.bincount(ids.ravel(), weights=w.ravel(), minlength=B * KP).reshape(B, K, P)
    tot = cnt.sum((1, 2), keepdims=True); pj = cnt / np.maximum(tot, 1)
    pc = pj.sum(2, keepdims=True); pp = pj.sum(1, keepdims=True)
    with np.errstate(all="ignore"):
        t = np.where(pj > 0, pj * np.log(pj / (pc * pp)), 0.0)
    return t.sum((1, 2))

def acc_loo(cols, poss, K):
    """Exactitud 'leave-one-out' de predecir el color de una cuerda con el color modal de su columna (misma posicion)
    menos la de predecir con el modal del quipu. cols: (B,n)."""
    B, n = cols.shape; ids = cols * P + poss[None] + (np.arange(B) * K * P)[:, None]
    cnt = np.bincount(ids.ravel(), minlength=B * K * P).reshape(B, K, P).astype(float)
    # columna: cnt[b,:,pos_i]
    cp = np.take_along_axis(cnt, np.broadcast_to(poss[None, None, :], (B, K, n)), axis=2)  # (B,K,n)
    own = np.take_along_axis(cp, cols[:, None, :], axis=1)[:, 0, :] - 1
    oth = np.where(np.arange(K)[None, :, None] == cols[:, None, :], -1, cp).max(1)
    hit_col = np.where(own > oth, 1.0, np.where(own == oth, 0.5, 0.0)).mean(1)
    tot = cnt.sum(2); ownb = np.take_along_axis(tot, cols, axis=1) - 1
    othb = np.where(np.arange(K)[None, :, None] == cols[:, None, :], -1, tot[:, :, None]).max(1)
    hit_b = np.where(ownb > othb, 1.0, np.where(ownb == othb, 0.5, 0.0)).mean(1)
    return hit_col - hit_b

def entropia(c):
    p = np.bincount(c) / len(c); p = p[p > 0]; return -(p * np.log(p)).sum()

def t1(codes, pos0, gsz, gid, sizes, rng, B1=B_N1, B2=B_N2, B3=B_N3):
    """codes: -1 enmascarado; pos0: posicion 0-based; gsz: tamano de grupo; gid: grupo; sizes: tamanos de todos los grupos en orden."""
    keep = (codes >= 0) & (gsz >= 3)
    if keep.sum() < 12: return None
    c = codes[keep]; p = np.minimum(pos0[keep], P - 1); g = gid[keep]
    if len(set(c)) < 2 or len(set(g)) < 3: return None
    K = codes.max() + 1; n = len(c)
    obs = mi_batch(c[None], p[None], np.ones((1, n)), K)[0]; H = entropia(c)
    out = dict(n=n, K=K, ngrupos=len(set(g)), MI=obs, H=H)
    one = np.ones((1, n))
    # N1: permuta colores en todo el quipu
    i1 = m.idx_perm(n, None, B1, rng)
    n1 = mi_batch(c[i1], p, np.ones((B1, n)), K)
    # N2: permuta colores dentro de cada grupo (conserva composicion de cada grupo)
    i2 = m.idx_perm(n, g, B2, rng)
    n2 = mi_batch(c[i2], p, np.ones((B2, n)), K)
    ag = acc_loo(c[None], p, K)[0]; agn = acc_loo(c[i2[:200]], p, K)
    out.update(acc_gain=ag, acc_gain_N2mean=agn.mean(), acc_gain_p=m.mid_p(ag, agn))
    # N3: permuta el orden de los GRUPOS completos (tamanos) conservando la secuencia de colores
    N = len(codes); sz = np.array(sizes); val = codes >= 0
    posm = np.empty((B3, N), int); keepm = np.empty((B3, N))
    for b in range(B3):
        s = rng.permutation(sz)
        pp = np.concatenate([np.arange(k) for k in s]); gg = np.repeat(s, s)
        posm[b] = np.minimum(pp, P - 1); keepm[b] = val & (gg >= 3)
    n3 = mi_batch(np.where(val, codes, 0), posm, keepm, K)
    for nm, nu in (("N1", n1), ("N2", n2), ("N3", n3)):
        sd = nu.std()
        out[nm + "_z"] = (obs - nu.mean()) / sd if sd > 0 else np.nan
        out[nm + "_p"] = m.mid_p(obs, nu)
        out[nm + "_nMI"] = (obs - nu.mean()) / H
    # regularidad de tamanos de grupo
    gs = pd.Series(sz[sz >= 3]); out["frac_tam_modal"] = gs.value_counts(normalize=True).iloc[0] if len(gs) else np.nan
    return out

def variantes(d):
    full = d.ckey.where(d.ckey.notna(), None)
    return {
        "full": full.tolist(),
        "full_sin_primera": [k if p > 1 else None for k, p in zip(d.ckey, d.pos)],
        "full_sin_extremos": [k if 1 < p < g else None for k, p, g in zip(d.ckey, d.pos, d.gsize)],
        "natural": [k if nd == "nat" else None for k, nd in zip(d.ckey, d.nd)],
        "tinte": [k if nd == "tinte" else None for k, nd in zip(d.ckey, d.nd)],
        "bin_nat_tinte": [{"nat": "N", "tinte": "T"}.get(nd) for nd in d.nd],
        "bin_estricto": [{"nat": "N", "tinte": "T"}.get(nd) for nd in d.nd2],
    }

def main():
    c, q = m.cargar(); pe = c[c.nivel == 0]
    rows = []
    for ik, (kfg, d) in enumerate(pe.groupby("kfg")):
        rng = np.random.default_rng([m.SEED, 1, ik])
        d = d.sort_values("orden"); pos0 = (d.pos.values - 1).astype(int)
        gsz = d.gsize.values; gid = d.grupo.values
        sizes = d.groupby("grupo", sort=False).size().tolist()
        for vn, lab in variantes(d).items():
            codes, _ = codifica(lab)
            r = t1(codes, pos0, gsz, gid, sizes, rng)
            if r: rows.append(dict(kfg=kfg, col=d.col.iloc[0], variante=vn, **r))
        if ik % 100 == 0: print("T1 mi", ik, flush=True)
    R = pd.DataFrame(rows); R.to_csv(m.OUT + r"\resultados_t1_mi.csv", index=False)
    # banderas por quipu (BH dentro de cada variante y nulo sobre quipus elegibles)
    for nm in ("N1", "N2", "N3"):
        R[nm + "_q"] = np.nan
        for vn in R.variante.unique():
            ix = R.index[(R.variante == vn) & R[nm + "_p"].notna()]
            R.loc[ix, nm + "_q"] = m.bh(R.loc[ix, nm + "_p"].values)
    R["columna_fuerte"] = (R.N2_q < .05) & (R.N3_q < .05) & (R.N2_nMI >= .25)
    R.to_csv(m.OUT + "/resultados_t1_mi.csv", index=False)
    print(R.groupby("variante").agg(n=("kfg", "size"), N2_sig=("N2_q", lambda x: (x < .05).sum()), N3_sig=("N3_q", lambda x: (x < .05).sum()),
          fuerte=("columna_fuerte", "sum"), nmi_med=("N2_nMI", "median"), nmi_p90=("N2_nMI", lambda x: x.quantile(.9))).round(3).to_string())
    # metaanalisis
    M = []
    for vn in R.variante.unique():
        d0 = R[R.variante == vn]
        for sub, d in (("todos", d0), ("regulares(>=60% grupos mismo tamano, >=4 grupos)", d0[(d0.frac_tam_modal >= .6) & (d0.ngrupos >= 4)])):
            for nm in ("N1", "N2", "N3"):
                x = pd.DataFrame(dict(kfg=d.kfg, eff=d[nm + "_nMI"], z=d[nm + "_z"], p=d[nm + "_p"]))
                M.append(dict(variante=vn, subconjunto=sub, nulo=nm, **m.meta(x, dos_colas=False)))
    M = pd.DataFrame(M)
    M["q_bh_stouffer"] = m.bh(M.p_stouffer.fillna(1).values)
    M.to_csv(m.OUT + r"\resultados_t1_meta.csv", index=False)
    print(M[["variante", "subconjunto", "nulo", "n", "eff_med", "z_stouffer", "p_stouffer", "frac_p05", "p_exceso_p05", "n_bh05"]].round(4).to_string())
    return R

if __name__ == "__main__":
    main()
