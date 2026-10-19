"""¿Los desajustes UR278 -> libro (UR266/UR275) son convención o error? Usa los enlaces de 29_lectura_incahuasi.
Uso: python analisis/34_comparada/desajustes.py (desde la raíz)."""
import csv, re
from math import comb
filas = [r for r in csv.DictReader(open('analisis/29_lectura_incahuasi/tabla_traducida.csv', encoding='utf-8'))
         if r['quipu'] == 'UR278' and r['cuerda'] == 'Σ fila']
sin = [r['grupo'] for r in filas if 'sin destino' in r['enlace']]
exactas, difs = [], []
for r in filas:
    if 'sin destino' in r['enlace']: continue
    m = re.search(r'UR266 g\d+=(\d+)', r['enlace'])
    d = int(m.group(1)) - int(r['valor'])  # libro - detalle
    (exactas if d == 0 else difs).append((r['grupo'], d))
print('filas', len(filas), '| sin destino', len(sin), '| con destino', len(exactas) + len(difs), '| exactas', len(exactas))
print('desajustes (libro - detalle):', difs)
pos = sum(d > 0 for _, d in difs); n = len(difs)
p_signo = min(1, 2 * sum(comb(n, k) for k in range(max(pos, n - pos), n + 1)) / 2 ** n)
uni = sum(abs(d) < 10 for _, d in difs)
p_uni = sum(comb(n, k) * (1/3)**k * (2/3)**(n-k) for k in range(uni, n + 1))  # nulo: error igual de probable en unidades, decenas o centenas
print(f'signo: {pos}+ / {n-pos}-  p={p_signo:.2f} | en unidades: {uni}/{n}  p(nulo 1/3)={p_uni:.4f}')
assert len(exactas) == 11 and n == 7
