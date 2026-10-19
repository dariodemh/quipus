"""Resolución de p: con B=1000 el p mínimo es 1/1001 y BH sobre ~480 quipus exige >=10 quipus en el mínimo para dar
q<0,05; el número de "significativos" queda acotado por B. Recalcula con B=20000 los quipus con p<0,05 en algún
estadístico (M1, M2) y repite BH con los p refinados (los demás conservan su p de B=1000).
Incluye el nulo por columnas para IDX. Salida: refinado.csv, salida_06_refinar.txt."""
import numpy as np, pandas as pd
from multiprocessing import Pool
from kfg import *

B2 = 20000
ST = ["PPS", "COL", "IDX", "SUB", "PPS_ady", "PPS_100", "PPS_ady100", "PPS_cadena", "PPS_cara01", "PPS_sumlog_local"]
MOD = {1: "M1_nivel", 2: "M2_magnitud"}
QS = None


def init():
    global QS
    QS = cargar()


def tarea(args):
    i, k = args
    Q = QS[k]; F = digit_model(Q["v"][Q["pres"]])
    o = obs(Q, F)
    row = {"kfg": k}
    for m, mn in MOD.items():
        pidx, seg = estratos(Q, m)
        R = run_null(Q["v"], Q["P"], Q["S"], Q["spar"], Q["col"], Q["gid"], Q["gi"], Q["ng"], pidx, seg, B2, 777 * m + 13 * i, F)
        for s in ST:
            j = NOMBRES.index(s)
            row[f"p2_{mn}_{s}"] = (1 + (R[:, j] >= o[j]).sum()) / (B2 + 1)
    return row


if __name__ == "__main__":
    d = pd.read_csv("nulos_por_quipu_q.csv")
    cand = d.kfg[np.any([d[f"p_{mn}_{s}"] < .05 for mn in MOD.values() for s in ST], axis=0)].tolist()
    print("candidatos", len(cand))
    with Pool(16, initializer=init) as P:
        res = P.map(tarea, list(enumerate(cand)), chunksize=1)
    r = pd.DataFrame(res)
    d = d.merge(r, on="kfg", how="left")
    L = [f"quipus refinados con B={B2}: {len(cand)}"]
    sig = {}
    for s in ST:
        parts = []
        for mn in MOD.values():
            p = d[f"p2_{mn}_{s}"].fillna(d[f"p_{mn}_{s}"])
            t = d[f"sd_{mn}_{s}"] > 0
            q = pd.Series(1.0, index=d.index); q[t] = bh(p[t])
            d[f"qr_{mn}_{s}"] = q
            sig[(s, mn)] = set(d.kfg[q < .05])
            parts.append(f"{mn}: test={t.sum()} p<.05={(p[t]<.05).sum()} (esp {.05*t.sum():.0f}) q<.05={(q<.05).sum()} q<.10={(q<.10).sum()}")
        L.append(f"{s}: " + " | ".join(parts))
    loc = ["PPS_ady", "PPS_ady100", "PPS_sumlog_local", "PPS_cara01"]
    glob = ["PPS", "COL", "IDX", "SUB", "PPS_100", "PPS_cadena"]
    for mn in MOD.values():
        u = set().union(*[sig[(s, mn)] for s in loc]); g = set().union(*[sig[(s, mn)] for s in glob])
        L.append(f"{mn}: locales q<.05 {len(u)}: {sorted(u)}")
        L.append(f"{mn}: KFG sin localidad q<.05 {len(g)}: {sorted(g)}")
    uM1 = set().union(*[sig[(s, 'M1_nivel')] for s in loc]); uM2 = set().union(*[sig[(s, 'M2_magnitud')] for s in loc])
    L.append(f"locales en M1 y M2: {len(uM1 & uM2)}: {sorted(uM1 & uM2)}")
    d.to_csv("refinado.csv", index=False)
    print("\n".join(L)); open("salida_06_refinar.txt", "w", encoding="utf8").write("\n".join(L) + "\n")
