"""33 · Familias de copias: alineamiento en estrella, errores conjuntivos/separativos, compatibilidad
de particiones, dirección de copia (aritmética interna, omisiones, daño), cruces de museo/sitio/
transcriptor, KFG frente a OKR, géneros del atlas (E→C) y publicación previa.
Uso: python 03_familias.py   (tras 01 y 02, fase todo)
Salidas: familias.csv, variantes.csv, direccion.csv, pares_copia.csv, estemas.md, salida_03.txt"""
import itertools
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy import stats

from comun import OUT, RAIZ, preparar

sys.stdout.reconfigure(encoding="utf-8")
FUENTES = [os.path.join(RAIZ, 'analisis/fuentes_txt'), os.path.join(RAIZ, 'docs/fichas')]
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s); print(s)


# ------------------------------------------------------------------ aritmética interna
def cierra(s, i, v):
    """¿El valor v en la fila i del quipu s cierra una suma interna? (diseño §8.1)"""
    if v <= 0:
        return False
    cu = s.cuerda.values[i]
    hijos = s[s.padre == cu]
    if len(hijos) >= 2 and hijos.v.sum() == v:
        return True                                     # colgante = Σ subsidiarias
    pad = s.padre.values[i]
    if isinstance(pad, str):
        her = s[s.padre == pad]
        p = s[s.cuerda == pad]
        if len(her) >= 2 and len(p) and her.v.sum() - s.v.values[i] + v == p.v.values[0]:
            return True                                 # sumando de su colgante
    pend = s[s.nivel == 0]
    if s.nivel.values[i] != 0:
        return False
    vals = pend.v.values.copy()
    pos = np.where(pend.index.values == s.index.values[i])[0][0]
    vals[pos] = v
    for L in range(2, 13):                              # cuerda = Σ contigua antes / después
        for a, b in ((pos - L, pos), (pos + 1, pos + 1 + L)):
            if a >= 0 and b <= len(vals) and (vals[a:b] > 0).sum() >= 2 and vals[a:b].sum() == v:
                return True
    for L in range(2, 13):                              # sumando de una cuerda vecina que cierra
        for st in range(max(0, pos - L + 1), pos + 1):
            en = st + L
            if en > len(vals):
                continue
            t = vals[st:en].sum()
            for c in (st - 1, en):
                if 0 <= c < len(vals) and vals[c] == t and (vals[st:en] > 0).sum() >= 2:
                    return True
    return False


def _demo():
    s = pd.DataFrame(dict(cuerda=['p1', 'p2', 'p3', 'p4', 'p4s1', 'p4s2'], v=[30, 10, 20, 12, 5, 7],
                          nivel=[0, 0, 0, 0, 1, 1], padre=[None, None, None, None, 'p4', 'p4']))
    assert cierra(s, 0, 30) and not cierra(s, 0, 31)
    assert cierra(s, 1, 10) and cierra(s, 3, 12) and cierra(s, 4, 5) and not cierra(s, 4, 6)


# ------------------------------------------------------------------ publicación previa
def alias(k):
    """Patrones regex de un identificador y sus alias (UR1xxx = ASxxx; ceros a la izquierda opcionales:
    las fuentes escriben UR6, UR 66, AS114)."""
    out = []
    m = re.match(r'([A-Z]+)(\d+)([A-Z]?)$', k)
    if not m:
        return [re.escape(k)]
    pre, num, suf = m[1], int(m[2]), m[3]
    formas = [(pre, num)]
    if pre == 'UR' and 1000 <= num < 2000:
        formas.append(('AS', num - 1000))
    if pre == 'AS':
        formas.append(('UR', num + 1000))
    for pr, n in formas:
        out.append(rf'\b{pr}\s?0*{n}\s?{suf}\b' if suf else rf'\b{pr}\s?0*{n}(?![A-Za-z0-9])')
    return out


def textos():
    t = {}
    for d in FUENTES:
        for r, _, fs in os.walk(d):
            for f in fs:
                if f.endswith(('.txt', '.md')):
                    t[os.path.relpath(os.path.join(r, f), RAIZ)] = open(os.path.join(r, f), encoding='utf-8',
                                                                        errors='ignore').read()
    return t


def publicado(a, b, T, ventana=600):
    """Fuentes donde aparecen los dos identificadores (o alias) a menos de `ventana` caracteres."""
    pa = [re.compile(x) for x in alias(a)]
    pb = [re.compile(x) for x in alias(b)]
    hits = []
    for f, s in T.items():
        ia = [m.start() for p in pa for m in p.finditer(s)]
        ib = [m.start() for p in pb for m in p.finditer(s)]
        if ia and ib and min(abs(x - y) for x in ia for y in ib) <= ventana:
            hits.append(f)
    return hits


# ------------------------------------------------------------------ OKR
def okr_meta():
    con = sqlite3.connect('file:' + os.path.join(RAIZ, 'data/external/open-khipu-repository/data/khipu.db') +
                          '?mode=ro', uri=True)
    km = pd.read_sql('select KHIPU_ID, INVESTIGATOR_NUM, MUSEUM_NUM, CREATED_BY from khipu_main', con)
    cb = pd.read_sql('select KHIPU_ID, CREATED_BY, count(*) n from cord group by 1, 2', con)
    cb = cb.sort_values('n').groupby('KHIPU_ID').CREATED_BY.last()
    vals = pd.read_sql('select c.KHIPU_ID, c.CORD_ID, sum(k.knot_value_type) v from knot k join cord c '
                       'on k.CORD_ID = c.CORD_ID group by 1, 2', con)
    pu = pd.read_csv(os.path.join(RAIZ, 'analisis/17_okr_pendientes/puente.csv'))
    pu = pu[pu.khipu_id.notna()].drop_duplicates('kfg').set_index('kfg')
    return km.set_index('KHIPU_ID'), cb, {k: Counter(g.v.astype(int)) for k, g in vals.groupby('KHIPU_ID')}, pu


def main():
    _demo()
    D = preparar()
    S = D['seqs']
    q = pd.read_csv(os.path.join(RAIZ, 'analisis/datos/quipus.csv')).set_index('kfg')
    atlas = pd.read_csv(os.path.join(RAIZ, 'analisis/28_atlas_generos/atlas.csv')).set_index('kfg')
    mitad = pd.read_csv(os.path.join(OUT, 'division.csv')).set_index('kfg').mitad
    P = pd.read_csv(os.path.join(OUT, 'pares_detalle_todo.csv'))
    C = pd.read_csv(os.path.join(OUT, 'celdas_alineadas_todo.csv'), low_memory=False)
    T = textos()
    km, cbmode, okrvals, pu = okr_meta()

    def proyecto(a, b):
        f = []
        s04 = pd.read_csv(os.path.join(RAIZ, 'analisis/04_concordancias/resultados/pares_significativos.csv'))
        if ((s04.A == a) & (s04.B == b)).any() or ((s04.A == b) & (s04.B == a)).any():
            f.append('04')
        sint = open(os.path.join(RAIZ, 'analisis/SINTESIS.md'), encoding='utf-8').read()
        if re.search(re.escape(a) + r'.{0,40}' + re.escape(b), sint) or re.search(re.escape(b) + r'.{0,40}' + re.escape(a), sint):
            f.append('SINTESIS')
        s09 = pd.read_csv(os.path.join(RAIZ, 'analisis/09_incahuasi/pares_corpus.csv'))
        s09 = s09[s09.p_bonf < .05]
        if (((s09.a == a) & (s09.b == b)) | ((s09.a == b) & (s09.b == a))).any():
            f.append('09 (valores compartidos, sin analizar)')
        return f

    # ---------------- post hoc sin orden (05): pares q_comb < 0,05 que el barrido no da como copia
    OL = pd.read_csv(os.path.join(OUT, 'orden_libre.csv'))
    OL = OL[OL.q_comb < .05]
    ya = {frozenset(x) for x in zip(P[P.nivel.isin(['demostrado', 'apoyado'])].A, P[P.nivel.isin(['demostrado', 'apoyado'])].B)}
    ph = []
    for _, x in OL.iterrows():
        if frozenset((x.A, x.B)) in ya:
            continue
        m = ((P.A == x.A) & (P.B == x.B)) | ((P.A == x.B) & (P.B == x.A))
        if m.any():  # el par ya tenía alineamiento del barrido: conservar orientación y escala
            x = x.copy(); old = P[m].iloc[0]; x['A'], x['B'] = old.A, old.B
        esc = float(P[m].escala.iloc[0]) if m.any() else 1.0
        P = P[~m]
        ph.append(dict(A=x.A, B=x.B, escala=esc, score=x.K, p=x.p_comb, q=x.q_comb, holm=np.nan, mismo_objeto=False,
                       transformacion=f'sin orden: {x.K} valores ≥100 compartidos, {x.L_orden} en el mismo orden',
                       alineadas=x.K, exactas=x.K, rt_pasa=np.nan,
                       nivel='apoyado (post hoc)' if (x.q < .05 and x.q_orden < .05) else 'propuesto (post hoc)'))
    P = pd.concat([P, pd.DataFrame(ph)], ignore_index=True)

    # ---------------- pares: publicación, cruces
    filas = []
    for _, x in P.iterrows():
        pub = publicado(x.A, x.B, T)
        lit = [h for h in pub if 'fuentes_txt' in h or ('fichas' in h and not os.path.basename(h).startswith('repo'))]
        pro = proyecto(x.A, x.B)
        filas.append(dict(publicado_antes='co-mención en literatura' if lit else ('solo en el proyecto' if pro else 'no'),
                          fuente='; '.join(lit + pro)))
    P = pd.concat([P, pd.DataFrame(filas)], axis=1)
    # Publicadas COMO copia o concordancia (verificado leyendo el pasaje; la co-mención sola no basta).
    PUB = {('UR006', 'UR009'): 'Urton 2005 (UR6/UR9/UR21)', ('UR006', 'UR021'): 'Urton 2005 (UR6/UR9/UR21)',
           ('UR009', 'UR021'): 'Urton 2005 (UR6/UR9/UR21)', ('UR1114', 'UR1123'): 'Urton 2005 (AS114/AS123)',
           ('AS159', 'AS173'): 'Urton 2005', ('UR064', 'UR068'): 'Urton y Brezine 2005; Urton 2017 cap. 5 (nivel II)',
           ('UR066', 'UR067'): 'Urton y Brezine 2005 («identical numerical values»)',
           ('UR053B', 'UR053C'): 'Urton 2017 cap. 8 («matching khipus»)',
           ('UR255', 'UR267A'): 'Urton y Chu 2015; Urton 2017', ('UR256', 'UR267B'): 'Urton y Chu 2015; Urton 2017',
           ('UR266', 'UR275'): 'Urton 2017 cap. 9 (18/43 exactas)'}
    PUB = {frozenset(k): v for k, v in PUB.items()}
    for i, x in P.iterrows():
        s = PUB.get(frozenset((x.A, x.B)))
        if s:
            P.loc[i, 'publicado_antes'] = 'sí, como copia/concordancia'
            P.loc[i, 'fuente'] = s + ('; ' + x.fuente if x.fuente else '')
            # §7: el equipo rojo es para pares NUEVOS; en los publicados el nivel lo dan Holm/BH
            if x.nivel == 'propuesto' and x.q < .05:
                P.loc[i, 'nivel'] = 'demostrado' if x.holm < .05 else 'apoyado'
            elif str(x.nivel).startswith('propuesto (post hoc)'):
                P.loc[i, 'nivel'] = 'apoyado (post hoc)'
    APOY = ['demostrado', 'apoyado', 'apoyado (post hoc)']

    def museo_norm(m):
        m = str(m).lower()
        for clave, nombre in (('berlin', 'Berlín'), ('incahuasi', 'Incahuasi'), ('puruchuco', 'Puruchuco'),
                              ('arqueolog', 'MNAAHP Lima'), ('pueblo libre', 'MNAAHP Lima'), ('branly', 'París'),
                              ('homme', 'París'), ('basel', 'Basilea'), ('goteborg', 'Gotemburgo'),
                              ('worldculture', 'Gotemburgo'), ('mallqui', 'Leymebamba'), ('banco central', 'BCRP Lima'),
                              ('peabody', 'Peabody'), ('dallas', 'Dallas'), ('lowe', 'Miami'),
                              ('temple radicati', 'Temple Radicati Lima'), ('american museum', 'AMNH')):
            if clave in m:
                return nombre
        return 'desconocido' if m in ('unknown', 'nan', '') else m

    def serie(k):
        # serie de registro = investigador: UR1xxx son registros de Ascher volcados en la serie UR (04, 14)
        return 'AS' if re.match(r'UR1\d{3}', k) else re.match(r'[A-Z]+', k)[0]

    def meta(k):
        kid = pu.khipu_id.get(k)
        r = km.loc[int(kid)] if kid == kid and kid is not None and int(kid) in km.index else None
        return dict(museo=museo_norm(q.museo.get(k)), procedencia=q.procedencia.get(k), prefijo=serie(k),
                    investigador=None if r is None else r.INVESTIGATOR_NUM,
                    inventario=None if r is None else r.MUSEUM_NUM,
                    creado_por=None if r is None else r.CREATED_BY,
                    cuerdas_por=cbmode.get(int(kid)) if kid == kid and kid is not None else None,
                    genero=atlas.genero.get(k), mitad=mitad.get(k), khipu_id=kid)
    M = {k: meta(k) for k in set(P.A) | set(P.B)}
    for lado in 'AB':
        for c in ('museo', 'procedencia', 'prefijo', 'creado_por', 'cuerdas_por', 'genero', 'inventario'):
            P[f'{c}_{lado}'] = P[lado].map(lambda k: M[k][c])
    P['cruza_museo'] = (P.museo_A != P.museo_B) & (P.museo_A != 'desconocido') & (P.museo_B != 'desconocido')
    conoc = lambda s: s.notna() & ~s.isin(['Unknown', 'unknown', 'Peru', 'South Peru', ''])
    P['sitios_distintos'] = conoc(P.procedencia_A) & conoc(P.procedencia_B) & (P.procedencia_A != P.procedencia_B)
    P['cruza_transcriptor'] = P.prefijo_A != P.prefijo_B
    P['cruza_capturista'] = P.cuerdas_por_A.notna() & P.cuerdas_por_B.notna() & (P.cuerdas_por_A != P.cuerdas_por_B)

    # ---------------- KFG frente a OKR
    def kfg_okr(k):
        kid = M[k]['khipu_id'] if k in M else pu.khipu_id.get(k)
        if kid != kid or kid is None or int(kid) not in okrvals:
            return np.nan
        a = Counter(S[k].v.astype(int)); b = okrvals[int(kid)]
        return sum((a & b).values()) / max(1, sum(a.values()))
    sig = P[P.nivel.isin(APOY)].copy()
    miembros = sorted(set(sig.A) | set(sig.B))
    ko = {k: kfg_okr(k) for k in miembros}
    log('KFG≈OKR (fracción del multiconjunto de valores de KFG presente en OKR), miembros de familias:')
    log(pd.Series(ko).describe().to_string())

    # ---------------- familias
    obj = sig[sig.mismo_objeto.fillna(False).astype(bool)]
    nodo = {k: k for k in miembros}
    for _, x in obj.iterrows():
        nodo[x.B] = nodo[x.A] = min(nodo[x.A], nodo[x.B])
    par = {k: k for k in miembros}

    def raiz(k):
        while par[k] != k:
            k = par[k]
        return k
    for _, x in sig.iterrows():
        par[raiz(x.A)] = raiz(x.B)
    fam = defaultdict(list)
    for k in miembros:
        fam[raiz(k)].append(k)
    fams = sorted(fam.values(), key=lambda m: (-len(m), m))
    famid = {k: f'F{n + 1:02d}' for n, m in enumerate(fams) for k in m}
    P['familia'] = [famid.get(a) if famid.get(a) == famid.get(b) else None for a, b in zip(P.A, P.B)]

    estemas, variantes_all, direcciones, famrows = [], [], [], []
    for n, m in enumerate(fams):
        fid = f'F{n + 1:02d}'
        E = sig[sig.A.isin(m) & sig.B.isin(m)]
        tot = Counter()
        for _, x in E.iterrows():
            tot[x.A] += x.alineadas + 1; tot[x.B] += x.alineadas + 1
        centro = tot.most_common(1)[0][0]
        # proyección en estrella sobre el centro (escala ya aplicada: se compara valor transformado)
        cols = {}
        span = {}
        for _, x in E.iterrows():
            if centro not in (x.A, x.B):
                continue
            otro = x.B if x.A == centro else x.A
            c = C[(C.A == x.A) & (C.B == x.B)]
            if c.empty:
                continue
            ic, io = ('i', 'j') if x.A == centro else ('j', 'i')
            vo = c.vB if x.A == centro else c.vA
            k = x.escala if x.A == centro else 1 / x.escala
            vo = (vo * k).round().astype(int)
            for a_, b_, v in zip(c[ic], c[io], vo):
                cols.setdefault(int(a_), {})[otro] = (int(b_), int(v))
            span[otro] = (c[ic].min(), c[ic].max())
        testigos = [centro] + sorted(span)
        sc = S[centro]
        filasV = []
        for i in range(len(sc)):
            if not any(lo <= i <= hi for lo, hi in span.values()):
                continue
            lect = {centro: int(sc.v.values[i])}
            for t in span:
                lo, hi = span[t]
                if lo <= i <= hi:
                    lect[t] = cols.get(i, {}).get(t, (None, '—'))[1]
            if len(lect) >= 2:
                filasV.append(dict(familia=fid, cuerda_centro=sc.cuerda.values[i], nivel=int(sc.nivel.values[i]),
                                   rota_centro=sc.terminacion.values[i] == 'B', **{t: lect.get(t) for t in testigos}))
        V = pd.DataFrame(filasV)
        var = V[V[testigos].apply(lambda r: len(set(x for x in r if x is not None and x == x)) > 1, axis=1)] if len(V) else V
        variantes_all.append(var)
        # particiones (≥3 testigos presentes)
        # Lachmann: solo columnas con ≥ 3 lecturas NUMÉRICAS (las omisiones «—» se cuentan aparte)
        norm = lambda v: v if isinstance(v, str) else str(int(v))
        splits = Counter(); conj, sep = Counter(), Counter(); omis_c = Counter()
        for _, r in V.iterrows():
            pres = {t: norm(r[t]) for t in testigos if r[t] is not None and r[t] == r[t]}
            for t in pres:
                omis_c[t] += pres[t] == '—'
            num = {t: v for t, v in pres.items() if v != '—'}
            if len(num) < 3 or len(set(num.values())) == 1:
                continue
            cnt = Counter(num.values())
            mayor, nmay = cnt.most_common(1)[0]
            unica_mayoria = list(cnt.values()).count(nmay) == 1
            for val, c in cnt.items():
                g = frozenset(t for t in num if num[t] == val)
                if c == 1 and unica_mayoria and nmay >= 2:
                    sep[next(iter(g))] += 1            # separativo: lectura singular frente al acuerdo
                elif c >= 2 and val != mayor:
                    conj[g] += 1                        # conjuntivo: lectura minoritaria compartida
            parts = frozenset(frozenset(t for t in num if num[t] == val) for val in cnt)
            splits[parts] += 1
        incompat = 0
        biparts = [p for p in splits if len(p) == 2 and min(len(g) for g in p) >= 2]
        for p1, p2 in itertools.combinations(biparts, 2):
            a1, a2 = sorted(p1, key=sorted)[0], sorted(p2, key=sorted)[0]
            if a1 & a2 and a1 - a2 and a2 - a1 and (a1 | a2) != frozenset().union(*p1):
                incompat += 1                           # cuatro gametos: contaminación o coincidencia
        # distancias por par (fracción de lecturas numéricas distintas donde ambos tienen lectura)
        dist = {}
        for t1, t2 in itertools.combinations(testigos, 2):
            sh = V[[t1, t2]].dropna() if len(V) else pd.DataFrame()
            if len(sh):
                a_, b_ = sh[t1].map(norm), sh[t2].map(norm)
                m_ = (a_ != '—') & (b_ != '—')
                dist[(t1, t2)] = (round((a_[m_] != b_[m_]).mean(), 3) if m_.any() else None, int(m_.sum()))
            else:
                dist[(t1, t2)] = (None, 0)
        # dirección por par en la familia
        for _, x in E.iterrows():
            c = C[(C.A == x.A) & (C.B == x.B)]
            if c.empty:
                direcciones.append(dict(familia=fid, A=x.A, B=x.B, veredicto='sin alineamiento (post hoc)'))
                continue
            sA, sB = S[x.A], S[x.B]
            k = x.escala
            vbt = (c.vB * k).round().astype(int)
            dif = c[(c.vA != vbt)]
            eA = eB = cA = cB = dano = 0
            for ii, rr in dif.iterrows():
                rotaA, rotaB = rr.termA == 'B', rr.termB == 'B'
                vb_ = int(round(rr.vB * k))
                if (rotaA and rr.vA < vb_) or (rotaB and vb_ < rr.vA):
                    dano += 1
                    continue
                okA, okB = cierra(sA, int(rr.i), int(rr.vA)), cierra(sB, int(rr.j), int(rr.vB))
                eA += okB and not okA; eB += okA and not okB; cA += okA; cB += okB
            # omisión de capa / cuerdas dentro del tramo alineado
            def omis(s, idx):
                lo, hi = idx.min(), idx.max()
                tramo = s.iloc[lo:hi + 1]
                fuera = tramo[~tramo.index.isin(idx)]
                return len(fuera), int((fuera.nivel > 0).sum())
            oA, osA = omis(sA, c.i.values); oB, osB = omis(sB, c.j.values)
            crit = []
            if eA != eB and max(eA, eB) >= 2:
                crit.append(x.A if eB > eA else x.B)          # el que cierra más = original
            if abs(oA - oB) >= 3 and abs(oA - oB) >= .1 * len(c):
                crit.append(x.A if oA > oB else x.B)          # el que tiene contenido extra en el tramo = completo
            if len(crit) == 2 and crit[0] == crit[1]:
                orig = crit[0]; veredicto = f'{orig} → {x.B if orig == x.A else x.A}'
            else:
                veredicto = 'sin dirección'
            direcciones.append(dict(familia=fid, A=x.A, B=x.B, variantes_valor=len(dif), dano=dano,
                                    cierra_A=cA, cierra_B=cB, errores_aritmeticos_A=eA, errores_aritmeticos_B=eB,
                                    extra_en_A=oA, extra_subs_A=osA, extra_en_B=oB, extra_subs_B=osB,
                                    criterios='|'.join(crit), veredicto=veredicto))
        famrows.append(dict(familia=fid, n=len(m), miembros=' '.join(m), centro=centro,
                            museos=len({M[k]['museo'] for k in m}), sitios=len({M[k]['procedencia'] for k in m}),
                            transcriptores=' '.join(sorted({f"{M[k]['prefijo']}/{M[k]['cuerdas_por']}" for k in m})),
                            generos=' '.join(f"{k}:{M[k]['genero']}" for k in m), variantes=len(var),
                            splits=len(splits), incompatibles=incompat))
        estemas.append((fid, m, centro, testigos, E, var, splits, conj, sep, incompat, dist, omis_c))

    F = pd.DataFrame(famrows)
    F.to_csv(os.path.join(OUT, 'familias.csv'), index=False)
    Dd = pd.DataFrame(direcciones)
    Dd.to_csv(os.path.join(OUT, 'direccion.csv'), index=False)
    if variantes_all:
        pd.concat(variantes_all).to_csv(os.path.join(OUT, 'variantes.csv'), index=False)
    log(F.to_string()); log(Dd.to_string())

    # ---------------- estemas.md (borrador automático; el texto interpretativo va en informe.md)
    w = ['# Estemas (salida automática de 03_familias.py)', '',
         'Notación: `A → B` = B deriva de A (solo con ≥ 2 criterios coincidentes); `A — B` = relación sin dirección; '
         '`A = B` = el mismo objeto leído dos veces. Lecturas en la escala del testigo central.', '']
    for fid, m, centro, testigos, E, var, splits, conj, sep, incompat, dist, omis_c in estemas:
        w.append(f'## {fid}: {", ".join(m)}')
        w.append(f'Centro del alineamiento: {centro}. Variantes: {len(var)}. Particiones informativas: {len(splits)}; '
                 f'incompatibles (contaminación o coincidencia): {incompat}.')
        w.append('```')
        for _, x in E.iterrows():
            d = Dd[(Dd.A == x.A) & (Dd.B == x.B)].veredicto
            rel = '=' if x.mismo_objeto is True else ('→' if (not d.empty and ' → ' in str(d.iloc[0])) else '—')
            a, b = x.A, x.B
            if rel == '→':
                a, b = d.iloc[0].split(' → ')
            w.append(f'{a:>8} {rel} {b:<8}  [{x.transformacion}; {x.exactas}/{x.alineadas} exactas; q={x.q:.1e}; {x.nivel}]')
        w.append('```')
        if len(testigos) >= 3:
            w.append('Patrones de lectura en columnas con ≥ 3 lecturas numéricas: ' + '; '.join(
                ' | '.join('+'.join(sorted(g)) for g in sorted(p, key=sorted)) + f' ×{c}' for p, c in splits.most_common(8)))
            w.append('Omisiones dentro del tramo de cada testigo: ' + ', '.join(f'{t} {omis_c.get(t, 0)}' for t in testigos))
            w.append('Errores separativos (lectura singular frente al acuerdo de ≥ 2): ' +
                     ', '.join(f'{t} {sep.get(t, 0)}' for t in testigos))
            w.append('Errores conjuntivos (lectura minoritaria compartida por ≥ 2): ' +
                     (', '.join(f"{'+'.join(sorted(g))} {c}" for g, c in conj.most_common(6)) or 'ninguno'))
            w.append('Distancias (fracción de lecturas distintas, n columnas): ' +
                     '; '.join(f'{a}–{b} {d[0]} (n={d[1]})' for (a, b), d in dist.items()))
        w.append('')
    open(os.path.join(OUT, 'estemas_auto.md'), 'w', encoding='utf-8').write('\n'.join(w))

    # ---------------- pares_copia.csv
    out = P[P.nivel != 'ninguno'].copy()
    out['nivel_out'] = np.where(out.mismo_objeto.fillna(False).astype(bool) & out.nivel.isin(['demostrado', 'apoyado']),
                                'mismo objeto (' + out.nivel + ')', out.nivel)
    pc = out.rename(columns={'A': 'kfg_a', 'B': 'kfg_b', 'score': 'similitud'})[
        ['kfg_a', 'kfg_b', 'transformacion', 'similitud', 'p', 'q', 'holm', 'nivel_out', 'publicado_antes', 'fuente',
         'familia', 'alineadas', 'exactas', 'tolerantes', 'discordantes', 'r_largo', 'p_sin_comunes', 'p_bloques',
         'cruza_museo', 'sitios_distintos', 'cruza_transcriptor', 'cruza_capturista', 'prefijo_A', 'prefijo_B', 'museo_A', 'museo_B', 'procedencia_A',
         'procedencia_B', 'cuerdas_por_A', 'cuerdas_por_B', 'genero_A', 'genero_B']].rename(columns={'nivel_out': 'nivel'})
    pc.to_csv(os.path.join(OUT, 'pares_copia.csv'), index=False, float_format='%.3g')

    # ---------------- sistema: cruces y géneros (E → C)
    S2 = P[P.nivel.isin(APOY) & ~P.mismo_objeto.fillna(False).astype(bool)]
    log('\nPares copia (sin mismo objeto):', len(S2), '| cruzan museo:', int(S2.cruza_museo.sum()),
        '| sitios conocidos distintos:', int(S2.sitios_distintos.sum()), '| cruzan serie de investigador:', int(S2.cruza_transcriptor.sum()), '| cruzan capturista OKR:', int(S2.cruza_capturista.sum()))
    r = pd.read_csv(os.path.join(OUT, 'barrido_todo.csv.gz'))
    qq = pd.read_csv(os.path.join(RAIZ, 'analisis/datos/quipus.csv')).set_index('kfg').procedencia
    ids = np.array(D['ids'])
    kn = pd.Series(qq.reindex(ids).values, index=ids)
    known = kn[~kn.isin(['Unknown', 'Peru', 'South Peru']) & kn.notna()]
    vc = known.value_counts()
    n_dist = (len(known) ** 2 - (vc ** 2).sum()) // 2
    log(f'Nulo de sitios distintos: {int(S2.sitios_distintos.sum())} pares copia entre {n_dist} pares de sitios conocidos distintos;'
        f' {int((S2.procedencia_A == S2.procedencia_B).sum())} dentro del mismo sitio entre {int(((vc * (vc - 1)) // 2).sum())} pares')
    inv = pd.Series(0, index=ids)
    for _, x in S2.iterrows():
        inv[x.A] = 1; inv[x.B] = 1
    g = atlas.genero.reindex(ids)
    h = mitad.reindex(ids)
    res = []
    for gen in sorted(g.dropna().unique()):
        for lado in 'EC':
            mm = h == lado
            a = int(((g == gen) & mm & (inv == 1)).sum()); b = int(((g == gen) & mm & (inv == 0)).sum())
            c = int(((g != gen) & mm & (inv == 1)).sum()); d = int(((g != gen) & mm & (inv == 0)).sum())
            orr, pf = stats.fisher_exact([[a, b], [c, d]])
            res.append(dict(genero=gen, mitad=lado, copiados=a, no_copiados=b, tasa=a / max(1, a + b),
                            tasa_resto=c / max(1, c + d), OR=orr, p=pf))
    G = pd.DataFrame(res)
    hip = G[(G.mitad == 'E') & (G.p < .10)].genero.tolist()
    GC = G[(G.mitad == 'C') & G.genero.isin(hip)].copy()
    if len(GC):
        o = np.argsort(GC.p.values)
        GC['holm'] = np.minimum(1, np.maximum.accumulate(GC.p.values[o] * (len(GC) - np.arange(len(GC)))))[np.argsort(o)]
    G.to_csv(os.path.join(OUT, 'generos_copia.csv'), index=False, float_format='%.3g')
    log('\nGéneros (implicación en ≥1 copia), E y C:'); log(G.to_string())
    log('Hipótesis llevadas a C:', hip); log(GC.to_string() if len(GC) else '(ninguna)')
    # por sitio
    sit = []
    for s_ in vc.index[vc >= 6]:
        sit.append(dict(sitio=s_, n=int(vc[s_]), copiados=int(inv[known[known == s_].index].sum())))
    log('\nImplicación por sitio (≥6 quipus):'); log(pd.DataFrame(sit).sort_values('copiados', ascending=False).to_string())
    open(os.path.join(OUT, 'salida_03.txt'), 'w', encoding='utf-8').write('\n'.join(LOG))


if __name__ == '__main__':
    main()
