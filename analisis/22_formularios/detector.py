"""22_formularios / detector: formulario con clave de reparto, nivel quipu (diseno.md §0-3).

Uso (desde la raíz del repo):  python analisis/22_formularios/detector.py
Salidas: quipus_detector.csv, salida_detector.txt (y lo importa archivos.py).
"""
import re, sys, itertools
from multiprocessing import Pool
import numpy as np, pandas as pd
from scipy import stats

AQ = 'analisis/22_formularios/'
SEED = 20261018
KS = range(2, 13)


def norm(s):
    return re.sub(r'\([^)]*\)', '', str(s)).strip()


def cargar():
    c = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
    q = pd.read_csv('analisis/datos/quipus.csv')
    ncu = c.groupby('kfg').size()
    p = c[c.nivel == 0].sort_values(['kfg', 'orden'])
    Q = {}
    for k, d in p.groupby('kfg', sort=False):
        cf = [norm(x) for x in d.color]
        Q[k] = dict(v=d.valor.fillna(0).to_numpy(float), cf=cf, cg=[x[:1] for x in cf],
                    g=d.grupo.to_numpy(), cu=d.cuerda.to_numpy(), n_cuerdas=int(ncu[k]))
    return Q, q


# ---------- candidatos ----------
def _valido(V):
    n, k = V.shape
    keep = V.sum(1) > 0
    V = V[keep]
    if len(V) < 3 or (len(V) - 1) * (k - 1) < 2 or (V == 0).mean() > 0.5:
        return None
    return keep


def candidatos(d, fams=('P', 'Cf', 'Cg')):
    """lista de (familia, clave, idx n×k) con idx = índices de colgantes en el quipu."""
    v, g = d['v'], d['g']
    # segmentos de grupo contiguos
    cortes = np.flatnonzero(np.r_[True, g[1:] != g[:-1], True])
    segs = list(zip(cortes[:-1], cortes[1:]))
    out, vistos = [], set()

    def add(fam, key, idx):
        idx = np.asarray(idx)
        keep = _valido(v[idx])
        if keep is None:
            return
        idx = idx[keep]
        h = idx.tobytes()
        if h in vistos:
            return
        vistos.add(h)
        out.append((fam, key, idx))

    if 'P' in fams:
        for k in KS:
            idx = [np.arange(a, b) for a, b in segs if b - a == k]
            if len(idx) >= 3:
                add('P', f'P{k}', np.array(idx))
    for fam, col in (('Cf', d['cf']), ('Cg', d['cg'])):
        if fam not in fams:
            continue
        for k in KS:
            occ = {}
            for a, b in segs:
                for s in range(a, b - k + 1):
                    occ.setdefault(tuple(col[s:s + k]), []).append(s)
            for m, st in occ.items():
                if len(st) < 3 or len(set(m)) < 2 or 'nan' in m or 'n' in m:  # desviación 1: color ausente
                    continue
                sel, fin = [], -1
                for s in st:
                    if s >= fin:
                        sel.append(s); fin = s + k
                if len(sel) >= 3:
                    add(fam, '|'.join(m), np.array(sel)[:, None] + np.arange(k))
    return out


# ---------- estadísticos ----------
def anova(V):
    Y = np.log1p(V)
    n, k = Y.shape
    gm = Y.mean()
    ssr = k * ((Y.mean(1) - gm) ** 2).sum()
    ssc = n * ((Y.mean(0) - gm) ** 2).sum()
    sse = max(((Y - gm) ** 2).sum() - ssr - ssc, 1e-9)
    dfe = (n - 1) * (k - 1)
    Fc = (ssc / (k - 1)) / (sse / dfe)
    Fr = (ssr / (n - 1)) / (sse / dfe)
    return stats.f.sf(Fc, k - 1, dfe), stats.f.sf(Fr, n - 1, dfe), Fr


def Frow_batch(Yb):
    """Yb: B×n×k -> F de fila por réplica."""
    B, n, k = Yb.shape
    gm = Yb.mean((1, 2), keepdims=True)
    ssr = k * ((Yb.mean(2, keepdims=True) - gm) ** 2).sum((1, 2))
    ssc = n * ((Yb.mean(1, keepdims=True) - gm) ** 2).sum((1, 2))
    sse = np.maximum(((Yb - gm) ** 2).sum((1, 2)) - ssr - ssc, 1e-9)
    return (ssr / (n - 1)) / (sse / ((n - 1) * (k - 1)))


def nulo2(V, rng, B=999):
    """barajar valores entre bloques, columna a columna; p de coescala."""
    Y = np.log1p(V)
    n, k = Y.shape
    obs = Frow_batch(Y[None])[0]
    perm = np.argsort(rng.random((B, n, k)), axis=1)
    Yb = np.take_along_axis(np.broadcast_to(Y, (B, n, k)), perm, axis=1)
    return (1 + (Frow_batch(Yb) >= obs - 1e-12).sum()) / (B + 1)


def perfil(V):
    Y = np.log1p(V)
    return (Y - Y.mean(1, keepdims=True)).mean(0)


def banderas(V):
    n, k = V.shape
    tot = V.sum(1, keepdims=True)
    suma = np.abs(V - (tot - V)) <= 1
    suma &= V > 0
    f_suma = suma.mean(0).max()
    d = np.diff(V, axis=1)
    mono = max((d <= 0).all(1).mean(), (d >= 0).all(1).mean()) if k >= 3 else np.nan
    iguales = np.mean([np.array_equal(a, b) for a, b in itertools.combinations(V, 2)])
    return dict(f_total_partes=f_suma, f_monotono=mono, f_filas_iguales=iguales,
                total_partes=f_suma >= .5, lista_ordenada=(mono >= .8) if k >= 3 else False,
                filas_casi_identicas=iguales >= .5)


def puntuar(d, cands):
    return np.array([anova(d['v'][idx])[0] for _, _, idx in cands])


def min_pC(d, rng):
    """nulo 1: barajar colores dentro del quipu y repetir la búsqueda cromática."""
    pm = rng.permutation(len(d['cf']))
    e = dict(d, cf=[d['cf'][i] for i in pm], cg=[d['cg'][i] for i in pm])
    cs = candidatos(e, fams=('Cf', 'Cg'))
    return puntuar(e, cs).min() if cs else 1.0


def min_p_todo(d, rng):
    """nulo 3: barajar valores entre todos los colgantes de nivel 0 (colores y grupos fijos), repetir búsqueda."""
    e = dict(d, v=d['v'][rng.permutation(len(d['v']))])
    cs = candidatos(e)
    return puntuar(e, cs).min() if cs else 1.0


def p_secuencial(f, obs, rng, R, Rmax=9999, h=10):
    """p de permutación min-p; R réplicas y, si p<=0.02, sigue en tandas hasta Rmax o h excedencias."""
    ex = sum(f(rng) <= obs for _ in range(R)); n = R
    if (1 + ex) / (n + 1) <= 0.02:
        while n < Rmax and ex < h:
            ex += sum(f(rng) <= obs for _ in range(500)); n += 500
    return (1 + ex) / (n + 1), n


def analizar_quipu(args):
    kfg, d, R1 = args
    rng = np.random.default_rng([SEED, sum(map(ord, kfg))])
    cands = candidatos(d)
    if not cands:
        return dict(kfg=kfg, n_cuerdas=d['n_cuerdas'], n_colg=len(d['v']), m=0)
    p = puntuar(d, cands)
    m = len(cands)
    i = int(np.argmin(p))
    # desviación 2: p_q por permutación min-p (nulo 3), porque el p paramétrico falló el control negativo
    p_perm, n_perm = p_secuencial(lambda g: min_p_todo(d, g), p[i] * (1 + 1e-9), rng, R1) if R1 else (np.nan, 0)
    esC = np.array([f != 'P' for f, _, _ in cands])
    iP = int(np.argmin(np.where(esC, 2, p))) if (~esC).any() else None
    iC = int(np.argmin(np.where(esC, p, 2))) if esC.any() else None
    r = dict(kfg=kfg, n_cuerdas=d['n_cuerdas'], n_colg=len(d['v']), m=m, p_param=min(1, m * p[i]), p_q=p_perm, n_perm=n_perm,
             fam=cands[i][0], clave=cands[i][1], k=cands[i][2].shape[1], n_bloques=len(cands[i][2]),
             p_col=p[i],
             pP=min(1, m * p[iP]) if iP is not None else np.nan, claveP=cands[iP][1] if iP is not None else '',
             pC=min(1, m * p[iC]) if iC is not None else np.nan, claveC=cands[iC][1] if iC is not None else '')
    if iC is not None and R1:
        r['p_n1'], _ = p_secuencial(lambda g: min_pC(d, g), p[iC] * (1 + 1e-9), rng, R1, Rmax=1999)
    for tag, j in (('', i), ('C_', iC), ('P_', iP)):
        if j is None:
            continue
        V = d['v'][cands[j][2]]
        _, pr, Fr = anova(V)
        r[tag + 'p_fila_param'] = pr
        r[tag + 'p_n2'] = nulo2(V, rng)
        sh = (V / V.sum(1, keepdims=True)).mean(0)
        r[tag + 'cuotas'] = '/'.join(f'{x:.2f}' for x in sh)
        r[tag + 'perfil'] = '/'.join(f'{x:.2f}' for x in perfil(V))
        r[tag + 'total_medio'] = V.sum(1).mean()
        r.update({tag + kk: vv for kk, vv in banderas(V).items()})
    return r


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    q = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    out = np.empty(n); out[o] = np.minimum(q, 1); return out


def holm(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    h = np.maximum.accumulate(p[o] * (n - np.arange(n)))
    out = np.empty(n); out[o] = np.minimum(h, 1); return out


def decidir(R):
    R = R.copy()
    t = R.m > 0
    R.loc[t, 'q_bh'] = bh(R.loc[t, 'p_q']); R.loc[t, 'holm'] = holm(R.loc[t, 'p_q'])
    # cromático necesita nulo 1; si no, baja a posicional si su mejor P también pasa BH con su p
    R.loc[t, 'qP_bh'] = bh(R.loc[t, 'pP'].fillna(1)); R.loc[t, 'qC_bh'] = bh(R.loc[t, 'pC'].fillna(1))
    R.loc[t, 'q_param'] = bh(R.loc[t, 'p_param'])
    def tipo(r):
        if not (r.m > 0 and r.q_bh < .05):
            return 'no'
        if r.fam == 'P':
            return 'posicional'
        if r.get('p_n1', 1) < .05:
            return 'cromatico'
        return 'posicional' if r.qP_bh < .05 else 'no'
    R['Q'] = R.apply(tipo, axis=1)
    def qplus(r):
        if r.Q == 'no': return False
        tag = '' if (r.Q == 'cromatico' or r.fam == 'P') else 'P_'
        return r.get(tag + 'p_n2', 1) < .05
    R['Qplus'] = R.apply(qplus, axis=1)
    return R


def barajar(Q, modo, rng):
    out = {}
    for k, d in Q.items():
        pm = rng.permutation(len(d['v']))
        if modo == 'N1':
            out[k] = dict(d, cf=[d['cf'][i] for i in pm], cg=[d['cg'][i] for i in pm])
        else:
            out[k] = dict(d, v=d['v'][pm])
    return out


if __name__ == '__main__':
    Q, q = cargar()
    lineas = []
    def say(*a):
        s = ' '.join(map(str, a)); print(s); lineas.append(s)
    with Pool(18) as pool:
        R = pd.DataFrame(pool.map(analizar_quipu, [(k, d, 199) for k, d in Q.items()], chunksize=4))
        R = decidir(R)
        R.to_csv(AQ + 'quipus_detector.csv', index=False)
        say(f'quipus con colgantes: {len(R)}; con >=1 candidato: {(R.m>0).sum()}; candidatos totales: {R.m.sum()}')
        say('Q por tipo:', R.Q.value_counts().to_dict(), '| Q+:', int(R.Qplus.sum()), '| Holm<.05:', int((R.holm < .05).sum()))
        say('\n== controles positivos ==')
        cols = ['kfg', 'm', 'fam', 'clave', 'n_bloques', 'p_q', 'p_param', 'n_perm', 'q_bh', 'holm', 'p_n1', 'Q', 'Qplus', 'cuotas', 'claveP', 'pP', 'P_cuotas', 'P_p_n2', 'claveC', 'pC', 'C_cuotas']
        say(R[R.kfg.isin(['UR278', 'UR270', 'UR053A', 'UR053C', 'UR053D', 'UR053B', 'UR053E'])][cols].to_string())
        for kf, pat in (('UR278', 'P9'), ('UR270', 'P9'), ('UR053A', 'W|R'), ('UR053C', 'W|R'), ('UR053D', 'W|R')):
            cs = candidatos(Q[kf]); ps = puntuar(Q[kf], cs)
            hit = [(f, ky, len(ix), f'{p:.2g}') for (f, ky, ix), p in zip(cs, ps) if ky.startswith(pat) or (pat == 'W|R' and ky in ('W|R|A', 'W|RL|AB', 'W|RB|AB'))]
            say(f'  {kf}: candidato control {pat}: {hit[:4]}  (m={len(cs)})')
        say('\n== controles negativos (corpus barajados, sin nulo 1; cuenta q_BH<.05) ==')
        rng = np.random.default_rng(SEED)
        for modo in ('N1', 'N3'):
            for rep in range(2):
                Qb = barajar(Q, modo, rng)
                Rb = decidir(pd.DataFrame(pool.map(analizar_quipu, [(k, d, 199) for k, d in Qb.items()], chunksize=4)))
                t = Rb.m > 0
                say(f'  {modo} rep{rep}: paramétrico q_BH<.05 {int((Rb.q_param<.05).sum())} | permutación: Q {Rb.Q.value_counts().to_dict()}; Holm<.05 {int((Rb.holm<.05).sum())}')
    open(AQ + 'salida_detector.txt', 'w', encoding='utf-8').write('\n'.join(lineas))
