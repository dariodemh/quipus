# -*- coding: utf-8 -*-
"""Descripcion fina de cuerdas: nudos, direccion, posicion decimal, largos, orden."""
import os, re
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
q = pd.read_csv(os.path.join(OUT, "ur262_cuerdas_arbol.csv"), dtype={"cuerda": str})
q["valor"] = q["valor"].fillna(0)

# --- parseo de nudos ---
pat = re.compile(r"(\d+)([SLE]+)\(([\d.]+),([SZU])\),(\d+)")
rows = []
for _, r in q.iterrows():
    if not isinstance(r["nudos"], str) or not r["nudos"]:
        continue
    for cl in r["nudos"].split(";"):
        m = pat.match(cl.strip())
        if m:
            rows.append(dict(cuerda=r.cuerda, ncl=int(m.group(1)), tipo=m.group(2),
                             pos=float(m.group(3)), direccion=m.group(4), aporte=int(m.group(5))))
        else:
            rows.append(dict(cuerda=r.cuerda, ncl=np.nan, tipo="PARSE_FAIL", pos=np.nan,
                             direccion="?", aporte=np.nan))
k = pd.DataFrame(rows)
k.to_csv(os.path.join(OUT, "ur262_nudos.csv"), index=False)

print("== racimos ==", len(k), "| cuerdas con racimos:", k.cuerda.nunique())
print("tipos:", k.tipo.value_counts().to_dict())
print("direcciones:", k.direccion.value_counts().to_dict())
print("posiciones (cm) min/med/max: %.2f %.2f %.2f" % (k.pos.min(), k.pos.median(), k.pos.max()))

# consistencia decimal: aporte vs posicion
def dec_ok(pos, aporte):
    if aporte == 0:
        return np.nan
    k10 = round(np.log10(aporte))
    return abs((pos / 10.0) - k10) < 1.0  # posicion ~ decena*10 cm (regla KFG aproximada)
k["ok"] = [dec_ok(p, a) for p, a in zip(k.pos, k.aporte)]
print("racimos con pos/aporte coherentes (|pos/10-dec|<1):", f"{100*k.ok.mean():.1f}%")

# tipo por posicion decimal
k["decena"] = np.log10(k.aporte).round().astype("Int64")
print("\ntipo de nudo por decena (aporte):")
print(pd.crosstab(k.decena, k.tipo).to_string())

# --- E en unidades ---
ult = []
for _, r in q.iterrows():
    if isinstance(r["nudos"], str) and r["nudos"]:
        last = r["nudos"].split(";")[-1]
        m = pat.match(last.strip())
        if m:
            ult.append((r.cuerda, m.group(2), int(m.group(5))))
u = pd.DataFrame(ult, columns=["cuerda", "tipo_ult", "aporte_ult"])
print("\n== ultimo racimo ==")
print(u.tipo_ult.value_counts().to_dict())
print("ultimo E con aporte 1:", int(((u.tipo_ult == "E") & (u.aporte_ult == 1)).sum()),
      "| ultimo E total:", int((u.tipo_ult == "E").sum()))
print("unidades 1 (aporte=1) por tipo:", u[u.aporte_ult == 1].tipo_ult.value_counts().to_dict())

# --- largos y valores ---
print("\n== largo vs valor ==")
vv = q[(q.valor > 0)]
print("Spearman global: %.3f" % vv[["largo", "valor"]].corr(method="spearman").iloc[0, 1])
for gg, s in vv.groupby("grupo"):
    if len(s) > 5:
        print("  grupo %d n=%d rho=%.3f" % (gg, len(s), s[["largo", "valor"]].corr(method="spearman").iloc[0, 1]))

print("\n== largo por nivel ==")
print(q.groupby("nivel").largo.describe()[["count", "mean", "50%", "max"]].to_string())

# --- orden decreciente dentro del grupo ---
print("\n== monotonia de pendientes dentro del grupo ==")
for gg, s in q[q.nivel == 0].groupby("grupo"):
    v = s.sort_values("orden").valor.values
    if len(v) > 2:
        d = np.diff(v)
        print("  G%d n=%d descendente en %d/%d pasos" % (gg, len(v), int((d <= 0).sum()), len(d)))

# --- subsidiarias: valor por posicion del hijo ---
q["pos_hijo"] = q.groupby("padre").cumcount() + 1
s1 = q[(q.nivel > 0) & (q.pos_hijo <= 4)]
print("\n== valor medio de la subsidiaria segun posicion entre hermanas ==")
print(s1.groupby("pos_hijo").agg(n=("valor", "size"), media=("valor", "mean"),
                                  mediana=("valor", "median"), grandes=("valor", lambda x: int((x >= 1000).sum()))).to_string())
