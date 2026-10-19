#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisis del cruce: discrepancias de valor clasificadas, color y largo.
Genera discrepancias.csv y resumen_quipus.csv."""
import os
import numpy as np
import pandas as pd
from decoder import decode

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

res = pd.read_csv(D('databook_vs_kfg.csv'))
db = pd.read_csv(D('databook_rows.csv'))
kf = pd.read_csv(D('..', '..', 'datos', 'cuerdas.csv'))
kf = kf[kf.kfg.str.startswith('AS')].copy()
kf['quipu'] = kf.kfg
est = pd.read_csv(D('databook_estructura.csv'))

res['valor_db'] = pd.to_numeric(res.valor_db, errors='coerce')
res['valor_kfg'] = pd.to_numeric(res.valor_kfg, errors='coerce')

# decodificar nudos KFG (con largo para posicion)
kf['kfg_sem'], kf['kfg_amb'], _ = zip(*kf.apply(lambda r: decode(r.nudos, r.largo), axis=1))
def _aporte(n):
    if pd.isna(n):
        return 0.0
    tot = 0.0
    for p in str(n).split(';'):
        if ',' in p:
            try:
                tot += float(p.rsplit(',', 1)[1])
            except ValueError:
                pass
    return tot
kf['kfg_aporte'] = kf.nudos.apply(_aporte)
res = res.merge(kf[['quipu', 'cuerda', 'kfg_sem', 'kfg_amb', 'kfg_aporte', 'nudos']],
                left_on=['quipu', 'cord_kfg'], right_on=['quipu', 'cuerda'], how='left')

# valor semantico del databook ya viene en valor_knots / knots_ambiguo
res['kfg_tiene_nudos'] = res.nudos.notna() & (res.nudos.astype(str).str.strip() != '')
res['db_tiene_nudos'] = res.knots_norm.notna() & (res.knots_norm.astype(str).str.strip() != '')

def subseq(a, b):
    a, b = str(int(a)), str(int(b))
    if len(a) > len(b): a, b = b, a
    it = iter(b)
    return all(ch in it for ch in a)

def classify(row):
    vd, vk = row.valor_db, row.valor_kfg
    if pd.isna(vd) or pd.isna(vk):
        return 'd_otras', 'valor faltante'
    if row.valor_dudoso:
        return 'd_valor_dudoso', 'Databook marca el valor con ? (incierto)'
    if not row.kfg_tiene_nudos and vk == 0:
        return 'd_kfg_sin_nudos', 'KFG no registra nudos (valor 0 por defecto)'
    db_sem, db_amb = row.valor_knots, bool(row.knots_ambiguo)
    kf_sem, kf_amb = row.kfg_sem, bool(row.kfg_amb)
    def sig(x):
        return int(str(int(round(x))).rstrip('0') or '0')
    db_ok = pd.notna(db_sem) and sig(db_sem) == sig(vd)
    kf_ok = pd.notna(kf_sem) and sig(kf_sem) == sig(vk)
    if db_ok and kf_ok:
        if vd > 0 and vk > 0 and max(vd, vk) / min(vd, vk) in (10, 100):
            return 'd_convencion_x10', 'ambas fuentes coherentes con sus nudos; difieren solo en la posicion decimal'
        return 'd_otras', 'cada fuente coherente con sus propios nudos'
    # (a) corrupcion OCR del numero impreso
    ocr = subseq(vd, vk) or (vd == 10 * vk) or (vk == 10 * vd) or (vd == 100 * vk) or (vk == 100 * vd)
    if ocr:
        return 'a_ocr', 'digitos insertados/perdidos: %d vs %d' % (int(vd), int(vk))
    if db_ok and not kf_ok:
        return 'b_error_kfg', 'nudos Databook dan %s; KFG imprime %s y sus nudos dan %s' % (db_sem, int(vk), kf_sem)
    if kf_ok and not db_ok:
        return 'c_error_databook', 'nudos KFG dan %s; Databook imprime %s y sus nudos dan %s' % (kf_sem, int(vd), db_sem)
    return 'd_otras', 'nudos ambiguos o no concluyentes (db=%s kfg=%s)' % (db_sem, kf_sem)

# solo pares comparables: mismo nivel, score alto
res = res[(res.nivel_db == res.nivel_kfg) & (res.score >= 3)].copy()
res[['clase', 'detalle']] = pd.DataFrame(res.apply(classify, axis=1).tolist(), index=res.index)
res['dif'] = res.valor_db - res.valor_kfg
res['color_eq'] = res.color_db_n.fillna('') == res.color_kfg_n.fillna('')
res['largo_dif'] = (res.largo_db - res.largo_kfg).abs()

disc = res[res.valor_db.notna() & res.valor_kfg.notna() & (res.valor_db != res.valor_kfg)].copy()
disc.to_csv(D('discrepancias.csv'), index=False, encoding='utf-8')
print('pares comparables', len(res), '| discrepancias', len(disc),
      '| tasa', round(len(disc) / len(res), 4))
print(disc.clase.value_counts().to_string())
for cl in disc.clase.unique():
    x = disc[disc.clase == cl]
    print('--', cl, len(x))
    print(x[['quipu', 'cord_db', 'cord_kfg', 'valor_db', 'valor_kfg', 'valor_knots',
             'kfg_sem', 'detalle']].head(4).to_string(max_colwidth=38))

# color / largo
m = res.copy()
m['color_eq'] = m.color_db_n.fillna('') == m.color_kfg_n.fillna('')
m['largo_dif'] = (m.largo_db - m.largo_kfg).abs()
print('\ncolor exacto %.3f | largo <=0.5 %.3f' % (m.color_eq.mean(), (m.largo_dif <= 0.5).mean()))

# resumen por quipu
db0 = db[db.cord_databook.str.match(r'^(p\d+|t\d+)$')]
kf0 = kf[kf.nivel == 0]
rows = []
for q in sorted(set(db.quipu) | set(kf0.quipu)):
    a = db0[db0.quipu == q]; b = kf0[kf0.quipu == q]
    rr = res[res.quipu == q]; e = est[est.quipu == q]
    rows.append(dict(quipu=q, en_kfg=q in set(kf0.quipu),
                     n_db0=len(a), n_kfg0=len(b),
                     n_esperado=(e.n_pendientes_desc.iloc[0] + e.n_tops_desc.iloc[0]) if len(e) else np.nan,
                     n_pares=len(rr),
                     n_disc=int((rr.valor_db != rr.valor_kfg).sum()),
                     color_eq=round(rr.color_eq.mean(), 3) if len(rr) else np.nan,
                     largo_ok=round((rr.largo_dif <= 0.5).mean(), 3) if len(rr) else np.nan))
pd.DataFrame(rows).to_csv(D('resumen_quipus.csv'), index=False)
