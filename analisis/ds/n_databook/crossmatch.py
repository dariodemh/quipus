#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cruce Databook (parser) vs KFG cuerdas.csv por alineacion de secuencia completa.
Escribe databook_vs_kfg.csv y resumen por quipu.
"""
import re, os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

db = pd.read_csv(D('databook_rows.csv'))
kf = pd.read_csv(D('..', '..', 'datos', 'cuerdas.csv'))
est = pd.read_csv(D('databook_estructura.csv'))

kf['quipu'] = kf.kfg

VOCAB = set()
def _vocab():
    global VOCAB
    if not VOCAB:
        for col in ('color',):
            for v in kf[col].dropna().astype(str):
                for p in re.split(r'[:/\-]', re.sub(r'\([^)]*\)', '', v)):
                    if p.strip(): VOCAB.add(p.strip())
    return VOCAB

def cset(c):
    if pd.isna(c): return frozenset()
    c = str(c).upper().strip()
    if c in ('BLUE', 'BIUE', 'BLU'): return frozenset(['BLUE'])
    if c in ('RED',): return frozenset(['RED'])
    c = re.sub(r'\([^)]*\)', '', c).replace('*', ':').replace(' ', '')
    c = re.sub(r'(?<=[A-Z])0', 'O', c)
    c = re.sub(r'0(?=[A-Z])', 'O', c)
    out = set()
    V = _vocab()
    for p in re.split(r'[:\-/]', c):
        p = p.strip(' .')
        if not p: continue
        if len(p) >= 3 and len(set(p)) == 1:
            p = p[0]
        if p not in V and p[::-1] in V and len(p) == 2:
            p = p[::-1]
        out.add(p)
    return frozenset(out)

db['_cs'] = db.color.apply(cset)
kf['_cs'] = kf.color.apply(cset)
db['nivel'] = db.cord_databook.str.count('s')
db['lab_num'] = db.label_ocr.astype(str).str.extract(r'^(\d{1,3})')[0]
db['lab_num'] = pd.to_numeric(db.lab_num, errors='coerce')
kf['nivel'] = kf.cuerda.str.count('s')
kf['lab_num'] = pd.to_numeric(kf.cuerda.str.extract(r'p(\d+)')[0], errors='coerce')

def score(a, b):
    s = 0.0
    va, vb = a['valor'], b['valor']
    d = abs(float(va) - float(vb))
    if d == 0: s += 1.5
    elif d <= 1: s += 1.0
    elif d <= 9: s += 0.3
    la, lb = a['largo'], b['largo']
    dl = abs(float(la) - float(lb))
    if dl <= 0.11: s += 1.5
    elif dl <= 0.6: s += 1.0
    elif dl <= 1.6: s += 0.5
    ca, cb = a['_cs'], b['_cs']
    if ca and cb:
        if ca == cb: s += 1.0
        elif ca & cb: s += 0.5
    if int(a['nivel']) == int(b['nivel']): s += 0.6
    else: s -= 0.8
    if int(a['nivel']) == 0 and pd.notna(a.get('lab_num')) and pd.notna(b.get('lab_num')):
        if int(a['lab_num']) == int(b['lab_num']): s += 0.8
    return s

def align(A, B):
    n, m = len(A), len(B)
    GAP = -0.9
    NEG = -99
    S = np.full((n + 1, m + 1), NEG)
    P = np.zeros((n + 1, m + 1), dtype=np.int8)
    S[0, 0] = 0
    for i in range(1, n + 1):
        S[i, 0] = S[i-1, 0] + GAP; P[i, 0] = 1
    for j in range(1, m + 1):
        S[0, j] = S[0, j-1] + GAP; P[0, j] = 2
    for i in range(1, n + 1):
        ai = A[i-1]
        for j in range(1, m + 1):
            sc = score(ai, B[j-1])
            diag = S[i-1, j-1] + (sc if sc > 0 else sc - 2.5)
            up = S[i-1, j] + GAP
            left = S[i, j-1] + GAP
            best, p = diag, 0
            if up > best: best, p = up, 1
            if left > best: best, p = left, 2
            S[i, j] = best; P[i, j] = p
    i, j = n, m
    pairs = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and P[i, j] == 0:
            pairs.append((i-1, j-1)); i -= 1; j -= 1
        elif i > 0 and (j == 0 or P[i, j] == 1):
            i -= 1
        else:
            j -= 1
    return pairs[::-1]

rows = []
for q in sorted(set(db.quipu) & set(kf.quipu)):
    A = db[db.quipu == q].reset_index()                   # orden de la tabla = orden fisico
    B = kf[kf.quipu == q].sort_values('orden').reset_index(drop=True)
    for i, j in align(A.to_dict('records'), B.to_dict('records')):
        a, b = A.iloc[i], B.iloc[j]
        sc = score(a, b)
        if sc < 1.2:
            continue
        rows.append(dict(quipu=q, db_row=int(a['index']), cord_db=a.cord_databook, cord_kfg=b.cuerda,
                         nivel_db=a.nivel, nivel_kfg=b.nivel,
                         valor_db=a.valor, valor_kfg=b.valor,
                         largo_db=a.largo, largo_kfg=b.largo, valor_knots=a.valor_knots, knots_ambiguo=a.knots_ambiguo, knots_norm=a.knots_norm,
                         valor_dudoso=bool(a.valor_dudoso),
                         color_db=a.color, color_kfg=b.color,
                         color_db_n=':'.join(sorted(a['_cs'])),
                         color_kfg_n=':'.join(sorted(b['_cs'])),
                         score=round(sc, 2)))
res = pd.DataFrame(rows)
res.to_csv(D('databook_vs_kfg.csv'), index=False)
print('pares', len(res), 'quipus', res.quipu.nunique())
print('mismo nivel', (res.nivel_db == res.nivel_kfg).mean().round(3))
m = res[res.nivel_db == res.nivel_kfg]
print('valor igual', (m.valor_db == m.valor_kfg).mean().round(3))
print('largo<=0.5', (abs(m.largo_db - m.largo_kfg) <= 0.5).mean().round(3))
print('color igual', (m.color_db_n == m.color_kfg_n).mean().round(3))
print(res.score.describe().round(2).to_dict())
