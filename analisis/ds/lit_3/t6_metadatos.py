"""T6. Metadatos: Brezine et al. (2024) y el conteo de khipus "no decimales"
de Urton (2019).

A) Brezine: la convencion KH#### se implementa en el OKR y debe servir de
   clave de union. Se comprueba cobertura y unicidad en quipus.csv.
B) Urton (2019): "casi un tercio" de los quipus del KDB no serian
   decimales/narrativos. Sin una definicion operativa, se usan tres
   proxies de "no decimal" basados en cuerdas sin nudos (valor 0 = ausente,
   regla 6 del brief). Se reporta la sensibilidad al umbral.
"""
import pandas as pd
from comun import cargar

c, q, _ = cargar()

print("=== A. Cobertura de la nomenclatura KH#### ===")
print("quipus en quipus.csv:", len(q))
kh = q.okr.astype(str).str.startswith("KH")
print("con id KH:", kh.sum(), f"({kh.mean():.1%})")
print("sin id KH:", (~kh).sum())
print("sin ningun okr:", q.okr.isna().sum(), q[q.okr.isna()].kfg.tolist())
print("\nPrefijos que aun no usan KH:")
print(q[~kh].kfg.str.extract(r"^([A-Z]+)")[0].value_counts().to_string())
print("\nokr duplicados (colisiones de clave):")
dup = q[q.okr.duplicated(keep=False) & q.okr.notna()]
print(dup[["kfg", "okr"]].sort_values("okr").to_string(index=False))
print("filas afectadas:", len(dup), "| ids OKR duplicados:", dup.okr.nunique())

print("\n=== B. Khipus 'no decimales' (proxy: cuerdas sin nudos) ===")
rows = []
for k, g in c.groupby("kfg"):
    p = g[g.nivel == 0]
    if len(p) == 0:
        continue
    rows.append((k, len(p), int(p.nudos.isna().sum())))
d = pd.DataFrame(rows, columns=["kfg", "npend", "sin_nudos"])
d["frac"] = d.sin_nudos / d.npend
print("khipus:", len(d))
print("sin ningun nudo:", (d.frac == 1).sum(), f"({(d.frac==1).mean():.1%})")
for thr in [0.5, 0.33, 0.25, 0.1]:
    m = d.frac > thr
    print(f"  >{thr:.0%} de colgantes sin nudos: {m.sum()} ({m.mean():.1%})")
print("\ndistribucion de la fraccion sin nudos:")
print(d.frac.describe().round(3).to_string())
print("\nComparacion: Urton (2019) dice 923 quipus en el KDB y 'casi un tercio' no decimales.")
print("Nuestro corpus KFG:", len(d), "quipus; el proxy mas cercano a 1/3 es >33% sin nudos.")
