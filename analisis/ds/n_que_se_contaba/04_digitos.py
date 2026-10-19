"""04. Benford y digito final por quipu y por tipo (recuento vs asignacion).

Tipo: el de 11_rosetta (fA_redondeo_por_quipu.csv):
  asignacion = frac >= 0,8 de cuerdas intactas >=10 multiples de 10
  recuento   = frac <= 0,2
OJO: la etiqueta se define con el digito final, asi que comparar digitos entre
grupos es en parte circular. Control: repetir excluyendo multiplos de 10 y de 5.

Benford: primer digito de valores >=10 de cuerdas intactas (terminacion K).
Por quipu: chi2 con p simulado bajo Benford (B=1000), solo n>=20.
Agregado: por grupo y global, chi2 y MAD.
Digito final: 0-9, uniformidad y exceso de 0.
"""
import numpy as np
import pandas as pd
from scipy.stats import chi2, mannwhitneyu
import comun as C

rng = np.random.default_rng(C.SEED)
B = 1000
c = C.cargar()
c = c[c.nudos.notna() & (c.terminacion == "K") & (c.valor >= 10)].copy()
c["d1"] = c.valor.astype(int).astype(str).str[0].astype(int)
c["d9"] = c.valor.astype(int) % 10

f = pd.read_csv(C.RAIZ / "11_rosetta" / "fA_redondeo_por_quipu.csv")
f["tipo"] = np.where(f.frac >= .8, "asignacion", np.where(f.frac <= .2, "recuento", "intermedio"))
print("quipus por tipo:", f.tipo.value_counts().to_dict())

BEN = np.log10(1 + 1 / np.arange(1, 10))


def mad1(v):
    if len(v) < 5:
        return np.nan
    obs = np.bincount(v, minlength=10)[1:10] / len(v)
    return float(np.abs(obs - BEN).mean())


def chi2_ben(v):
    if len(v) < 5:
        return np.nan, np.nan
    obs = np.bincount(v, minlength=10)[1:10]
    esp = BEN * len(v)
    st = ((obs - esp) ** 2 / esp).sum()
    return float(st), float(chi2.sf(st, 8))


def p_sim_ben(v, B=1000):
    """p simulado: probabilidad de un chi2 >= observado si los digitos son Benford."""
    st, _ = chi2_ben(v)
    if not np.isfinite(st):
        return np.nan
    sims = rng.choice(np.arange(1, 10), size=(B, len(v)), p=BEN)
    out = []
    for s in sims:
        obs = np.bincount(s, minlength=10)[1:10]
        esp = BEN * len(s)
        out.append(((obs - esp) ** 2 / esp).sum())
    return float((np.array(out) >= st).mean())


# ---------------------------------------------------------------- por quipu
filas = []
for k, cq in c.groupby("kfg"):
    v = cq.d1.to_numpy()
    if len(v) < 20:
        continue
    rango = cq.valor.max() / cq.valor.min()
    filas.append(dict(kfg=k, n=len(v), rango=rango, mad=mad1(v),
                      chi2=chi2_ben(v)[0], p=p_sim_ben(v)))
P = pd.DataFrame(filas)
P = P.merge(f[["kfg", "tipo", "frac", "procedencia"]], on="kfg", how="left")
P["q"] = C.bh(P.p.to_numpy())
print("\n=== Benford por quipu (n>=20) ===")
print("quipus probados:", len(P), "; rechazan Benford (q<0.05): %d (%.0f%%)" %
      ((P.q < .05).sum(), 100 * (P.q < .05).mean()))
print("MAD mediano: %.4f (Benford exacto = 0)" % P.mad.median())
print("por rango de valores (max/min):")
P["tramo"] = pd.cut(P.rango, [0, 10, 100, 1e9], labels=["<10", "10-100", ">100"])
print(P.groupby("tramo", observed=True).agg(n=("kfg", "size"), mad=("mad", "median"),
                                            rechaza=("q", lambda s: (s < .05).mean())).round(3).to_string())

# ---------------------------------------------------------------- agregado por tipo
print("\n=== Agregado por tipo (todos los valores) ===")
res = []
for tipo in ["recuento", "intermedio", "asignacion"]:
    ks = set(f.loc[f.tipo == tipo, "kfg"])
    v = c[c.kfg.isin(ks)].d1.to_numpy()
    if len(v) == 0:
        continue
    st, p = chi2_ben(v)
    print("%-11s n=%5d  MAD=%.4f  chi2=%.1f p=%.1e  d1=%s" %
          (tipo, len(v), mad1(v), st, p, np.round(np.bincount(v, minlength=10)[1:10] / len(v) * 100, 1).tolist()))
    res.append(dict(tipo=tipo, n=len(v), mad=mad1(v), chi2=st, p=p,
                    frac0=float((c[c.kfg.isin(ks)].d9 == 0).mean())))
D = pd.DataFrame(res)
print("\ndigito final 0 por tipo:")
print(D[["tipo", "n", "frac0"]].round(3).to_string(index=False))

# contraste entre grupos (nivel quipu)
A = P[P.tipo == "asignacion"].mad.dropna()
R = P[P.tipo == "recuento"].mad.dropna()
if len(A) >= 3 and len(R) >= 3:
    u = mannwhitneyu(A, R, alternative="greater")
    print("\nMAD asignacion (n=%d, mediana %.3f) vs recuento (n=%d, mediana %.3f): MW p=%.2e" %
          (len(A), A.median(), len(R), R.median(), u.pvalue))

# ---------------------------------------------------------------- control de circularidad
print("\n=== Control de circularidad: excluir valores multiplos de 10 y de 5 ===")
c2 = c[(c.valor % 10 != 0)]
print("valores no multiplos de 10:", len(c2))
for tipo in ["recuento", "asignacion"]:
    ks = set(f.loc[f.tipo == tipo, "kfg"])
    v = c2[c2.kfg.isin(ks)].d1.to_numpy()
    if len(v):
        st, p = chi2_ben(v)
        print("%-11s n=%5d MAD=%.4f chi2 p=%.2e" % (tipo, len(v), mad1(v), p))

print("\n=== Digito final por quipu (n>=20) ===")
filas = []
for k, cq in c.groupby("kfg"):
    v = cq.d9.to_numpy()
    if len(v) < 20:
        continue
    obs = np.bincount(v, minlength=10)
    st = ((obs - len(v) / 10) ** 2 / (len(v) / 10)).sum()
    filas.append(dict(kfg=k, n=len(v), frac0=float((v == 0).mean()),
                      chi2=st, p=float(chi2.sf(st, 9))))
L = pd.DataFrame(filas).merge(f[["kfg", "tipo"]], on="kfg", how="left")
L["q"] = C.bh(L.p.to_numpy())
print("quipus n>=20:", len(L), "; rechazan uniformidad (q<0.05): %d (%.0f%%)" %
      ((L.q < .05).sum(), 100 * (L.q < .05).mean()))
print("fraccion de 0 mediana: %.3f (uniforme = 0,10)" % L.frac0.median())
print(L.groupby("tipo").agg(n=("kfg", "size"), frac0=("frac0", "median"),
                            rechaza=("q", lambda s: (s < .05).mean())).round(3).to_string())

# ---------------------------------------------------------------- control de rango
print("\n=== Control: ¿el fracaso de Benford es solo restriccion de rango? ===")
# para cada quipu, esperado si los valores son uniformes entre su min y max
esp = np.zeros(9)
for k, cq in c.groupby("kfg"):
    if len(cq) < 20:
        continue
    lo, hi = cq.valor.min(), cq.valor.max()
    if hi <= lo:
        continue
    xs = np.linspace(lo, hi, 4000)
    d = np.array([int(str(int(x))[0]) for x in xs if x >= 1])
    fr = np.bincount(d, minlength=10)[1:10] / len(d)
    esp += fr * len(cq)
esp /= esp.sum()
obs = np.bincount(c.d1.to_numpy(), minlength=10)[1:10]
obs = obs / obs.sum()
print("observado   :", np.round(obs * 100, 1).tolist())
print("Benford     :", np.round(BEN * 100, 1).tolist())
print("rango-uniforme:", np.round(esp * 100, 1).tolist())
print("MAD obs-Benford = %.4f ; MAD obs-rango = %.4f" %
      (np.abs(obs - BEN).mean(), np.abs(obs - esp).mean()))

P.to_csv(C.OUT / "benford_por_quipu.csv", index=False)
L.to_csv(C.OUT / "digito_final_por_quipu.csv", index=False)
D.to_csv(C.OUT / "digitos_por_tipo.csv", index=False)
print("\nguardado benford_por_quipu.csv, digito_final_por_quipu.csv, digitos_por_tipo.csv")
