# -*- coding: utf-8 -*-
"""
Aproximación al inventario y frecuencias silábicas del aimara moderno
(corpus de Wikipedia aimara ya presente en el repo), como comparación con el
quechua de Huarochirí. No es texto colonial: sirve sólo de control tipológico.
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re, json
from collections import Counter
import numpy as np

SRC = '../n_descifrado_lm/corpus/aymara.txt'
VOW = set('aeiou')
text = open(SRC, encoding='utf-8', errors='ignore').read()[:300000]
text = text.lower().replace('’', '').replace("'", '')

def norm(w):
    for a, b in [('chh', 'C'), ('ch', 'C'), ('ll', 'L'), ('ñ', 'N'),
                 ('qh', 'Q'), ('kh', 'K'), ('ph', 'P'), ('th', 'T')]:
        w = w.replace(a, b)
    return w

def syll(w):
    if not any(c in VOW for c in w):
        return None
    n = len(w); nu = []; i = 0
    while i < n:
        if w[i] in VOW:
            j = i + 1
            while j < n and w[j] in VOW:
                j += 1
            nu.append((i, j)); i = j
        else:
            i += 1
    if not nu:
        return None
    sy = []; prev = 0
    for k, (a, b) in enumerate(nu):
        cons = w[prev:a]
        if k == 0:
            on = cons
        else:
            if len(cons) >= 2 and cons[-1] in 'lr':
                on = cons[-2:]; ex = cons[:-2]
            else:
                on = cons[-1:] if cons else ''; ex = cons[:-1]
            if ex:
                sy[-1] += ex
        sy.append(on + w[a:b]); prev = b
    if prev < n:
        sy[-1] += w[prev:]
    return [x for x in sy if x]

tok = [t for t in re.findall(r'[a-zñü]+', text) if len(t) >= 2]
sy = []
for t in tok:
    s = syll(norm(t))
    if s:
        sy.extend(s)
c = Counter(sy)
p = np.array(list(c.values())) / len(sy)
H = float(-(p * np.log2(p)).sum())
tc = Counter(''.join('V' if x in VOW else 'C' for x in s) for s in sy)
tot = sum(tc.values())
print('tokens', len(tok), 'silabas', len(sy), 'tipos', len(c), 'H', round(H, 3))
print('top', c.most_common(20))
print('tipos', [(k, round(100*v/tot, 1)) for k, v in tc.most_common(6)])
json.dump(dict(tokens=len(tok), silabas=len(sy), tipos=len(c), entropia_bits=H,
               top=c.most_common(25),
               tipos_silabicos=[(k, round(100*v/tot, 2)) for k, v in tc.most_common()]),
          open('silabas_aymara.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
