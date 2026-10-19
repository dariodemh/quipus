"""Salidas finales: ficha_nazca.csv con el perfil congelado y las variantes,
resumen por quipu y comparacion de formatos."""
import numpy as np, pandas as pd
from collections import Counter
from scipy.stats import spearmanr
from lib import load, records, canon, prof, corr, OUT, DAT

c = load(); Q = pd.read_csv(DAT / 'quipus.csv')
KS = [('UR1140', 9), ('UR1136', 9), ('UR223', 9), ('HP056', 9), ('UR234', 8), ('UR1131', 10)]

def M_of(k, size):
    return np.array([canon(r['vals'], r['pos'], size=size) for r in records(c, k, size=size)
                     if not np.isnan(r['vals']).any()])

profiles = {}
for k, size in KS:
    M = M_of(k, size); profiles[k] = prof(M)

nf = max(size - 2 for _, size in KS)
rows = []
for pos in range(1, nf + 1):
    row = dict(posicion=pos,
               rol='encabezado' if pos <= 2 else 'cuerpo',
               z_UR1140=profiles['UR1140'][pos - 1] if pos <= 7 else np.nan,
               z_UR1136=profiles['UR1136'][pos - 1] if pos <= 7 else np.nan,
               z_UR223=profiles['UR223'][pos - 1] if pos <= 7 else np.nan,
               z_HP056=profiles['HP056'][pos - 1] if pos <= 7 else np.nan,
               z_UR234=profiles['UR234'][pos - 1] if pos <= 6 else np.nan,
               z_UR1131=profiles['UR1131'][pos - 1] if pos <= 8 else np.nan)
    zs = [row[x] for x in ['z_UR1140', 'z_UR1136', 'z_UR223', 'z_HP056'] if not pd.isna(row[x])]
    row['z_media_4quipus'] = np.mean(zs) if zs else np.nan
    if pos <= 7:
        M4 = np.vstack([M_of(k, 9) for k in ['UR1140', 'UR1136', 'UR223', 'HP056']])
        row['media_cruda_UR1140'] = M_of('UR1140', 9)[:, pos - 1].mean()
        row['frac_max_4quipus'] = np.mean([np.argmax(r) == pos - 1 for r in M4])
        row['frac_max_UR1140'] = np.mean([np.argmax(r) == pos - 1 for r in M_of('UR1140', 9)])
    rows.append(row)
F = pd.DataFrame(rows)
F.to_csv(OUT / 'ficha_nazca.csv', index=False)
print('ficha_nazca.csv'); print(F.round(3).to_string(index=False))

# resumen por quipu
res = []
for k, size in KS:
    R = records(c, k, size=size)
    M = M_of(k, size)
    X = np.log10(M + 1); Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True, ddof=0)
    P = Z.mean(0)
    g = X.mean(); SSpos = len(M) * ((X.mean(0) - g) ** 2).sum(); SStot = ((X - g) ** 2).sum()
    eta = SSpos / SStot
    # rho medio por pares (Spearman entre registros)
    rs = []
    for i in range(len(M)):
        for j in range(i + 1, len(M)):
            rs.append(spearmanr(M[i], M[j]).statistic)
    q = Q[Q.kfg == k].iloc[0]
    res.append(dict(khipu=k, cuerdas_por_grupo=size, campos=size - 2, n_grupos=len(R),
                    n_completos=len(M), max_frac=float(np.mean([np.argmax(r) == 0 for r in M])),
                    c1_c2=float(np.median(M[:, 0] / np.maximum(M[:, 1], 1))),
                    eta2=float(eta), rho_medio=float(np.nanmean(rs)),
                    museo=str(q.museo)[:40], procedencia=q.procedencia))
R = pd.DataFrame(res)
R['r_con_ficha'] = [round(corr(profiles[k], profiles['UR1140']), 3) if (k != 'UR1140' and len(profiles[k]) == 7) else (1.0 if k == 'UR1140' else np.nan) for k in R.khipu]
R.to_csv(OUT / 'resumen_quipus.csv', index=False)
print('\nresumen_quipus.csv'); print(R.round(3).to_string(index=False))

# comparacion de formatos
comp = []
for k in ['UR1140', 'UR1136', 'UR223', 'HP056', 'UR234', 'UR1131']:
    size = dict(KS)[k]; comp.append(dict(formato=k, campos=size - 2, marcadores=2,
                                          perfil=np.round(profiles[k], 2).tolist()))
# Santa
allp = []
for k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    cols = list(d.col); vals = d.v.to_numpy(float); i = 0
    while i <= len(cols) - 6:
        if len(set(cols[i:i + 6])) == 1 and not np.isnan(vals[i:i + 6]).any() and np.ptp(vals[i:i + 6]) > 0:
            allp.append(vals[i:i + 6]); i += 6
        else:
            i += 1
MS = np.array(allp)
comp.append(dict(formato='Santa (6 quipus)', campos=6, marcadores=0,
                 perfil=np.round(prof(MS), 2).tolist()))
# Incahuasi
MI = np.array([gg.v.to_numpy(float) for g, gg in c[(c.kfg == 'UR278') & (c.nivel == 0)].sort_values('orden').groupby('grupo', sort=False)
               if len(gg) == 9 and not gg.v.isna().any()])
comp.append(dict(formato='UR278 Incahuasi', campos=9, marcadores=0,
                 perfil=np.round(prof(MI), 2).tolist()))
pd.DataFrame(comp).to_csv(OUT / 'comparacion_formatos.csv', index=False)
print('\ncomparacion_formatos.csv')
for x in comp:
    print(x['formato'], x['campos'], x['marcadores'], x['perfil'])
