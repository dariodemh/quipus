# -*- coding: utf-8 -*-
"""Selección del archivo Ica-Ocucaje-Callango-Ullujalla-Pisco y deduplicación
de objetos que aparecen con dos nombres (AS/UR vs KH)."""
import pandas as pd, re, unicodedata, os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode()
    return s.lower()

q = pd.read_csv(os.path.join(DAT, 'quipus.csv'))
q['proc_n'] = q['procedencia'].fillna('').map(norm)

# Patrón estricto por palabra (excluye 'Arica')
tokens = ['ica', 'ocucaje', 'callango', 'callengo', 'ullujalla', 'ullujaya', 'pisco']
def match(p):
    w = re.findall(r'[a-z]+', p)
    return any(t in w for t in tokens)
sel = q[q['proc_n'].map(match)].copy()
print('Quipus seleccionados:', len(sel))

# OKR / KH numbers -> detectar mismo objeto con dos nombres
okr = pd.read_csv(os.path.join(RAIZ, 'data', 'external', 'open-khipu-repository',
                               'data', 'okr-kh-numbers.csv'))
print('OKR-KH filas:', len(okr))

# Nombres alternos: mapear varios nombres al OKR canónico
alt2okr = {}
for _, r in okr.iterrows():
    okrnum = str(r['OKR Number']).strip()
    for nm in str(r['Other Names']).split(','):
        nm = nm.strip()
        if nm and nm != 'nan':
            alt2okr[nm] = okrnum

# Para cada quipu seleccionado, calcular su "objeto canónico"
def canon(row):
    idn = str(row['kfg']).strip()
    o = str(row['okr']).strip()
    # preferir OKR Number (KH...) si existe
    if o.startswith('KH'):
        return o
    # si el id es un nombre alterno, resolver
    if idn in alt2okr:
        return alt2okr[idn]
    if o in alt2okr:
        return alt2okr[o]
    return 'KH?' + idn

sel['objeto'] = sel.apply(canon, axis=1)
dup = sel.groupby('objeto').size()
print('\nObjetos con >1 fila (mismo objeto, dos nombres):')
mult = dup[dup > 1]
for ob in mult.index:
    rows = sel[sel['objeto'] == ob][['kfg', 'okr', 'procedencia', 'museo']]
    print(ob)
    print(rows.to_string(index=False))

sel.to_csv(os.path.join(os.path.dirname(__file__), 'sel_ica.csv'), index=False)
print('\nGuardado sel_ica.csv con', len(sel), 'filas;', sel['objeto'].nunique(), 'objetos únicos')
print(sel['procedencia'].value_counts().to_string())
