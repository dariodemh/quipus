"""UR1032 — grupos en orden, valores, colores; patron 5/3."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden')
col = s[s.nivel == 0]

# secuencia de tamaños de grupo -> patron
tam = col.groupby('grupo').size()
print('patron de tamanos (grupo:0..107):')
print(list(zip(tam.index, tam.values)))
