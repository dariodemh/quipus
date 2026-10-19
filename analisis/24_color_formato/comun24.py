"""Utilidades comunes de 24_color_formato. Solo lectura de datos."""
import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
DAT = RAIZ / "analisis" / "datos"
DB_URI = "file:" + (RAIZ / "data/external/open-khipu-repository/data/khipu.db").as_posix() + "?mode=ro"
SEED = 20261018


def norm(s):
    if not isinstance(s, str):
        return ""
    return re.sub(r"\([^)]*\)", "", s).strip()


def base(s):
    return re.split(r"[:\-/*%]", s)[0].strip() if s else ""


def compuesto(s):
    return bool(re.search(r"[:\-/]", s or ""))


def registrador(k):
    p = k[:2].upper()
    if p == "UR":
        n = int(re.sub(r"\D", "", k[2:6]) or 0)
        return "AS" if n >= 1000 else "UR"
    return p


def cargar():
    c = pd.read_csv(DAT / "cuerdas.csv", low_memory=False, keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    for k in ("grupo", "nivel", "orden"):
        c[k] = pd.to_numeric(c[k], errors="coerce").fillna(-1).astype(int)
    c["col"] = c["color"].map(norm)
    c["base"] = c["col"].map(base)
    c["comp"] = c["col"].map(compuesto)
    c["ausente"] = (c["valor"] == 0) & (c["nudos"] == "")
    c["pres"] = ~c["ausente"]
    c["reg"] = c["kfg"].map(registrador)
    return c


def okr():
    return sqlite3.connect(DB_URI, uri=True)


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    if n == 0:
        return p
    o = np.argsort(p)
    r = p[o] * n / np.arange(1, n + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    q = np.empty(n)
    q[o] = np.minimum(r, 1)
    return q


def holm(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.maximum.accumulate((n - np.arange(n)) * p[o])
    out = np.empty(n)
    out[o] = np.minimum(adj, 1)
    return out


def p_emp(obs, nulo):
    nulo = np.asarray(nulo)
    return (1 + np.sum(nulo >= obs)) / (1 + len(nulo))


def nmi(a, b):
    from sklearn.metrics import normalized_mutual_info_score
    return normalized_mutual_info_score(a, b)


if __name__ == "__main__":
    assert norm("W(0.0-12.5):MB(12.5-30)") == "W:MB"
    assert base("B:BB") == "B" and compuesto("W-MB") and not compuesto("AB")
    assert registrador("UR1140") == "AS" and registrador("UR053A") == "UR"
    assert np.allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
    assert np.allclose(bh([0.01, 0.04, 0.03]), [0.03, 0.04, 0.04])
    print("ok")
