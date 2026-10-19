# -*- coding: utf-8 -*-
"""Controles de validacion del catalogo de notas.

1) concordancia entre las notas de cuerdas.csv (KFG) y CORD_NOTES (OKR)
2) sin_nudo_final frente al campo estructurado `terminacion`
3) cuerdas superiores: union == 'T' frente a la nota "top cord"
"""
import os, sqlite3, numpy as np, pandas as pd
from sklearn.metrics import cohen_kappa_score

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
pd.set_option('display.width', 160)
an = pd.read_csv(os.path.join(AQUI, 'rasgos.csv'))
okr = pd.read_csv(os.path.join(AQUI, 'rasgos_okr.csv'))
cu = pd.read_csv(os.path.join(RAIZ, 'analisis', 'datos', 'cuerdas.csv'))
FEATS = ['rota', 'deterioro', 'perdida', 'reparacion', 'envoltura', 'marcador',
         'objeto', 'cuerda_superior', 'cordon_principal']

# ---- 1. concordancia KFG vs OKR (mapeando kfg -> OKR_NUM via quipus.csv)
oc = okr[okr.nivel == 'cuerda']
mapa = pd.read_csv(os.path.join(RAIZ, 'analisis', 'datos', 'quipus.csv')).set_index('kfg')['okr']
an['kh'] = an.kfg.map(mapa)
oc = oc.assign(kfg=oc.KHIPU_ID)
print('== 1. KFG vs OKR (notas de cuerda, kfg->KH)')
print('quipus con notas de cuerda: KFG %d (con KH %d), OKR %d, ambos %d' % (
    an.kfg.nunique(), an.kh.notna().nunique(), oc.KHIPU_ID.nunique(),
    len(set(an.kh.dropna()) & set(oc.KHIPU_ID))))
print('notas en quipus OKR que no estan en KFG: %d quipus' % len(set(oc.KHIPU_ID) - set(an.kh.dropna())))

# coincidencia literal de cadenas
a_set = set(zip(an.kh.dropna(), an.loc[an.kh.notna(), 'notas'].str.strip().str.lower()))
o_set = set(zip(oc.KHIPU_ID, oc.nota.str.strip().str.lower()))
print('cadenas (quipu,nota) KFG=%d OKR=%d interseccion=%d' % (
    len(a_set), len(o_set), len(a_set & o_set)))

common = sorted(set(an.kh.dropna()) & set(oc.KHIPU_ID))
print('quipus comunes: %d' % len(common))
filas = []
for f in FEATS:
    a = an[an.kh.isin(common)].groupby('kh')[f].max()
    b = oc[oc.KHIPU_ID.isin(common)].groupby('KHIPU_ID')[f].max()
    ambos = pd.concat([a, b], axis=1, keys=['kfg', 'okr']).fillna(False)
    if ambos.kfg.sum() + ambos.okr.sum() == 0:
        continue
    k = cohen_kappa_score(ambos.kfg, ambos.okr)
    filas.append({'rasgo': f, 'KFG': int(ambos.kfg.sum()), 'OKR': int(ambos.okr.sum()),
                  'ambos': int((ambos.kfg & ambos.okr).sum()), 'kappa': round(k, 3)})
print(pd.DataFrame(filas).to_string(index=False))

# ---- 2. sin_nudo_final vs terminacion
print('\n== 2. "no end knot" frente a terminacion (KFG)')
sub = an[an.sin_nudo_final]
print('cuerdas con "no end knot": %d; terminacion:' % len(sub))
print(sub.terminacion.value_counts(dropna=False).to_string())
print('cuerdas SIN la nota y su terminacion (muestra):')
print(an[~an.sin_nudo_final].terminacion.value_counts(dropna=False).head(5).to_string())
print('P(no end knot | terminacion=U) = %.3f  (n=%d)' % (
    an[an.terminacion == 'U'].sin_nudo_final.mean(), (an.terminacion == 'U').sum()))

# ---- 3. cuerdas superiores
print('\n== 3. cuerdas superiores (union T) frente a nota "top cord"')
tq = cu[cu.union.astype(str).str.upper() == 'T'].kfg.unique()
print('quipus con >=1 cuerda union T: %d; con nota top cord: %d; ambos: %d' % (
    len(tq), an.loc[an.cuerda_superior, 'kfg'].nunique(),
    len(set(tq) & set(an.loc[an.cuerda_superior, 'kfg']))))
# sensibilidad de la nota para detectar T, entre quipus anotados
ann = set(an.kfg)
t_ann = [k for k in tq if k in ann]
det = [k for k in t_ann if an.loc[(an.kfg == k) & an.cuerda_superior].shape[0] > 0]
print('de %d quipus con T y con notas, la nota menciona top cord en %d (%.0f%%)' % (
    len(t_ann), len(det), 100 * len(det) / max(1, len(t_ann))))
print('quipus con nota top cord y sin ninguna union T: %d' % len(
    set(an.loc[an.cuerda_superior, 'kfg']) - set(tq)))
