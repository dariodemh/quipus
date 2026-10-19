# -*- coding: utf-8 -*-
"""KH0083: reconstruccion de estructura. Salida acotada (~40 lineas)."""
import pandas as pd, numpy as np

C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy()
K['real'] = K['nudos'].notna()          # tiene nudos => valor real
K = K.sort_values('orden').reset_index(drop=True)

print('== total cuerdas:', len(K), '| colgantes:', (K.nivel == 0).sum())
print('== por nivel =='); print(K.nivel.value_counts().sort_index().to_string())

# hijos directos
child_count = K.groupby('padre')['cuerda'].count()
K['n_hijos'] = K['cuerda'].map(child_count).fillna(0).astype(int)

col = K[K.nivel == 0]
print('\n== colgantes por grupo (colgantes) ==')
gg = col.groupby('grupo')['cuerda'].count()
print('grupos:', gg.shape[0], '| tamaño: min', gg.min(), 'max', gg.max(), 'media %.2f' % gg.mean())
print('distribucion tamano grupo:'); print(gg.value_counts().sort_index().to_string())

print('\n== subsidiarias por colgante ==')
print('colgantes con 0/1/2/3+ hijas directas:',
      ((col.n_hijos == 0).sum(), (col.n_hijos == 1).sum(),
       (col.n_hijos == 2).sum(), (col.n_hijos >= 3).sum()))
print('profundidad maxima (nivel):', K.nivel.max())

print('\n== union x nivel ==')
print(pd.crosstab(K.nivel, K.union).to_string())

print('\n== torsion ==', K.torsion.value_counts().to_dict())
print('== terminacion =='); print(K.terminacion.value_counts(dropna=False).head(8).to_string())

# color primario (primer token antes de : / - )
def prim(s):
    if pd.isna(s): return 'NA'
    s = str(s).split(':')[0].split('/')[0].split('-')[0]
    return s.strip()
K['col1'] = K['color'].map(prim)
print('\n== color primario (top 12) ==')
print(K['col1'].value_counts().head(12).to_string())
print('\n== color primario SOLO colgantes (top 12) ==')
print(col['color'].map(prim).value_counts().head(12).to_string())

# direccion de nudos
def dirs(s):
    import re
    if pd.isna(s): return []
    return re.findall(r'\([^,]+,\s*([SZU?])\)', str(s))
alld = []
for s in K['nudos']:
    alld.extend(dirs(s))
from collections import Counter
print('\n== direccion de nudos (clusteres) ==', Counter(alld).most_common())
