"""Utilidades del equipo rojo (18). Lee analisis/datos/cuerdas.csv; no modifica nada fuera de esta carpeta.

Definiciones congeladas tal como las escribió 13 (§1 de su informe):
  registro = grupo de colgantes que no es separador rosa (todas las colgantes PK y ninguna anudada);
  cabecera = primer colgante anudado del registro (NaN si ninguno).
Valor 0 sin nudos = ausente.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
SEED = 18
RES = ["UR266", "UR275", "UR269"]


def cargar():
    c = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False, keep_default_na=False)
    q = pd.read_csv(RAIZ / "analisis/datos/quipus.csv", keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    return c, q


def registros(c, k, cab="primero"):
    """DataFrame (grupo, x) con la cabecera de cada registro.
    cab='primero': primer colgante anudado (definición de 13); 'max': mayor colgante del grupo;
    'suma': suma de colgantes anudados."""
    s = c[(c.kfg == k) & (c.nivel == 0)]
    out = []
    for g, x in s.groupby("grupo", sort=True):
        if x.color.str.startswith("PK").all() and not x.pres.any():
            continue
        p0 = x[x.pres]
        if not len(p0):
            v = np.nan
        elif cab == "primero":
            v = p0.valor.iloc[0]
        elif cab == "max":
            v = p0.valor.max()
        else:
            v = p0.valor.sum()
        out.append((g, v))
    return pd.DataFrame(out, columns=["grupo", "x"])


def pares_ab(c, qa, qb, cab="primero", lag=0):
    """Cabeceras alineadas registro a registro (registro i de A con i+lag de B); solo pares con ambas presentes."""
    A, B = registros(c, qa, cab).x.to_numpy(), registros(c, qb, cab).x.to_numpy()
    i = np.arange(len(A))
    j = i + lag
    m = (j >= 0) & (j < len(B))
    a, b = A[i[m]], B[j[m]]
    ok = ~np.isnan(a) & ~np.isnan(b)
    return a[ok].astype(np.int64), b[ok].astype(np.int64)


def diana(c, ks, solo_cab=False):
    """Valores únicos anudados de los quipus ks (todas las cuerdas, como 13; o solo cabeceras)."""
    if solo_cab:
        return np.unique(np.concatenate([registros(c, k).x.dropna().to_numpy() for k in ks]).astype(np.int64))
    p = c[c.pres & c.kfg.isin(ks)]
    return np.unique(p.valor.to_numpy().astype(np.int64))


def esperado_perm(a, b, S):
    """Esperanza exacta del nº de aciertos bajo el nulo 'barajar B' = (1/n) Σ_i Σ_j 1[a_i + b_j ∈ S]."""
    M = np.isin(a[:, None] + b[None, :], S)
    return M.sum() / len(a)


def p_emp(nul, obs):
    nul = np.asarray(nul)
    return (np.sum(nul >= obs) + 1) / (len(nul) + 1)
