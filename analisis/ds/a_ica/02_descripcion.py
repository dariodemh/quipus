# -*- coding: utf-8 -*-
"""Descripción del conjunto Ica: tabla por quipu (tamaños, estructura, color,
valores, sumas, cuerdas superiores, unión R/V, torsión, dirección de nudos)."""
import pandas as pd, numpy as np, os, re

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
HERE = os.path.dirname(__file__)

sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv'))
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv'))
g = pd.read_csv(os.path.join(DAT, 'grupos.csv'))
summ = pd.read_csv(os.path.join(RAIZ, 'data', 'external', 'data-science-khipu-article',
                                'data', 'khipu_summary.csv'))
sel['kfg'] = sel['kfg'].astype(str)
c['kfg'] = c['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy()

# Nº real de cuerdas con nudo (valor presente)
def nudos_cod(s):
    if pd.isna(s) or str(s).strip() in ('', 'nan'):
        return 0
    return len([x for x in str(s).split(';') if x.strip()])

cc['n_clusters'] = cc['nudos'].map(nudos_cod)
smm = summ.set_index('kfg_name')

rows = []
for kfg, sub in cc.groupby('kfg'):
    pend = sub[sub['nivel'] == 0]
    sub_n = sub[sub['nivel'] > 0]
    grupos = g[g['kfg'] == kfg]
    # colores de colgantes
    col = pend['color'].fillna('?').value_counts()
    # valores presentes
    val = pend.loc[pend['n_clusters'] > 0, 'valor'].dropna()
    total = val.sum() if len(val) else np.nan
    s = smm.loc[kfg] if kfg in smm.index else None
    rows.append(dict(
        kfg=kfg,
        proc=sel.loc[sel['kfg'] == kfg, 'procedencia'].iloc[0],
        n_colg=len(pend), n_subs=len(sub_n), n_grupos=len(grupos),
        max_subs=int(sub['nivel'].max()) if len(sub) else 0,
        color1=col.index[0] if len(col) else '',
        color2=col.index[1] if len(col) > 1 else '',
        frac_color1=round(col.iloc[0] / len(pend), 2) if len(col) else np.nan,
        n_colores=int(pend['color'].nunique()),
        val_min=int(val.min()) if len(val) else 0,
        val_max=int(val.max()) if len(val) else 0,
        val_total=int(total) if len(val) else 0,
        n_top_cords=int(s['num_top_cords']) if s is not None else -1,
        n_top_sum=int(s['num_top_cord_sum_clusters']) if s is not None else -1,
        n_top_dsum=int(s['num_top_cord_double_sum_clusters']) if s is not None else -1,
        r_ratio=round(float(s['r_ratio']), 2) if s is not None else np.nan,
        v_ratio=round(float(s['v_ratio']), 2) if s is not None else np.nan,
        pct_s_knots=round(float(s['percent_s_knots']), 1) if s is not None else np.nan,
        pct_z_knots=round(float(s['percent_z_knots']), 1) if s is not None else np.nan,
        benford=round(float(s['benford_match']), 3) if s is not None else np.nan,
    ))

tab = pd.DataFrame(rows).sort_values('kfg').reset_index(drop=True)
tab.to_csv(os.path.join(HERE, 'tabla_quipus.csv'), index=False)

pd.set_option('display.width', 240)
print(tab.to_string(index=False))
print('\n=== RESUMEN DEL CONJUNTO ===')
print('quipus:', len(tab), ' cuerdas:', len(cc), ' colgantes:', int(tab.n_colg.sum()),
      ' subsidiarias:', int(tab.n_subs.sum()), ' grupos:', int(tab.n_grupos.sum()))
print('colgantes por quipu: mediana %.1f  min %d  max %d' %
      (tab.n_colg.median(), tab.n_colg.min(), tab.n_colg.max()))
print('colores: nº colores distintos por quipu mediana %.1f' % tab.n_colores.median())
print('color dominante global:', pend_all := cc[(cc.nivel == 0)]['color'].value_counts().head(12).to_dict())
print('unión global:', cc['union'].value_counts().to_dict())
print('torsión global:', cc['torsion'].value_counts().to_dict())
print('con top cords (>0):', int((tab.n_top_cords > 0).sum()),
      '| con suma de top cords:', int((tab.n_top_sum > 0).sum()),
      '| con doble suma top:', int((tab.n_top_dsum > 0).sum()))
print('R>V quipus:', int((tab.r_ratio > 0.5).sum()), 'V>R quipus:', int((tab.v_ratio > 0.5).sum()))
