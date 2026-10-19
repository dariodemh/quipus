# -*- coding: utf-8 -*-
"""Control positivo: ¿redescubre el método los pares publicados por Urton (2005)?"""
import pandas as pd, numpy as np, os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos'); HERE = os.path.dirname(__file__)
sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv')); sel['kfg'] = sel['kfg'].astype(str)
OBJ = dict(zip(sel['kfg'], sel['objeto']))
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv')); c['kfg'] = c['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy(); cc['objeto'] = cc['kfg'].map(OBJ)
def ncl(s): return 0 if pd.isna(s) or str(s).strip() in ('', 'nan') else len([x for x in str(s).split(';') if x.strip()])
cc['ncl'] = cc['nudos'].map(ncl); cc = cc.sort_values(['kfg', 'orden'])

# Mapa AS -> KH
okr = pd.read_csv(os.path.join(RAIZ, 'data', 'external', 'open-khipu-repository', 'data', 'okr-kh-numbers.csv'))
as2kh, kh2as = {}, {}
for _, r in okr.iterrows():
    kh = str(r['OKR Number']).strip()
    for nm in str(r['Other Names']).split(','):
        nm = nm.strip()
        if nm.startswith(('AS', 'HP', 'UR')):
            as2kh[nm] = kh
            if kh not in kh2as: kh2as[kh] = nm

def series_of(ob):
    kfg = sel[sel['objeto'] == ob]['kfg'].iloc[0]
    sub = cc[(cc['objeto'] == ob) & (cc['kfg'] == kfg)]
    return sub[(sub['nivel'] == 0) & (sub['ncl'] > 0)]['valor'].astype(int).tolist()

print('=== Pares publicados por Urton (2005) y su estado en nuestros datos ===')
pairs = [('AS194', 'AS195', 'near Callango, Ica'), ('AS159', 'AS173', 'between Ica and Pisco'),
         ('AS114', 'AS123', 'Ica'), ('AS116', 'AS150', 'Ica')]
for a, b, nota in pairs:
    kha, khb = as2kh.get(a), as2kh.get(b)
    print('\n%s [%s] = %s  /  %s [%s] = %s' % (a, nota, kha, b, nota, khb))
    if kha in sel['objeto'].values and khb in sel['objeto'].values:
        sa, sb = series_of(kha), series_of(khb)
        print('  %s n=%d total=%d : %s' % (kha, len(sa), sum(sa), sa[:12]))
        print('  %s n=%d total=%d : %s' % (khb, len(sb), sum(sb), sb[:12]))
        # tramo contiguo común
        A, B = sa, sb
        m = [[0]*(len(B)+1) for _ in range(len(A)+1)]; best=0; bi=0
        for i in range(1,len(A)+1):
            for j in range(1,len(B)+1):
                if A[i-1]==B[j-1]:
                    m[i][j]=m[i-1][j-1]+1
                    if m[i][j]>best: best=m[i][j]; bi=i
        print('  tramo contiguo común más largo = %d  -> %s' % (best, A[bi-best:bi]))
    else:
        print('  (algún miembro fuera del set Ica)')

print('\n=== ¿Está AS114=KH0128 y AS123=KH0137 confirmado? ===')
print('AS114 ->', as2kh.get('AS114'), '| AS123 ->', as2kh.get('AS123'),
      '| AS159 ->', as2kh.get('AS159'), '| AS173 ->', as2kh.get('AS173'))
print('KH0175 ->', kh2as.get('KH0175'), '| KH0190 ->', kh2as.get('KH0190'))
