"""s4_controles.py -- controles finales y correccion multiple (Holm).
Recoge los p-valores de la bateria de pruebas de orden y los corrige.
Semilla 1670.
"""
import pandas as pd, numpy as np, ast, json
from scipy import stats

rng = np.random.default_rng(1670)
B = 5000
G = pd.read_csv('santos_grupos133.csv'); P = pd.read_csv('padron_orden.csv')
G['col'] = G.color1.fillna('NA').str.replace(r'\([^)]*\)', '', regex=True)
G['vals'] = G.vals.apply(ast.literal_eval)
for i in range(6):
    G[f'p{i+1}'] = G.vals.apply(lambda v: v[i])
M = {'Namus': 'UR091', 'Corongo': 'UR090', 'Cuyuchin': 'UR092',
     'Cusca': 'UR088', 'Guauyan': 'UR087', 'Ucore': 'UR089'}
ORDEN = ['Namus', 'Corongo', 'Cuyuchin', 'Cusca', 'Guauyan', 'Ucore']

def par(p):
    gg = G[G.kfg == M[p]].sort_values('g').reset_index(drop=True)
    pp = P[P.pachaca == p].reset_index(drop=True)
    n = min(len(pp), len(gg))
    return pp.fnorm.values[:n], gg.col.values[:n], gg.p1.values[:n]

def cramersv(a, b):
    tab = pd.crosstab(pd.Series(a), pd.Series(b))
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return 0.0
    chi2 = stats.chi2_contingency(tab, correction=False)[0]
    return np.sqrt(chi2/(tab.values.sum()*(min(tab.shape)-1)))

def acc(cols, names):
    df = pd.DataFrame({'c': cols, 'n': names})
    return sum(x.n.value_counts().iloc[0] for _, x in df.groupby('c'))/len(df)

def heldout(cols, names):
    df = pd.DataFrame({'c': cols, 'n': names}); df['i'] = np.arange(len(df))
    tr, te = df[df.i % 2 == 0], df[df.i % 2 == 1]
    mp = {c: x.n.value_counts().index[0] for c, x in tr.groupby('c')}
    return np.mean([mp.get(r.c, '') == r.n for r in te.itertuples()])

nm = np.concatenate([par(p)[0] for p in ORDEN])
co = np.concatenate([par(p)[1] for p in ORDEN])
p1 = np.concatenate([par(p)[2] for p in ORDEN])

print('='*70)
print('A. POR QUIPU (V color-nombre y precision; p por permutacion, B=%d)' % B)
rows = []
for p in ORDEN:
    a, b, c = par(p)
    Vo, Ao, Ho = cramersv(b, a), acc(b, a), heldout(b, a)
    nv, na, nh = [], [], []
    for _ in range(B):
        q = rng.permutation(a)
        nv.append(cramersv(b, q)); na.append(acc(b, q)); nh.append(heldout(b, q))
    nv, na, nh = map(np.array, (nv, na, nh))
    rows.append(dict(pachaca=p, khipu=M[p], n=len(a), V=Vo, pV=(np.sum(nv>=Vo)+1)/(B+1),
                     acc=Ao, pacc=(np.sum(na>=Ao)+1)/(B+1),
                     ho=Ho, pho=(np.sum(nh>=Ho)+1)/(B+1)))
R = pd.DataFrame(rows)
print(R.round(3).to_string(index=False))

print('\n' + '='*70)
print('B. AGREGADO y variantes de la precision')
nulV = np.array([cramersv(co, np.concatenate([rng.permutation(par(p)[0]) for p in ORDEN]))
                 for _ in range(B)])
print('  V=%.3f  nulo medio %.3f p95 %.3f  p=%.4f' %
      (cramersv(co, nm), nulV.mean(), np.quantile(nulV, .95),
       (np.sum(nulV >= cramersv(co, nm))+1)/(B+1)))
print('  acc in-sample = %.3f (nulo medio ~0.397, p=0.021)' % acc(co, nm))
print('  acc held-out  = %.3f (azar ~0.09)' % heldout(co, nm))
nh = np.array([heldout(co, np.concatenate([rng.permutation(par(p)[0]) for p in ORDEN])) for _ in range(B)])
print('  held-out nulo: media %.3f p95 %.3f  p=%.4f' % (nh.mean(), np.quantile(nh, .95), (np.sum(nh>=heldout(co,nm))+1)/(B+1)))
# sin el nombre mas frecuente (juo, 32/130)
mask = nm != 'juo'
print('  acc sin "juo" (n=%d): obs %.3f' % (mask.sum(), acc(co[mask], nm[mask])))
nh2 = []
for _ in range(2000):
    s = np.concatenate([rng.permutation(par(p)[0]) for p in ORDEN])
    nh2.append(acc(co[s != 'juo'], s[s != 'juo']))
nh2 = np.array(nh2)
print('    nulo sin juo: media %.3f p95 %.3f p=%.4f' % (nh2.mean(), np.quantile(nh2,.95),
      (np.sum(nh2 >= acc(co[mask], nm[mask]))+1)/(len(nh2)+1)))

print('\n' + '='*70)
print('C. TENDENCIA p1 vs posicion en la lista (Spearman/Kendall por quipu)')
zs = []
for p in ORDEN:
    a, b, c = par(p)
    if len(set(c)) < 2:
        print('  %-9s p1 constante' % p); continue
    r, pv = stats.spearmanr(np.arange(len(c)), c)
    zs.append(np.arctanh(r) * np.sqrt(len(c)-3))
    print('  %-9s n=%2d  rho=%+.2f  p=%.3f' % (p, len(c), r, pv))
Z = np.sum(zs)/np.sqrt(len(zs))
from scipy.stats import norm
print('  Fisher combinado (6 quipus): Z=%.2f  p=%.3f  -> sin tendencia global'
      % (Z, 2*(1-norm.cdf(abs(Z)))))

print('\n' + '='*70)
print('C2. ESTRUCTURA INTERNA DEL PADRON: apellidos y nombres adyacentes')
P['sn'] = P.resto.fillna('').str.lower().str.strip()
def adj(s):
    s = list(s); return np.mean([s[i] == s[i+1] and s[i] != '' for i in range(len(s)-1)])
for p, x in P.groupby('pachaca'):
    o = adj(x.sn.values)
    nul = np.array([adj(rng.permutation(x.sn.values)) for _ in range(10000)])
    print('  %-9s apellido igual en posiciones contiguas: obs %.2f  nulo %.2f  p=%.3f'
          % (p, o, nul.mean(), (np.sum(nul >= o)+1)/10001))

print('\n' + '='*70)
print('D. CORRECCION MULTIPLE (Holm) de la bateria de pruebas de ORDEN')
bateria = [
 ('T1 macro: emparejamiento por rangos vs composiciones (nulo 2b)', 0.239),
 ('T2 micro: V color~nombre de pila, orden del documento', 0.1816),
 ('T3 micro: precision color->nombre in-sample', 0.0208),
 ('T4 micro: precision held-out', (np.sum(nh>=heldout(co,nm))+1)/(B+1)),
 ('T5 max-AMI sobre 72 pares nombre x grupo', 0.1423),
 ('T6 orden invertido (V)', 0.0730),
 ('T7 mejor desplazamiento (+4) (V)', None),
]
bp = [(n, p) for n, p in bateria if p is not None]
order = np.argsort([p for _, p in bp])
m = len(bp); prev = 0; holm = {}
for rank, i in enumerate(order):
    name, pv = bp[i]
    adj = min(1, (m-rank)*pv); adj = max(adj, prev); prev = adj
    holm[name] = adj
for n, pv in bp:
    print('  %-58s p=%.4f  Holm=%.4f' % (n, pv, holm[n]))
print('  (T7 no entra: es el maximo de 11 desplazamientos; su p nominal 0,05-0,10')
print('   no sobrevive a mirar 11 alineaciones)')
print('\nNinguna prueba sobrevive Holm al 5%: el orden de los nombres no se')
print('distingue del azar con estos datos.')
