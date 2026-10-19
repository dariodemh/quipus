# -*- coding: utf-8 -*-
"""
Dualidad / mitades en los quipus del KFG.

Unidad de analisis: el quipu.  Nulo: permutacion de los valores (o etiquetas)
DENTRO de cada quipu, preservando el patron de datos faltantes y el tamano de
cada mitad.  B=2000 permutaciones, semilla fija.

Salidas: resultados.json, por_quipu.csv
"""
import json, re, warnings
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')
RUTA = 'analisis/datos/'
SEMILLA = 20261018
B = 2000
rng = np.random.default_rng(SEMILLA)

# ------------------------------------------------------------------ datos
C = pd.read_csv(RUTA + 'cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)      # valor solo si hay nudos
C['grupo_n'] = pd.to_numeric(C['grupo'], errors='coerce')
C = C.sort_values(['kfg', 'orden'], kind='mergesort')

def primera_dir(s):
    if not isinstance(s, str):
        return None
    d = re.findall(r',([SZU])\)', s)
    return d[0] if d else None

def dir_mayor(s):
    if not isinstance(s, str):
        return None
    d = [x for x in re.findall(r',([SZU])\)', s) if x in 'SZ']
    if not d:
        return None
    return 'S' if d.count('S') > d.count('Z') else ('Z' if d.count('Z') > d.count('S') else d[0])

def color_coarse(s):
    if not isinstance(s, str) or not s.strip():
        return None
    s = s.strip().upper().replace(' ', '').split('(')[0]
    for sep in (':', '/', '-', '_'):
        if sep in s:
            s = s.split(sep)[0]
            break
    return s if s else None

def color_exacto(s):
    if not isinstance(s, str) or not s.strip():
        return None
    return s.strip().upper().replace(' ', '').split('(')[0]

C['kd'] = C['nudos'].apply(primera_dir)
C['kd_may'] = C['nudos'].apply(dir_mayor)
C['col_c'] = C['color'].apply(color_coarse)
C['col_e'] = C['color'].apply(color_exacto)
C['uni'] = C['union'].where(C['union'].isin(['R', 'V']))
C['tor'] = C['torsion'].where(C['torsion'].isin(['S', 'Z']))

P = C[C['nivel'] == 0].copy()          # pendantes, en orden fisico
P['pos'] = P.groupby('kfg').cumcount()  # 0..n-1 dentro del quipu

# ------------------------------------------------------------- utilidades
def etiquetas_mitades(n):
    """0 = primera mitad, 1 = segunda mitad, -1 = cordel central (n impar)."""
    m = n // 2
    lab = np.full(n, -1, dtype=int)
    lab[:m] = 0
    lab[n - m:] = 1
    return lab, m

def perm_indices(N, B, rng):
    """B permutaciones de range(N) (matriz B x N)."""
    return np.argsort(rng.random((B, N)), axis=1)

def resumen(obs, null, lado, nombre, n_quipus, extra=None):
    obs = np.asarray(obs, float)
    null = np.asarray(null, float)
    with np.errstate(invalid='ignore'):
        agg = np.nanmean(null, axis=0)
        o = np.nanmean(obs)
        mu, sd = np.nanmean(agg), np.nanstd(agg)
        if lado == 'lower':
            pl = (1 + np.sum(agg <= o)) / (B + 1); pu = (1 + np.sum(agg >= o)) / (B + 1)
            p = pl
        elif lado == 'upper':
            pl = (1 + np.sum(agg <= o)) / (B + 1); pu = (1 + np.sum(agg >= o)) / (B + 1)
            p = pu
        else:
            pl = (1 + np.sum(agg <= o)) / (B + 1)
            pu = (1 + np.sum(agg >= o)) / (B + 1)
            p = min(1.0, 2 * min(pl, pu))
        z = (o - mu) / sd if sd > 0 else np.nan
    d = dict(test=nombre, n_quipus=int(n_quipus), obs=float(o), null_mean=float(mu),
             null_sd=float(sd), z=float(z), p=float(p), p_lower=float(pl), p_upper=float(pu),
             p_doscolas=float(min(1.0, 2 * min(pl, pu))), lado=lado)
    if extra:
        d.update(extra)
    # cola del 5% por quipu (heterogeneidad)
    with np.errstate(invalid='ignore'):
        if lado == 'lower':
            q = np.nanpercentile(null, 5, axis=1)
            ex = np.nanmean(obs <= q)
        elif lado == 'upper':
            q = np.nanpercentile(null, 95, axis=1)
            ex = np.nanmean(obs >= q)
        else:
            med = np.nanmedian(null, axis=1)
            dev = np.abs(null - med[:, None])
            q = np.nanpercentile(dev, 95, axis=1)
            ex = np.nanmean(np.abs(obs - med) >= q)
    d['frac_quipus_cola5'] = float(ex)
    n = len(obs)
    d['binom_p_cola5'] = float(stats.binomtest(int(round(ex * n)), n, 0.05,
                                               alternative='greater').pvalue)
    return d

# =====================================================================
# 1. SIMETRIA DE SUMAS ENTRE MITADES (primera vs segunda)
# =====================================================================
sum_obs, sum_null = [], []
eq_obs, eq_null = [], []
rat_obs, rat_null = [], []
trend_obs, trend_null = [], []
meta_sum = []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    lab, m = etiquetas_mitades(n)
    use = (lab >= 0) & q['vk'].notna().values
    if use.sum() < 4:
        continue
    v = q['vk'].values[use]
    l = lab[use]
    if l.min() == l.max():
        continue
    s1, s2 = v[l == 0].sum(), v[l == 1].sum()
    if s1 <= 0 or s2 <= 0:
        continue
    m1 = int((l == 0).sum())
    N = len(v)
    idx = perm_indices(N, B, rng)
    vp = v[idx]
    s1n = vp[:, :m1].sum(1)
    s2n = vp[:, m1:].sum(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        d = np.abs(np.log(s1 / s2))
        dn = np.abs(np.log(s1n / s2n))
    sum_obs.append(d); sum_null.append(dn)
    e = float(s1 == s2); en = (s1n == s2n).astype(float)
    eq_obs.append(e); eq_null.append(en)
    def cerca(r):
        return (np.minimum(np.abs(r - 2), np.abs(r - 0.5)) < 0.04) | \
               (np.minimum(np.abs(r - 3), np.abs(r - 1 / 3)) < 0.06)
    with np.errstate(divide='ignore', invalid='ignore'):
        rat_obs.append(float(cerca(np.array([s1 / s2]))[0]))
        rat_null.append(cerca(s1n / s2n).astype(float))
    # tendencia monotonica del valor con la posicion (explicacion aburrida)
    pos = np.arange(N)
    if np.std(v) > 0:
        rv = stats.rankdata(v)
        rp = stats.rankdata(pos)
        zp = (rp - rp.mean()) / rp.std()
        zv = (rv - rv.mean()) / rv.std()
        rho = float(np.mean(zp * zv))
        rhon = (zv[idx] @ zp) / N
    else:
        rho, rhon = np.nan, np.full(B, np.nan)
    trend_obs.append(rho); trend_null.append(rhon)
    meta_sum.append((k, n, s1, s2, float(d)))

sum_obs = np.array(sum_obs); sum_null = np.array(sum_null)
eq_obs = np.array(eq_obs); eq_null = np.array(eq_null)
rat_obs = np.array(rat_obs); rat_null = np.array(rat_null)
trend_obs = np.array(trend_obs); trend_null = np.array(trend_null)
NSUM = len(sum_obs)

res_sum = resumen(sum_obs, sum_null, 'lower', 'suma_mitades_simetria', NSUM,
                  {'descripcion': 'media de |log(s1/s2)|; menor = mas simetria',
                   'mediana_obs': float(np.nanmedian(sum_obs))})
res_eq = resumen(eq_obs, eq_null, 'upper', 'suma_mitades_igualdad_exacta', NSUM,
                 {'descripcion': 'proporcion de quipus con s1==s2'})
res_rat = resumen(rat_obs, rat_null, 'upper', 'suma_mitades_razon_fija_2o3', NSUM,
                  {'descripcion': 'proporcion con razon ~2:1 o ~3:1 (tol. 2-6%)'})
res_trend = resumen(trend_obs, trend_null, 'two', 'tendencia_valor_posicion', NSUM,
                    {'descripcion': 'media de rho de Spearman valor~posicion'})

# =====================================================================
# 2. ESPEJO DE VALORES Y COLORES EN POSICIONES
# =====================================================================
def test_match(col, nombre, lado='upper'):
    obs, null, obs_par, null_par = [], [], [], []
    for k, q in P.groupby('kfg', sort=False):
        n = len(q)
        if n < 6:
            continue
        m = n // 2
        prim = list(range(m))
        seg = list(range(n - m, n))
        pares = [(prim[i], seg[m - 1 - i]) for i in range(m)]
        pares_par = [(prim[i], seg[i]) for i in range(m)]
        vals = q[col].values
        presente = np.array([not pd.isna(x) for x in vals])
        posiciones = [p for p in prim + seg if presente[p]]
        if len(posiciones) < 4:
            continue
        mapa = {p: i for i, p in enumerate(posiciones)}
        vv = np.array([vals[p] for p in posiciones])
        def pares_validos(pp):
            a = [mapa[p] for p, qq in pp if p in mapa and qq in mapa]
            b = [mapa[qq] for p, qq in pp if p in mapa and qq in mapa]
            return np.array(a, int), np.array(b, int)
        ia, ib = pares_validos(pares)
        ja, jb = pares_validos(pares_par)
        if len(ia) < 3:
            continue
        idx = perm_indices(len(vv), B, rng)
        vp = vv[idx]
        o = np.mean(vv[ia] == vv[ib])
        on = np.mean(vp[:, ia] == vp[:, ib], axis=1)
        op = np.mean(vv[ja] == vv[jb])
        opn = np.mean(vp[:, ja] == vp[:, jb], axis=1)
        obs.append(o); null.append(on)
        obs_par.append(op); null_par.append(opn)
    if not obs:
        return None, None
    r = resumen(np.array(obs), np.array(null), lado, nombre, len(obs),
                {'descripcion': 'tasa de coincidencia en posiciones espejo'})
    rp = resumen(np.array(obs_par), np.array(null_par), lado, nombre + '_paralelo', len(obs_par),
                 {'descripcion': 'tasa de coincidencia en posiciones paralelas (control)'})
    return r, rp

res_vmir, res_vpar = test_match('vk', 'valores_espejo')
res_cmir, res_cpar = test_match('col_c', 'color_coarse_espejo')
res_cemir, res_cepar = test_match('col_e', 'color_exacto_espejo')

# =====================================================================
# 3. DIRECCION DE NUDO S/Z ENTRE MITADES Y SEGREGACION ESPACIAL
# =====================================================================
kd_obs, kd_null = [], []
kdr_obs, kdr_null = [], []
kdv_obs, kdv_null = [], []
meta_kd = []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    d = q['kd_may'].values
    ok = np.array([x in ('S', 'Z') for x in d])
    if ok.sum() < 4:
        continue
    lab, m = etiquetas_mitades(n)
    l = lab[ok]; x = d[ok]
    if (l == 0).sum() < 1 or (l == 1).sum() < 1:
        continue
    p1 = np.mean(x[l == 0] == 'S'); p2 = np.mean(x[l == 1] == 'S')
    N = len(x); m1 = int((l == 0).sum())
    idx = perm_indices(N, B, rng); xp = x[idx]
    dn = np.mean(xp[:, :m1] == 'S', axis=1) - np.mean(xp[:, m1:] == 'S', axis=1)
    kd_obs.append(p1 - p2); kd_null.append(dn)
    tr = np.sum(x[1:] != x[:-1])
    trn = np.sum(xp[:, 1:] != xp[:, :-1], axis=1)
    kdr_obs.append(tr); kdr_null.append(trn)
    v = q['vk'].values[ok]
    okv = ~np.isnan(v)
    if okv.sum() >= 4 and len(set(x[okv])) == 2:
        lv = np.log1p(v[okv]); xv = x[okv]
        sv = xv == 'S'
        dif = np.mean(lv[sv]) - np.mean(lv[~sv])
        idxv = perm_indices(len(lv), B, rng)
        lvp = lv[idxv]
        difn = np.mean(lvp[:, sv], axis=1) - np.mean(lvp[:, ~sv], axis=1)
        kdv_obs.append(dif); kdv_null.append(difn)
    meta_kd.append((k, n, float(p1), float(p2)))

res_kd = resumen(np.array(kd_obs), np.array(kd_null), 'two', 'direccion_nudo_mitades', len(kd_obs),
                 {'descripcion': 'media pS(1a mitad)-pS(2a mitad); >0 = S en la primera mitad'})
res_kdr = resumen(np.array(kdr_obs), np.array(kdr_null), 'two', 'direccion_nudo_rachas', len(kdr_obs),
                  {'descripcion': 'transiciones S<->Z; menos = segregacion espacial'})
res_kdv = resumen(np.array(kdv_obs), np.array(kdv_null), 'two', 'direccion_nudo_valor', len(kdv_obs),
                  {'descripcion': 'media log(1+v) S - Z'})

# =====================================================================
# 4. UNION R/V: MITADES, RACHAS, VALOR Y ALTERNANCIA POR GRUPO
# =====================================================================
u_obs, u_null, ur_obs, ur_null = [], [], [], []
uv_obs, uv_null = [], []
meta_u = []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    u = q['uni'].values
    ok = np.array([x in ('R', 'V') for x in u])
    if ok.sum() < 4:
        continue
    lab, m = etiquetas_mitades(n)
    l = lab[ok]; x = u[ok]
    if (l == 0).sum() < 1 or (l == 1).sum() < 1:
        continue
    p1 = np.mean(x[l == 0] == 'R'); p2 = np.mean(x[l == 1] == 'R')
    N = len(x); m1 = int((l == 0).sum())
    idx = perm_indices(N, B, rng); xp = x[idx]
    dn = np.mean(xp[:, :m1] == 'R', axis=1) - np.mean(xp[:, m1:] == 'R', axis=1)
    u_obs.append(p1 - p2); u_null.append(dn)
    tr = np.sum(x[1:] != x[:-1]); trn = np.sum(xp[:, 1:] != xp[:, :-1], axis=1)
    ur_obs.append(tr); ur_null.append(trn)
    v = q['vk'].values[ok]; okv = ~np.isnan(v)
    if okv.sum() >= 4 and len(set(x[okv])) == 2:
        lv = np.log1p(v[okv]); xv = x[okv]
        sr = xv == 'R'
        dif = np.mean(lv[sr]) - np.mean(lv[~sr])
        idxv = perm_indices(len(lv), B, rng); lvp = lv[idxv]
        difn = np.mean(lvp[:, sr], axis=1) - np.mean(lvp[:, ~sr], axis=1)
        uv_obs.append(dif); uv_null.append(difn)
    meta_u.append((k, n, float(p1), float(p2)))

res_u = resumen(np.array(u_obs), np.array(u_null), 'two', 'union_RV_mitades', len(u_obs),
                {'descripcion': 'media pR(1a)-pR(2a)'})
res_ur = resumen(np.array(ur_obs), np.array(ur_null), 'two', 'union_RV_rachas', len(ur_obs),
                 {'descripcion': 'transiciones R<->V; menos = bloques, mas = alternancia'})
res_uv = resumen(np.array(uv_obs), np.array(uv_null), 'two', 'union_RV_valor', len(uv_obs),
                 {'descripcion': 'media log(1+v) R - V'})

gr_obs, gr_null = [], []
for k, q in P.groupby('kfg', sort=False):
    maj = []
    for g, qq in q.groupby('grupo_n', sort=True):
        x = qq['uni'].dropna().values
        if len(x) >= 2 and len(set(x)) == 2:
            maj.append('R' if x.tolist().count('R') > x.tolist().count('V') else 'V')
    if len(maj) < 4 or len(set(maj)) < 2:
        continue
    x = np.array(maj)
    tr = np.sum(x[1:] != x[:-1])
    idx = perm_indices(len(x), B, rng); xp = x[idx]
    trn = np.sum(xp[:, 1:] != xp[:, :-1], axis=1)
    gr_obs.append(tr); gr_null.append(trn)
res_gr = resumen(np.array(gr_obs), np.array(gr_null), 'two', 'union_RV_alternancia_grupos', len(gr_obs),
                 {'descripcion': 'transiciones de la mayoria R/V entre grupos consecutivos'})

# =====================================================================
# 5. GRUPOS EMPAREJADOS EN ESPEJO (sumas y tamanos)
# =====================================================================
gsum_obs, gsum_null, gsize_obs, gsize_null = [], [], [], []
meta_g = []
for k, q in P.groupby('kfg', sort=False):
    qq = C[C['kfg'] == k]
    gs = qq.groupby('grupo_n')['vk'].sum()
    sz = qq.groupby('grupo_n').size()
    gs = gs[gs > 0]
    sz = sz.reindex(gs.index)
    G = len(gs)
    if G < 4:
        continue
    a = gs.values.astype(float); b = sz.values.astype(float)
    idx = perm_indices(G, B, rng)
    ap = a[idx]; bp = b[idx]
    ii = np.arange(G // 2)
    jj = G - 1 - ii
    with np.errstate(divide='ignore', invalid='ignore'):
        d = np.mean(np.abs(np.log(a[ii] / a[jj])))
        ds = np.mean(np.abs(b[ii] - b[jj]) / (b[ii] + b[jj]))
        dnull = np.mean(np.abs(np.log(ap[:, ii] / ap[:, jj])), axis=1)
        dsnull = np.mean(np.abs(bp[:, ii] - bp[:, jj]) / (bp[:, ii] + bp[:, jj]), axis=1)
    gsum_obs.append(d); gsum_null.append(dnull)
    gsize_obs.append(ds); gsize_null.append(dsnull)
    meta_g.append((k, G, float(d), float(ds)))

res_gsum = resumen(np.array(gsum_obs), np.array(gsum_null), 'lower', 'grupos_espejo_sumas', len(gsum_obs),
                   {'descripcion': 'media |log(si/sj)| en pares de grupos i, G-1-i'})
res_gsize = resumen(np.array(gsize_obs), np.array(gsize_null), 'lower', 'grupos_espejo_tamanos', len(gsize_obs),
                    {'descripcion': 'media |ni-nj|/(ni+nj) en pares de grupos espejo'})

# =====================================================================
# 6. TORSION S/Z ENTRE MITADES (potencia baja)
# =====================================================================
t_obs, t_null = [], []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    x = q['tor'].values
    ok = np.array([v in ('S', 'Z') for v in x])
    if ok.sum() < 4 or len(set(x[ok])) < 2:
        continue
    lab, m = etiquetas_mitades(n)
    l = lab[ok]; xx = x[ok]
    if (l == 0).sum() < 1 or (l == 1).sum() < 1:
        continue
    p1 = np.mean(xx[l == 0] == 'S'); p2 = np.mean(xx[l == 1] == 'S')
    N = len(xx); m1 = int((l == 0).sum())
    idx = perm_indices(N, B, rng); xp = xx[idx]
    dn = np.mean(xp[:, :m1] == 'S', axis=1) - np.mean(xp[:, m1:] == 'S', axis=1)
    t_obs.append(p1 - p2); t_null.append(dn)
res_t = resumen(np.array(t_obs), np.array(t_null), 'two', 'torsion_SZ_mitades', len(t_obs),
                {'descripcion': 'media pS(1a)-pS(2a) en torsion; solo quipus mixtos'})

# =====================================================================
# 7. COLOR: RACHAS Y COMPOSICION DE MITADES (secundario)
# =====================================================================
cr_obs, cr_null, tv_obs, tv_null = [], [], [], []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    x = q['col_c'].values
    ok = np.array([isinstance(v, str) for v in x])
    if ok.sum() < 6:
        continue
    xx = x[ok]
    if len(set(xx)) < 2:
        continue
    idx = perm_indices(len(xx), B, rng); xp = xx[idx]
    tr = np.sum(xx[1:] != xx[:-1]); trn = np.sum(xp[:, 1:] != xp[:, :-1], axis=1)
    cr_obs.append(tr); cr_null.append(trn)
    lab, m = etiquetas_mitades(n)
    l = lab[ok]
    if (l == 0).sum() < 2 or (l == 1).sum() < 2:
        continue
    cats = sorted(set(xx))
    F1 = np.array([np.mean(xx[l == 0] == c) for c in cats])
    F2 = np.array([np.mean(xx[l == 1] == c) for c in cats])
    tv = 0.5 * np.abs(F1 - F2).sum()
    G1 = np.array([np.mean(xp[:, l == 0] == c, axis=1) for c in cats]).T
    G2 = np.array([np.mean(xp[:, l == 1] == c, axis=1) for c in cats]).T
    tvn = 0.5 * np.abs(G1 - G2).sum(1)
    tv_obs.append(tv); tv_null.append(tvn)
res_cr = resumen(np.array(cr_obs), np.array(cr_null), 'two', 'color_rachas', len(cr_obs),
                 {'descripcion': 'transiciones de color primario'})
res_tv = resumen(np.array(tv_obs), np.array(tv_null), 'lower', 'color_mitades_composicion', len(tv_obs),
                 {'descripcion': 'distancia de variacion total entre paletas de las mitades'})

# =====================================================================
# 8. RESULTADOS: familia confirmatoria + Holm
# =====================================================================
familia = [res_sum, res_eq, res_vmir, res_cmir, res_kd, res_kdr, res_u, res_ur,
           res_uv, res_gsum, res_gsize, res_t]
ps = np.array([r['p'] for r in familia])
orden = np.argsort(ps)
m = len(ps)
holm = np.empty(m)
prev = 0.0
for rank, i in enumerate(orden):
    val = min(1.0, (m - rank) * ps[i])
    val = max(val, prev)
    holm[i] = val
    prev = val
for r, h in zip(familia, holm):
    r['p_holm'] = float(h)

secundarios = [res_rat, res_trend, res_vpar, res_cpar, res_cepar, res_cemir,
               res_kdv, res_gr, res_cr, res_tv]

# ---- tabla por quipu de las simetrias principales
filas = [dict(kfg=k, n=n, s1=s1, s2=s2, log_ratio=d) for (k, n, s1, s2, d) in meta_sum]
TQ = pd.DataFrame(filas).sort_values('log_ratio')
TQ.to_csv('analisis/ds/t_mitades/por_quipu.csv', index=False)

# ---- caso UR028 (Urton 2019)
ur = P[P.kfg == 'UR028'].copy()
urc = C[C.kfg == 'UR028']
ur_g = urc.groupby('grupo_n')['vk'].sum()
ur_n = ur.groupby('grupo_n').size()
caso_ur028 = {'grupos_sumas': {str(k): float(v) for k, v in ur_g.items()},
              'grupos_n': {str(k): int(v) for k, v in ur_n.items()},
              'n_pend': int(len(ur))}
if len(ur) >= 6:
    nn = len(ur); mm = nn // 2
    caso_ur028['s1'] = float(ur['vk'].iloc[:mm].sum())
    caso_ur028['s2'] = float(ur['vk'].iloc[nn - mm:].sum())

out = dict(meta=dict(B=B, semilla=SEMILLA, familia_n=len(familia),
                     n_quipus_total=int(P.kfg.nunique()), n_quipus_sum=int(NSUM)),
           familia=familia, secundarios=secundarios, caso_ur028=caso_ur028,
           top_simetria=TQ.head(12).to_dict(orient='records'))
with open('analisis/ds/t_mitades/resultados.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print('=== FAMILIA CONFIRMATORIA (Holm, m=%d) ===' % len(familia))
for r in familia:
    print('%-32s obs=%9.4f nulo=%9.4f z=%7.2f p=%.4f p_Holm=%.4f cola5=%.3f' %
          (r['test'], r['obs'], r['null_mean'], r['z'], r['p'], r['p_holm'], r['frac_quipus_cola5']))
print('=== SECUNDARIOS ===')
for r in secundarios:
    print('%-32s obs=%9.4f nulo=%9.4f z=%7.2f p=%.4f' %
          (r['test'], r['obs'], r['null_mean'], r['z'], r['p']))
print('UR028:', caso_ur028)
print(TQ.head(8).to_string(index=False))
