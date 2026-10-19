# -*- coding: utf-8 -*-
"""Exploracion: prueba H01-H15 SOLO en la mitad de exploracion.
Nulo por permutacion, semilla fija. No toca la mitad de confirmacion salvo
para H07/H08, que se limitan a reservar esas filas (no se evaluan aqui).
"""
import numpy as np, pandas as pd
from scipy import stats
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

RNG = np.random.default_rng(20261018)
NP = 4000
Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv')
c['valor'] = c.valor.fillna(0)
c = c[c.kfg.isin(Q)]
part = pd.read_csv('ds/n_tanteo/particion.csv')

TAG = {}
for _, r in part.iterrows():
    TAG[(r.kfg, r.unidad, int(r.id))] = r.mitad

def tag(k, grupo):
    return TAG.get((k, 'grupo', int(grupo)), 'NA')

def recs(k):
    """Registros = grupos de colgantes; vals ordenados; tag de particion."""
    g = c[(c.kfg == k) & (c.nivel == 0)]
    out = []
    for gr, gg in g.groupby('grupo'):
        gg = gg.sort_values('orden')
        out.append(dict(grupo=int(gr), vals=gg.valor.astype(int).tolist(),
                        cab=int(gg.valor.iloc[0]), suma=int(gg.valor.sum()),
                        tag=tag(k, gr)))
    return sorted(out, key=lambda x: x['grupo'])

def perm_p(obs, null, side='greater'):
    null = np.asarray(null)
    if side == 'greater':
        return (1 + (null >= obs).sum()) / (1 + len(null))
    return (1 + (null <= obs).sum()) / (1 + len(null))

res = []
def add(h, stat, n, obs, exp, p, extra=''):
    def fmt(x):
        return f'{x:9.4g}' if isinstance(x, (int, float, np.floating, np.integer)) else f'{str(x):>9s}'
    ps = f'{p:.4f}' if isinstance(p, (int, float, np.floating)) else '  na  '
    res.append(dict(id=h, estadistico=stat, n=n, observado=obs,
                    esperado=exp, p=p, extra=extra))
    print(f'{h} {stat:44s} n={n:3d} obs={fmt(obs)} esp={fmt(exp)} p={ps} {extra}')

# ---------- H01/H02: dinamica de saldo ----------
def dyn(kA, kB, cuota, half):
    A = {r['grupo']: max(r['vals']) for r in recs(kA) if max(r['vals']) > 0 and r['tag'] == half}
    B = {r['grupo']: max(r['vals']) for r in recs(kB) if max(r['vals']) > 0 and r['tag'] == half}
    gs = sorted(set(A) & set(B))
    if len(gs) < 4:
        return
    a = np.array([A[g] for g in gs]); b = np.array([B[g] for g in gs])
    forms = {
        'B_i-A_i-c': lambda a, b: b - a - cuota,
        'B_i+A_i+c': lambda a, b: b + a + cuota,
        'B_i-A_i+c': lambda a, b: b - a + cuota,
        'B_i+A_i-c': lambda a, b: b + a - cuota,
        'B_i-A_i':   lambda a, b: b - a,
        'B_i+A_i':   lambda a, b: b + a,
        'B_i-c':     lambda a, b: b - cuota,
        'B_i-2A_i':  lambda a, b: b - 2 * a,
    }
    best = None
    for nm, f in forms.items():
        pred = f(a[:-1], b[:-1])
        hits = int((pred == b[1:]).sum())
        if best is None or hits > best[2]:
            best = (nm, pred, hits)
    nm, pred, hits = best
    null = []
    for _ in range(NP):
        aa = RNG.permutation(a[:-1])
        null.append(int((forms[nm](aa, b[:-1]) == b[1:]).sum()))
    p = perm_p(hits, null)
    add(kA + '/' + kB, 'transiciones exactas (' + nm + ')', len(gs) - 1, hits,
        round(np.mean(null), 2), round(p, 4))

# ---------- H03/H04: cabeceras acumuladas ----------
def acum(k, cuota, half):
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == half]
    if len(rs) < 5:
        return
    H = np.array([r['cab'] for r in rs])
    net = np.array([sum(r['vals'][1:]) - cuota for r in rs])
    tot = np.array([sum(r['vals'][1:]) for r in rs])
    forms = {'H+N': H[:-1] + net[:-1], 'H-N': H[:-1] - net[:-1],
             'H+suma': H[:-1] + tot[:-1], 'H-suma': H[:-1] - tot[:-1]}
    best = max(forms.items(), key=lambda kv: int((kv[1] == H[1:]).sum()))
    hits = int((best[1] == H[1:]).sum())
    null = []
    for _ in range(NP):
        nn = RNG.permutation(net[:-1])
        null.append(int(((H[:-1] + nn) == H[1:]).sum()) if best[0] == 'H+N'
                    else int(((H[:-1] + RNG.permutation(tot[:-1])) == H[1:]).sum()))
    add(k, 'transiciones acumuladas (' + best[0] + ')', len(H) - 1, hits,
        round(np.mean(null), 2), round(perm_p(hits, null), 4))

# ---------- H05: cuota proporcional ----------
def cuota_prop(k, cuota, half):
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == half and len(r['vals']) > 1]
    if len(rs) < 5:
        return
    h = np.array([r['cab'] for r in rs], float)
    q = np.full(len(h), float(cuota))
    rate = q / h
    add(k, 'CV(cuota/cabecera) [2%->0, fija->alto]', len(h),
        round(float(rate.std() / rate.mean()), 3), '0 si 2 %',
        np.nan, f'cuota={cuota} rango {rate.min():.4f}-{rate.max():.4f}')

def cuota_prop269(half):
    rs = [r for r in recs('UR269') if r['cab'] > 0 and r['tag'] == half and len(r['vals']) > 1]
    C = {25, 40, 44, 46, 47}
    rs = [r for r in rs if any(v in C for v in r['vals'][1:])]
    if len(rs) < 5:
        return
    h = np.array([r['cab'] for r in rs], float)
    q = np.array([next(v for v in r['vals'][1:] if v in C) for r in rs], float)
    r = stats.pearsonr(h, q)[0]
    add('UR269', 'r(cabecera, cuota) [fija->0, 2%->1]', len(h), round(float(r), 3),
        '0 (fija)', np.nan, 'cuotas ' + str(sorted(set(q.astype(int)))))

# ---------- H06: cabecera = resto ----------
def reparto(k, half):
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == half and len(r['vals']) > 1]
    if len(rs) < 5:
        return
    o = np.array([r['cab'] for r in rs])
    s = np.array([sum(r['vals'][1:]) for r in rs])
    hits = int((o == s).sum()); hits1 = int((abs(o - s) <= 1).sum())
    null = []
    for _ in range(NP):
        oo = RNG.permutation(o)
        null.append(int((oo == s).sum()))
    add(k, 'registros con cab=suma(resto)', len(rs), hits,
        round(float(np.mean(null)), 2), round(perm_p(hits, null), 4), f'+-1: {hits1}')

# ---------- celdas UR270 y filas UR278 ----------
def cells270():
    out = {}
    g = c[c.kfg == 'UR270']
    for gr, gg in g.groupby('grupo'):
        gg = gg.sort_values('orden')
        cols = gg[gg.nivel == 0]
        sub = gg[gg.nivel > 0]
        cells = []
        for _, r in cols.iterrows():
            base = r.cuerda
            ss = sub[sub.padre == base].valor.sum()
            cells.append(int(r.valor + ss))
        out[int(gr)] = dict(cells=cells, tag=tag('UR270', gr), grupo=int(gr))
    return out

def rows278():
    out = {}
    g = c[(c.kfg == 'UR278') & (c.nivel == 0)]
    for gr, gg in g.groupby('grupo'):
        v = gg.sort_values('orden').valor.astype(int).tolist()
        if len(v) == 9:
            out[int(gr)] = dict(cells=v, tag=tag('UR278', gr), grupo=int(gr))
    return out

R270, R278 = cells270(), rows278()

# ---------- H07/H08: perfil de 9 partes (solo ajuste en exploracion) ----------
def shares(cells):
    s = sum(cells)
    return np.array(cells) / s if s else None

def perfil_9(rows, name):
    ex = [v['cells'] for v in rows.values() if v['tag'] == 'explorar' and len(v['cells']) == 9 and sum(v['cells']) > 0]
    co = [v['cells'] for v in rows.values() if v['tag'] == 'confirmar' and len(v['cells']) == 9 and sum(v['cells']) > 0]
    if len(ex) < 5 or len(co) < 5:
        print(name, 'filas insuficientes', len(ex), len(co))
        return None
    P = np.mean([shares(x) for x in ex], axis=0)
    # exploracion: error de ajuste (para congelar el perfil)
    mae_exp = np.mean([np.abs(np.array(x) - sum(x) * P).sum() / 9 for x in ex])
    # novenos iguales en exploracion
    mae_eq = np.mean([np.abs(np.array(x) - sum(x) / 9).sum() / 9 for x in ex])
    add(name, 'MAE ajuste perfil (exploracion)', len(ex), round(float(mae_exp), 2),
        round(float(mae_eq), 2), np.nan, 'perfil P=' + np.round(P * 100, 1).tolist().__str__())
    return P, ex, co

r278 = perfil_9(R278, 'UR278')
r270 = perfil_9(R270, 'UR270')
if r278: P278, ex278, co278 = r278
if r270: P270, ex270, co270 = r270

# H08: rho entre perfiles de columnas de exploracion y confirmacion
for rows, name in [(R278, 'UR278'), (R270, 'UR270')]:
    ex = [v['cells'] for v in rows.values() if v['tag'] == 'explorar' and len(v['cells']) == 9 and sum(v['cells']) > 0]
    co = [v['cells'] for v in rows.values() if v['tag'] == 'confirmar' and len(v['cells']) == 9 and sum(v['cells']) > 0]
    if len(ex) < 5 or len(co) < 5:
        continue
    pe = np.mean([shares(x) for x in ex], axis=0)
    pc = np.mean([shares(x) for x in co], axis=0)
    rho = stats.spearmanr(pe, pc)[0]
    null = [stats.spearmanr(pe, RNG.permutation(pc))[0] for _ in range(NP)]
    add(name, 'rho perfil explorar vs confirmar', len(co), round(float(rho), 3),
        round(float(np.mean(null)), 3), round(perm_p(rho, null), 4))

# ---------- H09: escalera ----------
v269 = [r['cab'] for r in recs('UR269')]
v269 += [v for r in recs('UR269') for v in r['vals']]
v278 = [v['cells'] for v in R278.values()]
s278 = [sum(x) for x in v278]
v266 = [r['cab'] for r in recs('UR266')]
v275 = [r['cab'] for r in recs('UR275')]
trip = [(a, b, d) for a in v269 for b in s278 for d in v266 + v275 if b - a == 100 and d - b == 100]
print('H09 triples en escalera de 100:', trip[:5], 'n=', len(trip))

# ---------- H10/H11: primer cordon = suma del resto ----------
def primer_suma(k):
    rs = [r for r in recs(k) if len(r['vals']) >= 3 and r['tag'] == 'explorar']
    if len(rs) < 5:
        print(k, 'grupos insuficientes', len(rs)); return
    obs = sum(1 for r in rs if r['vals'][0] == sum(r['vals'][1:]))
    null = []
    for _ in range(NP):
        first = RNG.permutation([r['vals'][0] for r in rs])
        rest = np.array([sum(r['vals'][1:]) for r in rs])
        null.append(int((first == rest).sum()))
    add(k, 'grupos con cordon 1 = suma(resto)', len(rs), obs,
        round(float(np.mean(null)), 2), round(perm_p(obs, null), 4))

# ---------- H12: UR276 parent=s1+s2 ----------
def h12():
    d276 = c[c.kfg == 'UR276']
    ok = 0
    for p in ['p1', 'p2', 'p3', 'p4', 'p5']:
        par = d276[(d276.cuerda == p)].valor.iloc[0]
        ss = d276[d276.padre == p].valor.sum()
        ok += int(par == ss)
    add('UR276', 'registros parent = s1+s2', 5, ok, round(5 * 0.02, 2), np.nan,
        'nulo aproximado: solo valores <=24')

# ---------- H13: valores de UR279 como totales ----------
def h13():
    v279 = [int(x) for x in c[(c.kfg == 'UR279') & (c.nivel == 0)].valor]
    pool = []
    for k in Q:
        if k == 'UR279':
            continue
        pool += [r['suma'] for r in recs(k)] + [r['cab'] for r in recs(k)]
    pool = [x for x in pool if x > 0]
    m = sum(1 for x in v279 if x in pool)
    # nulo: mismos valores, sorteados del pool con reemplazo
    null = [sum(1 for _ in v279 if RNG.choice(pool) in pool) for _ in range(200)]
    add('UR279', 'colgantes hallados como total en otro quipu', len(v279), m,
        round(float(np.mean(null)), 2), round(perm_p(m, null), 4),
        f'pool {len(pool)}; 24 % de cuerdas tienen valor unico, nulo alto')

# ---------- H16: reparto tolerante ----------
def reparto_tol(k, half):
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == half and len(r['vals']) > 1]
    if len(rs) < 5:
        return
    o = np.array([r['cab'] for r in rs], float)
    s = np.array([sum(r['vals'][1:]) for r in rs], float)
    obs = float((np.abs(o - s) / o < 0.05).mean())
    null = []
    for _ in range(NP):
        ss = s.copy()
        # barajar los destinos individuales entre registros
        allv = [v for r in rs for v in r['vals'][1:]]
        sizes = [len(r['vals']) - 1 for r in rs]
        perm = RNG.permutation(allv)
        idx = 0; sums = []
        for z in sizes:
            sums.append(perm[idx:idx + z].sum()); idx += z
        null.append(float((np.abs(o - np.array(sums)) / o < 0.05).mean()))
    add(k, 'frac. |cab-(cuota+dest)|/cab < 5 %', len(rs), round(obs, 3),
        round(float(np.mean(null)), 3), round(perm_p(obs, null), 4))

# ---------- llamadas de exploracion ----------
dyn('UR273A', 'UR273B', 17, 'explorar')
dyn('UR274A', 'UR274B', 17, 'explorar')
acum('UR275', 47, 'explorar')
acum('UR269', 47, 'explorar')
cuota_prop('UR275', 47, 'explorar')
cuota_prop('UR268', 208, 'explorar')
cuota_prop269('explorar')
for k in ['UR275', 'UR266', 'UR269', 'UR268']:
    reparto(k, 'explorar')
for k in ['UR275', 'UR266', 'UR269']:
    reparto_tol(k, 'explorar')
primer_suma('UR277')
primer_suma('UR272')
h12(); h13()

# ---------- H14: UR270 celdas vs filas UR278 (solo grupos de exploracion) ----------
def match_rows(cells, rows, k=6):
    out = []
    for g, r in rows.items():
        if len(r['cells']) != 9:
            continue
        out.append((g, sum(abs(a - b) <= 1 for a, b in zip(cells, r['cells']))))
    return out

ex270 = [r for r in R270.values() if r['tag'] == 'explorar' and len(r['cells']) == 9 and sum(r['cells']) > 0]
n_match = 0
for r in ex270:
    mm = match_rows(r['cells'], R278)
    if mm and max(x[1] for x in mm) >= 6:
        n_match += 1
add('H14', 'grupos UR270 con >=6/9 celdas en fila UR278', len(ex270), n_match,
    round(len(ex270) * 0.02, 2), np.nan, 'control positivo; nulo ~0 por azar')

# ---------- H15: perfil UR270 vs UR278 (solo exploracion) ----------
p270 = np.mean([shares(v['cells']) for v in R270.values()
                if v['tag'] == 'explorar' and len(v['cells']) == 9 and sum(v['cells']) > 0], axis=0)
p278 = np.mean([shares(v['cells']) for v in R278.values()
                if v['tag'] == 'explorar' and len(v['cells']) == 9 and sum(v['cells']) > 0], axis=0)
rho = stats.spearmanr(p270, p278)[0]
null = [stats.spearmanr(p270, RNG.permutation(p278))[0] for _ in range(NP)]
add('H15', 'rho perfil UR270 vs UR278', min(len(p270), len(p278)), round(float(rho), 3),
    round(float(np.mean(null)), 3), round(perm_p(rho, null), 4))

pd.DataFrame(res).to_csv('ds/n_tanteo/exploracion_resultados.csv', index=False)
print('\n--- guardado exploracion_resultados.csv ---')
