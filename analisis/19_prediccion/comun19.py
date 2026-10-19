"""Motor de prediccion ciega para el archivo de Incahuasi (carpeta 19_prediccion).

Idea: dada una cuerda "oculta" (conjunto `hide`, su valor no se lee nunca), cada regla del modelo de 13 intenta
predecirla SOLO con las demas cuerdas. Las correspondencias entre quipus (que cuerda es la copia de cual, que registro
de A+B va con que cabecera del libro) se buscan SIN mirar el valor oculto: alineacion LCS de las demas cifras y
emparejamiento por posicion en el hueco entre dos anclas (`contra`). Nada de aristas ya descubiertas del grafo.

Reglas (nombre -> relacion del informe 13):
  copia      cuerda = su copia en el quipu pareja (UR255/UR267A, UR256/UR267B, UR266/UR275, UR273A/UR274A,
             UR273B/UR274B, UR269/UR275, UR269/UR266)
  suma_AB    cabecera del libro (UR266/UR275/UR269) = A_i + B_i; y A_i = cabecera - B_i; B_i = cabecera - A_i
  fila278    cabecera del libro (UR266/UR275/UR269) = suma de la fila de UR278; y celda = cabecera - otras 8 celdas
  celda270   celda de UR278 = colgante + subsidiaria de UR270 (misma columna); y las componentes P, S = celda - otra
  cierre     cabecera de un registro = suma del resto de sus cuerdas (neto/partidas/cuota), si el quipu cierra
  cuota      cuerda en la posicion de la cuota = constante del quipu
"""
import sys
from bisect import bisect_left
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "13_sistema_incahuasi"))
import comun13 as C  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

SEED = 19
TOL = frozenset({0, 1, 10, 100, 1000, 10000})  # exacto o +-1 en un digito
TOL1 = frozenset({0, 1})                        # para sumas: solo exacto o +-1
SIS = ["UR270", "UR273A", "UR273B", "UR274A", "UR274B", "UR278", "UR266", "UR275", "UR269",
       "UR267A", "UR267B", "UR255", "UR256"]
PARES_COPIA = [("UR255", "UR267A"), ("UR256", "UR267B"), ("UR266", "UR275"), ("UR273A", "UR274A"),
               ("UR273B", "UR274B"), ("UR269", "UR275"), ("UR269", "UR266")]
LIBROS = ["UR266", "UR275", "UR269"]
SUMAS = [("UR273A", "UR273B", LIBROS), ("UR274A", "UR273B", LIBROS), ("UR267A", "UR267B", ["UR269"])]
CIERRE = ["UR275", "UR266", "UR269", "UR255", "UR256", "UR267A", "UR267B", "UR274B"]
CUOTA = ["UR266", "UR275", "UR269", "UR255", "UR256", "UR267A", "UR267B", "UR274A", "UR274B"]

_c, _q = C.archivo()
_c = _c[_c.kfg.isin(SIS)].sort_values(["kfg", "orden"]).reset_index(drop=True)
VAL, INFO, GR, ORD = {}, {}, {}, {}
for r in _c.itertuples():
    cid = (r.kfg, r.cuerda)
    VAL[cid] = int(r.valor) if r.pres and r.valor > 0 else None
    INFO[cid] = dict(nivel=int(r.nivel), grupo=int(r.grupo), color=str(r.color), pres=bool(r.pres), padre=r.padre)
    GR.setdefault(r.kfg, {}).setdefault(int(r.grupo), []).append(cid)
    ORD.setdefault(r.kfg, []).append(cid)


def kn(cid, hide):
    """Valor conocido (None si oculto o ausente)."""
    return None if (cid in hide or cid not in VAL) else VAL[cid]


def registros(k):
    """Registros de k: grupos que no son separadores rosa. Cabecera = primera colgante blanca si hay, si no la primera presente."""
    out = []
    for g, cids in sorted(GR[k].items()):
        l0 = [x for x in cids if INFO[x]["nivel"] == 0]
        pres = [x for x in l0 if INFO[x]["pres"]]
        if not pres and all(INFO[x]["color"].startswith("PK") for x in l0):
            continue  # separador rosa (los registros sin cuerdas anudadas SI cuentan, como en 13)
        blancas = [x for x in pres if INFO[x]["color"].startswith("W")]
        out.append(dict(g=g, cords=cids, l0=l0, header=(blancas or pres or [None])[0]))
    return out


REC = {k: registros(k) for k in SIS}
REC_DE = {}  # cid -> (quipu, indice de registro)
for k in SIS:
    for i, r in enumerate(REC[k]):
        for x in r["cords"]:
            REC_DE[x] = (k, i)


# ---------------------------------------------------------------- alineacion ciega
def anclas(X, Y, tol):
    """LCS de X e Y (listas de int|None; None nunca casa). Devuelve lista de pares (i, j)."""
    n, m = len(X), len(Y)
    H = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        xi, Hi, Hn = X[i], H[i], H[i + 1]
        for j in range(m):
            yj = Y[j]
            if xi is not None and yj is not None and abs(xi - yj) in tol:
                Hn[j + 1] = Hi[j] + 1
            else:
                Hn[j + 1] = Hn[j] if Hn[j] > Hi[j + 1] else Hi[j + 1]
    i, j, out = n, m, []
    while i and j:
        xi, yj = X[i - 1], Y[j - 1]
        if xi is not None and yj is not None and abs(xi - yj) in tol and H[i][j] == H[i - 1][j - 1] + 1:
            out.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif H[i - 1][j] >= H[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def contra(X, Y, i, tol):
    """Contraparte de X[i] (desconocido) en Y sin mirar su valor: ancla las demas cifras y empareja por orden
    dentro del hueco entre dos anclas si ambos huecos tienen igual longitud. Devuelve (j, longitud_hueco) o None."""
    A = anclas(X, Y, tol)
    ai = [a for a, _ in A]
    p = bisect_left(ai, i) - 1
    ap, bp = (A[p] if p >= 0 else (-1, -1))
    an, bn = (A[p + 1] if p + 1 < len(A) else (len(X), len(Y)))
    if (an - ap) != (bn - bp):
        return None
    return bp + 1 + (i - ap - 1), an - ap - 1  # (j, longitud del hueco: 1 = entre dos anclas contiguas)


# ---------------------------------------------------------------- motor
def _par(rule, via, pred, inputs, gap=0, **kw):
    return dict(rule=rule, via=via, pred=int(pred), inputs=tuple(inputs), gap=gap, **kw)


def r_copia(t, hide):
    """Copia en dos niveles: (1) registros emparejados por LCS de cabeceras; (2) dentro del registro, cuerda por posicion."""
    out = []
    k = t[0]
    if t not in REC_DE:
        return out
    _, i = REC_DE[t]
    for a, b in PARES_COPIA:
        if k not in (a, b):
            continue
        o = b if k == a else a
        HX = [kn(r["header"], hide) for r in REC[k]]
        HY = [kn(r["header"], hide) for r in REC[o]]
        rec = REC[k][i]
        if rec["header"] == t:
            X = list(HX)
            X[i] = None
            r_ = contra(X, HY, i, TOL1)
            if r_ is not None and 0 <= r_[0] < len(HY) and HY[r_[0]] is not None:
                j, gp = r_
                out.append(_par("copia", f"{o}->{k}", HY[j], [REC[o][j]["header"]], gap=gp))
            continue
        j = dict(anclas(HX, HY, TOL1)).get(i)
        if j is None:
            continue
        cx, cy = rec["cords"], REC[o][j]["cords"]
        X = [None if x in hide else kn(x, hide) for x in cx]
        Y = [kn(y, hide) for y in cy]
        p = cx.index(t)
        r_ = contra(X, Y, p, TOL1)
        if r_ is not None and 0 <= r_[0] < len(Y) and Y[r_[0]] is not None:
            q, gp = r_
            out.append(_par("copia", f"{o}->{k}", Y[q], [cy[q]], gap=gp))
    return out


def _cabs(k, hide):
    """Cabeceras (cid, valor|None) de los registros de k con cabecera >=100 conocida o desconocida."""
    return [(r["header"], kn(r["header"], hide)) for r in REC[k]]


def _suma_lista(ka, kb, hide):
    """Registros emparejados (por orden) de A y B: lista de (ha, hb, S|None)."""
    ra, rb = REC[ka], REC[kb]
    L = []
    for x, y in zip(ra, rb):
        va, vb = kn(x["header"], hide), kn(y["header"], hide)
        L.append((x["header"], y["header"], va + vb if va is not None and vb is not None else None))
    return L


def r_suma(t, hide):
    out = []
    for ka, kb, destinos in SUMAS:
        L = _suma_lista(ka, kb, hide)
        S = [s for _, _, s in L]
        for K in destinos:
            cab = _cabs(K, hide)
            Hv = [v for _, v in cab]
            # t es cabecera de A o B -> predice A = H - B
            for i, (ha, hb, s) in enumerate(L):
                if t in (ha, hb):
                    otro = hb if t == ha else ha
                    vo = kn(otro, hide)
                    if vo is None:
                        continue
                    X = list(S)
                    X[i] = None
                    r_ = contra(X, Hv, i, TOL1)
                    if r_ is not None and 0 <= r_[0] < len(Hv) and Hv[r_[0]] is not None:
                        j, gp = r_
                        out.append(_par("suma_AB", f"{ka}+{kb}:{K}", Hv[j] - vo, [cab[j][0], otro], gap=gp))
            # t es cabecera del libro -> predice S_i
            idx = [i for i, (h, _) in enumerate(cab) if h == t]
            if idx:
                j = idx[0]
                X = list(Hv)
                X[j] = None
                r_ = contra(X, S, j, TOL1)
                if r_ is not None and 0 <= r_[0] < len(S) and S[r_[0]] is not None:
                    i, gp = r_
                    out.append(_par("suma_AB", f"{ka}+{kb}:{K}", S[i], [L[i][0], L[i][1]], gap=gp))
    return out


def _filas278(hide):
    """Filas de UR278: (g, cords nivel 0, total|None, completa)."""
    rows = []
    for r in REC["UR278"]:
        l0 = r["l0"]
        if sum(INFO[x]["pres"] for x in l0) < 2:
            continue
        v = [kn(x, hide) for x in l0]
        rows.append((r["g"], l0, sum(v) if all(a is not None for a in v) else None))
    return rows


def r_fila278(t, hide):
    out = []
    rows = _filas278(hide)
    T = [tt for _, _, tt in rows]
    for K in LIBROS:
        cab = _cabs(K, hide)
        Hv = [v for _, v in cab]
        # t es celda de UR278
        for ri, (g, l0, tt) in enumerate(rows):
            if t in l0:
                otros = [kn(x, hide) for x in l0 if x != t]
                if any(o is None for o in otros) or len(l0) < 7:
                    continue
                X = list(T)
                X[ri] = None
                r_ = contra(X, Hv, ri, TOL1)
                if r_ is not None and 0 <= r_[0] < len(Hv) and Hv[r_[0]] is not None:
                    j, gp = r_
                    out.append(_par("fila278", f"UR278->{K}", Hv[j] - sum(otros), [cab[j][0]] + [x for x in l0 if x != t], gap=gp))
        # t es cabecera del libro
        idx = [i for i, (h, _) in enumerate(cab) if h == t]
        if idx:
            j = idx[0]
            X = list(Hv)
            X[j] = None
            r_ = contra(X, T, j, TOL1)
            if r_ is not None and 0 <= r_[0] < len(T) and T[r_[0]] is not None:
                i, gp = r_
                out.append(_par("fila278", f"UR278->{K}", T[i], rows[i][1], gap=gp))
    return out


def _g270(hide):
    """Grupos de UR270: g -> lista por columna de (Pcid, Scid|None)."""
    G = {}
    for r in REC["UR270"]:
        cols = []
        for x in r["l0"]:
            s = (x[0], x[1] + "s1")
            cols.append((x, s if s in VAL else None))
        G[r["g"]] = cols
    return G


G270 = _g270(set())
MINC = 4  # columnas coincidentes minimas para identificar la fila contraparte


def _ps(col, hide):
    p, s = col
    vp, vs = kn(p, hide), (kn(s, hide) if s else None)
    return vp + vs if vp is not None and vs is not None else None


def _mejor(vec, cands, excl, hide, getter):
    """Mejor candidato por nº de columnas k != excl con |vec[k]-cand[k]|<=1; exige >=MINC y unicidad."""
    mejores = []
    for key, cv in cands:
        n = 0
        for k in range(min(len(vec), len(cv))):
            if k == excl or vec[k] is None or cv[k] is None:
                continue
            n += abs(vec[k] - cv[k]) <= 1
        mejores.append((n, key))
    mejores.sort(reverse=True)
    if not mejores or mejores[0][0] < MINC or (len(mejores) > 1 and mejores[1][0] == mejores[0][0]):
        return None
    return mejores[0][1]


def r_celda270(t, hide):
    out = []
    rows278 = {r["g"]: r["l0"] for r in REC["UR278"]}
    if t[0] == "UR278":
        info = REC_DE.get(t)
        if not info:
            return out
        g = REC[info[0]][info[1]]["g"]
        l0 = rows278[g]
        if t not in l0:
            return out
        j = l0.index(t)
        vec = [kn(x, hide) for x in l0]
        cands = [(gg, [_ps(c, hide) for c in cols]) for gg, cols in G270.items()]
        best = _mejor(vec, cands, j, hide, None)
        if best is not None and j < len(G270[best]):
            p, s = G270[best][j]
            vp, vs = kn(p, hide), (kn(s, hide) if s else None)
            if vp is not None and vs is not None:
                out.append(_par("celda270", "UR270->UR278", vp + vs, [p, s]))
    elif t[0] == "UR270":
        for g, cols in G270.items():
            for j, (p, s) in enumerate(cols):
                if t not in (p, s):
                    continue
                otro = s if t == p else p
                vo = kn(otro, hide) if otro else None
                if vo is None:
                    continue
                vec = [_ps(c, hide) for c in cols]
                cands = [(gg, [kn(x, hide) for x in l0]) for gg, l0 in rows278.items()]
                best = _mejor(vec, cands, j, hide, None)
                if best is not None and j < len(rows278[best]):
                    cel = rows278[best][j]
                    vc = kn(cel, hide)
                    if vc is not None:
                        out.append(_par("celda270", "UR278->UR270", vc - vo, [cel, otro]))
    return out


def tasa_cierre(k, hide, excl_rec=None):
    ok = n = 0
    for i, r in enumerate(REC[k]):
        if i == excl_rec:
            continue
        v = [kn(x, hide) for x in r["cords"]]
        if len(v) < 3 or any(a is None for a in v) or r["header"] not in r["cords"]:
            continue
        h = kn(r["header"], hide)
        n += 1
        ok += abs(h - (sum(v) - h)) <= 1
    return (ok / n if n >= 4 else 0.0), n


def r_cierre(t, hide):
    k = t[0]
    if k not in CIERRE or t not in REC_DE:
        return []
    _, i = REC_DE[t]
    r = REC[k][i]
    if r["header"] is None:
        return []
    rate, n = tasa_cierre(k, hide, i)
    if rate < 0.5:
        return []
    otros = [x for x in r["cords"] if x != t]
    vals = [kn(x, hide) for x in otros]
    if any(v is None for v in vals) or len(otros) < 2:
        return []
    if t == r["header"]:
        pred = sum(vals)
    else:
        h = kn(r["header"], hide)
        pred = h - (sum(vals) - h)
    if pred <= 0:
        return []
    return [_par("cierre", f"{k}", pred, otros, tasa=round(rate, 2))]


def ctx_cuota(k, hide):
    """(c*, indice*) de la cuota del quipu k a partir de las cuerdas conocidas (indice = posicion entre las colgantes)."""
    cnt, pos = Counter(), {}
    for r in REC[k]:
        for ix, x in enumerate(r["l0"]):
            v = kn(x, hide)
            if ix >= 1 and v is not None and v < 300:
                cnt[v] += 1
                pos.setdefault(v, Counter())[ix] += 1
    if not cnt:
        return None
    c, nc = cnt.most_common(1)[0]
    if nc < 5:
        return None
    return c, pos[c].most_common(1)[0][0]


def r_cuota(t, hide):
    k = t[0]
    if k not in CUOTA or t not in REC_DE:
        return []
    _, i = REC_DE[t]
    r = REC[k][i]
    if t not in r["l0"]:
        return []
    cx = ctx_cuota(k, hide)
    if cx and r["l0"].index(t) == cx[1]:
        return [_par("cuota", k, cx[0], [])]
    return []


REGLAS = [r_copia, r_suma, r_fila278, r_celda270, r_cierre, r_cuota]


def predecir(t, hide=None):
    hide = {t} if hide is None else hide
    out = []
    for f in REGLAS:
        out += f(t, hide)
    return out


def metricas(pred, real):
    d = abs(int(pred) - int(real))
    rel = d / real if real else np.nan
    return dict(exacta=d == 0, d1=d <= 1, tol=d in TOL, r1=rel <= 0.01, r5=rel <= 0.05, rel=rel)


def presentes():
    return [x for x in VAL if VAL[x] is not None]


def rol(t):
    """cabecera = primera colgante blanca del registro; interna = cualquier otra cuerda (celda, neto, partida, cuota...)."""
    if t in REC_DE:
        k, i = REC_DE[t]
        if REC[k][i]["header"] == t:
            return "cabecera"
    return "interna"
