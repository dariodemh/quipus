"""Tabla de los 52 quipus de Incahuasi: ventanas, hits exactos no triviales (partes distintas, menor>=5, suma>=30), c modal, rango de x, cierre por primera cuerda."""
import pandas as pd
from collections import Counter
R = pd.read_csv("trios_por_quipu.csv"); D = pd.read_csv("trios_detalle.csv"); C = pd.read_csv("cierre_primera_por_quipu.csv").set_index("kfg")
D = D[D.exacto == 1]
def partes(r):
    x = [r.v1, r.v2, r.v3]; i = {"S1": 0, "S2": 1, "S3": 2}[r.patron]; p = sorted(x[:i]+x[i+1:]); return pd.Series(dict(tot=x[i], p_min=p[0], p_max=p[1]))
D = D.join(D.apply(partes, axis=1)); D = D[(D.p_min != D.p_max) & (D.p_min >= 5) & (D.tot >= 30)]
rows = []
for _, r in R[R.procedencia == "Incahuasi"].iterrows():
    d = D[D.kfg == r.kfg]; m = Counter(d.p_min).most_common(1)
    rows.append(dict(kfg=r.kfg, cuerdas_L0_presentes=r.n_cuerdas, ventanas=r.n_ventanas, grupos_de_3=r.n_trios3, hits_exactos_no_triviales=len(d), c_modal=m[0][0] if m else "", n_con_c_modal=m[0][1] if m else 0,
                     x_min=d.tot.min() if len(d) else "", x_max=d.tot.max() if len(d) else "", q_N1=r.q1_t0, q_N2_columnas=r.q2_t0 if r.n_trios3 >= 4 else "", cierre_primera_cuerda_t0=int(C.loc[r.kfg, "primera_t0"]) if r.kfg in C.index else ""))
T = pd.DataFrame(rows); T.to_csv("tabla_incahuasi.csv", index=False); pd.set_option("display.width", 250); print(T.round(3).to_string())
