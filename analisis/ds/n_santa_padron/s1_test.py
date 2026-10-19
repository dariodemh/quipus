"""s1_test.py -- pruebas de orden padron 1670 <-> grupos de los quipus del Santa.
Semilla fija 1670. Todos los nulos son permutaciones que destruyen el ORDEN
de los nombres dentro de cada pachaca (o el emparejamiento pachaca-quipu).
"""
import pandas as pd, numpy as np, ast, itertools, re, json
from scipy import stats
from math import comb

rng = np.random.default_rng(1670)
B = 20000  # permutaciones

G = pd.read_csv('santos_grupos133.csv')
P = pd.read_csv('padron_orden.csv')
G['col'] = G.color1.fillna('NA').str.replace(r'\([^)]*\)', '', regex=True)   # 33 niveles
G['vals'] = G.vals.apply(ast.literal_eval)
for i in range(6):
    G[f'p{i+1}'] = G.vals.apply(lambda v: v[i])
G['p1'] = G.p1

M = {'Namus': 'UR091', 'Corongo': 'UR090', 'Cuyuchin': 'UR092',
     'Cusca': 'UR088', 'Guauyan': 'UR087', 'Ucore': 'UR089'}
ORDEN_DOC = ['Namus', 'Corongo', 'Cuyuchin', 'Cusca', 'Guauyan', 'Ucore']
TRIB = {p: int((P.pachaca == p).sum()) for p in ORDEN_DOC}
GRP = G.groupby('kfg').size().to_dict()

print('='*70)
print('1. DESCRIPTIVOS')
print('tributarios por pachaca (padron):', TRIB, 'total', sum(TRIB.values()))
print('grupos de 6 por quipu:', {k: GRP[k] for k in GRP}, 'total', len(G))
print('colores distintos 1.a cuerda:', G.col.nunique(),
      '|singletons:', int((G.col.value_counts() == 1).sum()),
      '  (publicado: 32 y 17)')
print('rango p1 por quipu:', G.groupby('kfg').p1.agg(['min', 'max', 'sum']).to_dict('index'))
print('grupos con color homogeneo en las 6 cuerdas:', int((G.nhom == 1).sum()), '/', len(G))
print('union 1.a cuerda por quipu:', G.groupby(['kfg', 'union1']).size().unstack(fill_value=0).to_dict('index'))

# ------------------------------------------------------------------ 2. MACRO
print('\n' + '='*70)
print('2. TEST MACRO: orden/emparejamiento pachaca <-> quipu')
trib = np.array([TRIB[p] for p in ORDEN_DOC])
gr = np.array([GRP[M[p]] for p in ORDEN_DOC])
print('pachacas (orden del documento):', ORDEN_DOC)
print('tributarios:', trib.tolist(), ' grupos:', gr.tolist())
print('suma |diferencia| observada =', int(np.abs(trib-gr).sum()),
      ' Spearman =', round(stats.spearmanr(trib, gr)[0], 3))

# nulo 2a: permutar la asignacion de los 6 quipus a las 6 pachacas (720 permutaciones)
sizes = np.array([GRP[k] for k in ['UR087','UR088','UR089','UR090','UR091','UR092']])
obs = np.abs(trib - gr).sum()
vals = []
for perm in itertools.permutations(sizes):
    vals.append(np.abs(trib - np.array(perm)).sum())
vals = np.array(vals)
print('nulo 2a (720 permutaciones de quipus): min posible', vals.min(),
      ' P(sum|dif| <= obs) =', round((vals <= obs).mean(), 4),
      ' n permutaciones con ese valor =', int((vals == obs).sum()))

# nulo 2b: composiciones aleatorias de 133 en 6 partes, emparejadas por rango (ya en 12)
def comp(n=133, k=6):
    cuts = np.sort(rng.choice(np.arange(1, n), k-1, replace=False))
    return np.diff(np.r_[0, cuts, n])
d0 = np.abs(np.sort(trib) - np.sort(gr)).sum()
nul = np.array([np.abs(np.sort(trib) - np.sort(comp())) .sum() for _ in range(B)])
print('nulo 2b (composiciones uniformes, emparejamiento por rango): obs', int(d0),
      ' P(<=obs) =', round((nul <= d0).mean(), 3))

# ------------------------------------------------------------------ 3. MICRO
print('\n' + '='*70)
print('3. TEST MICRO: orden de los nombres vs orden de los grupos')

def pares(p):
    """Devuelve (nombres, colores, valores p1) alineados por posicion desde el inicio."""
    k = M[p]
    gg = G[G.kfg == k].sort_values('g').reset_index(drop=True)
    pp = P[P.pachaca == p].reset_index(drop=True)
    n = min(len(pp), len(gg))
    return (pp.fnorm.values[:n], gg.col.values[:n], gg.p1.values[:n],
            pp, gg, n)

def cramersv(a, b):
    tab = pd.crosstab(pd.Series(a), pd.Series(b))
    chi2 = stats.chi2_contingency(tab, correction=False)[0]
    n = tab.values.sum()
    return np.sqrt(chi2 / (n * (min(tab.shape) - 1)))

def acc_mapping(cols, names):
    """precision in-sample: cada color se asigna al nombre modal."""
    df = pd.DataFrame({'c': cols, 'n': names})
    ok = 0
    for c, x in df.groupby('c'):
        ok += x.n.value_counts().iloc[0]
    return ok / len(df)

# --- 3.1 hipotesis explicita de Medrano y Urton: color = nombre de pila, en orden
rows = []
for p in ORDEN_DOC:
    nm, co, p1, pp, gg, n = pares(p)
    rows.append(dict(pachaca=p, khipu=M[p], n_aligned=n, n_nombres=len(pp), n_grupos=len(gg),
                     V=cramersv(co, nm), acc=acc_mapping(co, nm)))
R = pd.DataFrame(rows)
print(R.round(3).to_string(index=False))

# agrupado: concatenar los pares alineados
allnm, allco = [], []
for p in ORDEN_DOC:
    nm, co, p1, pp, gg, n = pares(p)
    allnm += list(nm); allco += list(co)
allnm = np.array(allnm); allco = np.array(allco)
V_obs = cramersv(allco, allnm)
A_obs = acc_mapping(allco, allnm)
print('\nagregado: n =', len(allnm), ' V observada =', round(V_obs, 3),
      ' precision in-sample =', round(A_obs, 3),
      ' (nivel azar por color =', round((pd.Series(allnm).value_counts()/len(allnm)**1).max(), 1), ')')

# nulo: permutar nombres dentro de cada pachaca
def permutar_nombres():
    out = []
    for p in ORDEN_DOC:
        nm, co, p1, pp, gg, n = pares(p)
        out += list(rng.permutation(nm))
    return np.array(out)

Vs, As = [], []
for b in range(B if B <= 5000 else 5000):
    pn = permutar_nombres()
    Vs.append(cramersv(allco, pn))
    As.append(acc_mapping(allco, pn))
Vs = np.array(Vs); As = np.array(As)
pV = (np.sum(Vs >= V_obs) + 1) / (len(Vs) + 1)
pA = (np.sum(As >= A_obs) + 1) / (len(As) + 1)
print('nulo (permutar nombres dentro de pachaca, %d): V media %.3f p95 %.3f -> p = %.4f'
      % (len(Vs), Vs.mean(), np.quantile(Vs, .95), pV))
print('                                              precision media %.3f p95 %.3f -> p = %.4f'
      % (As.mean(), np.quantile(As, .95), pA))

json.dump(dict(V_obs=V_obs, pV=pV, A_obs=A_obs, pA=pA,
               Vnull_mean=float(Vs.mean()), Vnull_p95=float(np.quantile(Vs, .95)),
               Anull_mean=float(As.mean()), Anull_p95=float(np.quantile(As, .95)),
               per_khipu=R.to_dict('records')),
          open('res_31.json', 'w'), indent=1)
