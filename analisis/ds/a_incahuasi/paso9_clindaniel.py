# -*- coding: utf-8 -*-
"""Paso 9: (a) test del claim de Clindaniel UR267A '+106-15=91' y UR255 invertido;
(b) similitud de pares A/B (posibles 'pares atados')."""
import pandas as pd, numpy as np
RAIZ = "./"
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]; ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))

# (a) busca 106, 15, 91 y patrones de color
for k in ["UR267A", "UR267B", "UR255"]:
    d = ci[ci["kfg"] == k]
    print(f"\n=== {k}: {len(d)} cuerdas; valores clave ===")
    for target in [106, 15, 91]:
        sub = d[d["valor"] == target]
        if len(sub):
            print(f"  valor {target}: " + "; ".join(f"{r.cuerda}[{r.color}]" for _, r in sub.iterrows()))
    print("  colores (top):", d["color"].value_counts().head(8).to_dict())
    # W vs AB vs mottled: suma de W, suma de AB
    d2 = d[~d.sin_nudos]
    def tot(cols):
        m = d2["color"].fillna("").str.contains(cols, regex=True)
        return int(d2.loc[m, "valor"].sum()), int(m.sum())
    print("  suma valores W:", tot(r"^W($|[:\-])"), "| AB:", tot("AB"), "| mottled(AB:MB o similar):", tot(":"))

# (b) pares A/B
print("\n=== pares A/B: similitud de registros ===")
for a, b in [("UR267A", "UR267B"), ("UR273A", "UR273B"), ("UR274A", "UR274B")]:
    da = ci[(ci.kfg == a) & ~ci.sin_nudos]["valor"].astype(int).values
    db = ci[(ci.kfg == b) & ~ci.sin_nudos]["valor"].astype(int).values
    sa, sb = np.sort(da), np.sort(db)
    comm = len(set(da) & set(db))
    print(f"  {a}({len(da)}) vs {b}({len(db)}): valores compartidos={comm} "
          f"| suma A={da.sum()} suma B={db.sum()} | mediana {np.median(da):.0f}/{np.median(db):.0f}")

# (c) diferencias de union/torsion por serie
print("\ntorsion por serie:")
for pref in ["JC", "UR"]:
    d = ci[ci.kfg.str.startswith(pref)]
    print(f"  {pref}:", d["torsion"].value_counts().to_dict(), "| union:", d["union"].value_counts().to_dict())
