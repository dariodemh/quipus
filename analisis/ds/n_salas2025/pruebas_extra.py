# -*- coding: utf-8 -*-
"""Pruebas a nivel de quipu (evitar pseudorreplicación) y predicción 'cord = día'."""
import json
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar

RNG = np.random.default_rng(4242)
RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_salas2025"
c, q = cargar()
val = c[c.valida].copy()
p0 = float(val.par.mean())

qu = val.groupby("kfg").agg(n=("v", "size"), even=("par", "sum"),
                            total=("v", "sum"), u0=("u0", "sum"),
                            c100=("c100", "sum"),
                            unos=("v", lambda s: int((s == 1).sum()))).reset_index()
qu["frac_even"] = qu.even / qu.n
qu["frac_unos"] = qu.unos / qu.n
q10 = qu[qu.n >= 10].copy()
q10["z"] = (q10.even - q10.n * p0) / np.sqrt(q10.n * p0 * (1 - p0))
res = {}
res["n_quipus_n10"] = int(len(q10))
res["z_media"] = float(q10.z.mean())
res["z_sd"] = float(q10.z.std(ddof=1))
res["z_chi2"] = {"chi2": float(((q10.z) ** 2).sum()), "gl": int(len(q10)),
                 "p": float(stats.chi2.sf(((q10.z) ** 2).sum(), len(q10)))}
res["quipus_todos_pares"] = int((q10.even == q10.n).sum())
res["esperado_todos_pares"] = float((p0 ** q10.n).sum())
res["quipus_frac_even_gt_0.8"] = int((q10.frac_even > 0.8).sum())
res["esperado_frac_gt_0.8"] = float(sum(stats.binom.sf(int(np.floor(0.8 * n)), n, p0) for n in q10.n))
res["quipus_frac_even_lt_0.2"] = int((q10.frac_even < 0.2).sum())
res["esperado_frac_lt_0.2"] = float(sum(stats.binom.cdf(int(np.ceil(0.2 * n)) - 1, n, p0) for n in q10.n))

# paridad del total del quipu (si cada cuerda fuese un par, el total sería par)
obs_total_par = int((qu.total % 2 == 0).sum())
# nulo: permutar unidades dentro de cada quipu
B = 4000
cnt = 0
bloques = [(d.v.values.astype(int) // 10 * 10, (d.v.values.astype(int) % 10)) for _, d in val.groupby("kfg")]
for _ in range(B):
    s = 0
    for dec, uni in bloques:
        vp = dec + RNG.permutation(uni)
        if vp.sum() % 2 == 0:
            s += 1
    if s >= obs_total_par:
        cnt += 1
res["total_par"] = {"obs": obs_total_par, "n_quipus": int(len(qu)),
                    "tasa": float(obs_total_par / len(qu)),
                    "p_exceso": float((1 + cnt) / (B + 1))}

# ------------------------------------------- predicción cord = día (ssop)
grandes = qu[qu.n >= 100].copy()
res["cord_dia"] = {
    "n_quipus_ge100": int(len(grandes)),
    "fraccion_unos_media": float(grandes.frac_unos.mean()),
    "fraccion_unos_mediana": float(grandes.frac_unos.median()),
    "quipus_frac_unos_gt_0.8": int((grandes.frac_unos > 0.8).sum()),
    "quipus_frac_unos_lt_0.2": int((grandes.frac_unos < 0.2).sum()),
    "top": grandes.sort_values("frac_unos", ascending=False).head(10)[
        ["kfg", "n", "frac_unos"]].to_dict("records"),
}
print(json.dumps(res, ensure_ascii=False, indent=1))
with open(OUT + r"\extras.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
