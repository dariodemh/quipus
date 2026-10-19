"""Carga y utilidades para el equipo n_puruchuco_pacha.

Datos: analisis/datos/cuerdas.csv (KFG) + khipu.db (OKR) + puente.csv.
Regla del brief: 0 sin nudos = cuerda ausente.
Todo aqui es solo lectura de datos; nada se escribe fuera de esta carpeta.
"""
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
D = RAIZ / "analisis" / "datos"
DB = RAIZ / "data" / "external" / "open-khipu-repository" / "data" / "khipu.db"
PUENTE = RAIZ / "analisis" / "17_okr_pendientes" / "puente.csv"
SEED = 20261018


# ---------------------------------------------------------------- KFG
def cargar_kfg():
    c = pd.read_csv(D / "cuerdas.csv", low_memory=False, keep_default_na=False)
    q = pd.read_csv(D / "quipus.csv", low_memory=False, keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    c["grupo"] = c["grupo"].astype(int)
    c["nivel"] = c["nivel"].astype(int)
    c["orden"] = c["orden"].astype(int)
    # primeros 3 caracteres del codigo Ascher (sin rangos)
    c["col3"] = c["color"].str.split("(").str[0].str[:6]
    return c, q


# ---------------------------------------------------------------- OKR
def _cord_values(con, kid):
    """valor OKR = suma de knot_value_type por cuerda (TOTAL_VALUE de cluster esta a 0)."""
    d = pd.read_sql(
        "select c.CORD_ID, c.CORD_ORDINAL, c.PENDANT_FROM, c.ATTACHED_TO, c.ATTACHMENT_TYPE,"
        " c.CORD_LEVEL, c.CORD_CLASSIFICATION, c.INVESTIGATOR_CORD_NUM,"
        " coalesce(sum(k.knot_value_type),0) as valor, count(k.KNOT_ID) as nudos"
        " from cord c left join knot k on k.CORD_ID=c.CORD_ID"
        " where c.KHIPU_ID=? group by c.CORD_ID order by c.CORD_ORDINAL",
        con, params=(kid,))
    return d


def cargar_okr(kfg_ids=None):
    """Devuelve (cords, khipus) de OKR. cords: una fila por cuerda con valor."""
    con = sqlite3.connect(DB)
    p = pd.read_csv(PUENTE)
    p = p[p.khipu_id.notna()].copy()
    p["khipu_id"] = p.khipu_id.astype(int)
    mapa = p.drop_duplicates("kfg").set_index("kfg")["khipu_id"].to_dict()
    if kfg_ids is None:
        kfg_ids = list(mapa)
    frames = []
    for k in kfg_ids:
        kid = mapa.get(k)
        if kid is None:
            continue
        d = _cord_values(con, kid)
        if len(d) == 0:
            continue
        d["kfg"] = k
        d["khipu_id"] = kid
        frames.append(d)
    con.close()
    okr = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if len(okr):
        # jerarquia: padre = PENDANT_FROM (cord_id) ; nivel 0/1/2 desde OKR
        okr["padre_id"] = okr.PENDANT_FROM
        okr["nivel_okr"] = okr.CORD_LEVEL.fillna(1).astype(int) - 1
    return okr, mapa


def color_okr(kfg_ids):
    con = sqlite3.connect(DB)
    p = pd.read_csv(PUENTE)
    p = p[p.khipu_id.notna()].copy()
    p["khipu_id"] = p.khipu_id.astype(int)
    mapa = p.drop_duplicates("kfg").set_index("kfg")["khipu_id"].to_dict()
    ids = {mapa[k]: k for k in kfg_ids if k in mapa}
    if not ids:
        con.close()
        return pd.DataFrame()
    q = pd.read_sql(
        "select KHIPU_ID, CORD_ID, FULL_COLOR, PCORD_FLAG from ascher_cord_color",
        con)
    q = q[q.KHIPU_ID.isin(ids)].copy()
    q["kfg"] = q.KHIPU_ID.map(ids)
    con.close()
    return q


# ---------------------------------------------------------------- registros
def registros_kfg(c, k, usar_subs=True, min_cab=0):
    """Lista de registros por grupo KFG.

    Devuelve dict con, por grupo (incluidos los vacios entre min y max):
      x    = valor de la cabecera (primer colgante nivel 0 con valor>0; 0 si no hay)
      vals = valores de todas las cuerdas del grupo (nivel 0 + subsidiarias si usar_subs)
      p    = suma de colgantes nivel 0 (todas, no solo cabecera)
      s    = suma de la primera subsidiaria (nivel 1) de cada colgante
      celdas = [(colgante, s1)] por colgante
      colores, n
    """
    s = c[c.kfg == k].sort_values("orden")
    out = []
    gs = sorted(s.grupo.unique())
    for g in range(min(gs), max(gs) + 1):
        x = s[s.grupo == g]
        if len(x) == 0:
            out.append(dict(grupo=g, vacio=True, x=0, vals=[], p=0, s=0, celdas=[], colores=[], n=0))
            continue
        col = x[x.nivel == 0].sort_values("orden")
        anud = col[col.pres]
        cab = int(anud.valor.iloc[0]) if len(anud) else 0
        if usar_subs:
            vals = [int(v) for v in x[x.pres].valor]
        else:
            vals = [int(v) for v in col[col.pres].valor]
        p = int(col[col.pres].valor.sum())
        s1 = []
        celdas = []
        for _, r in col.iterrows():
            sub = x[(x.nivel == 1) & (x.padre == r.cuerda)]
            sv = int(sub[sub.pres].valor.sum()) if len(sub) else 0
            s1.append(sv)
            celdas.append((int(r.valor) if r.pres else 0, sv))
        out.append(dict(grupo=g, vacio=False, x=cab, vals=vals, p=p,
                        s=int(sum(s1)), celdas=celdas,
                        colores=list(x.col3), n=len(x)))
    return out


def registros_okr(okr, k, usar_subs=True):
    """Registros por grupos definidos por marcadoras M (rule d) o por racimos de
    PENDANT_FROM None. Devuelve bloques separados por cuerdas CORD_CLASSIFICATION='M'."""
    d = okr[okr.kfg == k].sort_values("CORD_ORDINAL")
    if d.empty:
        return []
    # nivel 0 OKR = cuerdas colgantes del cordon principal
    top = d[d.nivel_okr == 0].sort_values("CORD_ORDINAL")
    marca = top[top.CORD_CLASSIFICATION.fillna("") == "M"]
    marcas = set(marca.CORD_ORDINAL)
    bloques, cur = [], []
    for r in top.itertuples():
        if r.CORD_ORDINAL in marcas:
            if cur:
                bloques.append(cur)
            cur = []
        else:
            cur.append(r)
    if cur:
        bloques.append(cur)
    out = []
    for i, b in enumerate(bloques):
        vals = []
        for r in b:
            vals.append(int(r.valor))
            if usar_subs:
                sub = d[d.padre_id == r.CORD_ID]
                vals += [int(v) for v in sub.valor]
        anud = [r for r in b if r.valor > 0]
        out.append(dict(grupo=i, vacio=len(b) == 0, x=int(anud[0].valor) if anud else 0,
                        vals=vals, p=int(sum(r.valor for r in b)), s=0,
                        celdas=[(int(r.valor), int(d[d.padre_id == r.CORD_ID].valor.sum())) for r in b],
                        colores=[], n=len(b)))
    return out


def matriz_registros(regs, campo="p"):
    """Vector por registro (incluye huecos)."""
    return np.array([r[campo] for r in regs], dtype=float)


# ---------------------------------------------------------------- estadistica
def p_emp(obs, nulo, mayor_es_mejor=True):
    nulo = np.asarray(nulo, dtype=float)
    if mayor_es_mejor:
        return (1 + np.sum(nulo >= obs)) / (len(nulo) + 1)
    return (1 + np.sum(nulo <= obs)) / (len(nulo) + 1)


def bh(p):
    from scipy.stats import false_discovery_control
    p = np.asarray(p, dtype=float)
    return false_discovery_control(np.clip(p, 1e-300, 1))


TOL = {0, 1, 10, 100, 1000, 10000}


def coincide(a, b, tol=False):
    d = abs(int(a) - int(b))
    return d in TOL if tol else d == 0


def lcs(x, y, tol=True):
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            if coincide(x[i], y[j], tol):
                H[i + 1, j + 1] = H[i, j] + 1
            else:
                H[i + 1, j + 1] = max(H[i, j + 1], H[i + 1, j])
    return int(H[n, m])
