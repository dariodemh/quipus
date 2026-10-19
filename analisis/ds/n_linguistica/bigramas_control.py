# -*- coding: utf-8 -*-
"""
Control fonotáctico: información mutua entre sílabas contiguas (dentro de
palabra) frente a un nulo que baraja el segundo miembro de cada bigrama
(preserva frecuencias de sílabas y número de bigramas).
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re, json
from collections import Counter
import numpy as np

RNG = np.random.default_rng(20261018)
VOW = set('aeiou')

def normalize(w):
    w = w.lower()
    for a, b in [('ü', 'u'), ('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u')]:
        w = w.replace(a, b)
    w = w.replace('ç', 's').replace('z', 's').replace('x', 'S')
    w = w.replace('ch', 'C').replace('ll', 'L').replace('ñ', 'N')
    w = w.replace('rr', 'r').replace('qu', 'k')
    w = re.sub(r'hu(?=[aeiou])', 'w', w)
    w = w.replace('hu', 'u')
    w = re.sub(r'gu([ao])', r'w\1', w)
    w = re.sub(r'g([ei])', r'h\1', w)
    w = re.sub(r'c([ei])', r's\1', w)
    w = w.replace('c', 'k').replace('q', 'k').replace('h', '')
    return w.replace('v', 'b')

def syllabify(w):
    if not any(c in VOW for c in w):
        return None
    n = len(w); nuclei = []; i = 0
    while i < n:
        if w[i] in VOW:
            j = i + 1
            while j < n and w[j] in VOW:
                j += 1
            nuclei.append((i, j)); i = j
        else:
            i += 1
    if not nuclei:
        return None
    syl = []; prev = 0
    for idx, (a, b) in enumerate(nuclei):
        cons = w[prev:a]
        if idx == 0:
            onset = cons
        else:
            if len(cons) >= 2 and cons[-1] in 'lr':
                onset = cons[-2:]; extra = cons[:-2]
            else:
                onset = cons[-1:] if cons else ''; extra = cons[:-1]
            if extra:
                syl[-1] += extra
        syl.append(onset + w[a:b]); prev = b
    if prev < n:
        syl[-1] += w[prev:]
    return [x for x in syl if x]

def load(path):
    s = open(path, encoding='utf-8').read()
    s = s.replace('\u25a0', 'ñ').replace('\ufffd', 'ñ')
    s = re.sub(r'/\s*f\.?\s*\d+[rv]?\s*/', ' ', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    return [t for t in re.findall(r'[a-záéíóúñüç]+', s.lower()) if len(t) >= 2]

def pairs(path):
    A, B = [], []
    for t in load(path):
        s = syllabify(normalize(t))
        if s and len(s) > 1:
            for a, b in zip(s, s[1:]):
                A.append(a); B.append(b)
    return np.array(A), np.array(B)

def mi(A, B):
    ua = Counter(A); ub = Counter(B); n = len(A)
    pa = {k: v / n for k, v in ua.items()}
    pb = {k: v / n for k, v in ub.items()}
    bi = Counter(zip(A, B))
    return float(sum(c / n * np.log2((c / n) / (pa[a] * pb[b])) for (a, b), c in bi.items()))

res = {}
for name, path in [('quechua', 'corpus/huarochiri_quechua.txt'),
                   ('espanol', 'corpus/huarochiri_espanol_descartado.txt')]:
    A, B = pairs(path)
    obs = mi(A, B)
    null = np.array([mi(A, RNG.permutation(B)) for _ in range(300)])
    p = (1 + np.sum(null >= obs)) / (1 + len(null))
    alls = list(A) + list(B)
    tc = Counter(''.join('V' if c in VOW else 'C' for c in x) for x in alls)
    tot = sum(tc.values())
    res[name] = dict(bigramas=int(len(A)), tipos_bigrama=int(len(set(zip(A, B)))),
                     MI_bits=obs, MI_null=float(null.mean()),
                     MI_null_sd=float(null.std()), p_perm=float(p),
                     tipos_silabicos_pct={k: round(100 * v / tot, 2) for k, v in tc.most_common()})
    print(name, res[name])

with open('bigramas_control.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
