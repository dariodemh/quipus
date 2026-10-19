# -*- coding: utf-8 -*-
"""Archivo de Nazca y Atarco: descripcion del conjunto.
Lee analisis/datos/*.csv y produce tabla por quipu.
"""
import pandas as pd, numpy as np, os, sys

ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')

c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
g = pd.read_csv(os.path.join(D, 'grupos.csv'))

NOMBRES = ['Nazca', 'Atarco']
sub_q = q[q['procedencia'].isin(NOMBRES)].copy()
KFG = sub_q['kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy()

def tiene_sumas(grp):
    """Presencia de sumas: por grupo, si un colgante = suma de sus subsidiarias."""
    n = 0
    for kfg, df in grp.groupby('kfg'):
        for _, row in df[df['nivel'] == 0].iterrows():
            subs = df[df['padre'] == row['cuerda']]
            if len(subs) and row['valor'] > 0:
                if abs(subs['valor'].sum() - row['valor']) < 1e-6:
                    n += 1
    return n

def rango_nudos(nudos):
    """Direcciones de nudo presentes en una cadena."""
    dirs = set()
    if not isinstance(nudos, str):
        return dirs
    import re
    for m in re.finditer(r'([SLEU]+)\(([\d.]+),([SZU])\)', nudos):
        dirs.add(m.group(3))
    return dirs

rows = []
for kfg, df in s.groupby('kfg'):
    df = df.sort_values('orden')
    top = df[df['union'] == 'T']
    dirs = set()
    for nu in df['nudos'].dropna():
        dirs |= rango_nudos(nu)
    col = df['color'].dropna()
    coltop = col.value_counts().head(3)
    vals = df.loc[df['nivel'] == 0, 'valor']
    rows.append({
        'kfg': kfg,
        'okr': sub_q.loc[sub_q['kfg'] == kfg, 'okr'].values[0],
        'proc': sub_q.loc[sub_q['kfg'] == kfg, 'procedencia'].values[0],
        'museo': sub_q.loc[sub_q['kfg'] == kfg, 'museo'].values[0][:24],
        'N_cuerdas': len(df),
        'N_colg': (df['nivel'] == 0).sum(),
        'N_subs': (df['nivel'] >= 1).sum(),
        'N_top': len(top),
        'N_grp': df['grupo'].nunique(),
        'vmin': int(vals.min()), 'vmax': int(vals.max()),
        'suma_grupo': tiene_sumas(df),
        'tors_S': (df['torsion'] == 'S').sum(),
        'tors_Z': (df['torsion'] == 'Z').sum(),
        'u_R': (df['union'] == 'R').sum(),
        'u_V': (df['union'] == 'V').sum(),
        'u_U': (df['union'] == 'U').sum(),
        'dir': ''.join(sorted(dirs)),
        'colores_top': ';'.join(f'{k}:{v}' for k, v in coltop.items()),
        'pc_color': sub_q.loc[sub_q['kfg'] == kfg, 'pc_color'].values[0],
    })

res = pd.DataFrame(rows).sort_values(['proc', 'kfg'])
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 40)
print(res.to_string(index=False))

print('\n=== TOTAL cuerdas %d, colgantes %d, subsidiarias %d ===' %
      (len(s), (s['nivel'] == 0).sum(), (s['nivel'] >= 1).sum()))
print('niveles:', s['nivel'].value_counts().to_dict())
print('union global:', s['union'].value_counts(dropna=False).to_dict())
print('torsion global:', s['torsion'].value_counts(dropna=False).to_dict())
res.to_csv(os.path.join(ROOT, 'analisis', 'ds', 'a_nazca', 'tabla_quipus.csv'), index=False)
