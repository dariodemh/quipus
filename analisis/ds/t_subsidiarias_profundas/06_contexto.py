# -*- coding: utf-8 -*-
"""Contexto: procedencia, tamano, posicion en el quipu, color, longitud,
presencia de valores y repeticiones. Nulos de permutacion donde aplica.

Salida: contexto.txt (texto corto) y contexto.json
"""
import pandas as pd, numpy as np, os, json, re
from collections import defaultdict, Counter

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
rng = np.random.default_rng(11)

d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
q = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'quipus.csv'))
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan

def base_color(c):
    if not isinstance(c, str): return None
    m = re.match(r'^[A-Z0-9]{1,2}', c)
    return m.group(0) if m else None

d['bc'] = d.color.map(base_color)
res = {}

# --- 1. prevalencia por procedencia
D = T.groupby('kfg').size().rename('n_arboles').reset_index()
allq = q[['kfg', 'procedencia', 'region', 'pc_largo']].merge(D, on='kfg', how='left').fillna({'n_arboles': 0})
allq['profundo'] = allq.n_arboles > 0
allq['ncuerdas'] = allq.kfg.map(d.groupby('kfg').size())
tab = allq.groupby('procedencia').agg(quipus=('kfg', 'size'), con_profundo=('profundo', 'sum'))
tab['pct'] = 100 * tab.con_profundo / tab.quipus
res['proc'] = tab.sort_values('con_profundo', ascending=False).head(12).to_dict('index')
print('Prevalencia por procedencia (top):')
print(tab.sort_values(['con_profundo', 'quipus'], ascending=False).head(10).to_string())

from scipy.stats import fisher_exact, mannwhitneyu
inc = allq.procedencia.astype(str).str.contains('Incahuasi', case=False)
a = int(allq[inc].profundo.sum()); b = int(inc.sum() - a)
c = int(allq[~inc].profundo.sum()); e = int((~inc).sum() - c)
OR, pf = fisher_exact([[a, b], [c, e]])
print(f'Incahuasi: {a}/{a+b} vs resto {c}/{c+e} | OR={OR:.2f} p={pf:.2e}')
res['incahuasi'] = dict(a=a, b=b, c=c, e=e, OR=float(OR), p=float(pf))

# tamano del quipu
u = mannwhitneyu(allq[allq.profundo].ncuerdas, allq[~allq.profundo].ncuerdas, alternative='greater')
print('Cuerdas/quipu: profundo mediana %.0f vs resto %.0f | MWU p=%.2e' %
      (allq[allq.profundo].ncuerdas.median(), allq[~allq.profundo].ncuerdas.median(), u.pvalue))
res['tamano'] = dict(med_prof=float(allq[allq.profundo].ncuerdas.median()),
                     med_resto=float(allq[~allq.profundo].ncuerdas.median()), p=float(u.pvalue))

# --- 2. niveles: largo y presencia de valor (corpus vs arboles profundos)
print('\nPor nivel (corpus): n, %con valor, largo mediano')
lvl = d.groupby('nivel').agg(n=('cuerda', 'size'), conval=('v', lambda s: s.notna().mean()),
                             largo=('largo', 'median'))
print(lvl.head(9).to_string())

deep_cords = set()
for _, r in T.iterrows():
    g = d[d.kfg == r.kfg]
    ch = defaultdict(list)
    for cc, pp in zip(g.cuerda, g.padre):
        if isinstance(pp, str): ch[pp].append(cc)
    st = [r.raiz]
    while st:
        x = st.pop(); deep_cords.add((r.kfg, x)); st.extend(ch.get(x, []))
d['en_profundo'] = [(k, c) in deep_cords for k, c in zip(d.kfg, d.cuerda)]
print('\nDentro de arboles profundos, por nivel relativo al pendant:')
dd = d[d.en_profundo].copy()
root_niv = dd[dd.nivel == 0].set_index(['kfg', 'cuerda'])['nivel']
# nivel relativo = nivel - nivel del pendant del arbol (0 para raices)
# ya que las raices son nivel 0, rel = nivel
print(dd.groupby('nivel').agg(n=('cuerda', 'size'), conval=('v', lambda s: s.notna().mean()),
                              largo=('largo', 'median'), colores=('bc', 'nunique')).head(8).to_string())

# --- 3. color: hermanos distintos y madre-hijo
# precalcular estructura
COL = {(k, c): b for k, c, b in zip(d.kfg, d.cuerda, d.bc)}
STR = {}
for kfg, g in d[d.en_profundo].groupby('kfg'):
    ch = defaultdict(list)
    for cc, pp in zip(g.cuerda, g.padre):
        if isinstance(pp, str): ch[pp].append(cc)
    STR[kfg] = (ch, list(ch.items()))

def color_stats(colmap):
    dist, same = [], []
    for kfg, (ch, items) in STR.items():
        for p, ks in items:
            cc = [colmap.get((kfg, x)) for x in ks]
            cc = [x for x in cc if isinstance(x, str)]
            if len(cc) >= 2: dist.append(len(set(cc)) / len(cc))
            pc = colmap.get((kfg, p))
            if isinstance(pc, str):
                for k in ks:
                    kc = colmap.get((kfg, k))
                    if isinstance(kc, str): same.append(pc == kc)
    return np.mean(dist), np.mean(same), len(dist), len(same)

obs_d, obs_s, nn, edges = color_stats(COL)
print('\nArboles profundos: nodos con >=2 hijos con color: %d | distintos/media %.3f' % (nn, obs_d))
print('  aristas madre-hijo con color: %d | misma familia de color %.1f%%' % (edges, 100*obs_s))

# nulo: permutar colores dentro de cada quipu entre cuerdas con color
base_cols = {}
for kfg, g in d.groupby('kfg'):
    idx = g.index.to_numpy(); ok = idx[g.bc.notna().to_numpy()]
    base_cols[kfg] = ([(k, c) for k, c in zip(d.loc[ok, 'kfg'], d.loc[ok, 'cuerda'])], d.loc[ok, 'bc'].values)
nd, ns = [], []
for rep in range(500):
    cm = dict(COL)
    for kfg, (keys, vals) in base_cols.items():
        pv = rng.permutation(vals)
        for kk, vv in zip(keys, pv): cm[kk] = vv
    a, b, _, _ = color_stats(cm)
    nd.append(a); ns.append(b)
nd = np.array(nd); ns = np.array(ns)
p_d = (1 + (nd >= obs_d).sum()) / 501
p_s = (1 + (ns >= obs_s).sum()) / 501
print('  NULO color hermanos: obs %.3f nulo %.3f p=%.4f' % (obs_d, nd.mean(), p_d))
print('  NULO misma color: obs %.3f nulo %.3f p=%.4f' % (obs_s, ns.mean(), p_s))

# --- 4. posicion en el quipu: grupo y orden relativo
print('\nPosicion de los arboles profundos:')
T2 = T.merge(allq[['kfg', 'ncuerdas']], on='kfg')
T2['frac_orden'] = T2.raiz.map(lambda x: 0)
# orden de la raiz / total de cuerdas
ordmap = {(k, c): o for k, c, o in zip(d.kfg, d.cuerda, d.orden)}
T2['orden_raiz'] = [ordmap[(k, r)] for k, r in zip(T2.kfg, T2.raiz)]
T2['frac_orden'] = T2.orden_raiz / T2.ncuerdas
print('  grupos: mediana %d, rango %d-%d | grupo/total grupos' % (T2.grupo.median(), T2.grupo.min(), T2.grupo.max()))
print('  orden relativo en el quipu: mediana %.2f (0=izq, 1=der)' % T2.frac_orden.median())
print('  arboles en el primer 25%% del quipu: %.0f%%' % (100*(T2.frac_orden < .25).mean()))
# grupos totales por quipu
ng = d.groupby('kfg').grupo.nunique()
T2['grupo_frac'] = T2.grupo / T2.kfg.map(ng)
print('  grupo relativo: mediana %.2f' % T2.grupo_frac.median())

# --- 5. repeticiones de forma/valores dentro del quipu
def siblings(g):
    ch = defaultdict(list)
    for cc, pp in zip(g.cuerda, g.padre):
        if isinstance(pp, str): ch[pp].append(cc)
    return ch

sig = []
for _, r in T.iterrows():
    g = d[d.kfg == r.kfg]
    ch = siblings(g)
    nodes = [r.raiz]; st = [r.raiz]
    while st:
        x = st.pop()
        for k in ch.get(x, []): nodes.append(k); st.append(k)
    sub = g[g.cuerda.isin(nodes)].sort_values('orden')
    shape = tuple(sorted(len(ch.get(x, [])) for x in nodes))
    vals = tuple(sorted([round(float(x), 3) for x in sub.v.dropna()]))
    sig.append((r.kfg, shape, vals))
S = pd.DataFrame(sig, columns=['kfg', 'shape', 'vals'])
dup_shape = S.groupby(['kfg', 'shape']).size()
print('\nArboles con forma identica a otro del mismo quipu:',
      int(sum(v-1 for v in dup_shape if v > 1)), 'de', len(S))
print(dup_shape[dup_shape > 1].sort_values(ascending=False).head(6).to_string())

# --- 6. HP038: auto-similitud con los pendants p2..p8
h = d[d.kfg == 'HP038'].set_index('cuerda')
chain = ['p8s1s1', 'p8s1s1s8s1', 'p8s1s1s8s1s8s1', 'p8s1s1s8s1s8s1s8s1',
         'p8s1s1s8s1s8s1s8s1s9s1', 'p8s1s1s8s1s8s1s8s1s9s1s8s1',
         'p8s1s1s8s1s8s1s8s1s9s1s8s1s8s1']
orig = ['p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
print('\nHP038: cadena profunda vs pendants p2..p8 (color, largo)')
match = 0
for a, b in zip(chain, orig):
    ca, cb = base_color(h.at[a, 'color']), base_color(h.at[b, 'color'])
    la, lb = h.at[a, 'largo'], h.at[b, 'largo']
    match += (ca == cb)
    print('  %-38s %-4s %-4s | %5.1f vs %5.1f' % (a[-20:], ca, cb, la, lb))
print('  coincidencias de color: %d/7' % match)
res['hp038_color_match'] = int(match)
json.dump(res, open(os.path.join(OUT, 'contexto.json'), 'w'), indent=2, default=str)
