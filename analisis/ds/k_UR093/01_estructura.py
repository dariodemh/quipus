# -*- coding: utf-8 -*-
"""UR093: reconstruccion estructural. Solo imprime resumenes cortos."""
import pandas as pd, numpy as np

C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
G = pd.read_csv('analisis/datos/grupos.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy()
g = G[G.kfg == 'UR093'].copy()

print('== BASICO ==')
print('cuerdas', len(u), 'orden', u.orden.min(), u.orden.max())
print('nivel:', u.nivel.value_counts().sort_index().to_dict())
print('union:', u.union.value_counts(dropna=False).to_dict())
print('torsion:', u.torsion.value_counts(dropna=False).to_dict())

# sin nudos
sin_nudos = u[u.nudos.isna()]
print('\n== SIN NUDOS ==', len(sin_nudos))
print('  por nivel:', sin_nudos.nivel.value_counts().sort_index().to_dict())
print('  valor de las sin nudos (unicos):', sorted(sin_nudos.valor.unique())[:10])

# nivel 0 count per grupo
n0 = u[u.nivel == 0]
print('\n== NIVEL 0 (colgantes) por grupo ==')
print(n0.grupo.value_counts().sort_index().to_dict())

# subsidiaries per pendant distribution
sub = u[u.nivel == 1]
sp = sub.groupby('padre').size()
print('\n== SUBSIDIARIAS nivel1 por madre ==')
print('madres con >=1 sub:', len(sp), 'de', n0.shape[0])
print(sp.value_counts().sort_index().to_dict())
# nivel2
sub2 = u[u.nivel == 2]
print('cuerdas nivel2:', len(sub2), 'madres n2:', sub2.padre.nunique())

# colores
print('\n== COLOR (nivel0) top ==')
print(n0.color.value_counts().head(15).to_dict())
print('colores unicos totales:', u.color.nunique())

# valores
print('\n== VALORES ==')
print('nivel0 valor stats: min', n0.valor.min(), 'max', n0.valor.max(), 'sum', n0.valor.sum())
print('nivel0 ceros:', (n0.valor==0).sum(), 'de', len(n0))
print('nivel1 ceros:', (sub.valor==0).sum(), 'de', len(sub))
print('valor entero?', (u.valor.dropna()%1==0).all())
