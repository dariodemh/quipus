"""26_clave_local / prueba principal, controles, Incahuasi y refutación (diseno.md §3-8).

Uso (después de estructura.py y validacion.py): python analisis/26_clave_local/clave_local.py
Salidas: pruebas.csv, archivos_detalle.csv, pares_concordancia.csv, refutacion26.csv, salida_clave_local.txt
"""
import sys, re, itertools
sys.path.insert(0, 'analisis/26_clave_local')
from comun26 import *  # noqa
from scipy import stats

L = []
def say(*a):
    s = ' '.join(map(str, a)); print(s); L.append(s)

REP, R3 = cargar_reps()
q = tabla_quipus()
lab = dict(zip(q.kfg, q.archivo.where(q.archivo.notna(), None)))
labS = dict(zip(q.kfg, q.archivo_sitio.where(q.archivo_sitio.notna(), None)))
invs = dict(zip(q.kfg, q.inv)); proc = dict(zip(q.kfg, q.procedencia.astype(str).str.strip())); mus = dict(zip(q.kfg, q.mus))
EX = pares_excluidos()
# desviación 1: la exclusión de juegos con letra (misma base) NO se aplica a UR053A-E, que es el control positivo
excl = lambda a, b: frozenset((a, b)) in EX or (misma_base(a, b) and not (a in UR053 and b in UR053))
Qd = pd.read_csv('analisis/22_formularios/quipus_detector.csv').set_index('kfg').Q
rng = np.random.default_rng(SEED)
FUERA = ('UR053', 'Incahuasi')

# ---------- pares: concordancia por representación ----------
filas = []
for R in ('R1', 'R2'):
    ks = sorted(k for k in REP[R] if k in invs)
    for a, b in itertools.combinations(ks, 2):
        if excl(a, b): continue
        ra, rb = REP[R][a], REP[R][b]
        sh = [t for t in ra if t in rb]
        ds = {t: np.linalg.norm(ra[t][0] - rb[t][0]) for t in sh}
        sh3 = [t for t in sh if ra[t][2] >= 3]
        filas.append(dict(R=R, A=a, B=b, invA=invs[a], invB=invs[b], archA=lab[a], archB=lab[b],
                          dentro=lab[a] is not None and lab[a] == lab[b], comparte=bool(sh), concuerda=any(d <= DSTAR for d in ds.values()),
                          comparte3=bool(sh3), concuerda3=any(ds[t] <= DSTAR for t in sh3),
                          patrones_cerca='|'.join(t for t in sh if ds[t] <= DSTAR), dmin=min(ds.values(), default=np.nan)))
PA = pd.DataFrame(filas)
PA.to_csv(A26 + 'pares_concordancia.csv', index=False)

def S_de(R, col='concuerda', cond=None):
    X = PA[PA.R == R]
    if cond: X = X[X[cond]]
    return {frozenset((a, b)): float(v) for a, b, v in zip(X.A, X.B, X[col])}

def elegibles(R, fuera=FUERA, etiq=lab):
    return sorted(k for k in REP[R] if k in invs and etiq.get(k) not in fuera)

res = []
def correr(nombre, familia, ks, S, etiq, cruzados=False, B=9999):
    r = prueba_perm(ks, S, etiq, invs, B=B, cruzados=cruzados, rng=rng)
    det = '; '.join(f'{k}: {v["media_dentro"]:.3f} ({v["n_dentro"]}) vs {v["media_entre"]:.3f} ({v["n_entre"]})' for k, v in r['estratos'].items() if v['n_dentro'])
    say(f'  {nombre:55s} T = {r["T"]:+.4f}  p = {r["p"]:.4g}   [{det}]')
    res.append(dict(prueba=nombre, familia=familia, T=r['T'], p=r['p'], estratos=det))
    return r

say('== §5 prueba principal (mismo investigador; nulo: etiquetas de archivo permutadas dentro de investigador; sin UR053 ni Incahuasi) ==')
for R in ('R1', 'R2'):
    correr(f'{R} incondicional', 'primaria', elegibles(R), S_de(R), lab)
say('-- secundarias --')
for R in ('R1', 'R2'):
    ks = elegibles(R)
    correr(f'{R} condicional (pares que comparten patrón)', 'secundaria', ks, S_de(R, cond='comparte'), lab)
    correr(f'{R} incondicional, k>=3', 'secundaria', ks, S_de(R, 'concuerda3'), lab)
    correr(f'{R} condicional, k>=3', 'secundaria', ks, S_de(R, 'concuerda3', 'comparte3'), lab)
    correr(f'{R} incondicional, estratos con investigadores cruzados', 'secundaria', ks, S_de(R), lab, cruzados=True)
    correr(f'{R} incondicional, partición por sitio (Ica, Pachacamac enteros)', 'secundaria', elegibles(R, etiq=labS), S_de(R), labS)
    correr(f'{R} incondicional, CON UR053 (comparación con 22)', 'referencia', elegibles(R, fuera=('Incahuasi',)), S_de(R), lab)
for x in ('bandas', 'cabecera'):
    v = R3[x].dropna(); ks = sorted(k for k in v.index if k in invs and lab.get(k) not in FUERA)
    S = {frozenset((a, b)): -abs(v[a] - v[b]) for a, b in itertools.combinations(ks, 2) if not excl(a, b)}
    correr(f'R3 {x} (s = -|dif|)', 'secundaria', ks, S, lab, B=4999)

say('\n== control positivo: UR053A-E como único archivo (resto singleton) ==')
for R in ('R1', 'R2'):
    ks = sorted(k for k in REP[R] if k in invs and lab.get(k) != 'Incahuasi')
    et = {k: ('UR053' if lab.get(k) == 'UR053' else None) for k in ks}
    say(f'  {R}: miembros de UR053 elegibles {[k for k in ks if et[k]]}')
    correr(f'{R} control UR053', 'control', ks, S_de(R), et)
    correr(f'{R} control UR053, condicional', 'control', ks, S_de(R, cond='comparte'), et)

say('\n== §7 Incahuasi como único archivo ==')
for R in ('R1', 'R2'):
    ks = sorted(k for k in REP[R] if k in invs and lab.get(k) != 'UR053')
    et = {k: ('Incahuasi' if lab.get(k) == 'Incahuasi' else None) for k in ks}
    say(f'  {R}: miembros elegibles {sum(1 for k in ks if et[k])} ({pd.Series([invs[k] for k in ks if et[k]]).value_counts().to_dict()})')
    correr(f'{R} Incahuasi, mismo investigador', 'incahuasi', ks, S_de(R), et)
    correr(f'{R} Incahuasi, con estrato UR-JC', 'incahuasi', ks, S_de(R), et, cruzados=True)
    X = PA[(PA.R == R) & (PA.archA == 'Incahuasi') & (PA.archB == 'Incahuasi')]
    for nm, sel in (('UR-UR', (X.invA == 'UR') & (X.invB == 'UR')), ('JC-JC', (X.invA == 'JC') & (X.invB == 'JC')), ('UR-JC', X.invA != X.invB)):
        say(f'    pares dentro de Incahuasi {nm}: {len(X[sel])}, comparten {X[sel].comparte.mean():.2f}, concuerdan {X[sel].concuerda.mean():.3f}')

T = pd.DataFrame(res)
for fam in T.familia.unique():
    m = T.familia == fam
    T.loc[m, 'holm_familia'] = holm(T.loc[m, 'p'])
T['bh_todas'] = bh(T.p)
T.to_csv(A26 + 'pruebas.csv', index=False)
say('\n== resumen de pruebas ==')
say(T[['prueba', 'familia', 'T', 'p', 'holm_familia', 'bh_todas']].round(4).to_string())

# ---------- detalle por archivo ----------
say('\n== detalle por archivo (cada archivo como único etiquetado; mismo investigador; B = 1999) ==')
det = []
for R in ('R1', 'R2'):
    X = PA[PA.R == R]
    for a_ in sorted({x for x in lab.values() if x}):
        miem = [k for k in REP[R] if lab.get(k) == a_ and k in invs]
        if len(miem) < 2: continue
        ks = sorted(k for k in REP[R] if k in invs and (lab.get(k) not in FUERA or lab.get(k) == a_))
        et = {k: (a_ if lab.get(k) == a_ else None) for k in ks}
        r = prueba_perm(ks, S_de(R), et, invs, B=1999, rng=rng)
        D = X[(X.archA == a_) & (X.archB == a_) & (X.invA == X.invB)]
        det.append(dict(R=R, archivo=a_, n_quipus=len(miem), investigadores='/'.join(sorted({invs[k] for k in miem})), n_pares_dentro=len(D),
                        concuerdan_dentro=int(D.concuerda.sum()), T=r['T'], p=r['p'],
                        patrones_cerca=pd.Series('|'.join(D.patrones_cerca).split('|')).replace('', np.nan).dropna().value_counts().head(4).to_dict()))
DT = pd.DataFrame(det)
DT['bh'] = np.nan
for R in ('R1', 'R2'):
    m = (DT.R == R) & DT.p.notna()
    DT.loc[m, 'bh'] = bh(DT.loc[m, 'p']); DT.loc[m, 'holm'] = holm(DT.loc[m, 'p'])
DT.to_csv(A26 + 'archivos_detalle.csv', index=False)
say(DT.sort_values(['R', 'p']).round(4).to_string(max_colwidth=60))

# ---------- §8 refutación ----------
say('\n== §8 refutación con la representación invariante (cualquier investigador) ==')
MALAS = {'unknown', 'peru', 'nan', ''}
pal = lambda k: set(re.findall(r'\w{4,}', proc[k].lower()))
def estricto(a, b):
    return (proc[a].lower() not in MALAS and proc[b].lower() not in MALAS and not (lab[a] is not None and lab[a] == lab[b])
            and not (pal(a) & pal(b)) and mus[a] != mus[b])
ref = []
for R in ('R1', 'R2'):
    for a, b in itertools.combinations(sorted(k for k in REP[R] if k in invs), 2):
        if excl(a, b): continue
        tipo = 'dentro' if (lab[a] is not None and lab[a] == lab[b]) else ('estricto' if estricto(a, b) else 'otro')
        if tipo == 'otro': continue
        for t in REP[R][a]:
            if t in REP[R][b] and REP[R][a][t][2] >= 3:
                pa, pb = REP[R][a][t][0], REP[R][b][t][0]
                ref.append(dict(R=R, patron=t, k=len(pa), A=a, B=b, tipo=tipo, archA=lab[a], archB=lab[b], invA=invs[a], invB=invs[b],
                                procA=proc[a], procB=proc[b], d=np.linalg.norm(pa - pb), p_colA=REP[R][a][t][1], p_colB=REP[R][b][t][1],
                                QA=Qd.get(a, 'no'), QB=Qd.get(b, 'no'), _pa=pa, _pb=pb))
RF = pd.DataFrame(ref)
RF['crit'] = (RF.d <= DSTAR) & (RF.p_colA < .01) & (RF.p_colB < .01) & (RF.QA != 'no') & (RF.QB != 'no')
NB = 2000
def nulo_pares(D):
    """por par de quipus: ¿algún patrón compartido con d <= d*? bajo permutación de posiciones del perfil de A. -> (obs, nulo B)"""
    g = D.groupby(['A', 'B'])
    obs = int(g.d.min().le(DSTAR).sum()); nul = np.zeros(NB)
    for _, x in g:
        hit = np.zeros(NB, bool)
        for pa, pb in zip(x._pa, x._pb):
            P = np.argsort(rng.random((NB, len(pa))), axis=1)
            hit |= np.linalg.norm(pa[P] - pb, axis=1) <= DSTAR
        nul += hit
    return obs, g.ngroups, nul
out = []
for R in ('R1', 'R2', 'R1+R2'):
    X = RF if R == 'R1+R2' else RF[RF.R == R]
    for tipo, sel in (('dentro (sin UR053)', (X.tipo == 'dentro') & (X.archA != 'UR053')),
                      ('dentro (sin UR053 ni Incahuasi)', (X.tipo == 'dentro') & ~X.archA.isin(FUERA)),
                      ('estricto', X.tipo == 'estricto'), ('estricto, mismo investigador', (X.tipo == 'estricto') & (X.invA == X.invB)),
                      ('estricto, investigadores distintos', (X.tipo == 'estricto') & (X.invA != X.invB))):
        D = X[sel]
        if D.empty: continue
        o, n, nul = nulo_pares(D)
        Dc = D[(D.p_colA < .01) & (D.p_colB < .01) & (D.QA != 'no') & (D.QB != 'no')]
        oc, nc, nulc = nulo_pares(Dc) if len(Dc) else (0, 0, np.zeros(NB))
        sitios = {frozenset((r.procA, r.procB)) for r in Dc[Dc.d <= DSTAR].itertuples()}
        fila = dict(R=R, tipo=tipo, pares_quipu=n, concuerdan=o, tasa=o / n, nulo=nul.mean(), p=(1 + (nul >= o).sum()) / (NB + 1),
                    crit_pares=oc, crit_nulo=nulc.mean(), crit_p95=np.percentile(nulc, 95), crit_p=(1 + (nulc >= oc).sum()) / (NB + 1), crit_sitios=len(sitios))
        out.append(fila)
        say(f'  {R:6s} {tipo:36s}: {o}/{n} pares de quipus concuerdan ({o/n:.3f}; nulo {nul.mean():.1f}, p = {fila["p"]:.4g}) | criterio individual {oc} (nulo {nulc.mean():.2f}, p95 {fila["crit_p95"]:.0f}, p = {fila["crit_p"]:.3g}; pares de sitios {len(sitios)})')
RO = pd.DataFrame(out); RO.to_csv(A26 + 'refutacion26_resumen.csv', index=False)
RF.drop(columns=['_pa', '_pb']).to_csv(A26 + 'refutacion26.csv', index=False)
say('\n  pares estrictos que cumplen el criterio individual:')
C = RF[(RF.tipo == 'estricto') & RF.crit].drop(columns=['_pa', '_pb'])
say(C[['R', 'patron', 'A', 'B', 'invA', 'invB', 'procA', 'procB', 'd', 'p_colA', 'p_colB']].round(3).to_string() if len(C) else '   (ninguno)')
say('\n  patrones k>=3 con d<=d* en pares estrictos (top):', RF[(RF.tipo == 'estricto') & (RF.d <= DSTAR)].patron.value_counts().head(10).to_dict())
for R in ('R1', 'R2', 'R1+R2'):
    e = RO[(RO.R == R) & (RO.tipo == 'estricto')]; w = RO[(RO.R == R) & (RO.tipo == 'dentro (sin UR053)')]
    if len(e) and len(w):
        e, w = e.iloc[0], w.iloc[0]
        a_ = e.p < .05 and e.tasa >= w.tasa
        b_ = e.crit_pares >= 3 and e.crit_sitios >= 3 and e.crit_pares > e.crit_p95
        say(f'  REGLA {R}: (a) {a_} [estricto {e.tasa:.3f}, p={e.p:.3g} vs dentro {w.tasa:.3f}]; (b) {b_} [{e.crit_pares} pares, {e.crit_sitios} sitios, p95 {e.crit_p95:.0f}] -> {"REFUTA" if (a_ or b_) else "no refuta"}')
open(A26 + 'salida_clave_local.txt', 'w', encoding='utf-8').write('\n'.join(L))
