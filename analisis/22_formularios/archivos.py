"""22_formularios / archivos: formularios de archivo (exploración→confirmación), refutación y tasa (diseno.md §4-7).

Uso (desde la raíz, después de detector.py):  python analisis/22_formularios/archivos.py
Salidas: formularios.csv, refutacion_pares.csv, salida_archivos.txt
"""
import re, sys, sqlite3, itertools
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, 'analisis/22_formularios')
from detector import cargar, candidatos, anova, bh, holm, perfil, AQ, SEED

Q, q = cargar()
R = pd.read_csv(AQ + 'quipus_detector.csv').set_index('kfg')
L = []
def say(*a):
    s = ' '.join(map(str, a)); print(s); L.append(s)

# ---------- §4 archivos ----------
con = sqlite3.connect('file:data/external/open-khipu-repository/data/khipu.db?mode=ro', uri=True)
inv = pd.read_sql('select OKR_NUM, MUSEUM_NUM from khipu_main', con).drop_duplicates('OKR_NUM')
q = q.merge(inv, left_on='okr', right_on='OKR_NUM', how='left')
q = q[q.kfg.isin(Q)]
ARCH = {}  # nombre -> set de kfg
for k, base in ((k, re.match(r'^[A-Z]+\d+', k)) for k in q.kfg):
    if base:
        ARCH.setdefault('conjunto:' + base.group(0), set()).add(k)
MALAS = {'unknown', 'peru', 'nan', ''}
for k, p in zip(q.kfg, q.procedencia.astype(str)):
    if p.strip().lower() not in MALAS:
        ARCH.setdefault('procedencia:' + p.strip(), set()).add(k)
def invn(s):
    m = re.match(r'^\s*([A-Za-z.# ]*?)\s*(\d+)', str(s))
    return (m.group(1).upper().strip(), int(m.group(2))) if m else None
iv = [(k, mu, invn(n)) for k, mu, n in zip(q.kfg, q.museo, q.MUSEUM_NUM) if invn(n)]
par = {k: k for k, _, _ in iv}
def raiz(x):
    while par[x] != x: x = par[x]
    return x
for (a, ma, na), (b, mb, nb) in itertools.combinations(iv, 2):
    if ma == mb and na[0] == nb[0] and abs(na[1] - nb[1]) <= 1:
        par[raiz(a)] = raiz(b)
comp = {}
for k, mu, _ in iv:
    comp.setdefault(raiz(k), set()).add(k)
for r_, s in comp.items():
    if len(s) >= 2:
        ARCH['museo_consecutivo:' + '+'.join(sorted(s))[:60]] = s
ARCH = {a: s for a, s in ARCH.items() if len(s) >= 2}
MIEMBRO = {}
for a, s in ARCH.items():
    for k in s: MIEMBRO.setdefault(k, set()).add(a)
say(f'archivos: {len(ARCH)} (conjunto {sum(a.startswith("conj") for a in ARCH)}, procedencia {sum(a.startswith("proc") for a in ARCH)}, museo_consecutivo {sum(a.startswith("museo") for a in ARCH)}); quipus en algún archivo: {len(MIEMBRO)} de {len(Q)}')
say('  ejemplos museo_consecutivo:', [a for a in ARCH if a.startswith('museo')][:8])

# ---------- §5 partición ----------
ks = sorted(Q)
perm = np.random.default_rng(SEED).permutation(len(ks))
nE = (len(ks) + 1) // 2
MITAD = {ks[i]: ('E' if j < nE else 'C') for j, i in enumerate(perm)}
say('controles en mitades:', {k: MITAD[k] for k in ['UR053A', 'UR053B', 'UR053C', 'UR053D', 'UR053E', 'UR270', 'UR278']})

# bloques de un tipo en un quipu (sin umbral de validez salvo suma>0)
def bloques(d, fam, clave):
    v, g = d['v'], d['g']
    cortes = np.flatnonzero(np.r_[True, g[1:] != g[:-1], True])
    segs = list(zip(cortes[:-1], cortes[1:]))
    if fam == 'P':
        k = int(clave[1:])
        idx = [np.arange(a, b) for a, b in segs if b - a == k]
    else:
        col = d['cf'] if fam == 'Cf' else d['cg']
        m = clave.split('|'); k = len(m); idx = []; fin = -1
        for a, b in segs:
            for s in range(a, b - k + 1):
                if s >= fin and col[s:s + k] == m:
                    idx.append(np.arange(s, s + k)); fin = s + k
    if not idx:
        return np.zeros((0, 0))
    V = v[np.array(idx)]
    return V[V.sum(1) > 0]

def clr(V):
    Y = np.log1p(V); return Y - Y.mean(1, keepdims=True)

# candidatos por quipu (sin deduplicar entre familias) con p_col
CAND = {}
for k, d in Q.items():
    out = {}
    for f in ('P', 'Cf', 'Cg'):
        for fam, clave, idx in candidatos(d, fams=(f,)):
            out[(fam, clave)] = anova(d['v'][idx])[0]
    CAND[k] = out

rng = np.random.default_rng(SEED)
def conf_test(Vs, pi, B=20000):
    X = np.vstack([clr(V) for V in Vs]); n, k = X.shape
    obs = (X @ pi).sum(); ge = 0
    for _ in range(B // 2000):
        P = np.argsort(rng.random((2000, n, k)), axis=2)
        ge += ((np.take_along_axis(np.broadcast_to(X, (2000, n, k)), P, axis=2) @ pi).sum(1) >= obs - 1e-9).sum()
    return obs, (1 + ge) / (B + 1)

copias = pd.read_csv('analisis/14_copias/pares_resumen.csv')[['A', 'B', 'tipo']]
agreg = pd.read_csv('analisis/13_sistema_incahuasi/agregados_hallazgos.csv')
agreg = agreg[agreg.A != agreg.B]

filas = []
for a, s in ARCH.items():
    E = sorted(k for k in s if MITAD[k] == 'E'); C = sorted(k for k in s if MITAD[k] == 'C')
    if not E:
        continue
    tipos = {t for k in E for t in CAND[k]}
    cand = []
    for t in tipos:
        qs = [k for k in E if t in CAND[k]]
        Vs = [bloques(Q[k], *t) for k in qs]
        pE = anova(np.vstack(Vs))[0]
        if pE < 1e-3:
            cand.append((t, pE, qs, Vs))
    for fam in ('P', 'Cf', 'Cg'):
        for t, pE, qs, Vs in sorted([c for c in cand if c[0][0] == fam], key=lambda c: c[1])[:3]:
            pi = np.mean([perfil(V) for V in Vs], 0)
            cuE = np.vstack([V / V.sum(1, keepdims=True) for V in Vs]).mean(0)
            VC = {k: bloques(Q[k], *t) for k in C}
            VC = {k: V for k, V in VC.items() if len(V) >= 2}
            fila = dict(archivo=a, fam=fam, clave=t[1], k=len(pi), quipus_E=' '.join(qs), n_bloques_E=sum(map(len, Vs)),
                        p_E=pE, cuotas_E='/'.join(f'{x:.2f}' for x in cuE), perfil_E='/'.join(f'{x:.2f}' for x in pi),
                        quipus_C=' '.join(VC), n_bloques_C=sum(map(len, VC.values())))
            if sum(map(len, VC.values())) >= 3:
                T, pC = conf_test(list(VC.values()), pi)
                fila.update(T=T, p_C=pC, cuotas_C='/'.join(f'{x:.2f}' for x in np.vstack([V / V.sum(1, keepdims=True) for V in VC.values()]).mean(0)))
                # especificidad: quipus que no comparten archivo con ningún miembro de A
                vecinos = set().union(*[MIEMBRO.get(k, set()) for k in s])
                fuera = [k for k in Q if k not in s and not (MIEMBRO.get(k, set()) & vecinos)]
                cin = [(clr(V) @ pi).mean() for V in VC.values()]
                cout = [(clr(V) @ pi).mean() for V in (bloques(Q[k], *t) for k in fuera) if len(V) >= 2]
                fila.update(n_fuera=len(cout), conc_C=np.mean(cin), conc_fuera=np.mean(cout) if cout else np.nan,
                            p_local=stats.mannwhitneyu(cin, cout, alternative='greater').pvalue if cout else np.nan,
                            p_fuera_signo=stats.binomtest(int(np.sum(np.array(cout) > 0)), len(cout), alternative='greater').pvalue if cout else np.nan)
            else:
                fila.update(p_C=np.nan)
            # en cuántos quipus del archivo aparece (ambas mitades), con p_col nominal y Q
            todos = [k for k in sorted(s) if t in CAND[k]]
            fila['quipus_con_tipo'] = ' '.join(todos)
            fila['n_quipus_tipo'] = len(todos)
            fila['n_quipus_tipo_p05'] = sum(CAND[k][t] < .05 for k in todos)
            fila['n_quipus_Q'] = sum(R.loc[k, 'Q'] != 'no' for k in todos)
            fila['n_quipus_archivo'] = len(s)
            tot = [bloques(Q[k], *t).sum(1).mean() for k in todos]
            fila['escala_max_min'] = max(tot) / min(tot) if len(tot) >= 2 and min(tot) > 0 else np.nan
            fila['cuotas_por_quipu'] = '; '.join(f'{k}:' + '/'.join(f'{x:.2f}' for x in (lambda V: (V / V.sum(1, keepdims=True)).mean(0))(bloques(Q[k], *t))) for k in todos)
            cp = copias[copias.A.isin(s) & copias.B.isin(s)]
            fila['copias'] = '; '.join(f'{x.A}~{x.B}({x.tipo})' for x in cp.itertuples())
            ag = agreg[agreg.A.isin(s) & agreg.B.isin(s)]
            fila['sumas_13'] = '; '.join(f'{x}:{n}' for x, n in ag.groupby(['A', 'B']).size().items())
            filas.append(fila)

F = pd.DataFrame(filas)
t = F.p_C.notna()
F.loc[t, 'q_bh'] = bh(F.loc[t, 'p_C']); F.loc[t, 'holm'] = holm(F.loc[t, 'p_C'])
def nivel(r):
    if pd.isna(r.p_C): return 'no confirmable'
    if r.q_bh >= .05: return 'no confirmado'
    loc = r.p_local < .05 if pd.notna(r.p_local) else False
    gen = (r.p_fuera_signo < .05) and not loc if pd.notna(r.p_fuera_signo) else False
    esp = 'local' if loc else ('generico' if gen else 'indeterminado')
    return ('bien apoyado' if (r.holm < .05 and loc) else 'apoyado') + '-' + esp
F['nivel'] = F.apply(nivel, axis=1)
F.to_csv(AQ + 'formularios.csv', index=False)
say(f'\n== §5 formularios de archivo: tipos llevados a confirmación {len(F)}; confirmables {t.sum()}; BH<.05 {(F.q_bh<.05).sum()}; Holm<.05 {(F.holm<.05).sum()}')
say(F.nivel.value_counts().to_string())
cols = ['archivo', 'fam', 'clave', 'quipus_E', 'quipus_C', 'n_bloques_E', 'n_bloques_C', 'cuotas_E', 'cuotas_C', 'p_E', 'p_C', 'q_bh', 'holm', 'conc_C', 'conc_fuera', 'n_fuera', 'p_local', 'p_fuera_signo', 'n_quipus_tipo', 'n_quipus_tipo_p05', 'n_quipus_Q', 'escala_max_min', 'nivel']
say(F[F.q_bh < .05].sort_values('p_C')[cols].to_string(max_colwidth=40))
say('\n-- controles (todas las filas de sus archivos) --')
say(F[F.archivo.str.contains('UR053|Incahuasi|UR27')][cols].to_string(max_colwidth=40))

# ---------- §6 refutación ----------
def rel(a, b):
    if MIEMBRO.get(a, set()) & MIEMBRO.get(b, set()): return True
    if ((copias.A == a) & (copias.B == b)).any() or ((copias.A == b) & (copias.B == a)).any(): return True
    return False
proc = dict(zip(q.kfg, q.procedencia.astype(str).str.strip())); mus = dict(zip(q.kfg, q.museo))
musn = lambda k: re.sub(r'[^a-z]', '', str(mus[k]).lower())[:25]  # nombres de museo con grafías/mojibake distintas
conoc = {k for k, p in proc.items() if p.lower() not in MALAS}
PERF = {}
for k in Q:
    for (fam, clave), p in CAND[k].items():
        if fam == 'Cf' and p < .05:
            PERF.setdefault(clave, []).append((k, perfil(bloques(Q[k], 'Cf', clave)), p))
# d*: UR053A, C, D sobre W-R-A grueso
pr = {k: perfil(bloques(Q[k], 'Cg', 'W|R|A')) for k in ['UR053A', 'UR053C', 'UR053D']}
dstar = max(np.linalg.norm(pr[a] - pr[b]) for a, b in itertools.combinations(pr, 2))
say(f'\n== §6 refutación: d* = {dstar:.3f} (perfiles W-R-A: ' + '; '.join(f'{k} ' + '/'.join(f'{x:.2f}' for x in v) for k, v in pr.items()) + ')')
pares = []
for m, lst in PERF.items():
    for (a, pa, qa), (b, pb, qb) in itertools.combinations(lst, 2):
        r_ = rel(a, b)
        tipo = 'mismo_archivo' if r_ else ('no_relacionado' if (a in conoc and b in conoc and proc[a] != proc[b]) else 'otro')
        estricto = tipo == 'no_relacionado' and not (set(re.findall(r'\w{4,}', proc[a].lower())) & set(re.findall(r'\w{4,}', proc[b].lower()))) and musn(a) != musn(b)
        pares.append(dict(motivo=m, k=len(pa), A=a, B=b, tipo=tipo, estricto=estricto, procA=proc.get(a), procB=proc.get(b),
                          d=np.linalg.norm(pa - pb), p_colA=qa, p_colB=qb, QA=R.loc[a, 'Q'], QB=R.loc[b, 'Q'],
                          perfilA='/'.join(f'{x:.2f}' for x in pa), perfilB='/'.join(f'{x:.2f}' for x in pb), _pa=pa, _pb=pb))
P = pd.DataFrame(pares)
def S_test(D, B=2000):
    if D.empty: return 0, np.nan, np.nan
    obs = int((D.d <= dstar).sum()); nul = np.zeros(B)
    for (pa, pb) in zip(D._pa, D._pb):
        nul += np.array([np.linalg.norm(pa[rng.permutation(len(pa))] - pb) <= dstar for _ in range(B)])
    return obs, nul.mean(), (1 + (nul >= obs).sum()) / (B + 1)
for tp in ('mismo_archivo', 'no_relacionado'):
    for kk, sel in (('k=2', P.k == 2), ('k>=3', P.k >= 3)):
        D = P[(P.tipo == tp) & sel]
        o, mu, pp = S_test(D)
        say(f'  {tp:15s} {kk}: pares {len(D)}, con d<=d* {o} (nulo {mu:.1f}), p = {pp:.4g}; d mediana {D.d.median() if len(D) else np.nan:.2f}')
D = P[(P.tipo == 'no_relacionado') & P.estricto & (P.k >= 3)]
o, mu, pp = S_test(D)
say(f'  no_relacionado ESTRICTO (sin palabra de procedencia común, museo distinto) k>=3: pares {len(D)}, d<=d* {o} (nulo {mu:.1f}), p = {pp:.4g}')
crit = P[(P.tipo == 'no_relacionado') & (P.k >= 3) & (P.d <= dstar) & (P.QA != 'no') & (P.QB != 'no') & (P.p_colA < .01) & (P.p_colB < .01)]
a_, b_ = P[(P.tipo == 'mismo_archivo') & (P.k >= 3)], P[(P.tipo == 'no_relacionado') & (P.k >= 3)]
say(f'  Fisher k>=3, d<=d* dentro de archivo {(a_.d<=dstar).mean():.3f} vs no relacionados {(b_.d<=dstar).mean():.3f}: OR, p =', stats.fisher_exact([[(a_.d<=dstar).sum(), (a_.d>dstar).sum()], [(b_.d<=dstar).sum(), (b_.d>dstar).sum()]]))
say('  pares no relacionados k>=3 con d<=d*:'); say(b_[b_.d <= dstar][['motivo', 'A', 'B', 'procA', 'procB', 'estricto', 'd', 'p_colA', 'p_colB', 'QA', 'QB']].to_string())
b2 = P[(P.tipo == 'no_relacionado') & (P.k == 2)]
sa = [np.sign(float(r.perfilA.split('/')[0])) == np.sign(float(r.perfilB.split('/')[0])) for r in b2.itertuples()]
say(f'  k=2 no relacionados: mismo sentido de la razón en {np.mean(sa):.3f} de {len(sa)} (binomial p = {stats.binomtest(sum(sa), len(sa)).pvalue:.3g}); motivos: {b2.motivo.value_counts().head(5).to_dict()}')
say(f'  pares que cumplen el criterio individual de refutación (k>=3, ambos Q, p_col<.01, d<=d*): {len(crit)}')
say(crit.drop(columns=['_pa', '_pb']).to_string() if len(crit) else '  (ninguno)')
say('  motivos k>=3 compartidos por pares no relacionados (top 10):', P[(P.tipo == 'no_relacionado') & (P.k >= 3)].motivo.value_counts().head(10).to_dict())
P.drop(columns=['_pa', '_pb']).to_csv(AQ + 'refutacion_pares.csv', index=False)

# ---------- suplemento post hoc (declarado): Incahuasi P9 no entró por el tope de 3 tipos por familia ----------
s_ = ARCH['procedencia:Incahuasi']; t9 = ('P', 'P9')
E9 = [k for k in sorted(s_) if MITAD[k] == 'E' and t9 in CAND[k]]
V9 = [bloques(Q[k], *t9) for k in E9]; pi9 = np.mean([perfil(V) for V in V9], 0)
C9 = {k: bloques(Q[k], *t9) for k in sorted(s_) if MITAD[k] == 'C'}; C9 = {k: V for k, V in C9.items() if len(V) >= 2}
T9, p9 = conf_test(list(C9.values()), pi9)
say(f'\n== suplemento post hoc: Incahuasi P9: E={E9} (p_E={anova(np.vstack(V9))[0]:.2g}), C={list(C9)} bloques {sum(map(len, C9.values()))}; p_C = {p9:.4g}')
say('   cuotas E', np.round(np.vstack([V / V.sum(1, keepdims=True) for V in V9]).mean(0), 3), '| cuotas C', np.round(np.vstack([V / V.sum(1, keepdims=True) for V in C9.values()]).mean(0), 3))
U = F[F.q_bh < .05].drop_duplicates(['fam', 'clave', 'quipus_E', 'quipus_C'])
say(f'formularios de archivo confirmados (BH) distintos, sin duplicar archivos con los mismos quipus: {len(U)}; por conjunto de quipus: {U.groupby(["quipus_E","quipus_C"]).ngroups}')

# ---------- §7 tasa ----------
G = R[R.n_cuerdas >= 30]
miembros_conf = set()
for r_ in F[F.q_bh < .05].itertuples():
    miembros_conf |= set(r_.quipus_con_tipo.split())
say(f'\n== §7 tasa: quipus con >=30 cuerdas: {len(G)}')
for lab, msk in (('Q (cualquiera)', G.Q != 'no'), ('Q posicional', G.Q == 'posicional'), ('Q cromático', G.Q == 'cromatico'),
                 ('Q+ (con coescala de bloques)', G.Qplus), ('Holm<.05', G.holm < .05),
                 ('miembro de formulario de archivo confirmado', G.index.isin(miembros_conf))):
    n = int(msk.sum()); lo, hi = stats.binomtest(n, len(G)).proportion_ci()
    say(f'  {lab:45s} {n:4d} = {n/len(G):.3f} [{lo:.3f}, {hi:.3f}]')
say('  banderas entre los Q: total+partes', int(G[G.Q != 'no'].total_partes.fillna(False).astype(bool).sum()),
    '| lista ordenada', int(G[G.Q != 'no'].lista_ordenada.fillna(False).astype(bool).sum()),
    '| filas casi idénticas', int(G[G.Q != 'no'].filas_casi_identicas.fillna(False).astype(bool).sum()))
say('  Q por procedencia (top):', pd.crosstab(q.set_index('kfg').loc[G.index, 'procedencia'], G.Q != 'no').sort_values(True, ascending=False).head(10).to_dict('index'))
open(AQ + 'salida_archivos.txt', 'w', encoding='utf-8').write('\n'.join(L))
