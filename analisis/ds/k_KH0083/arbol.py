# -*- coding: utf-8 -*-
"""Imprime subarboles elegidos de KH0083 de forma compacta (indentada)."""
import pandas as pd, sys

C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy().sort_values('orden').reset_index(drop=True)
ch = {}
for _, r in K.iterrows():
    if pd.notna(r['padre']):
        ch.setdefault(r['padre'], []).append(r['cuerda'])
rec = {r['cuerda']: r for _, r in K.iterrows()}

def show(name, depth=0, maxdepth=5):
    r = rec[name]
    val = f'{r.valor:g}' if pd.notna(r.valor) else '?'
    knot = 'K' if pd.notna(r.nudos) else '-'
    z = 'Z' if (isinstance(r['nudos'], str) and ',Z)' in r['nudos']) else ' '
    print('  ' * depth + f'{name:22s} v={val:>6s} {knot}{z} c={str(r.color)[:22]}')
    if depth < maxdepth:
        for c in sorted(ch.get(name, []), key=lambda x: x):
            show(c, depth + 1, maxdepth)

roots = sys.argv[1:] if len(sys.argv) > 1 else ['p13', 'p14', 'p46', 'p48']
for rt in roots:
    print('=== ' + rt + ' ===')
    show(rt)
