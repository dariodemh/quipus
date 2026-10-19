"""Paso 5: predicciones prerregistradas (predicciones_preregistradas.md y informe.md §5).
Parte A: hipótesis post hoc de ceques UR050 + UR055."""
import pickle, numpy as np, pandas as pd
from pathlib import Path
import plantillas as T

OUT = Path(__file__).resolve().parent
DAT = pickle.load(open(OUT / 'datos.pkl', 'rb')); K = DAT['K']; meta = DAT['meta']
rng = np.random.default_rng(20261018)

def runs(c):
    cut = np.flatnonzero(c[1:] != c[:-1]) + 1
    st = np.concatenate([[0], cut]); return st, np.diff(np.concatenate([st, [len(c)]]))

print('== A. UR050 + UR055 como par de ceques ==')
nr = {k: len(runs(v['col'])[0]) for k, v in K.items()}
for k in ['UR050', 'UR055']:
    st, ln = runs(K[k]['col'])
    print(k, 'colgantes', len(K[k]['col']), 'rachas de color', len(st), 'largos', list(ln)[:40])
ref = [k for k, v in K.items() if 150 <= len(v['col']) <= 200 and k not in ('UR050', 'UR055')]
f1 = np.mean([15 <= nr[k] <= 21 for k in ref]); f2 = np.mean([20 <= nr[k] <= 26 for k in ref])
print(f'A1 nulo (n={len(ref)} quipus de 150-200 colgantes): P[15-21]={f1:.3f}, P[20-26]={f2:.3f}, par≈{2*f1*f2:.3f}')
a, b = nr['UR050'], nr['UR055']
A1 = (15 <= a <= 21 and 20 <= b <= 26) or (15 <= b <= 21 and 20 <= a <= 26)
print('A1 se cumple:', A1)
for k in ['UR050', 'UR055']:
    st, ln = runs(K[k]['col'])
    m = pd.factorize(K[k]['col'][st])[0]
    if len(m) >= 9:
        o = T.P9a(m[None, :])[0]
        null = T.P9a(rng.permuted(np.tile(m, (9999, 1)), axis=1))
        print(f'A2 {k}: P9a(rachas)={o:.3f}, p={(1+np.sum(null>=o))/10000:.4f}')
    else:
        print(f'A2 {k}: {len(m)} rachas, no evaluable')
print('A3', meta.loc[['UR050', 'UR055'], ['museo', 'procedencia']].to_string())
cl = pd.read_csv(OUT.parent / 'ds/n_no_numericos/quipus_clase.csv').set_index('kfg')
print(cl.loc[['UR050', 'UR055', 'UR054', 'UR052'], ['num_canuto_cords', 'f_CL', 'f_CN', 'ncuerdas']].to_string())


# ================= Parte C (prerregistrada en predicciones_preregistradas.md §C) =================
from collections import Counter
from scipy.stats import spearmanr
B = 9999
def eta_test(V, lab):
    ok = ~np.isnan(V); L = np.log10(V[ok] + 1); lab = np.asarray(lab)[ok]
    if len(L) < 6 or len(set(lab)) < 2: return np.nan, np.nan
    o = T._eta(L[None, :], lab)[0]
    null = T._eta(rng.permuted(np.tile(L, (B, 1)), axis=1), lab)
    return o, (1 + np.sum(null >= o - 1e-12)) / (1 + B)

def bands(k):
    c = k['col']; st, ln = runs(c)
    r = ln[(ln >= 4) & (ln <= 12)]
    if not len(r): return None, []
    u, n = np.unique(r, return_counts=True); kk = u[np.lexsort((u, n))[-1]]
    return kk, [np.arange(s, s + l) for s, l in zip(st, ln) if l == kk]

print('\n== C1. P4r: perfil de valores por posición dentro de la banda ==')
C1 = []
for k in ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092', 'UR028', 'UR1114', 'UR1140', 'HP033', 'UR1123']:
    kk, bs = bands(K[k])
    if not bs: print(k, 'sin bandas'); continue
    idx = np.concatenate(bs); pos = np.concatenate([np.arange(len(b)) for b in bs])
    o, p = eta_test(K[k]['vals'][idx], pos)
    C1.append(dict(khipu=k, largo_banda=kk, n_bandas=len(bs), eta2=o, p=p))
    print(f'{k}: banda={kk} n={len(bs)} eta2={o:.3f} p={p:.4f}')
pd.DataFrame(C1).to_csv(OUT / 'pred_C1.csv', index=False)

print('\n== C2. P9a: la fase del trío ordena los valores ==')
C2 = []
for k in ['UR053C', 'UR053A', 'UR053D', 'QU001', 'UR1033B', 'UR1099', 'UR210', 'UR218', 'AS089', 'HP051_B', 'UR1121', 'UR073']:
    v = K[k]['vals']; ph = np.arange(len(v)) % 3
    o, p = eta_test(v, ph)
    # fase cuyo color modal es W y fracción de tríos en que esa cuerda es la mayor
    col = K[k]['col']; fw = None; frac = np.nan
    for f in range(3):
        if Counter(col[ph == f]).most_common(1)[0][0] == 'W': fw = f
    if fw is not None:
        st = fw - 1 if fw >= 1 else 2  # inicio del trío = la fase anterior a W, como AB W RB
        tri = [np.arange(i, i + 3) for i in range(st, len(v) - 2, 3)]
        w = [np.nanargmax(v[t]) == 1 for t in tri if np.sum(~np.isnan(v[t])) == 3]
        frac = np.mean(w) if w else np.nan
    C2.append(dict(khipu=k, eta2_fase=o, p=p, fase_W=fw, frac_W_mayor=frac))
    print(f'{k}: eta2={o:.3f} p={p:.4f} faseW={fw} W mayor del trío={frac}')
pd.DataFrame(C2).to_csv(OUT / 'pred_C2.csv', index=False)

print('\n== C3. P11a/b: los bloques repetidos comparten perfil de valores ==')
def blocks(k):
    G = T.groups(k); c = k['col']; tup = [tuple(c[x]) for x in G]; best = []
    by = {}
    for i, t in enumerate(tup):
        if len(t) >= 3 and len(set(t)) > 1: by.setdefault(len(t), []).append(i)
    for L, ids in by.items():
        if len(ids) < 2: continue
        mod = np.array(Counter(tup[i] for i in ids).most_common(1)[0][0])
        sel = [G[i] for i in ids if np.mean(np.array(tup[i]) == mod) >= .8]
        if len(sel) > len(best): best = sel
    return best
def mean_rho(M):
    rs = []
    for i in range(len(M)):
        for j in range(i + 1, len(M)):
            ok = ~np.isnan(M[i]) & ~np.isnan(M[j])
            if ok.sum() >= 3 and np.ptp(M[i][ok]) > 0 and np.ptp(M[j][ok]) > 0:
                rs.append(spearmanr(M[i][ok], M[j][ok])[0])
    return np.mean(rs) if rs else np.nan
C3 = []
for k in ['UR1057', 'UR1131', 'HP055', 'AS202', 'UR1176', 'AS074', 'AS089', 'AS203', 'UR1099', 'UR1149', 'UR1175',
          'UR172', 'UR1088', 'AS048', 'AS178', 'HP051_B', 'UR1121', 'UR1144', 'UR068', 'UR006']:
    bl = blocks(K[k])
    if len(bl) < 2: print(k, 'sin bloques'); continue
    M = K[k]['vals'][np.array(bl)]
    o = mean_rho(M)
    cells = M[~np.isnan(M)]; mask = ~np.isnan(M)
    ident = np.mean([np.mean(M[i][mask[i] & mask[j]] == M[j][mask[i] & mask[j]])
                     for i in range(len(M)) for j in range(i + 1, len(M)) if (mask[i] & mask[j]).sum()])
    null = []
    for _ in range(999):
        X = M.copy(); X[mask] = rng.permutation(cells); null.append(mean_rho(X))
    null = np.array(null); p = (1 + np.sum(null >= o - 1e-12)) / 1000 if not np.isnan(o) else np.nan
    C3.append(dict(khipu=k, bloques=len(bl), largo=len(bl[0]), rho_medio=o, p=p, celdas_identicas=ident))
    print(f'{k}: {len(bl)} bloques de {len(bl[0])}; rho={o:.3f} p={p:.3f}; idénticas={ident:.2f}')
pd.DataFrame(C3).to_csv(OUT / 'pred_C3.csv', index=False)


# ================= Parte D (prerregistrada en predicciones_preregistradas.md §D) =================
import importlib.util
from scipy.stats import binomtest
spec = importlib.util.spec_from_file_location('p6b', OUT / '03_p6b.py'); P6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P6)

def best_alignment(kfg):
    k = K[kfg]; v0 = np.nan_to_num(k['vals']); best = (0, None)
    for j in P6.socios(kfg):
        vj = np.nan_to_num(K[j]['vals'])
        for L, idx in P6.plan(k):
            if len(vj) < L: continue
            S = v0[idx].sum(0); W = sw(vj, L)
            hit = ((S[None, :] == W) & (S[None, :] >= 1)).sum(1)
            i = int(hit.argmax())
            if hit[i] > best[0]: best = (int(hit[i]), (j, L, idx, i))
    return best
from numpy.lib.stride_tricks import sliding_window_view as sw
print('\n== C4. P6b fuera de Puruchuco ==')
for kfg in ['KH0033', 'UR044', 'QU013', 'UR068']:
    n, (j, L, idx, i) = best_alignment(kfg)
    k = K[kfg]; v0 = np.nan_to_num(k['vals']); vj = np.nan_to_num(K[j]['vals'])
    S = v0[idx].sum(0); W = vj[i:i + L]
    print(f'{kfg} -> {j}: L={L}, {idx.shape[0]} secciones desde colgante {idx[0,0]+1}, ventana {i+1}-{i+L}, coincidencias {n}')
    print('   suma :', S.astype(int).tolist()); print('   dest.:', W.astype(int).tolist())
    # copia trivial? valores idénticos k vs j en alineación directa
    m = min(len(v0), len(vj)); print(f'   identidad directa k/j: {np.mean(v0[:m]==vj[:m]):.2f}, tamaños {len(v0)}/{len(vj)}')
    # (i) subsidiarias
    s1 = k['s1']; s1j = K[j]['s1'][i:i + L]
    Ss = np.nan_to_num(s1)[idx].sum(0); ok = ~np.isnan(s1j) & (~np.isnan(s1[idx])).any(0)
    obs = int(np.sum((Ss == s1j) & ok & (Ss >= 1)))
    an = ~np.isnan(s1); null = []
    for _ in range(9999):
        x = np.nan_to_num(s1).copy(); x[an] = rng.permutation(x[an]); Sx = x[idx].sum(0)
        null.append(np.sum((Sx == s1j) & ok & (Sx >= 1)))
    print(f'   (i) subsidiarias: {obs}/{int(ok.sum())} posiciones, p={(1+np.sum(np.array(null)>=obs))/10000:.4f}')
    # (ii) fallos a ±10^j
    def near(a, b): d = np.abs(a - b); return (d > 0) & np.isin(d, [1, 10, 100, 1000])
    miss = (S != W) & (S >= 1)
    o2 = int(np.sum(near(S, W) & miss)); null2 = []
    anv = ~np.isnan(k['vals'])
    for _ in range(9999):
        x = v0.copy(); x[anv] = rng.permutation(v0[anv]); Sx = x[idx].sum(0)
        null2.append(np.sum(near(Sx, W) & (Sx != W) & (Sx >= 1)))
    print(f'   (ii) fallos a ±10^j: {o2}/{int(miss.sum())}, p={(1+np.sum(np.array(null2)>=o2))/10000:.4f}')

print('\n== C2b. ¿UR053A/C/D son copias? y binomial de «W mayor» ==')
for a, b in [('UR053A', 'UR053C'), ('UR053A', 'UR053D'), ('UR053C', 'UR053D'), ('UR053B', 'UR053C')]:
    va, vb = np.nan_to_num(K[a]['vals']), np.nan_to_num(K[b]['vals'])
    best = max(np.mean(va[max(0, -s):max(0, -s) + min(len(va) - max(0, -s), len(vb) - max(0, s))] ==
                       vb[max(0, s):max(0, s) + min(len(va) - max(0, -s), len(vb) - max(0, s))])
               for s in range(-len(va) + 5, len(vb) - 5))
    print(f'{a}/{b}: mejor fracción de valores idénticos con desfase = {best:.2f}')
for k in ['UR053A', 'UR053C', 'UR053D']:
    v = K[k]['vals']; col = K[k]['col']; ph = np.arange(len(v)) % 3
    fw = [f for f in range(3) if Counter(col[ph == f]).most_common(1)[0][0] == 'W'][0]
    st = fw - 1 if fw >= 1 else 2
    tri = [np.arange(i, i + 3) for i in range(st, len(v) - 2, 3)]
    w = [np.nanargmax(v[t]) == 1 for t in tri if np.sum(~np.isnan(v[t])) == 3]
    print(f'{k}: W mayor en {sum(w)}/{len(w)} tríos, binomial(1/3) p={binomtest(sum(w), len(w), 1/3, alternative="greater").pvalue:.2g}')
