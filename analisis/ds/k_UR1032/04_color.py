"""UR1032 — patron de color, W como marcador, secuencia por grupo."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()
col['pos'] = col.groupby('grupo').cumcount()

# color abreviado por cuerda (agrupar rangos a su primer token)
def ab(c):
    if pd.isna(c): return '?'
    c = str(c)
    for tok in c.replace('(', ':').replace(')', ':').replace('/', ':').replace('-', ':').split(':'):
        tok = tok.strip()
        if tok and tok[0].isalpha():
            return tok[:3]
    return '?'
col['cab'] = col.color.map(ab)
s['cab'] = s.color.map(ab)

print('colores abreviados colgantes:'); print(col.cab.value_counts().to_dict())
print('\n=== secuencia de color por grupo (colgantes) ===')
for gid, sub in col.groupby('grupo'):
    seq = ''.join('W' if x == 'W' else ('.' if x in ('LB',) else x[0]) for x in sub.cab)
    vals = ','.join(str(int(v)) for v in sub.valor)
    print(f'g{gid:>3}: {seq:<7} v[{vals}]')
