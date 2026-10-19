# -*- coding: utf-8 -*-
"""Monografia Leymebamba (UR001-UR022). Script 01: descripcion del conjunto.
Salida: tabla.csv (una fila por quipu) + resumen por consola.
No imprime nada grande: solo agregados.
"""
import pandas as pd, numpy as np, re, json, os

RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]

c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
q = pd.read_csv(os.path.join(ROOT, "analisis/datos/quipus.csv"))
g = pd.read_csv(os.path.join(ROOT, "analisis/datos/grupos.csv"))

c = c[c.kfg.isin(LE)].copy()
q = q[q.kfg.isin(LE)].copy()
g = g[g.kfg.isin(LE)].copy()
print("quipus UR001-UR022 presentes:", c.kfg.nunique(), "cuerdas:", len(c), "grupos:", len(g))

# valor: 0 con nudos vacio = ausente
c["sin_nudos"] = c.nudos.isna() | (c.nudos.astype(str).str.strip() == "") | (c.nudos.astype(str).str.strip() == "nan")
c["valor_real"] = np.where(c.sin_nudos, np.nan, c.valor)

# ---- direcciones de nudo y tipos ----
def parse_knots(s):
    if not isinstance(s, str) or s.strip() in ("", "nan"):
        return []
    out = []
    for cl in s.split(";"):
        m = re.match(r"(\d+)([A-Za-z]+)\(([-\d.]+),([SZU])\)(?:,(\d+))?$", cl.strip())
        if m:
            out.append({"tipo": m.group(2), "dir": m.group(4), "n": int(m.group(1)),
                        "pos": float(m.group(3)), "val": int(m.group(5)) if m.group(5) else None})
    return out

c["knots"] = c.nudos.apply(parse_knots)

rows = []
dirc = {}
for kfg, sub in c.groupby("kfg"):
    sub = sub.sort_values("orden")
    n = len(sub)
    col = sub[sub.nivel == 0]
    ncol = len(col)
    nsub = (sub.nivel > 0).sum()
    maxnivel = int(sub.nivel.max())
    ngrupos = sub.grupo.nunique()
    vr = sub.valor_real.dropna()
    # sumas internas: cordon o colgante = suma de sus hijos
    hijos = sub[sub.padre.notna()].groupby("padre").valor_real.sum()
    sumas = 0
    for p, s in hijos.items():
        pv = sub.loc[sub.cuerda == p, "valor_real"]
        if len(pv) and not np.isnan(pv.iloc[0]) and abs(pv.iloc[0] - s) < 1e-6:
            sumas += 1
    # colores de colgantes
    colc = col.color.dropna().astype(str)
    farb = colc.value_counts().to_dict()
    # torsion, union
    tor = sub.torsion.value_counts(dropna=False).to_dict()
    uni = sub.union.value_counts(dropna=False).to_dict()
    # direcciones de nudo
    dirs = {}
    for k in sub.knots:
        for kk in k:
            dirs[kk["dir"]] = dirs.get(kk["dir"], 0) + 1
    dirc[kfg] = dirs
    term = sub.terminacion.value_counts(dropna=False).to_dict()
    rows.append({
        "kfg": kfg, "n_cuerdas": n, "n_colgantes": ncol, "n_subsidiarias": int(nsub),
        "max_nivel": maxnivel, "n_grupos": ngrupos,
        "valores_no_ausentes": len(vr),
        "val_min": vr.min() if len(vr) else np.nan, "val_max": vr.max() if len(vr) else np.nan,
        "val_mediana": vr.median() if len(vr) else np.nan, "val_suma": vr.sum() if len(vr) else np.nan,
        "n_sumas_internas": sumas,
        "colores_colgantes": ";".join(f"{k}:{v}" for k, v in sorted(farb.items(), key=lambda x: -x[1])),
        "uniones": ";".join(f"{k}:{v}" for k, v in uni.items()),
        "torsiones": ";".join(f"{k}:{v}" for k, v in tor.items()),
        "terminaciones": ";".join(f"{k}:{v}" for k, v in term.items()),
        "dirs_nudo": ";".join(f"{k}:{v}" for k, v in sorted(dirs.items())),
    })

T = pd.DataFrame(rows).sort_values("kfg")
T.to_csv(os.path.join(RUTA, "tabla.csv"), index=False)
pd.set_option("display.width", 250, "display.max_columns", 40)
print(T[["kfg", "n_cuerdas", "n_colgantes", "n_subsidiarias", "max_nivel", "n_grupos",
         "valores_no_ausentes", "val_min", "val_max", "n_sumas_internas"]].to_string(index=False))
print("\nTOTAL cuerdas:", T.n_cuerdas.sum(), " colgantes:", T.n_colgantes.sum())
print("Sumas internas por quipu:", T.n_sumas_internas.sum())
print("\nUniones agregadas:", c.union.value_counts(dropna=False).to_dict())
print("Torsiones agregadas:", c.torsion.value_counts(dropna=False).to_dict())
print("Direcciones de nudo agregadas:", {k: v for k, v in sorted(_c) } if False else
      {d: sum(dd.get(d, 0) for dd in dirc.values()) for d in ["S", "Z", "U"]})
print("niveles:", c.nivel.value_counts().sort_index().to_dict())
