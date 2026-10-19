"""UR231: plantilla de 6 conjuntos x 14 ranuras (alineada por el grupo 0D)."""
import pandas as pd, numpy as np
from scipy import stats

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
g = pd.read_csv(OUT + 'grupos_resumen.csv').set_index('grupo')

# inicio de cada conjunto = grupo 0D - 4 (el 0D ocupa la ranura 5)
starts = [(-2, 'A'), (11, 'B'), (23, 'C'), (37, 'D'), (51, 'E'), (65, 'F')]
rows = []
for s, name in starts:
    for slot in range(1, 15):
        gg = s + slot - 1
        if gg < 0 or gg > 79:
            rows.append(dict(set=name, slot=slot, grupo=gg, color='(falta)', n=0, nval=0, suma=0, fiber=''))
        else:
            r = g.loc[gg]
            rows.append(dict(set=name, slot=slot, grupo=gg, color=str(r.color).split('(')[0],
                             n=int(r.n), nval=int(r.nval), suma=float(r.suma), fiber=str(r.fiber)))
T = pd.DataFrame(rows)
T.to_csv(OUT + 'plantilla_6x14.csv', index=False)

print('Ranura: color | nval/suma  (seis conjuntos)')
for slot in range(1, 15):
    d = T[T.slot == slot]
    print('%2d: ' % slot + ' | '.join('%s %s%s' % (r.color[:9], '' if r.nval == 0 else '%d/%d' % (r.nval, r.suma), '' if r.fiber != 'V' else ' [V]') for _, r in d.iterrows()))

# proporciones entre ranuras cuantificadas
piv = T.pivot_table(index='set', columns='slot', values='suma', aggfunc='sum')
piv = piv.reindex(['A', 'B', 'C', 'D', 'E', 'F'])
print('\nTotales por ranura (solo ranuras con datos):')
print(piv[[2, 3, 5, 6, 8]].astype(int).to_string())
print('\nRazon 6/5:', np.round((piv[6] / piv[5]).values, 2))
print('Razon 6/8:', np.round((piv[6] / piv[8]).values, 2))
print('Razon 8/5:', np.round((piv[8] / piv[5]).values, 2))
print('\nPor cuerda con valor:')
print((piv[[5, 6, 8]] / T.pivot_table(index='set', columns='slot', values='nval', aggfunc='sum').reindex(['A', 'B', 'C', 'D', 'E', 'F'])[[5, 6, 8]]).round(1).to_string())
r = piv.loc[['B', 'C', 'D', 'E', 'F']]
print('\nB-F razon 6/5: media %.2f sd %.2f CV %.1f%%' % ((r[6] / r[5]).mean(), (r[6] / r[5]).std(), (r[6] / r[5]).std() / (r[6] / r[5]).mean() * 100))
