"""P2b (post hoc, declarado): ¿la preferencia W de la cabecera-máximo (T3) y del total (T1)
sobrevive sin el archivo de Incahuasi y por registrador? Salida: p2b_preferido.csv"""
from collections import Counter

import numpy as np
import pandas as pd

import comun24 as C

rng = np.random.default_rng(C.SEED)
REP = 1999
c = C.cargar()
q = pd.read_csv(C.DAT / "quipus.csv", keep_default_na=False)
inca = set(q[q.region.str.contains("Inca", case=False) | q.procedencia.str.contains("Inca", case=False)].kfg)
c0 = c[(c.nivel == 0) & (c.col != "")]
pool = {kg: list(x.col) for kg, x in c0.groupby(["kfg", "grupo"])}
I = pd.read_csv(C.AQUI / "p2_instancias.csv", keep_default_na=False)
I["grupo"] = I.grupo.astype(int)
out = []
for t in ["T1", "T3"]:
    for lab, filt in [("sin Incahuasi", lambda d: ~d.kfg.isin(inca)), ("solo Incahuasi", lambda d: d.kfg.isin(inca)),
                      ("UR sin Incahuasi", lambda d: (d.reg == "UR") & ~d.kfg.isin(inca)),
                      ("AS", lambda d: d.reg == "AS")]:
        x = I[(I.tipo == t) & filt(I)]
        qs = [(k, y) for k, y in x.groupby("kfg") if len(y) >= 3]
        if len(qs) < 3:
            continue
        obs = sum(Counter(y.col).most_common(1)[0][0] == "W" for _, y in qs)
        pools = [[pool[(k, g)] for g in y.grupo] for k, y in qs]
        nul = np.array([sum(Counter([p[rng.integers(len(p))] for p in pl]).most_common(1)[0][0] == "W"
                            for pl in pools) for _ in range(REP)])
        out.append(dict(tipo=t, subconjunto=lab, n_quipus=len(qs), modal_W=obs, nulo_W=round(nul.mean(), 2),
                        p=C.p_emp(obs, nul)))
R = pd.DataFrame(out)
R.to_csv(C.AQUI / "p2b_preferido.csv", index=False)
print(len(inca), "quipus de Incahuasi")
print(R.to_string())

# control de posición: en los mismos quipus, ¿la primera cuerda que NO es máximo también es W?
c0 = c0.sort_values(["kfg", "orden"]).copy()
c0["pos"] = c0.groupby(["kfg", "grupo"]).cumcount()
c0["k"] = c0.groupby(["kfg", "grupo"]).pos.transform("size")
t3 = I[I.tipo == "T3"]
qs = [k for k, y in t3.groupby("kfg") if len(y) >= 3]
prim = c0[(c0.pos == 0) & (c0.k >= 3) & c0.kfg.isin(qs) & c0.pres]
prim = prim[~prim.set_index(["kfg", "grupo"]).index.isin(t3.set_index(["kfg", "grupo"]).index)]
w_t3 = (t3[t3.kfg.isin(qs)].col == "W").mean()
w_pr = (prim.col == "W").mean()
# por quipu: diferencia W(T3) - W(primera no máximo); signo
d = []
for k in qs:
    a = t3[t3.kfg == k].col.eq("W").mean()
    b = prim[prim.kfg == k].col.eq("W")
    if len(b) >= 3:
        d.append(a - b.mean())
d = np.array(d)
from scipy.stats import wilcoxon
nz = d[d != 0]
pw = wilcoxon(nz).pvalue if len(nz) > 5 else np.nan
ctrl = pd.DataFrame([dict(W_T3=round(w_t3, 3), W_primera_no_max=round(w_pr, 3), quipus=len(d),
                          T3_mas_W=int((d > 0).sum()), T3_menos_W=int((d < 0).sum()), p_wilcoxon=pw)])
ctrl.to_csv(C.AQUI / "p2b_control_posicion.csv", index=False)
print(ctrl.to_string())
