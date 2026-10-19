"""Carga OKR en el formato de lib18/comun13 y utilidades de registro.

No modifica nada: lee cuerdas_okr.csv (generado por 01_tabla_okr.py) y reutiliza
las funciones congeladas de analisis/18_equipo_rojo/lib18.py y analisis/13_sistema_incahuasi/comun13.py.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "analisis/18_equipo_rojo"))
sys.path.insert(0, str(RAIZ / "analisis/13_sistema_incahuasi"))
import lib18  # noqa: E402
import comun13 as C  # noqa: E402

INC = ([f"JC{i:03d}" for i in range(1, 24)]
       + [f"UR{i}" for i in range(255, 281) if i not in (267, 273, 274)]
       + ["UR267A", "UR267B", "UR273A", "UR273B", "UR274A", "UR274B"])
RES = ["UR266", "UR275", "UR269"]
TOLS = [0, 1, 10, 100, 1000, 10000]
SEED = 4218


def cargar(fuente="okr", inc=True):
    if fuente == "kfg":
        c, _ = lib18.cargar()
        c["orden"] = c.orden.astype(int)
        c["grupo"] = c.grupo.astype(int)
        c["sep"] = c.color.str.startswith("PK")
        c["clas"] = ""
        c["cord_id"] = np.nan
        if inc:
            c = c[c.kfg.isin(INC)].reset_index(drop=True)
        return c
    c = pd.read_csv(AQUI / "cuerdas_okr.csv", keep_default_na=False)
    c["valor"] = pd.to_numeric(c.valor, errors="coerce").fillna(0).round().astype(int)
    c = c[c.orden.astype(str).str.strip() != ""].copy()
    c["pres"] = c.pres.astype(str).str.lower().isin(["true", "1"])
    c["nivel"] = c.nivel.astype(int)
    c["orden"] = c.orden.astype(float).astype(int)
    c["grupo"] = c.grupo.astype(int)
    c["sep"] = c.sep.astype(str).str.lower().isin(["true", "1"])
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    if inc:
        c = c[c.kfg.isin(INC)].reset_index(drop=True)
    return c


def conjunto(c, ks):
    p = c[c.pres & c.kfg.isin(ks)]
    return np.unique(p.valor.to_numpy())


def hallados(v, S, tol=False):
    v = np.asarray(v)
    if tol:
        return np.isin(np.abs(v[:, None] - np.asarray(S)[None, :]), TOLS).any(1)
    return np.isin(v, np.asarray(S))


def registros(c, k, cab="primero"):
    """Igual que lib18.registros: registro = grupo no separador; cabecera = primer colgante anudado.
    Devuelve tambien el indice de grupo para poder alinear por numero de grupo."""
    return lib18.registros(c, k, cab)


def pares(c, qa, qb, cab="primero"):
    A, B = registros(c, qa, cab), registros(c, qb, cab)
    n = min(len(A), len(B))
    ok = (A.x[:n].notna() & B.x[:n].notna()).to_numpy()
    return (A.x[:n].to_numpy()[ok].astype(np.int64),
            B.x[:n].to_numpy()[ok].astype(np.int64),
            A.grupo[:n].to_numpy()[ok], B.grupo[:n].to_numpy()[ok])


def p_emp(nul, obs):
    nul = np.asarray(nul)
    return (np.sum(nul >= obs) + 1) / (len(nul) + 1)


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    h = np.maximum.accumulate((m - np.arange(m)) * p[o])
    out = np.empty(m)
    out[o] = np.minimum(1, h)
    return out
