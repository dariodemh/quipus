"""Parsea `nudos` en racimos y marca violaciones de la convencion decimal.
Salidas (en esta carpeta): racimos.csv, cuerdas_flags.csv, quipus_flags.csv
"""
import re, math
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
d = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", keep_default_na=False, low_memory=False)
R = re.compile(r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Z])\)(?:,(-?\d+))?$")
ESTAND = {"S", "L", "E"}

rows = []
for i, r in d.iterrows():
    if not r.nudos:
        continue
    for j, k in enumerate(r.nudos.split(";")):
        m = R.match(k)
        if not m:
            rows.append(dict(i=i, j=j, tipo="?", n=np.nan, pos=np.nan, dir="?", ap=np.nan))
            continue
        n, t, p, dr, v = m.groups()
        rows.append(dict(i=i, j=j, tipo=t, n=int(n), pos=float(p), dir=dr, ap=float(v) if v is not None else np.nan))
c = pd.DataFrame(rows)
c = c.join(d[["kfg", "cuerda", "orden", "nivel", "grupo", "valor", "color", "union", "torsion", "largo"]], on="i")
c["valor"] = pd.to_numeric(c.valor, errors="coerce")
ncl = c.groupby("i").j.transform("max") + 1
c["ncl"] = ncl
c["ultimo"] = c.j == ncl - 1

# nivel decimal: S -> log10(ap/n) si es potencia de 10; el resto = unidades (0)
def nivel(r):
    if r.tipo == "S":
        if not (r.n > 0 and r.ap == r.ap and r.ap > 0):
            return np.nan
        x = math.log10(r.ap / r.n)
        return round(x) if abs(x - round(x)) < 1e-9 else np.nan
    if r.tipo in ("L", "E", "EE", "LL", "BL", "SP", "TF", "U"):
        return 0
    return np.nan
c["niv"] = c.apply(nivel, axis=1)

# --- flags a nivel de racimo
c["v_nofig_unid"] = (c.tipo.isin(["L", "E"])) & (~c.ultimo)           # L/E con algo debajo (nudo "inferior" de Hyland)
c["v_S_unid_debajo"] = (c.tipo == "S") & (c.niv == 0) & (~c.ultimo)   # S de unidades con algo debajo
c["v_over9"] = (c.tipo == "S") & (c.n > 9)
c["v_L1"] = (c.tipo == "L") & (c.n == 1)
c["v_L10"] = (c.tipo == "L") & (c.n >= 10)
c["v_Emulti"] = (c.tipo == "E") & (c.n > 1)
c["v_tiporaro"] = ~c.tipo.isin(ESTAND)
c["v_Spot"] = (c.tipo == "S") & c.niv.isna() & c.ap.notna()           # S cuyo aporte no es n*10^k
c["v_sinvalor"] = c.ap.isna()
# orden de niveles (arriba->abajo debe ser estrictamente decreciente)
def orden_mal(g):
    g = g.sort_values("j"); l = g.niv.values
    mal = np.zeros(len(g), bool)
    for a in range(1, len(g)):
        if not (np.isnan(l[a]) or np.isnan(l[a - 1])) and l[a] >= l[a - 1] and not (l[a] == 0 and l[a - 1] == 0 and False):
            mal[a] = True
    return pd.Series(mal, index=g.index)
c["v_orden"] = c.groupby("i", group_keys=False).apply(orden_mal)

# --- bandas posicionales por quipu: (kfg, nivel>0, niv); valla de Tukey con holgura minima
def bandas(g):
    out = pd.Series(False, index=g.index); otro = pd.Series(False, index=g.index)
    g = g[g.niv.notna()]
    fen = {}
    for (sub, lv), h in g.groupby([g.nivel > 0, "niv"]):
        if len(h) < 8:
            continue
        q1, q3 = h.pos.quantile([.25, .75]); w = max(1.5 * (q3 - q1), 1.5)
        fen[(sub, lv)] = (q1 - w, q3 + w, h.pos.median())
    for ix, r in g.iterrows():
        f = fen.get((r.nivel > 0, r.niv))
        if f is None:
            continue
        if not (f[0] <= r.pos <= f[1]):
            out[ix] = True
            otro[ix] = any(k[0] == (r.nivel > 0) and k[1] != r.niv and v[0] <= r.pos <= v[1] for k, v in fen.items())
    return pd.DataFrame({"v_banda": out[g.index], "v_banda_otro": otro[g.index]})
bd = c.groupby("kfg", group_keys=False).apply(bandas)
c = c.join(bd)
c[["v_banda", "v_banda_otro"]] = c[["v_banda", "v_banda_otro"]].fillna(False).astype(bool)
c["nether"] = c.v_nofig_unid | c.v_S_unid_debajo
c.to_csv(AQUI / "racimos.csv", index=False)

# --- a nivel de cuerda
fl = [x for x in c.columns if x.startswith("v_")] + ["nether"]
cu = c.groupby("i")[fl].any()
# valor vs suma de aportes (solo cuerdas con todos los aportes)
suma = c.groupby("i").ap.apply(lambda s: s.sum() if s.notna().all() else np.nan)
cu["v_valor_dist"] = (suma != pd.to_numeric(d.valor.loc[suma.index], errors="coerce"))
# direccion mixta: S y Z presentes
dirs = c.groupby("i").dir.apply(set)
cu["dir_mixta"] = dirs.apply(lambda s: {"S", "Z"} <= s)
cu["con_nudos"] = True
cu = d[["kfg", "orden", "cuerda", "nivel", "valor", "color", "union", "terminacion", "notas"]].join(cu)
for x in fl + ["v_valor_dist", "dir_mixta"]:
    cu[x] = cu[x].fillna(False).astype(bool)
cu["con_nudos"] = cu.con_nudos.fillna(False).astype(bool)
cu["v_alt"] = False  # Alt_Value vacio en los 57 818 registros (ver informe)
cu.to_csv(AQUI / "cuerdas_flags.csv", index=False)

# --- a nivel de quipu
g = cu[cu.con_nudos].groupby("kfg")
q = pd.DataFrame({"n_cuerdas_nudos": g.size()})
for x in [x for x in cu.columns if x.startswith("v_") or x in ("nether", "dir_mixta")]:
    q["n_" + x] = g[x].sum()
    q["f_" + x] = q["n_" + x] / q.n_cuerdas_nudos
q.to_csv(AQUI / "quipus_flags.csv")
print(q.shape, c.shape)
print(cu[cu.con_nudos][[x for x in cu.columns if x.startswith("v_") or x in ("nether", "dir_mixta")]].sum())
print((cu[cu.con_nudos][["v_nofig_unid", "v_S_unid_debajo", "v_over9", "v_L1", "v_L10", "v_Emulti", "v_tiporaro", "v_Spot", "v_orden", "v_banda", "v_valor_dist"]].mean() * 100).round(2))
