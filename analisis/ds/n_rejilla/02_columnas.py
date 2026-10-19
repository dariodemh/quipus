"""02 · Las 9 partes: efecto de columna, orden y firma relativa.

Filas = registros. Columnas = las 9 partes (posicion ordinal dentro del grupo).
Fuentes: UR278 (28 filas x 9 columnas, tabla de 13/05) y UR270 (grupos con 9
colgantes; celda = colgante + 1.a subsidiaria, verificado en 13/07).

Controles:
  - permutar columnas dentro de cada fila (rompe la etiqueta de columna y conserva
    el tamano y la composicion de cada registro);
  - para el orden, comparar la identidad con las 9! permutaciones.
"""
import itertools
import sys
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, spearmanr
sys.path.insert(0, ".")
from comun_rejilla import RAIZ, SEMILLA, COLS9, cargar_cuerdas, ic_bootstrap, color_familia

rng = np.random.default_rng(SEMILLA)
c, q = cargar_cuerdas()

# ---------------------------------------------------------------- matrices
t = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/ur278_tabla.csv")
U278 = t.set_index("grupo")[COLS9].astype(float)
U278 = U278[U278.notna().sum(axis=1) >= 7]

u = c[(c.kfg == "UR270") & (c.nivel == 0)]
filas270 = []
for g, s in u.groupby("grupo"):
    s = s.sort_values("orden")
    if len(s) != 9:
        continue
    sub = c[(c.kfg == "UR270") & (c.nivel == 1) & (c.padre.isin(s.cuerda))]
    celdas = []
    for _, p in s.iterrows():
        ss = sub[sub.padre == p.cuerda].sort_values("orden")
        celdas.append(p.valor + (ss.iloc[0].valor if len(ss) else np.nan))
    filas270.append([g] + celdas)
U270 = pd.DataFrame(filas270, columns=["grupo"] + COLS9).set_index("grupo")
# valor 0 sin nudos = ausente
for g in U270.index:
    for col in COLS9:
        v = U270.loc[g, col]
        if v == 0:
            U270.loc[g, col] = np.nan

print("UR278 filas:", len(U278), "| completas:", U278.notna().all(axis=1).sum())
print("UR270 filas:", len(U270), "| completas:", U270.notna().all(axis=1).sum())

# ---------------------------------------------------------------- proporcion
def proporciones(M):
    return M.div(M.sum(axis=1, min_count=1), axis=0)


P278 = proporciones(U278)
P270 = proporciones(U270)
P = P278  # firma primaria: 28 registros de UR278

# ---------------------------------------------------------------- efecto columna
C = U278.dropna()
chi, p_fried = friedmanchisquare(*[C[c] for c in COLS9])
W_kendall = chi / (len(C) * (len(COLS9) - 1))
print(f"\nFriedman: chi2={chi:.1f}, p={p_fried:.2e}, W de Kendall={W_kendall:.3f} (n={len(C)})")

rango = P.rank(axis=1, ascending=False)
rango_medio = rango.mean()


def var_medias(Pm):
    return float(Pm.mean().var())


obs = var_medias(P.fillna(P.mean()))
null = []
for _ in range(5000):
    X = P.copy()
    for i in range(len(X)):
        v = X.iloc[i].values.copy()
        rng.shuffle(v)
        X.iloc[i] = v
    null.append(var_medias(X.fillna(X.mean())))
null = np.array(null)
p_var = (1 + np.sum(null >= obs)) / (len(null) + 1)
print(f"varianza de las medias por columna: obs={obs:.5f}, nulo={null.mean():.5f}, p={p_var:.4f}")

# correlacion media entre filas (patron de rangos)
tau = []
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        a, b = P.iloc[i], P.iloc[j]
        ok = a.notna() & b.notna()
        if ok.sum() >= 7:
            tau.append(spearmanr(a[ok], b[ok]).statistic)
print(f"Spearman medio entre pares de filas: {np.mean(tau):.3f} (min {np.min(tau):.2f}, max {np.max(tau):.2f}, n={len(tau)} pares)")
# nulo: permutar dentro de cada fila
tau_null = []
for _ in range(500):
    X = P.copy()
    for i in range(len(X)):
        v = X.iloc[i].values.copy()
        rng.shuffle(v)
        X.iloc[i] = v
    tt = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            a, b = X.iloc[i], X.iloc[j]
            ok = a.notna() & b.notna()
            if ok.sum() >= 7:
                tt.append(spearmanr(a[ok], b[ok]).statistic)
    tau_null.append(np.mean(tt))
p_tau = (1 + np.sum(np.array(tau_null) >= np.mean(tau))) / 501
print(f"  nulo {np.mean(tau_null):.3f}; p={p_tau:.4f}")

# ---------------------------------------------------------------- mayor / menor
mx = P.idxmax(axis=1)
mn = P.idxmin(axis=1)
print("\ncolumna maxima:", mx.value_counts().to_dict())
print("columna minima:", mn.value_counts().to_dict())
n_mx12 = int(mx.isin(["c1", "c2"]).sum())
n_mn89 = int(mn.isin(["c8", "c9"]).sum())
n = len(P)
# P(al menos n_mx12 exitos) con p=2/9 por fila
from scipy.stats import binom
p_mx = binom.sf(n_mx12 - 1, n, 2 / 9)
p_mn = binom.sf(n_mn89 - 1, n, 2 / 9)
print(f"max en c1/c2: {n_mx12}/{n} (esperado {n*2/9:.1f}), binomial p={p_mx:.2e}")
print(f"min en c8/c9: {n_mn89}/{n} (esperado {n*2/9:.1f}), binomial p={p_mn:.2e}")

# lo mismo dentro de UR270 (7 filas, otra grabacion fisica)
mx270 = P270.idxmax(axis=1)
mn270 = P270.idxmin(axis=1)
print("UR270 columna maxima:", mx270.value_counts().to_dict(),
      "| minima:", mn270.value_counts().to_dict())

# control aburrido: estan las columnas ordenadas de mayor a menor?
desc = 0
tot = 0
for i in range(len(U278)):
    v = U278.iloc[i].dropna().values
    desc += int(np.all(np.diff(v) <= 0))
    tot += len(v) - 1
pares_desc = 0
for i in range(len(U278)):
    v = U278.iloc[i].dropna().values
    pares_desc += int(np.sum(np.diff(v) <= 0))
print(f"filas ordenadas de mayor a menor: {desc}/{len(U278)}; pares adyacentes descendentes: {pares_desc}/{tot} ({pares_desc/tot:.2f})")

# ---------------------------------------------------------------- orden entre quipus
pares = [(0, 21), (4, 25), (5, 26), (8, 27), (9, 28)]
perms = list(itertools.permutations(range(9)))
filas_orden = []
for g270, g278 in pares:
    a = U270.loc[g270].values.astype(float)
    b = U278.loc[g278].values.astype(float)
    ok = ~np.isnan(a) & ~np.isnan(b)
    hits = []
    for perm in perms:
        bb = b[list(perm)]
        hits.append(int(np.sum(np.abs(a[ok] - bb[ok]) <= 1)))
    hits = np.array(hits)
    h_id = int(np.sum(np.abs(a[ok] - b[ok]) <= 1))
    p_id = (1 + np.sum(hits >= h_id)) / len(perms)
    best = perms[int(np.argmax(hits))]
    filas_orden.append(dict(g270=g270, g278=g278, n=int(ok.sum()), aciertos_identidad=h_id,
                            max_perm=int(hits.max()), mejor_permutacion=str(best),
                            identidad_es_optima=bool(h_id == hits.max()),
                            n_optimas=int((hits == hits.max()).sum()),
                            p_permutacion=p_id))
O = pd.DataFrame(filas_orden)
O.to_csv("orden_9_partes.csv", index=False, encoding="utf-8-sig")
print("\nOrden de las 9 partes entre UR270 y UR278:")
print(O.to_string(index=False))
print("p combinado (producto, filas tratadas como independientes):", f"{np.prod(O.p_permutacion):.2e}")

# ---------------------------------------------------------------- firma
def firma(Pm, nombre):
    out = []
    for col in COLS9:
        v = Pm[col].dropna().values
        lo, hi = ic_bootstrap(v)
        out.append(dict(parte=col, quipu=nombre, prop_media=float(np.mean(v)),
                        ic_low=lo, ic_high=hi, n=len(v),
                        rango_medio=float(Pm.rank(axis=1, ascending=False)[col].mean())))
    return pd.DataFrame(out)


F278 = firma(P278, "UR278")
F270 = firma(P270, "UR270")
rho = spearmanr(F278.prop_media, F270.prop_media)
print(f"\nCorrelacion de la firma UR278 vs UR270 (9 columnas): rho={rho.statistic:.2f}, p={rho.pvalue:.4f}")

# color / posicion por columna y quipu
s278 = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
s278["pos"] = s278.groupby("grupo").cumcount() + 1
s278 = s278[s278.pos <= 9]
u270 = c[(c.kfg == "UR270") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
u270["pos"] = u270.groupby("grupo").cumcount() + 1
u270 = u270[u270.pos <= 9]
sub270 = c[(c.kfg == "UR270") & (c.nivel == 1)].copy()

filas = []
for i, col in enumerate(COLS9, start=1):
    a = s278[s278.pos == i]
    b = u270[u270.pos == i]
    bs = sub270[sub270.padre.isin(b.cuerda)]
    filas.append(dict(
        parte=col, posicion=i,
        prop_media=float(F278.loc[i - 1, "prop_media"]),
        ic_low=float(F278.loc[i - 1, "ic_low"]), ic_high=float(F278.loc[i - 1, "ic_high"]),
        prop_media_UR270=float(F270.loc[i - 1, "prop_media"]),
        rango_medio=float(F278.loc[i - 1, "rango_medio"]),
        color_UR278=a.color.mode().iat[0] if len(a) else "",
        color_UR270_colgante=b.color.mode().iat[0] if len(b) else "",
        color_UR270_subsidiaria=bs.color.mode().iat[0] if len(bs) else "",
        nivel_UR278=0, nivel_UR270_colgante=0, nivel_UR270_subsidiaria=1,
        union_UR278=a.union.mode().iat[0] if len(a) else "",
        union_UR270=b.union.mode().iat[0] if len(b) else "",
        torsion_UR278=a.torsion.mode().iat[0] if len(a) else "",
        torsion_UR270=b.torsion.mode().iat[0] if len(b) else "",
        es_max=int((mx == col).sum()), es_min=int((mn == col).sum()),
        n_filas=len(P),
        n_UR278=int(P278[col].notna().sum()), n_UR270=int(P270[col].notna().sum()),
        marca_color="no: el color es de la fila (UR278) o del nivel (UR270)",
    ))
F = pd.DataFrame(filas)
F.to_csv("firma_9_partes.csv", index=False, encoding="utf-8-sig")
print("\nfirma_9_partes.csv:")
print(F[["parte", "prop_media", "ic_low", "ic_high", "prop_media_UR270",
         "rango_medio", "es_max", "es_min", "color_UR278"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# ---------------------------------------------------------------- controles extra
# (a) la proporcion no depende del tamano del registro
rr = [spearmanr(P[col], U278.sum(axis=1)).statistic for col in COLS9]
print(f"\n|rho| medio (proporcion de la columna vs total de la fila): {np.nanmean(np.abs(rr)):.2f}")
# (b) mismo patron en UR270 por separado
r270 = spearmanr(F270.prop_media, F278.prop_media)
print(f"UR270 (7 filas) reproduce el rango de UR278: rho={r270.statistic:.2f}")

# ---------------------------------------------------------------- resumen de pruebas
Pru = pd.DataFrame([
    dict(prueba="Friedman columnas (26 filas completas)", estadistico=float(chi),
         nulo="", p=float(p_fried)),
    dict(prueba="varianza de medias por columna", estadistico=float(obs),
         nulo=float(null.mean()), p=float(p_var)),
    dict(prueba="Spearman medio entre filas", estadistico=float(np.mean(tau)),
         nulo=float(np.mean(tau_null)), p=float(p_tau)),
    dict(prueba="maximo en c1/c2 (18/28)", estadistico=float(n_mx12),
         nulo=float(n * 2 / 9), p=float(p_mx)),
    dict(prueba="minimo en c8/c9 (16/28)", estadistico=float(n_mn89),
         nulo=float(n * 2 / 9), p=float(p_mn)),
    dict(prueba="identidad optima en 5/5 pares", estadistico=5.0,
         nulo=1.0, p=float(np.prod(O.p_permutacion))),
    dict(prueba="rho firma UR278 vs UR270", estadistico=float(r270.statistic),
         nulo=0.0, p=float(r270.pvalue)),
    dict(prueba="|rho| proporcion vs total (media)", estadistico=float(np.nanmean(np.abs(rr))),
         nulo=0.0, p=np.nan),
])
Pru.to_csv("pruebas_columnas.csv", index=False, encoding="utf-8-sig")
print("\npruebas_columnas.csv:")
print(Pru.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
