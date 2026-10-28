# -*- coding: utf-8 -*-
"""Detectores del lector. Cada uno empaqueta un método ya validado del proyecto (la ruta de origen
va en el comentario de cada función y en la `fuente` de cada afirmación). No hay métodos nuevos.

Contrato: detector(d, ctx) -> dict(titulo, datos, afirmaciones=[dict(texto, nivel, fuente)]).
  d   = cuerdas de UN quipu (esquema de analisis/datos/cuerdas.csv, ya pasado por `preparar`).
  ctx = Contexto (corpus KFG, tablas publicadas del repo, OKR en solo lectura).
Niveles: dato (descripción de la transcripción), bien apoyado, apoyado, propuesto (los de analisis/SINTESIS.md).
"""
import importlib.util
import math
import os
import re
import sqlite3
from functools import cached_property
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

RAIZ = Path(__file__).resolve().parents[1]
AN = RAIZ / "analisis"
DB = "file:" + (RAIZ / "data/external/open-khipu-repository/data/khipu.db").as_posix() + "?mode=ro"
os.environ.setdefault("NUMBA_CACHE_DIR", str(Path(__file__).resolve().parent / "__pycache__"))
SEED = 20261018

# Punto de enganche: funciones detector(d, ctx) -> dict con el mismo contrato. Se ejecutan al final de cada
# ficha. Pensado para los detectores de analisis/30_frontera_estructura/ cuando estén cerrados.
DETECTORES_EXTRA = []


def _modulo(nombre, ruta):
    """Importa un script del repo por ruta (sin tocarlo)."""
    import sys
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m  # la caché de numba necesita el módulo registrado
    spec.loader.exec_module(m)
    return m


def af(texto, nivel, fuente):
    return dict(texto=texto, nivel=nivel, fuente=fuente)


def norm_color(s):
    # regla del proyecto (brief): quitar los rangos en cm "W(0.0-12.5)" -> "W"
    return re.sub(r"\([^)]*\)", "", s).strip()


def preparar(c):
    """Tipos y columnas derivadas comunes. Valor 0 sin nudos = cuerda ausente (convención de 01/08/13)."""
    c = c.copy()
    for k in ("cuerda", "padre", "nudos", "color", "torsion", "union", "terminacion", "kfg"):
        c[k] = c[k].fillna("").astype(str) if k in c else ""
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype("int64")
    for k in ("orden", "nivel", "grupo"):
        c[k] = pd.to_numeric(c[k], errors="coerce").fillna(0).astype("int64")
    c["anudada"] = c.nudos.str.strip() != ""
    c["pres"] = c.anudada | (c.valor > 0)
    c["colorn"] = c.color.map(norm_color)
    return c.sort_values(["kfg", "orden"], kind="stable").reset_index(drop=True)


def bh(p):
    p = np.asarray(p, float)
    if len(p) == 0:
        return p
    o = np.argsort(p)
    r = np.minimum.accumulate((p[o] * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1]
    out = np.empty(len(p))
    out[o] = np.minimum(r, 1)
    return out


def p_emp(obs, nulo):
    return (1 + np.sum(np.asarray(nulo) >= obs - 1e-12)) / (1 + len(nulo))


# --------------------------------------------------------------------------- contexto
class Contexto:
    """Corpus y tablas publicadas; todo perezoso para que una ficha suelta cargue solo lo que usa."""

    def __init__(self):
        self.rng = np.random.default_rng(SEED)

    @cached_property
    def C(self):
        return preparar(pd.read_csv(AN / "datos/cuerdas.csv", low_memory=False, keep_default_na=False))

    @cached_property
    def extra(self):  # 19 quipus de OKR sin KFG, mismo esquema (17_okr_pendientes)
        return preparar(pd.read_csv(AN / "17_okr_pendientes/cuerdas_extra.csv", low_memory=False, keep_default_na=False))

    @cached_property
    def Q(self):
        return pd.read_csv(AN / "datos/quipus.csv").set_index("kfg")

    @cached_property
    def matriz(self):
        return pd.read_csv(AN / "28_atlas_generos/matriz.csv", index_col=0)

    @cached_property
    def atlas(self):
        return pd.read_csv(AN / "28_atlas_generos/atlas.csv", index_col=0)

    @cached_property
    def enmiendas(self):  # enmiendas al atlas congelado (no tocan atlas.csv)
        return pd.read_csv(AN / "28_atlas_generos/enmiendas.csv", index_col=0)

    @cached_property
    def alt30(self):  # alternancia de color en el corpus, con q BH (30_frontera_estructura/06_alternancia.py)
        return pd.read_csv(AN / "30_frontera_estructura/alternancia_corpus.csv", index_col=0)

    @cached_property
    def copias33(self):  # pares de copia con nivel (33_estematica); fuera los especulativos y los propuestos de 04
        c = pd.read_csv(AN / "33_estematica/pares_copia.csv")
        return c[c.nivel.isin(NIV33)]

    @cached_property
    def form22(self):
        return pd.read_csv(AN / "22_formularios/quipus_detector.csv").set_index("kfg")

    @cached_property
    def copias14(self):
        return pd.read_csv(AN / "14_copias/pares_resumen.csv")

    @cached_property
    def resumen04(self):
        r = pd.read_csv(AN / "04_concordancias/resultados/pares_resumen_todos.csv.gz")
        return r[(r.q < .05) & (r.q_orden < .05)]

    @cached_property
    def okr(self):
        return sqlite3.connect(DB, uri=True)

    @cached_property
    def por_quipu(self):
        return {k: d for k, d in self.C.groupby("kfg", sort=False)}

    @cached_property
    def CC(self):  # Smith-Waterman log-odds de 04 (numba)
        return _modulo("concordancias04", AN / "04_concordancias/concordancias.py")

    @cached_property
    def N01(self):  # detectores de sumas internas de 01 (numba)
        return _modulo("nucleo01", AN / "01_aritmetica/nucleo.py")

    @cached_property
    def corpus_rel(self):
        """Estructuras del corpus para las relaciones entre quipus (mismas definiciones que 04)."""
        seq, tot, ps = {}, {}, {}
        filas = {}  # k -> (matriz de filas P, dueños)
        for k, d in self.por_quipu.items():
            s = _secuencia(d)
            if len(s) >= 3:
                seq[k] = s
            t = _totales(d)
            if t[2] >= 2:
                tot[k] = t
            for kk, (P, S) in _celdas(d).items():
                filas.setdefault(kk, []).append((k, P))
                if S.any():
                    ps.setdefault(k, {})[kk] = P + S
        filas = {kk: (np.vstack([P for _, P in v]), np.concatenate([[k] * len(P) for k, P in v]))
                 for kk, v in filas.items()}
        return dict(seq=seq, tot=tot, ps=ps, filas=filas)


# --------------------------------------------------------------------------- 1. resumen físico
def fisico(d, ctx):
    p, s = d[d.nivel == 0], d[d.nivel > 0]
    tam = p.groupby("grupo").size()
    col = d.colorn.replace("", "?").value_counts()
    v = d.valor[d.valor > 0]
    datos = dict(
        cuerdas=len(d), colgantes=len(p), subsidiarias=len(s),
        niveles={int(k): int(n) for k, n in d.nivel.value_counts().sort_index().items()},
        grupos=int(p.grupo.nunique()),
        cuerdas_por_grupo=dict(min=int(tam.min()), mediana=float(tam.median()), max=int(tam.max()),
                               modal=int(tam.mode().iloc[0])) if len(tam) else {},
        colores_distintos=int(len(col)), colores=col.head(10).to_dict(),
        torsion=d.torsion.replace("", "?").value_counts().to_dict(),
        valores=dict(min=int(v.min()), mediana=float(v.median()), max=int(v.max()), suma_colgantes=int(p.valor.sum()))
        if len(v) else {},
        rotas=int((d.terminacion == "B").sum()), sin_nudos=int((~d.anudada).sum()),
        union_superior_T=int((d.union == "T").sum()),
    )
    k = d.kfg.iloc[0]
    if k in ctx.Q.index:
        q = ctx.Q.loc[k]
        datos.update(okr=q.okr, museo=q.museo, procedencia=q.procedencia)
    if k in ctx.matriz.index and pd.notna(ctx.matriz.loc[k, "okr_marcadoras"]):
        datos["marcadoras_OKR"] = int(ctx.matriz.loc[k, "okr_marcadoras"])
    a = [af(f"{len(d)} cuerdas ({len(p)} colgantes, {len(s)} subsidiarias) en {datos['grupos']} grupos; "
            f"{datos['rotas']} rotas, {datos['sin_nudos']} sin nudos.", "dato", "analisis/datos/cuerdas.csv"),
         af("Color normalizado sin rangos en cm. Los nombres de color dependen del transcriptor (UR1107 = UR237: "
            "0 de 23 etiquetas iguales); comparar colores solo dentro del mismo transcriptor.", "bien apoyado",
            "analisis/24_color_formato/informe.md")]
    return dict(titulo="Resumen físico", datos=datos, afirmaciones=a)


# --------------------------------------------------------------------------- 2. gramática numérica
RX_NUDO = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([A-Za-z?]+)\)(?:,(-?\d+))?")  # n_nudos_imposibles §3.1


def _posicional(v):
    """True si v = d·10^k con k>=1 (lugar de decenas o más)."""
    if v < 10:
        return False
    k = int(math.floor(math.log10(v)))
    return v % 10 ** k == 0


def no_decimal(nudos):
    """Copiada de analisis/28_atlas_generos/01_matriz.py: lugar repetido o cifra >9 en un lugar."""
    if not nudos.strip():
        return None
    lugares = []
    for tok in nudos.split(";"):
        m = re.search(r",\s*(-?\d+)\s*$", tok)
        if not m:
            continue
        v = int(m.group(1))
        if v <= 0:
            continue
        k = int(np.floor(np.log10(v)))
        if v % 10 ** k:
            return True
        lugares.append(k)
    if not lugares:
        return None
    return len(lugares) != len(set(lugares))


def _racimos(nudos):
    out = []
    for m in RX_NUDO.finditer(nudos):
        n, t, _, dr, v = m.groups()
        out.append((t, int(n), dr, int(v) if v is not None else int(n)))
    return out


def _vueltas_okr(ctx, okr):
    """Cuerdas con algún nudo largo de >=10 vueltas reales en OKR (n_nudos_imposibles: NUM_TURNS)."""
    try:
        return ctx.okr.execute(
            """select count(distinct k.CORD_ID) from knot k join cord c on c.CORD_ID=k.CORD_ID
               join khipu_main m on m.KHIPU_ID=c.KHIPU_ID
               where m.OKR_NUM=? and k.TYPE_CODE='L' and k.NUM_TURNS>=10""", (okr,)).fetchone()[0]
    except sqlite3.Error:
        return None


def gramatica(d, ctx):
    F = "analisis/ds/n_nudos_imposibles/informe.md"
    an = d[d.anudada]
    nd = an.nudos.map(no_decimal)
    frac = float(nd.dropna().astype(float).mean()) if nd.notna().any() else float("nan")
    multi, l10, l10amb, tipos = 0, 0, 0, {}
    for s in an.nudos:
        R = _racimos(s)
        for t, *_ in R:
            tipos[t] = tipos.get(t, 0) + 1
        uni = [v for t, n, _, v in R if t in ("L", "E") and not _posicional(v)]
        multi += len(uni) >= 2 and sum(uni) > 9          # «multiunidad real»: notación aditiva
        l10 += any(t == "L" and v >= 10 and not _posicional(v) for t, n, _, v in R)
        l10amb += any(t == "L" and _posicional(v) and str(v).startswith("1") for t, n, _, v in R)
    k = d.kfg.iloc[0]
    okr = ctx.Q.okr.get(k) if k in ctx.Q.index else (k if k.startswith("KH") else None)
    vr = _vueltas_okr(ctx, okr) if okr else None
    zs = d.torsion.isin(["S", "Z"])
    fz = float((d.torsion == "Z").sum() / zs.sum()) if zs.any() else float("nan")
    datos = dict(cuerdas_anudadas=int(len(an)), frac_no_decimal=frac, tipos_de_nudo=tipos,
                 cuerdas_aditivas=int(multi), L_10_o_mas_KFG=int(l10), L_ambiguos_KFG=int(l10amb),
                 L_10_o_mas_OKR=vr, frac_torsion_Z=fz)
    a = []
    if len(an):
        estandar = frac < .05
        a.append(af(f"Decimal {'estándar' if estandar else 'NO estándar'}: {frac:.0%} de las cuerdas anudadas violan la "
                    "gramática decimal (lugar repetido o cifra >9 en un lugar).", "dato",
                    "analisis/28_atlas_generos/01_matriz.py (no_decimal)"))
    if multi:
        a.append(af(f"{multi} cuerdas con varias unidades en el lugar de las unidades que suman >9 (notación aditiva o "
                    "tally: clase aparte, 915 cuerdas en 76 quipus del corpus).", "dato", F))
    if vr:
        a.append(af(f"{vr} cuerdas con nudos largos de >=10 vueltas reales (OKR NUM_TURNS). No son errores: KFG y OKR "
                    "coinciden al 92,8 % y varias llevan notas del transcriptor.", "apoyado", F))
    elif l10 and vr is None:
        a.append(af(f"{l10} cuerdas con L>=10 en las unidades (vueltas >=10 según la convención KFG); sin OKR para "
                    "confirmar vueltas.", "propuesto", F))
    if l10amb and vr is None:
        a.append(af(f"{l10amb} cuerdas con L de valor 10, 100… : en KFG el número antes de L es el VALOR, no las "
                    "vueltas («200L» = 2 vueltas en centenas); sin OKR no se distingue 10 vueltas de valor posicional.",
                    "bien apoyado", F))
    if frac >= .5 and fz >= .5:
        a.append(af(f"Mayoría no decimal con torsión Z ({fz:.0%}): rasgo del género aditivo/tally (OR 26 en OKR).",
                    "apoyado", "analisis/27_familia_z/ y SINTESIS.md §27_familia_z"))
    return dict(titulo="Gramática numérica", datos=datos, afirmaciones=a)


# --------------------------------------------------------------------------- 3. estructura interna
def _q01(d):
    """Diccionario de analisis/01_aritmetica/nucleo.py::cargar para un solo quipu."""
    d = d.reset_index(drop=True)
    idx = {n: i for i, n in enumerate(d.cuerda)}
    par = np.array([idx.get(p, -1) if p else -1 for p in d.padre], np.int64)
    lvl = d.nivel.to_numpy(np.int64)
    L0 = np.where(lvl == 0)[0].astype(np.int64)
    g = d.grupo.to_numpy()[L0]
    gs = np.concatenate([[0], np.where(np.diff(g) != 0)[0] + 1, [len(L0)]]).astype(np.int64)
    return dict(v=d.valor.to_numpy(np.int64), pres=d.pres.to_numpy(), par=par, lvl=lvl, L0=L0, sub=lvl > 0,
                isT=(d.union.to_numpy()[L0] == "T"), gs=gs, df=d)


def _ejemplos_sumas(d, n=4):
    """Casos concretos (para verificar en el objeto): colgante = Σ subsidiarias; extremo de grupo = Σ resto
    (analisis/28_atlas_generos/02_atlas.py::ejemplo_suma); cuerda superior = Σ grupo vecino."""
    ej = []
    hijos = d[d.nivel > 0].groupby("padre")
    val = dict(zip(d.cuerda, d.valor))
    for padre, h in hijos:
        nz = h.valor[h.valor > 0]
        if len(nz) >= 2 and val.get(padre, 0) >= 10 and val[padre] == nz.sum():
            ej.append(f"{padre} = {val[padre]} = Σ de sus {len(nz)} subsidiarias")
    p = d[d.nivel == 0]
    for g, x in p.groupby("grupo"):
        vals = x.valor.to_numpy()
        if (vals > 0).sum() < 3:
            continue
        for i in (0, len(vals) - 1):
            resto = np.delete(vals, i)
            if vals[i] >= 10 and (resto > 0).sum() >= 2 and vals[i] == resto.sum():
                ej.append(f"grupo {g}: {x.cuerda.iloc[i]} = {vals[i]} = Σ de los otros {(resto > 0).sum()} colgantes")
    tot = p.groupby("grupo").valor.sum()
    for r in p[p.union == "T"].itertuples():
        for gg in (r.grupo - 1, r.grupo + 1):
            if r.valor >= 10 and tot.get(gg, -1) == r.valor:
                ej.append(f"cuerda superior {r.cuerda} = {r.valor} = Σ del grupo {gg}")
    return ej[:n], len(ej)


def sumas(d, ctx, B=999):
    F01 = "analisis/01_aritmetica/nucleo.py (R1, A, TA, F; nulo dentro de nivel)"
    N = ctx.N01
    Q = _q01(d)
    obs = N.todo(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"])
    pidx, seg = N.estratos(Q, 1)
    R = N.run_null(Q["v"], Q["par"], Q["L0"], Q["isT"], Q["gs"], Q["sub"], pidx, seg, B, SEED, 1)
    nom = {"R1 colgante=Σsubsidiarias": 0, "F colgante=Σ vecinos": 2, "A total de grupo(s) adyacentes": 3,
           "TA cuerda superior=Σ grupos": 4}
    res = {n: dict(obs=int(obs[j]), esperado=float(R[:, j].mean()), p=float(p_emp(obs[j], R[:, j])))
           for n, j in nom.items()}
    ej, nej = _ejemplos_sumas(d)
    datos = dict(pruebas=res, ejemplos=ej, n_ejemplos=nej)
    a = []
    pmin = min(r["p"] for r in res.values() if r["obs"] > 0) if any(r["obs"] for r in res.values()) else 1
    if pmin * len(nom) < .05:
        mejor = min((r["p"], n) for n, r in res.items() if r["obs"] > 0)[1]
        a.append(af(f"Sumas internas por encima del azar ({mejor}: {res[mejor]['obs']} frente a "
                    f"{res[mejor]['esperado']:.1f} esperadas; p={pmin:.4f}, Bonferroni sobre 4 pruebas).",
                    "apoyado", F01))
    elif nej:
        a.append(af(f"{nej} sumas exactas sueltas, pero el recuento no supera al azar (p mínimo {pmin:.2f}): el 74 % "
                    "de quipus «con sumas» del KFG es esperable por azar.", "propuesto",
                    "analisis/08_auditoria_sumas/informe.md"))
    k = d.kfg.iloc[0]
    if k in ctx.matriz.index:
        r = ctx.matriz.loc[k]
        if r.sumas_q < .05:
            a.append(af(f"Contabilidad interna verificable en el corpus: sumas locales robustas a dos nulos "
                        f"(q={r.sumas_q:.3f}).", "bien apoyado", "analisis/08_auditoria_sumas/refinado.csv"))
        if r.filatotal_q < .05:
            a.append(af(f"Formato «fila + cuerda-total suelta» (q={r.filatotal_q:.4f}).", "bien apoyado",
                        "analisis/14_copias/fila_total_por_quipu.csv"))
    return dict(titulo="Sumas internas", datos=datos, afirmaciones=a)


def _pbinom_poisson(ps, obs):
    """P(X >= obs) con X = Σ Bernoulli(p_i) (Poisson-binomial exacta)."""
    f = np.zeros(len(ps) + 1)
    f[0] = 1
    for p in ps:
        f[1:] = f[1:] * (1 - p) + f[:-1] * p
        f[0] *= 1 - p
    return float(f[obs:].sum())


def formato(d, ctx):
    """Encabezado (campo 1 máximo, n_ficha_nazca/10_tablas), formato por color (24, n_color_posicion)."""
    from sklearn.metrics import normalized_mutual_info_score as nmi
    rng = np.random.default_rng(SEED)
    p = d[d.nivel == 0]
    a, datos = [], {}
    # encabezado: el primer colgante (o el último) es el máximo de su grupo
    gr = [x.valor.to_numpy() for _, x in p.groupby("grupo") if (x.valor > 0).sum() >= 3]
    if len(gr) >= 3:
        ps = [1 / len(v) for v in gr]
        for lado, f in (("primer", lambda v: np.argmax(v) == 0), ("último", lambda v: np.argmax(v[::-1]) == 0)):
            o = int(sum(f(v) for v in gr))
            pv = _pbinom_poisson(ps, o)
            datos[f"max_{lado}"] = dict(grupos=len(gr), obs=o, esperado=round(sum(ps), 1), p=pv)
            if pv < .025 and o / len(gr) >= .5:
                a.append(af(f"Encabezado: el {lado} colgante es el máximo en {o} de {len(gr)} grupos (esperado "
                            f"{sum(ps):.1f}; p={pv:.1e}). «1.ª columna mayor = partida principal, no total».",
                            "apoyado", "analisis/10_tablas/informe.md; analisis/ds/n_ficha_nazca/informe.md"))
    # color ~ grupo (24_color_formato/p3_transcriptor.py, 199 permutaciones)
    x = p[p.colorn != ""]
    if len(x) >= 20 and x.grupo.nunique() >= 4 and x.colorn.nunique() >= 2:
        o = nmi(x.colorn, x.grupo)
        nul = [nmi(rng.permutation(x.colorn.values), x.grupo) for _ in range(199)]
        datos["color_grupo"] = dict(NMI=round(o, 3), NMI_nulo=round(float(np.mean(nul)), 3), p=p_emp(o, nul))
        if datos["color_grupo"]["p"] < .05:
            a.append(af(f"El color marca el grupo (NMI {o:.2f} frente a {np.mean(nul):.2f} del nulo; "
                        f"p={datos['color_grupo']['p']:.3f}).", "apoyado",
                        "analisis/24_color_formato/p3_transcriptor.py"))
    # color ~ posición dentro de grupos del tamaño modal (n_color_posicion): columnas por color
    tam = p.groupby("grupo").size()
    if len(tam):
        k = int(tam.mode().iloc[0])
        y = p[p.grupo.isin(tam[tam == k].index)].copy()
        y["j"] = y.groupby("grupo").cumcount() + 1
        y = y[y.colorn != ""]
        if k >= 2 and y.grupo.nunique() >= 3 and y.colorn.nunique() >= 2:
            o = nmi(y.colorn, y.j)
            nul = [nmi(rng.permutation(y.colorn.values), y.j) for _ in range(199)]
            pv = p_emp(o, nul)
            cols = {int(j): (z.colorn.value_counts().index[0], round(z.colorn.value_counts(normalize=True).iloc[0], 2))
                    for j, z in y.groupby("j")}
            datos["color_posicion"] = dict(k=k, grupos=int(y.grupo.nunique()), NMI=round(o, 3),
                                           NMI_nulo=round(float(np.mean(nul)), 3), p=pv, columnas=cols)
            if pv < .05:
                marc = "; ".join(f"col {j}: {c} ({s:.0%})" for j, (c, s) in cols.items() if s >= .6)
                a.append(af(f"El color marca columna en los grupos de {k} (NMI {o:.2f} frente a {np.mean(nul):.2f}; "
                            f"p={pv:.3f}). {marc or 'Sin color dominante por columna.'} El color es FORMATO "
                            "(identidad de columna), no un valor.", "apoyado",
                            "analisis/ds/n_color_posicion/informe.md; analisis/24_color_formato/informe.md"))
            if 1 in cols and cols[1][1] >= .6:
                a.append(af(f"La cuerda inicial de cada grupo es {cols[1][0]} en el {cols[1][1]:.0%} de los grupos "
                            "(«blanco = primera cuerda del grupo» en el corpus: 64/133 frente a 43,8).", "dato",
                            "analisis/24_color_formato/informe.md"))
    return dict(titulo="Encabezados y formato por color", datos=datos, afirmaciones=a)


def ficha_nazca(d, ctx):
    """Registros de n campos + 2 marcadoras y regla «campo 1 máximo» con orientación congelada.
    Lógica de analisis/ds/n_ficha_nazca/lib.py (records, canon) y p4_barrido.py (binomial 1/size)."""
    L = _nazca_lib()
    c = d.assign(v=np.where(d.anudada, d.valor, np.nan), col=d.colorn.replace("", "?"),
                 dir1="", torsion=d.torsion.replace("", "?"), union=d.union.replace("", "?"))
    k = d.kfg.iloc[0]
    filas, a = [], []
    for size in (8, 9, 10):
        R = L.records(c, k, size=size)
        if len(R) < 3:
            continue
        M = [L.canon(r["vals"], r["pos"], size=size) for r in R if not np.isnan(r["vals"]).any()]
        if not M:
            continue
        o = int(sum(np.argmax(m) == 0 for m in M))
        pv = binomtest(o, len(M), 1 / size, alternative="greater").pvalue
        filas.append(dict(size=size, registros=len(R), completos=len(M), campo1_max=o, p=pv, p_bonf=min(1, 3 * pv),
                          marcadoras=sorted({r["pos"] for r in R})))
    datos = dict(barrido=filas)
    for f in filas:
        if f["p_bonf"] < .05 and f["campo1_max"] / f["completos"] >= .8:
            a.append(af(f"Ficha «encabezado + par marcador»: registros de {f['size']} cuerdas = {f['size'] - 2} campos + "
                        f"2 marcadoras; el campo 1 es el máximo en {f['campo1_max']} de {f['completos']} registros "
                        f"(p={f['p_bonf']:.1e}, Bonferroni sobre 3 tamaños).", "apoyado",
                        "analisis/ds/n_ficha_nazca/informe.md; analisis/ds/n_ur1140_nazca/informe.md"))
    return dict(titulo="Formato Nazca/Berlín (encabezado de campos + par marcador)", datos=datos, afirmaciones=a)


_NZ = None


def _nazca_lib():
    global _NZ
    if _NZ is None:
        _NZ = _modulo("nazca_lib", AN / "ds/n_ficha_nazca/lib.py")
    return _NZ


def formulario(d, ctx):
    """Formulario con clave de reparto (analisis/22_formularios/detector.py). En el corpus se lee el
    resultado publicado (corregido por BH/Holm sobre 651 quipus); en un CSV nuevo se recalcula."""
    k = d.kfg.iloc[0]
    F = "analisis/22_formularios/quipus_detector.csv"
    if k in ctx.form22.index and k in ctx.por_quipu:
        r = ctx.form22.loc[k]
        datos = {c: (None if pd.isna(r[c]) else r[c]) for c in ("Q", "fam", "clave", "cuotas", "p_q", "q_bh", "holm")}
        fuente_calc = "publicado"
    else:
        D = _modulo("detector22", AN / "22_formularios/detector.py") if not hasattr(ctx, "_D22") else ctx._D22
        ctx._D22 = D
        p = d[d.nivel == 0]
        cf = [D.norm(x) for x in p.color]
        dd = dict(v=p.valor.to_numpy(float), cf=cf, cg=[x[:1] for x in cf], g=p.grupo.to_numpy(),
                  cu=p.cuerda.to_numpy(), n_cuerdas=len(d))
        r = D.analizar_quipu((k, dd, 199))
        q = "no" if not r.get("m") or r.get("p_q", 1) >= .05 else ("posicional" if r["fam"] == "P" else "cromatico")
        datos = dict(Q=q, fam=r.get("fam"), clave=r.get("clave"), cuotas=r.get("cuotas"), p_q=r.get("p_q"),
                     q_bh=None, holm=None)
        fuente_calc = "recalculado (sin corrección de corpus)"
    datos["calculo"] = fuente_calc
    a = []
    if datos["Q"] not in (None, "no"):
        fuerte = datos["holm"] is not None and datos["holm"] < .05
        a.append(af(f"Formulario {datos['Q']}: bloques que repiten la clave {datos['clave']} con reparto "
                    f"{datos['cuotas']} (p perm={datos['p_q']:.4f}"
                    + (f"; q BH={datos['q_bh']:.4f}; Holm={datos['holm']:.3f}" if datos["q_bh"] is not None else "")
                    + ").", "apoyado" if fuerte else "propuesto", F))
    if k in ctx.matriz.index and ctx.matriz.loc[k, "form_archivo"] == "bien apoyado-local":
        a.append(af("Clave de reparto compartida por los quipus de su archivo (formulario local).", "apoyado",
                    "analisis/22_formularios/formularios.csv; analisis/26_clave_local/"))
    return dict(titulo="Formulario con clave de reparto", datos=datos, afirmaciones=a)


# --------------------------------------------------------------------------- 4. relaciones entre quipus
def _secuencia(d):  # 04: valores de las cuerdas con nudos (todas las jerarquías) en orden
    return d.valor[d.anudada].to_numpy(np.int64)


def _totales(d):  # 04: totales de grupos con >=2 colgantes anudados
    p = d[(d.nivel == 0) & d.anudada]
    cnt = p.groupby("grupo").size()
    ok = sorted(cnt[cnt >= 2].index)
    p = p[p.grupo.isin(ok)]
    return p.valor.to_numpy(np.int64), pd.Categorical(p.grupo, categories=ok).codes.astype(np.int64), len(ok)


def _celdas(d):
    """n_cuota_entrega/lib_cuota.py::celdas: por grupo de >=5 colgantes, vectores P y S1 (0 = ausente)."""
    p = d[d.nivel == 0]
    s1 = d[(d.nivel == 1) & (d.cuerda == d.padre + "s1")]
    m1 = dict(zip(s1.padre, np.where(s1.pres, s1.valor, 0)))
    out = {}
    for g, x in p.groupby("grupo"):
        if len(x) < 5:
            continue
        P = np.where(x.pres, x.valor, 0).astype(np.int64)
        S = np.array([m1.get(c, 0) for c in x.cuerda], np.int64)
        P2, S2 = out.get(len(x), (np.empty((0, len(x)), np.int64),) * 2)
        out[len(x)] = (np.vstack([P2, P]), np.vstack([S2, S]))
    return out


def _celda_stat(V, filas):
    """Nº de grupos-fuente cuya mejor fila destino acierta >= 2/3 de las columnas (±1, ambas >0);
    n_cuota_entrega/03_relaciones.py (6/9 en UR270->UR278), con valores >=10. V, filas: {k: matriz}."""
    s = 0
    for k, X in V.items():
        if k not in filas:
            continue
        T = filas[k]
        # solo cuentan celdas >=10: con valores pequeños las coincidencias ±1 caen (04, negativos)
        h = ((X[:, None, :] >= 10) & (T[None] >= 10) & (np.abs(X[:, None, :] - T[None]) <= 1)).sum(2)
        s += int((h.max(1) >= math.ceil(2 * k / 3)).sum())
    return s


def p_secuencial(nulo, obs, rng, B=199, Bmax=20000, h=10):
    """p de permutación en tandas (como p_secuencial de 22_formularios/detector.py): sigue mientras haya
    menos de h excedencias, hasta Bmax réplicas. nulo(rng) -> estadístico nulo."""
    ex = n = 0
    while n < Bmax and (n == 0 or ex < h):
        b = B if n == 0 else min(2000, Bmax - n)
        ex += sum(nulo(rng) >= obs - 1e-12 for _ in range(b))
        n += b
    return (1 + ex) / (1 + n)


def relaciones(d, ctx, B=199):
    """Relaciones con el corpus. Tres detectores, cada uno con su nulo; BH sobre todos los quipus comparados
    (los no refinados cuentan con p=1, conservador, como en 04):
      copia    SW log-odds de 04 (ambos sentidos = inversión); p = max(nulo barajado, nulo por bloques de 5);
               cola Gumbel (04).
      totales  totales de grupo de A en orden entre las cuerdas de B (04 tarea 2); p = max(nulo de orden,
               nulo de magnitud); A->B y B->A.
      celda    colgante + 1.ª subsidiaria de A = filas de B en >=2/3 de las columnas (13; n_cuota_entrega/03);
               nulo: permutar el vector dentro de cada grupo; se descarta si con solo P ya coincide igual."""
    CC, K = ctx.CC, ctx.corpus_rel
    k = d.kfg.iloc[0]
    rng = np.random.default_rng(SEED)
    hall = []

    def reporta(tipo, o, d_, con, det, p):
        hall.append(dict(tipo=tipo, origen=o, destino=d_, con=con, detalle=det, p=p))

    # --- copias / cuasi-duplicados (04 tarea 1) ---
    a = _secuencia(d)
    otros = [j for j in K["seq"] if j != k]
    if len(a) >= 3:
        obs = np.array([CC.score_dup(a, K["seq"][j], CC.GAP) for j in otros])
        p = np.ones(len(otros))
        for i in np.where((obs >= 20) | (obs >= np.sort(obs)[-3]))[0]:
            b = K["seq"][otros[i]]
            # 04 exige los dos nulos: barajado simple y por bloques de 5 (conserva rachas de valores repetidos)
            p[i] = max(CC.p_valor(obs[i:i + 1], np.array([[CC.score_dup(CC.barajar(a, bl), CC.barajar(b, bl), CC.GAP)
                                                            for _ in range(B)]]))[0][0] for bl in (1, 5))
        q = bh(p)
        for i in np.where(q < .05)[0]:
            b = K["seq"][otros[i]]
            sc, sentido, path = CC.traza(CC.matriz_dup(a, b))
            al = [(x, y) for x, y in path if x is not None and y is not None]
            ex = sum(a[x] == b[y] for x, y in al)
            reporta("copia" if sentido == "directo" else "copia invertida", k, otros[i], otros[i],
                    f"{k} ~ {otros[i]}: {ex}/{len(al)} cuerdas alineadas exactas ({sc:.0f} bits)", p[i])
            hall[-1]["q"] = q[i]

    # --- totales de grupo que reaparecen en orden (A -> B y B -> A) ---
    def totales(t):
        return np.bincount(t[1], weights=t[0], minlength=t[2]).astype(np.int64)

    def p_sum(t, b, o):
        pv, gid, ng = t
        tot = totales(t)
        n_ord = np.array([[CC.score_sum(rng.permutation(tot), b, CC.GAP) for _ in range(B)]])
        n_mag = np.array([[CC.score_sum(totales((rng.permutation(pv), gid, ng)), CC.barajar(b, 1), CC.GAP)
                           for _ in range(B)]])
        return max(CC.p_valor(np.array([o]), n_ord)[0][0], CC.p_valor(np.array([o]), n_mag)[0][0])

    mio = _totales(d)
    pares = []
    if mio[2] >= 2:
        pares += [(k, j, mio, K["seq"][j]) for j in otros]
    if len(a) >= 3:
        pares += [(j, k, K["tot"][j], a) for j in K["tot"] if j != k]
    if pares:
        obs = np.array([CC.score_sum(totales(t), b, CC.GAP) for _, _, t, b in pares])
        p = np.ones(len(pares))
        for i in np.where((obs >= 15) | (obs >= np.sort(obs)[-2]))[0]:
            p[i] = p_sum(pares[i][2], pares[i][3], obs[i])
        q = bh(p)
        for i in np.where(q < .05)[0]:
            o, d_ = pares[i][:2]
            reporta("totales en orden", o, d_, d_ if o == k else o,
                    f"totales de grupo de {o} reaparecen en orden entre las cuerdas de {d_} ({obs[i]:.0f} bits)", p[i])
            hall[-1]["q"] = q[i]

    # --- celda = P + S1 (fuente con subsidiarias -> filas del destino), ambos sentidos ---
    mias = _celdas(d)
    filas_mias = {kk: P for kk, (P, S) in mias.items()}
    ps_mia = {kk: P + S for kk, (P, S) in mias.items() if S.any()}
    Fl = K["filas"]
    cand = []  # (origen, destino, V = P+S1 de origen, P de origen, filas de destino)
    if ps_mia:
        for j in otros:
            fj = {kk: Fl[kk][0][Fl[kk][1] == j] for kk in ps_mia if kk in Fl}
            fj = {kk: T for kk, T in fj.items() if len(T)}
            if fj:
                cand.append((k, j, ps_mia, {kk: filas_mias[kk] for kk in ps_mia}, fj))
    for j, V in K["ps"].items():
        fj = {kk: filas_mias[kk] for kk in V if kk in filas_mias}
        if j != k and fj:
            cand.append((j, k, V, {kk: Fl[kk][0][Fl[kk][1] == j] for kk in V}, fj))
    p = np.ones(len(cand))
    obs = np.zeros(len(cand), int)
    for i, (o, d_, V, P, fj) in enumerate(cand):
        obs[i] = _celda_stat(V, fj)
        if obs[i] >= 2 and _celda_stat(P, fj) < obs[i]:  # con solo P ya coincide: es copia de filas, no celda
            p[i] = p_secuencial(lambda g: _celda_stat({kk: g.permuted(X, axis=1) for kk, X in V.items()}, fj),
                                obs[i], rng)
    q = bh(p)
    for i in np.where(q < .05)[0]:
        o, d_, V, P, fj = cand[i]
        reporta("celda = P + S1", o, d_, d_ if o == k else o,
                f"{obs[i]} grupos de {o} (colgante + 1.ª subsidiaria) coinciden con filas de {d_} en >=2/3 de "
                f"las columnas; con solo P: {_celda_stat(P, fj)}", p[i])
        hall[-1]["q"] = q[i]

    # --- relaciones documentadas en el repo ---
    doc = [r for r in RELACIONES_DOC if k in re.split(r"[+/]", r[0]) or k in re.split(r"[+/]", r[1])]
    for _, x in ctx.copias14.iterrows():
        if k in (x.A, x.B):
            nv = {"mismo_objeto": "bien apoyado", "copia": "apoyado"}.get(x.tipo, "propuesto")
            doc.append((x.A, x.B, f"{x.tipo.replace('_', ' ')} ({x.n_exacta}/{x.n_alineadas} exactas; q04={x.q_04:.1e})",
                        nv, "analisis/14_copias/pares_resumen.csv; analisis/04_concordancias/resultados/pares_significativos.csv"))
    # 33_estematica: se añade si el par no está ya documentado con un nivel igual o mayor
    for x in ctx.copias33[(ctx.copias33.kfg_a == k) | (ctx.copias33.kfg_b == k)].itertuples():
        nv = NIV33[x.nivel]
        if any(_mismo_par(x.kfg_a, x.kfg_b, o, d_) and RANGO[n] >= RANGO[nv] for o, d_, _, n, _ in doc):
            continue
        cifras = f"; {x.exactas:.0f}/{x.alineadas:.0f} exactas" if pd.notna(x.alineadas) else ""
        doc.append((x.kfg_a, x.kfg_b, f"copia: {x.transformacion}{cifras}"
                    + (f"; Holm={x.holm:.1e}" if pd.notna(x.holm) else "") + (f"; familia {x.familia}" if pd.notna(x.familia) else "")
                    + f" (33: {x.nivel})", nv, "analisis/33_estematica/pares_copia.csv; analisis/33_estematica/informe.md"))
    F = ("lector (recalculado): analisis/04_concordancias/concordancias.py; "
         "analisis/ds/n_cuota_entrega/03_relaciones.py")
    # recalculadas: BH solo dentro de esta consulta (no sobre las ~210 000 parejas del corpus) -> «propuesto»;
    # si coinciden con una documentada, vale el nivel de la documentada
    def aviso(h):  # una recalculada que el repo ya evaluó como negativa o especulativa lo dice
        n = [n for o, d_, _, n, _ in doc if n in ("negativa", "especulativo") and _mismo_par(h["origen"], h["destino"], o, d_)]
        return f" Evaluada en 33_estematica: {n[0].upper()} (ver documentada)." if n else ""

    afs = [af(f"{h['tipo']}: {h['detalle']} (p={h['p']:.1e}; q BH en esta consulta={h['q']:.3f}).{aviso(h)}", "propuesto", F)
           for h in hall]
    afs += [af(f"{o} → {d_}: {txt} [documentada]", nv, f) for o, d_, txt, nv, f in doc]
    if not hall and not doc:
        afs.append(af(f"Sin relaciones con otros quipus del corpus ({len(otros)} comparados; BH q>=0,05 en copia, "
                      "totales y celda).", "dato", F))
    return dict(titulo="Relaciones con otros quipus del corpus", datos=dict(detectadas=hall), afirmaciones=afs)


RELACIONES_DOC = [  # (origen, destino, qué, nivel, fuente) — de analisis/SINTESIS.md
    ("UR270", "UR278", "cada celda de UR278 = colgante + 1.ª subsidiaria de UR270 (5 grupos con >=6/9; solo P: 0; p=0,0002)",
     "bien apoyado", "analisis/ds/n_cuota_entrega/relaciones.csv; analisis/13_sistema_incahuasi/; analisis/16_verificacion_incahuasi/"),
    ("UR270", "UR273B", "Σ colgantes de cada grupo = cabecera del componente B (4/9; p=0,0004)", "bien apoyado",
     "analisis/ds/n_cuota_entrega/informe.md"),
    ("UR278", "UR266", "totales de fila reaparecen en orden (11 exactos; q=1e-8, q de orden=7e-4)", "bien apoyado",
     "analisis/04_concordancias/resultados/pares_resumen_todos.csv.gz; analisis/29_lectura_incahuasi/coherencia.py"),
    ("UR278", "UR275", "totales de fila reaparecen en orden como cabeceras (7)", "apoyado",
     "analisis/29_lectura_incahuasi/coherencia.py; analisis/13_sistema_incahuasi/grafo_quipus.csv"),
    ("UR266", "UR275", "copia del libro (44 de 46 aristas exactas)", "bien apoyado",
     "analisis/13_sistema_incahuasi/grafo_quipus.csv; analisis/09_incahuasi/informe.md"),
    ("UR273A+UR273B", "UR266/UR275/UR269", "parte A + parte B = cabecera del libro (8/18 exactas, Holm 0,002)", "bien apoyado",
     "analisis/13_sistema_incahuasi/informe.md; analisis/16_verificacion_incahuasi/informe.md"),
    ("UR267A+UR267B", "UR269", "A + B = filas de UR269 con cuota 25 (5/26; p=5e-4)", "apoyado",
     "analisis/16_verificacion_incahuasi/informe.md"),
    ("UR255", "UR267A", "comparten los brutos x; cuota 15 (trío [x, c, x−c])", "apoyado", "analisis/09_incahuasi/informe.md"),
    ("UR256", "UR267B", "comparten los brutos x; cuota 10 (trío [x, c, x−c])", "apoyado", "analisis/09_incahuasi/informe.md"),
    ("UR273A", "UR274A", "copia", "apoyado", "analisis/13_sistema_incahuasi/informe.md"),
    ("UR273B", "UR274B", "copia", "apoyado", "analisis/13_sistema_incahuasi/informe.md"),
    ("UR068", "UR067", "secciones suman columna a columna (15/20; Holm<=0,0006), jerarquía de Urton y Brezine", "bien apoyado",
     "analisis/ds/n_puruchuco_pacha/informe.md"),
    ("UR063", "UR068", "consolida columna a columna (14/20; Holm<=0,0006)", "bien apoyado",
     "analisis/ds/n_puruchuco_pacha/informe.md"),
    ("UR063", "UR073/UR078", "consolida bloques (5/5 cabeceras, p=1e-4)", "propuesto", "analisis/04_concordancias/informe.md"),
    ("UR021", "UR006", "fuente de los meses 13–16 (0/300 permutaciones)", "apoyado", "analisis/12_urton2017/informe.md"),
    # rondas 17–18 (SINTESIS: «33_estematica», «30_frontera_estructura», «Desajustes UR278 → libro»)
    ("UR234", "UR1104", "extracto de un campo: UR1104 reproduce en orden las cabeceras (campo 1) de los registros de 8 "
     "cuerdas de UR234: 8 de 4 cifras exactas; la única variante (3102/3012) es el mismo nudo en otra posición decimal. "
     "UR1104 conserva 2016, la cabecera que en UR234 está rota (predicción verificable en el objeto). Post hoc",
     "apoyado", "analisis/33_estematica/informe.md; analisis/33_estematica/05_orden_libre.py"),
    ("UR231", "UR108", "extracto de un campo: UR108 reproduce la cuerda 9 de las 6 secciones de UR231 (5/6 exactas; con 7 "
     "cuerdas el orden aporta solo 1/60). Si se confirma, apoya la unión de los fragmentos VA16135a/b. Post hoc",
     "propuesto", "analisis/33_estematica/informe.md; analisis/33_estematica/05_orden_libre.py"),
    ("KH0049", "UR122", "UR122 copia la sección de subtotales (B1, B3–B5) de la tabla jerárquica de KH0049 (bloques de 18: "
     "B0 = B1+B2 en 14/18, B1 = B3+B4+B5 en 7/18; p=5e-5 cada una). La discrepancia 15652/15649 está en las dos: "
     "viene del original o de una fuente común. Post hoc", "apoyado",
     "analisis/30_frontera_estructura/07_ur122_kh0049.py; analisis/33_estematica/informe.md"),
    ("UR278", "UR266/UR275", "desajustes detalle → libro: de las 26 filas de UR278, 18 tienen destino; 11 son exactas y 7 "
     "desajustes (libro − detalle: +6, +100, +1, −1, +1, −1, −1). Sin dirección (4+/3−, p=1,0); 6 de 7 en las unidades "
     "(p=0,007). Error de conteo de vueltas en nudos largos, no convención. La fila g29 (1507) apunta a UR266 g2, "
     "destino ya de g1: revisar si es duplicado", "apoyado", "analisis/34_comparada/desajustes.py; analisis/SINTESIS.md"),
    ("UR004", "UR091", "totales de grupo en orden (candidata del lector): evaluada y NEGATIVA (exactos p=0,41; ±1 nudo "
     "p=0,51; multibloque p=0,7)", "negativa", "analisis/33_estematica/06_candidatas_lector.py; salida_06.txt"),
    ("UR1034", "UR1145", "totales de grupo en orden (candidata del lector): 5 exactos en orden (p(L)=4e-4), pero 4 de 5 "
     "totales < 20 y nada con ±1 nudo ni multibloque (q=1): ESPECULATIVA", "especulativo",
     "analisis/33_estematica/06_candidatas_lector.py; salida_06.txt"),
]
NIV33 = {"bien apoyado": "bien apoyado", "mismo objeto (bien apoyado)": "bien apoyado", "apoyado": "apoyado",
         "apoyado (post hoc)": "apoyado", "apoyado (entre museos)": "apoyado", "propuesto (post hoc)": "propuesto", "ninguno (negativa)": "negativa",
         "especulativo (post hoc)": "especulativo"}
RANGO = {"bien apoyado": 3, "apoyado": 2, "propuesto": 1, "especulativo": 0, "negativa": 0}


def _mismo_par(a, b, o, d_):
    """¿El par (a, b) es el documentado o -> d_? Los documentados pueden agrupar quipus: «UR273A+UR273B», «UR266/UR275»."""
    o, d_ = re.split(r"[+/]", o), re.split(r"[+/]", d_)
    return (a in o and b in d_) or (b in o and a in d_)


# --------------------------------------------------------------------------- 5. género del atlas
PRED = {  # frases fijas de analisis/28_atlas_generos/02_atlas.py::pred (para un CSV nuevo)
    "NAZ": "Registros = campos + 2 marcadoras; el campo 1 es el máximo en >=90 % de los registros; ningún campo suma a otros.",
    "ARC": "Sus totales o celdas reaparecen en otros quipus del mismo archivo; una relectura del objeto debe conservarlos.",
    "FOR": "Otro quipu del mismo archivo repetirá las proporciones de la clave (±0,05) aunque cambie la escala.",
    "TAL": "En el objeto: torsión Z, nudos largos de muchas vueltas en racimos no decimales; ninguna cuerda es suma de otras.",
    "NON": "En foto: cuerdas sin nudos o con nudos no axiales; una retranscripción no hallará valores decimales.",
    "SUM": "Totales de grupo adyacentes a sus partes; un documento equivalente declarará totales exactos.",
    "ASG": "Cifras redondas y cuotas iguales por unidad, sin filas co-crecientes.",
    "TAB": "La 1.ª columna será la mayor y una fila grande lo será en todas; el total de fila NO estará en el quipu.",
    "SEG": "Cambios de color y marcadoras caen en fronteras de grupo; no se espera aritmética entre bloques.",
    "SIN": "Decimal sin estructura detectada. Refuta: un detector congelado que encienda en una retranscripción.",
}


def _fila_matriz(d, fichas):
    """Fila parcial de matriz.csv con lo que el lector recalcula; el resto queda vacío (reglas lo tratan
    como ausente). Columnas y definiciones de analisis/28_atlas_generos/01_matriz.py."""
    g = {s["titulo"]: s["datos"] for s in fichas}
    gr, fi = g["Gramática numérica"], g["Resumen físico"]
    nz = [f["p_bonf"] for f in g["Formato Nazca/Berlín (encabezado de campos + par marcador)"]["barrido"]]
    sp = [r["p"] * 4 for r in g["Sumas internas"]["pruebas"].values()]
    fo = g["Formulario con clave de reparto"]
    intact = d[(d.terminacion == "K") & (d.valor >= 10)]
    rr = int((intact.valor % 10 == 0).sum())
    rel = g["Relaciones con otros quipus del corpus"]["detectadas"]
    return pd.Series(dict(
        n_cuerdas=len(d), frac_anudada=d.anudada.mean(), frac_rota=(d.terminacion == "B").mean(),
        frac_nodec=gr["frac_no_decimal"], frac_Z=gr["frac_torsion_Z"],
        vueltas10=gr["L_10_o_mas_OKR"] or gr["L_10_o_mas_KFG"],
        nazca_p=min(nz) if nz else np.nan, okr_marcadoras=np.nan, sumas_q=min(sp), sumas_q_M1=min(sp),
        sumas_01=False, filatotal_q=np.nan, rel_archivo="propuesta" if rel else "", copias="", trio_xcx=False,
        form_Q=fo["Q"] or "no", form_holm=np.nan, form_qbh=fo["p_q"] if fo["p_q"] is not None else np.nan,
        form_archivo=np.nan, santa_q=np.nan, santa_pcorpus=np.nan, calend_q=np.nan, procedencia="",
        okr_frac_camelido=np.nan, pure_tally=False, nonum_subtipo=np.nan,
        red_n=len(intact), red_frac=rr / len(intact) if len(intact) else np.nan,
        red_q=binomtest(rr, len(intact), .1, alternative="greater").pvalue if len(intact) else np.nan,
        cuotas_rep_q=np.nan, tabla_R=np.nan, tabla_K=np.nan, tabla_q_orden=np.nan, tabla_rho=np.nan,
        color_grupo_p=g["Encabezados y formato por color"].get("color_grupo", {}).get("p", np.nan), segm_q=np.nan))


def genero(d, ctx, fichas):
    RG = ctx.__dict__.get("_RG") or _modulo("reglas28", AN / "28_atlas_generos/reglas.py")
    ctx._RG = RG
    k = d.kfg.iloc[0]
    F = "analisis/28_atlas_generos/atlas.csv; analisis/28_atlas_generos/reglas.py"
    if k in ctx.atlas.index and k in ctx.por_quipu:
        r = ctx.atlas.loc[k]
        recalc = RG.clasificar(ctx.matriz.loc[[k]]).loc[k, "genero"]  # las reglas sobre la matriz publicada
        datos = dict(genero=r.genero, nombre=r.genero_nombre, confianza=r.confianza, evidencia=r.evidencia,
                     prediccion=r.prediccion, estabilidad=r.estabilidad, reglas_reproducen=bool(recalc == r.genero),
                     calculo="atlas publicado")
        nivel = "apoyado" if r.confianza == "alta" else "propuesto"
    else:
        M = _fila_matriz(d, fichas).to_frame(k).T
        out, pobre = RG.reglas(k, M.iloc[0])
        if out:
            gg = sorted(out, key=lambda x: (-out[x][0], RG.ORDEN.index(x)))[0]
            lv, _, ev = out[gg]
        else:
            gg, lv, ev = "SIN", 0, "datos insuficientes" if pobre else "decimal sin estructura detectada"
        conf = {3: "alta", 2: "media", 1: "baja"}.get(min(lv, 2), "sin genero")  # recálculo parcial: tope «media»
        datos = dict(genero=gg, nombre=RG.NOMBRE[gg], confianza=conf, evidencia=ev, prediccion=PRED.get(gg, ""),
                     calculo="reglas del atlas sobre rasgos recalculados (parciales; tope de confianza: media)")
        nivel = "propuesto"
    a = [af(f"Género: {datos['nombre']} ({datos['genero']}), confianza {datos['confianza']}. {datos['evidencia']}",
            nivel, F),
         af(f"Predicción comprobable: {datos['prediccion']}", "propuesto", F)]
    if k in ctx.por_quipu and k in ctx.enmiendas.index:  # atlas.csv queda congelado; la enmienda se muestra aparte
        e = ctx.enmiendas.loc[k]
        datos["enmienda"] = dict(genero=e.genero_nuevo, nombre=RG.NOMBRE[e.genero_nuevo], confianza=e.confianza,
                                 evidencia=e.evidencia, fuente=e.fuente, fecha=e.fecha)
        a.append(af(f"Enmienda al atlas ({e.fecha}): {RG.NOMBRE[e.genero_nuevo]} ({e.genero_nuevo}), confianza "
                    f"{e.confianza}. {e.evidencia}", "apoyado" if e.confianza == "alta" else "propuesto",
                    f"analisis/28_atlas_generos/enmiendas.csv; {e.fuente}"))
    return dict(titulo="Género del atlas", datos=datos, afirmaciones=a)


# --------------------------------------------------------------------------- 6. detectores de 30_frontera_estructura
# Enganchados en DETECTORES_EXTRA (al final de este bloque). Son genéricos: no nombran quipus.
def _acf_prom(X, base):
    """Copiada de analisis/30_frontera_estructura/01_internas.py::acf_prom (match=True; T2): prominencia máxima de la
    autocorrelación de coincidencias de color en los desfases 2..n//3. X (N, n) códigos de color.
    Devuelve (prominencia, desfase) por fila."""
    n = X.shape[1]
    K = n // 3
    A = [(X[:, :-k] == X[:, k:]).mean(1) - base for k in range(1, K + 2)]
    pr = np.array([np.where(A[k - 1] > 0, A[k - 1] - (A[k - 2] + A[k]) / 2, -1.0) for k in range(2, K + 1)])
    return pr.max(0), pr.argmax(0) + 2


def alternancia(d, ctx, Bmax=9999):
    """Alternancia de dos colores A/B/A/B (desfase 2) entre colgantes. Estadístico T2 y nulo de
    analisis/30_frontera_estructura/06_alternancia.py: permutar los colores (p en tandas de 1000, hasta 9 999
    réplicas o 10 excedencias). Pares de colores vecinos y columna dominante: 04_diagnosticos.py.
    En el corpus el nivel sale de la q BH publicada (515 quipus, alternancia_corpus.csv); en un CSV, propuesto."""
    from collections import Counter
    F = "analisis/30_frontera_estructura/06_alternancia.py; analisis/30_frontera_estructura/informe.md §4.3"
    T = "Alternancia de dos colores (tabla de dos columnas intercalada)"
    p = d[d.nivel == 0]
    col = p.colorn.replace("", "?").to_numpy()
    v = p.valor.to_numpy()
    u, c = np.unique(col, return_inverse=True)
    if len(c) < 10 or len(u) < 2:  # mismo filtro que t2 de 01_internas.py
        return dict(titulo=T, datos=dict(evaluado=False), afirmaciones=[])
    base = ((np.bincount(c) / len(c)) ** 2).sum()
    o, lag = _acf_prom(c[None, :], base)
    o, lag = float(o[0]), int(lag[0])
    alt = sum(col[i] != col[i + 1] and col[i] == col[i + 2] for i in range(len(col) - 2))
    datos = dict(evaluado=True, desfase=lag, estadistico=round(o, 4), posiciones_alternas=int(alt), colgantes=len(col),
                 colores=len(u))
    a = []
    if lag != 2:  # solo interesa el desfase 2; el nulo no se corre (ahorra tiempo en --todos)
        return dict(titulo=T, datos=datos, afirmaciones=a)
    rng = np.random.default_rng(SEED)
    ex = n = 0
    while n < Bmax and (n == 0 or ex < 10):
        b = min(1000, Bmax - n)
        ex += int((_acf_prom(rng.permuted(np.tile(c, (b, 1)), axis=1), base)[0] >= o - 1e-12).sum())
        n += b
    pv = (1 + ex) / (1 + n)
    top = [x for x, _ in Counter(col).most_common(2)]
    pares = [(v[i], v[i + 1]) for i in range(len(col) - 1) if col[i] == top[0] and col[i + 1] == top[1]]
    pares += [(v[i + 1], v[i]) for i in range(len(col) - 1) if col[i] == top[1] and col[i + 1] == top[0]]
    g0, g1 = int(sum(x > y for x, y in pares)), int(sum(y > x for x, y in pares))
    nulos = bool(pares) and np.mean([max(x, y) <= 1 for x, y in pares]) >= .5
    ps = binomtest(max(g0, g1), g0 + g1, .5).pvalue if g0 + g1 else 1.0
    datos.update(p=pv, replicas=n, colores_alternos=top, pares=len(pares),
                 dominante=dict(color=top[0] if g0 >= g1 else top[1], gana=max(g0, g1), de=g0 + g1, p_signo=float(ps)),
                 valores_casi_nulos=bool(nulos))
    k = d.kfg.iloc[0]
    pub = ctx.alt30.loc[k] if k in ctx.por_quipu and k in ctx.alt30.index else None
    txt = (f"Alternancia de dos colores {top[0]}/{top[1]} con desfase 2: {alt} de {len(col)} posiciones alternan "
           f"(p perm={pv:.1e}, {n} réplicas")
    if pub is not None and pub.q < .05 and pub.lag == 2:
        datos["q_corpus"] = float(pub.q)
        a.append(af(txt + f"; q BH del corpus={pub.q:.4f}, 515 quipus).", "apoyado",
                    F + "; analisis/30_frontera_estructura/alternancia_corpus.csv"))
    elif pv < .05:
        a.append(af(txt + "; sin corrección de corpus).", "propuesto", F))
    if a:
        dom = datos["dominante"]
        a.append(af("Se lee como una tabla de dos columnas escrita intercalando (unidad = par de cuerdas, columna = color)"
                    + (f"; en los pares con valor, {dom['color']} es mayor en {dom['gana']} de {dom['de']} "
                       f"(p signo={ps:.3f})" if ps < .05 else "; ningún color domina dentro del par")
                    + ("; los valores son casi todos 0 o 1: el formato es seguro, el contenido no" if nulos else "") + ".",
                    "propuesto",
                    "analisis/30_frontera_estructura/informe.md (4.3 y 5); 04_diagnosticos.py"))
    return dict(titulo=T, datos=datos, afirmaciones=a)


def totales_columna(d, ctx, B=20000):
    """Totales por columna entre bloques de igual tamaño (generaliza analisis/30_frontera_estructura/07_ur122_kh0049.py).
    Los colgantes se cortan en bloques consecutivos del tamaño de grupo modal. Candidato: bloque T y tramo de 2 o 3
    bloques consecutivos P1..Pm (sin T) con T = Σ P posición a posición (exacto, T > 0). Nulo de 07: permutar las
    posiciones del último sumando dentro de su bloque (B réplicas). BH sobre todos los candidatos del quipu; los que
    no llegan a 3 aciertos (ni a 1/3 del bloque) cuentan con p = 1 (conservador, como en 04)."""
    F = "analisis/30_frontera_estructura/07_ur122_kh0049.py; analisis/30_frontera_estructura/informe.md (T6)"
    T = "Totales por columna entre bloques (tabla jerárquica)"
    p = d[d.nivel == 0]
    v = p.valor.to_numpy(np.int64)
    tam = p.groupby("grupo").size()
    k = int(tam.mode().iloc[0]) if len(tam) else 0
    nb = len(v) // k if k else 0
    datos = dict(bloque=k, bloques=nb, significativos=[])
    if k < 4 or nb < 3:
        return dict(titulo=T, datos=datos, afirmaciones=[])
    X = v[:nb * k].reshape(nb, k)
    cand = [(i, j, m) for m in (2, 3) for j in range(nb - m + 1) for i in range(nb) if not j <= i < j + m]
    obs = np.array([((X[i] == X[j:j + m].sum(0)) & (X[i] > 0)).sum() for i, j, m in cand])
    pv = np.ones(len(cand))
    rng = np.random.default_rng(SEED)
    for c in np.where(obs >= max(3, k / 3))[0]:
        i, j, m = cand[c]
        z = ((X[i] == X[j:j + m - 1].sum(0) + rng.permuted(np.tile(X[j + m - 1], (B, 1)), axis=1)) & (X[i] > 0)).sum(1)
        pv[c] = (1 + (z >= obs[c]).sum()) / (1 + B)
    q = bh(pv)
    sig = [dict(total=f"B{cand[c][0]}", partes="+".join(f"B{x}" for x in range(cand[c][1], cand[c][1] + cand[c][2])),
                exactas=int(obs[c]), de=k, p=float(pv[c]), q=float(q[c])) for c in np.argsort(-obs) if q[c] < .05]
    datos.update(candidatos=len(cand), significativos=sig)
    a = [af(f"Totales por columna: {s['total']} = {s['partes']} en {s['exactas']} de {k} posiciones (bloques de {k} "
            f"colgantes; p={s['p']:.1e}; q BH sobre {len(cand)} candidatos del quipu={s['q']:.1e}).", "propuesto", F)
         for s in sig]
    tot = {s["total"] for s in sig}
    if any(x in tot for s in sig for x in s["partes"].split("+")):
        a.append(af("Los totales encadenan (un bloque-total es a su vez sumando de otro): tabla jerárquica de 3 niveles "
                    "o más.", "propuesto", F))
    return dict(titulo=T, datos=datos, afirmaciones=a)


DETECTORES_EXTRA.extend([alternancia, totales_columna])
