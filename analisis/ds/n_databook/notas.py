#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrae y clasifica las Observaciones (prosa) de Ascher & Ascher 1988.
Genera notas_ascher.csv: una fila por afirmacion numerada."""
import re, os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

raw = pd.read_csv(D('databook_observaciones_raw.csv'))

ITEM = re.compile(r'^\s*[\*\(]*\s*(\d{1,2}|[lI])\s*[\.\)]\s*')
SUB = re.compile(r'^\s*[\(\[]?([a-z]|[ivx]{1,4}|\d{1,2})\)\s+', re.I)

def clean(t):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\s+([,.;:])', r'\1', t)
    return t

items = []
for q, gr in raw.groupby('quipu'):
    cur = None
    for _, r in gr.sort_values('orden').iterrows():
        t = str(r.texto).strip()
        m = ITEM.match(t)
        # evitar falsos items: "1.5 cm" o "2.0"
        if m and not re.match(r'^\s*[\*\(]*\s*\d+\s*[\.\)]\s*\d', t):
            if cur: items.append(cur)
            cur = dict(quipu=q, item=m.group(1).replace('l', '1').replace('I', '1'), texto=t[m.end():])
        else:
            if cur:
                cur['texto'] += ' ' + t
            else:
                cur = dict(quipu=q, item='', texto=t)
    if cur: items.append(cur)

df = pd.DataFrame(items)
df['texto'] = df.texto.apply(clean)
df['item'] = df['item'].astype(str)

SUM = r'\b(sum|total|totals|add|added|plus|minus|subtract|difference|product|multipl|twice|half|double|equals?|equal to|amounts? to|average)\b'
COUNT = r'\b(number of|count|cords?|pendants?|subsidiar|knots?|groups? of)\b'
NUM = r'\d'

def tipo(t):
    tl = t.lower()
    tags = []
    if re.search(SUM, tl): tags.append('relacion_aritmetica')
    if re.search(r'\b(sum of|total of|equals?|equal to|is the same|twice|half|double)\b', tl): tags.append('suma_igualdad')
    if re.search(r'\b(number of|counts?|total number)\b', tl): tags.append('conteo')
    if re.search(r'\b(color|colour|spacing|group|construction|mend|broken|missing|end knot)\b', tl): tags.append('construccion_color')
    if re.search(r'\bvalue\b', tl): tags.append('valor')
    return ','.join(tags) if tags else 'otro'

df['tipo'] = df.texto.apply(tipo)
df['item'] = df.item.astype(str)
df['tiene_numeros'] = df.texto.str.contains(NUM)
df['numeros'] = df.texto.apply(lambda t: ','.join(re.findall(r'\d+(?:\.\d+)?', t))[:80])
df.to_csv(D('notas_ascher.csv'), index=False, encoding='utf-8')

print('items', len(df), '| quipus', df.quipu.nunique())
print('con numeros', int(df.tiene_numeros.sum()), '| con relacion aritmetica',
      int(df.tipo.str.contains('relacion_aritmetica').sum()),
      '| suma/igualdad', int(df.tipo.str.contains('suma_igualdad').sum()))
print(df.tipo.value_counts().head(10).to_string())
print('\nejemplos suma/igualdad:')
print(df[df.tipo.str.contains('suma_igualdad')][['quipu', 'item', 'texto']].head(12).to_string(max_colwidth=100))
