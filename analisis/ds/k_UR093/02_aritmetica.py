# -*- coding: utf-8 -*-
"""UR093: aritmetica interna."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy()
u['valor'] = u.valor.fillna(0)

n0 = u[u.nivel == 0].copy()
# suma de subsidiarias directas (nivel1 con padre = colgante)
sub1 = u[u.nivel == 1].groupby('padre').valor.sum()
sub2 = u[u.nivel == 2].groupby('padre').valor.sum()  # suma nivel2 por su madre nivel1
# reconstruir suma total por colgante = sub1 directas + (para cada sub1, sus nivel2)
# suma recursiva: valor de cada nivel1 + sus nivel2
lvl1 = u[u.nivel == 1].copy()
lvl1['val_total'] = lvl1.valor
l2sum = u[u.nivel==2].groupby('padre').valor.sum()
lvl1['val_total'] = lvl1['valor'] + lvl1.padre.map(lambda p: l2sum.get(p,0))
tot1 = lvl1.groupby('padre').val_total.sum()

n0['sum_subs'] = n0.cuerda.map(lambda p: tot1.get(p, np.nan))
n0['n_subs'] = n0.cuerda.map(lambda p: (u.padre==p).sum())
n0['tiene_subs'] = n0.n_subs > 0

# caso 1: colgante = suma subsidiarias (donde tiene subs)
con = n0[n0.tiene_subs]
match = con[con.valor == con.sum_subs]
print('== COLGANTE = SUMA SUBS (solo con subs) ==')
print('pendants con subs:', len(con), ' matches exactos:', len(match))
print('  tasa match:', round(len(match)/len(con),4))
# sin subs que tengan valor distinto de 0
sin = n0[~n0.tiene_subs]
print('pendants sin subs:', len(sin), 'con valor>0:', (sin.valor>0).sum())

# suma total del quipu
print('\ntotal valor nivel1 (hojas):', u[u.nivel==1].valor.sum())
print('total nivel0:', n0.valor.sum())
print('total todo:', u.valor.sum())

# grupo = suma de grupos (no hay top cords); revisar si grupo suma coincide con algo
print('\n== grupos: suma de valores nivel0 por grupo ==')
gg = n0.groupby('grupo').valor.agg(['sum','count'])
print(gg.to_string())

# valores repetidos
print('\n== valores mas frecuentes (nivel0) ==')
print(n0.valor.value_counts().head(15).to_dict())
print('== valores mas frecuentes (nivel1) ==')
print(u[u.nivel==1].valor.value_counts().head(15).to_dict())

n0.to_csv('analisis/ds/k_UR093/colgantes.csv', index=False)
print('\nguardado colgantes.csv')
