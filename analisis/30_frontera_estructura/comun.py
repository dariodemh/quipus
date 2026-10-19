"""Datos, frontera, division A/B, companeros y utilidades comunes (ver diseno.md)."""
import re, time
import numpy as np, pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
SEMILLA = 20261018

C = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv")
C["valor"] = C["valor"].fillna(0).astype(np.int64)
C["col"] = C["color"].fillna("?").astype(str).map(lambda s: re.sub(r"\([^)]*\)", "", s).strip())
Q = pd.read_csv(RAIZ / "analisis/datos/quipus.csv").set_index("kfg")
ATLAS = pd.read_csv(RAIZ / "analisis/28_atlas_generos/atlas.csv").set_index("kfg")
FRONTERA = sorted(ATLAS.index[(ATLAS.genero == "SIN") & ATLAS.evidencia.str.startswith("decimal sin estructura")])
assert len(FRONTERA) == 180

MISMO_OBJETO = {frozenset(p) for p in [("UR1107", "UR237"), ("AS125", "UR247"), ("KH0033", "UR044")]}


def division():
    rng = np.random.default_rng(SEMILLA)
    mitad = {}
    for est in ["UR", "AS", "otro"]:
        ks = [k for k in FRONTERA if (k[:2] if k[:2] in ("UR", "AS") else "otro") == est]
        ks = list(rng.permutation(ks))
        h = len(ks) // 2
        for k in ks[:h]: mitad[k] = "A"
        for k in ks[h:]: mitad[k] = "B"
    return mitad


def museo_norm(m):
    s = str(m).lower()
    for clave, pats in [("BERLIN", ["berlin"]), ("INCAHUASI", ["incah", "inahuasi"]),
                        ("BCR", ["banco central"]), ("SOLDI", ["soldi"]), ("HAMBURG", ["hamburg"]),
                        ("PARIS", ["quai branly", "musee de l homme"]),
                        ("HANNOVER", ["landesmuseum hannover", "hanover, west germany"]),
                        ("ICA", ["museo regional de ica", "museo de ica", "loan to ica"]),
                        ("MNAAHP", ["arqueolog", "pueblo libre", "museo nacional, lima", "museo nacion de"])]:
        if any(p in s for p in pats):
            return clave
    return s.strip()


DESCONOCIDO = {"unknown", "peru", "south peru", "aankoop", "", "nan"}
MUSEO = {k: museo_norm(Q.loc[k, "museo"]) for k in Q.index}
SITIO = {k: (None if str(Q.loc[k, "procedencia"]).strip().lower() in DESCONOCIDO else str(Q.loc[k, "procedencia"]).strip().lower()) for k in Q.index}


class Quipu:
    def __init__(self, k):
        d = C[C.kfg == k].sort_values("orden")
        p = d[d.nivel == 0]
        self.k = k
        self.v = p.valor.to_numpy(np.int64)
        self.g = p.grupo.to_numpy()
        self.col = p.col.to_numpy()
        self.todos = d.valor.to_numpy(np.int64)  # todas las cuerdas, cualquier nivel
        idx = dict(zip(p.cuerda, range(len(p))))
        s = d[(d.nivel == 1) & d.padre.isin(idx)]
        self.sub_padre = np.array([idx[x] for x in s.padre], dtype=int)
        self.sub_v = s.valor.to_numpy(np.int64)


_CACHE = {}
def quipu(k):
    if k not in _CACHE: _CACHE[k] = Quipu(k)
    return _CACHE[k]


def companeros(k, tipo):
    """tipo 'amplio' (I1-I7) o 'sitio' (I8-I9)."""
    if tipo == "amplio":
        s = set(FRONTERA) | {x for x in Q.index if MUSEO[x] == MUSEO[k]}
        if SITIO[k]: s |= {x for x in Q.index if SITIO[x] == SITIO[k]}
    else:
        s = {x for x in Q.index if SITIO[x] == SITIO[k]} if SITIO[k] else {x for x in Q.index if MUSEO[x] == MUSEO[k]}
    s.discard(k)
    return sorted(x for x in s if frozenset((k, x)) not in MISMO_OBJETO and x in set(C.kfg))


def tol(a, b):
    """a == b o difieren en exactamente una cifra por una unidad (sin acarreo). Vectorizado."""
    a = np.asarray(a, np.int64); b = np.asarray(b, np.int64)
    lo = np.minimum(a, b); d = np.abs(a - b)
    out = d == 0
    p = 1
    for _ in range(8):
        out |= (d == p) & ((lo // p) % 10 != 9) & (lo >= 0) & (p <= 10 * np.maximum(lo, 1))
        p *= 10
    return out


def variantes(v):
    """valores w con tol(v, w)."""
    out = {v}; p = 1
    for _ in range(8):
        if (v // p) % 10 != 9 and p <= 10 * max(v, 1): out.add(v + p)
        if v - p >= 0 and ((v - p) // p) % 10 != 9 and p <= 10 * max(v - p, 1): out.add(v - p)
        p *= 10
    return out


def pesos(v):
    nz = v[v > 0]
    if len(nz) == 0: return np.zeros(len(v))
    vals, cnt = np.unique(nz, return_counts=True)
    f = dict(zip(vals, cnt / len(nz)))
    return np.array([-np.log(f[x]) if x > 0 else 0.0 for x in v])


def p_escalada(obs, nulo_fn, etapas, b_max, presupuesto_s=120.0):
    """nulo_fn(N, rng) -> array de N estadisticos nulos. Escalada Besag-Clifford.
    Devuelve p, N, b. obs None -> NA."""
    if obs is None or (isinstance(obs, float) and np.isnan(obs)): return np.nan, 0, 0
    rng = np.random.default_rng(SEMILLA)
    N = b = 0; t0 = time.time()
    for i, n_et in enumerate(etapas):
        falta = n_et - N
        t1 = time.time()
        z = nulo_fn(falta, rng)
        b += int(np.sum(z >= obs - 1e-12)); N = n_et
        dt = time.time() - t1
        if b > b_max or i + 1 == len(etapas): break
        if dt / falta * (etapas[i + 1] - N) > presupuesto_s: break
    return (b + 1) / (N + 1), N, b


def bh(p):
    p = np.asarray(p, float); q = np.full_like(p, np.nan); m = ~np.isnan(p)
    if m.sum() == 0: return q
    x = p[m]; n = len(x); o = np.argsort(x)
    r = x[o] * n / np.arange(1, n + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    y = np.empty(n); y[o] = np.minimum(r, 1); q[m] = y
    return q


def holm(p):
    p = np.asarray(p, float); h = np.full_like(p, np.nan); m = ~np.isnan(p)
    x = p[m]; n = len(x); o = np.argsort(x)
    r = np.maximum.accumulate(x[o] * (n - np.arange(n)))
    y = np.empty(n); y[o] = np.minimum(r, 1); h[m] = y
    return h


if __name__ == "__main__":
    assert tol(19, 29) and tol(5, 4) and not tol(95, 105) and not tol(19, 20) and tol(100, 100)
    assert variantes(19) == {19, 18, 29, 9, 119}
    assert all(tol(19, w) for w in variantes(19)) and all(variantes(w).__contains__(19) for w in variantes(19))
    assert all((w in variantes(v)) == bool(tol(v, w)) for v in range(0, 300) for w in range(0, 1300))
    assert np.allclose(bh([0.01, 0.04, 0.03]), [0.03, 0.04, 0.04])
    m = division(); print(pd.Series(m).value_counts().to_dict())
    print("companeros UR1107:", len(companeros("UR1107", "amplio")), len(companeros("UR1107", "sitio")))
    print("museos frontera:", pd.Series([MUSEO[k] for k in FRONTERA]).value_counts().head(8).to_dict())
