# -*- coding: utf-8 -*-
"""Consulta la base OKR (khipu.db) para KH0083. Salida acotada."""
import sqlite3, os

DB = os.path.join('data', 'external', 'open-khipu-repository', 'data', 'khipu.db')
con = sqlite3.connect(DB)
cur = con.cursor()

print('== tablas ==')
for (n,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(n)

print('\n== khipu_main cols ==')
print([d[1] for d in cur.execute('PRAGMA table_info(khipu_main)')])
print('\n== cord cols ==')
print([d[1] for d in cur.execute('PRAGMA table_info(cord)')])
print('\n== knot cols ==')
print([d[1] for d in cur.execute('PRAGMA table_info(knot)')])
print('\n== knot_cluster cols ==')
print([d[1] for d in cur.execute('PRAGMA table_info(knot_cluster)')])

# find KH0083
print('\n== khipu_main KH0083 ==')
cols = [d[1] for d in cur.execute('PRAGMA table_info(khipu_main)')]
q = 'SELECT * FROM khipu_main WHERE ' + ' OR '.join([f'"{c}" LIKE ?' for c in cols])
rows = list(cur.execute(q, ['%KH0083%'] * len(cols)))
print('filas:', len(rows))
for r in rows[:5]:
    for c, v in zip(cols, r):
        if v not in (None, '', 0):
            print(f'  {c} = {v}')
    print('  ---')
con.close()
