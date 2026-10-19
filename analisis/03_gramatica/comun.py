"""Utilidades comunes del equipo 03_gramatica: carga, tokens, teoría de la información, referencias.

Uso: importar desde los scripts t1..t5. `python comun.py` corre las autocomprobaciones.
"""
import math
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "analisis" / "datos"
AQUI = Path(__file__).resolve().parent
RES = AQUI / "resultados"
RES.mkdir(exist_ok=True)
SEMILLA = 20261017

# ---------------------------------------------------------------- nudos
_CL = re.compile(r"^(\d+)([A-Za-z]+)\(([^,]*),([^)]*)\)(?:,(.*))?$")


def parse_nudos(s):
    """'3S(7.5,U),30;9L(9.0,U),9' -> [(n, tipo, pos_cm, dir, aporte), ...] arriba->abajo."""
    out = []
    if not isinstance(s, str) or not s:
        return out
    for cl in s.split(";"):
        m = _CL.match(cl.strip())
        if not m:
            continue
        n, t, pos, d, v = m.groups()
        try:
            pos = float(pos)
        except ValueError:
            pos = np.nan
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = np.nan
        out.append((int(n), t.upper(), pos, d.strip().upper(), v))
    return out


def lugar(n, v):
    """Lugar decimal de un racimo a partir de su aporte (10^lugar); None si no se puede."""
    if n and v and v > 0:
        return int(round(math.log10(v / n)))
    return None


def patron(cls):
    """Patrón de nudos sin dígitos: tipos + lugar decimal, p. ej. 'S2.S1.L0'; '-' si no hay nudos."""
    if not cls:
        return "-"
    partes = []
    for n, t, pos, d, v in cls:
        p = lugar(n, v)
        partes.append(f"{t}{'?' if p is None else p}")
    return ".".join(partes)


def anomalia_decimal(cls):
    """Cuerda no conforme con la notación decimal de Locke (criterio tipo 'STRING' de Sivan, más estricto).
    True si: >1 racimo de tipo largo/ocho, o un largo/ocho no es el último racimo, o lugares no
    estrictamente decrecientes hacia abajo, o dos racimos con el mismo lugar."""
    if not cls:
        return False
    tipos = [t for _, t, _, _, _ in cls]
    lar = [i for i, t in enumerate(tipos) if t in ("L", "E", "EE", "LL")]
    if len(lar) > 1 or (lar and lar[-1] != len(tipos) - 1):
        return True
    lugares = [lugar(n, v) for n, _, _, _, v in cls]
    lugares = [x for x in lugares if x is not None]
    return any(a <= b for a, b in zip(lugares, lugares[1:]))


def norm_color(c):
    if not isinstance(c, str) or not c.strip():
        return "?"
    return re.sub(r"\([^)]*\)", "", c).strip()


def cargar():
    """Cuerdas con columnas derivadas. Devuelve (cuerdas, quipus)."""
    c = pd.read_csv(DATOS / "cuerdas.csv", low_memory=False)
    q = pd.read_csv(DATOS / "quipus.csv")
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    cls = c["nudos"].map(parse_nudos)
    c["n_racimos"] = cls.map(len)
    c["anudada"] = c["n_racimos"] > 0
    c["tok_color"] = c["color"].map(norm_color)
    c["tok_patron"] = cls.map(patron)
    c["tok_tipos"] = cls.map(lambda x: "".join(t for _, t, _, _, _ in x) or "-")
    c["union_n"] = c["union"].replace({"Unknown": "U", "?": "U"}).fillna("U")
    c["torsion"] = c["torsion"].fillna("U")
    c["tok_full"] = c["tok_color"] + "|" + c["tok_patron"] + "|" + c["union_n"] + "|" + c["torsion"]
    c["tok_colpat"] = c["tok_color"] + "|" + c["tok_patron"]
    # magnitud: nº de dígitos del valor (0 = sin nudos)
    c["magn"] = np.where(c["anudada"] & (c["valor"] > 0),
                         np.floor(np.log10(c["valor"].clip(lower=1))) + 1, 0).astype(int)
    c["anom_dec"] = cls.map(anomalia_decimal)
    dirs = cls.map(lambda x: [d for _, _, _, d, _ in x if d in ("S", "Z")])
    c["n_dirS"] = dirs.map(lambda x: x.count("S"))
    c["n_dirZ"] = dirs.map(lambda x: x.count("Z"))
    c["rota"] = c["terminacion"].eq("B")
    q["sitio"] = [sitio(p) or sitio(r) for p, r in zip(q["procedencia"], q["region"])]
    return c, q


_SITIOS = [("pachac", "Pachacamac"), ("incahuasi", "Incahuasi"), ("leymebamba", "Leymebamba"),
           ("huaquerones", "Huaquerones"), ("armatambo", "Armatambo"), ("puruchuco", "Puruchuco"),
           ("nazca", "Nazca"), ("atarco", "Nazca"), ("acari", "Nazca"), ("ica", "Ica"), ("ocucaje", "Ica"),
           ("ullujal", "Ica"), ("ullujay", "Ica"), ("callango", "Ica"), ("playa miller", "N. Chile"), ("pisco", "Ica"), ("paracas", "Ica"),
           ("puntilla", "Ica"), ("santa", "Santa"), ("arica", "N. Chile"), ("lluta", "N. Chile"),
           ("quillagua", "N. Chile"), ("chancay", "Chancay"), ("huando", "Chancay"), ("huacho", "Huacho"),
           ("huaura", "Huacho"), ("lima", "Lima"), ("cajamarquilla", "Lima"), ("maranga", "Lima"),
           ("rimac", "Lima"), ("lurin", "Lima"), ("chuquitanta", "Lima"), ("molina", "Lima"),
           ("tambo colorado", "Ica")]


def sitio(p):
    """Procedencia arqueológica gruesa (no museo). None si desconocida o es un nombre de colección."""
    if not isinstance(p, str):
        return None
    s = p.lower()
    if "unknown" in s or "gaffron" in s or "aankoop" in s or "donation" in s or "dr " in s:
        return None
    for k, v in _SITIOS:
        if k in s:
            return v
    return None


def secuencias(c, col, min_len=10, nivel0=True):
    """{kfg: (tokens np.array[str], grupos np.array[int])} de colgantes en orden."""
    d = c[c["nivel"] == 0] if nivel0 else c
    out = {}
    for k, g in d.groupby("kfg", sort=True):
        if len(g) >= min_len:
            out[k] = (g[col].to_numpy(), g["grupo"].to_numpy())
    return out


# ------------------------------------------------------- teoría de la información
def codificar(seq):
    _, inv = np.unique(np.asarray(seq), return_inverse=True)
    return inv.astype(np.int64)


def entropia_conteos(cnt, axis=-1):
    cnt = np.asarray(cnt, dtype=float)
    tot = cnt.sum(axis=axis, keepdims=True)
    p = np.divide(cnt, tot, out=np.zeros_like(cnt), where=tot > 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -np.where(p > 0, p * np.log2(p), 0.0).sum(axis=axis)
    return h


def entropia(x):
    return float(entropia_conteos(np.bincount(codificar(x))))


def _hgram(x, k, V):
    """Entropía de k-gramas solapados (plug-in) de una secuencia entera codificada."""
    n = len(x) - k + 1
    if n <= 0:
        return 0.0
    code = np.zeros(n, dtype=np.int64)
    for j in range(k):
        code = code * V + x[j:j + n]
    _, cnt = np.unique(code, return_counts=True)
    return float(entropia_conteos(cnt))


def h_cond(x, k, V=None):
    """H(X_t | X_{t-k..t-1}) = H(k+1-gramas) - H(k-gramas). k=0 -> entropía unigrama."""
    x = np.asarray(x, dtype=np.int64)
    V = V or int(x.max()) + 1
    if k == 0:
        return _hgram(x, 1, V)
    return _hgram(x, k + 1, V) - _hgram(x, k, V)


def mi_lags(X, lags, V):
    """Información mutua plug-in I(X_t; X_{t+d}) para cada fila de X (P x n) y cada d. -> (P, len(lags))."""
    X = np.atleast_2d(X)
    P, n = X.shape
    out = np.zeros((P, len(lags)))
    off = (np.arange(P) * V * V)[:, None]
    for j, d in enumerate(lags):
        if d >= n - 1:
            out[:, j] = np.nan
            continue
        a, b = X[:, :-d], X[:, d:]
        cnt = np.bincount((off + a * V + b).ravel(), minlength=P * V * V).reshape(P, V, V).astype(float)
        hj = entropia_conteos(cnt.reshape(P, -1))
        ha = entropia_conteos(cnt.sum(2))
        hb = entropia_conteos(cnt.sum(1))
        out[:, j] = ha + hb - hj
    return out


def mi_etiqueta(tok, lab, Vt, Vl):
    """I(tok; lab) para filas de tok (P x n) con etiquetas fijas lab (n,). -> (P,)"""
    tok = np.atleast_2d(tok)
    P, n = tok.shape
    off = (np.arange(P) * Vt * Vl)[:, None]
    cnt = np.bincount((off + tok * Vl + lab[None, :]).ravel(), minlength=P * Vt * Vl).reshape(P, Vt, Vl)
    cnt = cnt.astype(float)
    return entropia_conteos(cnt.sum(2)) + entropia_conteos(cnt.sum(1)) - entropia_conteos(cnt.reshape(P, -1))


def barajar(x, P, rng):
    """P permutaciones independientes de x (P x n)."""
    return rng.permuted(np.tile(x, (P, 1)), axis=1)


def barajar_grupos(x, grupos, P, rng):
    """Permuta el orden de los grupos conservando el orden interno de cada grupo."""
    cortes = np.flatnonzero(np.diff(grupos)) + 1
    bloques = np.split(np.asarray(x), cortes)
    out = np.empty((P, len(x)), dtype=np.asarray(x).dtype)
    for i in range(P):
        out[i] = np.concatenate([bloques[j] for j in rng.permutation(len(bloques))])
    return out


def zipf_exponente(seq, min_rank=1, max_rank=None):
    """Pendiente -log f vs log r (MCO) sobre la curva rango-frecuencia."""
    _, cnt = np.unique(np.asarray(seq), return_counts=True)
    f = np.sort(cnt)[::-1].astype(float)
    r = np.arange(1, len(f) + 1)
    sel = (r >= min_rank) & (f > 0)
    if max_rank:
        sel &= r <= max_rank
    if sel.sum() < 3:
        return np.nan
    return float(-np.polyfit(np.log(r[sel]), np.log(f[sel]), 1)[0])


def heaps(seq):
    """Curva de vocabulario V(n) y exponente beta de V ~ n^beta (ajuste log-log)."""
    vistos, v = set(), []
    for t in seq:
        vistos.add(t)
        v.append(len(vistos))
    v = np.array(v, dtype=float)
    n = np.arange(1, len(v) + 1)
    beta = float(np.polyfit(np.log(n), np.log(v), 1)[0]) if len(v) >= 5 else np.nan
    return v, beta


def bh(p):
    """Benjamini-Hochberg: q-valores."""
    p = np.asarray(p, dtype=float)
    q = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    pv = p[ok]
    m = len(pv)
    if m == 0:
        return q
    o = np.argsort(pv)
    r = pv[o] * m / np.arange(1, m + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    qq = np.empty(m)
    qq[o] = np.minimum(r, 1)
    q[ok] = qq
    return q


def holm(p):
    p = np.asarray(p, dtype=float)
    m = len(p)
    o = np.argsort(p)
    adj = np.maximum.accumulate((m - np.arange(m)) * p[o])
    out = np.empty(m)
    out[o] = np.minimum(adj, 1)
    return out


# ------------------------------------------------------------- referencias de texto
_DIGQ = ["chh", "ch'", "ch", "ll", "qh", "q'", "kh", "k'", "ph", "p'", "th", "t'", "sh"]
_VOC = set("aeiouáéíóú")


def _fonemas(palabra, digrafos):
    i, out = 0, []
    while i < len(palabra):
        for d in digrafos:
            if palabra.startswith(d, i):
                out.append(d)
                i += len(d)
                break
        else:
            out.append(palabra[i])
            i += 1
    return out


_ATAQUES_ES = {"pr", "br", "tr", "dr", "cr", "gr", "fr", "pl", "bl", "cl", "gl", "fl"}


def silabear(palabra, lengua="qu"):
    """Silabeo aproximado por reglas (C)(C)V(V)(C). Suficiente como referencia estadística."""
    dig = _DIGQ if lengua == "qu" else ["ch", "ll", "rr", "qu", "gu"]
    f = _fonemas(palabra, dig)
    es_v = [x in _VOC or (lengua == "es" and x == "y" and (i == len(f) - 1)) for i, x in enumerate(f)]
    # núcleos: secuencias de vocales (en español i/u átonas forman diptongo; simplificamos: toda secuencia
    # de vocales = un núcleo salvo dos vocales fuertes a/e/o seguidas, que forman hiato)
    nucleos, i = [], 0
    while i < len(f):
        if es_v[i]:
            j = i + 1
            while j < len(f) and es_v[j] and not (f[j - 1] in "aeo" and f[j] in "aeo") and lengua == "es":
                j += 1
            nucleos.append((i, j))
            i = j
        else:
            i += 1
    if not nucleos:
        return ["".join(f)]
    cortes = []
    for (a1, b1), (a2, b2) in zip(nucleos, nucleos[1:]):
        cons = f[b1:a2]
        if len(cons) <= 1:
            cortes.append(b1)
        elif lengua == "es" and "".join(cons[-2:]) in _ATAQUES_ES:
            cortes.append(a2 - 2)
        else:
            cortes.append(a2 - 1)
    sil, ini = [], 0
    for ct in cortes:
        sil.append("".join(f[ini:ct]))
        ini = ct
    sil.append("".join(f[ini:]))
    return [s for s in sil if s]


def texto_referencia(nombre, nivel="silaba"):
    """Devuelve (tokens, grupos=palabra) del texto de referencia (DUDH en ref/)."""
    lengua = "es" if nombre == "Spanish" else "qu"
    t = (AQUI / "ref" / f"udhr_{nombre}.txt").read_text(encoding="utf-8").lower()
    t = unicodedata.normalize("NFC", t)
    palabras = re.findall(r"[a-zñáéíóúü']+", t)
    palabras = [p.strip("'") for p in palabras if p.strip("'")]
    toks, grp = [], []
    for i, p in enumerate(palabras):
        unid = silabear(p, lengua) if nivel == "silaba" else list(p)
        toks += unid
        grp += [i] * len(unid)
    return np.array(toks), np.array(grp)


def tabla_sintetica(n, frec, k, fidelidad, rng):
    """Tabla con k columnas periódicas: cada columna tiene un token 'propio' (muestreado de frec) que
    aparece con prob. 'fidelidad'; si no, token al azar según frec. Devuelve (tokens int, grupos=fila)."""
    V = len(frec)
    p = frec / frec.sum()
    propio = rng.choice(V, size=k, p=p)
    col = np.arange(n) % k
    azar = rng.choice(V, size=n, p=p)
    tok = np.where(rng.random(n) < fidelidad, propio[col], azar)
    return tok.astype(np.int64), np.arange(n) // k


if __name__ == "__main__":
    # autocomprobaciones mínimas
    cl = parse_nudos("3S(7.5,U),30;9L(9.0,Z),9")
    assert cl == [(3, "S", 7.5, "U", 30.0), (9, "L", 9.0, "Z", 9.0)], cl
    assert patron(cl) == "S1.L0"
    assert not anomalia_decimal(cl)
    assert anomalia_decimal(parse_nudos("3L(7.5,U),3;9L(9.0,Z),9"))
    assert anomalia_decimal(parse_nudos("2S(5,U),20;3S(9,U),30"))
    assert norm_color("MB(0.0-7.0)/W(7.0-35.0)") == "MB/W"
    assert silabear("runakuna") == ["ru", "na", "ku", "na"], silabear("runakuna")
    assert silabear("qhelqesqa") == ["qhel", "qes", "qa"], silabear("qhelqesqa")
    assert silabear("hombre", "es") == ["hom", "bre"]
    x = np.array([0, 1, 2] * 30)
    assert abs(h_cond(x, 1)) < 0.01 and abs(entropia(x) - math.log2(3)) < 1e-9
    m = mi_lags(x[None, :], [1, 3], 3)[0]
    assert abs(m[0] - math.log2(3)) < 0.01 and abs(m[1] - math.log2(3)) < 0.01
    assert np.allclose(bh([0.01, 0.04, 0.03]), [0.03, 0.04, 0.04])
    rng = np.random.default_rng(0)
    bg = barajar_grupos(np.arange(6), np.array([0, 0, 1, 1, 2, 2]), 3, rng)
    assert all(sorted(r.tolist()) == list(range(6)) for r in bg)
    print("ok")
