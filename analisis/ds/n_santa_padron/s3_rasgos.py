"""s3_rasgos.py -- test de orden con busqueda sobre rasgos (max-estadistico).
Pregunta: ¿existe ALGUN par (rasgo del nombre, rasgo del grupo) que se alinee
mejor de lo que permite el azar, corrigiendo por haber buscado muchos pares?
Nulo: permutar los nombres DENTRO de cada pachaca (destruye el orden, conserva
tamanos, margenes de nombres y composicion por pachaca). Semilla 1670.
Estadistico: informacion mutua AJUSTADA (AMI), que corrige por cardinalidad
(la V de Cramer se dispara con rasgos de muchos niveles y n=121).
"""
import pandas as pd, numpy as np, ast, json, warnings
from math import comb
from sklearn.metrics import adjusted_mutual_info_score as ami
warnings.filterwarnings('ignore')

rng = np.random.default_rng(1670)
B = 3000
G = pd.read_csv('santos_grupos133.csv'); P = pd.read_csv('padron_orden.csv')
G['col'] = G.color1.fillna('NA').str.replace(r'\([^)]*\)', '', regex=True)
G['vals'] = G.vals.apply(ast.literal_eval)
for i in range(6):
    G[f'p{i+1}'] = G.vals.apply(lambda v: v[i])
M = {'Namus': 'UR091', 'Corongo': 'UR090', 'Cuyuchin': 'UR092',
     'Cusca': 'UR088', 'Guauyan': 'UR087', 'Ucore': 'UR089'}
ORDEN = ['Namus', 'Corongo', 'Cuyuchin', 'Cusca', 'Guauyan', 'Ucore']

frames = []
for p in ORDEN:
    gg = G[G.kfg == M[p]].sort_values('g').reset_index(drop=True)
    pp = P[P.pachaca == p].reset_index(drop=True)
    n = min(len(pp), len(gg))
    d = pd.DataFrame(dict(pachaca=p, khipu=M[p], i=np.arange(n)))
    d['fn'] = pp.fnorm.values[:n]
    d['sn'] = pp.resto.fillna('').str.lower().str.strip().values[:n]
    d['hijo'] = pp.hijo_de.values[:n].astype(int)
    d['don'] = pp['don'].values[:n].astype(int)
    rep_fn, rep_sn, seen_f, seen_s = [], [], set(), set()
    for a, b in zip(d.fn, d.sn):
        rep_fn.append(int(a in seen_f)); rep_sn.append(int(b in seen_s and b != ''))
        seen_f.add(a); seen_s.add(b)
    d['rep_fn'] = rep_fn; d['rep_sn'] = rep_sn
    d['fn_freq'] = d.fn.map(d.fn.value_counts())
    d['pos'] = np.arange(n); d['pos_mod2'] = d.pos % 2
    d['col'] = gg.col.values[:n]
    d['solid'] = gg.col.str.contains(r'[:/\-]').values[:n].astype(int)
    d['union'] = gg.union1.values[:n]
    d['p1'] = gg.p1.values[:n]
    d['p1_0'] = (d.p1 == 0).astype(int)
    for j in range(2, 7):
        d[f'p{j}'] = gg[f'p{j}'].values[:n]
    frames.append(d)
D = pd.concat(frames, ignore_index=True)
print('marco alineado:', D.groupby('pachaca').size().to_dict(), 'n =', len(D))

def qbin(x):
    return pd.qcut(pd.Series(x).rank(method='first'), 3, labels=False).values \
        if pd.Series(x).nunique() > 2 else np.zeros(len(x), int)
D['p1_bin'] = qbin(D.p1.values); D['p4_bin'] = qbin(D.p4.values)
D['p2_bin'] = qbin(D.p2.values)
# rasgos de nombre de cardinalidad controlada (top-8 + resto)
for c, k in [('fn_top', ('fn', 8)), ('sn_top', ('sn', 8))]:
    src, kk = k
    top = D[src].value_counts().head(kk).index
    D[c] = np.where(D[src].isin(top), D[src], 'otro')

NAME_F = ['fn', 'fn_top', 'sn_top', 'hijo', 'don', 'rep_fn', 'rep_sn',
          'fn_freq', 'pos_mod2']
GROUP_F = ['col', 'solid', 'union', 'p1', 'p1_0', 'p1_bin', 'p4_bin', 'p2_bin']

def tabla(X):
    return {f'{a}|{b}': ami(X[a].astype(str), X[b].astype(str), average_method='arithmetic')
            for a in NAME_F for b in GROUP_F}

obs = tabla(D)
mx = max(obs.values()); best = max(obs, key=obs.get)
print('\nAMI max observada = %.3f en %s' % (mx, best))
print('top 10 pares:')
for k, x in sorted(obs.items(), key=lambda t: -t[1])[:10]:
    print('  %-18s %+.3f' % (k, x))

idx = {p: np.where(D.pachaca.values == p)[0] for p in ORDEN}
perm_cols = ['fn', 'fn_top', 'sn_top', 'hijo', 'don', 'rep_fn', 'rep_sn', 'fn_freq']
def permutar():
    X = D.copy()
    for p, ii in idx.items():
        for c in perm_cols:
            X.loc[ii, c] = rng.permutation(D.loc[ii, c].values)
    return X

nul_mx = np.empty(B); nul_best = np.empty(B)
for b in range(B):
    t = tabla(permutar())
    nul_mx[b] = max(t.values()); nul_best[b] = t[best]
p_mx = (np.sum(nul_mx >= mx)+1)/(B+1)
p_best = (np.sum(nul_best >= obs[best])+1)/(B+1)
print('\nnulo (%d permutaciones de nombres dentro de pachaca):' % B)
print('  max AMI: media %.3f p95 %.3f  ->  p (corregido por busqueda de %d pares) = %.4f'
      % (nul_mx.mean(), np.quantile(nul_mx, .95), len(obs), p_mx))
print('  el par %s por separado: p sin corregir = %.4f' % (best, p_best))

print('\n' + '='*70)
print('PRUEBA DIRIGIDA (post hoc): Namus, "hijo de" al final vs UR091 p1=0 al final')
print('hijo  =', D[D.pachaca=='Namus'].hijo.tolist(), '(solo los 15 alineados)')
print('p1_0  =', D[D.pachaca=='Namus'].p1_0.tolist())
print('P(5 hijos ocupan las 5 ultimas de 18) = 1/C(18,5) = %.6f' % (1/comb(18,5)))
print('P(6 ceros ocupan los 6 ultimos de 15) = 1/C(15,6) = %.6f' % (1/comb(15,6)))
print('P(ambos) = %.2e  <- el par de rasgos se eligio tras ver los datos' % (1/(comb(18,5)*comb(15,6))))
print('control valido = p del max-estadistico: %.4f' % p_mx)

json.dump(dict(obs=obs, maxAMI=mx, best=best, p_max=p_mx, p_best=p_best,
               null_max_mean=float(nul_mx.mean()), null_max_p95=float(np.quantile(nul_mx,.95))),
          open('res_rasgos.json', 'w'), indent=1)
