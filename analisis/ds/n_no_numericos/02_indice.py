"""Indice de anomalia decimal v2: violaciones bien separadas.
Escribe clusters.csv, cuerdas_anom.csv, quipus_indice.csv
"""
import pandas as pd, numpy as np, re

C = pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv', dtype={'nudos': str, 'color': str, 'notas': str})
Q = pd.read_csv('analisis/datos/quipus.csv')
pat = re.compile(r'^(\d+)([A-Z?]+)\(([\d.]+),([SZU?])\)(?:,([\d.]+))?$')
rows = []
for r in C.itertuples():
    s = r.nudos
    if not isinstance(s, str) or not s.strip(): continue
    for k, seg in enumerate(s.split(';')):
        seg = seg.strip()
        if not seg: continue
        m = pat.match(seg)
        if not m: continue
        n, t, pos, d, v = m.groups()
        rows.append((r.kfg, r.cuerda, int(k), int(n), t, float(pos), d,
                     float(v) if v is not None else np.nan))
K = pd.DataFrame(rows, columns=['kfg','cuerda','k','n','tipo','pos','dir','val'])
K['units_type'] = K.tipo.isin(['L','LL','E','EE']) & (K.val.fillna(99) < 10)

def expo(t, v):
    if pd.isna(v) or v <= 0: return np.nan
    iv = int(round(v))
    return len(str(iv)) - len(str(iv).rstrip('0'))
K['exp'] = [expo(t, v) for t, v in zip(K.tipo, K.val)]
K['isl'] = K.groupby(['kfg','cuerda'])['k'].transform('max') == K.k
# exponente del racimo siguiente (mas abajo)
K['exp_next'] = K.groupby(['kfg','cuerda'])['exp'].shift(-1)
K['nclust_cord'] = K.groupby(['kfg','cuerda'])['k'].transform('max') + 1

K['v_S_unit']  = (K.tipo=='S') & (K.val.fillna(99) % 10 != 0)
K['v_E_out']   = (K.tipo.isin(['E','EE'])) & (K.val.fillna(1) > 1)
K['v_L_above'] = (K.tipo.isin(['L','LL'])) & (~K['isl']) & (K.exp_next.fillna(0) > 0)
K['v_order']   = (K.exp_next.fillna(K.exp) > K.exp) & K.exp.notna()
K['dup_unit']  = (K.exp==0) & (K.groupby(['kfg','cuerda','exp'])['k'].transform('size')>1)
K['dup_hi']    = (K.exp>0)  & (K.groupby(['kfg','cuerda','exp'])['k'].transform('size')>1)

K['anom'] = K[['v_S_unit','v_E_out','v_L_above','v_order','dup_unit','dup_hi']].any(axis=1)
K['nanom_flags'] = K[['v_S_unit','v_E_out','v_L_above','v_order','dup_unit','dup_hi']].sum(axis=1)

cord = K.groupby(['kfg','cuerda']).agg(nclust=('k','size'), nanom=('anom','sum'),
    vS=('v_S_unit','sum'), vE=('v_E_out','sum'), vLab=('v_L_above','sum'),
    vord=('v_order','sum'), dupu=('dup_unit','sum'), duph=('dup_hi','sum')).reset_index()
cord = C[['kfg','cuerda','nivel','padre','color','torsion','union','largo','terminacion','valor','grupo']].merge(
    cord, on=['kfg','cuerda'], how='left')
for c in ['nclust','nanom','vS','vE','vLab','vord','dupu','duph']: cord[c]=cord[c].fillna(0)
cord['knotless'] = cord.nclust==0
cord['color'] = cord.color.fillna('')
cord['color_comp'] = cord.color.str.count(r'[:\-/]') + 1
cord['rich_color'] = cord.color_comp>=2
cord['has_child'] = cord.cuerda.isin(cord.padre.dropna())
cord['impossible_zero'] = (~cord.knotless) & (cord.valor==0)
cord.to_csv('analisis/ds/n_no_numericos/cuerdas_anom.csv', index=False)
K.to_csv('analisis/ds/n_no_numericos/clusters.csv', index=False)

def qsum(d):
    n=len(d); nk=(~d.knotless).sum(); ncl=d.nclust.sum()
    return pd.Series(dict(ncuerdas=n, ncuerdas_nudo=nk, nclusters=ncl,
        frac_sin_nudo=1-nk/n if n else np.nan,
        nanom=d.nanom.sum(), rate_anom=d.nanom.sum()/max(ncl,1),
        vS=d.vS.sum(), vE=d.vE.sum(), vLab=d.vLab.sum(), vord=d.vord.sum(),
        dupu=d.dupu.sum(), duph=d.duph.sum(),
        frac_dup_cords=((d.dupu+d.duph)>0).sum()/max(nk,1),
        n_sin_nudo_rico=((d.knotless)&(d.rich_color)).sum(),
        frac_rico_sin_nudo=((d.knotless)&(d.rich_color)).sum()/max((d.knotless).sum(),1),
        n_imposible=d.impossible_zero.sum(),
        n_color=len(set(d.color[d.color!=''])), frac_rico=(d.color_comp>=2).mean(),
        n_subs=(d.nivel>0).sum(), frac_subs=(d.nivel>0).mean(),
        n_top=(d.union=='T').sum()))
QI = cord.groupby('kfg').apply(qsum, include_groups=False).reset_index().merge(Q, on='kfg', how='left')
QI.to_csv('analisis/ds/n_no_numericos/quipus_indice.csv', index=False)

print('clusters', len(K), 'anom rate', round(K.anom.mean(),4))
print(K.groupby('tipo')[['v_S_unit','v_E_out','v_L_above','v_order','dup_unit','dup_hi']].mean().round(3).to_string())
s=QI[QI.ncuerdas_nudo>=10]
print('\nDistribucion rate_anom (>=10 cuerdas con nudo, n=%d)'%len(s))
print(s[['rate_anom','frac_dup_cords','vord','vLab','vS','vE']].describe().round(3).to_string())
print('\nTop 30 rate_anom:')
t=QI[QI.ncuerdas_nudo>=10].sort_values('rate_anom',ascending=False).head(30)
print(t[['kfg','ncuerdas','ncuerdas_nudo','nclusters','rate_anom','vS','vE','vLab','vord','dupu','duph','procedencia']].to_string(index=False))
print('\nmediana rate por prefijo')
QI['pref']=QI.kfg.str.extract(r'^([A-Z]+)')
print(QI.groupby('pref').rate_anom.agg(['size','median','mean']).round(3).to_string())
