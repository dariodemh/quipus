"""P4: barrido del corpus. Grupos de 8, 9 y 10 con 2 marcadoras; regla 'campo 1 maximo'
y correlacion con la ficha congelada de UR1140."""
import numpy as np, pandas as pd
from collections import Counter
from lib import load, records, canon, prof, corr, perm_p, holm, bh, OUT

c = load()
KS = {'UR1140': 9, 'UR1136': 9, 'UR223': 9, 'HP056': 9}
def Mat(k, size):
    out = []
    for r in records(c, k, size=size):
        if np.isnan(r['vals']).any():
            continue
        out.append(canon(r['vals'], r['pos'], size=size))
    return np.array(out)

M0 = Mat('UR1140', 9); f0 = prof(M0)
print('ficha UR1140 (n=%d):' % len(M0), np.round(f0, 3))

rows = []
for size in [8, 9, 10]:
    qs = []
    for k, d in c[c.nivel == 0].groupby('kfg'):
        R = records(c, k, size=size)
        if len(R) >= 3:
            qs.append((k, R))
    print(f'\n== tamano {size}: {len(qs)} quipus con >=3 grupos de {size} y 2 marcadoras ==')
    for k, R in qs:
        M = np.array([canon(r['vals'], r['pos'], size=size) for r in R if not np.isnan(r['vals']).any()])
        n = len(R); nc = len(M)
        mf = float(np.mean([np.argmax(r) == 0 for r in M])) if nc else np.nan
        tipos = Counter(str(r['pos']) for r in R)
        row = dict(khipu=k, size=size, n_grupos=n, n_completos=nc, max_frac=mf,
                   pos_marcadoras=str(dict(tipos)), maj=str(Counter(r['maj'] for r in R).most_common(1)[0][0]))
        if size == 9 and nc >= 3:
            r_, p_ = perm_p(M, f0, B=999)
            row.update(r_ficha=r_, p_ficha=p_)
        rows.append(row)
R = pd.DataFrame(rows)
R['p_bin'] = [__import__('scipy.stats', fromlist=['binomtest']).binomtest(int(round(r.max_frac * r.n_completos)), int(r.n_completos), 1 / r.size).pvalue
              if r.n_completos and not np.isnan(r.max_frac) else np.nan for r in R.itertuples()]
# correccion sobre TODAS las pruebas hechas (todas las filas tienen p bin)
R['p_bin_holm'] = holm(R.p_bin.fillna(1).values)
R['p_bin_bh'] = bh(R.p_bin.fillna(1).values)

# familia de correlaciones (solo 9) y correccion sobre todos los quipus del corpus
for col in ['p_ficha', 'p_ficha_holm', 'p_ficha_bh', 'p_ficha_holm651', 'p_ficha_bh651']:
    if col not in R:
        R[col] = np.nan
T = R[R['size'] == 9]
ok = T.p_ficha.notna().values
idx = T.index[ok]
R.loc[idx, 'p_ficha_holm'] = holm(T.loc[ok, 'p_ficha'].values)
R.loc[idx, 'p_ficha_bh'] = bh(T.loc[ok, 'p_ficha'].values)
# familia conservadora: 651 quipus, p=1 para los no testables
q651 = np.ones(651); q651[:ok.sum()] = T.loc[ok, 'p_ficha'].values
R.loc[idx, 'p_ficha_holm651'] = holm(q651)[:ok.sum()]
R.loc[idx, 'p_ficha_bh651'] = bh(q651)[:ok.sum()]

pd.set_option('display.width', 200)
print('\n== quipus con >=3 grupos y campo 1 maximo en >=50% ==')
X = R[(R.n_completos >= 3) & (R.max_frac >= 0.5)].sort_values(['size', 'max_frac'], ascending=[True, False])
print(X[['khipu', 'size', 'n_grupos', 'n_completos', 'max_frac', 'p_bin', 'p_bin_holm',
         'r_ficha', 'p_ficha', 'p_ficha_holm', 'p_ficha_holm651', 'pos_marcadoras']].round(4).to_string(index=False))

print('\n== resumen por tamano ==')
for s in [8, 9, 10]:
    S = R[R['size'] == s]
    print(f'size {s}: quipus={len(S)}, con >=3 completos={int((S.n_completos>=3).sum())}, '
          f'max_frac medio={S.max_frac.mean():.2f}, quipus con max_frac=1={int((S.max_frac==1).sum())}')

R.to_csv(OUT / 'barrido_corpus.csv', index=False)
print('\nescrito barrido_corpus.csv')
