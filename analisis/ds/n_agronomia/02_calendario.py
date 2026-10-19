# -*- coding: utf-8 -*-
"""
02_calendario.py -- que predice la agronomia para 9 periodos de 40 dias y
cuanto se parece a la firma real de UR278.
Pruebas exactas por enumeracion de subconjuntos (C(9,k)); Holm entre modelos.
"""
import numpy as np, pandas as pd, itertools, math
from pathlib import Path
from scipy import stats
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
rng = np.random.default_rng(20261018)

d = pd.read_csv(AQUI/"columnas_ur278.csv")
p = d.cuota.to_numpy(); partes = d.parte.tolist()
X = pd.read_csv(RAIZ/"analisis/13_sistema_incahuasi/ur278_tabla.csv")
X = X[X.n == 9][partes].to_numpy(float)

# --- 1. cuan "picuda" es la firma ----------------------------------------
cv_obs = p.std(ddof=1)/p.mean()
max_obs = p.max()
activos = math.ceil(1/max_obs)
print("Firma observada: CV=%.3f, cuota maxima=%.3f, periodos activos implicitos>=%d"
      % (cv_obs, max_obs, activos))
print("Si k periodos concentran toda la actividad y son iguales, cuota=1/k:")
for k in range(2, 10):
    print("   k=%d -> cuota por periodo %.3f" % (k, 1/k))

# CV teorico de calendarios de picos (pesos iguales en k periodos, 0 en el resto)
def cv_picos(k):
    w = np.zeros(9); w[:k] = 1/k
    return w.std(ddof=1)/w.mean()
print("CV teorico con picos en k periodos:", {k: round(cv_picos(k), 3) for k in (2, 3, 4, 5, 6)})
print("CV observado = %.3f -> equivalente a picos repartidos en ~%d periodos"
      % (cv_obs, round(1/cv_obs**2, 1)))

# --- 2. modelos de calendario -------------------------------------------
# Set = periodos con actividad (cosecha, o siembra en el modelo de mano de obra).
MODELOS = [
 ("M1_mani_1cosecha_enero", "maní, 1 cosecha; año inicia en enero (Guaman Poma); siembra p1, cosecha 140 d después", {4,5}),
 ("M2_mani_1cosecha_junio", "maní, 1 cosecha; año inicia en solsticio de junio; siembra p2 (ago), cosecha 140 d después", {5,6}),
 ("M3_mani_2cosechas_enero", "maní, 2 cosechas; siembras p1 y p5, cosechas p4-p5 y p8-p9", {4,5,8,9}),
 ("M4_mani_2cosechas_junio", "maní, 2 cosechas; siembras p2 y p6, cosechas p5-p6 y p9", {5,6,9}),
 ("M5_aji_continuo", "ají: trasplante y cosecha escalonada, 6 periodos", {3,4,5,6,7,8}),
 ("M6_frijol_3cosechas", "frijol, 3 cosechas (ciclo 100 d); siembras p1,p4,p7; cosechas p3,p6,p9", {3,6,9}),
 ("M7_siembra_p1p2", "mano de obra de siembra/preparación concentrada en p1-p2 (no cosecha)", {1,2}),
 ("M8_sin_estacionalidad", "actividad repartida por igual en los 9 periodos", set(range(1,10))),
]
filas = []
for nombre, desc, S in MODELOS:
    k = len(S)
    idx = [i for i in range(9) if (i+1) in S]
    dentro = p[idx].mean(); fuera = p[[i for i in range(9) if i not in idx]].mean() if k < 9 else dentro
    stat = dentro - fuera
    # p exacto: fraccion de subconjuntos del mismo tamano con stat >= observado
    if k == 9:
        pex = 1.0
    else:
        cnt = tot = 0
        for comb in itertools.combinations(range(9), k):
            tot += 1
            dd = p[list(comb)].mean() - p[[i for i in range(9) if i not in comb]].mean()
            if dd >= stat - 1e-12: cnt += 1
        pex = cnt/tot
    filas.append(dict(modelo=nombre, descripcion=desc, k=k, set=",".join(map(str, sorted(S))),
                      cuota_dentro=dentro, cuota_fuera=fuera, stat=stat, p_exacta=pex,
                      n_subconjuntos=tot if k < 9 else 1))
R = pd.DataFrame(filas)
# Holm
R = R.sort_values("p_exacta").reset_index(drop=True)
m = len(R); adj = []; prev = 0
for i, pv in enumerate(R.p_exacta):
    a = min(1.0, (m-i)*pv); a = max(a, prev); adj.append(a); prev = a
R["p_holm"] = adj
R = R.sort_values("p_exacta")
print("\nModelos de calendario (prueba exacta de subconjuntos):")
print(R[["modelo","k","cuota_dentro","cuota_fuera","stat","p_exacta","p_holm"]].to_string(index=False))

# --- 3. compatibilidad con "9 campos/cuadrillas" -------------------------
# CV esperado de 9 rendimientos independientes con CV de campo 15-30%
sims = []
for cvf in (0.10, 0.15, 0.20, 0.30):
    v = rng.normal(1.0, cvf, size=(20000, 9)).clip(0.05)
    v = v/v.sum(1, keepdims=True)
    sims.append((cvf, np.percentile(v.std(1, ddof=1)/v.mean(1), [5, 50, 95])))
print("\nCV de cuota esperado para 9 campos independientes (simulación):")
for cvf, q in sims:
    print("  CV de campo %.2f -> CV de cuota 5-50-95%%: %.3f / %.3f / %.3f"
          % (cvf, q[0], q[1], q[2]))

# --- 4. gradiente posicional dentro de fila ------------------------------
rho_fila = np.array([stats.spearmanr(np.arange(1, 10), X[i])[0] for i in range(len(X))])
signos = (rho_fila < 0).sum()
p_signo = stats.binomtest(signos, len(X), 0.5, alternative="greater").pvalue
print("\nGradiente posicional: %d/%d filas con rho<0 (sign test p=%.5f)"
      % (signos, len(X), p_signo))
print("  (las filas no son independientes; el test válido es el nulo de 01_datos.py, p=0.0245)")

R.to_csv(AQUI/"calendario_modelos.csv", index=False)
print("\nGuardado: calendario_modelos.csv")
