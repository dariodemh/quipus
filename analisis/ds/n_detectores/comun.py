"""Base común para los detectores dirigidos (equipo n_detectores).

- Carga cuerdas/quipus/grupos del proyecto (analisis/datos).
- Define REGISTRO = grupo de colgantes que no es separador (PK sin nudos).
  Cabecera = primer colgante anudado (nivel 0, pres) del grupo.
- Tolerancia '±1 dígito' = {0,1,10,100,1000,10000} como en 13_sistema_incahuasi.
- Familias: procedencia (>=3 quipus) y museo (>=3 quipus).
- Pares excluidos: mismo objeto y copias conocidas (14_copias, 04_concordancias).
"""
from pathlib import Path
import itertools
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
D = RAIZ / "analisis" / "datos"
TOL = np.array([0, 1, 10, 100, 1000, 10000], dtype=np.int64)
TOLSET = set(TOL.tolist())
MIN_REC = 3          # quipus con >=3 registros entran en el barrido
SEMILLA = 20261017


def cargar():
    c = pd.read_csv(D / "cuerdas.csv", low_memory=False, keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    c["orden"] = pd.to_numeric(c["orden"], errors="coerce").fillna(0).astype(int)
    c["nivel"] = pd.to_numeric(c["nivel"], errors="coerce").fillna(0).astype(int)
    c["grupo"] = pd.to_numeric(c["grupo"], errors="coerce").fillna(-1).astype(int)
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    q = pd.read_csv(D / "quipus.csv", keep_default_na=False)
    q["procedencia"] = q["procedencia"].replace("", "Unknown")
    q["museo"] = q["museo"].replace("", "Unknown")
    return c, q


def es_separador(x):
    x0 = x[x.nivel == 0]
    return len(x0) > 0 and bool(x0.color.str.startswith("PK").all()) and not bool(x0.pres.any())


def registros(c, k):
    """Lista de registros de un quipu.

    Cada registro: dict(grupo, x=cabecera (0 si no hay), pend=valores nivel 0 en orden,
    rest=valores anudados no cabecera, first=primera cuerda no cabecera).
    """
    s = c[c.kfg == k]
    out = []
    for g, x in s.groupby("grupo", sort=True):
        if es_separador(x):
            continue
        x0 = x[x.nivel == 0]
        if len(x0) == 0:
            continue
        p0 = x0[x0.pres]
        cab = int(p0.valor.iloc[0]) if len(p0) else 0
        pend = [int(v) for v in x0[x0.pres].valor.tolist()]
        resto = x.drop(p0.index[0]) if len(p0) else x
        vals = [int(v) for v in resto[resto.pres].valor.tolist()]
        first = int(resto[resto.pres].valor.iloc[0]) if bool(resto.pres.any()) else None
        out.append(dict(grupo=int(g), x=cab, pend=pend, rest=vals, first=first,
                        ncols=len(pend)))
    return out


def todos_los_registros(c, min_rec=MIN_REC):
    """dict kfg -> lista de registros (solo quipus con >=min_rec registros)."""
    R = {}
    for k in c.kfg.unique():
        r = registros(c, k)
        if len(r) >= min_rec:
            R[k] = r
    return R


def cabeceras(R):
    """dict kfg -> array de cabeceras (>0) en orden de registro."""
    return {k: np.array([r["x"] for r in v if r["x"] > 0], dtype=np.int64)
            for k, v in R.items()}


def familias(q):
    """Devuelve (fproc, fmuseo): dict kfg->nombre de familia y lista de miembros."""
    fp, fm = {}, {}
    for col, f in [("procedencia", fp), ("museo", fm)]:
        vc = q[col].value_counts()
        for fam in vc[vc >= 3].index:
            for k in q.loc[q[col] == fam, "kfg"]:
                f[k] = (col, fam)
    return fp, fm


def _pares_de_archivo():
    """Pares mismo objeto / copia conocida (14_copias + 04_concordancias).

    Excepción deliberada: NO se excluyen los pares internos de Incahuasi, porque son el
    sistema contable que hay que recuperar como control positivo (UR273A+B->UR266/UR275,
    UR278->UR266, etc.). Sí se excluyen las copias entre museos y los mismo-objeto.
    """
    pares = set()
    _q = pd.read_csv(D / "quipus.csv", keep_default_na=False)
    INC = set(_q.loc[_q.procedencia == "Incahuasi", "kfg"].astype(str))

    def add(a, b):
        a, b = str(a), str(b)
        if a in INC and b in INC:
            # pares internos de Incahuasi: son el sistema contable y los controles
            return
        pares.add(frozenset((a, b)))

    p = RAIZ / "analisis" / "14_copias" / "pares_resumen.csv"
    if p.exists():
        d = pd.read_csv(p)
        for a, b in zip(d.A, d.B):
            add(a, b)
    v = RAIZ / "analisis" / "14_copias" / "verificacion_pares.csv"
    if v.exists():
        d = pd.read_csv(v)
        for a, b in zip(d.A, d.B):
            add(a, b)
    for f in (RAIZ / "analisis" / "04_concordancias" / "resultados").glob("archivo_*_aristas.csv"):
        d = pd.read_csv(f)
        if len(d) == 0:
            continue
        for a, b in zip(d.origen, d.destino):
            add(a, b)
    return pares


EXCLUIDOS = _pares_de_archivo()


def excluido(a, b):
    return frozenset((a, b)) in EXCLUIDOS


def bh(p):
    from scipy.stats import false_discovery_control
    p = np.asarray(p, dtype=float)
    out = np.ones_like(p)
    ok = np.isfinite(p)
    if ok.any():
        out[ok] = false_discovery_control(p[ok])
    return out


def p_emp(obs, nul):
    nul = np.asarray(nul)
    return (np.sum(nul >= obs) + 1) / (len(nul) + 1)


def parejas(R, min_rec=MIN_REC):
    ks = sorted([k for k in R if len(R[k]) >= min_rec])
    return list(itertools.combinations(ks, 2))
