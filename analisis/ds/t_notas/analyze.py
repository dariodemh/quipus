# -*- coding: utf-8 -*-
"""Analisis del catalogo de rasgos no numericos (notas cualitativas).

Unidad de analisis = quipu (BRIEF, regla 1). Todos los tests llevan nulo de
permutacion explicito, semilla fija y correccion BH-FDR.
"""
import os, numpy as np, pandas as pd
from scipy.stats import chi2_contingency

RNG = np.random.default_rng(20261018)
B = 10000
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
pd.set_option('display.width', 160)

an = pd.read_csv(os.path.join(AQUI, 'rasgos.csv'))
q = pd.read_csv(os.path.join(RAIZ, 'analisis', 'datos', 'quipus.csv'))
cu = pd.read_csv(os.path.join(RAIZ, 'analisis', 'datos', 'cuerdas.csv'))
FEATS = ['rota', 'deterioro', 'perdida', 'desprendida', 'reparacion', 'sin_nudo_final',
         'nudo_extra', 'cuerda_superior', 'cordon_principal', 'envoltura', 'marcador',
         'objeto', 'pelo', 'color_anomalo']
META = ['fibra', 'etiqueta', 'clasif_tipo']

# grupos de procedencia (se conservan las que tienen >=8 quipus anotados)
def grupo(p):
    p = str(p)
    if p == 'Unknown': return 'Desconocida'
    if p == 'Pachacamac': return 'Pachacamac'
    if p == 'Leymebamba': return 'Leymebamba'
    if p in ('Ica', 'Ica/Pisco', 'Nazca', 'Santa', 'Paracas'): return 'Costa sur'
    return 'Otras'
q['grupo_proc'] = q.procedencia.map(grupo)
meta = q.set_index('kfg')[['procedencia', 'region', 'museo', 'grupo_proc', 'okr', 'pc_estructura']]

# ---------------------------------------------------------------- 1. catalogo
tot_q = q.kfg.nunique()
ann_q = an.kfg.nunique()
cat = pd.DataFrame({
    'cuerdas': [an[f].sum() for f in FEATS + META],
    'quipus': [an.loc[an[f], 'kfg'].nunique() for f in FEATS + META],
}, index=FEATS + META)
cat['%_quipus_anotados'] = (100 * cat.quipus / ann_q).round(1)
cat['%_todos'] = (100 * cat.quipus / tot_q).round(1)
cat = cat.sort_values('quipus', ascending=False)
print('== CATALOGO (base: %d cuerdas anotadas, %d quipus anotados de %d)' % (len(an), ann_q, tot_q))
print(cat.to_string())
cat.to_csv(os.path.join(AQUI, 'tabla_catalogo.csv'))

porq = an.groupby('kfg')[FEATS].sum()
porq[FEATS] = porq[FEATS] > 0
porq['n_anot'] = an.groupby('kfg').size()
porq['n_rasgos'] = (porq[FEATS] > 0).sum(axis=1)
porq = porq.join(meta)
print('\n== distribution de rasgos por quipu (n=%d)' % len(porq))
print(porq.n_rasgos.value_counts().sort_index().to_string())
print('\ncorrelacion n_anot vs n_rasgos: Spearman %.3f' %
      porq[['n_anot', 'n_rasgos']].corr(method='spearman').iloc[0, 1])
print('\nTop 10 quipus por n de rasgos distintos:')
print(porq.sort_values(['n_rasgos', 'n_anot'], ascending=False)
      .head(10)[['n_anot', 'n_rasgos', 'procedencia', 'grupo_proc']].to_string())
porq.to_csv(os.path.join(AQUI, 'tabla_por_quipu.csv'))

# ------------------------------------------------ 2. procedencia (quipu nivel)
MIN_ANOT = 5
sub = porq[porq.n_anot >= MIN_ANOT].copy()
print('\n== test procedencia: %d quipus con >=%d cuerdas anotadas' % (len(sub), MIN_ANOT))
print(sub.grupo_proc.value_counts().to_string())

filas = []
tabs = {}
for f in FEATS:
    tab = pd.crosstab(sub.grupo_proc, sub[f])
    tab = tab.reindex(columns=[False, True], fill_value=0)
    tab = tab[tab.sum(axis=1) >= 5]
    if tab.shape[0] < 2 or tab[True].sum() < 3:
        continue
    chi2, p_as, dof, _ = chi2_contingency(tab.values, correction=False)
    # nulo: permutar etiquetas de procedencia entre quipus
    y = sub[f].values.astype(bool)
    g = sub.grupo_proc.values
    gs = np.array(sorted(set(g)))
    geq = 0
    for _ in range(B):
        gp = RNG.permutation(g)
        # chi2 rapido con tablas 2 x k
        obs = np.array([[np.sum((gp == s) & y), np.sum((gp == s) & ~y)] for s in gs])
        if (obs.sum(1) == 0).any() or (obs.sum(0) == 0).any():
            continue
        e = np.outer(obs.sum(1), obs.sum(0)) / obs.sum()
        c = ((obs - e) ** 2 / e).sum()
        if c >= chi2: geq += 1
    p_perm = (1 + geq) / (B + 1)
    # tasas por grupo (Wilson 95%)
    tasas = {}
    for s in tab.index:
        k, n = int(tab.loc[s, True]), int(tab.loc[s].sum())
        ph = k / n
        z = 1.96; den = 1 + z * z / n
        cen = (ph + z * z / (2 * n)) / den
        half = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
        tasas[s] = '%.0f%% (%d/%d)' % (100 * ph, k, n)
    filas.append({'rasgo': f, 'chi2': chi2, 'gl': dof, 'p_asint': p_as, 'p_perm': p_perm, **tasas})
    tabs[f] = tab

res = pd.DataFrame(filas)
if len(res):
    from scipy.stats import false_discovery_control
    res['q_BH'] = false_discovery_control(res.p_perm.values, method='bh')
    res = res.sort_values('p_perm')
    print(res.round(4).to_string(index=False))
    res.to_csv(os.path.join(AQUI, 'tabla_procedencia.csv'), index=False)
    print('\nTabla de contingencia del rasgo mas asociado:')
    print(tabs[res.iloc[0].rasgo].to_string())

# ------------------------------------- 3. co-ocurrencia dentro de cada quipu
def cooc(a, b, etiqueta):
    d = an[an.groupby('kfg').kfg.transform('size') >= 3]
    obs = int((d[a] & d[b]).sum())
    geq = 0
    idx = d.groupby('kfg').indices
    av, bv = d[a].values.astype(bool), d[b].values.astype(bool)
    sims = np.empty(B)
    for j in range(B):
        s = 0
        for _, ii in idx.items():
            sh = av[ii].copy(); RNG.shuffle(sh)
            s += int((sh & bv[ii]).sum())
        sims[j] = s
        if s >= obs: geq += 1
    p = (1 + geq) / (B + 1)
    print('%-28s ambos=%4d  nulo dentro-quipu media=%.1f [p5=%.0f,p95=%.0f]  p=%.4f' % (
        etiqueta, obs, sims.mean(), np.percentile(sims, 5), np.percentile(sims, 95), p))
    return {'par': etiqueta, 'ambos': obs, 'nulo_media': sims.mean(), 'p_perm': p}

print('\n== co-ocurrencia a nivel de cuerda, permutando DENTRO de cada quipu')
co = []
co.append(cooc('rota', 'reparacion', 'rota & reparacion'))
co.append(cooc('rota', 'perdida', 'rota & perdida'))
co.append(cooc('rota', 'desprendida', 'rota & desprendida'))
co.append(cooc('rota', 'deterioro', 'rota & deterioro'))
co.append(cooc('reparacion', 'desprendida', 'reparacion & desprendida'))
pd.DataFrame(co).to_csv(os.path.join(AQUI, 'tabla_coocurrencia.csv'), index=False)

# ------------------------------- 4. las notas no son aleatorias en la cuerda
print('\n== notas vs campos estructurados (nulo: permutar anotacion dentro del quipu)')
cu['an'] = cu.notas.notna()
cu['vacia'] = cu.nudos.isna() | (cu.nudos.astype(str).str.strip() == '')
cu['unionU'] = cu.union.astype(str).str.upper().eq('U')
cu['sub'] = cu.nivel > 0
idx = cu.groupby('kfg').indices
for var in ['vacia', 'unionU', 'sub']:
    y = cu[var].values.astype(float)
    a = cu['an'].values.astype(bool)
    obs = y[a].mean() - y[~a].mean()
    geq = 0
    for _ in range(2000):
        ap = np.zeros_like(a)
        for _, ii in idx.items():
            sh = a[ii].copy(); RNG.shuffle(sh); ap[ii] = sh
        if (y[ap].mean() - y[~ap].mean()) >= obs: geq += 1
    print('%-8s P(%s|anotada)=%.3f  P(%s|no anotada)=%.3f  dif=%+.3f  p=%.4f' % (
        var, var, y[a].mean(), var, y[~a].mean(), obs, (1 + geq) / 2001))

# ------------------------------------- 5. cobertura y sensibilidad de coleccion
print('\n== cobertura del catalogo')
anyf = an[FEATS].any(axis=1)
print('cuerdas anotadas con >=1 rasgo: %d/%d (%.0f%%)' % (anyf.sum(), len(an), 100 * anyf.mean()))
print('quipus anotados con >=1 rasgo: %d/%d (%.0f%%)' % (
    an.loc[anyf, 'kfg'].nunique(), an.kfg.nunique(),
    100 * an.loc[anyf, 'kfg'].nunique() / an.kfg.nunique()))
print('notas que solo son metadatos (fibra/etiqueta/tipo): %d' % (
    (an[META].any(axis=1) & ~anyf).sum()))

print('\n== tasa por 100 cuerdas anotadas, por grupo de procedencia')
grp = an.kfg.map(meta.grupo_proc)
tab = an.groupby(grp)[FEATS].sum()
tab['n_anot'] = an.groupby(grp).size()
tasas = (100 * tab[FEATS].div(tab.n_anot, axis=0)).round(1)
tasas['n_anot'] = tab.n_anot
print(tasas.T.to_string())

print('\n== sensibilidad: solo quipus UR (mismo equipo de transcripcion)')
ur = an[an.kfg.str.startswith('UR')]
urg = ur.kfg.map(meta.grupo_proc)
t2 = ur.groupby(urg)[['rota', 'reparacion']].sum()
t2['n_anot'] = ur.groupby(urg).size()
t2['tasa_rota_%'] = (100 * t2.rota / t2.n_anot).round(1)
print(t2.to_string())
from scipy.stats import fisher_exact
cs = ur[(urg == 'Costa sur')]
ley = ur[(urg == 'Leymebamba')]
a = int(cs.rota.sum()); b = len(cs) - a
c_ = int(ley.rota.sum()); d_ = len(ley) - c_
print('UR Costa sur vs Leymebamba (cuerdas): rota %d/%d vs %d/%d, Fisher p=%.4f' % (
    a, len(cs), c_, len(ley), fisher_exact([[a, b], [c_, d_]])[1]))
# a nivel de quipu
pq = porq[porq.index.str.startswith('UR')]
cq = pq[pq.grupo_proc == 'Costa sur']; lq = pq[pq.grupo_proc == 'Leymebamba']
print('UR por quipu: rota %d/%d vs %d/%d, Fisher p=%.4f' % (
    cq.rota.sum(), len(cq), lq.rota.sum(), len(lq),
    fisher_exact([[cq.rota.sum(), len(cq) - cq.rota.sum()],
                  [lq.rota.sum(), len(lq) - lq.rota.sum()]])[1]))
print('\n== efecto coleccion (anotador): tasa de rota por prefijo')
pref = an.kfg.str[:2]
print(an.groupby(pref).agg(n_anot=('rota', 'size'), rota=('rota', 'sum'),
                           tasa=('rota', 'mean')).query('n_anot>=50').round(3).to_string())
