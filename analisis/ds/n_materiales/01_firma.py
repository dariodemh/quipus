# -*- coding: utf-8 -*-
"""
01_firma.py  --  Firma de manufactura por quipu (rasgos NO numericos) y controles.

Salidas:
  firma_quipu.csv        una fila por quipu KFG + rasgos OKR
  cuerdas_rasgos.csv     cord-level con torsion, union, terminacion, dir. nudo, fibra, grosor
Uso: python 01_firma.py
"""
import re, sqlite3, os
import numpy as np
import pandas as pd

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
DB = os.path.join(RAIZ, 'data', 'external', 'open-khipu-repository', 'data', 'khipu.db')
AQUI = os.path.dirname(os.path.abspath(__file__))

c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(DAT, 'quipus.csv'))

# ---------- color: familia gruesa (primer token) ----------
def fam_color(s):
    if not isinstance(s, str) or s.strip() == '':
        return None
    t = re.split(r'[:\-/]', s.strip())[0]
    t = re.sub(r'\(.*', '', t)
    return t if t else None

c['color_fam'] = c['color'].map(fam_color)
# tokens mezclados: cuantos hilos combina
c['color_mixto'] = c['color'].fillna('').str.contains(r'[:\-/]')

# ---------- direccion de nudos por tipo ----------
# formato  nTIPO(pos,direccion),valor   ej 3S(7.5,U),30 ; 9L(9.0,U),9
RE_NUDO = re.compile(r'(\d+)([A-Z]+)\(([0-9.]+),\s*([SZU])\)')

def parse_nudos(s):
    """devuelve dict con conteos de nudos por (tipo,dir)."""
    out = {}
    if not isinstance(s, str):
        return out
    for m in RE_NUDO.finditer(s):
        n = int(m.group(1)); tipo = m.group(2); d = m.group(4)
        out[(tipo, d)] = out.get((tipo, d), 0) + n
    return out

parsed = c['nudos'].map(parse_nudos)

def cnt(tipos, d):
    tot = 0
    for p in parsed:
        for (t, dd), n in p.items():
            if t in tipos and dd == d:
                tot += n
    return tot

for tipo, nombre in [(('S',), 'simple'), (('L','LL'), 'largo'), (('E','EE'), 'ocho')]:
    for d in 'SZ':
        c[f'nd_{nombre}_{d}'] = [sum(n for (t,dd),n in p.items() if t in tipo and dd==d) for p in parsed]
    c[f'nd_{nombre}_n'] = c[f'nd_{nombre}_S'] + c[f'nd_{nombre}_Z']

# ---------- OKR: fibra, grosor, twist, canutos, notas ----------
con = sqlite3.connect(DB)
cord = pd.read_sql("""select KHIPU_ID, CORD_ID, FIBER, THICKNESS, TWIST, TWIST_ANGLE,
                             ATTACHMENT_TYPE, TERMINATION, CORD_LENGTH, CORD_LEVEL,
                             PENDANT_FROM, CLUSTER_ID, CLUSTER_ORDINAL, CORD_ORDINAL,
                             CANUTO_ID, CORD_NOTES, CREATED_BY
                      from cord""", con)
km = pd.read_sql("select KHIPU_ID, OKR_NUM, PROVENANCE, REGION, MUSEUM_NAME from khipu_main", con)
pc = pd.read_sql("select KHIPU_ID, STRUCTURE, THICKNESS, FIBER, TERMINATION, BEGINNING, TWIST from primary_cord", con)
pc = pc.drop_duplicates('KHIPU_ID')
can = pd.read_sql("select KHIPU_ID, count(*) n_canutos, count(distinct CANUTO_ID) n_can_clusters from canuto group by 1", con)

# fibra OKR: limpiar
cord['FIBER'] = cord['FIBER'].replace({'': None})
fib_map = {'CN':'algodon','CL':'camelido','W':'lana','H':'cabello','CC':'mezcla','V':'vegetal','AH':'pelo_animal'}

q2 = q.merge(km, left_on='okr', right_on='OKR_NUM', how='left')
q2 = q2.merge(pc, on='KHIPU_ID', how='left', suffixes=('', '_pc'))
q2 = q2.merge(can, on='KHIPU_ID', how='left')

# grosor / fibra por quipu
g = cord.groupby('KHIPU_ID')
okr = pd.DataFrame({
    'n_cord_okr': g.size(),
    'thick_mean': g.THICKNESS.mean(),
    'thick_med': g.THICKNESS.median(),
    'thick_sd': g.THICKNESS.std(),
    'thick_cv': g.THICKNESS.std() / g.THICKNESS.mean(),
    'thick_n': g.THICKNESS.count(),
    'fib_n': g.FIBER.count(),
    'cl_n': cord.assign(x=(cord.FIBER=='CL').astype(int)).groupby('KHIPU_ID').x.sum(),
    'cn_n': cord.assign(x=(cord.FIBER=='CN').astype(int)).groupby('KHIPU_ID').x.sum(),
    'twist_n': g.TWIST.count(),
    'n_canuto_cords': cord.assign(x=cord.CANUTO_ID.notna().astype(int)).groupby('KHIPU_ID').x.sum(),
    'created_by': g.CREATED_BY.agg(lambda s: s.mode().iloc[0] if len(s.mode()) else None),
    'created_by_uniq': g.CREATED_BY.nunique(),
}).reset_index()
q2 = q2.merge(okr, on='KHIPU_ID', how='left')
q2['fib_frac_cl'] = q2.cl_n / q2.fib_n.replace(0, np.nan)
q2['fib_frac_cod'] = q2.fib_n / q2.n_cord_okr.replace(0, np.nan)
q2['canuto_frac'] = q2.n_canuto_cords / q2.n_cord_okr.replace(0, np.nan)
q2['thick_sd_rel'] = q2.thick_sd / q2.thick_mean

# ---------- agregados KFG por quipu ----------
c['torsion_ok'] = c['torsion'].isin(['S','Z'])
c['union_ok'] = c['union'].isin(['R','V','T'])
c['term_ok'] = c['terminacion'].notna() & (c['terminacion'].astype(str) != 'nan')

def frac(df, col, val, den):
    return df[col].eq(val).sum() / den if den else np.nan

rows = []
for kfg, d in c.groupby('kfg'):
    n = len(d)
    dep = d[d.nivel == 0]
    nt = d.torsion_ok.sum()
    nu = d.union_ok.sum()
    nterm = d.term_ok.sum()
    # entropia de color (familias) -- normalizada por log(n colores posibles observados)
    vc = d.color_fam.dropna().value_counts()
    p = vc / vc.sum()
    H = -(p * np.log(p)).sum() if len(p) > 1 else 0.0
    fams = set(d.color_fam.dropna())
    rows.append(dict(
        kfg=kfg, n_cuerdas=n, n_pend=len(dep), n_grupos=d.grupo.nunique(),
        n_sub=d.nivel.gt(0).sum(),
        # torsion
        n_tors=nt, pS_tors=d.torsion.eq('S').sum()/nt if nt else np.nan,
        pU_tors=d.torsion.eq('U').sum()/n,
        # nudos por tipo
        n_nd_simple=d.nd_simple_n.sum(), pS_nd_simple=(d.nd_simple_S.sum()/d.nd_simple_n.sum()) if d.nd_simple_n.sum() else np.nan,
        n_nd_largo=d.nd_largo_n.sum(), pS_nd_largo=(d.nd_largo_S.sum()/d.nd_largo_n.sum()) if d.nd_largo_n.sum() else np.nan,
        n_nd_ocho=d.nd_ocho_n.sum(), pS_nd_ocho=(d.nd_ocho_S.sum()/d.nd_ocho_n.sum()) if d.nd_ocho_n.sum() else np.nan,
        # union
        n_union=nu, pR=d.union.eq('R').sum()/nu if nu else np.nan,
        pV=d.union.eq('V').sum()/nu if nu else np.nan,
        pT=d.union.eq('T').sum()/nu if nu else np.nan,
        pU_union=d.union.eq('U').sum()/n,
        # terminacion
        n_term=nterm, pK=d.terminacion.eq('K').sum()/nterm if nterm else np.nan,
        pB_term=d.terminacion.eq('B').sum()/nterm if nterm else np.nan,
        pU_term=d.terminacion.eq('U').sum()/nterm if nterm else np.nan,
        pR_term=d.terminacion.eq('R').sum()/nterm if nterm else np.nan,
        n_term_tipos=d.terminacion.nunique(),
        # color
        n_fam=len(fams), H_color=H,
        H_color_norm=H/np.log(len(fams)) if len(fams) > 1 else 0.0,
        colores_por_cuerda=len(fams)/n,
        pW=d.color_fam.eq('W').sum()/d.color_fam.notna().sum() if d.color_fam.notna().sum() else np.nan,
        pAB=d.color_fam.eq('AB').sum()/d.color_fam.notna().sum(),
        pMB=d.color_fam.eq('MB').sum()/d.color_fam.notna().sum(),
        p_mixto=d.color_mixto.mean(),
        # geometria (solo descriptiva/control)
        largo_med=d.largo.median(), largo_cv=d.largo.std()/d.largo.mean(),
    ))
f = pd.DataFrame(rows)
f['pref'] = f.kfg.str[:2]
f = f.merge(q2[['kfg','okr','museo','procedencia','region','pc_largo','pc_color','pc_estructura',
                'n_cord_okr','thick_mean','thick_med','thick_cv','thick_sd_rel','thick_n',
                'fib_n','cl_n','cn_n','fib_frac_cl','fib_frac_cod','canuto_frac','twist_n',
                'created_by','created_by_uniq','KHIPU_ID']], on='kfg', how='left')

# pureza (rasgo dominante) por quipu
def pureza(d, col, ok=None):
    s = d[col]
    if ok is not None:
        s = s[ok.reindex(d.index, fill_value=False)]
    s = s.dropna()
    if len(s) == 0: return np.nan, 0
    vc = s.value_counts(normalize=True)
    return vc.iloc[0], len(s)

for col, okcol, nombre in [('torsion','torsion_ok','tors'), ('union','union_ok','union'),
                           ('terminacion','term_ok','term'), ('color_fam',None,'color')]:
    vals = []
    for kfg, d in c.groupby('kfg'):
        ok = d[okcol] if okcol else None
        vals.append((kfg, *pureza(d, col, ok)))
    tmp = pd.DataFrame(vals, columns=['kfg', f'pur_{nombre}', f'n_pur_{nombre}'])
    f = f.merge(tmp, on='kfg', how='left')

# ejes discretos (rasgo dominante por quipu)
f['eje_tors'] = np.select([f.pS_tors>.5, f.pS_tors<.5], ['S','Z'], None).astype(object)
f['eje_ndS'] = np.select([f.pS_nd_simple>.5, f.pS_nd_simple<.5], ['S','Z'], None).astype(object)
f['eje_union'] = np.select([f.pR>.5, f.pR<.5], ['R','V'], None).astype(object)
f['eje_term'] = f[['pK','pB_term','pU_term']].idxmax(axis=1).map({'pK':'K','pB_term':'B','pU_term':'U'})
f.to_csv(os.path.join(AQUI, 'firma_quipu.csv'), index=False)

# cord-level para analisis internos
keep = ['kfg','orden','cuerda','tipo','nivel','padre','grupo','valor','nudos','color','color_fam',
        'color_mixto','torsion','union','largo','terminacion','notas',
        'nd_simple_S','nd_simple_Z','nd_simple_n','nd_largo_S','nd_largo_Z','nd_largo_n',
        'nd_ocho_S','nd_ocho_Z','nd_ocho_n']
c[keep].to_csv(os.path.join(AQUI, 'cuerdas_rasgos.csv'), index=False)

# cord OKR con quipu kfg para fibra/grosor
cord2 = cord.merge(q2[['KHIPU_ID','kfg']], on='KHIPU_ID', how='inner')
cord2.to_csv(os.path.join(AQUI, 'cuerdas_okr.csv'), index=False)

print('quipus', len(f), 'columnas', len(f.columns))
print(f[['n_tors','pS_tors','pur_tors','n_nd_simple','pur_union','pur_term','pur_color']].describe().round(3).to_string())
print('\ncobertura: torsion %d, nudos %d, union %d, term %d, grosor %d, fibra %d' % (
    f.n_tors.gt(0).sum(), f.n_nd_simple.gt(0).sum(), f.n_union.gt(0).sum(),
    f.n_term.gt(0).sum(), f.thick_n.gt(0).sum(), f.fib_n.gt(0).sum()))
