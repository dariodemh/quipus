# -*- coding: utf-8 -*-
"""Robustez: (a) clases de valores (multiplos, repdigitos) frente al nulo de digitos;
(b) efecto de quitar quipus atipicos o duplicados; (c) Incahuasi 15/47 dentro de su decada;
(d) quien sostiene el exceso de 1 en posicion de etiqueta; (e) test global de clustering.
"""
import pandas as pd, numpy as np, os
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False).set_index("kfg")
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)


def dig(v): return [int(x) for x in str(v)]


def tabla_B2(df):
    """devuelve freq, esperado B2 y p por valor para el corpus df"""
    f = pd.Series(df.valor.values).value_counts()
    L = df.valor.map(lambda v: len(str(v)))
    nL = L.value_counts().to_dict()
    marg = {}
    for l in sorted(nL):
        sub = df[L == l]
        marg[l] = {p: sub.valor.map(lambda v: dig(v)[p]).value_counts(normalize=True).to_dict()
                   for p in range(l)}
    exp = {}
    for v in f.index:
        l = len(str(v))
        if l == 1:
            exp[v] = nL[l] / 9
        else:
            pr = 1.0
            for p, d in enumerate(dig(v)):
                pr *= marg[l][p].get(d, 1e-12)
            exp[v] = nL[l] * pr
    return f, exp

f, exp = tabla_B2(k)
pd.set_option("display.width", 250)

# ---------- (a) clases ----------
def es_rep(v):
    d = dig(v); return len(set(d)) == 1 and len(d) >= 2
clases = {
    "multiplos de 5": lambda v: v % 5 == 0,
    "multiplos de 10": lambda v: v % 10 == 0,
    "multiplos de 100": lambda v: v % 100 == 0,
    "repdigitos (11,22,...,222)": es_rep,
    "palindromos (>=2 dig)": lambda v: len(str(v)) >= 2 and str(v) == str(v)[::-1],
    "suma de digitos <=3": lambda v: sum(dig(v)) <= 3,
    "potencias de 10": lambda v: str(v)[0] == "1" and set(str(v)[1:]) <= {"0"},
}
rows = []
for nom, fn in clases.items():
    vals = [v for v in f.index if fn(v)]
    o = int(f[vals].sum()); e = float(sum(exp[v] for v in vals))
    rows.append({"clase": nom, "obs": o, "esp_B2": round(e, 1), "ratio": o / e if e else np.nan,
                 "p": stats.poisson.sf(o - 1, e) if e > 0 else 1.0})
CL = pd.DataFrame(rows)
CL["q"] = stats.false_discovery_control(CL.p.values, method="bh")
print("=== (a) clases de valores frente al nulo de digitos B2 ===")
print(CL.to_string(index=False, float_format=lambda x: f"{x:.3g}"))

# ---------- (b) quitar atipicos ----------
print("\n=== (b) sensibilidad a quipus atipicos ===")
casos = [([], "todos"), (["UR1109"], "sin UR1109 (53 cienes)"),
         (["UR1084"], "sin UR1084 (copia de HP055)"),
         (["UR1109", "UR1084", "UR266"], "sin los tres")]
for drop, nom in casos:
    sub = k[~k.kfg.isin(drop)]
    fs, es = tabla_B2(sub)
    out = []
    for v in [100, 200, 110, 47, 33, 22, 15, 10]:
        o = fs.get(v, 0); e = es.get(v, 1e-9)
        out.append(f"{v}:{o/e:.2f}x")
    print(f"{nom:<32} " + "  ".join(out))

# ---------- (c) Incahuasi 15 y 47 dentro de su decada ----------
print("\n=== (c) Incahuasi: 15 dentro de 10-19 y 47 dentro de 40-49 ===")
prov = q.reindex(sorted(k.kfg.unique())).procedencia.fillna("Unknown").astype(str)
inc = set(prov[prov == "Incahuasi"].index)
k["inc"] = k.kfg.isin(inc)
for v, lo, hi, nom in [(15, 10, 19, "Incahuasi"), (47, 40, 49, "Incahuasi"),
                       (15, 10, 19, "resto"), (47, 40, 49, "resto")]:
    sub = k[k.inc] if nom == "Incahuasi" else k[~k.inc]
    dec = sub[(sub.valor >= lo) & (sub.valor <= hi)]
    p = (dec.valor == v).mean()
    print(f"{nom:<12} v={v}: {int((dec.valor==v).sum()):>4}/{len(dec):>5} = {p*100:.1f}% de la decada")
a = k[(k.inc) & (k.valor.between(10, 19))].valor.eq(15).sum(); n1 = k[(k.inc) & (k.valor.between(10, 19))].shape[0]
b = k[(~k.inc) & (k.valor.between(10, 19))].valor.eq(15).sum(); n2 = k[(~k.inc) & (k.valor.between(10, 19))].shape[0]
print("Fisher 15:", stats.fisher_exact([[a, n1 - a], [b, n2 - b]]))
a = k[(k.inc) & (k.valor.between(40, 49))].valor.eq(47).sum(); n1 = k[(k.inc) & (k.valor.between(40, 49))].shape[0]
b = k[(~k.inc) & (k.valor.between(40, 49))].valor.eq(47).sum(); n2 = k[(~k.inc) & (k.valor.between(40, 49))].shape[0]
print("Fisher 47:", stats.fisher_exact([[a, n1 - a], [b, n2 - b]]))

# ---------- (d) quien sostiene 1 en primera posicion ----------
print("\n=== (d) valor 1 en primera cuerda del grupo: aporte por quipu ===")
k0 = k[k.nivel == 0].copy()
prim = k0.groupby(["kfg", "grupo"]).orden.transform("min")
k0["primero"] = k0.orden == prim
ap = []
for qq, s in k0.groupby("kfg"):
    n = len(s); ng = s.grupo.nunique()
    obs = int(((s.valor == 1) & s.primero).sum())
    esp = ng * (s.valor == 1).mean()
    if obs - esp > 0: ap.append((qq, obs, round(esp, 1), round(obs - esp, 1)))
ap = pd.DataFrame(ap, columns=["kfg", "obs", "esp", "exceso"]).sort_values("exceso", ascending=False)
print(ap.head(10).to_string(index=False))
print("quipus con exceso>0:", len(ap), "| suma exceso:", round(ap.exceso.sum(), 1))

# ---------- (e) test global de clustering ----------
print("\n=== (e) clustering global (tabla de concentracion) ===")
T = pd.read_csv(OUT + r"\tabla_concentracion.csv")
print("suma n_sobre_obs:", int(T.n_sobre_obs.sum()), "| suma n_sobre_null:", round(T.n_sobre_null.sum(), 1),
      "| razon:", round(T.n_sobre_obs.sum() / T.n_sobre_null.sum(), 2))
print("valores con q_sobre<0.05:", int((T.q_sobre < .05).sum()), "/", len(T))
