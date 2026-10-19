"""Resume sumas_por_quipu.csv: q-values BH por tipo y nulo, fracción de quipus con contabilidad interna, tasa base."""
import json, numpy as np, pandas as pd
from pathlib import Path
from nucleo import bh
D = Path(__file__).parent
d = pd.read_csv(D / "sumas_por_quipu.csv")
q = pd.read_csv(D.parents[0] / "datos/quipus.csv")
MODOS = ["N1_global", "N2_nivel", "N3_nivel_grupo", "N4_bloques_grupo"]
TIPOS = ["R1", "F", "A", "TA", "R4", "R5a", "R5b", "Fany", "Fsub", "comp"]
for m in MODOS:
    for s in TIPOS:
        t = d[f"sd_{m}_{s}"] > 0
        qq = pd.Series(1.0, index=d.index); qq[t] = bh(d.loc[t, f"p_{m}_{s}"])
        d[f"q_{m}_{s}"] = qq; d[f"test_{m}_{s}"] = t
d["sig_N2"] = d["q_N2_nivel_comp"] < .05
d["sig_N4"] = d["q_N4_bloques_grupo_comp"] < .05
d["sig_N1"] = d["q_N1_global_comp"] < .05
d["sig_N3"] = d["q_N3_nivel_grupo_comp"] < .05
d["sig_TA_N2"] = d["q_N2_nivel_TA"] < .05
d["exceso_comp"] = d["obs_comp"] - d["E_N2_nivel_comp"]
d = d.merge(q[["kfg", "procedencia"]], on="kfg")
d.to_csv(D / "resultado_por_quipu.csv", index=False)
n = len(d)
print("n quipus", n)
rows = []
for s in TIPOS:
    r = dict(tipo=s, **{"n>=1_obs": int((d[f"obs_{s}"] > 0).sum())})
    for m in MODOS:
        r[f"{m}:E_n>=1"] = round(d[f"P1_{m}_{s}"].sum(), 1)
        r[f"{m}:testables"] = int(d[f"test_{m}_{s}"].sum())
        r[f"{m}:p<.05"] = int((d[f"p_{m}_{s}"] < .05).sum())
        r[f"{m}:q<.05"] = int((d[f"q_{m}_{s}"] < .05).sum())
    rows.append(r)
T = pd.DataFrame(rows).set_index("tipo")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 50)
print(T.T)
T.to_csv(D / "tabla_deteccion_por_tipo.csv")
# Storey pi0 (lambda=0.5) para el compuesto, N2 y N4
for m in ["N1_global", "N2_nivel", "N3_nivel_grupo", "N4_bloques_grupo"]:
    t = d[f"test_{m}_comp"]; p = d.loc[t, f"p_{m}_comp"].values
    pi0 = min(1, (p > .5).mean() / .5)
    print(m, "testables", t.sum(), "pi0", round(pi0, 3), "fraccion no nula (sobre testables) >=", round(1 - pi0, 3), "p<.05:", (p < .05).sum(), "esperados por azar:", round(.05 * t.sum(), 1))
print("sig N1/N2/N3/N4:", d.sig_N1.sum(), d.sig_N2.sum(), d.sig_N3.sum(), d.sig_N4.sum(), "N2&N4:", (d.sig_N2 & d.sig_N4).sum(), "N2|N4|N1|N3:", (d.sig_N1 | d.sig_N2 | d.sig_N3 | d.sig_N4).sum())
print("TA sig N2:", d.sig_TA_N2.sum(), " T-quipus:", (d.obs_TA_elig > 0).sum())
# fracción que cumple >=1 relación "cruda"
for s in ["comp", "F", "Fany", "A", "R1", "R5b"]:
    print(s, "crudo >=1:", round((d[f"obs_{s}"] > 0).mean(), 3), " esperado nulo N2:", round(d[f"P1_N2_nivel_{s}"].mean(), 3), " N4:", round(d[f"P1_N4_bloques_grupo_{s}"].mean(), 3))
# por tamaño
d["tam"] = pd.cut(d.n_pos, [0, 10, 30, 100, 300, 5000])
print(d.groupby("tam", observed=True).agg(n=("kfg", "size"), sig_N2=("sig_N2", "sum"), testables=("test_N2_nivel_comp", "sum"), med_pos=("n_pos", "median")))
print(d[d.sig_N2][["kfg", "procedencia", "n_pos", "obs_comp", "E_N2_nivel_comp", "p_N2_nivel_comp", "q_N2_nivel_comp", "obs_R1", "obs_F", "obs_R4", "obs_R5a", "obs_R5b", "sig_N4"]].to_string())
print(d[d.sig_TA_N2][["kfg", "procedencia", "obs_TA", "obs_TA_elig", "E_N2_nivel_TA", "q_N2_nivel_TA", "q_N4_bloques_grupo_TA"]].to_string())
