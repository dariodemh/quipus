"""Utilidades comunes de 10_tablas: selección de quipus tabulares y construcción de matrices filas x columnas.

Fila = grupo de colgantes del tamaño modal (>=2) del quipu; columna = posición dentro del grupo.
Igual que 03_gramatica/t2_tabla.py, salvo que aquí se excluyen las cuerdas superiores (union T),
que se tratan aparte como candidatas a resumen. Celda vacía (sin nudos) = NaN (ausente, no cero).
Unidad de análisis = quipu. Semilla fija.
"""
import re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import false_discovery_control

RAIZ = Path(r"./analisis")
OUT = RAIZ / "10_tablas"
SEED = 20261017


def bh(p):
    p = np.asarray(p, float)
    q = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    if ok.any():
        q[ok] = false_discovery_control(p[ok])
    return q


def pemp(obs, null, mayor=True):
    """p empírico unilateral con +1."""
    null = np.asarray(null, float)
    null = null[~np.isnan(null)]
    if np.isnan(obs) or len(null) == 0:
        return np.nan
    k = (null >= obs - 1e-12).sum() if mayor else (null <= obs + 1e-12).sum()
    return (k + 1) / (len(null) + 1)


def color_base(c):
    """Código Ascher sin rangos en cm; primer token = color principal."""
    if not isinstance(c, str) or not c.strip():
        return "?", "?"
    k = re.sub(r"\([^)]*\)", "", c).strip()
    t = [x for x in re.split(r"[:/%*_\-]+", k) if x]
    return k, (t[0] if t else "?")


def cargar():
    c = pd.read_csv(RAIZ / "datos" / "cuerdas.csv", low_memory=False)
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    c["v"] = np.where(c.nudos.notna(), c.valor, np.nan)
    cb = c.color.map(color_base)
    c["ckey"] = cb.str[0]
    c["cmain"] = cb.str[1]
    c["tipos"] = c.nudos.fillna("").map(lambda s: "".join(re.findall(r"\d+([A-Z]+)\(", s)) or "-")
    c["nsub"] = c.cuerda.map(lambda s: 0)  # se rellena abajo
    hijos = c[c.nivel == 1].groupby(["kfg", "padre"]).size()
    idx = pd.MultiIndex.from_arrays([c.kfg, c.cuerda])
    c["nsub"] = hijos.reindex(idx).fillna(0).astype(int).to_numpy()
    return c


def seleccion():
    """Quipus con estructura de columnas fuerte según 02 (columna_fuerte) o 03 (grupos explícitos q<0,05)."""
    t = pd.read_csv(RAIZ / "03_gramatica" / "resultados" / "t2_por_quipu.csv")
    t = t[t.clase == "quipu"]
    g = t.pivot_table(index="kfg", columns="var", values="q_g_p")
    m = pd.read_csv(RAIZ / "02_color" / "resultados_t1_mi.csv")
    m = m[m.variante == "full"].set_index("kfg")
    s = pd.DataFrame(index=sorted(set(g.index) | set(m.index)))
    s["q03_color"] = g["color"]
    s["q03_magn"] = g["magn"]
    s["fuerte02"] = m["columna_fuerte"].reindex(s.index, fill_value=False).astype(bool)
    s["sel"] = (s.q03_color < .05) | (s.q03_magn < .05) | s.fuerte02
    return s[s.sel]


def matriz(cq):
    """cq = cuerdas de un quipu. Devuelve dict con V (R x K valores, NaN vacío), C (color), T (tipos de nudo),
    O (orden de la cuerda), grupos (ids de grupo de cada fila) o None."""
    p = cq[(cq.nivel == 0) & (cq.union != "T")]
    tam = p.groupby("grupo").size()
    vc = tam[tam >= 2].value_counts()
    if vc.empty:
        return None
    K = int(vc.idxmax())
    gs = tam[tam == K].index.to_numpy()
    if len(gs) < 3:
        return None
    pp = p[p.grupo.isin(gs)]
    R = len(gs)
    sh = (R, K)
    return {"V": pp.v.to_numpy(float).reshape(sh), "C": pp.ckey.to_numpy().reshape(sh),
            "Cm": pp.cmain.to_numpy().reshape(sh), "T": pp.tipos.to_numpy().reshape(sh),
            "O": pp.orden.to_numpy().reshape(sh), "S": pp.nsub.to_numpy().reshape(sh), "grupos": gs,
            "K": K, "R": R}


def matrices():
    c = cargar()
    s = seleccion()
    out = {}
    for k in s.index:
        m = matriz(c[c.kfg == k])
        if m is not None:
            out[k] = m
    return out, c, s


# ---------------------------------------------------------------- permutaciones
def perm_fila(V, rng):
    """Baraja las celdas dentro de cada fila (destruye identidad de columna, conserva cada fila)."""
    return rng.permuted(V, axis=1)


def perm_col(V, rng):
    """Baraja cada columna entre filas por separado (conserva cada columna, destruye la coherencia de fila)."""
    return rng.permuted(V, axis=0)


def perm_ambos(V, rng):
    """Nulo del encargo: filas barajadas entre sí y columnas barajadas dentro de cada fila."""
    return rng.permuted(rng.permutation(V, axis=0), axis=1)


if __name__ == "__main__":
    # autocomprobación mínima
    V = np.arange(12.).reshape(3, 4)
    r = np.random.default_rng(0)
    assert sorted(perm_fila(V, r)[1]) == [4, 5, 6, 7]
    assert sorted(perm_col(V, r)[:, 2]) == [2, 6, 10]
    assert abs(pemp(5, [1, 2, 3]) - 0.25) < 1e-9
    M, c, s = matrices()
    print(len(s), "seleccionados;", len(M), "con matriz (R>=3, K>=2)")
    print(pd.Series({k: (m["R"], m["K"]) for k, m in M.items()}).value_counts().head())
