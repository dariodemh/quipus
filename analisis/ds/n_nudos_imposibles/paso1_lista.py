# -*- coding: utf-8 -*-
"""Paso 1: identificar cuerdas con nudos imposibles en lectura decimal.
- L (largo) con >=10 vueltas: el nudo largo decimal admite 2-9.
- E/S en posicion imposible: mas de un nudo L/E (unidad multiple) o L/E que no
  esta en el ultimo racimo (unidad no al final). Se anade E con n>=10.
Salida: cuerdas_imposibles.csv, resumen_quipus_imposibles.csv
"""
import re, pandas as pd, numpy as np

BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_parsed.pkl")
# reparseo robusto: valor final opcional (UR044 no lo trae)
KNOT_RE = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([A-Za-z?]+)\)(?:,(-?\d+))?")
def parse_nudos(s):
    if not isinstance(s, str) or not s.strip():
        return []
    return [dict(n=int(m.group(1)), tipo=m.group(2), pos=float(m.group(3)),
                 dir=m.group(4), val=int(m.group(5)) if m.group(5) is not None else None)
            for m in KNOT_RE.finditer(s)]
df["knots"] = df["nudos"].map(parse_nudos)

def flags(ks):
    """Devuelve (tiene_L10, tiene_pos_imposible, n_L, n_E, n_S, n_racimos, detalle)."""
    tipos = [k["tipo"] for k in ks]
    idx_LE = [i for i,t in enumerate(tipos) if t in ("L","E")]
    n_L = sum(t=="L" for t in tipos); n_E = sum(t=="E" for t in tipos)
    L10 = any(k["tipo"]=="L" and k["n"]>=10 for k in ks) or any(k["tipo"]=="E" and k["n"]>=10 for k in ks)
    pos_imp = len(idx_LE) > 1 or (len(idx_LE)==1 and idx_LE[0] != len(ks)-1)
    det = []
    if any(k["tipo"]=="L" and k["n"]>=10 for k in ks): det.append("L>=10")
    if any(k["tipo"]=="E" and k["n"]>=10 for k in ks): det.append("E>=10")
    if len(idx_LE) > 1: det.append("multi_unidad")
    if len(idx_LE)==1 and idx_LE[0]!=len(ks)-1: det.append("unidad_no_final")
    return pd.Series(dict(L10=L10, pos_imp=pos_imp, n_L=n_L, n_E=n_E,
                          n_S=sum(t=="S" for t in tipos), n_rac=len(ks),
                          imposible=L10 or pos_imp, detalle=";".join(det)))

fl = df.knots.apply(flags)
df = pd.concat([df, fl], axis=1)

print("cuerdas:", len(df))
print("con L>=10:", int(df.L10.sum()), " quipus:", df[df.L10].kfg.nunique())
print("pos imposible (multi/unidad no final):", int(df.pos_imp.sum()), " quipus:", df[df.pos_imp].kfg.nunique())
print("cualquiera:", int(df.imposible.sum()), " quipus:", df[df.imposible].kfg.nunique())
def _maxL(ks):
    v=[k['n'] for k in ks if k['tipo']=='L' and k['n']>=10]
    return max(v) if v else 0
print("L>=10 por n vueltas:", df[df.L10].knots.map(_maxL).value_counts().sort_index().to_dict())

q = pd.read_csv(BASE + r"\analisis\datos\quipus.csv", dtype=str, keep_default_na=False)
q["okr"] = q["okr"].replace("", np.nan)
df = df.merge(q[["kfg","okr","museo","procedencia","region"]], on="kfg", how="left")
df.to_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_imposibles.pkl")

# resumen por quipu
g = df.groupby("kfg").agg(n_cuerdas=("cuerda","size"),
                          n_imp=("imposible","sum"), n_L10=("L10","sum"),
                          n_posimp=("pos_imp","sum"),
                          okr=("okr","first"), museo=("museo","first"),
                          procedencia=("procedencia","first"), region=("region","first"))
g["frac_imp"] = g.n_imp / g.n_cuerdas
g = g[g.n_imp > 0].sort_values(["n_imp","frac_imp"], ascending=False)
print("\nquipus con >=1 cuerdas imposibles:", len(g))
print(g.head(20).round(3).to_string())
g.to_csv(BASE + r"\analisis\ds\n_nudos_imposibles\resumen_quipus_imposibles.csv")
print("\nfilas con L>=10 y su quipu (primeras 40):")
print(df[df.L10][["kfg","cuerda","nivel","valor","nudos","detalle"]].head(40).to_string())
