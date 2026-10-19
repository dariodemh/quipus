"""Preparación de datos para n_narrative_threads.
Lee analisis/datos/cuerdas.csv y quipus.csv; no modifica nada.
"""
import re
import numpy as np
import pandas as pd

BASE = "."
RNG = np.random.default_rng(20261018)


def clean_color(s):
    if not isinstance(s, str):
        return ""
    s = re.sub(r"\([^)]*\)", "", s)
    return s.strip()


def color_family(s):
    """Primera familia cromática del código Ascher (antes de :, -, /)."""
    s = clean_color(s)
    if not s:
        return ""
    return re.split(r"[:/\-]", s)[0]


def is_chromatic(s):
    """Color 'marcado' = no blanco ni marrón natural (W, AB, MB, KB...)."""
    f = color_family(s)
    if not f:
        return np.nan
    return 0 if f in {"W", "AB", "MB", "KB", "LB", "NB", "DB", "HB", "YB", "B"} else 1


def knot_dirs(nudos):
    """Devuelve lista de direcciones S/Z de los nudos de una cuerda."""
    if not isinstance(nudos, str):
        return []
    return re.findall(r"\([^,]+,\s*([SZ])\)", nudos)


def knot_dir_cord(nudos):
    ds = knot_dirs(nudos)
    if not ds:
        return ""
    s, z = ds.count("S"), ds.count("Z")
    if s and z:
        return "M"  # mixta
    return "S" if s else "Z"


def n_clusters(nudos):
    if not isinstance(nudos, str) or not nudos.strip():
        return 0
    return len([x for x in nudos.split(";") if x.strip()])


def max_long_turns(nudos):
    if not isinstance(nudos, str):
        return 0
    return max([int(x) for x in re.findall(r"(\d+)[LE]", nudos)] or [0])


def load():
    d = pd.read_csv(f"{BASE}/analisis/datos/cuerdas.csv", dtype=str)
    q = pd.read_csv(f"{BASE}/analisis/datos/quipus.csv", dtype=str)
    d["nivel"] = pd.to_numeric(d["nivel"], errors="coerce")
    d["orden"] = pd.to_numeric(d["orden"], errors="coerce")
    d["valor_n"] = pd.to_numeric(d["valor"], errors="coerce")
    d["largo_n"] = pd.to_numeric(d["largo"], errors="coerce")
    d["color_f"] = d["color"].map(color_family)
    d["color_limpio"] = d["color"].map(clean_color)
    d["cromatico"] = d["color"].map(is_chromatic)
    d["kdir"] = d["nudos"].map(knot_dir_cord)
    d["ncl"] = d["nudos"].map(n_clusters)
    d["maxL"] = d["nudos"].map(max_long_turns)
    d["union2"] = d["union"].where(d["union"].isin(["R", "V"]))
    d["torsion2"] = d["torsion"].where(d["torsion"].isin(["S", "Z"]))
    return d, q


# ---------- estadística ----------
def perm_test(stat_fn, labels, n_perm=5000, rng=RNG):
    """Permutación simple de etiquetas; devuelve obs y p bilateral."""
    obs = stat_fn(labels)
    null = np.empty(n_perm)
    lab = np.asarray(labels)
    for i in range(n_perm):
        null[i] = stat_fn(rng.permutation(lab))
    p = (1 + np.sum(np.abs(null) >= abs(obs))) / (n_perm + 1)
    return obs, null, p


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    q = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * p[idx]
        running = max(running, val)
        q[idx] = min(1.0, running)
    # Holm es step-down; para reportar q tipo FDR usar BH
    return q


def bh(pvals):
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    q = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        idx = order[rank]
        val = p[idx] * m / (rank + 1)
        prev = min(prev, val)
        q[idx] = min(1.0, prev)
    return q
