"""Inspeccion de los casos altos: duplicados de base, reglas que los explican."""
import numpy as np, pandas as pd, pickle
from pathlib import Path
from motor import cargar
A = Path(__file__).resolve().parent
B = pd.read_csv(A / "cuerdas_legibles.csv")
R = pd.read_csv(A / "quipus_legibles.csv")
O = pd.read_csv(A / "inter_pred.csv")
with open(A / "inter_estructura.pkl", "rb") as f:
    E = pickle.load(f)
cop, seq = E["cop"], E["seq"]

# --- pares con mayor coincidencia de valores (posibles duplicados de base)
filas = []
for a, b in cop.groupby(["kfg", "otro"]).size().index[:0]:
    pass
for (a, b), d in cop.groupby(["kfg", "otro"]):
    if a > b:
        continue
    filas.append(dict(a=a, b=b, n=len(d), hit=d.hit.sum(), fr=d.hit.mean()))
D = pd.DataFrame(filas).sort_values("fr", ascending=False)
print("=== pares con >=8 predicciones y >=75% de valores identicos (candidatos a duplicado) ===")
print(D[(D.n >= 8) & (D.fr >= 0.75)].round(3).to_string(index=False))

print("\n=== reglas exactas de los 12 quipus con mayor tasa_neta (nval>=20) ===")
top = R[R.nval >= 20].sort_values("tasa_neta", ascending=False).head(12).kfg.tolist()
for k in top:
    d = B[B.kfg == k]
    reg = {}
    for r in d[d.hit == 1].reglas.fillna(""):
        for x in r.split(";"):
            if x:
                reg[x] = reg.get(x, 0) + 1
    print("%-8s nval=%3d hit=%2d neta=%.2f  reglas_hit=%s  valores=%s" %
          (k, len(d), d.hit.sum(), R.set_index("kfg").loc[k, "tasa_neta"],
           sorted(reg.items(), key=lambda z: -z[1])[:4],
           d.valor.value_counts().head(3).to_dict()))

print("\n=== UR1097, UR1130, UR067, UR066: detalle de predicciones ===")
for k in ["UR1097", "UR1130", "UR067", "UR066"]:
    d = B[B.kfg == k]
    o = O[O.kfg == k]
    print("\n%s  nval=%d  valores mas comunes=%s" % (k, len(d), d.valor.value_counts().head(4).to_dict()))
    print("  intra via=%d hit=%d ; inter pred=%d hit=%d  socios=%s" %
          (d.via_intra.sum(), d.hit_intra.sum(), d.via_inter.sum(), d.hit_inter.sum(),
           o.otro.value_counts().head(4).to_dict()))
    print("  " + d[d.hit == 1].head(6)[["cuerda", "valor", "reglas"]].to_string(index=False).replace("\n", "\n  "))
