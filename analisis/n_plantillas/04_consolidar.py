"""Une puntuaciones, calcula p_corpus, BH y Holm por mitad, controles, agrupamiento y clase no numérica.
Salidas: puntuaciones.csv, controles.csv, coincidencias.csv, agrupamiento.txt, no_numericos.csv."""
import pickle, numpy as np, pandas as pd
from pathlib import Path
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

OUT = Path(__file__).resolve().parent
DAT = pickle.load(open(OUT / 'datos.pkl', 'rb')); K = DAT['K']; meta = DAT['meta']; mit = DAT['mit']
d = pd.concat([pd.read_csv(OUT / 'obs_perm.csv')] + ([pd.read_csv(OUT / 'p6b.csv')] if (OUT / 'p6b.csv').exists() else []),
              ignore_index=True)
npend = {k: len(v['vals']) for k, v in K.items()}
d['n_colg'] = d.kfg.map(npend)
COMPOS = {'P3', 'P12'}

# p_corpus: percentil superior entre quipus de tamaño parecido con el estadístico definido
pc = np.full(len(d), np.nan)
for t, g in d.groupby('plantilla'):
    if t.startswith('P9b'): continue
    x = g.estadistico.to_numpy(); n = g.n_colg.to_numpy()
    for i, idx in enumerate(g.index):
        ref = (n >= n[i] / 1.5) & (n <= n[i] * 1.5); ref[i] = False
        if ref.sum() < 20: ref = np.ones(len(x), bool); ref[i] = False
        pc[d.index.get_loc(idx)] = (1 + np.sum(x[ref] >= x[i] - 1e-12)) / (1 + ref.sum())
d['p_corpus'] = pc
# p para la corrección
base = {t: g.estadistico.mean() for t, g in d.groupby('plantilla') if t.startswith('P9b')}
def pfin(r):
    if r.plantilla.startswith('P9b'): return base[r.plantilla] if r.estadistico > 0 else 1.0
    if r.plantilla in COMPOS: return r.p_corpus
    return r.p_perm
d['p'] = d.apply(pfin, axis=1)
d['mitad'] = d.kfg.map(mit)
d['q'] = np.nan; d['q_holm'] = np.nan
for m, g in d.groupby('mitad'):
    d.loc[g.index, 'q'] = multipletests(g.p, method='fdr_bh')[1]
    d.loc[g.index, 'q_holm'] = multipletests(g.p, method='holm')[1]
d['coincide'] = (d.q < .05) & ((d.p_corpus <= .05) | d.plantilla.isin(COMPOS)) & ~d.plantilla.str.startswith('P9b')
d['procedencia'] = d.kfg.map(meta.procedencia); d['museo'] = d.kfg.map(meta.museo)
cols = ['kfg', 'plantilla', 'estadistico', 'p', 'q', 'mitad', 'q_holm', 'p_perm', 'B', 'p_corpus', 'coincide',
        'n_colg', 'procedencia', 'museo']
d = d.sort_values(['plantilla', 'p'])
d[cols].rename(columns={'kfg': 'khipu'}).to_csv(OUT / 'puntuaciones.csv', index=False)
print('pruebas por mitad:', d.groupby('mitad').size().to_dict())

# ---------- controles positivos ----------
CTRL = {'P3': ['UR029', 'UR091', 'AS026A', 'AS157', 'UR023'], 'P4r': ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092'],
        'P5a': ['UR266', 'UR275', 'UR278'], 'P5b': ['UR266', 'UR275', 'UR278'], 'P5c': ['UR266', 'UR275', 'UR278'],
        'P6b': ['UR063', 'UR064', 'UR066', 'UR067', 'UR068', 'UR073'], 'P8ar': ['UR006', 'UR009', 'UR021'],
        'P9a': ['UR053B', 'UR053C']}
rows = []
for t, ks in CTRL.items():
    for k in ks:
        r = d[(d.kfg == k) & (d.plantilla == t)]
        rows.append(dict(plantilla=t, khipu=k, en_puerta=len(r) > 0,
                         estadistico=r.estadistico.iloc[0] if len(r) else np.nan,
                         p=r.p.iloc[0] if len(r) else np.nan, p_corpus=r.p_corpus.iloc[0] if len(r) else np.nan,
                         q=r.q.iloc[0] if len(r) else np.nan, mitad=mit.get(k)))
ctl = pd.DataFrame(rows); ctl.to_csv(OUT / 'controles.csv', index=False)
ctl['ok'] = (ctl.p < .05) & (ctl.p_corpus <= .10)
print(ctl.to_string()); print(ctl.groupby('plantilla').ok.agg(['sum', 'size']))

# ---------- coincidencias y agrupamiento ----------
cl = pd.read_csv(OUT.parent / 'ds/n_no_numericos/quipus_clase.csv').set_index('kfg')
can = (cl.num_canuto_cords.fillna(0) > 0); cam = (cl.f_CL.fillna(0) > 0)
co = d[d.coincide]
co[cols].to_csv(OUT / 'coincidencias.csv', index=False)
lines = []
for t, g in d.groupby('plantilla'):
    m = g[g.coincide]
    lines.append(f'\n## {t}: {len(m)} coincidencias / {len(g)} pruebas '
                 f'(exploración {int((m.mitad=="exploracion").sum())}, confirmación {int((m.mitad=="confirmacion").sum())})')
    if len(m) == 0: continue
    lines.append('  ' + ', '.join(f'{r.kfg}({r.mitad[:4]}, p={r.p:.1e}, q={r.q:.2g}, pc={r.p_corpus:.3f})' for r in m.itertuples()))
    for var, lab in [('procedencia', 'procedencia'), ('museo', 'museo')]:
        vc = m[var].value_counts()
        top = vc.index[0]; a = int(vc.iloc[0]); b = len(m) - a
        c_ = int((g[var] == top).sum()) - a; e = len(g) - len(m) - c_
        p = fisher_exact([[a, b], [c_, e]], alternative='greater')[1]
        lines.append(f'  {lab} más frecuente: {top} {a}/{len(m)} (base {int((g[var]==top).sum())}/{len(g)}), Fisher p={p:.2g}')
    for s, lab in [(can, 'canutos'), (cam, 'camélido')]:
        mm = m.kfg.map(s).fillna(False).astype(bool); gg = g.kfg.map(s).fillna(False).astype(bool)
        lines.append(f'  {lab}: {mm.mean():.2f} en coincidencias vs {gg.mean():.2f} en probados')
open(OUT / 'agrupamiento.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print('\n'.join(lines))

# ---------- clase no numérica ----------
NN = ['UR178', 'UR179', 'UR180', 'UR050', 'UR052', 'UR054', 'UR055', 'AS076', 'JC012', 'UR203', 'UR215']
nn = d[d.kfg.isin(NN)][cols].sort_values(['kfg', 'p'])
nn.to_csv(OUT / 'no_numericos.csv', index=False)
print(nn[nn.p < .05].to_string())


# ---------- exceso sobre la tasa base, replicación entre mitades y agrupamiento corregido ----------
from scipy.stats import poisson
MALO = {'Unknown', 'unknown', 'Peru'}
res, conf_tests = [], []
for t, g in d.groupby('plantilla'):
    if t.startswith('P9b'): continue
    n = len(g); m = g[g.coincide]; E = .05 * n; o = len(m)
    lo, hi = poisson.ppf(.025, o) if o else 0, poisson.ppf(.975, o)
    r = dict(plantilla=t, pruebas=n, coincidencias=o, esperado_max=round(E, 1), razon=round(o / E, 2) if E else np.nan,
             IC95_coinc=f'[{lo:.0f}, {hi:.0f}]', expl=int((m.mitad == 'exploracion').sum()), conf=int((m.mitad == 'confirmacion').sum()))
    # agrupamiento: categoría elegida en EXPLORACIÓN, probada en CONFIRMACIÓN
    for var in ('procedencia', 'museo'):
        ge = g[g.mitad == 'exploracion']; me = ge[ge.coincide & ~ge[var].isin(MALO)]
        if len(me) < 2: r[f'{var}_expl'] = ''; continue
        top = me[var].value_counts().index[0]; a = int((me[var] == top).sum())
        pe = fisher_exact([[a, int(ge.coincide.sum()) - a], [int((ge[var] == top).sum()) - a,
                           int((~ge.coincide).sum()) - (int((ge[var] == top).sum()) - a)]], alternative='greater')[1]
        gc = g[g.mitad == 'confirmacion']; ac = int((gc.coincide & (gc[var] == top)).sum())
        bc = int(gc.coincide.sum()) - ac; cc = int((gc[var] == top).sum()) - ac; dc = len(gc) - ac - bc - cc
        pcf = fisher_exact([[ac, bc], [cc, dc]], alternative='greater')[1]
        r[f'{var}_expl'] = f'{top}: {a}/{len(ge[ge.coincide])} (p={pe:.2g})'
        r[f'{var}_conf'] = f'{ac}/{int(gc.coincide.sum())} (base {int((gc[var]==top).sum())}/{len(gc)}), p={pcf:.2g}'
        conf_tests.append((t, var, pcf))
    res.append(r)
R = pd.DataFrame(res)
if conf_tests:
    hp = multipletests([x[2] for x in conf_tests], method='holm')[1]
    for (t, var, _), h in zip(conf_tests, hp):
        R.loc[R.plantilla == t, f'{var}_conf_holm'] = round(h, 4)
R.to_csv(OUT / 'exceso_replicacion.csv', index=False)
print(R.to_string())
print('pruebas de agrupamiento en confirmación (familia Holm):', len(conf_tests))
