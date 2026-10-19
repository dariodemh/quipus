# -*- coding: utf-8 -*-
"""
Estructura de bloques y alineamiento de las dicotomias (R/V, S/Z, color) en los
quipus del KFG.  Nulos: (a) permutacion de etiquetas dentro del quipu;
(b) permutacion de GRUPOS completos (preserva composicion y tamano de cada grupo).

Unidad: el quipu.  B=2000, semilla fija.
Salida: bloques.json
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

C = pd.read_csv(RUTA + 'cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)
C['gr'] = pd.to_numeric(C['grupo'], errors='coerce')
C = C.sort_values(['kfg', 'orden'], kind='mergesort')

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

C['kd'] = C['nudos'].apply(dir_mayor)
C['col_c'] = C['color'].apply(color_coarse)
C['uni'] = C['union'].where(C['union'].isin(['R', 'V']))
P = C[C['nivel'] == 0].copy()

def perm_indices(N, B, rng):
    return np.argsort(rng.random((B, N)), axis=1)

def pval(obs, nullagg, lado):
    if lado == 'lower':
        return (1 + np.sum(nullagg <= obs)) / (B + 1)
    if lado == 'upper':
        return (1 + np.sum(nullagg >= obs)) / (B + 1)
    pl = (1 + np.sum(nullagg <= obs)) / (B + 1)
    pu = (1 + np.sum(nullagg >= obs)) / (B + 1)
    return min(1.0, 2 * min(pl, pu))

def res(obs, null, lado, nombre, nq, extra=None):
    obs = np.asarray(obs, float); null = np.asarray(null, float)
    with np.errstate(invalid='ignore'):
        agg = np.nanmean(null, axis=0)
        o, mu, sd = np.nanmean(obs), np.nanmean(agg), np.nanstd(agg)
        pl = (1 + np.sum(agg <= o)) / (B + 1)
        pu = (1 + np.sum(agg >= o)) / (B + 1)
        p = pl if lado == 'lower' else (pu if lado == 'upper' else min(1.0, 2 * min(pl, pu)))
    d = dict(test=nombre, n_quipus=int(nq), obs=float(o), null_mean=float(mu),
             null_sd=float(sd), z=float((o - mu) / sd) if sd > 0 else np.nan,
             p=float(p), p_lower=float(pl), p_upper=float(pu),
             p_doscolas=float(min(1.0, 2 * min(pl, pu))), lado=lado)
    if extra:
        d.update(extra)
    return d

def runs_of(x):
    x = np.asarray(x)
    if len(x) == 0:
        return 0
    return 1 + int(np.sum(x[1:] != x[:-1]))

def bloques_perm(g, B, rng):
    """B permutaciones de bloques (grupos) preservando su contenido interno.
    Devuelve lista de arrays de indices ordenados segun cada permutacion."""
    idxs = [np.where(g == u)[0] for u in pd.unique(g)]
    perms = np.argsort(rng.random((B, len(idxs))), axis=1)
    return idxs, perms

def aplicar(idxs, perm):
    return np.concatenate([idxs[j] for j in perm])

def perm_within_groups(x, g, B, rng):
    """B permutaciones de x DENTRO de cada grupo (estratificadas)."""
    out = np.empty((B, len(x)), dtype=x.dtype)
    grupos = [np.where(g == u)[0] for u in pd.unique(g)]
    for b in range(B):
        y = x.copy()
        for m in grupos:
            y[m] = x[rng.permutation(m)]
        out[b] = y
    return out

# =====================================================================
# 1. RACHAS, PUREZA DE GRUPO, ALINEAMIENTO CON FRONTERAS DE GRUPO
#     Y NULL DE BLOQUES PARA SUMAS/COLORES
# =====================================================================
filas = {c: {'runs': [], 'runs_null': [], 'runs_null_grp': [],
             'pureza': [], 'pureza_null': [],
             'frontera': [], 'frontera_null': [],
             'maxD': [], 'maxD_null': [], 'maxD_null_grp': [], 'argmax': []}
         for c in ['uni', 'kd']}
sum_blk_obs, sum_blk_null = [], []
col_blk_obs, col_blk_null = [], []
adj_obs, adj_null = [], []
metadatos = []

for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    g = q['gr'].values
    # ---- sumas de mitades con null de bloques
    v = q['vk'].values
    if np.sum(~np.isnan(v)) >= 4:
        fino = np.where(~np.isnan(v))[0]
        idxs, perms = bloques_perm(g, B, rng)
        # observado: mitades sobre TODAS las posiciones (los ausentes no suman)
        m = n // 2
        s1 = np.nansum(v[:m]); s2 = np.nansum(v[n - m:])
        if s1 > 0 and s2 > 0:
            dn = np.empty(B)
            for b in range(B):
                o = aplicar(idxs, perms[b])
                vv = v[o]
                a, c = np.nansum(vv[:m]), np.nansum(vv[n - m:])
                dn[b] = abs(np.log(a / c)) if a > 0 and c > 0 else np.nan
            sum_blk_obs.append(abs(np.log(s1 / s2))); sum_blk_null.append(dn)
    # ---- color espejo con null de bloques
    col = q['col_c'].values
    pres = np.array([isinstance(x, str) for x in col])
    if pres.sum() >= 6:
        m = n // 2
        idxs, perms = bloques_perm(g, B, rng)
        def match_col(order):
            x = col[order]
            ok = np.array([isinstance(y, str) for y in x])
            a = x[:m]; b = x[n - m:][::-1]
            good = ok[:m] & ok[n - m:][::-1]
            if good.sum() < 3:
                return np.nan
            return np.mean(a[good] == b[good])
        ob = match_col(np.arange(n))
        if not np.isnan(ob):
            vals = np.array([match_col(aplicar(idxs, perms[b])) for b in range(B)])
            col_blk_obs.append(ob); col_blk_null.append(vals)
    # ---- dicotomias uni / kd
    for col, etiquetas in [('uni', ('R', 'V')), ('kd', ('S', 'Z'))]:
        x0 = q[col].values
        ok = np.array([z in etiquetas for z in x0])
        if ok.sum() < 6 or len(set(x0[ok])) < 2:
            continue
        x = x0[ok]; gg = g[ok]
        N = len(x)
        # rachas observadas
        r = runs_of(x)
        idx = perm_indices(N, B, rng); xp = x[idx]
        rn = 1 + np.sum(xp[:, 1:] != xp[:, :-1], axis=1)
        filas[col]['runs'].append(r); filas[col]['runs_null'].append(rn)
        # pureza por grupo (grupos con >=2 cuerdas etiquetadas)
        pure, tot = 0, 0
        for u in pd.unique(gg):
            xu = x[gg == u]
            if len(xu) >= 2:
                tot += 1
                pure += int(len(set(xu)) == 1)
        if tot >= 2:
            filas[col]['pureza'].append(pure / tot)
            gp = np.empty(B)
            for b in range(B):
                xb = xp[b]; p = 0
                for u in pd.unique(gg):
                    xu = xb[gg == u]
                    if len(xu) >= 2:
                        p += int(len(set(xu)) == 1)
                gp[b] = p / tot
            filas[col]['pureza_null'].append(gp)
        # rachas con null de bloques
        idxs, perms = bloques_perm(gg, B, rng)
        rb = np.empty(B)
        for b in range(B):
            rb[b] = runs_of(x[aplicar(idxs, perms[b])])
        filas[col]['runs_null_grp'].append(rb)
        # fraccion de cambios que caen en frontera de grupo
        ch = np.where(x[1:] != x[:-1])[0] + 1
        if len(ch) >= 1:
            fr = np.mean(gg[ch] != gg[ch - 1])
            frn = np.empty(B)
            for b in range(B):
                xb = xp[b]
                chb = np.where(xb[1:] != xb[:-1])[0] + 1
                frn[b] = np.mean(gg[chb] != gg[chb - 1]) if len(chb) else np.nan
            filas[col]['frontera'].append(fr); filas[col]['frontera_null'].append(frn)
        # scan de punto de cambio: max |p_izq - p_der| en el 20-80% central
        lo, hi = int(np.ceil(0.2 * N)), int(np.floor(0.8 * N))
        sgrid = np.arange(lo, hi + 1)
        def maxD(vec):
            cs = np.cumsum(vec == etiquetas[0])
            iz = cs[sgrid - 1] / sgrid
            de = (cs[-1] - cs[sgrid - 1]) / (N - sgrid)
            dd = np.abs(iz - de)
            j = int(np.argmax(dd))
            return dd[j], sgrid[j] / N
        D, am = maxD(x)
        Dn = np.empty(B); amn = np.empty(B)
        for b in range(B):
            Dn[b], amn[b] = maxD(xp[b])
        filas[col]['maxD'].append(D); filas[col]['maxD_null'].append(Dn)
        filas[col]['argmax'].append(am)
        filas[col].setdefault('argmax_null', []).append(amn)
        # null de bloques para maxD
        Db = np.empty(B)
        for b in range(B):
            Db[b] = maxD(x[aplicar(idxs, perms[b])])[0]
        filas[col]['maxD_null_grp'].append(Db)
        metadatos.append((k, col, N, len(pd.unique(gg)), r, D, am))

out = {}
for col in ['uni', 'kd']:
    f = filas[col]
    if not f['runs']:
        continue
    out[col + '_rachas'] = res(f['runs'], f['runs_null'], 'lower', col + '_rachas_cord', len(f['runs']))
    out[col + '_rachas_vs_bloques'] = res(f['runs'], f['runs_null_grp'], 'lower', col + '_rachas_vs_null_grupos', len(f['runs']))
    out[col + '_pureza_grupo'] = res(f['pureza'], f['pureza_null'], 'upper', col + '_pureza_grupo', len(f['pureza']))
    out[col + '_cambios_en_frontera'] = res(f['frontera'], f['frontera_null'], 'upper', col + '_cambios_en_frontera', len(f['frontera']))
    out[col + '_maxD'] = res(f['maxD'], f['maxD_null'], 'upper', col + '_maxD_vs_perm_cuerdas', len(f['maxD']),
                              {'argmax_mediana': float(np.median(f['argmax'])),
                               'frac_argmax_0.4_0.6': float(np.mean((np.array(f['argmax']) >= 0.4) & (np.array(f['argmax']) <= 0.6)))})
    out[col + '_maxD_vs_bloques'] = res(f['maxD'], f['maxD_null_grp'], 'upper', col + '_maxD_vs_null_grupos', len(f['maxD']))
    out[col + '_argmax_conc'] = {'argmax_mediana': float(np.median(f['argmax'])),
                                 'media_abs_argmax_menos_0.5': float(np.mean(np.abs(np.array(f['argmax']) - 0.5))),
                                 'frac_0.4_0.6': float(np.mean((np.array(f['argmax']) >= 0.4) & (np.array(f['argmax']) <= 0.6))),
                                 'n': len(f['argmax'])}
    # contraste: cuan centrado esta el punto de cambio observado frente al nulo
    obs_conc = np.abs(np.array(f['argmax']) - 0.5)
    null_conc = np.nanmean(np.abs(np.array(f['argmax_null']) - 0.5), axis=1)
    p_conc = (1 + np.sum(null_conc <= np.mean(obs_conc))) / (B + 1)
    out[col + '_argmax_conc']['p_mas_central_que_nulo'] = float(p_conc)
    out[col + '_argmax_conc']['nulo_media_abs'] = float(np.mean(null_conc))

out['suma_mitades_vs_null_grupos'] = res(sum_blk_obs, sum_blk_null, 'lower',
                                         'suma_mitades_vs_null_grupos', len(sum_blk_obs))
out['color_espejo_vs_null_grupos'] = res(col_blk_obs, col_blk_null, 'lower',
                                         'color_espejo_vs_null_grupos', len(col_blk_obs))

# =====================================================================
# 2. ASOCIACIONES ENTRE DICOTOMIAS Y CON EL COLOR (AB vs MB)
# =====================================================================
def asoc(colx, valx, nombre, target):
    obs, null = [], []
    for k, q in P.groupby('kfg', sort=False):
        a = q[colx].values; b = q[valx].values
        ok = np.array([z in ('R', 'V') for z in a]) & np.array([z in ('S', 'Z') for z in b])
        if ok.sum() < 8:
            continue
        aa = a[ok]; bb = b[ok]
        if len(set(aa)) < 2 or len(set(bb)) < 2:
            continue
        # diferencia de la tasa del nivel `target` entre S y Z
        def dif(xa, xb):
            return np.mean(xa[xb == 'S'] == target) - np.mean(xa[xb == 'Z'] == target)
        o = dif(aa, bb)
        idx = perm_indices(len(aa), B, rng)
        dn = np.array([dif(aa[idx[t]], bb) for t in range(B)])
        obs.append(o); null.append(dn)
    return res(obs, null, 'two', nombre, len(obs))

out['union_x_direccion'] = asoc('uni', 'kd', 'union_x_direccion', 'R')

def asoc_color(colx, nombre, target, permitidos):
    """Tasa del nivel `target` en cuerdas AB vs MB."""
    obs, null = [], []
    for k, q in P.groupby('kfg', sort=False):
        a = q[colx].values; b = q['col_c'].values
        ok = np.array([z in permitidos for z in a]) & np.array([z in ('AB', 'MB') for z in b])
        if ok.sum() < 8:
            continue
        aa = a[ok]; bb = b[ok]
        if len(set(aa)) < 2 or len(set(bb)) < 2:
            continue
        def dif(xa, xb):
            return np.mean(xa[xb == 'AB'] == target) - np.mean(xa[xb == 'MB'] == target)
        o = dif(aa, bb)
        idx = perm_indices(len(aa), B, rng)
        dn = np.array([dif(aa[idx[t]], bb) for t in range(B)])
        obs.append(o); null.append(dn)
    return res(obs, null, 'two', nombre, len(obs))

out['union_color_AB_MB'] = asoc_color('uni', 'union_color_AB_MB', 'R', ('R', 'V'))
out['direccion_color_AB_MB'] = asoc_color('kd', 'direccion_color_AB_MB', 'S', ('S', 'Z'))

# color AB vs MB y valor
obs, null = [], []
for k, q in P.groupby('kfg', sort=False):
    v = q['vk'].values; b = q['col_c'].values
    ok = ~np.isnan(v) & np.array([z in ('AB', 'MB') for z in b])
    if ok.sum() < 8:
        continue
    vv = np.log1p(v[ok]); bb = b[ok]
    if len(set(bb)) < 2:
        continue
    o = np.mean(vv[bb == 'AB']) - np.mean(vv[bb == 'MB'])
    idx = perm_indices(len(vv), B, rng); vp = vv[idx]
    dn = np.mean(vp[:, bb == 'AB'], axis=1) - np.mean(vp[:, bb == 'MB'], axis=1)
    obs.append(o); null.append(dn)
out['valor_color_AB_MB'] = res(obs, null, 'two', 'valor_color_AB_MB', len(obs))

# valor AB vs MB DENTRO de grupo (control de composicion por grupos)
obs, null = [], []
for k, q in P.groupby('kfg', sort=False):
    v = q['vk'].values; b = q['col_c'].values; g = q['gr'].values
    ok = ~np.isnan(v) & np.array([z in ('AB', 'MB') for z in b])
    if ok.sum() < 8:
        continue
    vv = np.log1p(v[ok]); bb = b[ok]; gg = g[ok]
    grupos = [np.where(gg == u)[0] for u in pd.unique(gg)]
    grupos = [m for m in grupos
              if len(set(bb[m])) == 2 and np.sum(bb[m] == 'AB') >= 2 and np.sum(bb[m] == 'MB') >= 2]
    if len(grupos) < 2:
        continue
    def dif(bcol):
        return np.mean([np.mean(vv[m][bcol[m] == 'AB']) - np.mean(vv[m][bcol[m] == 'MB'])
                        for m in grupos])
    o = dif(bb)
    bp = perm_within_groups(bb, gg, B, rng)
    dn = np.array([dif(bp[t]) for t in range(B)])
    obs.append(o); null.append(dn)
out['valor_color_AB_MB_dentro_grupo'] = res(obs, null, 'two', 'valor_color_AB_MB_dentro_grupo', len(obs))

# control mecanico: S vs Z dentro de (grupo, tipo del primer nudo, n de nudos)
q = P[P['kd'].isin(['S', 'Z']) & P['vk'].notna()].copy()
q['l'] = np.log1p(q['vk'])
q['tipos'] = q['nudos'].apply(lambda s: ''.join(re.findall(r'\d+([SLE]+)\(', s)) if isinstance(s, str) else '')
q['t1'] = q['tipos'].str[0]
q['ncl'] = q['tipos'].str.len()
estratos = []
for (k, g, t1, ncl), qq in q.groupby(['kfg', 'gr', 't1', 'ncl']):
    if qq['kd'].nunique() == 2 and len(qq) >= 4:
        estratos.append(qq[qq['kd'] == 'S']['l'].mean() - qq[qq['kd'] == 'Z']['l'].mean())
estratos = np.array(estratos)
out['control_dir_valor_estratos'] = {
    'n_estratos': int(len(estratos)),
    'media_dif_S_Z': float(np.mean(estratos)),
    'frac_negativos': float(np.mean(estratos < 0)),
    'sign_p': float(stats.binomtest(int(np.sum(estratos < 0)), len(estratos), 0.5).pvalue)}

# AB en primera vs segunda mitad
obs, null = [], []
for k, q in P.groupby('kfg', sort=False):
    n = len(q); b = q['col_c'].values
    ok = np.array([z in ('AB', 'MB') for z in b])
    if ok.sum() < 8:
        continue
    pos = np.arange(n)
    prim = ok & (pos < n // 2); seg = ok & (pos >= n - n // 2)
    if prim.sum() < 2 or seg.sum() < 2:
        continue
    o = np.mean(b[prim] == 'AB') - np.mean(b[seg] == 'AB')
    idx = perm_indices(n, B, rng); bp = b[idx]
    dn = np.mean(bp[:, prim] == 'AB', axis=1) - np.mean(bp[:, seg] == 'AB', axis=1)
    obs.append(o); null.append(dn)
out['color_AB_mitades'] = res(obs, null, 'two', 'color_AB_mitades', len(obs))

# direccion S/Z y valor DENTRO de grupo
obs, null = [], []
for k, q in P.groupby('kfg', sort=False):
    v = q['vk'].values; d = q['kd'].values; g = q['gr'].values
    ok = ~np.isnan(v) & np.array([z in ('S', 'Z') for z in d])
    if ok.sum() < 8:
        continue
    vv = np.log1p(v[ok]); dd = d[ok]; gg = g[ok]
    grupos = [np.where(gg == u)[0] for u in pd.unique(gg)]
    grupos = [m for m in grupos if len(set(dd[m])) == 2 and m.sum() >= 4]
    if len(grupos) < 2:
        continue
    def difd(dcol):
        return np.mean([np.mean(vv[m][dcol[m] == 'S']) - np.mean(vv[m][dcol[m] == 'Z'])
                        for m in grupos])
    o = difd(dd)
    dp = perm_within_groups(dd, gg, B, rng)
    dn = np.array([difd(dp[t]) for t in range(B)])
    obs.append(o); null.append(dn)
out['valor_direccion_dentro_grupo'] = res(obs, null, 'two', 'valor_direccion_dentro_grupo', len(obs))

# =====================================================================
# 3. ORDEN DE GRUPOS: TAMANO/VALOR, PARES ADYACENTES VS ESPEJO
# =====================================================================
rho_sum, rho_sz = [], []
adj_sum, adj_null_pares = [], []
for k, q in P.groupby('kfg', sort=False):
    gs = C[C['kfg'] == k].groupby('gr')['vk'].sum()
    gs = gs[gs > 0]
    sz = C[C['kfg'] == k].groupby('gr').size().reindex(gs.index)
    G = len(gs)
    if G < 3:
        continue
    idx = np.arange(G)
    if gs.nunique() > 1:
        rho_sum.append(stats.spearmanr(idx, gs.values).statistic)
    if sz.nunique() > 1:
        rho_sz.append(stats.spearmanr(idx, sz.values).statistic)
    if G >= 3:
        a = gs.values.astype(float)
        d = np.mean(np.abs(np.log(a[1:] / a[:-1])))
        idxp = perm_indices(G, B, rng); ap = a[idxp]
        dn = np.mean(np.abs(np.log(ap[:, 1:] / ap[:, :-1])), axis=1)
        adj_sum.append(d); adj_null_pares.append(dn)

out['orden_grupo_vs_suma'] = {'media_rho': float(np.mean(rho_sum)), 'n': len(rho_sum),
                              'frac_positivos': float(np.mean(np.array(rho_sum) > 0))}
out['orden_grupo_vs_tamano'] = {'media_rho': float(np.mean(rho_sz)), 'n': len(rho_sz),
                                'frac_positivos': float(np.mean(np.array(rho_sz) > 0))}
out['grupos_adyacentes_sumas'] = res(adj_sum, adj_null_pares, 'lower', 'grupos_adyacentes_sumas', len(adj_sum))

# =====================================================================
# 4. UR028 con subsidiarias: suma por agrupacion de Urton (2019)
# =====================================================================
q = C[C['kfg'] == 'UR028'].sort_values('orden').copy()
q['top'] = q['cuerda'].str.extract(r'^(p\d+)')[0]
gsum = C[C['kfg'] == 'UR028'].groupby('gr')['vk'].sum()
caso = {'sumas_por_grupo_con_subs': {str(int(k)): float(v) for k, v in gsum.items()},
        'suma_p1': float(q[q.top == 'p1']['vk'].sum()),
        'suma_p2_p4': float(q[q.top.isin(['p2', 'p3', 'p4'])]['vk'].sum()),
        'suma_p5_p74': float(q[q.top.apply(lambda s: int(s[1:]) if isinstance(s, str) else -1).between(5, 74)]['vk'].sum()),
        'n_pend': int((q.nivel == 0).sum())}
out['caso_UR028'] = caso

with open('analisis/ds/t_mitades/bloques.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print('=== BLOQUES Y ASOCIACIONES ===')
for k, v in out.items():
    if isinstance(v, dict) and 'p' in v:
        print('%-34s obs=%9.4f nulo=%9.4f z=%7.2f p=%.4f n=%d' %
              (v.get('test', k), v['obs'], v['null_mean'], v['z'], v['p'], v['n_quipus']))
    elif isinstance(v, dict):
        print(k, v)
print('UR028:', caso)
