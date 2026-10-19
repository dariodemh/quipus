"""P3: efecto del transcriptor sobre el vocabulario de color (diseno.md §4).

Salidas: p3_quipu.csv (alfabeto por quipu), p3_pruebas.csv, p3_vocabulario.csv, p3_mismo_objeto.csv,
p3_nmi_grupo.csv
"""
from collections import Counter

import numpy as np
import pandas as pd
from scipy.stats import kruskal

import comun24 as C

rng = np.random.default_rng(C.SEED)
NREP = 9999
RARE = 40
c = C.cargar()
cc = c[c.col != ""]
q = pd.read_csv(C.DAT / "quipus.csv", keep_default_na=False)
con = C.okr()
km = pd.read_sql("select INVESTIGATOR_NUM kfg, lower(CREATED_BY) captura from khipu_main", con)
con.close()
km = km.drop_duplicates("kfg")

rows = []
for k, x in cc.groupby("kfg"):
    cols = x.col.values
    r = dict(kfg=k, reg=x.reg.iloc[0], n=len(cols), alfabeto=len(set(cols)), bases=len(set(x.base)),
             frac_comp=round(x.comp.mean(), 3), frac_W=round((x.base == "W").mean(), 3))
    if len(cols) >= RARE:
        r["alf_rare"] = np.mean([len(set(rng.choice(cols, RARE, replace=False))) for _ in range(200)])
        r["bases_rare"] = np.mean([len(set(rng.choice(x.base.values, RARE, replace=False))) for _ in range(200)])
    rows.append(r)
A = pd.DataFrame(rows).merge(q[["kfg", "region", "procedencia"]], on="kfg", how="left").merge(km, on="kfg", how="left")
A.to_csv(C.AQUI / "p3_quipu.csv", index=False)


def kw_perm(df, var, lab, min_n=5):
    d = df.dropna(subset=[var])
    keep = d[lab].value_counts()
    d = d[d[lab].isin(keep[keep >= min_n].index)]
    if d[lab].nunique() < 2:
        return None
    gs = d[lab].values
    v = d[var].values
    H = kruskal(*[v[gs == g] for g in np.unique(gs)]).statistic
    nul = []
    for _ in range(NREP):
        p = rng.permutation(gs)
        nul.append(kruskal(*[v[p == g] for g in np.unique(p)]).statistic)
    med = d.groupby(lab)[var].median().round(2).to_dict()
    nn = d[lab].value_counts().to_dict()
    return dict(H=round(H, 2), p=C.p_emp(H, np.array(nul)), grupos=len(med),
                medianas="; ".join(f"{g}={med[g]} (n={nn[g]})" for g in med))


T = []
for var in ["alf_rare", "bases_rare", "frac_comp"]:
    r = kw_perm(A, var, "reg")
    T.append(dict(prueba=f"{var} ~ registrador", **r))
# dentro de región (control de colección/sitio)
for reg_, x in A.groupby("region"):
    if reg_ in ("", "Unknown"):
        continue
    r = kw_perm(x, "alf_rare", "reg", min_n=4)
    if r:
        T.append(dict(prueba=f"alf_rare ~ registrador | región {reg_}", **r))
# captura de datos dentro de UR
r = kw_perm(A[A.reg == "UR"], "alf_rare", "captura")
T.append(dict(prueba="alf_rare ~ captura(CREATED_BY) | registrador UR", **r))
r = kw_perm(A[A.reg == "AS"], "alf_rare", "captura")
if r:
    T.append(dict(prueba="alf_rare ~ captura(CREATED_BY) | registrador AS", **r))
# captura dentro de UR y misma región
for reg_, x in A[A.reg == "UR"].groupby("region"):
    if reg_ in ("", "Unknown"):
        continue
    r = kw_perm(x, "alf_rare", "captura", min_n=4)
    if r:
        T.append(dict(prueba=f"alf_rare ~ captura | UR, región {reg_}", **r))
TT = pd.DataFrame(T)
TT.to_csv(C.AQUI / "p3_pruebas.csv", index=False)

# vocabulario por registrador
V = []
voc = {g: Counter(x.col) for g, x in cc.groupby("reg")}
allc = set().union(*voc.values())
for g, cnt in voc.items():
    tot = sum(cnt.values())
    otros = set().union(*[set(v) for h, v in voc.items() if h != g])
    excl = [k for k in cnt if k not in otros]
    V.append(dict(reg=g, cuerdas=tot, quipus=cc[cc.reg == g].kfg.nunique(), codigos=len(cnt),
                  codigos_exclusivos=len(excl), cuerdas_con_cod_exclusivo=round(sum(cnt[k] for k in excl) / tot, 3),
                  frac_compuesto=round(cc[cc.reg == g].comp.mean(), 3),
                  top5=", ".join(f"{a}:{round(b / tot, 2)}" for a, b in cnt.most_common(5))))
pd.DataFrame(V).to_csv(C.AQUI / "p3_vocabulario.csv", index=False)

# mismo objeto leído dos veces
pr = pd.read_csv(C.RAIZ / "analisis/14_copias/pares_resumen.csv")
fa = pd.read_csv(C.RAIZ / "analisis/14_copias/filas_alineadas.csv", keep_default_na=False)
M = []
for r in pr[pr.tipo == "mismo_objeto"].itertuples():
    x = fa[(fa.A == r.A) & (fa.B == r.B)]
    a, b = x.color_A.map(C.norm), x.color_B.map(C.norm)
    ok = (a != "") & (b != "")
    a, b = a[ok], b[ok]
    nul = [C.nmi(list(a), list(rng.permutation(b.values))) for _ in range(999)]
    M.append(dict(A=r.A, B=r.B, reg=f"{C.registrador(r.A)}/{C.registrador(r.B)}", n=len(a),
                  etiqueta_igual=round((a.values == b.values).mean(), 3),
                  base_igual=round((a.map(C.base).values == b.map(C.base).values).mean(), 3),
                  NMI=round(C.nmi(list(a), list(b)), 3), NMI_nulo=round(np.mean(nul), 3),
                  p_NMI=C.p_emp(C.nmi(list(a), list(b)), nul),
                  ejemplos="; ".join(f"{u}->{v}" for u, v in list(Counter(zip(a, b)).most_common(6)))))
pd.DataFrame(M).to_csv(C.AQUI / "p3_mismo_objeto.csv", index=False)

# robustez: color ~ grupo (NMI) por quipu, por registrador
R = []
c0 = c[(c.nivel == 0) & (c.col != "")]
for k, x in c0.groupby("kfg"):
    if len(x) < 20 or x.grupo.nunique() < 4 or x.col.nunique() < 2:
        continue
    o = C.nmi(list(x.col), list(x.grupo))
    nul = [C.nmi(list(rng.permutation(x.col.values)), list(x.grupo)) for _ in range(199)]
    R.append(dict(kfg=k, reg=x.reg.iloc[0], NMI=o, NMI_nulo=np.mean(nul), p=C.p_emp(o, nul)))
R = pd.DataFrame(R)
R.to_csv(C.AQUI / "p3_nmi_grupo.csv", index=False)

pd.set_option("display.width", 250)
print(A.groupby("reg")[["n", "alfabeto", "alf_rare", "bases_rare", "frac_comp"]].median().round(2))
print(TT.to_string())
print(pd.DataFrame(V).to_string())
print(pd.DataFrame(M).to_string())
print(R.groupby("reg").agg(n=("kfg", "size"), sobre_p05=("p", lambda p: int((p <= 0.05).sum())),
                           NMI=("NMI", "median"), NMI_nulo=("NMI_nulo", "median")))
