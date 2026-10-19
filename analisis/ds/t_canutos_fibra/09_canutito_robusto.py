"""
Canutitos, version robusta:
  - efecto por quipu medido como AUC (rango) para no dejar que un quipu domine
  - estadistico = media de (AUC-0.5) sobre los quipus con ambas clases
  - nulo: permutacion DENTRO de cada quipu
  - paleta: los canutitos usan colores distintos de las cuerdas?
"""
import os, sqlite3
import numpy as np
import pandas as pd
from scipy import stats

BASE = r"."
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20241018)
NPERM = 20000

q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
cord = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)
con = sqlite3.connect(os.path.join(BASE, "data", "external", "open-khipu-repository",
                                   "data", "khipu.db"))
canit = pd.read_sql("select CANUTITO_ID,CORD_ID from canutito", con)
colc = pd.read_sql("select CANUTITO_ID,COLOR_CD_1,CANUTITO_FIBER from ascher_canutito_color", con)

kids = q.loc[q.n_canutito > 0, "KHIPU_ID"].tolist()
c = cord[cord.KHIPU_ID.isin(kids)].copy()
c["can"] = c.CORD_ID.isin(canit.CORD_ID).astype(int)
c["vpos"] = (c.valor.fillna(0) > 0).astype(int)
c["blanco"] = c.color.fillna("").astype(str).str.startswith("W").astype(int)
c["logv"] = np.log10(c.valor.clip(lower=1))


def auc(x, y):
    """AUC de x separando y=1 vs y=0."""
    if len(np.unique(y)) < 2:
        return np.nan
    r = stats.rankdata(x)
    n1 = (y == 1).sum()
    n0 = (y == 0).sum()
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def test_auc(df, var, reps=NPERM):
    d = df[[var, "can", "KHIPU_ID"]].dropna()
    obs_k, w = [], []
    for kid, g in d.groupby("KHIPU_ID"):
        if g.can.nunique() < 2 or len(g) < 15:
            continue
        a = auc(g[var].values, g.can.values)
        if not np.isnan(a):
            obs_k.append(a - 0.5)
            w.append(len(g))
    obs = np.mean(obs_k)
    groups = [g for _, g in d.groupby("KHIPU_ID") if g.can.nunique() > 1 and len(g) >= 15]
    cnt = 0
    for _ in range(reps):
        s = []
        for g in groups:
            yv = g.can.values.copy()
            rng.shuffle(yv)
            a = auc(g[var].values, yv)
            if not np.isnan(a):
                s.append(a - 0.5)
        if abs(np.mean(s)) >= abs(obs):
            cnt += 1
    return obs, (cnt + 1) / (reps + 1), np.mean([o + .5 for o in obs_k]), len(obs_k)


print("=" * 72)
print("CANUTITO: MARCADO SELECTIVO (AUC por quipu, nulo intragrupo)")
rows = []
for var in ["vpos", "logv", "blanco", "CORD_LEVEL", "CORD_LENGTH"]:
    e, p, mauc, nk = test_auc(c, var)
    rows.append(dict(variable=var, efecto_auc_medio=mauc, dif=mauc - .5,
                     p_perm=p, n_quipus=nk))
R = pd.DataFrame(rows)
print(R.round(4).to_string(index=False))
R.to_csv(os.path.join(OUT, "canutito_tests_auc.csv"), index=False)

print("\nAUC por quipu y variable (0.5 = sin efecto):")
tab = []
for var in ["vpos", "logv", "blanco", "CORD_LENGTH"]:
    for kid, g in c.groupby("KHIPU_ID"):
        if g.can.nunique() < 2 or len(g) < 15:
            continue
        tab.append(dict(quipu=int(kid), variable=var, n=len(g), n_can=int(g.can.sum()),
                        auc=round(auc(g[var].values, g.can.values), 3)))
T = pd.DataFrame(tab).pivot(index="quipu", columns="variable", values="auc")
print(T.to_string())
print("\n(blanco: 4 quipus tienen 0-4 cuerdas blancas; el AUC es inestable ahi)")

print("\n" + "=" * 72)
print("PALETA: los canutitos usan colores que las cuerdas no usan?")
m = canit.merge(colc, on="CANUTITO_ID", how="left")
nuevos = []
for kid in kids:
    cc = set(m.loc[m.CORD_ID.isin(cord.loc[cord.KHIPU_ID == kid, "CORD_ID"]), "COLOR_CD_1"].dropna())
    cu = set(cord.loc[cord.KHIPU_ID == kid, "color"].dropna().astype(str))
    cu = {x for s in cu for x in s.replace(":", "-").replace("/", "-").split("-") if x}
    nuevos.append(dict(quipu=int(kid), colores_canutito=len(cc), colores_cuerda=len(cu),
                       canutito_fuera_de_cuerda=len(cc - cu) if cc else 0))
print(pd.DataFrame(nuevos).to_string(index=False))
print("\nfibra del canutito:", colc.CANUTITO_FIBER.value_counts().to_dict())
print("colores de canutito mas frecuentes:", colc.COLOR_CD_1.value_counts().head(8).to_dict())
