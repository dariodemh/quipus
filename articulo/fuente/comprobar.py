"""Comprueba que lo que el texto dice de cada figura coincida con los datos que la figura dibuja (datos.json).
Uso: python articulo/fuente/comprobar.py      Falla con AssertionError si algo no cuadra."""
import json, os, re
from statistics import mean

S = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(f'{S}/datos.json', encoding='utf-8'))
ES = open(f'{S}/plantilla.html', encoding='utf-8').read()
EN = open(f'{S}/plantilla.en.html', encoding='utf-8').read()
fallos = []

def dice(es, en=None):
    """El texto en español (y en inglés, si se da) contiene la frase."""
    ok = es in ES and (en is None or en in EN)
    if not ok:
        fallos.append(f'el texto ya no dice: {es!r}' + (f' / {en!r}' if en and en not in EN else ''))
    return ok

def igual(nombre, real, texto):
    if real != texto:
        fallos.append(f'{nombre}: los datos dan {real}, el texto dice {texto}')

# figura 1: la primera cuerda de UR278
igual('fig 1, valor de la cuerda', sum(k[3] for k in D['ej415']['k']), 415)
dice('Suma 415.', 'adds up to 415.') if 'adds up to 415' in EN else dice('Suma 415.')

# hallazgo 1 / figura 6: grupos de UR270 con >= 6 de 9 celdas y el ejemplo del grupo 0
igual('fig 6, grupos con >=6/9', sum(1 for g in D['ur270'] if (g['exactas'] or 0) >= 6), 5)
g0 = next(g for g in D['ur270'] if g['g'] == 0)
igual('fig 6, grupo 0: exactas', g0['exactas'], 8)
dice('Coinciden ocho de nueve')

# figura 7 y hallazgo 4: totales de fila y destinos en el libro
tot = D['totales']
destino = lambda t, q: re.search(q + r' g(\d+)=(\d+)(?: \(([+-]\d+)\))?', t['enlace'])
d66 = [destino(t, 'UR266') for t in tot]
con = [m for m in d66 if m]
igual('fig 7, filas', len(tot), 26)
igual('fig 7, filas con destino', len(con), 18)
igual('fig 7, exactas en UR266', sum(1 for m in con if not m.group(3)), 11)
igual('fig 7, exactas en UR275', sum(1 for t in tot if (m := destino(t, 'UR275')) and not m.group(3)), 7)
igual('hallazgo 4, diferencias', [int(m.group(3)) for m in con if m.group(3)], [6, 100, 1, -1, 1, -1, -1])
dice('las 26 filas de UR278')
dice('de las 18 filas que tienen destino, 11 coinciden exactamente y 7 no')
dice('+6 · +100 · +1 · −1 · +1 · −1 · −1')

# figura 8 y hallazgo 2: UR273A + UR273B
igual('fig 8, registros', len(D['ab']), 18)
igual('fig 8, sumas en el libro', sum(r['hit'] for r in D['ab']), 8)
dice('ocho de dieciocho sumas')

# figura 9 y hallazgo 3: perfil de columnas
cols = [mean(f[j] for f in D['perfil']['filas']) for j in range(9)]
orden = sorted(range(9), key=lambda j: -cols[j])
if set(orden[:2]) != {0, 1} or set(orden[-2:]) != {7, 8}:
    fallos.append(f'fig 9: las dos primeras columnas no son las mayores o las dos últimas no son las menores: {[round(c) for c in cols]}')
dice('con las dos primeras como las mayores y las dos últimas como las menores')

# figura 10: la cuerda 180
igual('fig 10, valor transcrito', sum(k[3] for k in D['p180']['k']), 238)
dice('y suma 238')

# figura 12: red de copias
dice('algunos pares más que los 25 del primer análisis')
if len(D['copias']) <= 25:
    fallos.append(f'fig 12: el pie dice que hay más de 25 pares y hay {len(D["copias"])}')
entre = [c for c in D['copias'] if c['nivel'].startswith('bien apoyado') and c['ma'] != c['mb'] and 'desconocido' not in (c['ma'], c['mb'])]
if entre:
    fallos.append(f'fig 12: pares entre museos marcados bien apoyados, pero el texto dice apoyado: {[(c["a"], c["b"]) for c in entre]}')

# figura 14 y hallazgo 7: KH0049 en bloques de 18
B = D['kh0049']
igual('fig 14, bloques', (len(B), {len(b) for b in B}), (6, {18}))
igual('hallazgo 7, B0 = B1 + B2', sum(B[0][i] == B[1][i] + B[2][i] for i in range(18)), 14)
igual('hallazgo 7, B1 = B3 + B4 + B5', sum(B[1][i] == B[3][i] + B[4][i] + B[5][i] for i in range(18)), 7)
dice('Un bloque es la suma de otros dos en 14 de 18 posiciones')

# figura 15 y hallazgo 8: UR040
igual('fig 15, cuerdas de UR040', len(D['ur040']), 33)
dice('Las 33 cuerdas colgantes de UR040')

# figura 16: UR1107 y UR237
v = D['ur1107']
num = lambda x: x is not None and x == x
igual('fig 16, valores iguales', sum(1 for r in v if num(r['va']) and r['va'] == r['vb']), 23)
igual('fig 16, cuerdas', len(v), 26)
igual('fig 16, etiquetas de color iguales', sum(1 for r in v if r['a'] == r['b']), 0)
dice('Los valores coinciden en 23 de las 26 cuerdas con nudos')

# figura 19 y hallazgo 12: el atlas
igual('fig 19, cuadros', len(D['atlas']), 651)
dice('Los 651 quipus del corpus, uno por cuadrito')

# figura 21: el cero
k = D['cero']['k']
igual('fig 21, valor', D['cero']['v'], 1202)
igual('fig 21, cm entre millar y centena', k[1][2] - k[0][2], 7)
igual('fig 21, cm de centena a unidades', k[2][2] - k[1][2], 14)
dice('Entre el millar y la centena hay 7 cm; entre la centena y las unidades, donde falta la decena, hay 14.')

# figuras con cifras escritas en figuras.js: se cotejan con su fuente
JS = open(f'{S}/figuras.js', encoding='utf-8').read()
for cifras, fuente in [
        ("['UR053A', .70, .17, .13], ['UR053B', .57, .26, .17], ['UR053C', .61, .23, .16], ['UR053D', .66, .16, .18], ['UR053E', .64, .18, .18]",
         'fig 18: repartos de SINTESIS.md (UR053A–E)'),
        ("8031, 7892, 8167", 'fig 20: M0, media y rango del 95 % de nulos_corpus.npz'),
        ("7913, 7790, 8036", 'fig 20: M1'), ("8094, 7975, 8209", 'fig 20: M2'),
        ("const mal = new Set([3, 11, 17, 22, 30, 36, 41, 47, 52, 58, 61, 66]);", 'fig 3: 12 fallos de 68')]:
    if cifras not in JS:
        fallos.append(f'{fuente}: figuras.js ya no tiene {cifras!r}')

# las dos versiones tienen las mismas fichas del lector
igual('fig 22, líneas de fichas es/en', [len(x) for x in D['fichas'].values()], [len(x) for x in D['fichas_en'].values()])

if fallos:
    raise AssertionError('\n' + '\n'.join(fallos))
print('todo cuadra')
