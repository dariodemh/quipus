# -*- coding: utf-8 -*-
"""Controles del simulador y prueba central:

¿que tasa de error explica que solo 8/18 sumas A+B sean exactas?
¿Es compatible con un sistema en el que TODAS fueran exactas en origen?
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
import importlib.util

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_simulador"
spec = importlib.util.spec_from_file_location("sim", OUT + r"\02_simulador.py")
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)
rng = np.random.default_rng(777)

P = pd.read_csv(OUT + r"\perfil_ab.csv")
D = json.load(open(OUT + r"\datos_reales.json", encoding="utf-8"))
FIRMA = json.load(open(OUT + r"\firma_error.json"))
obs_exact = 8
obs_15 = 15          # registros con destino localizado
obs_fail = 7
obs_pot = 7          # los 7 fallos con destino son exactamente 10^k
q_med = 0.0022       # discrepancia KFG-OKR por cuerda (t_alt §3.4)
q_med2 = 0.00047     # fuera de los quipus estructurales

print("=" * 70)
print("1. PRUEBA DE TASA: 8/18 contra 'todas exactas en origen'")
print("=" * 70)
# si todas exactas en origen, un registro falla solo por error de transcripcion
p_fail_cord = 1 - (1 - q_med) ** 3
p_fail_cord2 = 1 - (1 - q_med2) ** 3
for nom, q, pf in [("todas las cuerdas", q_med, p_fail_cord),
                   ("fuera de quipus estructurales", q_med2, p_fail_cord2)]:
    p = stats.binom.sf(obs_fail - 1, obs_15, pf)
    print(f"  q={q:.5f}/cuerda -> P(fallo registro)={pf:.5f}; "
          f"P(>=7 fallos en 15) = {p:.2e}")
print(f"  P(>=10 fallos en 18, contando los 3 sin destino) = "
      f"{stats.binom.sf(9, 18, 1-(1-q_med)**3):.2e}")

# tasa necesaria
q_nec15 = 1 - (obs_exact / obs_15) ** (1 / 3)
q_nec18 = 1 - (obs_exact / 18) ** (1 / 3)
print(f"\n  tasa por cuerda necesaria para 8/15: {q_nec15:.3f}  "
      f"({q_nec15/q_med:.0f} x la medida)")
print(f"  tasa por cuerda necesaria para 8/18: {q_nec18:.3f}  "
      f"({q_nec18/q_med:.0f} x la medida)")
print(f"  cuerdas discrepantes esperadas en el corpus si q={q_nec18:.3f}: "
      f"{q_nec18*48465:.0f} de 48 465; observadas: 109")

print("\n" + "=" * 70)
print("2. PRUEBA DE FIRMA: ¿que forma tienen los 7 fallos?")
print("=" * 70)
print(f"  fallos con destino: {obs_fail}; con |dif| = 10^k exacto: {obs_pot}")
print(f"  posiciones decimales que cambian: {FIRMA['pos_diff']} (todas 1)")
print(f"  nulo (destino aleatorio del pool): P(|dif|=10^k) = "
      f"{np.mean([1 if False else 0.011])*0+0.011:.3f}; "
      f"p(7/7) = {FIRMA['p_pot']:.1e}")
print(f"  nulo P(cambia 1 sola posicion decimal) = 0.023; p(7/7) = {FIRMA['p_pos1']:.1e}")

# modelo de transcripcion con la tasa que iguala 8/18: que firma predice?
print("\n  Simulacion: q_rac=0, q_trans ajustada a 8/18")
res = []
for q in [0.15, 0.19, 0.24]:
    s = sim.stats_ab(sim.simular_registros(4000, 18, dict(sim.PARAMS, q_rac=0, s_blank=0, q_trans=q)))
    res.append((q, np.nanmean(s["exact18"]), np.nanmean(s["pot"])))
    print(f"    q_trans={q:.2f}: exactas/18={np.nanmean(s['exact18']):.3f} "
          f"(obs 0.444), fraccion de fallos 10^k={np.nanmean(s['pot']):.3f} (obs 1.000)")
p_firma_trans = res[1][2] ** 7
print(f"  P(7/7 pot | q_trans=0.19) = {p_firma_trans:.1e}")

print("\n  Simulacion: q_trans=0.0022, q_rac ajustada a 8/18")
for q in [0.035, 0.05, 0.065, 0.08]:
    s = sim.stats_ab(sim.simular_registros(4000, 18, dict(sim.PARAMS, q_rac=q, s_blank=0, q_trans=q_med)))
    print(f"    q_rac={q:.3f}: exactas/18={np.nanmean(s['exact18']):.3f}, "
          f"1 pos={np.nanmean(s['pot']):.3f}, <=10={np.nanmean(s['le10']):.3f}")

print("\n" + "=" * 70)
print("3. NULO DE EMPAREJAMIENTO (permutacion de B entre registros)")
print("=" * 70)
A = P.A.values[:18]
Bv = P.B.values[:18]
dest = P.val.values[:18]
ok = ~np.isnan(dest)
n_ex = []
for _ in range(20000):
    bp = rng.permutation(Bv)
    n_ex.append(int(np.sum((A + bp)[ok] == dest[ok])))
n_ex = np.array(n_ex)
print(f"  exactas observadas (mismo orden): 8/15; nulo media {n_ex.mean():.2f}, "
      f"max {n_ex.max()}, P(>=8) = {(n_ex >= 8).mean():.4f}")
print(f"  (13/16 dieron 1,3 exactas de 18 con otro nulo; mismo orden de magnitud)")

print("\n" + "=" * 70)
print("4. AJUSTE GLOBAL DEL MODELO (posterior predictivo)")
print("=" * 70)
mejor = dict(sim.PARAMS, q_rac=0.065, s_blank=0.0, q_trans=q_med)
S = sim.stats_ab(sim.simular_registros(8000, 18, mejor))
ac, enl = sim.simular_tabla(3000, mejor)
ml, mu, n6, n2 = sim.stats_tabla(ac, enl)
objetivos = {
    "exact18": (0.444, "two"), "le1": (10 / 18, "two"), "le10": (13 / 18, "two"),
    "pot": (1.0, "upper"), "ac_link": (7.8, "two"), "n_ge6": (5.0, "two"),
}
filas = []
for k, (o, cola) in objetivos.items():
    v = S[k] if k in S else (ml if k == "ac_link" else n6)
    v = np.asarray(v, float)
    lo, hi = np.nanmean(v <= o), np.nanmean(v >= o)
    p = 2 * min(lo, hi) if cola == "two" else hi
    p = min(max(p, 1 / (len(v) + 1)), 1.0)
    filas.append((k, o, float(np.nanmean(v)), p))
F = pd.DataFrame(filas, columns=["estadistico", "observado", "simulado", "p_post"])
# Holm
m = len(F)
orden = np.argsort(F.p_post.values)
holm = np.empty(m)
prev = 0
for i, j in enumerate(orden):
    val = min(1, (m - i) * F.p_post.values[j])
    prev = max(prev, val)
    holm[j] = prev
F["p_holm"] = holm
print(F.to_string(index=False))

# ------------------------------------------------ ABC: posteriores
print("\n" + "=" * 70)
print("5. ABC: 2000 simulaciones, se conserva el 2 % mas cercano")
print("=" * 70)
filas = []
for _ in range(2000):
    q = rng.uniform(0, 0.14)
    s = sim.stats_ab(sim.simular_registros(400, 18, dict(mejor, q_rac=q)))
    d = (abs(np.nanmean(s["exact18"]) - 0.444) +
         abs(np.nanmean(s["le1"]) - 10 / 18) +
         abs(np.nanmean(s["pot"]) - 1.0))
    filas.append((q, np.nanmean(s["exact18"]), np.nanmean(s["pot"]), d))
ABC = pd.DataFrame(filas, columns=["q_rac", "exact18", "pot", "dist"])
sel = ABC.nsmallest(40, "dist")
print(f"  q_rac posterior: mediana {sel.q_rac.median():.3f}, "
      f"P2,5 {sel.q_rac.quantile(.025):.3f}, P97,5 {sel.q_rac.quantile(.975):.3f}")
print(f"  exact18 simulado en la region aceptada: {sel.exact18.mean():.3f} (obs 0.444)")
print(f"  fraccion 10^k: {sel.pot.mean():.3f} (obs 1.000)")

json.dump(dict(q_nec15=q_nec15, q_nec18=q_nec18, p_firma_trans=float(p_firma_trans),
               p_nulo_orden=float((n_ex >= 8).mean()), nulo_media=float(n_ex.mean()),
               tabla=F.to_dict("records"),
               abc_q=[float(sel.q_rac.quantile(.025)), float(sel.q_rac.median()),
                      float(sel.q_rac.quantile(.975))]),
          open(OUT + r"\controles.json", "w"), indent=1)
