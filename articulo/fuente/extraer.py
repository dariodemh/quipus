"""Extrae de los datos del repo quipus lo que necesitan las figuras del artículo. Salida: datos.json"""
import json, re, sys, os
import pandas as pd

R = sys.argv[1]            # raíz del repo quipus
OUT = sys.argv[2]
SCR = os.path.dirname(os.path.abspath(OUT))
d = pd.read_csv(f'{R}/analisis/datos/cuerdas.csv', low_memory=False)
d['color'] = d['color'].fillna('').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s))
Q = lambda k: d[d.kfg == k]
D = {}

def knots(s):
    """'4S(4.5,Z),400;...' -> [[n, tipo, pos_cm, valor], ...]"""
    out = []
    if not isinstance(s, str): return out
    for m in re.finditer(r'(\d+)([SLE])\(([\d.]+|nan)?,?([SZU]?)\),(\d+)', s):
        n, t, pos, _, v = m.groups()
        out.append([int(n), t, float(pos) if pos and pos != 'nan' else None, int(v)])
    return out

def cord(r):
    return dict(c=r.cuerda, v=None if pd.isna(r.valor) else int(r.valor), col=r.color, k=knots(r.nudos),
                l=None if pd.isna(r.largo) else float(r.largo))

# --- cuerda de ejemplo y p180
w = Q('UR278')
D['ej415'] = cord(w[w.cuerda == 'p1'].iloc[0])
D['p180'] = cord(w[w.cuerda == 'p180'].iloc[0])

# --- UR278: filas de 9
filas = []
for g, x in w[w.nivel == 0].groupby('grupo'):
    if len(x) != 9: continue
    filas.append(dict(g=int(g), cel=[cord(r) for r in x.itertuples()]))
D['ur278'] = filas

# --- UR270: P y S1 por grupo de 9; emparejar con UR278
u = Q('UR270')
grupos = []
for g, x in u[u.nivel == 0].groupby('grupo'):
    if len(x) != 9: continue
    cel = []
    for r in x.itertuples():
        s = u[(u.padre == r.cuerda) & (u.nivel == 1)]
        s1 = s.iloc[0] if len(s) else None
        cel.append(dict(P=cord(r), S=cord(s1) if s1 is not None else None))
    suma = [(c['P']['v'] or 0) + ((c['S'] or {}).get('v') or 0) for c in cel]
    best, bg = -1, None
    for f in filas:
        vals = [c['v'] for c in f['cel']]
        n = sum(a == b for a, b in zip(suma, vals))
        if n > best: best, bg = n, f['g']
    grupos.append(dict(g=int(g), cel=cel, suma=suma, destino=bg if best >= 6 else None, exactas=best))
D['ur270'] = grupos

# --- totales de fila de UR278 y destino en el libro (tabla traducida)
t = pd.read_csv(f'{R}/analisis/29_lectura_incahuasi/tabla_traducida.csv')
tot = t[(t.quipu == 'UR278') & t.rol.str.contains('total del registro')]
D['totales'] = [dict(g=int(r.grupo), v=int(r.valor), enlace=r.enlace) for r in tot.itertuples()]

# --- UR273A + UR273B por número de grupo
# la prueba original (13_sistema_incahuasi/04_componentes.py) compara 18 registros; en g6 la primera cuerda de UR273A
# es la cuota fija de 30, que 29_lectura ya no llama cabecera, pero el registro entra en la cuenta de 8/18
cab = t[t.quipu.isin(['UR273A', 'UR273B']) & t.rol.str.contains('cabecera del componente|cuota fija del componente')]
A = cab[cab.quipu == 'UR273A'].groupby('grupo').valor.first()
B = cab[cab.quipu == 'UR273B'].groupby('grupo').valor.first()
ocho = {2950, 1653, 1737, 1827, 1780, 2247, 1765, 1506}
D['ab'] = [dict(g=int(g), a=int(A[g]), b=int(B[g]), s=int(A[g] + B[g]), hit=int(A[g] + B[g]) in ocho)
           for g in sorted(set(A.index) & set(B.index))]
assert len(D['ab']) == 18 and sum(r['hit'] for r in D['ab']) == 8, D['ab']

# --- perfil de columnas
comp = [[c['v'] for c in f['cel']] for f in filas if all(c['v'] for c in f['cel'])]
D['perfil'] = dict(filas=comp, bambamarca=[104, 75, 78, 68, 49, 75, 67, 30, 27])

# --- KH0049 y UR122 en bloques de 18
def bloques(k):
    v = [None if pd.isna(x) else int(x) for x in Q(k)[Q(k).nivel == 0].valor]
    return [v[i:i + 18] for i in range(0, len(v), 18)]
D['kh0049'] = bloques('KH0049'); D['ur122'] = bloques('UR122')

# --- UR040
x = Q('UR040'); D['ur040'] = [dict(col=r.color, v=None if pd.isna(r.valor) else int(r.valor)) for r in x[x.nivel == 0].itertuples()]

# --- UR1107 / UR237: mismas cuerdas, etiquetas de color
v = pd.read_csv(f'{R}/analisis/14_copias/verificacion_UR1107_UR237.csv')
D['ur1107'] = [dict(a=r.color_A, b=r.color_B, va=r.valor_A, vb=r.valor_B) for r in v.itertuples()]

# --- un cero real: MM018 p29 = 1202 (millar, centena, hueco, unidades)
r = Q('MM018'); D['cero'] = dict(kfg='MM018', **cord(r[r.cuerda == 'p29'].iloc[0]))

# --- red de copias
p = pd.read_csv(f'{R}/analisis/33_estematica/pares_copia.csv')
p = p[p.nivel.str.match(r'^(bien apoyado|apoyado|propuesto)')]
D['copias'] = [dict(a=r.kfg_a, b=r.kfg_b, ma=r.museo_A, mb=r.museo_B, pa=r.procedencia_A, pb=r.procedencia_B,
                    ex=int(r.exactas), al=int(r.alineadas), nivel=r.nivel) for r in p.itertuples()]

# --- atlas
a = pd.read_csv(f'{R}/analisis/28_atlas_generos/atlas.csv')
e = pd.read_csv(f'{R}/analisis/28_atlas_generos/enmiendas.csv')
gen = dict(zip(a.kfg, zip(a.genero, a.confianza)))
for r in e.itertuples(): gen[r.kfg] = (r.genero_nuevo, r.confianza)
D['atlas'] = [dict(k=k, g=g, c=c, p=str(pr)) for (k, (g, c)), pr in zip(gen.items(), a.procedencia)]

# --- fichas del lector (líneas con etiqueta, por sección); las .en.txt son traducciones a mano de la salida del lector
for clave, suf in [('fichas', ''), ('fichas_en', '.en')]:
    fich = {}
    for k in ['UR278', 'KH0049', 'UR040', 'UR1104']:
        sec, out = None, []
        for line in open(f'{SCR}/ficha_{k}{suf}.txt', encoding='utf-8'):
            if line.startswith('## '): sec = line[3:].strip()
            m = re.match(r'- \[([A-ZÁ ]+)\] (.*?)\s*$', line)
            if m and sec: out.append([sec, m.group(1), m.group(2)])
        fich[k] = out
    D[clave] = fich
assert [len(v) for v in D['fichas'].values()] == [len(v) for v in D['fichas_en'].values()], 'las fichas .en no cuadran con las originales'

# --- mapa
# --- mapa: Natural Earth 1:50m (dominio público), vía el paquete world-atlas 2.0.2 (TopoJSON)
topo = json.load(open(f'{SCR}/descargas/countries-50m.json'))
(sx, sy), (tx0, ty0) = topo['transform']['scale'], topo['transform']['translate']
def arco(i):
    pts, x, y = [], 0, 0
    for dx, dy in topo['arcs'][i if i >= 0 else ~i]:
        x, y = x + dx, y + dy
        pts.append((x * sx + tx0, y * sy + ty0))
    return pts if i >= 0 else pts[::-1]
def anillo(idx, caja=(-86, -62, -23, 4)):
    """une los arcos y recorta a la caja (las partes de fuera quedan pegadas al borde, fuera de la vista)"""
    out = []
    for i in idx:
        out += arco(i)[1 if out else 0:]
    if not any(caja[0] < x < caja[1] and caja[2] < y < caja[3] for x, y in out):
        return []
    out = [(round(min(max(x, caja[0]), caja[1]), 2), round(min(max(y, caja[2]), caja[3]), 2)) for x, y in out]
    # ponytail: decimación simple (salta puntos a menos de 0,06° del anterior); basta a la escala del mapa
    keep = [out[0]]
    for x, y in out[1:]:
        if abs(x - keep[-1][0]) + abs(y - keep[-1][1]) > .06:
            keep.append((x, y))
    return [list(p) for p in keep]
paises = {}
for geo in topo['objects']['countries']['geometries']:
    nombre = geo['properties']['name']
    if nombre in ('Peru', 'Ecuador', 'Colombia', 'Brazil', 'Bolivia', 'Chile'):
        polis = geo['arcs'] if geo['type'] == 'MultiPolygon' else [geo['arcs']]
        paises[nombre] = [a for a in (anillo(p[0]) for p in polis) if len(a) > 3]
D['peru'] = paises.pop('Peru')
D['vecinos'] = [a for v in paises.values() for a in v]

json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print({k: (len(v) if hasattr(v, '__len__') else v) for k, v in D.items()})
print('cero', D.get('cero')); print('ur270 destinos', [(x['g'], x['destino'], x['exactas']) for x in grupos])
print('ab', D['ab']); print('copias', len(D['copias']))
