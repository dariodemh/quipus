"""Verifica que el 'valor' escrito en la ficha coincide con la suma de los nudos transcritos.

Notacion de la ficha: '9L(7,Z)' aporta 9; '1S(3.5,Z)' aporta 1 en la posicion que le toque.
Se prueban varios modelos posicionales y se informa cual encaja con el valor escrito:
  dec   : decimal estandar descendente (n racimos -> 10^(n-1-i)); primer racimo = decenas/centenas
  dec_r : el mismo pero en orden inverso (posiciones crecientes hacia abajo)
  t+u   : primer racimo x10 (decenas), todos los demas sumados como unidades
  u     : todos los racimos sumados como unidades
  c+t+u : 3 racimos = centenas+decenas+unidades (igual que dec con n=3)
Un '?' en la celda no impide el calculo. Un solo racimo => comprobacion vacua.

Uso: python verificar.py [fichero.csv ...]   (sin argumentos: todos los transcripcion_*.csv)
"""
import csv, glob, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r'(\d+)\s*([SLEB]{1,2})\s*\(')


def clusters(nudos):
    return [int(m.group(1)) for m in PAT.finditer(nudos or '')]


def models(cs):
    n = len(cs)
    out = {}
    out['dec'] = sum(c * 10 ** (n - 1 - i) for i, c in enumerate(cs))
    out['dec_r'] = sum(c * 10 ** i for i, c in enumerate(cs))
    out['t+u'] = cs[0] * 10 + sum(cs[1:])
    out['u'] = sum(cs)
    return out


def main(files=None):
    files = files or sorted(glob.glob(os.path.join(HERE, 'transcripcion_*.csv')))
    resumen = []
    for f in files:
        rows = list(csv.DictReader(open(f, encoding='utf-8')))
        stats = {'f': os.path.basename(f), 'filas': len(rows), 'con_nudos': 0,
                 'verificables': 0, 'ok': 0, 'vacuas': 0, 'modelos': {}, 'descuadres': []}
        for r in rows:
            cs = clusters(r['nudos'])
            v = (r['valor'] or '').strip()
            if not cs:
                if v not in ('', '0'):
                    stats['descuadres'].append((r['cuerda'], 'sin nudos pero valor ' + v))
                continue
            stats['con_nudos'] += 1
            try:
                vv = int(re.sub(r'[^0-9]', '', v) or -1)
            except ValueError:
                continue
            if len(cs) == 1:
                stats['vacuas'] += 1
                if vv not in (cs[0], 10 * cs[0], 100 * cs[0]):
                    stats['descuadres'].append((r['cuerda'], f'escrito {vv} vs unico racimo {cs[0]}'))
                continue
            stats['verificables'] += 1
            mm = models(cs)
            hit = [k for k, val in mm.items() if val == vv]
            if hit:
                stats['ok'] += 1
                for k in hit:
                    stats['modelos'][k] = stats['modelos'].get(k, 0) + 1
            else:
                stats['descuadres'].append(
                    (r['cuerda'], f'escrito {vv} vs nudos {cs} -> ' + ' '.join(f'{k}={x}' for k, x in mm.items())))
        resumen.append(stats)
        print(f"== {stats['f']}: filas {stats['filas']}, con nudos {stats['con_nudos']}, "
              f"verificables {stats['verificables']}, coinciden {stats['ok']}, vacuas {stats['vacuas']}")
        if stats['modelos']:
            print('   modelo(s) que encajan:', stats['modelos'])
        for d in stats['descuadres']:
            print('   DESCUADRE', d[0], '-', d[1])
    tot_v = sum(s['verificables'] for s in resumen)
    tot_ok = sum(s['ok'] for s in resumen)
    print(f"\nTOTAL: {len(resumen)} fichas, {sum(s['con_nudos'] for s in resumen)} cuerdas con nudos, "
          f"{tot_v} verificables, {tot_ok} coinciden ({100*tot_ok/max(tot_v,1):.1f}%), "
          f"{sum(s['vacuas'] for s in resumen)} vacuos, {sum(len(s['descuadres']) for s in resumen)} descuadres")
    json.dump(resumen, open(os.path.join(HERE, 'verificacion.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1:] or None)
