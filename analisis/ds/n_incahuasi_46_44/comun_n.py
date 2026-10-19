"""Carga y utilidades comunes para n_incahuasi_46_44.

No modifica nada fuera de esta carpeta. Reutiliza el cargador de 09_incahuasi/comun.py
(solo lectura). Convenciones del brief: valor 0 sin nudos = cuerda ausente.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "analisis" / "09_incahuasi"))
from comun import cargar  # noqa: E402

ARCHIVO = ([f"JC{i:03d}" for i in range(1, 24)]
           + [f"UR{i}" for i in range(255, 281) if i not in (267, 273, 274)]
           + ["UR267A", "UR267B", "UR273A", "UR273B", "UR274A", "UR274B"])


def cargar_todo():
    c, q = cargar()
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    return c, q


def registros(s):
    """Registros de un quipu con la definición del equipo 13 (03_constantes.py).

    Registro = grupo con cabecera (primer colgante presente, nivel 0, x>=100)
    y >=1 cuerda anudada más. Devuelve lista de dicts en orden de grupo.
    """
    R = []
    for g, x in s[s.pres].groupby("grupo", sort=True):
        p0 = x[x.nivel == 0]
        if len(p0) == 0 or len(x) < 2:
            continue
        xv = int(p0.valor.iloc[0])
        if xv < 100:
            continue
        R.append(dict(grupo=int(g), cab=xv,
                      vals=[int(v) for v in x.valor],
                      resto=[int(v) for v, cu in zip(x.valor, x.cuerda)
                             if cu != p0.cuerda.iloc[0]]))
    return R


def registros_lax(s):
    """Definición laxa: grupo con una cabecera presente de nivel 0 y valor >=100.

    No exige que el grupo tenga más cuerdas. Recupera quipus fragmentarios que la
    definición estricta descarta (p. ej. UR273A pasa de 1 a 21 registros), lo que
    importa para no dejar fuera posibles componentes.
    """
    out = []
    for g, x in s[s.pres].groupby("grupo", sort=True):
        p0 = x[(x.nivel == 0) & x.pres]
        if len(p0) and int(p0.valor.iloc[0]) >= 100:
            out.append(int(p0.valor.iloc[0]))
    return np.array(out, dtype=int)


def bh(p):
    from scipy.stats import false_discovery_control
    p = np.asarray(p, dtype=float)
    out = np.full(len(p), np.nan)
    m = np.isfinite(p)
    if m.any():
        out[m] = false_discovery_control(p[m])
    return out


def holm(p):
    p = np.asarray(p, dtype=float)
    out = np.full(len(p), np.nan)
    idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0:
        return out
    o = idx[np.argsort(p[idx])]
    m = len(o)
    run = 0.0
    for i, j in enumerate(o):
        run = max(run, (m - i) * p[j])
        out[j] = min(1.0, run)
    return out


# ---------------------------------------------------------------- UR269
def registros_ur269(u):
    """Registros de UR269 definidos sobre las cuerdas de nivel 0 en orden.

    Un bloque empieza/termina en una cuerda rosa (PK) sin nudos. Dentro del bloque,
    un registro empieza en la primera cuerda de nivel 0 presente con valor >= 100;
    las cuerdas menores (cuotas, netos parciales) se agregan al registro abierto.
    Esto repara el caso en que la digitalización partió un registro en dos grupos
    (p. ej. g56 = 2468, 2422 y g57 = 46).
    """
    u = u.sort_values("orden")
    bloques, act = [], None
    for g, x in u.groupby("grupo", sort=True):
        x0 = x[x.nivel == 0]
        if len(x0) and x.color.str.startswith("PK").all() and not x.pres.any():
            act = None
            continue
        if not x.pres.any():
            continue
        heads = x0[(x0.nivel == 0) & x0.pres & (x0.valor >= 100)]
        if len(heads):
            if act is None:
                act = dict(bloque=len(bloques), filas=[])
                bloques.append(act)
            h = heads.iloc[0]
            act["filas"].append(dict(grupo=int(g), cab=int(h.valor), vals=[]))
        if act is None:
            continue
        act["filas"][-1]["vals"].extend(int(v) for v in x0.valor)
    # numerar filas y anotar cuota explícita (valor 15..60 en el registro)
    filas = []
    for b in bloques:
        for i, f in enumerate(b["filas"], start=1):
            cu = [v for v in f["vals"][1:] if 15 <= v <= 60]
            filas.append(dict(bloque=b["bloque"], fila=i, tam=len(b["filas"]),
                              grupo=f["grupo"], cab=f["cab"], vals=f["vals"],
                              cuota=cu[0] if cu else np.nan))
    return pd.DataFrame(filas), bloques
