"""Cifras finales citadas en el informe (una sola pasada, salida corta)."""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent
B = pd.read_csv(A / "cuerdas_legibles.csv")
R = pd.read_csv(A / "quipus_legibles.csv")
O = pd.read_csv(A / "inter_pred.csv")

print("--- global")
print("cuerdas %d ; via %d (%.1f%%) ; hit %d (%.2f%%) ; nulo %.2f%%" %
      (len(B), B.via.sum(), 100 * B.via.mean(), B.hit.sum(), 100 * B.hit.mean(), 100 * B.p_null.mean()))
print("acierto si via %.3f ; quipus hit=0 %d/%d" % (B.hit.sum() / B.via.sum(), (R.hit == 0).sum(), R.nval.gt(0).sum()))
print("quipus q<0.05 %d ; cuerdas en ellos %d" % (R.sig.sum(), R[R.sig].nval.sum()))
print("tasa_neta>0.10 %d ; >0.25 %d" % ((R.tasa_neta > .10).sum(), (R.tasa_neta > .25).sum()))

print("\n--- por regla")
print(pd.read_csv(A / "reglas_resumen.csv").round(3).to_string(index=False))

print("\n--- cierre: quipus")
d = B[B.reglas.fillna("").str.contains("cierre")]
print(d.groupby("kfg").agg(n=("hit", "size"), hit=("hit", "sum")).to_string())

print("\n--- hija_unica: quipus con >=5 aciertos y nulo < mitad")
h = B[B.reglas.fillna("").str.contains("hija_unica")]
g = h.groupby("kfg").agg(n=("hit", "size"), hit=("hit", "sum"), pn=("p_null", "sum"))
sel = g[(g.hit >= 5) & (g.pn < g.hit / 2)]
print(len(sel), "quipus;", list(sel.index[:12]))
print("suma de sus aciertos:", int(sel.hit.sum()), "de", int(g.hit.sum()))

print("\n--- copia")
print(O[O.regla == "copia_quipu"].groupby(["kfg", "otro"]).agg(n=("hit", "size"), hit=("hit", "sum")).round(2).to_string())
print("copia total: %d pred, %d hit" % ((O.regla == "copia_quipu").sum(), O[O.regla == "copia_quipu"].hit.sum()))
print("copia_grupo: %d pred, %d hit (%.3f)" % ((O.regla == "copia_grupo").sum(),
      O[O.regla == "copia_grupo"].hit.sum(), O[O.regla == "copia_grupo"].hit.mean()))
print("suma_dos: %d pred, %d hit (%.3f)" % ((O.regla == "suma_dos").sum(),
      O[O.regla == "suma_dos"].hit.sum(), O[O.regla == "suma_dos"].hit.mean()))

print("\n--- Incahuasi 13")
sis = ["UR270", "UR273A", "UR273B", "UR274A", "UR274B", "UR278", "UR266", "UR275", "UR269", "UR267A", "UR267B", "UR255", "UR256"]
T = R[R.kfg.isin(sis)]
print("nval %d hit %d neta %.3f ; sin via %d" % (T.nval.sum(), T.hit.sum(),
      (T.hit.sum() - T.hit_null.sum()) / T.nval.sum(), int((T.via == 0).sum())))
print(T[["kfg", "nval", "via", "hit", "tasa_neta"]].sort_values("tasa_neta", ascending=False).round(3).to_string(index=False))

print("\n--- generos")
print(R[R.nval > 0].groupby("genero").agg(nq=("kfg", "size"), neta=("tasa_neta", "mean"), sig=("sig", "sum")).round(3).to_string())
