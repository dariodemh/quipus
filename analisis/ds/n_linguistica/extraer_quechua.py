# -*- coding: utf-8 -*-
"""
Extrae el texto QUEchua del Manuscrito de Huarochirí (ed. bilingüe Arguedas,
texto djvu de archive.org) y calcula frecuencias de sílabas y bigramas.

Método: clasificador de n-gramas de caracteres (Naive Bayes) entrenado con
líneas de alta confianza; se conserva sólo el bloque quechua (líneas 539-7985
del texto, que excluye el aparato crítico final).
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re, json
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

RAW = 'corpus/arguedas_raw.txt'
OUT = 'corpus/huarochiri_quechua.txt'
OUT2 = 'corpus/huarochiri_espanol_descartado.txt'

SPANISH = set('''de la que el los las del con por para como sus fue era al se en un una su no lo le y a es son este esta estos estas pero mas muy cuando desde hasta entre sobre todo todos porque donde ya habia fueron ser estaba tiene tenia hizo dijo ante bajo contra durante mediante segun sin tras hacia asi tambien solo cada otro otra otros otras cual cuales quien quienes cuyo cuya ni o u e'''.split())

def score_es(line):
    w = re.findall(r'[a-záéíóúñü]+', line.lower())
    if len(w) < 3:
        return 0.0
    return sum(x in SPANISH for x in w) / len(w)

lines = open(RAW, encoding='utf-8').read().split('\n')
lo, hi = 539, 7986          # texto principal + suplementos; fuera el aparato final

def clean(s):
    s = re.sub(r'/\s*f\.?\s*\d+[rv]?\s*/', ' ', s)
    s = re.sub(r'^\s*\d{1,3}\s*$', '', s)
    s = s.replace('\ufffd', 'ñ')
    return s.strip()

cand = [(i, clean(l)) for i, l in enumerate(lines) if lo <= i < hi and clean(l)]

# --- entrenamiento de alta confianza ---
es_train = [s for _, s in cand if score_es(s) >= 0.30 and len(s) >= 30]
qu_train = [s for _, s in cand if score_es(s) <= 0.04 and len(s) >= 30 and
            re.search(r'[ñc]h|ñ|hu|qu|cuna|manta|pim|pas\b', s)]
print('train es', len(es_train), 'qu', len(qu_train))

X = es_train + qu_train
y = np.array([1] * len(es_train) + [0] * len(qu_train))
vec = CountVectorizer(analyzer='char', ngram_range=(2, 4), min_df=2,
                      lowercase=True, max_features=60000)
Xv = vec.fit_transform(X)
clf = MultinomialNB(alpha=0.3).fit(Xv, y)
proba = clf.predict_proba(vec.transform([s for _, s in cand]))[:, 1]

kept, dropped = [], []
for (i, s), p in zip(cand, proba):
    if p < 0.35:
        kept.append(s)
    else:
        dropped.append(s)

open(OUT, 'w', encoding='utf-8').write('\n'.join(kept))
open(OUT2, 'w', encoding='utf-8').write('\n'.join(dropped))
print('líneas quechua', len(kept), 'castellanas', len(dropped),
      'caracteres', sum(map(len, kept)))
print('--- muestra quechua ---')
print('\n'.join([x for x in kept if len(x) > 20][:12]))
print('--- muestra descartada ---')
print('\n'.join([x for x in dropped if len(x) > 20][:8]))
