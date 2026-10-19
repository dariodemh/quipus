"""Carga común para 13_sistema_incahuasi (reutiliza analisis/09_incahuasi/comun.py)."""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[0] / "09_incahuasi"))
from comun import cargar  # noqa: E402

ARCHIVO = [f"JC{i:03d}" for i in range(1, 24)] + [f"UR{i}" for i in range(255, 281) if i not in (267, 273, 274)] \
    + ["UR267A", "UR267B", "UR273A", "UR273B", "UR274A", "UR274B"]
TOL = {0, 1, 10, 100, 1000, 10000}  # exacto o ±1 en un dígito


def casi(a, b):
    return abs(int(a) - int(b)) in TOL


def archivo():
    c, q = cargar()
    c = c[c.kfg.isin(ARCHIVO)].copy()
    return c, q


def volcar(c, k, f=None):
    """Imprime un quipu grupo a grupo: valor_color con subsidiarias entre corchetes."""
    s = c[c.kfg == k].sort_values("orden")
    out = []
    for g, x in s.groupby("grupo", sort=True):
        toks = []
        for _, r in x.iterrows():
            v = str(r.valor) if r.pres else "·"
            t = f"{v}_{r.color}" if r.nivel == 0 else f"[{r.cuerda[r.cuerda.find('s'):]}:{v}_{r.color}]"
            toks.append(t)
        p = x[(x.nivel == 0) & x.pres].valor.sum()
        out.append(f"g{g} (Σp={p}): " + " ".join(toks))
    txt = f"== {k}\n" + "\n".join(out)
    print(txt, file=f)
    return txt


import numpy as np  # noqa: E402
from numba import njit  # noqa: E402


@njit(cache=True)
def _tol(d):
    d = abs(d)
    return d == 0 or d == 1 or d == 10 or d == 100 or d == 1000 or d == 10000


@njit(cache=True)
def lcs(x, y):
    """Subsecuencia común más larga con coincidencia exacta o ±1 en un dígito."""
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            if _tol(x[i] - y[j]):
                H[i + 1, j + 1] = H[i, j] + 1
            else:
                H[i + 1, j + 1] = max(H[i, j + 1], H[i + 1, j])
    return H[n, m]


def vecinos_magnitud(pool, rng, k=40):
    """Devuelve f(v) que sustituye v por un valor del pool con magnitud parecida (uno de los k más cercanos en log)."""
    ps = np.sort(np.asarray(pool, dtype=np.int64))
    lp = np.log(ps)

    def f(vals):
        idx = np.searchsorted(lp, np.log(np.asarray(vals, dtype=float)))
        lo = np.clip(idx - k // 2, 0, len(ps) - k)
        return ps[lo + rng.integers(0, k, size=len(vals))]
    return f


def bh(p):
    from scipy.stats import false_discovery_control
    return false_discovery_control(np.asarray(p, dtype=float))
