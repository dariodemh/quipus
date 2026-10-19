# -*- coding: utf-8 -*-
"""UR093: reconstruccion estructural completa (resumenes cortos)."""
import pandas as pd, numpy as np, re, json
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
G = pd.read_csv('analisis/datos/grupos.csv', low_memory=False)
Q = pd.read_csv('analisis/datos/quipus.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
g = G[G.kfg == 'UR093'].copy()
u['valor'] = u.valor.fillna(0)

print('== BASICO ==')
print('cuerdas', len(u), '| orden', u.orden.min(), u.orden.max(), '| niveles', u.nivel.value_counts().sort_index().to_dict())
print('grupos', g.grupo.nunique(), '| tipo', u.tipo.value_counts().to_dict())
print('union', u.union.value_counts(dropna=False).to_dict())
print('torsion', u.torsion.value_counts(dropna=False).to_dict())
print('terminacion', u.terminacion.value_counts(dropna=False).head(10).to_dict())
print('pc', Q[Q.kfg=='UR093'][['pc_largo','pc_color']].to_dict('records'))

print('\n== NIVEL 0 por grupo ==')
n0 = u[u.nivel == 0]
print(n0.groupby('grupo').size().to_dict())
print('grupo de nivel1/2:', u[u.nivel>0].grupo.value_counts(dropna=False).sort_index().to_dict())

print('\n== SUBSIDIARIAS ==')
l1 = u[u.nivel == 1]; l2 = u[u.nivel == 2]
sp = l1.groupby('padre').size()
print('colgantes con >=1 sub:', len(sp), 'de', len(n0))
print('dist num subs:', sp.value_counts().sort_index().to_dict())
print('nivel2: cuerdas', len(l2), 'madres nivel1', l2.padre.nunique())
print('subs por nivel0 (recursivo):')
def count_all(name):
    return (u.padre == name).sum() + sum(count_all(c) for c in u[u.padre == name].cuerda)
tot = n0.cuerda.map(count_all)
print(tot.value_counts().sort_index().to_dict())

print('\n== SIN NUDOS ==')
sn = u[u.nudos.isna()]
print('total', len(sn), 'por nivel', sn.nivel.value_counts().sort_index().to_dict(),
      'por grupo', sn.grupo.value_counts().sort_index().to_dict())
print('valores distintos de sin nudos:', sorted(sn.valor.unique()))
print('colores sin nudos:', sn.color.value_counts().head(8).to_dict())

print('\n== COLORES ==')
print('n colores unicos', u.color.nunique(), '| nivel0 top', n0.color.value_counts().head(12).to_dict())
print('colores con ":"', u.color.str.contains(':', na=False).sum(),
      '| con "-"', u.color.str.contains('-', na=False).sum(),
      '| con "/"', u.color.str.contains('/', na=False).sum())
print('\n== LARGOS ==')
print(u.groupby('nivel').largo.describe()[['count','mean','50%','max']].round(1).to_string())
print('\n== VALORES ==')
print('suma total', u.valor.sum(), '| nivel0', n0.valor.sum(), '| nivel1', l1.valor.sum(), '| nivel2', l2.valor.sum())
print('n con valor>0', (u.valor>0).sum(), '| max', u.valor.max(), '| valor 0 con nudos no vacio:', ((u.valor==0)&u.nudos.notna()).sum())
print('multiplos de 10:', (u.valor[u.valor>0]%10==0).sum(), 'de', (u.valor>0).sum())
print('\n== NUDOS: direccion ==')
dirs = re.findall(r'(\d*)([SLE]+)\(([\d.]+),([SZU])\)', ';'.join(u.nudos.dropna()))
from collections import Counter
print(Counter(d[3] for d in dirs))
print('tipos:', Counter(d[1][0] for d in dirs))
