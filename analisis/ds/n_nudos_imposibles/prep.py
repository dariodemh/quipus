# -*- coding: utf-8 -*-
"""Paso 0: cargar cuerdas/quipus, parsear nudos, marcar nudos imposibles.
Solo lectura de analisis/datos/*.csv. Salida: cuerdas_parsed.pkl (en esta carpeta).
"""
import re, pickle
import pandas as pd

BASE = r"."
CUERDAS = BASE + r"\analisis\datos\cuerdas.csv"
QUIPUS  = BASE + r"\analisis\datos\quipus.csv"

# nTIPO(pos,direccion),valor
KNOT_RE = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([A-Za-z?]+)\),(-?\d+)")

def parse_nudos(s):
    if not isinstance(s, str) or not s.strip():
        return []
    out = []
    for m in KNOT_RE.finditer(s):
        out.append(dict(n=int(m.group(1)), tipo=m.group(2), pos=float(m.group(3)),
                        dir=m.group(4), val=int(m.group(5))))
    return out

def limpiar_color(s):
    if not isinstance(s, str):
        return ""
    return re.sub(r"\([^)]*\)", "", s).strip()

df = pd.read_csv(CUERDAS, dtype=str, keep_default_na=False)
for c in ["orden", "nivel", "grupo", "valor"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["knots"] = df["nudos"].map(parse_nudos)
df["color_limpio"] = df["color"].map(limpiar_color)

print("cuerdas:", len(df), "quipus:", df.kfg.nunique())
print("con nudos parseados:", (df.knots.map(len) > 0).sum())
print("cuerdas con texto nudos pero 0 parseados:", ((df.nudos.str.strip() != "") & (df.knots.map(len) == 0)).sum())
# tipos observados
from collections import Counter
tipos = Counter(k["tipo"] for ks in df.knots for k in ks)
print("tipos:", tipos.most_common(12))
print("quipus en quipus.csv:", len(pd.read_csv(QUIPUS, dtype=str)))
print(df[["kfg","cuerda","nudos","valor"]].head(3).to_string())

df.to_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_parsed.pkl")
print("guardado cuerdas_parsed.pkl")
