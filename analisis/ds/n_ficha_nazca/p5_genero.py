"""P5: el genero 'ficha de n campos con encabezado mayor'. Marcadores a 2 campos
de un extremo, razon campo1/campo2, y comparacion con Santa e Incahuasi."""
import numpy as np, pandas as pd
from collections import Counter
from scipy.stats import binomtest, spearmanr
from lib import load, records, canon, prof, corr, holm, bh, OUT, DAT, RNG

c = load()
Q = pd.read_csv(DAT / 'quipus.csv')
FICHA = ['UR1140', 'UR1136', 'UR223', 'HP056', 'UR234', 'UR1131']

print('== templanza de las marcadoras: posiciones en grupos de 8/9/10 con exactamente 2 ==')
for size in [8, 9, 10]:
    pos = Counter()
    for k, dd in c[c.nivel == 0].groupby('kfg'):
        for g, gg in dd.groupby('grupo', sort=False):
            if len(gg) != size:
                continue
            cols = list(gg.sort_values('orden').col); cc = Counter(cols)
            maj, nm = cc.most_common(1)[0]
            if nm != size - 2 or cc[maj] != size - 2:
                continue
            mk = tuple(i + 1 for i, x in enumerate(cols) if x != maj)
            pos[mk] += 1
    tot = sum(pos.values())
    d2 = sum(v for k, v in pos.items() if k[0] == 3 and k[1] == 4 or k[0] == size - 3 and k[1] == size - 2)
    print(f'size {size}: {tot} grupos; top={pos.most_common(6)}; a 2 de un extremo={d2}/{tot}={d2/tot:.2f}')

print('\n== cabecera (2 campos antes/despues del par) y razon c1/c2 ==')
rows = []
for k in FICHA:
    size = {'UR234': 8, 'UR1131': 10}.get(k, 9)
    M = np.array([canon(r['vals'], r['pos'], size=size) for r in records(c, k, size=size)
                  if not np.isnan(r['vals']).any()])
    if not len(M):
        continue
    mf = np.mean([np.argmax(r) == 0 for r in M])
    ratio = np.median(M[:, 0] / np.maximum(M[:, 1], 1))
    # 2o campo es el minimo?
    f2min = np.mean([np.argmin(r) == 1 for r in M])
    # efecto posicional interno
    X = np.log10(M + 1); Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True, ddof=0)
    P = Z.mean(0); eta = np.var(P) / np.var(Z)
    rows.append(dict(khipu=k, size=size, n=len(M), max_frac=mf, c1_c2=ratio, f2_min=f2min,
                     eta2=eta, perfil=np.round(P, 2).tolist()))
    print(f'{k:<7} n={len(M):>2} campos={size-2} max_c1={mf:.0%} mediana c1/c2={ratio:.1f} '
          f'c2=min {f2min:.0%} | perfil {np.round(P,2)}')

print('\n== Santa (grupos de 6) ==')
rows_s = []
for k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    V = []
    for g, gg in d.groupby('grupo', sort=False):
        if len(gg) != 6:
            continue
        v = gg.v.to_numpy(float)
        if np.isnan(v).any() or np.ptp(v) == 0:
            continue
        V.append(v)
    M = np.array(V)
    if not len(M):
        continue
    P = prof(M)
    fmaxpos = np.mean([np.argmax(r) for r in M])
    mf = np.mean([np.argmax(r) == 0 for r in M])
    print(f'{k}: n={len(M):>2} perfil {np.round(P,2)} max_pos_medio={fmaxpos:.1f} max_c1={mf:.0%}')
    rows_s.append(dict(khipu=k, n=len(M), max_frac=mf, perfil=np.round(P, 2).tolist()))

print('\n== Incahuasi UR278 (grupos de 9, 9 columnas) ==')
d = c[(c.kfg == 'UR278') & (c.nivel == 0)].sort_values('orden')
V = []
for g, gg in d.groupby('grupo', sort=False):
    if len(gg) != 9:
        continue
    v = gg.v.to_numpy(float)
    if np.isnan(v).any():
        continue
    V.append(v)
M = np.array(V)
print('n grupos completos', len(M), 'media por columna', np.round(M.mean(0), 0))
# canonico: mayor a menor; para comparar perfiles, ordenar cada fila descendentemente
Ms = np.sort(M, axis=1)[:, ::-1]
P = prof(Ms); print('perfil ordenado desc', np.round(P, 2))
print('max en col 1 (fisica):', np.mean([np.argmax(r) == 0 for r in M]).round(3),
      '| col 1 es max o empata:', np.mean([r[0] >= r.max() - 1e-9 for r in M]).round(3))
print('Spearman perfil vs posicion:', spearmanr(P, np.arange(1, 10)))
# correlacion con la ficha Nazca de 7 campos en las 7 primeras posiciones
f7 = prof(np.array([canon(r['vals'], r['pos']) for r in records(c, 'UR1140') if not np.isnan(r['vals']).any()]))
print('r de UR278 (9 col) con ficha Nazca 7 campos, 7 primeras:', round(corr(P[:7], f7), 3))

# --- test de genero: maxfrac vs tasa base del mismo tamano, excluyendo los focos ---
print('\n== test de genero: max en campo 1 vs tasa base (grupos del mismo tamano, sin los focos) ==')
FOCOS = set(FICHA) | {'UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092', 'UR278'}
def base(size):
    hit = tot = 0
    for k, dd in c[(c.nivel == 0)].groupby('kfg'):
        if k in FOCOS:
            continue
        for r in records(c, k, size=size):
            v = r['vals']
            if np.isnan(v).any() or np.ptp(v) == 0:
                continue
            vv = canon(v, r['pos'], size=size)
            tot += 1; hit += int(np.argmax(vv) == 0)
    return (hit / tot if tot else np.nan), tot
res = []
for k in FICHA + ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092', 'UR278']:
    size = {'UR234': 8, 'UR1131': 10}.get(k, 9)
    if k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']:
        size = 6
    if k == 'UR278':
        size = 9
    p0, ntot = base(size)
    if k in FICHA:
        Mx = np.array([canon(r['vals'], r['pos'], size=size) for r in records(c, k, size=size)
                       if not np.isnan(r['vals']).any()])
    elif k == 'UR278':
        Mx = np.array([gg.v.to_numpy(float) for g, gg in c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden').groupby('grupo', sort=False)
                       if len(gg) == 9 and not gg.v.isna().any()])
    else:
        Mx = np.array([gg.v.to_numpy(float) for g, gg in c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden').groupby('grupo', sort=False)
                       if len(gg) == 6 and not gg.v.isna().any() and np.ptp(gg.v.to_numpy(float)) > 0])
    if not len(Mx):
        continue
    h = int(np.sum([np.argmax(r) == 0 for r in Mx]))
    p = binomtest(h, len(Mx), p0, alternative='greater').pvalue
    res.append(dict(khipu=k, size=size, campos=size - (2 if k in FICHA else 0), n=len(Mx),
                    hit=h, max_frac=h / len(Mx), base=round(p0, 3), p=p))
R = pd.DataFrame(res)
R['holm'] = holm(R.p.values); R['bh'] = bh(R.p.values)
print(R.round(4).to_string(index=False))
R.to_csv(OUT / 'genero.csv', index=False)
print('\nescrito genero.csv')
