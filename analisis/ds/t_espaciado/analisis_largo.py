"""¿El largo de las cuerdas se relaciona con el valor o con el color DENTRO del quipu?

Controles: permutaciones dentro de quipu (y dentro de grupo para color),
residualización de log(largo) respecto de nº de racimos y nivel, semilla fija.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
c = c[c.tiene_nudos & (c.largo > 0) & c.valor.notna()].copy()
c['loglargo'] = np.log(c.largo)

SEED = 20261017
NPERM = 2000
rng_global = np.random.default_rng(SEED)


def rankdata(x):
    return stats.rankdata(x)


def fast_rho(xr, yr):
    """Pearson sobre rangos ya centrados."""
    return float(np.dot(xr, yr) / (np.linalg.norm(xr) * np.linalg.norm(yr) + 1e-12))


def within_quipu_rho(df, xcol, ycol, min_n=8, nperm=NPERM, seed=SEED):
    """Correlación de Spearman dentro de cada quipu + nulo permutando x dentro de quipu."""
    grupos = []
    for k, d in df.groupby('kfg'):
        d = d.dropna(subset=[xcol, ycol])
        if len(d) < min_n or d[xcol].nunique() < 4 or d[ycol].nunique() < 4:
            continue
        xr = rankdata(d[xcol].values); xr -= xr.mean()
        yr = rankdata(d[ycol].values); yr -= yr.mean()
        grupos.append((xr, yr))
    obs = np.mean([fast_rho(x, y) for x, y in grupos])
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for b in range(nperm):
        s = 0.0
        for x, y in grupos:
            s += fast_rho(rng.permutation(x), y)
        null[b] = s / len(grupos)
    p1 = (1 + np.sum(null >= obs)) / (nperm + 1)   # una cola: positivo
    p2 = (1 + np.sum(np.abs(null) >= abs(obs))) / (nperm + 1)
    return dict(n_quipus=len(grupos), obs=obs, null_mean=null.mean(),
                null_sd=null.std(), p_una_cola=p1, p_dos_colas=p2,
                frac_pos=np.mean([fast_rho(x, y) > 0 for x, y in grupos]))


def within_unit_rho(df, xcol, ycol, unitcols, min_n=5, nperm=NPERM, seed=SEED):
    """Spearman dentro de cada unidad (quipu o grupo), nulo permutando x en la unidad."""
    grupos = []
    for key, d in df.groupby(unitcols):
        d = d.dropna(subset=[xcol, ycol])
        if len(d) < min_n or d[xcol].nunique() < 4 or d[ycol].nunique() < 4:
            continue
        xr = rankdata(d[xcol].values); xr -= xr.mean()
        yr = rankdata(d[ycol].values); yr -= yr.mean()
        grupos.append((xr, yr))
    if not grupos:
        return None
    obs = np.mean([fast_rho(x, y) for x, y in grupos])
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for b in range(nperm):
        s = 0.0
        for x, y in grupos:
            s += fast_rho(rng.permutation(x), y)
        null[b] = s / len(grupos)
    p1 = (1 + np.sum(null >= obs)) / (nperm + 1)
    p2 = (1 + np.sum(np.abs(null) >= abs(obs))) / (nperm + 1)
    return dict(n_unidades=len(grupos), obs=obs, null_mean=null.mean(),
                null_sd=null.std(), p_una_cola=p1, p_dos_colas=p2,
                frac_pos=np.mean([fast_rho(x, y) > 0 for x, y in grupos]))


def residualizar_largo(df):
    """log(largo) residual tras quipu (efectos fijos) + dummies de n_clusters y nivel."""
    d = df.copy()
    d['ncl'] = d.n_clusters.clip(upper=6)
    d['niv'] = d.nivel.clip(upper=2)
    X = pd.concat([pd.get_dummies(d.ncl, prefix='ncl', drop_first=True),
                   pd.get_dummies(d.niv, prefix='niv', drop_first=True)], axis=1).astype(float)
    y = d.loglargo.values.astype(float)
    # demeaning por quipu (efectos fijos)
    ymat = pd.DataFrame({'y': y, 'kfg': d.kfg.values})
    y_dm = y - ymat.groupby('kfg').y.transform('mean').values
    Xm = X.copy(); Xm['kfg'] = d.kfg.values
    X_dm = X - Xm.groupby('kfg').transform('mean').values
    beta, *_ = np.linalg.lstsq(X_dm.values, y_dm, rcond=None)
    d['largo_resid'] = y_dm - X_dm.values @ beta
    return d


print('=== 0. muestra ===')
print('cuerdas con nudos, largo>0:', len(c), '| quipus:', c.kfg.nunique())
print('quipus con >=8 cuerdas y >=4 valores:', c.groupby('kfg').filter(lambda d: len(d) >= 8 and d.valor.nunique() >= 4).kfg.nunique())

# ---------------- 1. LARGO vs VALOR ----------------
print('\n=== 1. largo vs valor (dentro de quipu) ===')
r_raw = within_quipu_rho(c, 'largo', 'valor')
print('Spearman largo~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r_raw.items()})

c = residualizar_largo(c)
r_res = within_quipu_rho(c, 'largo_resid', 'valor')
print('Spearman largo_resid~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r_res.items()})

c['logcola'] = np.log(c.cola.clip(lower=0.05))
r_cola = within_quipu_rho(c, 'logcola', 'valor')
print('Spearman cola~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r_cola.items()})

# control físico esperado: largo vs nº de racimos
r_ncl = within_quipu_rho(c, 'largo', 'n_clusters')
print('Spearman largo~n_clusters (control físico):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r_ncl.items()})

# solo colgantes (nivel 0), para quitar el efecto del nivel
c0 = c[c.nivel == 0]
r0 = within_quipu_rho(c0, 'largo', 'valor')
print('solo nivel 0, Spearman largo~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r0.items()})
r0r = within_quipu_rho(c0, 'largo_resid', 'valor')
print('solo nivel 0, Spearman largo_resid~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r0r.items()})

# mismo número de racimos (evita el artefacto de partialling)
same_ncl = within_unit_rho(c, 'largo', 'valor', ['kfg', 'n_clusters'], min_n=5, nperm=1000)
print('mismo n_clusters, Spearman largo~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in same_ncl.items()})
same_ncl_cola = within_unit_rho(c, 'cola', 'valor', ['kfg', 'n_clusters'], min_n=5, nperm=1000)
print('mismo n_clusters, Spearman cola~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in same_ncl_cola.items()})
same_grupo = within_unit_rho(c, 'largo', 'valor', ['kfg', 'grupo'], min_n=5, nperm=1000)
print('mismo grupo, Spearman largo~valor:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in same_grupo.items()})

# confusión entre quipus: medias por quipu
qm = c.groupby('kfg').agg(ml=('loglargo', 'mean'), mv=('logvalor', 'mean'),
                          nc=('n_clusters', 'mean'))
qm = qm[qm.index.isin(c.groupby('kfg').size()[lambda s: s >= 8].index)]
print('entre quipus: Spearman media loglargo ~ media logvalor:',
      round(stats.spearmanr(qm.ml, qm.mv).statistic, 3), '| n=', len(qm))
print('entre quipus: Spearman media loglargo ~ media n_clusters:',
      round(stats.spearmanr(qm.ml, qm.nc).statistic, 3))

# ---------------- 2. LARGO vs COLOR ----------------
print('\n=== 2. largo vs color ===')


def epsilon2_kw(y, labels, min_por_color=2, min_n=6):
    """epsilon² de Kruskal-Wallis; devuelve nan si no hay 2 colores con >=2 cuerdas."""
    n = len(y)
    if n < min_n:
        return np.nan
    cats, inv, cnt = np.unique(labels, return_inverse=True, return_counts=True)
    if len(cats) < 2 or cnt.min() < min_por_color:
        return np.nan
    r = stats.rankdata(y)
    mr = np.bincount(inv, weights=r) / cnt
    H = 12.0 / (n * (n + 1)) * np.sum(cnt * (mr - (n + 1) / 2.0) ** 2)
    k = len(cats)
    return (H - k + 1) / (n - k)


def perm_color(df, ycol, groupcols, nperm=1000, seed=SEED, min_n=6, min_por_color=2):
    """epsilon² medio por unidad (quipu o grupo) + nulo permutando color dentro de la unidad."""
    unidades = []
    for key, d in df.groupby(groupcols):
        d = d.dropna(subset=[ycol, 'color_simple'])
        y = d[ycol].values.astype(float)
        lab = d.color_simple.values
        e = epsilon2_kw(y, lab, min_por_color, min_n)
        if np.isfinite(e):
            unidades.append((y, lab, len(np.unique(lab))))
    if not unidades:
        return None
    obs = np.mean([epsilon2_kw(y, lab, min_por_color, min_n) for y, lab, _ in unidades])
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for b in range(nperm):
        s = 0.0
        for y, lab, _ in unidades:
            s += epsilon2_kw(y, rng.permutation(lab), min_por_color, min_n)
        null[b] = s / len(unidades)
    p = (1 + np.sum(null >= obs)) / (nperm + 1)
    return dict(n_unidades=len(unidades), obs=obs, null_mean=null.mean(),
                null_sd=null.std(), p=p)


color = c[c.color_simple.notna() & (c.color_simple != 'MIX')].copy()
print('cuerdas con color simple:', len(color), '| quipus:', color.kfg.nunique())
col_q = perm_color(color, 'loglargo', ['kfg'], nperm=1000)
print('color~largo, unidades=quipu:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_q.items()})
col_q0 = perm_color(color[color.nivel == 0], 'loglargo', ['kfg'], nperm=1000)
print('color~largo, nivel 0, unidades=quipu:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_q0.items()})
col_qr = perm_color(color, 'largo_resid', ['kfg'], nperm=1000)
print('color~largo_resid, unidades=quipu:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_qr.items()})
col_g = perm_color(color, 'loglargo', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~largo, unidades=grupo (control layout):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_g.items()})
col_g0 = perm_color(color[color.nivel == 0], 'loglargo', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~largo, nivel 0, unidades=grupo:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_g0.items()})
col_gr = perm_color(color, 'largo_resid', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~largo_resid, unidades=grupo (controla n_clusters y nivel):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_gr.items()})
col_ncl = perm_color(color, 'n_clusters', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~n_clusters, unidades=grupo:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_ncl.items()})

# control positivo: color~valor (se sabe que el color codifica categorías)
col_val = perm_color(color, 'logvalor', ['kfg'], nperm=1000)
print('color~valor (control positivo), unidades=quipu:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_val.items()})
col_val_g = perm_color(color, 'logvalor', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~valor, unidades=grupo:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_val_g.items()})

# descriptivo: diferencia W vs no-W dentro de quipu
w = color.groupby('kfg').apply(
    lambda d: (np.log(d[d.color_simple == 'W'].largo).mean() - np.log(d[d.color_simple != 'W'].largo).mean())
    if (d.color_simple == 'W').sum() >= 3 and (d.color_simple != 'W').sum() >= 3 else np.nan,
    include_groups=False).dropna()
print('log largo W - no W dentro de quipu: media', round(w.mean(), 3), '| n quipus', len(w),
      '| % W mas largas', round((w > 0).mean(), 3), '| Wilcoxon p', f'{stats.wilcoxon(w).pvalue:.3g}')

# entre quipus (confusión): mediana de largo por color a nivel global
print('\nmediana de largo por color (global, sin control):')
vc = color.color_simple.value_counts()
print(color[color.color_simple.isin(vc[vc >= 300].index)].groupby('color_simple').agg(
    n=('largo', 'size'), mediana=('largo', 'median')).round(1).sort_values('mediana').to_string())

# ¿qué colores sostienen el efecto? desviación de la media del quipu
color['loglargo_c'] = color.loglargo - color.groupby('kfg').loglargo.transform('mean')
diag = color[color.color_simple.isin(vc[vc >= 200].index)].groupby('color_simple').agg(
    n=('loglargo_c', 'size'), quipus=('kfg', 'nunique'), desv=('loglargo_c', 'mean'))
print('\ndesviación media de log largo respecto de la media del quipu:')
print(diag.round(3).sort_values('desv').to_string())
# sin colores raros (presentes en <5 quipus)
raros = diag[diag.quipus < 5].index.tolist()
print('colores raros excluidos:', raros)
color2 = color[~color.color_simple.isin(raros)]
col_g2 = perm_color(color2, 'loglargo', ['kfg', 'grupo'], nperm=1000, min_n=5)
print('color~largo, unidades=grupo, sin colores raros:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_g2.items()})
col_q2 = perm_color(color2, 'loglargo', ['kfg'], nperm=1000)
print('color~largo, unidades=quipu, sin colores raros:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in col_q2.items()})

# guardar tabla de p-values para corrección Holm
pv = {
    'largo~valor': r_raw['p_dos_colas'],
    'mismo_ncl~valor': same_ncl['p_dos_colas'],
    'mismo_grupo~valor': same_grupo['p_dos_colas'],
    'cola_mismo_ncl~valor': same_ncl_cola['p_dos_colas'],
    'color~largo_quipu': col_q['p'],
    'color~largo_grupo': col_g['p'],
    'color~largo_grupo_nivel0': col_g0['p'],
    'color~largo_resid_grupo': col_gr['p'],
    'color~nclusters_grupo': col_ncl['p'],
    'color~valor_quipu': col_val['p'],
    'color~valor_grupo': col_val_g['p'],
}
pd.Series(pv, name='p').to_csv(os.path.join(BASE, 'pvalues_largo.csv'))
print('\np-values guardados:', {k: f'{v:.2e}' for k, v in pv.items()})
