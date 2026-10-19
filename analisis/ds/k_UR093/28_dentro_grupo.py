# -*- coding: utf-8 -*-
"""UR093: control de la correlacion colgante-subsidiarias dentro de grupo,
y descriptivos finales / anomalias."""
import pandas as pd, numpy as np
from scipy.stats import spearmanr, chi2_contingency, kruskal
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l0 = u[u.nivel == 0]; l1 = u[u.nivel == 1]
child = {}
for c, p in zip(u.cuerda, u.padre):
    if pd.notna(p): child.setdefault(p, []).append(c)
def subtree(c):
    return int(u.set_index('cuerda').valor[c]) + sum(subtree(k) for k in child.get(c, []))
rows = []
for p in l0.cuerda:
    if p in child:
        rows.append((p, int(l0[l0.cuerda == p].valor.iloc[0]), sum(subtree(k) for k in child[p]),
                     int(l0[l0.cuerda == p].grupo.iloc[0])))
d = pd.DataFrame(rows, columns=['p', 'val', 'sumsub', 'grupo'])
d = d[d.sumsub > 0]
print('colgantes con sumsub>0:', len(d))
print('Spearman global:', round(spearmanr(d.val, d.sumsub).statistic, 3))
# dentro de grupo: rho ponderado por n
rhos = []
for g, grp in d.groupby('grupo'):
    if len(grp) >= 4 and grp.val.nunique() > 1 and grp.sumsub.nunique() > 1:
        r = spearmanr(grp.val, grp.sumsub).statistic
        rhos.append((g, len(grp), r))
        print(' grupo', g, 'n', len(grp), 'rho', round(r, 3))
print('rho medio dentro de grupo:', round(np.nanmean([x[2] for x in rhos]), 3), 'en', len(rhos), 'grupos')

# nulo: permutar val dentro de grupo
rng = np.random.default_rng(0); sim = []
for _ in range(1000):
    dd = d.copy()
    dd['val'] = dd.groupby('grupo').val.transform(lambda s: rng.permutation(s.values))
    sim.append(spearmanr(dd.val, dd.sumsub).statistic)
sim = np.array(sim); obs = spearmanr(d.val, d.sumsub).statistic
print('p permutation (val dentro de grupo):', (1 + (sim >= obs).sum()) / 1001, '| nulo media', round(sim.mean(), 3))

# chi2 color familia vs valor>0 (colgantes)
def fam(c):
    c = str(c).split('(')[0]; c = c.split(':')[0].split('-')[0].split('/')[0]
    return {'W': 'blanco', 'AB': 'marron', 'MB': 'marron', 'KB': 'marron', 'YB': 'amarillo',
            'RB': 'rojo', 'RL': 'rojo'}.get(c, 'otro')
l0 = l0.assign(fam=l0.color.map(fam), pos=l0.valor > 0)
ct = pd.crosstab(l0.fam, l0.pos)
print('\nchi2 color familia x valor>0:', ct.values.tolist(), 'p=', round(chi2_contingency(ct).pvalue, 4))
ctg = pd.crosstab(l0.grupo, l0.pos)
print('chi2 grupo x valor>0 p=', round(chi2_contingency(ctg).pvalue, 4))
print('Kruskal valor por grupo p=', round(kruskal(*[g.valor.values for _, g in l0.groupby('grupo')]).pvalue, 4))

print('\n== ANOMALIAS ==')
print('union U:', u[u.union == 'U'][['cuerda','nivel','grupo','valor','color','largo','notas']].to_string(max_colwidth=40))
print('torsion no S:', u[u.torsion != 'S'][['cuerda','torsion','union','largo']].to_string())
print('terminacion U:', u[u.terminacion == 'U'][['cuerda','nivel','valor','union']].head(12).to_string(index=False))
print('cuerdas con 2 clusters:', u[u.nudos.fillna('').str.count(';') == 1].cuerda.tolist())
print('cuerdas con valor 0 y nudos:', len(u[(u.valor == 0) & u.nudos.notna()]))
print('colgantes sin nudos:', len(l0[l0.nudos.isna()]), 'de', len(l0))
print('subs sin nudos:', len(l1[l1.nudos.isna()]), 'de', len(l1))
