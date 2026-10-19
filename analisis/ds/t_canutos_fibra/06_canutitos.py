"""
Canutitos (envolturas de hilo en el EXTREMO de la cuerda, terminacion TT):
marcan cuerdas selectivamente?  Nulo: permutar la etiqueta 'tiene canutito'
DENTRO de cada quipu (estratificado), 20 000 veces.
Estadistico: suma estandarizada de las diferencias observadas entre quipus.
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
canit = pd.read_sql("select CANUTITO_ID,CORD_ID,START_POS,END_POS,CANUTITO_LENGTH from canutito", con)
cols = pd.read_sql("select CANUTITO_ID,COLOR_CD_1,CANUTITO_FIBER from ascher_canutito_color", con)
print("canutitos:", len(canit), " con color:", len(cols), " colores distintos:",
      cols.COLOR_CD_1.nunique())
print(cols.COLOR_CD_1.value_counts().head(10).to_dict())

kids = q.loc[q.n_canutito > 0, "KHIPU_ID"].tolist()
c = cord[cord.KHIPU_ID.isin(kids)].copy()
c["canutito"] = c.CORD_ID.isin(canit.CORD_ID).astype(int)
c["vpos"] = (c.valor.fillna(0) > 0).astype(int)
c["blanco"] = c.color.fillna("").astype(str).str.startswith("W").astype(int)
c["logv"] = np.log10(c.valor.clip(lower=1))

print("\ncobertura por quipu:")
print(c.groupby("KHIPU_ID").agg(n=("CORD_ID", "size"), marcadas=("canutito", "sum"),
                                frac=("canutito", "mean")).round(3).to_string())

print("\nposicion del canutito en la cuerda (cm desde el inicio / largo):")
cc = canit.merge(c[["CORD_ID", "CORD_LENGTH", "KHIPU_ID"]], on="CORD_ID")
cc["rel"] = cc.START_POS / cc.CORD_LENGTH.replace(0, np.nan)
print(cc.rel.describe().round(3).to_string())
print("largo del canutito (cm):", canit.CANUTITO_LENGTH.describe().round(2).to_dict())

# ------------------------------------------------------------- tests
def stratified_test(df, var, y="canutito", reps=NPERM):
    d = df[[var, y, "KHIPU_ID"]].dropna()
    if var in ("vpos", "blanco"):
        stat = lambda s: s.mean()
    else:
        stat = lambda s: np.median(s) if len(s) else np.nan
    obs_k, sizes = [], []
    for kid, g in d.groupby("KHIPU_ID"):
        a = g.loc[g[y] == 1, var]
        b = g.loc[g[y] == 0, var]
        if len(a) < 3 or len(b) < 3:
            continue
        obs_k.append(stat(a) - stat(b))
        sizes.append((len(a), len(b)))
    if not obs_k:
        return np.nan, np.nan, 0
    obs_k = np.array(obs_k)
    obs = obs_k.sum()
    # nulo: permutar dentro de cada quipu
    groups = [g for _, g in d.groupby("KHIPU_ID")]
    cnt = 0
    for _ in range(reps):
        s = 0.0
        for g, (na, nb) in zip(groups, sizes):
            yv = g[y].values.copy()
            rng.shuffle(yv)
            a = g[var].values[yv == 1]
            b = g[var].values[yv == 0]
            if len(a) < 2 or len(b) < 2:
                continue
            s += stat(a) - stat(b)
        if abs(s) >= abs(obs):
            cnt += 1
    return obs, (cnt + 1) / (reps + 1), len(obs_k)


res = []
for var in ["vpos", "logv", "blanco", "CORD_LEVEL", "CORD_LENGTH"]:
    obs, p, nk = stratified_test(c, var)
    res.append(dict(variable=var, efecto=obs, p_perm=p, n_quipus=nk))
R = pd.DataFrame(res)
print("\n" + "=" * 70)
print("MARCADO SELECTIVO (nulo: permutacion dentro de cada quipu)")
print(R.round(4).to_string(index=False))
print("  vpos: diferencia en la proporcion de cuerdas con valor>0")
print("  logv: diferencia de mediana de log10(valor)")
print("  blanco: diferencia en la proporcion de cuerdas blancas")
R.to_csv(os.path.join(OUT, "canutito_tests.csv"), index=False)

# por quipu, la senal mas fuerte
print("\ndetalle por quipu (proporcion con valor>0 y blancura):")
tab = c.groupby(["KHIPU_ID", "canutito"]).agg(n=("CORD_ID", "size"),
                                              pval_pos=("vpos", "mean"),
                                              blanco=("blanco", "mean"),
                                              med_valor=("valor", "median")).round(2)
print(tab.to_string())

# color del canutito vs color de la cuerda
m = canit.merge(cols, on="CANUTITO_ID").merge(
    cord[["CORD_ID", "color", "valor"]], on="CORD_ID")
m["cuerda_color1"] = m.color.fillna("").astype(str).str.split(":").str[0].str.split("-").str[0]
print("\ncoincidencia color canutito == primer color de la cuerda: %.1f%% (n=%d)"
      % (100 * (m.COLOR_CD_1 == m.cuerda_color1).mean(), len(m)))
print(pd.crosstab(m.COLOR_CD_1, m.cuerda_color1).to_string())
