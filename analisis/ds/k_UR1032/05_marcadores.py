"""UR1032 — singletons/marcadores, direccion de nudo, verificacion color-tamano."""
import pandas as pd, numpy as np, re
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()

# tamano y color dominante por grupo
def ab(c):
    if pd.isna(c): return '?'
    for tok in re.split(r'[^A-Za-z]+', str(c)):
        if tok: return tok[:3]
    return '?'
col['cab'] = col.color.map(ab)
tam = col.groupby('grupo').size()
print('== color dominante vs tamano de grupo ==')
res = col.groupby('grupo').cab.agg(lambda x: x.value_counts().to_dict())
for gid in range(108):
    t = tam[gid]
    d = res[gid]
    mix = 'MIX' if len(d) > 1 else list(d)[0]
    print(f'g{gid:>3} tam={t} {d} {mix}')
