# -*- coding: utf-8 -*-
"""02 - Descriptivo: cuanto se ata el color a la posicion y cuantos "cambios" hay.

Universo: k>=2 (k=1 no permite controlar posicion).
- fraccion de posiciones con color constante / modal >=80%
- informacion mutua normalizada color~posicion, frente a barajado global
- pares de grupos del mismo k con los MISMOS colores en distinto orden ("swap")
Salidas: descriptivo_pos.csv, swaps.csv
"""
import numpy as np
import pandas as pd

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"
rng = np.random.default_rng(20261018)

B = pd.read_csv(OUT + r"\base_color_pos.csv", low_memory=False)
B = B[B.k >= 2].copy()

# ---------- 1. color por posicion ----------
pos = B.groupby(["kfg", "k", "pos"]).col3.agg(["nunique", "size", "count"]).reset_index()
pos = pos.rename(columns={"nunique": "ncol", "size": "ngrupos"})
# modal share
mod = B.groupby(["kfg", "k", "pos", "col3"]).size().rename("n").reset_index()
mod = mod.sort_values(["kfg", "k", "pos", "n"], ascending=[True, True, True, False])
top = mod.groupby(["kfg", "k", "pos"]).head(1).copy()
top = top.merge(pos[["kfg", "k", "pos", "ngrupos", "ncol"]], on=["kfg", "k", "pos"])
top["share"] = top.n / top.ngrupos


# informacion mutua color~posicion por quipu
def nmi(df, pcol="posk"):
    ct = pd.crosstab(df[pcol], df.col3).values.astype(float)
    n = ct.sum()
    if n == 0:
        return np.nan
    px = ct.sum(1) / n
    py = ct.sum(0) / n
    pxy = ct / n
    with np.errstate(divide="ignore", invalid="ignore"):
        mi = np.nansum(pxy * np.log(pxy / (px[:, None] * py[None, :])))
    hx = -np.nansum(px * np.log(px))
    hy = -np.nansum(py * np.log(py))
    den = min(hx, hy)
    return mi / den if den > 1e-12 else np.nan

rows = []
for kfg, g in B.groupby("kfg"):
    # posicion global dentro del quipu (para MI usar (k,pos) como categoria)
    gg = g.copy()
    gg["posk"] = gg.k.astype(str) + "_" + gg.pos.astype(str)
    obs = nmi(gg)
    nulls = []
    for _ in range(50):
        sh = gg.copy()
        sh["col3"] = rng.permutation(sh.col3.values)
        nulls.append(nmi(sh))
    rows.append(dict(kfg=kfg, nmi=obs, nmi_null=np.nanmean(nulls),
                     n=len(g), k=g.k.iloc[0]))
MI = pd.DataFrame(rows)

# resumen de posiciones
posr = top.groupby(["kfg", "k"]).agg(
    npos=("pos", "size"), frac_const=("ncol", lambda s: np.mean(s == 1)),
    frac_mod80=("share", lambda s: np.mean(s >= 0.80)),
    share_med=("share", "median")).reset_index()

print("=== universo k>=2 ===")
print("quipus:", B.kfg.nunique(), "| cuerdas:", len(B), "| estratos:", len(posr))
print("posiciones:", len(top), "| color constante: %.3f | modal>=80%%: %.3f | modal mediana %.3f" %
      (np.mean(top.ncol == 1), np.mean(top.share >= .8), top.share.median()))
print("por quipu, mediana frac pos constantes: %.3f (P25 %.3f P75 %.3f)" %
      (posr.groupby("kfg").frac_const.mean().median(),
       posr.groupby("kfg").frac_const.mean().quantile(.25),
       posr.groupby("kfg").frac_const.mean().quantile(.75)))
print("NMI color~posicion: mediana %.3f | nulo %.3f | diferencia %.3f" %
      (MI.nmi.median(), MI.nmi_null.median(), (MI.nmi - MI.nmi_null).median()))
print("NMI por k:")
print(MI.groupby("k").nmi.median().round(3).to_string())

# ---------- 2. pares swap ----------
sw = []
for (kfg, k), g in B.groupby(["kfg", "k"]):
    grupos = list(g.grupo.unique())
    if len(grupos) < 2:
        continue
    seq = {}
    for u in grupos:
        h = g[g.grupo == u].sort_values("pos")
        seq[u] = h.col3.tolist()
    for i in range(len(grupos)):
        for j in range(i + 1, len(grupos)):
            a, b = grupos[i], grupos[j]
            sa, sb = seq[a], seq[b]
            if sorted(sa) != sorted(sb) or sa == sb:
                continue
            # posiciones donde se intercambian dos colores
            for x in range(len(sa)):
                for z in range(x + 1, len(sa)):
                    if sa[x] == sb[z] and sa[z] == sb[x] and sa[x] != sa[z]:
                        ya = g[(g.grupo == a) & (g.pos == x)].iloc[0]
                        yb1 = g[(g.grupo == b) & (g.pos == x)].iloc[0]
                        yaz = g[(g.grupo == a) & (g.pos == z)].iloc[0]
                        ybz = g[(g.grupo == b) & (g.pos == z)].iloc[0]
                        if any(q.ausente for q in (ya, yb1, yaz, ybz)):
                            continue
                        d_pos = (ya.y - yb1.y) ** 2 + (yaz.y - ybz.y) ** 2
                        d_col = (ya.y - ybz.y) ** 2 + (yaz.y - yb1.y) ** 2
                        sw.append(dict(kfg=kfg, k=k, grupoA=a, grupoB=b, pos1=x, pos2=z,
                                       color1=sa[x], color2=sa[z],
                                       d_pos=d_pos, d_col=d_col,
                                       gana="color" if d_col < d_pos else "posicion"))
S = pd.DataFrame(sw)
S.to_csv(OUT + r"\swaps.csv", index=False)
print("\n=== swaps ===")
print("pares de posiciones intercambiadas:", len(S), "| quipus:", S.kfg.nunique() if len(S) else 0)
if len(S):
    print("gana color: %d (%.3f) | gana posicion: %d" %
          ((S.gana == "color").sum(), (S.gana == "color").mean(), (S.gana == "posicion").sum()))
    print(S.groupby("color1").size().sort_values(ascending=False).head(8).to_string())

posr.to_csv(OUT + r"\descriptivo_pos.csv", index=False)
MI.to_csv(OUT + r"\nmi_color_pos.csv", index=False)
