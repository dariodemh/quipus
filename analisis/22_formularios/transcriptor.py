"""22_formularios / control por transcriptor (ronda pedida por el coordinador).

Repite la prueba de refutación y el contraste dentro/entre archivos solo entre quipus del MISMO transcriptor.
Dos definiciones de transcriptor:
  inv  = investigador del registro (prefijo; UR>=1000 = Ascher), la misma regla que analisis/24_color_formato/comun24.py
  dig  = moda de cord.CREATED_BY en OKR (quien DIGITALIZÓ las cuerdas; lo pidió el coordinador)
Entrada: refutacion_pares.csv (de archivos.py). Salidas: transcriptor_quipus.csv, transcriptor_pares_{inv,dig}.csv,
transcriptor_resumen.csv, salida_transcriptor.txt
Uso: python analisis/22_formularios/transcriptor.py
"""
import re, sqlite3
import numpy as np, pandas as pd
from scipy import stats

AQ = 'analisis/22_formularios/'
DSTAR = 0.434  # d* de salida_archivos.txt (máx. distancia UR053A/C/D en W|R|A)
rng = np.random.default_rng(20261018)
L = []
def say(*a):
    s = ' '.join(map(str, a)); print(s); L.append(s)

def inv(k):  # = comun24.registrador
    p = k[:2].upper()
    if p == 'UR':
        return 'AS' if int(re.sub(r'\D', '', k[2:6]) or 0) >= 1000 else 'UR'
    return p

con = sqlite3.connect('file:data/external/open-khipu-repository/data/khipu.db?mode=ro', uri=True)
cb = pd.read_sql('select m.OKR_NUM okr, lower(c.CREATED_BY) dig, count(*) n from cord c join khipu_main m using(KHIPU_ID) group by 1, 2', con)
cb = cb.sort_values('n').drop_duplicates('okr', keep='last')
q = pd.read_csv('analisis/datos/quipus.csv')[['kfg', 'okr']].merge(cb[['okr', 'dig']], how='left')
q['inv'] = q.kfg.map(inv)
q[['kfg', 'okr', 'inv', 'dig']].to_csv(AQ + 'transcriptor_quipus.csv', index=False)
say('tabla investigador x digitalizador (quipus):'); say(pd.crosstab(q.inv, q.dig).to_string())
T = q.set_index('kfg')

P = pd.read_csv(AQ + 'refutacion_pares.csv')
for col in ('inv', 'dig'):
    P[col + 'A'] = P.A.map(T[col]); P[col + 'B'] = P.B.map(T[col])
pf = lambda s: np.array([float(x) for x in s.split('/')])
P['_pa'] = P.perfilA.map(pf); P['_pb'] = P.perfilB.map(pf)

def S(D, B=2000):
    if D.empty: return 0, np.nan, np.nan
    obs = int((D.d <= DSTAR).sum()); nul = np.zeros(B)
    for pa, pb in zip(D._pa, D._pb):
        nul += np.array([np.linalg.norm(pa[rng.permutation(len(pa))] - pb) <= DSTAR for _ in range(B)])
    return obs, nul.mean(), (1 + (nul >= obs).sum()) / (B + 1)

def potencia(n, p0, p1=0.25, a=0.05):
    """potencia binomial unilateral para detectar tasa p1 (la de dentro de archivo) frente a p0 (nulo permutado)."""
    if n == 0: return np.nan
    c = stats.binom.ppf(1 - a, n, p0) + 1
    return stats.binom.sf(c - 1, n, p1)

filas = []
for defi in ('inv', 'dig'):
    say(f'\n===== transcriptor = {defi} =====')
    M = P[(P[defi + 'A'] == P[defi + 'B']) & P[defi + 'A'].notna()].copy(); M['tr'] = M[defi + 'A']
    say('pares mismo transcriptor por tipo:', pd.crosstab(M.tr, [M.tipo, M.k >= 3]).to_dict('index'))
    mh = []
    for tr in ['TODOS'] + sorted(M.tr.unique()):
        X = M if tr == 'TODOS' else M[M.tr == tr]
        for kk, sel in (('k=2', X.k == 2), ('k>=3', X.k >= 3)):
            a_, b_ = X[sel & (X.tipo == 'mismo_archivo')], X[sel & (X.tipo == 'no_relacionado')]
            if len(a_) + len(b_) == 0: continue
            oa, ma, pa = S(a_); ob, mb, pb = S(b_)
            tab = [[(a_.d <= DSTAR).sum(), (a_.d > DSTAR).sum()], [(b_.d <= DSTAR).sum(), (b_.d > DSTAR).sum()]]
            fo, fp = stats.fisher_exact(tab) if len(a_) and len(b_) else (np.nan, np.nan)
            p0 = mb / len(b_) if len(b_) else np.nan
            crit = b_[(b_.k >= 3) & (b_.d <= DSTAR) & (b_.QA != 'no') & (b_.QB != 'no') & (b_.p_colA < .01) & (b_.p_colB < .01)]
            r = dict(definicion=defi, transcriptor=tr, k=kk, n_dentro=len(a_), cerca_dentro=oa, nulo_dentro=ma, p_dentro=pa,
                     n_entre=len(b_), cerca_entre=ob, nulo_entre=mb, p_entre=pb, n_entre_estricto=int(b_.estricto.sum()),
                     cerca_entre_estricto=int((b_.estricto & (b_.d <= DSTAR)).sum()), OR=fo, p_fisher=fp,
                     potencia_entre_25pc=potencia(len(b_), p0) if len(b_) else np.nan, pares_criterio=len(crit))
            filas.append(r)
            if tr != 'TODOS' and len(a_) and len(b_): mh.append(np.array(tab, float) + 0)
            say(f'  {tr:6s} {kk:4s}: dentro {oa}/{len(a_)} (nulo {ma:.1f}, p={pa:.3g}) | entre {ob}/{len(b_)} (nulo {mb:.1f}, p={pb:.3g}; estrictos {r["cerca_entre_estricto"]}/{r["n_entre_estricto"]}) | OR={fo:.2f} p={fp:.3g} | potencia(25%)={r["potencia_entre_25pc"]:.2f} | criterio refutación: {len(crit)}')
    if mh:
        # Mantel-Haenszel a mano sobre estratos (transcriptor x k)
        num = sum(t[0, 0] * t[1, 1] / t.sum() for t in mh); den = sum(t[0, 1] * t[1, 0] / t.sum() for t in mh)
        say(f'  OR de Mantel-Haenszel estratificado por transcriptor y k: {num/den if den else np.inf:.2f} ({len(mh)} estratos con ambos tipos)')
    X = M[(M.tipo == 'no_relacionado') & (M.d <= DSTAR)]
    say('  pares no relacionados, mismo transcriptor, d<=d*:')
    say(X[['tr', 'motivo', 'k', 'A', 'B', 'procA', 'procB', 'estricto', 'd', 'p_colA', 'p_colB', 'QA', 'QB']].sort_values(['k', 'd'], ascending=[False, True]).to_string() if len(X) else '   (ninguno)')
    M.drop(columns=['_pa', '_pb']).assign(definicion=defi).to_csv(AQ + f'transcriptor_pares_{defi}.csv', index=False)

# sensibilidad: UR053A-E domina los pares dentro de archivo; repetir sin él (investigador fijo)
say('\n== sensibilidad: investigador fijo, sin pares UR053~UR053 ==')
M = P[(P.invA == P.invB)].copy(); M = M[~(M.A.str.startswith('UR053') & M.B.str.startswith('UR053'))]
for tr in ('UR', 'AS'):
    for kk, sel in (('k=2', M.k == 2), ('k>=3', M.k >= 3)):
        a_, b_ = M[sel & (M.invA == tr) & (M.tipo == 'mismo_archivo')], M[sel & (M.invA == tr) & (M.tipo == 'no_relacionado')]
        oa, ma, pa = S(a_); ob, mb, pb = S(b_)
        tab = [[oa, len(a_) - oa], [ob, len(b_) - ob]]
        fo, fp = stats.fisher_exact(tab) if len(a_) and len(b_) else (np.nan, np.nan)
        say(f'  {tr} {kk}: dentro {oa}/{len(a_)} (nulo {ma:.1f}, p={pa:.3g}) | entre {ob}/{len(b_)} (nulo {mb:.1f}, p={pb:.3g}) | OR={fo:.2f} p={fp:.3g}')
        filas.append(dict(definicion='inv_sin_UR053', transcriptor=tr, k=kk, n_dentro=len(a_), cerca_dentro=oa, nulo_dentro=ma, p_dentro=pa,
                          n_entre=len(b_), cerca_entre=ob, nulo_entre=mb, p_entre=pb, OR=fo, p_fisher=fp))

# mezcla de transcriptores en los pares entre archivos originales
say('\n== composición de los pares de refutación originales ==')
for tp in ('mismo_archivo', 'no_relacionado'):
    X = P[P.tipo == tp]
    say(f'  {tp}: mismo investigador {(X.invA == X.invB).mean():.2f} de {len(X)}; mismo digitalizador {(X.digA == X.digB).mean():.2f}')
pd.DataFrame(filas).to_csv(AQ + 'transcriptor_resumen.csv', index=False)
open(AQ + 'salida_transcriptor.txt', 'w', encoding='utf-8').write('\n'.join(L))
