"""Aplica tres nulos por permutación a las relaciones KFG reimplementadas (B=1000 por quipu y nulo, semilla fija).
M0 barajar todo el quipu; M1 dentro de nivel; M2 dentro de nivel x nº de dígitos (conserva la magnitud de cada cuerda).
Huecos (0 sin nudos) fijos. Salidas: nulos_por_quipu.csv, nulos_corpus.npz."""
import time, numpy as np, pandas as pd
from multiprocessing import Pool
from kfg import *

B = 1000
MODOS = {0: "M0_quipu", 1: "M1_nivel", 2: "M2_magnitud"}
QS = None


def init():
    global QS
    QS = cargar()


def ext(M):  # añade columna any4 = >=1 relación de los 4 tipos
    return np.c_[M, (M[..., :4].sum(-1) > 0)]


def tarea(args):
    i, k = args
    Q = QS[k]
    F = digit_model(Q["v"][Q["pres"]])
    o = ext(obs(Q, F)[None])[0]
    row = {"kfg": k, "n_colg": len(Q["P"]), "n_pres": int(Q["pres"].sum())}
    names = NOMBRES + ["any4"]
    for j, nm in enumerate(names):
        row[f"obs_{nm}"] = o[j]
    agg = {}
    for m, mn in MODOS.items():
        pidx, seg = estratos(Q, m)
        R = ext(run_null(Q["v"], Q["P"], Q["S"], Q["spar"], Q["col"], Q["gid"], Q["gi"], Q["ng"], pidx, seg, B, 1009 * (m + 1) + 7 * i, F))
        for j, nm in enumerate(names):
            c = R[:, j]
            row[f"E_{mn}_{nm}"] = c.mean(); row[f"sd_{mn}_{nm}"] = c.std()
            row[f"p_{mn}_{nm}"] = (1 + (c >= o[j]).sum()) / (B + 1)
            row[f"P1_{mn}_{nm}"] = (c > 0).mean()
        agg[m] = (R.astype(np.float32), (R > 0).astype(np.int16))
    return row, agg


if __name__ == "__main__":
    t = time.time()
    Qs = cargar()
    ks = sorted(Qs, key=lambda k: -len(Qs[k]["P"]))
    with Pool(16, initializer=init) as P:
        res = P.map(tarea, list(enumerate(ks)), chunksize=1)
    d = pd.DataFrame([r for r, _ in res])
    d.to_csv("nulos_por_quipu.csv", index=False)
    out = {}
    for m, mn in MODOS.items():
        out[f"{mn}_sum"] = sum(a[m][0] for _, a in res)
        out[f"{mn}_ind"] = sum(a[m][1].astype(np.int32) for _, a in res)
    np.savez_compressed("nulos_corpus.npz", **out)
    print("listo", round(time.time() - t), "s")
