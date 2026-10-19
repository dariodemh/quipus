"""Primera lectura de los resultados: por regla, por procedencia, tamanos, top."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent
B = pd.read_csv(A / "cuerdas_legibles.csv")
R = pd.read_csv(A / "quipus_legibles.csv")
O = pd.read_csv(A / "inter_pred.csv")
N = np.load(A / "nulo_resumen.npz")

print("=== por regla (solo cuerdas con esa via) ===")
for r in ["subs", "subs_res", "hija_unica", "superior", "grupo_total", "cierre"]:
    m = B.reglas.fillna("").str.contains(r)
    if m.sum():
        print("%-12s n=%5d  hit=%4d  tasa=%.3f  p_null=%.3f  exceso=%.3f" %
              (r, m.sum(), B[m].hit.sum(), B[m].hit.mean(), B[m].p_null.mean(),
               B[m].hit.mean() - B[m].p_null.mean()))
for r in ["copia", "suma_dos"]:
    m = B.reglas.fillna("").str.contains(r)
    if m.sum():
        print("%-12s n=%5d  hit=%4d  tasa=%.3f  p_null=%.3f  exceso=%.3f" %
              (r, m.sum(), B[m].hit.sum(), B[m].hit.mean(), B[m].p_null.mean(),
               B[m].hit.mean() - B[m].p_null.mean()))

print("\n=== agregado por tipo de via ===")
print("intra: via %d hit %d (%.3f) ; inter: via %d hit %d (%.3f)" % (
    B.via_intra.sum(), B.hit_intra.sum(), B.hit_intra.sum() / max(1, B.via_intra.sum()),
    B.via_inter.sum(), B.hit_inter.sum(), B.hit_inter.sum() / max(1, B.via_inter.sum())))
print("sin via: %d (%.1f%% de las cuerdas con valor)" % ((B.via == 0).sum(), 100 * (B.via == 0).mean()))

print("\n=== procedencias con >=5 quipus y >=100 cuerdas ===")
g = B.groupby("procedencia").agg(nq=("kfg", "nunique"), nc=("hit", "size"), hit=("hit", "sum"),
                                 pn=("p_null", "sum"))
g["tasa"] = g.hit / g.nc; g["exceso"] = g.hit / g.nc - g.pn / g.nc
print(g[g.nq >= 5].sort_values("exceso", ascending=False).round(3).head(15).to_string())

print("\n=== por tamano (cuerdas con valor) ===")
R["cubo"] = pd.cut(R.nval, [0, 10, 20, 50, 100, 200, 10000], right=False)
print(R.groupby("cubo", observed=True).agg(nq=("kfg", "size"), tasa=("tasa", "mean"),
      neta=("tasa_neta", "mean"), cob=("cobertura", "mean"), ac=("acierto_si_via", "mean"),
      sig=("sig", "sum")).round(3).to_string())

print("\n=== con T / sin T ; con subsidiarias / sin ===")
R["sub"] = R.nsub > 0
print(R.groupby("sub").agg(nq=("kfg", "size"), neta=("tasa_neta", "mean"), sig=("sig", "mean")).round(3).to_string())
print(R.assign(T=R.nT > 0).groupby("T").agg(nq=("kfg", "size"), neta=("tasa_neta", "mean"), sig=("sig", "mean")).round(3).to_string())

print("\n=== top 15 tasa_neta (nval>=20) ===")
cols = ["kfg", "procedencia", "nval", "hit", "hit_null", "tasa_neta", "cobertura", "acierto_si_via", "q", "nT", "nsub"]
print(R[R.nval >= 20].sort_values("tasa_neta", ascending=False)[cols].head(15).round(3).to_string(index=False))

print("\n=== quipus grandes (nval>=100) ordenados por neta ===")
print(R[R.nval >= 100].sort_values("tasa_neta", ascending=False)[cols].head(10).round(3).to_string(index=False))
print(R[R.nval >= 100].sort_values("tasa_neta")[cols].head(5).round(3).to_string(index=False))
