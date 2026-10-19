"""Resumen por ficha: cuerdas, cuerdas con nudos, valores, subsidiarias, verificacion.

Lee los transcription_*.csv y verificacion.json y escribe resumen.csv.
"""
import csv, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r'(\d+)\s*([SLEB]{1,2})\s*\(')


def main():
    ver = {v['f']: v for v in json.load(open(os.path.join(HERE, 'verificacion.json'), encoding='utf-8'))}
    rows_out = []
    for f in sorted(glob.glob(os.path.join(HERE, 'transcripcion_*.csv'))):
        rows = list(csv.DictReader(open(f, encoding='utf-8')))
        name = os.path.basename(f).replace('transcripcion_', '').replace('_record.csv', '')
        vals = [int(re.sub(r'[^0-9]', '', r['valor'])) for r in rows
                if re.sub(r'[^0-9]', '', r['valor'] or '')]
        knotrows = [r for r in rows if PAT.search(r['nudos'] or '')]
        subs = [r for r in rows if 's' in r['cuerda']]
        blanks = [r for r in rows if not PAT.search(r['nudos'] or '')]
        v = ver.get(os.path.basename(f), {})
        rows_out.append(dict(
            ficha=name, cuerdas=len(rows), con_nudos=len(knotrows), sin_nudos=len(blanks),
            subsidiarias=len(subs), suma_valores=sum(vals), max_valor=max(vals) if vals else 0,
            verificables=v.get('verificables', 0), coinciden=v.get('ok', 0),
            descuadres=len(v.get('descuadres', [])),
            colores=';'.join(sorted({r['color'].split('(')[0].split('/')[0].strip('?') for r in rows})),
        ))
    cols = list(rows_out[0].keys())
    with open(os.path.join(HERE, 'resumen.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_out)
    print('ficha    cuerdas con/sin nudos  subs  suma  max  verif ok  desc  colores')
    for r in rows_out:
        print(f"{r['ficha']:8} {r['cuerdas']:4} {r['con_nudos']:5}/{r['sin_nudos']:<5} {r['subsidiarias']:5} "
              f"{r['suma_valores']:6} {r['max_valor']:4} {r['verificables']:5} {r['coinciden']:3} {r['descuadres']:4}  {r['colores']}")
    print('\nTOTAL cuerdas', sum(r['cuerdas'] for r in rows_out),
          '| con nudos', sum(r['con_nudos'] for r in rows_out),
          '| sin nudos', sum(r['sin_nudos'] for r in rows_out),
          '| suma de valores', sum(r['suma_valores'] for r in rows_out))


if __name__ == '__main__':
    main()
