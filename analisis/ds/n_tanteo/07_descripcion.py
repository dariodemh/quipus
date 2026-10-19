# -*- coding: utf-8 -*-
"""Descriptivos para el informe: cuotas, perfiles, UR277/272/276/279, escaleras."""
import numpy as np, pandas as pd
from scipy import stats
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv'); c['valor'] = c.valor.fillna(0)
c = c[c.kfg.isin(Q)]
part = pd.read_csv('ds/n_tanteo/particion.csv')
TAG = {(r.kfg, r.unidad, int(r.id)): r.mitad for _, r in part.iterrows()}

def recs(k):
    g = c[(c.kfg == k) & (c.nivel == 0)]
    out = []
    for gr, gg in g.groupby('grupo'):
        gg = gg.sort_values('orden')
        out.append(dict(grupo=int(gr), vals=gg.valor.astype(int).tolist(), cab=int(gg.valor.iloc[0])))
    return sorted(out, key=lambda x: x['grupo'])

out = []
# --- cuotas y tasas ---
for k, q in [('UR275', 47), ('UR266', 47), ('UR268', 208)]:
    rs = [r for r in recs(k) if r['cab'] > 0 and q in r['vals'][1:]]
    rate = np.array([q / r['cab'] for r in rs])
    out.append((k, 'tasa cuota/cabecera', len(rs), round(rate.mean()*100, 2),
                round(rate.min()*100, 2), round(rate.max()*100, 2)))
# UR269: cuota explicita
rs = [r for r in recs('UR269') if r['cab'] > 0]
C = {25, 40, 44, 46, 47}; rr = []
for r in rs:
    qq = next((v for v in r['vals'][1:] if v in C), None)
    if qq and r['cab'] > 0: rr.append(qq / r['cab'])
out.append(('UR269', 'tasa cuota/cabecera', len(rr), round(np.mean(rr)*100, 2),
            round(min(rr)*100, 2), round(max(rr)*100, 2)))
# cuota modal por quipu
for k in ['UR275','UR266','UR269','UR268']:
    vals = [v for r in recs(k) for v in r['vals'][1:] if v in {25,40,44,46,47,208}]
    out.append((k, 'cuota modal', len(vals), pd.Series(vals).mode().iloc[0], '', ''))

for row in out: print(row)
# --- perfil 9 columnas UR278 ---
def rows9(k):
    g = c[(c.kfg == k) & (c.nivel == 0)]
    out = []
    for gr, gg in g.groupby('grupo'):
        v = gg.sort_values('orden').valor.astype(int).tolist()
        if len(v) == 9 and sum(v) > 0:
            out.append(np.array(v))
    return out
V = np.array(rows9('UR278')); P = V / V.sum(1, keepdims=True)
print('UR278 filas 9 col:', len(V))
print('perfil % medio:', np.round(P.mean(0)*100, 1).tolist())
print('sd %:', np.round(P.std(0)*100, 1).tolist())
print('CV intra-fila medio:', round(float((V.std(1)/V.mean(1)).mean()), 3))
print('correlacion |share - total| por columna:', [round(float(abs(np.corrcoef(P[:,j], V.sum(1))[0,1])),2) for j in range(9)])
print('filas con orden exacto c1>c2>...:', int(sum(all(np.diff(v) < 0) for v in V)))

# --- UR277 / UR272 ---
for k in ['UR277','UR272']:
    vals = np.array([v for r in recs(k) for v in r['vals']])
    small = vals[vals <= 60]
    print(f'{k}: cordones {len(vals)}, <=60 {len(small)} ({100*len(small)/len(vals):.0f} %), '
          f'mediana {np.median(small):.0f}, p10-p90 {np.percentile(small,10):.0f}-{np.percentile(small,90):.0f}, '
          f'max {vals.max()}, >100 {int((vals>100).sum())}')
# --- UR276 / UR279 ---
print('UR276: 5 colgantes, valores', recs('UR276')[0]['vals'])
print('UR279: 12 colgantes, valores', recs('UR279')[0]['vals'])

# --- escaleras d=100 entre UR269, UR278, UR266/275 ---
v269 = sorted({v for r in recs('UR269') for v in r['vals'] if v > 0})
s278 = sorted({int(v.sum()) for v in V})
v266 = sorted({r['cab'] for r in recs('UR266') if r['cab'] > 0})
v275 = sorted({r['cab'] for r in recs('UR275') if r['cab'] > 0})
def ladders(a, b, d, step=100):
    sb = set(b); return [(x, x+step, x+2*step) for x in a if x+step in sb and x+2*step in d]
print('escaleras +100 UR269->UR278->UR266:', ladders(v269, s278, set(v266)))
print('escaleras +100 UR269->UR278->UR275:', ladders(v269, s278, set(v275)))
print('escaleras -100:', ladders(v269, s278, set(v266), -100))

# --- detalle de la escalera conocida ---
for v in [2433, 2533, 2633]:
    print('valor', v, 'en UR269' if v in v269 else '', 'en sumas UR278' if v in s278 else '',
          'en cab UR266' if v in v266 else '', 'en cab UR275' if v in v275 else '')

# --- control aburrido: perfil en funcion del tamano ---
big = P[V.sum(1) > np.median(V.sum(1))].mean(0)
small = P[V.sum(1) <= np.median(V.sum(1))].mean(0)
print('perfil filas grandes %:', np.round(big*100,1).tolist())
print('perfil filas pequenas %:', np.round(small*100,1).tolist())
print('rho grandes vs pequenas:', round(float(stats.spearmanr(big, small)[0]),3))
