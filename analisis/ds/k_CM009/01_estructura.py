# -*- coding: utf-8 -*-
"""CM009: reconstrucción de estructura y valores.
Fuente: data/external/khipu-computational-toolkit/legacy/data/processed/cord_hierarchy.csv
(export de la base KFG 'khipu_database.db'; CM009 NO está en analisis/datos/*.csv).
"""
import pandas as pd, re, numpy as np

P = "data/external/khipu-computational-toolkit/legacy/data/processed/cord_hierarchy.csv"
d = pd.read_csv(P)
q = d[d.khipu_id == "CM009"].copy().sort_values("cord_id").reset_index(drop=True)
print("n cuerdas:", len(q))
print("niveles:", q.cord_level.value_counts().to_dict())
print("clases/attachment:", q.attachment.value_counts().to_dict())
print("twist:", q.twist.value_counts().to_dict())
print("color:", q.color.value_counts().to_dict())
print("largo valores:", sorted(q.cord_length.unique())[:5])
print("¿todos largo 45?:", bool((q.cord_length == 45).all()))

# secuencia
print("\nsecuencia (pos, cord, color, valor, nudos):")
for i, r in q.iterrows():
    print(f"{int(r.pendant_num):2d} {r.cord_name:>3} {r.color:>5} v={int(r.numeric_value):5d} "
          f"kc={'' if pd.isna(r.num_knot_clusters) else int(r.num_knot_clusters)} | {'' if pd.isna(r.knots_string) else r.knots_string}")

# resumen valores
print("\nvalor total:", int(q.numeric_value.sum()))
print("cuerdas sin nudos:", int((~q.has_knots).sum()), "->", list(q[~q.has_knots].cord_name))
print("valores repetidos (>1 vez):")
vc = q.numeric_value.value_counts()
print(vc[vc > 1].to_dict())

# parsear nudos
def parse(s):
    if not isinstance(s, str): return []
    out = []
    for cl in s.split(";"):
        m = re.match(r"(\d+)([A-Z]+)\(([\d.]+),(\w)\),(\d+)", cl.strip())
        if m:
            out.append(dict(n=int(m.group(1)), tipo=m.group(2), pos=float(m.group(3)),
                            dir=m.group(4), ap=int(m.group(5))))
    return out
q["clusters"] = q.knots_string.apply(parse)
allcl = [c for cl in q.clusters for c in cl]
print("\ntipos de nudo:", pd.Series([c['tipo'] for c in allcl]).value_counts().to_dict())
print("direcciones de nudo:", pd.Series([c['dir'] for c in allcl]).value_counts().to_dict())
print("posiciones Y (cm) de clusters:", sorted(set(c['pos'] for c in allcl)))
q.to_csv("analisis/ds/k_CM009/cm009_cuerdas.csv", index=False)
print("\nguardado cm009_cuerdas.csv")
