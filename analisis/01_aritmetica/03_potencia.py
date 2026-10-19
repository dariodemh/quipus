"""Potencia: planta una suma real (la última cuerda de cada grupo = suma de las anteriores del grupo) en una fracción phi de los
grupos de >=3 cuerdas presentes y mide qué fracción de quipus detecta el pipeline (compuesto, BH-FDR sobre 651 quipus)."""
import sys, numpy as np, pandas as pd
from multiprocessing import Pool
from pathlib import Path
from nucleo import *
B = 1000
QS = None
def init():
    global QS
    QS, _ = cargar()
def comp(M): return M[..., 0] + M[..., 2] + M[..., 6] + M[..., 8] + M[..., 10]
def plantar(Q, phi, rng):
    v = Q["v"].copy(); pres = Q["pres"].copy(); gs = Q["gs"]; L0 = Q["L0"]; n = 0
    for g in range(len(gs) - 1):
        idx = L0[gs[g]:gs[g + 1]]
        if len(idx) >= 3 and (v[idx[:-1]] > 0).sum() >= 2 and rng.random() < phi:
            v[idx[-1]] = v[idx[:-1]].sum(); pres[idx[-1]] = True; n += 1
    Q2 = dict(Q); Q2["v"] = v; Q2["pres"] = pres
    return Q2, n
def tarea(a):
    i, k, phi = a
    rng = np.random.default_rng(100 + i)
    Q, npl = plantar(QS[k], phi, rng)
    obs = comp(todo(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"]))
    out = {"kfg": k, "phi": phi, "plantadas": npl, "obs": int(obs)}
    for m, nm in [(1, "N2"), (2, "N3"), (3, "N4")]:
        p, s = estratos(Q, min(m, 2))
        R = comp(run_null(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"], p, s, B, 31 * i + m, m))
        out[f"p_{nm}"] = (1 + (R >= obs).sum()) / (B + 1); out[f"sd_{nm}"] = R.std()
    return out
if __name__ == "__main__":
    Qs, _ = cargar(); ks = list(Qs)
    jobs = [(i, k, phi) for phi in (1.0, 0.5, 0.0) for i, k in enumerate(ks)]
    with Pool(12, initializer=init) as P: res = P.map(tarea, jobs, chunksize=4)
    d = pd.DataFrame(res); rows = []
    for phi, e in d.groupby("phi"):
        for nm in ["N2", "N3", "N4"]:
            t = e[f"sd_{nm}"] > 0; q = pd.Series(1.0, index=e.index); q[t] = bh(e.loc[t, f"p_{nm}"])
            e = e.assign(**{f"q_{nm}": q})
            rows.append(dict(phi=phi, nulo=nm, quipus_con_plantacion=int((e.plantadas > 0).sum()), detectados_q05=int((q < .05).sum()),
                             detectados_p05=int((e[f"p_{nm}"] < .05).sum()),
                             pct_de_plantables=round(100 * (q < .05).sum() / max(1, (e.plantadas > 0).sum()), 1)))
    T = pd.DataFrame(rows); print(T.to_string()); T.to_csv(Path(__file__).parent / "potencia.csv", index=False)
