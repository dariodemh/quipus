"""Lateralidad de las sumas PPS (Medrano y Khosla: 54 % a la derecha vs ~50 % en pseudoquipus muestreados del corpus).
Aquí el nulo es intra-quipu: M1 (nivel) y M2 (nivel x magnitud), B=500. Estadístico: fracción de relaciones con
sumandos a la derecha (lado de la ventana; difiere levemente del signo de handedness del KFG)."""
import numpy as np, pandas as pd
from multiprocessing import Pool
from kfg import *
B = 500
QS = None
def init():
    global QS
    QS = cargar()
def tarea(a):
    i, k = a
    Q = QS[k]; F = digit_model(Q["v"][Q["pres"]])
    out = np.zeros((2, B, 2))
    for m in (1, 2):
        pidx, seg = estratos(Q, m)
        rng = np.random.default_rng(31 * i + m)
        for b in range(B):
            v = Q["v"].copy()
            for s in range(len(seg) - 1):
                x = v[pidx[seg[s]:seg[s + 1]]]; v[pidx[seg[s]:seg[s + 1]]] = rng.permutation(x)
            ri, rs, _ = pps(v[Q["P"]])
            out[m - 1, b] = [(rs > ri).sum(), len(ri)]
    return out
if __name__ == "__main__":
    r = pd.read_csv("relaciones_pps.csv")
    o = (r.lado == "der").mean()
    Qs = cargar(); ks = list(Qs)
    with Pool(16, initializer=init) as P:
        res = P.map(tarea, list(enumerate(ks)), chunksize=4)
    S = sum(res)
    L = [f"observado: {o:.3f} a la derecha ({(r.lado=='der').sum()}/{len(r)})"]
    for m, nm in ((0, "M1_nivel"), (1, "M2_magnitud")):
        f = S[m, :, 0] / S[m, :, 1]
        L.append(f"{nm}: media {f.mean():.3f} IC95 [{np.percentile(f,2.5):.3f}-{np.percentile(f,97.5):.3f}] p(>=obs)={(1+(f>=o).sum())/(B+1):.4f}")
    # por quipu: fracción de quipus con mayoría derecha
    g = r.groupby("kfg").lado.apply(lambda s: (s == "der").mean())
    L.append(f"quipus con >=5 relaciones: {(r.groupby('kfg').size()>=5).sum()}; mediana de fracción derecha {g[r.groupby('kfg').size()>=5].median():.3f}")
    print("\n".join(L)); open("salida_08_lateralidad.txt", "w", encoding="utf8").write("\n".join(L) + "\n")
