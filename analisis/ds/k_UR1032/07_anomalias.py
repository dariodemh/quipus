"""UR1032 — marcadores (singletons), nudos, cuerdas sin nudos, valores raros."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()
sizes = col.groupby('grupo').size()

# cuerdas de los grupos singleton
print('== grupos singleton (candidatos a marcador) ==')
for gid in [0, 15, 34, 54, 72, 89]:
    r = col[col.grupo == gid]
    print(r[['orden','cuerda','grupo','valor','nudos','color','union','largo','terminacion','notas']].to_string())

print('\n== cuerdas largas (posibles cuerdas guia/madre) top largo ==')
print(s.sort_values('largo', ascending=False)[['orden','cuerda','nivel','grupo','valor','color','union','largo']].head(12).to_string())

print('\n== nudos strings distintos (top) ==')
print(s.nudos.value_counts().head(25).to_dict())

print('\n== cuerdas con nudos pero valor 0 (contradiccion) ==')
bad = s[(s.valor == 0) & s.nudos.notna()]
print(len(bad)); print(bad[['orden','cuerda','grupo','valor','nudos','color']].head(20).to_string())
