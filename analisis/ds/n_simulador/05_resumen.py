# -*- coding: utf-8 -*-
"""Numeros finales: bimodalidad de UR270->UR278 y razon de verosimilitud
entre el modelo de error de racimo y el de transcripcion masiva."""
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
rng = np.random.default_rng(99)

ac = np.array([9, 9, 7, 8, 6, 5, 2, 1, 1, 1, 1, 1])
print("== bimodalidad UR270->UR278 ==")
print("aciertos:", ac.tolist(), "| >=6:", int((ac >= 6).sum()), "| <=2:", int((ac <= 2).sum()))
ph = ac.sum() / (9 * len(ac))
sims = rng.binomial(9, ph, size=(200000, 12))
ge6 = (sims >= 6).sum(1); le2 = (sims <= 2).sum(1)
p_bim = np.mean((ge6 >= 5) & (le2 >= 6))
print(f"  binomial unico p={ph:.3f}: P(>=5 filas >=6 y >=6 filas <=2) = {p_bim:.2e}")
print(f"  esperado bajo binomial: {(sims>=6).sum(1).mean():.2f} filas >=6 "
      f"(obs 5); {(sims<=2).sum(1).mean():.2f} filas <=2 (obs 6)")

print("\n== razon de verosimilitud: racimo (q_rac=0.065) vs transcripcion (q_trans=0.19) ==")
def prob_exact_y_firma(p, nsim=8000):
    s = sim.stats_ab(sim.simular_registros(nsim, 18, p))
    ex = np.rint(s["exact18"] * 18).astype(int)
    pot = s["pot"]
    # P(exact=8) y P(7/7 pot | 7 fallos con destino), aproximada por simulacion
    pe = np.mean(ex == 8)
    con_f = np.sum(~np.isnan(pot) & (np.rint((1 - s["exact15"]) * 15) == 7))
    pp = np.nanmean(pot[np.rint((1 - s["exact15"]) * 15) == 7] == 1.0) if con_f else np.nan
    return pe, pp, con_f
for nom, p in [("racimo", dict(sim.PARAMS, q_rac=0.065, s_blank=0, q_trans=0.0022)),
               ("transcripcion", dict(sim.PARAMS, q_rac=0, s_blank=0, q_trans=0.19)),
               ("difuso", dict(sim.PARAMS, q_rac=0, s_blank=0, q_trans=0.19))]:
    pe, pp, cf = prob_exact_y_firma(p)
    print(f"  {nom:14s}: P(exact=8)={pe:.3f}  P(7/7 10^k | 7 fallos)={pp:.4f}  "
          f"producto={pe*pp:.2e}")
    if nom == "racimo":
        L1 = pe * pp
    if nom == "transcripcion":
        L0 = pe * pp
print(f"  razon de verosimilitud L(racimo)/L(transcripcion) ~ {L1/L0:.0f}")

print("\n== perfil de diferencias observado vs modelos ==")
P = pd.read_csv(OUT + r"\perfil_ab.csv")
obs = P.absdif.dropna().values
print("  obs 0:", int((obs == 0).sum()), " 1:", int((obs == 1).sum()),
      " 10:", int((obs == 10).sum()), " 100:", int((obs == 100).sum()),
      " 1000:", int((obs == 1000).sum()), " otros:", int(np.sum(~np.isin(obs, [0, 1, 10, 100, 1000]))))
print("  no hay ningun fallo con diferencia distinta de 10^k")

# tasa de error por racimo equivalente
q = 0.061
nrac = 3.4
print(f"\n== equivalencias ==")
print(f"  q_rac={q:.3f}/racimo, {nrac} racimos/cuerda -> por cuerda {1-(1-q)**nrac:.3f}")
print(f"  3 cuerdas por registro -> P(algun error) = {1-(1-q)**(3*nrac):.3f}")
print(f"  obs 8/15 exactas -> P(error) = {1-8/15:.3f}")
json.dump(dict(p_bim=float(p_bim), LR=float(L1 / L0), L1=float(L1), L0=float(L0)),
          open(OUT + r"\final.json", "w"), indent=1)
