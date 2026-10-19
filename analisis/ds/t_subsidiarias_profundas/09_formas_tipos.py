# -*- coding: utf-8 -*-
"""Tipologia de formas, suma de hojas y plantillas repetidas de color."""
import pandas as pd, numpy as np, os, json
from collections import defaultdict, Counter

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
rng = np.random.default_rng(3)
d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))

# tipologia simple
def tipo(r):
    if r.altura >= 4 and r.frac_cadena >= 0.5: return 'cadena larga'
    if r.grado_max >= 8 and r.altura <= 3: return 'abanico ancho'
    if r.frac_cadena >= 0.5: return 'cadena con ramas'
    return 'arbol ramificado'
T['tipo'] = T.apply(tipo, axis=1)
print('Tipologia (n=%d):' % len(T))
print(T.tipo.value_counts().to_string())
print('\nPor tipo: media de n, altura, nivel3, %con valor')
print(T.groupby('tipo').agg(n=('raiz', 'size'), cuerdas=('n', 'mean'), altura=('altura', 'mean'),
                            nivel3=('n_nivel3', 'mean'), frac_cadena=('frac_cadena', 'mean')).round(2).to_string())

# suma de hojas: padre = suma de todas las hojas de su subarbol
res = []
for kfg, g in d.groupby('kfg'):
    if kfg not in set(T.kfg): continue
    ch = defaultdict(list)
    for c, p in zip(g.cuerda, g.padre):
        if isinstance(p, str): ch[p].append(c)
    V = dict(zip(g.cuerda, g.v))
    def leaves(x):
        if not ch.get(x): return [x]
        out = []
        for k in ch[x]: out += leaves(k)
        return out
    for p in ch:
        lv = leaves(p)
        if len(lv) >= 2 and pd.notna(V.get(p)) and all(pd.notna(V.get(k)) for k in lv):
            res.append((kfg, p, V[p], sum(V[k] for k in lv), len(lv)))
L = pd.DataFrame(res, columns=['kfg', 'padre', 'valor', 'suma_hojas', 'n_hojas'])
L['ok'] = abs(L.valor - L.suma_hojas) < 1e-6
print('\npadre = suma de hojas del subarbol: %d/%d = %.1f%%' % (L.ok.sum(), len(L), 100*L.ok.mean()))
print('  por tamano de subarbol:'); print(L.groupby('n_hojas').agg(n=('ok','size'), ok=('ok','sum')).head(8).to_string())

# nulo de permutacion para suma de hojas (200 reps)
obs = int(L.ok.sum())
obs_by = L.groupby('n_hojas').ok.sum().to_dict()
null = []
groups = list(d.groupby('kfg'))
for rep in range(200):
    V2 = d.v.to_numpy().copy()
    for _, g in groups:
        idx = g.index.to_numpy(); ok = idx[~np.isnan(d.v.to_numpy()[idx])]
        V2[ok] = rng.permutation(d.v.to_numpy()[ok])
    vm = dict(zip(zip(d.kfg, d.cuerda), V2))
    cnt = 0
    for kfg, g in d.groupby('kfg'):
        if kfg not in set(T.kfg): continue
        ch = defaultdict(list)
        for cc, pp in zip(g.cuerda, g.padre):
            if isinstance(pp, str): ch[pp].append(cc)
        def lv(x):
            if not ch.get(x): return [x]
            o = []
            for k in ch[x]: o += lv(k)
            return o
        for p in ch:
            ls = lv(p)
            if len(ls) >= 2 and pd.notna(vm[(kfg, p)]) and all(pd.notna(vm[(kfg, k)]) for k in ls):
                if abs(vm[(kfg, p)] - sum(vm[(kfg, k)] for k in ls)) < 1e-6: cnt += 1
    null.append(cnt)
null = np.array(null)
print('  NULO: obs=%d nulo media %.1f p=%.4f' % (obs, null.mean(), (1 + (null >= obs).sum()) / 201))

# plantilla de color repetida en KH0197 y en general
def color_template(kfg, raiz):
    g = d[d.kfg == kfg]
    ch = defaultdict(list)
    for c, p in zip(g.cuerda, g.padre):
        if isinstance(p, str): ch[p].append(c)
    cmap = dict(zip(g.cuerda, g.color))
    levels = defaultdict(list)
    st = [(raiz, 0)]
    while st:
        x, lv = st.pop()
        levels[lv].append(str(cmap[x]))
        for k in ch.get(x, []): st.append((k, lv + 1))
    return tuple((lv, tuple(sorted(v))) for lv, v in sorted(levels.items()) if lv >= 2)

tpl = {}
for kfg in T.kfg.unique():
    for r in T[T.kfg == kfg].raiz:
        tpl[(kfg, r)] = color_template(kfg, r)
cnt = Counter(tpl.values())
print('\nPlantillas de color (niveles>=2) repetidas dentro del mismo quipu:')
rep = []
for kfg in T.kfg.unique():
    cs = Counter(v for (k, r), v in tpl.items() if k == kfg)
    for t, c in cs.items():
        if c > 1: rep.append((kfg, c, len(t)))
print(sorted(rep, key=lambda x: -x[1])[:10])
print('  arboles que comparten plantilla exacta con otro del mismo quipu:',
      sum(c for *_, c, _l in [(a, c, l) for a, c, l in rep]) - len(rep))

T.to_csv(os.path.join(OUT, 'arboles_tipos.csv'), index=False)
json.dump(dict(tipos=T.tipo.value_counts().to_dict(), hoja_ok=int(L.ok.sum()), hoja_n=int(len(L)),
               hoja_p=float((1 + (null >= obs).sum()) / 201)),
          open(os.path.join(OUT, 'tipos.json'), 'w'), indent=2, default=str)
