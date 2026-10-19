"""Hits exactos no triviales (partes distintas, parte menor>=5, suma>=30) fuera y dentro de Incahuasi; constancia de la parte menor."""
import pandas as pd
from collections import Counter
D = pd.read_csv(OUT_ := "trios_detalle.csv"); R = pd.read_csv("trios_por_quipu.csv").set_index("kfg")
D = D[D.exacto == 1].copy()
def partes(r):
    x = [r.v1, r.v2, r.v3]; i = {"S1": 0, "S2": 1, "S3": 2}[r.patron]; t = x[i]; p = sorted(x[:i]+x[i+1:]); return pd.Series(dict(tot=t, p_min=p[0], p_max=p[1]))
D = D.join(D.apply(partes, axis=1))
D = D[(D.p_min != D.p_max) & (D.p_min >= 5) & (D.tot >= 30)]
out = []
for k, d in D.groupby("kfg"):
    m = Counter(d.p_min).most_common(1)[0]
    out.append(dict(kfg=k, procedencia=R.loc[k, "procedencia"], hits=len(d), menor_modal=m[0], n_modal=m[1], prop_modal=m[1]/len(d), q1_t0=R.loc[k, "q1_t0"], q2_t0=R.loc[k, "q2_t0"]))
O = pd.DataFrame(out).sort_values("hits", ascending=False); O.to_csv("trios_no_triviales.csv", index=False)
print(O[O.hits >= 3].to_string())
