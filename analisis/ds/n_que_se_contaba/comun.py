"""Utilidades comunes de n_que_se_contaba.

Reglas del brief: unidad de analisis = quipu; nulos explicitos; semilla fija;
correccion multiple BH. Valores 0 sin nudos = ausentes (NaN).
"""
from pathlib import Path
import re
import numpy as np
import pandas as pd
from scipy.stats import false_discovery_control

RAIZ = Path(r"./analisis")
OUT = RAIZ / "ds" / "n_que_se_contaba"
SEED = 20261017


def bh(p):
    p = np.asarray(p, float)
    q = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    if ok.any():
        q[ok] = false_discovery_control(p[ok])
    return q


def pemp(obs, null, mayor=True):
    """p empirico unilateral con +1 (nunca 0)."""
    null = np.asarray(null, float)
    null = null[~np.isnan(null)]
    if np.isnan(obs) or len(null) == 0:
        return np.nan
    k = (null >= obs - 1e-12).sum() if mayor else (null <= obs + 1e-12).sum()
    return (k + 1) / (len(null) + 1)


def cargar():
    c = pd.read_csv(RAIZ / "datos" / "cuerdas.csv", low_memory=False)
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    # valor valido solo si hay nudos (0 sin nudos = ausente)
    c["v"] = np.where(c.nudos.notna() & c.nudos.astype(str).str.strip().ne(""),
                       c.valor, np.nan)
    return c


def tablas(c, min_filas=3, min_cols=4, modo="modal"):
    """Reconstruye matrices filas x columnas como 10_tablas/comun.matriz.

    Fila = grupo de colgantes de tamano modal (>=2); columna = posicion dentro del grupo.
    Devuelve dict kfg -> dict(V, R, K, grupos, colores).
    """
    out = {}
    base = c[(c.nivel == 0) & (c.union != "T")]
    for k, cq in base.groupby("kfg", sort=True):
        tam = cq.groupby("grupo").size()
        vc = tam[tam >= 2].value_counts()
        if vc.empty:
            continue
        K = int(vc.idxmax())
        if K < min_cols:
            continue
        gs = tam[tam == K].index.to_numpy()
        if len(gs) < min_filas:
            continue
        pp = cq[cq.grupo.isin(gs)]
        if len(pp) != len(gs) * K:  # seguridad
            continue
        V = pp.v.to_numpy(float).reshape(len(gs), K)
        if np.isfinite(V).sum() < 0.6 * V.size:
            continue
        out[k] = {"V": V, "R": len(gs), "K": K, "grupos": gs,
                  "colores": pp.color.to_numpy().reshape(len(gs), K)}
    return out


# ---------------------------------------------------------------- demografia
def siler_lx(x, a1=0.20, b1=1.0, a2=0.025, a3=4.5e-5, b3=0.09):
    """Supervivencia l(x) bajo mortalidad Siler (x en anos). Aproxima una
    tabla de vida preindustrial de alta mortalidad (e0 ~ 28 anos)."""
    x = np.asarray(x, float)
    H = (a1 / b1) * (1 - np.exp(-b1 * x)) + a2 * x + (a3 / b3) * (np.exp(b3 * x) - 1)
    return np.exp(-H)


def edad_estable(bordes, r=0.0):
    """Distribucion de edad estable (r=0) para bandas [b0,b1)."""
    bordes = np.asarray(bordes, float)
    L = np.array([siler_lx(bordes[i]) - siler_lx(bordes[i + 1]) for i in range(len(bordes) - 1)])
    w = np.exp(-r * (bordes[:-1] + np.diff(bordes) / 2))
    p = L * w
    return p / p.sum()


def bandas_5(n=9):
    """n bandas quinquenales desde 0-4; la ultima abierta."""
    b = list(range(0, 5 * n + 1, 5))
    return np.array(b[: n + 1], float)


def perfil_piramide(sh, modelo):
    """Ajuste maximo sobre todas las permutaciones de columnas.
    sh: matriz R x K de proporciones por fila (filas normalizadas).
    modelo: vector K de proporciones esperadas.
    Devuelve (r_max, perm) con r de Pearson medio entre fila observada y modelo.
    """
    from itertools import permutations
    K = sh.shape[1]
    obs = sh.mean(0)
    best = (-2, None)
    for perm in permutations(range(K)):
        m = modelo[list(perm)]
        # correlacion entre el perfil medio observado y el modelo
        if np.std(m) < 1e-12:
            continue
        r = np.corrcoef(obs, m)[0, 1]
        if r > best[0]:
            best = (r, perm)
    return best


def cv_intrafila(V):
    """Coeficiente de variacion dentro de fila (dispersion de magnitudes)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        mu = np.nanmean(V, axis=1)
        sd = np.nanstd(V, axis=1, ddof=1)
        cv = sd / mu
    return cv[np.isfinite(cv)]


def razon_max_min(V):
    with np.errstate(invalid="ignore", divide="ignore"):
        mx = np.nanmax(V, axis=1)
        mn = np.nanmin(V, axis=1)
        r = mx / mn
    return r[np.isfinite(r)]
