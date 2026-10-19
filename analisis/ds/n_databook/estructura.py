#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrae el numero esperado de colgantes/tops de la descripcion del cordon principal."""
import re, glob, os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '..', '..', 'fuentes_txt', 'databook')

def expected(path):
    txt = open(path, encoding='utf8', errors='replace').read()
    head = re.split(r'Cord\s+Knots', txt)[0]
    n = 0
    found = False
    for line in head.splitlines():
        mg = re.search(r'(\d+)\s+groups? of (\d+) (?:pendant )?cords?', line)
        if mg:
            n += int(mg.group(1)) * int(mg.group(2)); found = True
            continue
        for m in re.finditer(r'group of (\d+) (?:pendant )?cords?', line):
            n += int(m.group(1)); found = True
        singles = re.findall(r'(?<!top )pendant cord \((\d+)\)', line)
        n += len(singles)
        if singles:
            found = True
    tops = len(re.findall(r'top cord', head))
    return (n if found else None), tops

rows = []
for f in sorted(glob.glob(os.path.join(SRC, 'as[0-9]*.txt'))):
    q = 'AS%03d' % int(re.search(r'as(\d+)\.txt', f).group(1))
    n, tops = expected(f)
    rows.append(dict(quipu=q, n_pendientes_desc=n, n_tops_desc=tops))
pd.DataFrame(rows).to_csv(os.path.join(BASE, 'databook_estructura.csv'), index=False)
print(pd.DataFrame(rows).head())
print('sin descripcion:', sum(1 for r in rows if r['n_pendientes_desc'] is None))
