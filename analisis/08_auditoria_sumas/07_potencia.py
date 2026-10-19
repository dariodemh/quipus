"""Potencia del test por quipu (nulo M2, B=1000, BH sobre todo el corpus) plantando sumas como el equipo 01:
en una fracción phi de los grupos de >=3 colgantes (>=2 no nulos), la última cuerda := suma de las anteriores del grupo.
Compara estadísticos: PPS (definición KFG, sin localidad), PPS_ady, PPS_ady100, PPS_sumlog_local. Salida: potencia.csv."""
import numpy as np, pandas as pd
from multiprocessing import Pool
from kfg import *

B = 1000
PHI = (0.0, 0.1, 0.25, 0.5, 1.0)
ST = ["PPS", "PPS_ady", "PPS_ady100", "PPS_sumlog_local"]
QS = None


def init():
    global QS
    QS = cargar()


def plantar(Q, phi, rng):
    v = Q["v"].copy(); pres = Q["pres"].copy(); P = Q["P"]; n = 0
    for g in range(Q["ng"]):
        idx = P[Q["gid"] == g]
        if len(idx) >= 3 and (v[idx[:-1]] > 0).sum() >= 2 and rng.random() < phi:
            v[idx[-1]] = v[idx[:-1]].sum(); pres[idx[-1]] = True; n += 1
    Q2 = dict(Q); Q2["v"] = v; Q2["pres"] = pres
    return Q2, n


def tarea(a):
    i, k, phi = a
    Q, npl = plantar(QS[k], phi, np.random.default_rng(500 + i))
    F = digit_model(Q["v"][Q["pres"]])
    o = obs(Q, F)
    pidx, seg = estratos(Q, 2)
    R = run_null(Q["v"], Q["P"], Q["S"], Q["spar"], Q["col"], Q["gid"], Q["gi"], Q["ng"], pidx, seg, B, 99 * i + int(phi * 100), F)
    out = {"kfg": k, "phi": phi, "plantadas": npl}
    for s in ST:
        j = NOMBRES.index(s)
        out[f"p_{s}"] = (1 + (R[:, j] >= o[j]).sum()) / (B + 1); out[f"sd_{s}"] = R[:, j].std()
    return out


if __name__ == "__main__":
    Qs = cargar(); ks = sorted(Qs, key=lambda k: -len(Qs[k]["P"]))
    jobs = [(i, k, phi) for phi in PHI for i, k in enumerate(ks)]
    with Pool(16, initializer=init) as P:
        res = P.map(tarea, jobs, chunksize=2)
    d = pd.DataFrame(res); rows = []
    for phi, e in d.groupby("phi"):
        e = e.copy(); pl = e.plantadas > 0
        anyq = np.zeros(len(e), bool)
        for s in ST:
            t = e[f"sd_{s}"] > 0; q = pd.Series(1.0, index=e.index); q[t] = bh(e.loc[t, f"p_{s}"])
            if s != "PPS": anyq |= (q < .05).values
            rows.append(dict(phi=phi, estadistico=s, plantables=int(pl.sum()), det_q05=int((q[pl] < .05).sum()),
                             det_p05=int((e.loc[pl, f"p_{s}"] < .05).sum()), pot_q05=round((q[pl] < .05).mean(), 3) if pl.any() else 0,
                             pot_p05=round((e.loc[pl, f"p_{s}"] < .05).mean(), 3) if pl.any() else 0))
        rows.append(dict(phi=phi, estadistico="union_locales", plantables=int(pl.sum()), det_q05=int((anyq & pl.values).sum()),
                         pot_q05=round((anyq & pl.values).sum() / max(1, pl.sum()), 3)))
    T = pd.DataFrame(rows); print(T.to_string()); T.to_csv("potencia.csv", index=False)
    open("salida_07_potencia.txt", "w", encoding="utf8").write(T.to_string() + "\n")
