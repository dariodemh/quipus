# -*- coding: utf-8 -*-
"""KH0083: nudos raros, conteo de nudos vs valor, E fuera de unidades."""
import pandas as pd, re
from collections import Counter
C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy().sort_values('orden').reset_index(drop=True)
K['real'] = K['nudos'].notna()

tok = re.compile(r'(\d+)([A-Z]+)\(([\d.]+),([SZU?])\)')

def clusters(s):
    return tok.findall(str(s))

# n de nudos por cuerda
nk = []
for s in K['nudos']:
    n = sum(int(m[0]) for m in clusters(s)) if pd.notna(s) else 0
    nk.append(n)
K['n_nudos'] = nk

print('== tipos de racimo y direccion (KH0083) ==')
allc = []
for s in K['nudos'].dropna():
    allc += clusters(s)
print('tipos:', Counter(m[1] for m in allc))
print('dirs :', Counter(m[3] for m in allc))

# E/EE fuera de la ultima posicion (patron "E sobre unidades")
weird = []
for _, r in K.iterrows():
    if pd.isna(r['nudos']):
        continue
    cs = clusters(r['nudos'])
    for i, m in enumerate(cs):
        if m[1] in ('E', 'EE') and i != len(cs) - 1:
            weird.append((r['cuerda'], r['valor'], r['nudos']))
print('\n== cuerdas con E/EE NO en la posicion final (n=%d) ==' % len(weird))
for w in weird[:15]:
    print('  ', w[0], w[1], '|', w[2])

# valor == n de nudos ? (conteo unario)
eq = K[(K['real']) & (K['valor'] == K['n_nudos']) & (K['valor'] > 0)]
print('\n== cuerdas con valor == n de nudos (unario): %d de %d reales ==' % (len(eq), int(K['real'].sum())))
print('  ejemplos:', list(eq['cuerda'].head(8)))

# BL
bl = K[K['nudos'].astype(str).str.contains('BL', na=False)]
print('\n== cuerdas con tipo BL:', len(bl))
for r in bl.itertuples():
    print('  ', r.cuerda, r.valor, '|', r.nudos)

# valor max por nivel
print('\n== valor: max/mediana por nivel ==')
print(K[K['valor'] > 0].groupby('nivel')['valor'].agg(['count', 'max', 'median']).to_string())
