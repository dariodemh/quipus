# -*- coding: utf-8 -*-
"""UR001. Cuerdas 'hub' (muchas subsidiarias) y verificacion de lectura decimal."""
import pandas as pd, numpy as np
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
sub=r[r.nivel>0]
hubs=sub.padre.value_counts()
print('=== hubs (madres con mas subsidiarias) ===')
for h,n in hubs.head(6).items():
    row=r[r.cuerda==h].iloc[0]
    print(f'{h}: orden={int(row.orden)} grupo={int(row.grupo)} color={row.color} union={row.union} valor={int(row.valor)} nudos={row.nudos}')
    ch=sub[sub.padre==h]
    print('   hijas vals:',list(ch.valor.astype(int)),'| colores:',list(ch.color)[:8])

# p1 en detalle
print('\n=== p1 y sus 17 subsidiarias ===')
ch=r[r.padre=='p1']
print(ch[['cuerda','valor','color','union','torsion']].to_string(index=False))

# verificacion decimal: recomputar valor desde nudos no es trivial; solo inspeccionar
print('\n=== nudos de las 6 cuerdas mayores ===')
for _,row in r.sort_values('valor',ascending=False).head(6).iterrows():
    print(f'{row.cuerda}: {row.nudos}  (valor={int(row.valor)})')

# ¿los nudos usan posiciones decimales estandar (unidades/decenas/centenas/millares)?
print('\n=== tipos de racimo de nudo (S/L/E...) ===')
import re
allk=r.nudos.dropna().str.cat(sep=';')
kinds=re.findall(r'(\d+)([A-Z]+)\(',allk)
from collections import Counter
cnt=Counter(k[1] for k in kinds)
print(dict(cnt))
