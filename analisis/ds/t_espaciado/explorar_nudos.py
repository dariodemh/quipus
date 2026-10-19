"""Exploración de la posición de los racimos de nudos (cm desde el inicio de la cuerda)."""
import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
cl = pd.read_pickle(os.path.join(D, 'clusters.pkl'))
cl = cl.drop_duplicates(['kfg', 'cuerda', 'pos'])

pd.set_option('display.width', 180)

# ---- 1. sanidad y orden decimal ----
print('--- sanidad ---')
print('cuerdas con nudos:', int(c.tiene_nudos.sum()), '| clusters:', len(cl))
print('pos_max > largo (+0.01):', int((c.pos_max > c.largo + 0.01).sum()),
      '| largo==0:', int((c.largo == 0).sum()))
print('clusters por cuerda (con nudos):', c[c.tiene_nudos].n_clusters.describe(percentiles=[.5, .9]).round(2).to_dict())

sub = cl.dropna(subset=['valor_racimo']).sort_values(['kfg', 'cuerda', 'pos'])

def mono(x):
    v = x.valor_racimo.values
    return int(np.all(np.diff(v) <= 1e-9))

mm = sub.groupby(['kfg', 'cuerda']).apply(mono, include_groups=False)
sz = sub.groupby(['kfg', 'cuerda']).size()
mm = mm[sz >= 2]
print('\naportes descendentes con la posición (cuerdas >=2 racimos):',
      round(mm.mean(), 4), 'n=', len(mm))

# violaciones del orden decimal
sub['dec'] = sub.groupby(['kfg', 'cuerda']).valor_racimo.diff()
viol = sub[sub.dec > 1e-9]
print('\nracimos que suben de aporte al bajar (violaciones):', len(viol), 'en',
      viol.groupby(['kfg', 'cuerda']).ngroups, 'cuerdas')
print(viol[['kfg', 'cuerda', 'pos', 'tipo', 'n', 'valor_racimo']].head(6).to_string())

# ---- 2. huecos entre racimos ----
sub['gap'] = sub.groupby(['kfg', 'cuerda']).pos.diff()
sub['rank'] = sub.groupby(['kfg', 'cuerda']).cumcount()
g = sub.dropna(subset=['gap']).merge(c[['kfg', 'cuerda', 'largo', 'n_clusters']],
                                     on=['kfg', 'cuerda'], how='left', suffixes=('', '_c'))
g = g[(g.largo > 0) & (g.gap >= 0)]
g['gap_frac'] = g.gap / g.largo
print('\n--- huecos entre racimos consecutivos ---')
print('gap cm:', g.gap.describe(percentiles=[.1, .5, .9]).round(2).to_dict())
print('gap / largo:', g.gap_frac.describe(percentiles=[.1, .5, .9]).round(3).to_dict())
print('correlación gap ~ largo:', round(g[['gap', 'largo']].corr().iloc[0, 1], 3),
      '| gap ~ n_clusters:', round(g[['gap', 'n_clusters']].corr().iloc[0, 1], 3))

# pares g1 vs g2 en cuerdas de 3 racimos
tres = g[g.n_clusters == 3].pivot(index=['kfg', 'cuerda'], columns='rank', values='gap')
tres = tres[[1, 2]].rename(columns={1: 'g1', 2: 'g2'}).dropna()
print('cuerdas de 3 racimos:', len(tres),
      '| g1>g2:', round((tres.g1 > tres.g2).mean(), 3),
      '| mediana g1/g2:', round(tres.g1.median(), 2), '/', round(tres.g2.median(), 2),
      '| Wilcoxon p:', f'{stats.wilcoxon(tres.g1, tres.g2).pvalue:.3g}')

# ¿el hueco se explica por el tamaño del racimo?
print('correlación gap ~ n nudos del racimo:', round(g[['gap', 'n']].corr().iloc[0, 1], 3))

# ---- 3. cola, primer nudo y longitud ----
last = sub.groupby(['kfg', 'cuerda']).tail(1)[['kfg', 'cuerda', 'pos', 'tipo']]
cc = c.merge(last, on=['kfg', 'cuerda'], how='inner', suffixes=('', '_ult'))
cc = cc[(cc.largo > 0) & (cc.pos_max <= cc.largo + 0.01)]
print('\n--- cola (largo - pos del último racimo) ---')
print(cc.cola.describe(percentiles=[.05, .25, .5, .75, .95]).round(2).to_dict())
print('cola ~ n_clusters:', round(cc[['cola', 'n_clusters']].corr().iloc[0, 1], 3),
      '| cola ~ logvalor:', round(cc[['cola', 'logvalor']].corr().iloc[0, 1], 3),
      '| cola ~ pos_max:', round(cc[['cola', 'pos_max']].corr().iloc[0, 1], 3))
print('largo ~ pos_max R2:', round(np.corrcoef(cc.largo, cc.pos_max)[0, 1] ** 2, 3))
# ICC de cola por quipu (¿estilo del fabricante?)
grp = cc.groupby('kfg').cola
mu = cc.cola.mean()
between = grp.mean().sub(mu).pow(2).mul(grp.size()).sum()
total = cc.cola.sub(mu).pow(2).sum()
print('fracción de varianza de la cola entre quipus (eta2):', round(between / total, 3))

# cola por color simple dentro de quipu (solo descriptivo)
s = cc[cc.color_simple.notna() & (cc.color_simple != 'MIX')]
vc = s.color_simple.value_counts()
keep = vc[vc >= 300].index
print('cola mediana por color simple (n>=300):')
print(s[s.color_simple.isin(keep)].groupby('color_simple').cola.agg(['count', 'median']).round(2).sort_values('median').to_string())

# ---- 4. ¿la amplitud de los nudos se relaciona con el número de dígitos? ----
cc['span'] = cc.pos_max - cc.pos_min
print('\nspan vs n_clusters corr:', round(cc[['span', 'n_clusters']].corr().iloc[0, 1], 3),
      '| span/largo:', cc.span.div(cc.largo).describe(percentiles=[.1, .5, .9]).round(2).to_dict())
print('posición del primer nudo ~ largo:', round(cc[['pos_min', 'largo']].corr().iloc[0, 1], 3),
      '| primer nudo/largo:', cc.pos_min.div(cc.largo).describe(percentiles=[.1, .5, .9]).round(3).to_dict())
