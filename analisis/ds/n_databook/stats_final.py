#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cifras finales para el informe."""
import os, re, glob
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

db = pd.read_csv(D('databook_rows.csv'))
res = pd.read_csv(D('databook_vs_kfg.csv'))
disc = pd.read_csv(D('discrepancias.csv'))
kf = pd.read_csv(D('..', '..', 'datos', 'cuerdas.csv'))
kf = kf[kf.kfg.str.startswith('AS')].copy()
kf['quipu'] = kf.kfg
est = pd.read_csv(D('databook_estructura.csv'))
notas = pd.read_csv(D('notas_ascher.csv'))

print('== PARSER ==')
print('filas', len(db), '| quipus', db.quipu.nunique(), '| archivos', len(glob.glob(os.path.join(BASE, '..', '..', 'fuentes_txt', 'databook', 'as[0-9]*.txt'))))
print('nivel', db.cord_databook.str.count('s').value_counts().sort_index().to_dict())
print('color ausente %.3f | valor dudoso %d | sumas explicitas %d' %
      (db.color.isna().mean(), db.valor_dudoso.sum(),
       db.valor_expr.fillna('').str.contains(r'\+').sum()))
dv = db[db.valor.notna()]
print('filas con valor', len(dv))
print('valor == decodificacion de sus nudos: %.3f' % (dv.valor == dv.valor_knots).mean())
print('valor == decodificacion (misma decena): %.3f' % (
    dv.valor.apply(lambda x: str(int(x)).rstrip('0')) == dv.valor_knots.apply(lambda x: str(int(x)).rstrip('0'))).mean())

db0 = db[db.cord_databook.str.match(r'^(p\d+|t\d+)$')]
esp = est.n_pendientes_desc.fillna(0) + est.n_tops_desc.fillna(0)
print('\n== COBERTURA ==')
print('nivel0 parseado total', len(db0), '| esperado por descripcion', int(esp.sum()))
cov = db0.groupby('quipu').size().rename('n').to_frame().join(est.set_index('quipu'))
cov['esp'] = cov.n_pendientes_desc.fillna(0) + cov.n_tops_desc.fillna(0)
cov = cov[cov.esp > 0]
cov['cob'] = cov.n / cov.esp
print('cobertura nivel0: mediana %.3f p25 %.3f | quipus <70%%: %d/%d' %
      (cov.cob.median(), cov.cob.quantile(.25), int((cov.cob < 0.7).sum()), len(cov)))

print('\n== CRUCE ==')
r = res[(res.nivel_db == res.nivel_kfg) & (res.score >= 3)]
print('pares totales', len(res), '| comparables', len(r), '| quipus', r.quipu.nunique())
rv = r[r.valor_db.notna() & r.valor_kfg.notna()]
print('pares con valor en ambas fuentes', len(rv))
print('valor igual %.3f | largo<=0.5 %.3f | color igual %.3f' %
      ((rv.valor_db == rv.valor_kfg).mean(), ((r.largo_db - r.largo_kfg).abs() <= 0.5).mean(),
       (r.color_db_n.fillna('') == r.color_kfg_n.fillna('')).mean()))
print('discrepancias valor', len(disc), 'tasa %.4f' % (len(disc) / len(r)))
print(disc.clase.value_counts().to_string())
print('\nquipus con discrepancia', disc.quipu.nunique(), '| top5 share %.2f' %
      (disc.groupby('quipu').size().nlargest(5).sum() / len(disc)))

print('\n== CONTEOS DE CUERDAS ==')
both = set(db0.quipu) & set(kf[kf.nivel == 0].quipu)
print('quipus databook', db0.quipu.nunique(), '| KFG AS', kf.quipu.nunique())
print('en ambos', len(both), '| solo databook', len(set(db0.quipu) - set(kf.quipu)),
      '| solo KFG', len(set(kf.quipu) - set(db.quipu)))
print('KFG solo:', sorted(set(kf.quipu) - set(db.quipu)))
print('KFG largo==0:', int((kf.largo == 0).sum()), '| con valor>0 y largo 0:', int(((kf.largo == 0) & (kf.valor > 0)).sum()))

print('\n== COLOR / LARGO ==')
m = r.copy()
print('color exacto %.3f' % (m.color_db_n.fillna('') == m.color_kfg_n.fillna('')).mean())
print('color sin W %.3f' % m.apply(lambda x: frozenset(str(x.color_db_n).split(':')).difference(['W', '', 'nan']) ==
                                   frozenset(str(x.color_kfg_n).split(':')).difference(['W', '', 'nan']), axis=1).mean())
print('largo dif media %.2f | max %.1f | >1cm %d' %
      ((m.largo_db - m.largo_kfg).abs().mean(), (m.largo_db - m.largo_kfg).abs().max(),
       int(((m.largo_db - m.largo_kfg).abs() > 1).sum())))

print('\n== NOTAS ==')
print('items', len(notas), '| quipus', notas.quipu.nunique(),
      '| con numeros', int(notas.tiene_numeros.sum()),
      '| aritmetica', int(notas.tipo.str.contains('relacion_aritmetica').sum()),
      '| suma/igualdad', int(notas.tipo.str.contains('suma_igualdad').sum()))
