# -*- coding: utf-8 -*-
"""Catalogo de rasgos no numericos en las notas cualitativas de los quipus.

Fuentes
  - analisis/datos/cuerdas.csv   columna `notas` (KFG, 2493 cuerdas anotadas)
  - khipu.db                     khipu_main.NOTES, primary_cord.NOTES/plainnotes,
                                 cord.CORD_NOTES (OKR)

Salidas (en esta carpeta)
  rasgos.csv       una fila por cuerda anotada de cuerdas.csv + flags
  rasgos_okr.csv   una fila por nota de OKR + flags
No imprime notas completas: solo recuentos.
"""
import re, sqlite3, os
import pandas as pd

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = os.path.join(RAIZ, 'analisis', 'datos')
DB = os.path.join(RAIZ, 'data', 'external', 'open-khipu-repository', 'data', 'khipu.db')
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- taxonomia v2
# Patrones en minusculas. precision revisada a mano sobre muestras (ver informe).
PAT = {
    # condicion fisica
    'rota':          r'\bbroken\b|\bbreak(?:s|ing)?\b|\bcut\b|\bfragment|\bfray|\btorn\b|\bhalf-broken\b',
    'deterioro':     r'\bdeteriorat|\brotten\b|\brot\b|\bdecay|\bworn\b|\bcrush|\bmildew|\binsect|\brodent|\bhole\b|\bdamaged?\b|\bstain',
    'perdida':       r'\bmissing\b|\babsent\b|\blost\b|\bgone\b|\bno longer\b|\bnot survive\b|\bdoes not survive\b',
    'desprendida':   r'\bdetached?\b',
    'reparacion':    r'\brepair|\bmend|\bsplic|\bre-?attach|\bre-?tie|\bre-?knott|\breconstruct|\brestor|\bglued\b|\bconsolidat|\bsewn\b|\bre-?unite|\bincorrectly repaired',
    # nudos / construccion
    'sin_nudo_final': r'no end knot|sin nudo final',
    'nudo_extra':    r'\bextra knot|\bdouble knot|knot above (?:the )?bar|knot (?:in|on) the (?:main|primary) cord|nudo en el cord[oó]n principal|\bodd knot|\bunusual knot',
    'cuerda_superior': r'\btop cord|\bcuerda superior',
    'cordon_principal': r'primary cord|main cord|cord[oó]n principal|cuerda principal|cord[oó]n doblado',
    'envoltura':     r'\bwrapp|\bwraped\b|\bwrapped\b',
    'marcador':      r'\bmarker',
    # objetos / materiales anadidos
    'objeto':        r'\bmetal\b|\bwire\b|\bpin\b|\bwood\b|\bshell\b|\bgourd\b|\bbead|\bbar\b|\bcloth\b|\btassel|\bfeather|\bpluma\b',
    'pelo':          r'\bhair\b|\bpelo\b',
    # color
    'color_anomalo': r'__AND__',
    'fibra':         r'\bfib(?:er|re)\b',
    # ruido documental (se mide, no es rasgo del quipu)
    'etiqueta':      r'\bsee ob\.?|\bsee observation|\bsee general note|\bsee sketch|\bsee diagram|\blabel\b|\btag\b|\bmuseum num|\bphoto',
    'clasif_tipo':   r'\btype [a-d]\b|\bvalue \d|\balt\.? ?value',
}
PAT = {k: re.compile(v, re.I) for k, v in PAT.items()}
# color_anomalo = mencion de color Y de una anomalia de color en la misma nota
COLOR = re.compile(r'\bcolou?r\b', re.I)
ANOM = re.compile(r'faded?|discolou?r|stain|dyed?|paint|indistinct|uncertain|no color|cannot', re.I)


def flags(s):
    s = s if isinstance(s, str) else ''
    f = {k: bool(p.search(s)) for k, p in PAT.items() if k != 'color_anomalo'}
    f['color_anomalo'] = bool(COLOR.search(s) and ANOM.search(s))
    return f


# ---------------------------------------------------------------- cuerdas.csv
cu = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
cu['notas'] = cu['notas'].fillna('')
an = cu[cu['notas'].str.strip() != ''].copy()
F = pd.DataFrame([flags(s) for s in an['notas']], index=an.index)
an = pd.concat([an, F], axis=1)
an.to_csv(os.path.join(OUT, 'rasgos.csv'), index=False, encoding='utf-8')
print('== cuerdas.csv: %d cuerdas anotadas de %d (%d quipus de %d)' % (
    len(an), len(cu), an.kfg.nunique(), cu.kfg.nunique()))
res = pd.DataFrame({'cuerdas': F.sum(),
                    'quipus': pd.Series({k: an.loc[F[k], 'kfg'].nunique() for k in F.columns})})
print(res.sort_values('quipus', ascending=False).to_string())

# ---------------------------------------------------------------- OKR
con = sqlite3.connect(DB)
rows = []
for q, lvl in [('select OKR_NUM, NOTES from khipu_main', 'quipu'),
               ('select k.OKR_NUM, p.NOTES from primary_cord p join khipu_main k using(KHIPU_ID)', 'pc'),
               ('select k.OKR_NUM, p.plainnotes from primary_cord p join khipu_main k using(KHIPU_ID)', 'pc_plain'),
               ('select k.OKR_NUM, c.CORD_NOTES from cord c join khipu_main k using(KHIPU_ID)', 'cuerda')]:
    d = pd.read_sql(q, con)
    d.columns = ['KHIPU_ID', 'nota']
    d = d[d['nota'].notna() & (d['nota'].astype(str).str.strip() != '')]
    d['nivel'] = lvl
    rows.append(d)
okr = pd.concat(rows, ignore_index=True)
G = pd.DataFrame([flags(s) for s in okr['nota']], index=okr.index)
okr = pd.concat([okr, G], axis=1)
okr.to_csv(os.path.join(OUT, 'rasgos_okr.csv'), index=False, encoding='utf-8')
print('\n== khipu.db: %d notas en %d quipus (quipu %d / pc %d / cuerda %d)' % (
    len(okr), okr.KHIPU_ID.nunique(), (okr.nivel == 'quipu').sum(),
    (okr.nivel.str.startswith('pc')).sum(), (okr.nivel == 'cuerda').sum()))
res2 = pd.DataFrame({'notas': G.sum(),
                     'quipus': pd.Series({k: okr.loc[G[k], 'KHIPU_ID'].nunique() for k in G.columns})})
print(res2.sort_values('quipus', ascending=False).to_string())
