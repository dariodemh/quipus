"""s2_orden.py -- profundiza el test de orden: variantes de alineacion, controles
negativos, periodicidad de color vs nombres, y bloques Namus/UR091.
Semilla 1670."""
import pandas as pd, numpy as np, ast, itertools, json
from scipy import stats
from math import comb

rng = np.random.default_rng(1670)
B = 10000
G = pd.read_csv('santos_grupos133.csv'); P = pd.read_csv('padron_orden.csv')
G['col'] = G.color1.fillna('NA').str.replace(r'\([^)]*\)', '', regex=True)
G['vals'] = G.vals.apply(ast.literal_eval)
for i in range(6):
    G[f'p{i+1}'] = G.vals.apply(lambda v: v[i])

M = {'Namus': 'UR091', 'Corongo': 'UR090', 'Cuyuchin': 'UR092',
     'Cusca': 'UR088', 'Guauyan': 'UR087', 'Ucore': 'UR089'}
ORDEN = ['Namus', 'Corongo', 'Cuyuchin', 'Cusca', 'Guauyan', 'Ucore']

def par(p, k=None):
    k = k or M[p]
    gg = G[G.kfg == k].sort_values('g').reset_index(drop=True)
    pp = P[P.pachaca == p].reset_index(drop=True)
    n = min(len(pp), len(gg))
    return pp.fnorm.values[:n], gg.col.values[:n], gg.p1.values[:n]

def concat(order_names=True):
    nm, co, p1 = [], [], []
    for p in ORDEN:
        a, b, c = par(p); nm += list(a); co += list(b); p1 += list(c)
    return np.array(nm), np.array(co), np.array(p1)

def cramersv(a, b):
    tab = pd.crosstab(pd.Series(a), pd.Series(b))
    chi2 = stats.chi2_contingency(tab, correction=False)[0]
    return np.sqrt(chi2 / (tab.values.sum() * (min(tab.shape) - 1)))

def acc(cols, names):
    df = pd.DataFrame({'c': cols, 'n': names})
    return sum(x.n.value_counts().iloc[0] for _, x in df.groupby('c')) / len(df)

def acc_heldout(cols, names):
    """ajusta color->nombre en posiciones pares, evalua en impares"""
    df = pd.DataFrame({'c': cols, 'n': names, 'i': np.arange(len(names))})
    tr, te = df[df.i % 2 == 0], df[df.i % 2 == 1]
    mp = {c: x.n.value_counts().index[0] for c, x in tr.groupby('c')}
    return np.mean([mp.get(r.c, '') == r.n for r in te.itertuples()])

nm, co, p1 = concat()
print('n alineado total', len(nm))

# ---------------- 4.1 variantes de alineacion ----------------
print('\n' + '='*70)
print('4. VARIANTES DE ALINEACION (estadistico = V de Cramer color vs nombre)')
res = []
V0 = cramersv(co, nm)
def perm(B, rev=False, off=0):
    out = []
    for b in range(B):
        s = []
        for p in ORDEN:
            a, _, _ = par(p)
            a = a[::-1] if rev else a
            s += list(rng.permutation(a))
        out.append(s)
    return out

for etiqueta, rev, off in [('orden del documento', False, 0), ('orden invertido', True, 0)]:
    obs_v = V0 if not rev else cramersv(co, np.concatenate([par(p)[0][::-1] for p in ORDEN]))
    nul = []
    for b in range(3000):
        s = []
        for p in ORDEN:
            a, _, _ = par(p)
            a = a[::-1] if rev else a
            s += list(rng.permutation(a))
        nul.append(cramersv(co, np.array(s)))
    nul = np.array(nul)
    p = (np.sum(nul >= obs_v)+1)/(len(nul)+1)
    print('  %-22s V=%.3f  nulo medio %.3f p95 %.3f  p=%.4f' % (etiqueta, obs_v, nul.mean(), np.quantile(nul,.95), p))
    res.append((etiqueta, obs_v, p))

# desplazamientos (offset): alinear nombre i con grupo i+off
print('\ndesplazamiento (nombre i con grupo i+off), V:')
for off in range(-5, 6):
    aa, bb = [], []
    for p in ORDEN:
        a, b, _ = par(p)
        if off >= 0:
            a2, b2 = a[:len(a)-off], b[off:]
        else:
            a2, b2 = a[-off:], b[:len(b)+off]
        aa += list(a2); bb += list(b2)
    print('  off=%+d n=%3d V=%.3f' % (off, len(aa), cramersv(bb, aa)))

# ---------------- 4.2 controles negativos ----------------
print('\n' + '='*70)
print('5. CONTROLES NEGATIVOS (precision in-sample color->nombre)')
A0 = acc(co, nm)
# (a) nulo de permutacion (ya calculado en s1) -- repetimos con B=10000
nulA = []
for b in range(B):
    s = []
    for p in ORDEN:
        a, _, _ = par(p); s += list(rng.permutation(a))
    nulA.append(acc(co, np.array(s)))
nulA = np.array(nulA)
pA = (np.sum(nulA >= A0)+1)/(len(nulA)+1)
print('(a) nulo de orden: A=%.3f nulo medio %.3f p95 %.3f p=%.4f' %
      (A0, nulA.mean(), np.quantile(nulA, .95), pA))

# (b) emparejamientos equivocados: 720 asignaciones pachaca->quipu
print('(b) las 720 asignaciones pachaca-quipu (V y precision agregadas):')
rows = []
for perm in itertools.permutations([G[G.kfg==k] for k in M.values()]):
    pass
ks = ['UR087','UR088','UR089','UR090','UR091','UR092']
VA, AA = [], []
for perm in itertools.permutations(ks):
    mp = dict(zip(ORDEN, perm))
    a_, b_ = [], []
    for p in ORDEN:
        gg = G[G.kfg==mp[p]].sort_values('g').reset_index(drop=True)
        pp = P[P.pachaca==p].reset_index(drop=True)
        n = min(len(pp), len(gg))
        a_ += list(pp.fnorm.values[:n]); b_ += list(gg.col.values[:n])
    VA.append(cramersv(b_, a_)); AA.append(acc(b_, a_))
VA = np.array(VA); AA = np.array(AA)
print('    V: obs %.3f | media %.3f | max %.3f | rango del percentil de lo observado: %.3f'
      % (V0, VA.mean(), VA.max(), (VA < V0).mean()))
print('    A: obs %.3f | media %.3f | max %.3f | percentil: %.3f'
      % (A0, AA.mean(), AA.max(), (AA < A0).mean()))

# (c) orden aleatorio de los grupos dentro de cada quipu (destruye el orden real
#     pero conserva todo lo demas) -- equivalente al nulo de (a), ya hecho.

# (d) khipus de control del corpus: mismos tamanos, misma estructura de 6?
print('(d) ver s3_control_corpus.py')

# ---------------- 4.3 periodicidad ----------------
print('\n' + '='*70)
print('6. PERIODICIDAD: color vs nombres (fraccion de coincidencias a distancia k)')
def ac(seq, lag):
    return np.mean([seq[i] == seq[i+lag] for i in range(len(seq)-lag)])
for p in ORDEN:
    a, b, _ = par(p)
    print(' %-9s n=%2d  color: ' % (p, len(b)) + ' '.join('%d:%.2f' % (L, ac(b, L)) for L in (1,2,3,4,5,6)) +
          '   nombre: ' + ' '.join('%d:%.2f' % (L, ac(a, L)) for L in (1,2,3,4,5,6)))
print('\n(para comparar: coincidencia esperada por azar con m categorias ~ 1/m)')
print('colores distintos por quipu:', G.groupby('kfg').col.nunique().to_dict())

# ---------------- 4.4 bloque Namus / UR091 ----------------
print('\n' + '='*70)
print('7. BLOQUES Namus: "hijo de" (ultimos 5) vs p1=0 en UR091 (ultimos 6)')
pp = P[P.pachaca=='Namus'].reset_index(drop=True)
gg = G[G.kfg=='UR091'].sort_values('g').reset_index(drop=True)
print('nombres 13-17:', pp.nombre.values[13:].tolist())
print('hijo_de por posicion:', pp.hijo_de.astype(int).tolist())
print('p1 UR091 por grupo:', gg.p1.tolist())
print('union:', gg.union1.tolist())
print('P(6 ultimos de 15 son justo los 6 con p1=0 | 6 ceros al azar) = 1/C(15,6) = %.5f'
      % (1/comb(15,6)))
# test conjunto: 5 hijos de 18 al final Y 6 ceros de 15 al final
print('P(ambos bloques al final por azar) = 1/(C(18,5)*C(15,6)) = %.2e'
      % (1/(comb(18,5)*comb(15,6))))
# pero el estadistico se eligio tras mirar: max sobre 2x5 rasgos binarios
print('  (post hoc: ver s3 para el max-estadistico sobre rasgos)')
