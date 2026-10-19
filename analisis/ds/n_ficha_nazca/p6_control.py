"""P6: control clave. Tasa base de 'campo 1 maximo' en grupos con 2 marcadoras
(todos los quipus, sin los focos) y estructura interna de Incahuasi."""
import numpy as np, pandas as pd
from collections import Counter
from scipy.stats import spearmanr, binomtest
from lib import load, records, canon, prof, corr, holm, OUT, RNG

c = load()
FOCOS = {'UR1140', 'UR1136', 'UR223', 'HP056', 'UR234', 'UR1131'}

print('== tasa base en grupos CON 2 marcadoras (canonico), por tamano ==')
for size in [8, 9, 10]:
    ids = []
    for k, dd in c[c.nivel == 0].groupby('kfg'):
        for r in records(c, k, size=size):
            if np.isnan(r['vals']).any() or np.ptp(r['vals']) == 0:
                continue
            ids.append((k, canon(r['vals'], r['pos'], size=size)))
    D = pd.DataFrame(ids, columns=['k', 'v'])
    D['f1max'] = [np.argmax(x) == 0 for x in D.v]
    N = D[~D.k.isin(FOCOS)]
    print(f'size {size}: todos {D.f1max.sum()}/{len(D)} = {D.f1max.mean():.3f}  quipus={D.k.nunique()}'
          f' || sin focos {N.f1max.sum()}/{len(N)} = {N.f1max.mean():.3f}  quipus={N.k.nunique()}')
    g = D.groupby('k').f1max.agg(['sum', 'count'])
    print('   quipus con >=3 registros:', len(g[g['count'] >= 3]),
          '| de ellos con f1max=100%:', int(((g['sum'] == g['count']) & (g['count'] >= 3)).sum()),
          '| con f1max>=80%:', int(((g['sum'] / g['count'] >= 0.8) & (g['count'] >= 3)).sum()))
    if size == 9:
        print('   detalle quipus con >=3 registros (sum/count):')
        print(g[g['count'] >= 3].sort_values('count', ascending=False).to_string())

print('\n== Incahuasi UR278: orden interno de los grupos de 9 ==')
d = c[(c.kfg == 'UR278') & (c.nivel == 0)].sort_values('orden')
rhos = []; dec = 0; n = 0
for g, gg in d.groupby('grupo', sort=False):
    if len(gg) != 9:
        continue
    v = gg.v.to_numpy(float)
    if np.isnan(v).any():
        continue
    n += 1
    rho = spearmanr(v, np.arange(9)).statistic
    rhos.append(rho)
    dec += int(all(v[i] >= v[i + 1] for i in range(8)))
print(f'n grupos={n}  Spearman medio(valor,posicion)={np.mean(rhos):.3f} '
      f'(mediana {np.median(rhos):.3f})  estrictamente decrecientes={dec}/{n}')
print('posicion del maximo por grupo:', dict(Counter(np.argmax(gg.v.to_numpy(float)) + 1 for g, gg in d.groupby('grupo') if len(gg) == 9)))
# perfil fisico (sin ordenar)
M = np.array([gg.v.to_numpy(float) for g, gg in d.groupby('grupo', sort=False) if len(gg) == 9 and not gg.v.isna().any()])
P = prof(M)
print('perfil fisico UR278:', np.round(P, 2), '| r con posicion:', round(spearmanr(P, np.arange(1, 10)).statistic, 3))

print('\n== Santa: perfil por posicion con bandas de color de 6 (metodo del informe previo) ==')
for k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    V = []
    cols = list(d.col); vals = d.v.to_numpy(float)
    i = 0
    while i <= len(cols) - 6:
        if len(set(cols[i:i + 6])) == 1 and not np.isnan(vals[i:i + 6]).any() and np.ptp(vals[i:i + 6]) > 0:
            V.append(vals[i:i + 6]); i += 6
        else:
            i += 1
    if not V:
        print(k, 'sin bandas'); continue
    M = np.array(V); P = prof(M)
    print(f'{k}: n={len(M):>2} perfil {np.round(P,2)} max_pos={np.mean([np.argmax(r)+1 for r in M]):.1f} '
          f'frac_max_pos4={np.mean([np.argmax(r)==3 for r in M]):.0%}')
