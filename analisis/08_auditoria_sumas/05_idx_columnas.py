"""Sumas indexadas (IDX): nulo más duro que baraja los valores de colgantes DENTRO de cada columna (mismo índice en el
grupo) entre grupos. Conserva la distribución de cada columna (p. ej. columnas de valores repetidos) y destruye solo el
alineamiento entre grupos. B=2000. Salida: idx_columnas.csv."""
import numpy as np, pandas as pd
from numba import njit
from kfg import *

B = 2000


@njit(cache=True)
def null_col(a0, pres, gid, gi, ng, B, seed):
    np.random.seed(seed)
    out = np.zeros(B)
    n = len(a0)
    maxi = 0
    for i in range(n):
        if gi[i] + 1 > maxi: maxi = gi[i] + 1
    for b in range(B):
        a = a0.copy()
        for k in range(maxi):
            idx = np.array([i for i in range(n) if gi[i] == k and pres[i]], dtype=np.int64)
            x = a0[idx].copy(); np.random.shuffle(x)
            a[idx] = x
        out[b] = idx_sum(a, gid, gi, ng)
    return out


Qs = cargar()
d = pd.read_csv("nulos_por_quipu_q.csv")
rows = []
for i, k in enumerate(d.kfg):
    Q = Qs[k]
    a = Q["v"][Q["P"]]; pr = Q["pres"][Q["P"]]
    o = idx_sum(a, Q["gid"], Q["gi"], Q["ng"])
    r = null_col(a, pr, Q["gid"], Q["gi"], Q["ng"], B, 4242 + i)
    rows.append(dict(kfg=k, obs_IDX=o, E_col=r.mean(), sd_col=r.std(), p_col=(1 + (r >= o).sum()) / (B + 1)))
x = pd.DataFrame(rows)
t = x.sd_col > 0
x["q_col"] = 1.0; x.loc[t, "q_col"] = bh(x.loc[t, "p_col"])
x = x.merge(d[["kfg", "n_colg", "q_M2_magnitud_IDX", "E_M2_magnitud_IDX"]], on="kfg")
x.to_csv("idx_columnas.csv", index=False)
L = [f"IDX corpus: obs {x.obs_IDX.sum()} vs nulo columna {x.E_col.sum():.1f} (M2: {x.E_M2_magnitud_IDX.sum():.1f})",
     f"testables {t.sum()}, p<.05 {(x.p_col<.05).sum()} (esp {0.05*t.sum():.0f}), q<.05 {(x.q_col<.05).sum()}",
     x[(x.q_col < .05) | (x.q_M2_magnitud_IDX < .05)].round(4).to_string()]
print("\n".join(L)); open("salida_05_idx_columnas.txt", "w", encoding="utf8").write("\n".join(L) + "\n")
