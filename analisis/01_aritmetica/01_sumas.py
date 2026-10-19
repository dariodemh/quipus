"""Tarea 1: relaciones de suma por quipu vs nulos por permutación. Salida: sumas_por_quipu.csv, sumas_global.json."""
import sys, json, time
import numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nucleo import *

B = 2000
MODOS = {0: "N1_global", 1: "N2_nivel", 2: "N3_nivel_grupo", 3: "N4_bloques_grupo"}
STAT = {"R1": 0, "Fany": 13, "Fsub": 14, "F": 2, "A": 3, "TA": 4, "R4": 6, "R5a": 8, "R5b": 10}
QS = None


def init():
    global QS
    QS, _ = cargar()


def comp(M):  # compuesto: R1+F+R4+R5a+R5b (el nulo se calcula sobre la misma suma, así que el solapamiento no sesga)
    return M[..., 0] + M[..., 2] + M[..., 6] + M[..., 8] + M[..., 10]


def tarea(args):
    i, k = args
    Q = QS[k]
    obs = todo(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"])
    row = {"kfg": k, "n_cuerdas": len(Q["v"]), "n_pos": int(obs[12]), "n_grupos": len(Q["gs"]) - 1}
    for n, x in zip(NOMBRES, obs):
        row[f"obs_{n}"] = int(x)
    row["obs_comp"] = int(comp(obs))
    sums = {}
    for m, nm in MODOS.items():
        pidx, seg = estratos(Q, min(m, 2))
        R = run_null(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"], pidx, seg, B, 7919 * (m + 1) + i, m)
        sums[m] = np.c_[R, comp(R)]  # columna 16 = compuesto
        o = np.r_[obs, comp(obs)]
        for s, j in list(STAT.items()) + [("comp", 16)]:
            col = sums[m][:, j]
            row[f"E_{nm}_{s}"] = col.mean()
            row[f"sd_{nm}_{s}"] = col.std()
            row[f"p_{nm}_{s}"] = (1 + (col >= o[j]).sum()) / (B + 1)
            row[f"P1_{nm}_{s}"] = (col >= 1).mean()  # prob. nula de >=1 relación
    # también guardamos las sumas nulas para el nulo agregado del corpus (solo composite y tipos)
    return row, {m: sums[m][:, [0, 2, 3, 4, 6, 8, 10, 13, 14, 16]].astype(np.int32) for m in MODOS}


if __name__ == "__main__":
    t = time.time()
    Qs, q = cargar()
    ks = list(Qs)
    with Pool(12, initializer=init) as P:
        res = P.map(tarea, list(enumerate(ks)), chunksize=2)
    df = pd.DataFrame([r for r, _ in res])
    nullsum = {m: sum(s[m] for _, s in res) for m in MODOS}  # (B, 8) suma entre quipus, columnas R1,F,A,TA,R4,R5a,R5b,comp
    cols = ["R1", "F", "A", "TA", "R4", "R5a", "R5b", "Fany", "Fsub", "comp"]
    glob = {}
    for m, nm in MODOS.items():
        for j, s in enumerate(cols):
            o = df[f"obs_{s}"].sum()
            nl = nullsum[m][:, j]
            glob[f"{nm}_{s}"] = dict(obs=int(o), E=float(nl.mean()), sd=float(nl.std()), p=float((1 + (nl >= o).sum()) / (B + 1)))
    df.to_csv(__import__("pathlib").Path(__file__).parent / "sumas_por_quipu.csv", index=False)
    json.dump(glob, open(__import__("pathlib").Path(__file__).parent / "sumas_global.json", "w"), indent=1)
    print("listo", time.time() - t)
