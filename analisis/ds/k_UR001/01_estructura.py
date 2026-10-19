# -*- coding: utf-8 -*-
"""UR001 (KH0237, Leymebamba). Reconstruccion estructural.
Salida compacta a stdout; tablas completas a CSV en esta carpeta."""
import pandas as pd, numpy as np, json

D = 'analisis/datos/'
d = pd.read_csv(D+'cuerdas.csv')
g = pd.read_csv(D+'grupos.csv')
q = pd.read_csv(D+'quipus.csv')
pd.set_option('display.width', 200)

r = d[d.kfg=='UR001'].copy().sort_values('orden').reset_index(drop=True)
gr = g[g.kfg=='UR001'].copy()

print('=== METADATOS ===')
print(q[q.kfg=='UR001'][['okr','museo','procedencia','region','pc_largo','pc_color','pc_estructura']].to_string(index=False))

print('\n=== TAMANO ===')
print('cuerdas:', len(r), '| nivel0:', (r.nivel==0).sum(), 'nivel1:', (r.nivel==1).sum(), 'nivel2:', (r.nivel==2).sum())
print('grupos:', r.grupo.nunique(), '| nudos totales:', r.nudos.notna().sum(), '| sin nudos:', r.nudos.isna().sum())

print('\n=== UNION ===')
print(r.union.value_counts(dropna=False).to_string())
print('union T (cuerda superior):', (r.union=='T').sum())

print('\n=== TORSION ===')
print(r.torsion.value_counts(dropna=False).to_string())

print('\n=== COLOR (top 12) ===')
print(r.color.value_counts().head(12).to_string())
print('colores distintos:', r.color.nunique())
print('colores con mezcla (":"):', r.color.str.contains(':').sum())

print('\n=== VALORES ===')
print('valor>0:', (r.valor>0).sum(), '| valor==0 con nudos:', ((r.valor==0)&r.nudos.notna()).sum())
print('max:', r.valor.max(), '| mediana:', r.valor.median())

# direcciones de nudo
import re
dirs = r.nudos.dropna().str.findall(r'\d+[SLE]+\([\d.]+,[SZU]\)').explode().dropna()
dd = dirs.str.extract(r',(\w)\)')[0].value_counts()
print('\n=== DIRECCIONES DE NUDO (S/Z/U) ===')
print(dd.to_string())

# cuerdas por grupo
r['_es_pend'] = r.nivel==0
gc = r[r.nivel==0].groupby('grupo').size()
print('\n=== CUERDAS POR GRUPO (pendientes) ===')
print('min', gc.min(), 'max', gc.max(), 'mediana', int(gc.median()))
print(gc.describe().round(2).to_string())

# subsidiarias por pendiente
sub = r[r.nivel>0].groupby(r[r.nivel>0].padre.str.extract(r'(p\d+)$')[0]).size()
print('\n=== SUBSIDIARIAS POR COLGANTE (top 15) ===')
print(sub.sort_values(ascending=False).head(15).to_string())
print('pendientes con >=1 subsidiaria:', sub.shape[0], '| max sub:', sub.max())

# guardar
r.to_csv('analisis/ds/k_UR001/ur001_cuerdas.csv', index=False)
gr.to_csv('analisis/ds/k_UR001/ur001_grupos.csv', index=False)
print('\n[guardado ur001_cuerdas.csv, ur001_grupos.csv]')
