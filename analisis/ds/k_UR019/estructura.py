# -*- coding: utf-8 -*-
"""Reconstruccion de la estructura de UR019 (KFG UR019 = OKR KH0255, CMA-480/LC1-109.3).
Solo lectura de datos. Imprime tablas pequenas.
"""
import pandas as pd, sqlite3, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
G = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'grupos.csv'))
Q = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'quipus.csv'))

KP = 'UR019'
d = C[C['kfg'] == KP].sort_values('orden').reset_index(drop=True)
g = G[G['kfg'] == KP].reset_index(drop=True)
q = Q[Q['kfg'] == KP].iloc[0]

pd.set_option('display.width', 220); pd.set_option('display.max_colwidth', 45)
print('=== METADATOS ===')
print(q.to_dict())
print('n cuerdas:', len(d), '| grupos:', len(g))
print()
print('=== GRUPOS (posicion en cm sobre el cordon principal) ===')
print(g.to_string(index=False))
print()
print('=== CUERDAS ===')
cols = ['orden','cuerda','tipo','nivel','padre','grupo','valor','alt','nudos','color','torsion','union','largo','terminacion','notas']
print(d[cols].to_string(index=False))

# --- union T = cuerdas superiores?
print()
print('union counts:', d['union'].value_counts().to_dict())
print('cuerdas con union T (superiores):', d[d['union']=='T']['cuerda'].tolist())
print('nudos por direccion (parseo de la cadena nudos):')
import re
for _,r in d.iterrows():
    if pd.isna(r['nudos']):
        continue
    dirs = re.findall(r'\([0-9.]+,([SZU])\)', str(r['nudos']))
    print(' ', r['cuerda'], dirs)
