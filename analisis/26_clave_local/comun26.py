"""26_clave_local / común: representaciones invariantes al vocabulario, archivos, investigador y prueba por permutación.

Reutiliza analisis/22_formularios/detector.py (cargar, candidatos, anova, perfil). Ver diseno.md.
"""
import re, sys, sqlite3, itertools
import numpy as np, pandas as pd
sys.path.insert(0, 'analisis/22_formularios')
from detector import cargar, candidatos, anova, perfil  # noqa: E402

A26 = 'analisis/26_clave_local/'
SEED = 20261018
DSTAR = 0.434  # 22_formularios: máx. distancia UR053A/C/D en W|R|A
UR053 = {'UR053A', 'UR053B', 'UR053C', 'UR053D', 'UR053E'}


def inv(k):  # = 24_color_formato/comun24.registrador = 22_formularios/transcriptor.inv
    p = k[:2].upper()
    if p == 'UR':
        return 'AS' if int(re.sub(r'\D', '', k[2:6]) or 0) >= 1000 else 'UR'
    return p


def recod(m):
    """secuencia de colores -> patrón por orden de aparición: W,R,W,A -> 'ABAC'."""
    d = {}
    return ''.join(d.setdefault(x, chr(65 + len(d))) for x in m)


def invertir(d):
    return {**d, 'v': d['v'][::-1].copy(), 'cf': d['cf'][::-1], 'cg': d['cg'][::-1], 'g': d['g'][::-1].copy(), 'cu': d['cu'][::-1]}


def representar(d):
    """{'R1': {patrón: (perfil, p, k, nb)}, 'R2': {...}, 'bandas': x, 'cabecera': y} con p_col < .05."""
    out = {'R1': {}, 'R2': {}}
    for fam, R in (('Cf', 'R1'), ('P', 'R2')):
        for _, clave, idx in candidatos(d, fams=(fam,)):
            V = d['v'][idx]; p = anova(V)[0]
            if not p < .05:
                continue
            pat = recod(clave.split('|')) if R == 'R1' else clave
            if pat not in out[R] or p < out[R][pat][1]:
                out[R][pat] = (perfil(V), p, V.shape[1], len(V))
    cf, g = np.array(d['cf'], object), d['g']
    ok = (cf[1:] != 'nan') & (cf[:-1] != 'nan')
    ch = ok & (cf[1:] != cf[:-1]); fr = g[1:] != g[:-1]
    out['bandas'] = (ch & fr).sum() / ch.sum() if ch.sum() >= 3 else np.nan
    cab = []
    for gg in pd.unique(g):
        c = [x for x in cf[g == gg] if x != 'nan']
        if len(c) >= 3:
            moda = pd.Series(c).mode().iloc[0]
            cab.append(c[0] != moda)
    out['cabecera'] = np.mean(cab) if len(cab) >= 3 else np.nan
    return out


def concord(ra, rb, kmin=2):
    """(comparten patrón, concuerdan: algún patrón compartido con d <= d*) para R1 o R2 ya extraídos."""
    sh = [t for t in ra if t in rb and ra[t][2] >= kmin]
    return bool(sh), any(np.linalg.norm(ra[t][0] - rb[t][0]) <= DSTAR for t in sh)


def museo_norm(s):
    s = re.sub(r'[^a-z]', '', str(s).lower())
    return 'berlin' if 'berlin' in s else s[:25]


def tabla_quipus():
    """kfg, okr, museo, procedencia, inv, MUSEUM_NUM, archivo (partición principal), archivo_sitio (sensibilidad)."""
    q = pd.read_csv('analisis/datos/quipus.csv')
    con = sqlite3.connect('file:data/external/open-khipu-repository/data/khipu.db?mode=ro', uri=True)
    mn = pd.read_sql('select OKR_NUM, MUSEUM_NUM from khipu_main', con).drop_duplicates('OKR_NUM')
    q = q.merge(mn, left_on='okr', right_on='OKR_NUM', how='left').drop(columns='OKR_NUM')
    q['inv'] = q.kfg.map(inv)
    q['mus'] = q.museo.map(museo_norm)
    pr = q.procedencia.astype(str).str.strip()
    nb = {'UR1140', 'UR1136', 'UR223', 'HP056', 'UR234', 'UR1131'}
    ica = pr.str.contains(r'\bIca\b|Ocucaje|Callango|Pisco', regex=True)
    reglas = [
        (q.kfg.isin(nb), lambda r: 'Nazca-Berlin'),
        (pr == 'Santa', lambda r: 'Santa'),
        ((q.museo == 'Puruchuco Museum') | (pr == 'Huaquerones'), lambda r: 'Puruchuco-Huaquerones'),
        (pr == 'Leymebamba', lambda r: 'Leymebamba'),
        (pr.str.contains('Armatambo'), lambda r: 'Armatambo'),
        (pr == 'Pachacamac', lambda r: 'Pachacamac|' + r.mus),
        (ica, lambda r: 'Ica|' + r.mus),
        (pr.str.contains('Nazca'), lambda r: 'Nazca|' + r.mus),
    ]
    arch = pd.Series([None] * len(q), index=q.index, dtype=object)
    for m, f in reglas:
        sel = m & arch.isna()
        arch[sel] = [f(r) for r in q[sel].itertuples()]
    # 9. inventario consecutivo (regla de 22_formularios/archivos.py) para el resto
    def invn(s):
        m = re.match(r'^\s*([A-Za-z.# ]*?)\s*(\d+)', str(s))
        return (m.group(1).upper().strip(), int(m.group(2))) if m else None
    resto = [(i, r.mus, invn(r.MUSEUM_NUM)) for i, r in q[arch.isna()].iterrows() if invn(r.MUSEUM_NUM)]
    par = {i: i for i, _, _ in resto}
    def raiz(x):
        while par[x] != x: x = par[x]
        return x
    for (a, ma, na), (b, mb, nb_) in itertools.combinations(resto, 2):
        if ma == mb and na[0] == nb_[0] and abs(na[1] - nb_[1]) <= 1:
            par[raiz(a)] = raiz(b)
    comp = {}
    for i, _, _ in resto:
        comp.setdefault(raiz(i), []).append(i)
    for c in comp.values():
        if len(c) >= 2:
            arch[c] = 'inv_consec|' + '+'.join(sorted(q.kfg[c]))[:50]
    arch[q.procedencia.astype(str).str.strip() == 'Incahuasi'] = 'Incahuasi'
    arch[q.kfg.isin(UR053)] = 'UR053'
    q['archivo'] = arch
    sitio = arch.copy()
    sitio[arch.fillna('').str.startswith('Pachacamac|')] = 'Pachacamac'
    sitio[arch.fillna('').str.startswith('Ica|')] = 'Ica'
    q['archivo_sitio'] = sitio
    return q


def pares_excluidos():
    """copias / mismo objeto (14_copias) y juegos con letra (misma base)."""
    c = pd.read_csv('analisis/14_copias/pares_resumen.csv')
    ex = {frozenset(x) for x in zip(c.A, c.B)}
    return ex


def misma_base(a, b):
    ma, mb = re.match(r'^([A-Z]+\d+)[A-Z]$', a), re.match(r'^([A-Z]+\d+)[A-Z]$', b)
    return bool(ma and mb and ma.group(1) == mb.group(1))


def prueba_perm(ks, S, lab, invs, B=9999, cruzados=False, rng=None):
    """T = sum_s w_s (media dentro - media entre) / sum w_s; nulo: permutar etiquetas de archivo dentro de investigador.

    ks: lista de quipus; S: dict frozenset(a,b) -> valor (pares ausentes = no cuentan); lab: etiqueta de archivo por quipu
    (None = singleton); invs: investigador por quipu. cruzados=False: solo pares del mismo investigador, estrato = investigador;
    True: estrato = par de investigadores. Para un control de un solo archivo (UR053, Incahuasi) se etiqueta solo ese
    archivo y el resto va como singleton. Devuelve dict con T, p, detalle por estrato.
    """
    rng = rng or np.random.default_rng(SEED)
    n = len(ks); pos = {k: i for i, k in enumerate(ks)}
    L = np.array([lab[k] if lab[k] is not None else f'_solo_{k}' for k in ks], object)
    codes = pd.factorize(L)[0]
    I = np.array([invs[k] for k in ks])
    ia, ja, st, sv, stn = [], [], [], [], {}
    for pr_, v in S.items():
        a, b = tuple(pr_)
        if a not in pos or b not in pos: continue
        if not cruzados and I[pos[a]] != I[pos[b]]: continue
        key = '-'.join(sorted({I[pos[a]], I[pos[b]]})) if cruzados else I[pos[a]]
        ia.append(pos[a]); ja.append(pos[b]); st.append(stn.setdefault(key, len(stn))); sv.append(v)
    ia, ja, st, sv = map(np.array, (ia, ja, st, sv))
    if len(sv) == 0:
        return dict(T=np.nan, p=np.nan, estratos={})
    ns = len(stn)
    tot_s = np.bincount(st, sv, ns); tot_n = np.bincount(st, minlength=ns).astype(float)
    def T_de(c):
        w = c[ia] == c[ja]
        sw = np.bincount(st, sv * w, ns); nw = np.bincount(st, w.astype(float), ns)
        nb = tot_n - nw
        with np.errstate(invalid='ignore', divide='ignore'):
            d = sw / nw - (tot_s - sw) / nb
        return d, nw, nb
    d0, nw0, nb0 = T_de(codes)
    ok = (nw0 > 0) & (nb0 > 0)
    wts = np.where(ok, nw0, 0)
    if wts.sum() == 0:
        return dict(T=np.nan, p=np.nan, estratos={})
    T0 = np.nansum(d0 * wts) / wts.sum()
    grupos = [np.flatnonzero(I == x) for x in np.unique(I)]
    ge = 0
    for _ in range(B):
        c = codes.copy()
        for g in grupos:
            c[g] = codes[g][rng.permutation(len(g))]
        d, _, _ = T_de(c)
        ge += np.nansum(np.where(ok, d, 0) * wts) / wts.sum() >= T0 - 1e-12
    sw0 = np.bincount(st, sv * (codes[ia] == codes[ja]), ns)
    det = {k: dict(n_dentro=int(nw0[i]), n_entre=int(nb0[i]), media_dentro=sw0[i] / nw0[i] if nw0[i] else np.nan,
                   media_entre=(tot_s[i] - sw0[i]) / nb0[i] if nb0[i] else np.nan) for k, i in stn.items()}
    return dict(T=T0, p=(1 + ge) / (B + 1), estratos=det)


def construir_reps():
    """Calcula R1/R2/R3 de todos los quipus; escribe patrones.csv y quipus26.csv."""
    Q, _ = cargar()
    filas, fq = [], []
    for k, d in Q.items():
        r = representar(d)
        for R in ('R1', 'R2'):
            for pat, (pf, p, kk, nb) in r[R].items():
                filas.append(dict(kfg=k, R=R, patron=pat, k=kk, n_bloques=nb, p_col=p, perfil='/'.join(f'{x:.4f}' for x in pf)))
        fq.append(dict(kfg=k, n_colg=len(d['v']), n_R1=len(r['R1']), n_R2=len(r['R2']), bandas=r['bandas'], cabecera=r['cabecera']))
    pd.DataFrame(filas).to_csv(A26 + 'patrones.csv', index=False)
    pd.DataFrame(fq).to_csv(A26 + 'quipus26.csv', index=False)


def cargar_reps():
    """-> REP[R][kfg][patron] = (perfil, p, k, nb); R3 DataFrame indexado por kfg."""
    P = pd.read_csv(A26 + 'patrones.csv')
    REP = {'R1': {}, 'R2': {}}
    for r in P.itertuples():
        REP[r.R].setdefault(r.kfg, {})[r.patron] = (np.array([float(x) for x in r.perfil.split('/')]), r.p_col, r.k, r.n_bloques)
    return REP, pd.read_csv(A26 + 'quipus26.csv').set_index('kfg')


def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); out = np.empty(m); run = 0
    for r, i in enumerate(o):
        run = max(run, (m - r) * p[i]); out[i] = min(1, run)
    return out


def bh(p):
    p = np.asarray(p, float); o = np.argsort(p)[::-1]; m = len(p); out = np.empty(m); run = 1
    for r, i in enumerate(o):
        run = min(run, p[i] * m / (m - r)); out[i] = run
    return out


if __name__ == '__main__':  # autocomprobación mínima
    assert recod(['W', 'R', 'W', 'A']) == 'ABAC' and recod(['MB', 'AB', 'MB']) == recod(['W', 'R', 'W'])
    assert misma_base('UR131A', 'UR131C') and not misma_base('UR131A', 'UR132A')
    # prueba_perm: archivo con concordancia total dentro debe dar p pequeño
    ks = [f'Q{i}' for i in range(20)]; lab = {k: ('A' if i < 5 else None) for i, k in enumerate(ks)}
    S = {frozenset(p): float(lab[p[0]] == 'A' and lab[p[1]] == 'A') for p in itertools.combinations(ks, 2)}
    r = prueba_perm(ks, S, lab, {k: 'X' for k in ks}, B=999)
    assert r['T'] == 1 and r['p'] < .01, r
    print('ok')
