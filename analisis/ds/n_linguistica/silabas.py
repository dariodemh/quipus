# -*- coding: utf-8 -*-
"""
Fonología y sílabas del quechua del Manuscrito de Huarochirí (ca. 1608).

- normaliza la ortografía colonial a una representación fonológica aproximada
- silabifica (onset máximo; estructuras V, CV, CVC, CCV...)
- frecuencias de sílabas y de bigramas silábicos
- inventario y curva de rarefacción
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re, json
from collections import Counter
import numpy as np

SRC = 'corpus/huarochiri_quechua.txt'
OUT = 'silabas_huarochiri.json'
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
    w = w.replace('v', 'b')
    return w

def is_v(c):
    return c in VOW

def syllabify(w):
    """onset máximo; devuelve lista de sílabas o None si no hay vocal."""
    if not any(is_v(c) for c in w):
        return None
    n = len(w)
    nuclei = []
    i = 0
    while i < n:
        if is_v(w[i]):
            j = i + 1
            while j < n and is_v(w[j]):
                j += 1
            nuclei.append((i, j))
            i = j
        else:
            i += 1
    if not nuclei:
        return None
    syl = []
    prev_end = 0
    for idx, (a, b) in enumerate(nuclei):
        cons = w[prev_end:a]
        if idx == 0:
            onset = cons
        else:
            if len(cons) >= 2 and cons[-1] in 'lr' and cons[-2] not in VOW:
                onset = cons[-2:]
                extra = cons[:-2]
            else:
                onset = cons[-1:] if cons else ''
                extra = cons[:-1]
            if extra:
                syl[-1] += extra
        syl.append(onset + w[a:b])
        prev_end = b
    if prev_end < n:
        syl[-1] += w[prev_end:]
    return [s for s in syl if s]

def is_v(c):
    return c in VOW

# --- lectura y limpieza -------------------------------------------------------
raw = open(SRC, encoding='utf-8').read()
raw = raw.replace('\u25a0', 'ñ').replace('\ufffd', 'ñ')
raw = re.sub(r'/\s*f\.?\s*\d+[rv]?\s*/', ' ', raw)
raw = re.sub(r'^\s*(CAPITULO|Cap[ií]tulo|CAP\.).*$', '', raw, flags=re.M)
raw = re.sub(r'^\s*\d{1,3}\s*$', '', raw, flags=re.M)
raw = re.sub(r'-\s*\n\s*', '', raw)
tokens = re.findall(r'[a-záéíóúñüç]+', raw.lower())
tokens = [t for t in tokens if len(t) >= 2]

syls, words, bad = [], [], 0
for t in tokens:
    w = normalize(t)
    s = syllabify(w)
    if not s:
        bad += 1
        continue
    words.append(w)
    syls.extend(s)

cnt = Counter(syls)
print('tokens', len(tokens), 'palabras usables', len(words), 'sílabas', len(syls),
      'tipos', len(cnt), 'descartadas', bad)
print('top sílabas:', cnt.most_common(25))

big = Counter()
for t in tokens:
    s = syllabify(normalize(t))
    if s and len(s) > 1:
        for a, b in zip(s, s[1:]):
            big[(a, b)] += 1
print('top bigramas:', big.most_common(20))

def stype(s):
    return ''.join('V' if is_v(c) else 'C' for c in s)

tc = Counter(stype(s) for s in syls)
tot = sum(tc.values())
print('tipos silábicos:', [(k, v, round(100*v/tot, 2)) for k, v in tc.most_common(12)])

p = np.array(list(cnt.values())) / len(syls)
H = float(-(p * np.log2(p)).sum())
print('entropía sílabas (bits)', round(H, 3))
curve = []
seen = set(); k = 0
for s in syls:
    seen.add(s); k += 1
    if k in (500, 1000, 2000, 5000, 10000, 20000, 40000, 60000, 80000):
        curve.append((k, len(seen)))
print('rarefacción', curve)

cov = {}
acc = 0
for i, (k, v) in enumerate(cnt.most_common(), 1):
    acc += v
    for q in (0.90, 0.95, 0.99):
        if q not in cov and acc / len(syls) >= q:
            cov[q] = i
cv = Counter(x for x in syls if stype(x) == 'CV')
cvcov = {}
acc = 0
for i, (k, v) in enumerate(cv.most_common(), 1):
    acc += v
    for q in (0.90, 0.95, 0.99):
        if q not in cvcov and acc / sum(cv.values()) >= q:
            cvcov[q] = i
res = dict(tokens=len(tokens), palabras=len(words), silabas=len(syls), cobertura=cov,
           cv_tipos=len(cv), cv_cobertura=cvcov,
           tipos_silaba=len(cnt), entropia_bits=H,
           top_silabas=cnt.most_common(40),
           top_bigramas=[[a, b, n] for (a, b), n in big.most_common(30)],
           tipos_silabicos=[(k, v, round(100*v/tot, 2)) for k, v in tc.most_common()],
           rarefaccion=curve, inventario=sorted(cnt))
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print('guardado', OUT)

esp = open('corpus/huarochiri_espanol_descartado.txt', encoding='utf-8').read()
esp = esp.replace('\u25a0', 'ñ').replace('\ufffd', 'ñ')
et = [t for t in re.findall(r'[a-záéíóúñüç]+', esp.lower()) if len(t) >= 2]
esyl = []
for t in et:
    s = syllabify(normalize(t))
    if s: esyl.extend(s)
ec = Counter(esyl)
ep = np.array(list(ec.values())) / len(esyl)
He = float(-(ep * np.log2(ep)).sum())
print('CONTROL castellano: sílabas', len(esyl), 'tipos', len(ec),
      'entropía', round(He, 3), 'top', ec.most_common(10))
res['control_espanol'] = dict(silabas=len(esyl), tipos=len(ec),
                              entropia_bits=He, top=ec.most_common(15))
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
