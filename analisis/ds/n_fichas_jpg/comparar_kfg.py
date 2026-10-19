"""Compara las 11 fichas de Huacones con la base KFG (cuerdas.csv) a nivel de quipu.

Metricas por quipu:
  - frac_sin_nudos : proporcion de cuerdas con 'nudos' vacio
  - mediana_valor  : mediana de los valores de las cuerdas con nudos
  - frac_le9       : proporcion de cuerdas con nudos y valor <= 9
  - frac_ge100     : proporcion de cuerdas con nudos y valor >= 100
Comparacion: Mann-Whitney U (quipu = unidad), y percentil de cada ficha dentro de KFG.
"""
import csv, glob, os, re
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def fichas_metrics():
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, 'transcripcion_*.csv'))):
        rows = list(csv.DictReader(open(f, encoding='utf-8')))
        name = os.path.basename(f).replace('transcripcion_', '').replace('_record.csv', '')
        kn = [r for r in rows if re.search(r'\d+[SLEB]+\(', r['nudos'] or '')]
        vals = [int(re.sub(r'[^0-9]', '', r['valor'])) for r in kn]
        out.append(dict(kfg=name, n=len(rows),
                        frac_sin_nudos=1 - len(kn) / len(rows),
                        mediana_valor=np.median(vals) if vals else np.nan,
                        frac_le9=np.mean([v <= 9 for v in vals]) if vals else np.nan,
                        frac_ge100=np.mean([v >= 100 for v in vals]) if vals else np.nan))
    return pd.DataFrame(out)


def kfg_metrics():
    c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'),
                    usecols=['kfg', 'nudos', 'valor'], dtype={'nudos': str})
    c['tiene'] = c['nudos'].fillna('').str.strip().str.len() > 0
    g = c.groupby('kfg')
    d = pd.DataFrame({
        'n': g.size(),
        'frac_sin_nudos': 1 - g['tiene'].mean(),
        'mediana_valor': g.apply(lambda x: x.loc[x['tiene'], 'valor'].median(), include_groups=False),
        'frac_le9': g.apply(lambda x: (x.loc[x['tiene'], 'valor'] <= 9).mean(), include_groups=False),
        'frac_ge100': g.apply(lambda x: (x.loc[x['tiene'], 'valor'] >= 100).mean(), include_groups=False),
    }).reset_index()
    return d


def main():
    f = fichas_metrics()
    k = kfg_metrics()
    print('--- fichas Huacones (11)')
    print(f.to_string(index=False, float_format=lambda x: f'{x:.2f}'))
    print('\n--- KFG (651 quipus): mediana [IQR]')
    for col in ['n', 'frac_sin_nudos', 'mediana_valor', 'frac_le9', 'frac_ge100']:
        x = k[col].dropna()
        print(f'  {col:15} mediana {x.median():7.2f}  IQR [{x.quantile(.25):.2f}, {x.quantile(.75):.2f}]')
    print('\n--- Mann-Whitney (quipu = unidad): Huacones vs KFG')
    for col in ['n', 'frac_sin_nudos', 'mediana_valor', 'frac_le9', 'frac_ge100']:
        a = f[col].dropna(); b = k[col].dropna()
        u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
        print(f'  {col:15} Huacones {a.median():7.2f} vs KFG {b.median():7.2f}   p={p:.2e}'
              f'   percentil medio de las fichas = {np.mean([(b < v).mean() for v in a]):.2f}')
    print('\n--- JC001-JC023 (Incahuasi, mismo prefijo JC) para contexto')
    jj = k[k.kfg.str.startswith('JC0')]
    print(jj[['n', 'frac_sin_nudos', 'mediana_valor', 'frac_le9', 'frac_ge100']]
          .describe().loc[['count', '50%']].to_string(float_format=lambda x: f'{x:.2f}'))
    f.to_csv(os.path.join(HERE, 'comparacion_kfg_fichas.csv'), index=False)


if __name__ == '__main__':
    main()
