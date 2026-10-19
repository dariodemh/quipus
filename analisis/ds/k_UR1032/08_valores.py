"""UR1032 — valores por posicion dentro de grupo; lectura binaria; valores>=5."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()
col['size'] = col.groupby('grupo')['grupo'].transform('size')
col['pos'] = col.groupby('grupo').cumcount()

print('== valor medio/no-nulo por posicion, en grupos de 5 (azul) ==')
g5 = col[col['size'] == 5]
print(g5.groupby('pos').valor.agg(['count','mean','sum', lambda x:(x>0).mean()]).rename(columns={'<lambda_0>':'frac>0'}))
print('\n== valor por posicion en grupos de 3 (blanco) ==')
g3 = col[col['size'] == 3]
print(g3.groupby('pos').valor.agg(['count','mean','sum', lambda x:(x>0).mean()]).rename(columns={'<lambda_0>':'frac>0'}))

print('\n== valores >=5 ==')
print(col[col.valor >= 5][['orden','cuerda','grupo','valor','nudos','color','size']].to_string())

print('\n== nudos con S simple (decenas?) ==')
print(s[s.nudos.notna() & s.nudos.str.contains(r'\dS\(')][['orden','cuerda','grupo','valor','nudos']].to_string())

# total colgantes con al menos un nudo
print('\ncolgantes con nudo:', int((col.valor>0).sum()), 'de', len(col))
print('colgantes vacios:', int((col.valor==0).sum()))
