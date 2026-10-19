# -*- coding: utf-8 -*-
"""Estructura de los arboles de subsidiarias del KFG.
Salida: arboles.csv (una fila por arbol profundo, raiz = cuerda de nivel 0)
No imprime tablas grandes."""
import pandas as pd, numpy as np, os
from collections import defaultdict, deque

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
d['nudos'] = d['nudos'].astype('object')
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan
d['vpos'] = d['v'].where(d['v'] > 0)


def metrics(names, ch, depth, v, vpos):
    height = {}
    order = sorted(names, key=lambda n: -depth[n])
    for n in order:
        ks = ch.get(n, [])
        height[n] = 0 if not ks else 1 + max(height[k] for k in ks)
    internal = [n for n in names if ch.get(n)]
    deg = [len(ch[n]) for n in internal]
    leaves = [n for n in names if not ch.get(n)]
    chain = sum(1 for x in deg if x == 1)
    rel = {n: depth[n] - depth[names[0]] for n in names}
    widths = pd.Series([rel[n] for n in names]).value_counts().sort_index()
    sum_ok = sum_test = 0
    for n in internal:
        ks = ch[n]
        vals = [vpos.get(k) for k in ks]
        if len(ks) >= 2 and pd.notna(vpos.get(n)) and all(pd.notna(x) for x in vals):
            sum_test += 1
            if abs(sum(vals) - vpos[n]) < 1e-6:
                sum_ok += 1
    leavesum = sum(vpos[l] for l in leaves if pd.notna(vpos.get(l)))
    rootv = vpos.get(names[0], np.nan)
    return dict(n=len(names), altura=max(height.values()), n_internos=len(internal),
                grado_medio=(np.mean(deg) if deg else np.nan),
                grado_max=(max(deg) if deg else 0),
                frac_cadena=(chain / len(internal) if internal else np.nan),
                n_hojas=len(leaves),
                n_nivel3=sum(1 for n in names if rel[n] >= 3),
                ancho_niveles=';'.join(f'{int(k)}:{int(x)}' for k, x in widths.items()),
                suma_ok=sum_ok, suma_test=sum_test, suma_hojas=leavesum, valor_raiz=rootv,
                ratio_raiz_hojas=(rootv / leavesum if (pd.notna(rootv) and leavesum) else np.nan),
                n_con_valor=sum(1 for x in v.values() if pd.notna(x)))


rows = []
for kfg, g in d.groupby('kfg', sort=False):
    ch = defaultdict(list)
    for c, p in zip(g['cuerda'], g['padre']):
        if isinstance(p, str):
            ch[p].append(c)
    depth = dict(zip(g['cuerda'], g['nivel']))
    v = dict(zip(g['cuerda'], g['v']))
    vpos = dict(zip(g['cuerda'], g['vpos']))
    roots = g.loc[g['nivel'] == 0, 'cuerda'].tolist()
    for r in roots:
        desc = [r]
        q = deque([r])
        while q:
            x = q.popleft()
            for k in ch.get(x, []):
                desc.append(k); q.append(k)
        m = metrics(desc, ch, depth, v, vpos)
        if m['altura'] >= 3:
            g0 = g.set_index('cuerda')
            m.update(kfg=kfg, raiz=r, grupo=int(g0.loc[r, 'grupo']))
            rows.append(m)

T = pd.DataFrame(rows)
cols = ['kfg', 'raiz', 'grupo', 'n', 'altura', 'n_internos', 'grado_medio', 'grado_max',
        'frac_cadena', 'n_hojas', 'n_nivel3', 'ancho_niveles', 'suma_ok', 'suma_test',
        'suma_hojas', 'valor_raiz', 'ratio_raiz_hojas', 'n_con_valor']
T = T[cols]
T.to_csv(os.path.join(OUT, 'arboles.csv'), index=False)
print('arboles profundos (altura>=3):', len(T), 'en', T.kfg.nunique(), 'quipus')
print(T.groupby('kfg').agg(arboles=('raiz', 'size'), nodos=('n', 'sum'), altura_max=('altura', 'max'),
                           max_nivel3=('n_nivel3', 'max')).sort_values('nodos', ascending=False).head(15).to_string())
print('altura dist:', T.altura.value_counts().sort_index().to_dict())
print('suma jerarquica exacta:', int(T.suma_ok.sum()), '/', int(T.suma_test.sum()))
print('nodos en arboles profundos:', int(T.n.sum()), '/', len(d))
