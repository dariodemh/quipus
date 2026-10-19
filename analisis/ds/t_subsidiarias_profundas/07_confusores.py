# -*- coding: utf-8 -*-
"""Control de confusores: tamano del quipu y procedencia.
Ajusta regresion logistica (profundo ~ log cuerdas + Incahuasi) y
Poisson (n arboles ~ log pendants + Incahuasi). Reporta tambien tasas
estratificadas por tamano."""
import pandas as pd, numpy as np, os, json
import statsmodels.api as sm
import statsmodels.formula.api as smf

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
q = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'quipus.csv'))
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))

n_c = d.groupby('kfg').size().rename('ncuerdas')
n_p = d[d.nivel == 0].groupby('kfg').size().rename('npend')
n_a = T.groupby('kfg').size().rename('narboles')
n_n3 = T.groupby('kfg').n_nivel3.sum().rename('n_nivel3')
Q = q[['kfg', 'procedencia']].copy()
Q = Q.merge(n_c, on='kfg', how='left').merge(n_p, on='kfg', how='left')
Q = Q.merge(n_a, on='kfg', how='left').merge(n_n3, on='kfg', how='left').fillna(0)
Q['inca'] = Q.procedencia.astype(str).str.contains('Incahuasi', case=False).astype(int)
Q['profundo'] = (Q.narboles > 0).astype(int)
Q['ln'] = np.log(Q.ncuerdas)
Q['lnp'] = np.log(Q.npend)

print('n=%d quipus | profundos=%d' % (len(Q), Q.profundo.sum()))
print('\nTasas por tamano (cuerdas):')
Q['bin'] = pd.cut(Q.ncuerdas, [0, 50, 100, 200, 400, 10000], labels=['<50', '50-99', '100-199', '200-399', '>=400'])
print(Q.groupby('bin', observed=True).agg(quipus=('kfg', 'size'), profundos=('profundo', 'sum'),
                                          pct=('profundo', lambda s: 100*s.mean())).to_string())

print('\nDentro de >=100 cuerdas: Incahuasi vs resto')
big = Q[Q.ncuerdas >= 100]
print(big.groupby('inca').agg(quipus=('kfg', 'size'), profundos=('profundo', 'sum'),
                              pct=('profundo', lambda s: 100*s.mean())).to_string())
from scipy.stats import fisher_exact
a = int(big[(big.inca == 1)].profundo.sum()); b = int((big.inca == 1).sum() - a)
c = int(big[(big.inca == 0)].profundo.sum()); e = int((big.inca == 0).sum() - c)
print('  Fisher: OR=%.2f p=%.4f' % (fisher_exact([[a, b], [c, e]])[0], fisher_exact([[a, b], [c, e]])[1]))

print('\n--- Logit profundo ~ ln(cuerdas) + Incahuasi')
m1 = smf.logit('profundo ~ ln + inca', data=Q).fit(disp=0)
print(m1.summary2().tables[1].round(4).to_string())
print('  OR inca=%.2f (IC95 %.2f-%.2f) p=%.4f' % (np.exp(m1.params['inca']),
      np.exp(m1.conf_int().loc['inca', 0]), np.exp(m1.conf_int().loc['inca', 1]), m1.pvalues['inca']))
print('  OR x2 cuerdas=%.2f' % np.exp(m1.params['ln'] * np.log(2)))

print('\n--- Poisson n_arboles ~ ln(pendants) + Incahuasi (solo quipus con >=1 profundo)')
sub = Q[Q.profundo == 1].copy()
m2 = smf.glm('narboles ~ lnp + inca', data=sub, family=sm.families.Poisson()).fit()
print(m2.summary2().tables[1].round(4).to_string())
print('  IRR inca=%.2f p=%.4f' % (np.exp(m2.params['inca']), m2.pvalues['inca']))

print('\n--- Poisson n_nivel3 ~ ln(cuerdas) + Incahuasi (todos)')
m3 = smf.glm('n_nivel3 ~ ln + inca', data=Q, family=sm.families.Poisson()).fit()
print(m3.summary2().tables[1].round(4).to_string())
print('  IRR inca=%.2f p=%.4f' % (np.exp(m3.params['inca']), m3.pvalues['inca']))

# proporcion de nivel>=3 dentro del quipu
Q['prop_n3'] = Q.n_nivel3 / Q.ncuerdas
print('\nProporcion de cuerdas en nivel>=3: mediana %.4f | max %.3f (%s)' %
      (Q.prop_n3.median(), Q.prop_n3.max(), Q.loc[Q.prop_n3.idxmax(), 'kfg']))
print(Q.sort_values('prop_n3', ascending=False).head(8)[['kfg', 'ncuerdas', 'narboles', 'n_nivel3', 'prop_n3', 'inca']].to_string(index=False))

Q.to_csv(os.path.join(OUT, 'quipus_contexto.csv'), index=False)
json.dump(dict(logit_inca_or=float(np.exp(m1.params['inca'])), logit_inca_p=float(m1.pvalues['inca']),
               logit_ln_or=float(np.exp(m1.params['ln'])), logit_ln_p=float(m1.pvalues['ln']),
               poisson_inca_irr=float(np.exp(m2.params['inca'])), poisson_inca_p=float(m2.pvalues['inca']),
               fisher_big_or=float(fisher_exact([[a, b], [c, e]])[0]),
               fisher_big_p=float(fisher_exact([[a, b], [c, e]])[1])),
          open(os.path.join(OUT, 'confusores.json'), 'w'), indent=2)
