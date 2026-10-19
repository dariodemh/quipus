"""UR1032 — reconstruccion estructural (Nazca, 541 cuerdas)."""
import pandas as pd, numpy as np

C = pd.read_csv('analisis/datos/cuerdas.csv')
G = pd.read_csv('analisis/datos/grupos.csv')
K = 'UR1032'
s = C[C.kfg == K].copy()
g = G[G.kfg == K].copy()

print('== cabecera ==')
print('cuerdas:', len(s), '| grupos(cuerdas.csv):', s.grupo.nunique(),
      '| grupos(grupos.csv):', len(g))
print('orden rango:', s.orden.min(), s.orden.max())
print('grupos.csv desde/hasta max:', g.desde.max(), g.hasta.max())

# colgantes por grupo
col = s[s.nivel == 0]
print('\n== colgantes por grupo ==')
print(col.groupby('grupo').size().value_counts().sort_index().to_dict())

# estructura completa: madre -> subsidiarias
print('\n== primeras 60 cuerdas (orden, nombre, nivel, grupo, valor, color, union, largo) ==')
print(s.sort_values('orden')[['orden', 'cuerda', 'nivel', 'padre', 'grupo',
      'valor', 'color', 'union', 'largo', 'terminacion']].head(60).to_string())

# R vs V
print('\n== union R (recto) ==')
print(s[s.union == 'R'][['orden', 'cuerda', 'grupo', 'valor', 'color', 'largo']].to_string())

# notas
print('\n== notas no nulas ==')
print(s[s.notas.notna()][['orden', 'cuerda', 'grupo', 'valor', 'nudos', 'notas']].to_string())
