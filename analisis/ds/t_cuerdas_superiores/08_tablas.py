# -*- coding: utf-8 -*-
"""Genera tablas finales: por quipu, por unidad, y las 23 sumas exactas."""
import pandas as pd, numpy as np, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
q = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'quipus.csv'))
g = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'grupos.csv'))
kf = pd.read_csv(os.path.join(ROOT, 'data/external/data-science-khipu-article/data/khipu_summary.csv'))
r = pd.read_csv(os.path.join(BASE, 'unidades_resultados.csv'))

# --- tabla por quipu ---
rows = []
for kfg, d in r.groupby('kfg'):
    meta = q[q.kfg == kfg].iloc[0]
    nT = int(c[(c.kfg == kfg) & (c.union == 'T')].shape[0])
    n0T = int(c[(c.kfg == kfg) & (c.union == 'T') & (c.nivel == 0)].shape[0])
    krow = kf[kf.kfg_name.astype(str) == kfg]
    rows.append(dict(
        kfg=kfg, region=meta['region'], procedencia=str(meta['procedencia'])[:38],
        pc_largo=meta['pc_largo'], pc_color=str(meta['pc_color'])[:28],
        pc_estructura=meta['pc_estructura'], n_grupos=int(g[g.kfg == kfg].shape[0]),
        n_T_total=nT, n_T_nivel0=n0T, n_unidades=len(d),
        n_con_valor=int(d.top_val.notna().sum()), n_blancas=int(d.top_val.isna().sum()),
        n_full_prev=int(d.prev_full_l0.sum()), n_full_next=int(d.next_full_l0.sum()),
        n_full_any=int(d.any_full_l0.sum()),
        exactas='; '.join(d[d.any_full_l0].apply(
            lambda x: f"{x['top']}={x['top_val']:.0f}", axis=1)) if d.any_full_l0.any() else '',
        kfg_num_top=int(krow['num_top_cords'].iloc[0]) if len(krow) else np.nan,
        kfg_num_sum=int(krow['num_top_cord_sum_clusters'].iloc[0]) if len(krow) else np.nan,
    ))
Q = pd.DataFrame(rows).sort_values(['n_full_any', 'kfg'], ascending=[False, True])
Q.to_csv(os.path.join(BASE, 'tabla_quipus.csv'), index=False)
print(Q[['kfg','n_grupos','n_T_total','n_unidades','n_con_valor','n_blancas',
         'n_full_prev','n_full_any','kfg_num_top','kfg_num_sum','exactas']].to_string(index=False))

# --- tabla de las 23 exactas ---
rows = []
for _, u in r[r.any_full_l0 & r.top_val.notna()].iterrows():
    side = 'prev' if u.prev_full_l0 else 'next'
    gr = u.grupo - 1 if side == 'prev' else u.grupo + 1
    gg = c[(c.kfg == u.kfg) & (c.grupo == gr) & (c.nivel == 0)].sort_values('orden')
    rows.append(dict(
        kfg=u.kfg, top=u.top, valor=u.top_val, lado=side,
        n=len(gg), suma=gg['valor'].sum(),
        cuerdas='+'.join(f"{x.cuerda}:{x.valor:g}" for x in gg.itertuples()),
        colores='|'.join(sorted(gg['color'].astype(str).unique())),
        n_colores=gg['color'].nunique(),
        hijos=';'.join(f"{x.cuerda}={x.valor:g}" for x in
                       c[(c.kfg == u.kfg) & (c.padre == u.top)].itertuples() if pd.notna(x.valor)),
    ))
E = pd.DataFrame(rows).sort_values(['kfg', 'top'])
E.to_csv(os.path.join(BASE, 'tabla_exactas.csv'), index=False)
print('\nEXACTAS')
print(E[['kfg','top','valor','lado','n','suma','cuerdas','n_colores']].to_string(index=False, max_colwidth=70))

# --- tabla compacta de todas las unidades ---
T = r[['kfg','top','top_color','top_val','grupo','n_kids','n_kids_T','prev_n','prev_sum',
       'prev_full_l0','next_n','next_sum','next_full_l0','any_full_l0',
       'any_contig_l0','any_color_l0','any_alt_l0']].copy()
T['prev_dif'] = T['top_val'] - T['prev_sum']
T['next_dif'] = T['top_val'] - T['next_sum']
T.columns = ['kfg','cuerda_superior','color_superior','valor','grupo','n_hijos','n_hijos_T',
             'prev_n','prev_suma','prev_exacta','next_n','next_suma','next_exacta',
             'exacta_cualquier_lado','contiguo_l0','color_grupo_completo','alterno_l0','prev_dif','next_dif']
T.to_csv(os.path.join(BASE, 'tabla_todas_unidades.csv'), index=False)
print('\nunidades totales', len(T), 'con valor', T.valor.notna().sum())
