# -*- coding: utf-8 -*-
"""01 - Construye la tabla de analisis del diseno "grupos de tamano fijo".

Unidad: quipu.  Estrato: (quipu, k) con >=4 grupos de tamano k y datos completos.
Dentro de cada grupo, pos = rango de la cuerda (0..k-1) segun `orden`.
Objetivo: describir cuanto varia el color ENTRE GRUPOS en una misma posicion.
Salidas: base_color_pos.csv, diseno_resumen.csv
"""
import re
import numpy as np
import pandas as pd

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_color_posicion"

# ---------- datos ----------
c = pd.read_csv(RAIZ + r"/analisis/datos/cuerdas.csv", low_memory=False)
c["col"] = c.color.astype(str).map(lambda s: re.sub(r"\([^)]*\)", "", s))
c["ausente"] = (c.valor.fillna(-1) == 0) & c.nudos.fillna("").eq("")
c["L"] = pd.to_numeric(c.largo, errors="coerce")
c["nrac"] = c.nudos.fillna("").map(lambda s: 0 if s == "" else s.count(";") + 1)

# grupos: se define sobre TODAS las cuerdas nivel 0 (para no correr la posicion)
p0 = c[c.nivel == 0].sort_values(["kfg", "orden"]).copy()
p0["gsize"] = p0.groupby(["kfg", "grupo"]).orden.transform("size")
p0["pos"] = p0.groupby(["kfg", "grupo"]).cumcount()

# solo grupos completos (color y valor en todas sus cuerdas)
ok = p0.groupby(["kfg", "grupo"]).apply(
    lambda g: g.color.notna().all() and g.valor.notna().all(), include_groups=False)
ok.name = "completo"
p0 = p0.merge(ok, left_on=["kfg", "grupo"], right_index=True, how="left")

# tamanos k con >=4 grupos
cnt = (p0[p0.completo].groupby(["kfg", "gsize"]).grupo.nunique()
       .rename("ngrupos").reset_index())
eleg = cnt[cnt.ngrupos >= 4].rename(columns={"gsize": "k"}).copy()
p0 = p0.merge(eleg[["kfg", "k"]], left_on=["kfg", "gsize"],
              right_on=["kfg", "k"], how="inner")
p0 = p0[p0.completo].copy()

# ---------- colores: >=3 cuerdas en el quipu, resto OTRO ----------
vc = p0.groupby(["kfg", "col"]).size().rename("ncol").reset_index()
p0 = p0.merge(vc, on=["kfg", "col"], how="left")
p0["col3"] = np.where(p0.ncol >= 3, p0.col, "OTRO")
p0["y"] = np.log1p(p0.valor.astype(float))

# ---------- totales de grupo ----------
p0["es_total"] = False
for (k, g), idx in p0.groupby(["kfg", "grupo"]).groups.items():
    v = p0.loc[idx, "valor"].astype(float)
    if len(idx) >= 4 and v.sum() > 0:
        tot = v.sum()
        p0.loc[idx[v.values * 2 == tot], "es_total"] = True

# ---------- copias: componentes de filas_alineadas ----------
cp = pd.read_csv(RAIZ + "/analisis/14_copias/filas_alineadas.csv", low_memory=False)
pairs = cp[["A", "B"]].dropna().drop_duplicates().values.tolist()
padre = {}
def find(x):
    padre.setdefault(x, x)
    while padre[x] != x:
        padre[x] = padre[padre[x]]
        x = padre[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        padre[rb] = ra
for a, b in pairs:
    union(a, b)
fams = {}
for x in list(padre):
    fams.setdefault(find(x), []).append(x)

# representante = el miembro con mas cuerdas nivel 0 con color y valor
n0 = p0.groupby("kfg").size()
rep = {}
for f, members in fams.items():
    members = [m for m in members if m in n0.index]
    if members:
        rep[f] = max(members, key=lambda m: n0[m])
p0["familia"] = p0.kfg.map({m: f for f, ms in fams.items() for m in ms})
p0["es_rep"] = p0.apply(lambda r: rep.get(r.familia) == r.kfg
                        if pd.notna(r.familia) else True, axis=1)
p0["en_copias"] = p0.familia.notna()

# ---------- descriptivo: variacion de color por posicion ----------
# fraccion de posiciones (kfg,k,pos) con >=2 colores entre grupos
vp = (p0.groupby(["kfg", "k", "pos"]).col3.nunique().rename("ncol_pos").reset_index())
vp["variable"] = vp.ncol_pos >= 2
res = []
for (kfg, k), g in vp.groupby(["kfg", "k"]):
    res.append(dict(kfg=kfg, k=k, npos=len(g), nvar=int(g.variable.sum()),
                    frac_var=g.variable.mean()))
DES = pd.DataFrame(res)
DES["ngrupos"] = DES.set_index(["kfg", "k"]).index.map(
    eleg.set_index(["kfg", "k"]).ngrupos)
DES.to_csv(OUT + r"\diseno_resumen.csv", index=False)

# identificabilidad: variacion dentro de grupo (color no colineal con grupo)
wg = (p0.groupby(["kfg", "grupo"]).col3.nunique() > 1).groupby("kfg").any()
DES["var_dentro_grupo"] = DES.kfg.map(wg)
DES["var_entre_grupos"] = DES.kfg.map(DES.groupby("kfg").frac_var.max() > 0)

p0.to_csv(OUT + r"\base_color_pos.csv", index=False)

print("quipus con >=4 grupos de igual k:", p0.kfg.nunique())
print("estratos (kfg,k):", len(DES), "| cuerdas:", len(p0))
print("k:", DES.k.value_counts().sort_index().to_dict())
print("posiciones con >=2 colores: %d/%d = %.3f" %
      (vp.variable.sum(), len(vp), vp.variable.mean()))
print("por quipu: mediana frac posiciones variables = %.3f (P25 %.3f P75 %.3f)" %
      (DES.groupby('kfg').frac_var.mean().median(),
       DES.groupby('kfg').frac_var.mean().quantile(.25),
       DES.groupby('kfg').frac_var.mean().quantile(.75)))
print("quipus con alguna posicion variable:", int((DES.groupby('kfg').frac_var.max() > 0).sum()))
print("quipus con color variable dentro de grupo:", int(wg.sum()))
print("ambos (A y B identificables):", int(((DES.groupby('kfg').frac_var.max() > 0) & wg).sum()))
print("ausentes:", int(p0.ausente.sum()), "| totales:", int(p0.es_total.sum()),
      "| en copias:", int(p0.en_copias.sum()))
print("colores por quipu (mediana):", p0.groupby('kfg').col3.nunique().median())
print(DES.groupby('kfg').frac_var.mean().describe().round(3).to_string())
