"""33 · Evaluación de dos candidatas del lector (post hoc, encargo del coordinador).
(a) UR004 -> UR091 «totales en orden»: n.º de totales de grupo de UR004 (grupos con >=2 colgantes
    anudados, total >=10) que aparecen como cuerda de UR091 en orden creciente (subsecuencia creciente
    más larga). Nulo: 9 999 barajados de los colgantes de UR004 conservando tamaños de grupo.
(b) UR1034 ~ UR1145 (y también la inversa de (a)): valores >=10 compartidos y su orden (LIS);
    nulo: barajar UR1145 (rachas) 9 999 veces. Además, la medida multibloque del barrido (01).
Salida: salida_06.txt"""
import bisect
import numpy as np
import pandas as pd
from comun import preparar, OUT
import os

rng = np.random.default_rng(20261033)
D = preparar(); S = D['seqs']


def lis(x):
    t = []
    for v in x:
        i = bisect.bisect_left(t, v); t[i:i + 1] = [v]
    return len(t)


def _tol(t, v):
    d = abs(int(t) - int(v))
    return d == 0 or d in (1, 10, 100, 1000, 10000)


def totales_en_orden(a, b, perm=None, tol=False, ver=False):
    p = S[a][S[a].nivel == 0].copy()
    if perm is not None:
        p['v'] = perm
    g = p.groupby('grupo').v
    tot = [t for t, n in zip(g.sum(), g.apply(lambda s: (s > 0).sum())) if n >= 2 and t >= 10]
    vb = S[b].v.values
    hits = []
    for t in tot:
        js = [j for j, v in enumerate(vb) if (_tol(t, v) if tol else t == v)]
        if js:
            hits.append(js[0])
            if ver:
                print('   total', t, '-> cuerda', S[b].cuerda.values[js[0]], vb[js[0]])
    return len(hits), max(lis(hits), lis([-h for h in hits])) if hits else 0


def compartidos(a, b, vb=None):
    va = S[a].v.values
    vb = S[b].v.values if vb is None else vb
    pa = {}
    for i, v in enumerate(va):
        if v >= 10:
            pa.setdefault(v, i)
    pb = {}
    for i, v in enumerate(vb):
        if v >= 10:
            pb.setdefault(v, i)
    com = sorted(set(pa) & set(pb), key=lambda v: pa[v])
    o = [pb[v] for v in com]
    return len(com), (max(lis(o), lis([-x for x in o])) if o else 0)


log = []
for a, b, tol in (('UR004', 'UR091', False), ('UR004', 'UR091', True), ('UR1034', 'UR1145', False),
                  ('UR1034', 'UR1145', True)):
    k, L = totales_en_orden(a, b, tol=tol, ver=tol)
    pv = S[a][S[a].nivel == 0].v.values
    nul = np.array([totales_en_orden(a, b, rng.permutation(pv), tol=tol) for _ in range(999 if tol else 9999)])
    nn = len(nul)
    log.append(f'(a) totales de grupo de {a} en {b} ({"±1 nudo" if tol else "exactos"}): {k} aparecen, {L} en orden; '
               f'p(k)={((nul[:, 0] >= k).sum() + 1) / (nn + 1):.4f}  p(L)={((nul[:, 1] >= L).sum() + 1) / (nn + 1):.4f}  '
               f'nulo medio k={nul[:, 0].mean():.2f} L={nul[:, 1].mean():.2f}')
for a, b in (('UR1034', 'UR1145'), ('UR004', 'UR091')):
    k, L = compartidos(a, b)
    from comun import barajar_rachas
    vb = S[b].v.values.astype(np.int64)
    np.random.seed(20261033)
    nul = np.array([compartidos(a, b, barajar_rachas(vb)) for _ in range(9999)])
    log.append(f'(b) {a}~{b}: {k} valores >=10 compartidos, {L} en orden; p(L | mismos valores)='
               f'{((nul[:, 1] >= L).sum() + 1) / 10000:.4f} (nulo medio L={nul[:, 1].mean():.2f})')
r = pd.read_csv(os.path.join(OUT, 'barrido_todo.csv.gz'))
for a, b in (('UR004', 'UR091'), ('UR1034', 'UR1145')):
    m = r[((r.A == a) & (r.B == b)) | ((r.A == b) & (r.B == a))].iloc[0]
    log.append(f'barrido multibloque {a}~{b}: score {m.score:.1f} (máx. nulo {m.null_max:.1f}), p={m.p:.2g}, q={m.q:.2g}')
open(os.path.join(OUT, 'salida_06.txt'), 'w', encoding='utf-8').write('\n'.join(log))
print('\n'.join(log))

# filas en pares_copia.csv (se corre después de 03; reemplaza filas previas de estas dos candidatas)
pc = pd.read_csv(os.path.join(OUT, 'pares_copia.csv'))
cand = {('UR004', 'UR091'), ('UR1034', 'UR1145')}
pc = pc[~pc.apply(lambda x: (x.kfg_a, x.kfg_b) in cand or (x.kfg_b, x.kfg_a) in cand, axis=1)]
filas = [dict(kfg_a='UR004', kfg_b='UR091', transformacion='totales de grupo en orden (resumen)', similitud=np.nan,
              p=0.45, q=np.nan, holm=np.nan, nivel='ninguno (negativa)', publicado_antes='no',
              fuente='candidata del lector; 04 tarea 2 q=0,096; 06 ±1 nudo p=0,51'),
         dict(kfg_a='UR1034', kfg_b='UR1145', transformacion='totales de grupo en orden (resumen), 5 exactos',
              similitud=np.nan, p=4e-4, q=0.147, holm=np.nan, nivel='especulativo (post hoc)', publicado_antes='no',
              fuente='candidata del lector; q de 04 tarea 2 sobre 311 150 pares; 4 de 5 totales <20')]
pd.concat([pc, pd.DataFrame(filas)], ignore_index=True).to_csv(os.path.join(OUT, 'pares_copia.csv'), index=False,
                                                              float_format='%.3g')
