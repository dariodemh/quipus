"""33 · Detalle, equipo rojo y nivel de cada par seleccionado (q<0,20 o p<1e-3) del barrido.
Uso: python 02_pares.py [fase]   (fase = todo por defecto)
Salidas: pares_detalle.csv, celdas_alineadas.csv, salida_02.txt"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

from comun import ESCALAS, GAP, KMAX, OUT, SEED, TAU, detalle, evaluar_pares, p_valor, preparar

FASE = sys.argv[1] if len(sys.argv) > 1 else 'todo'
N_RT = 199


def comunes(D):
    v = D['V']
    return set(pd.Series(v).value_counts().index[:10].tolist()) | {0}


def evaluar_sub(D, pares, filtro, modo):
    """p empírico de los pares con secuencias filtradas (filtro: fn(df)->máscara) y nulo `modo`."""
    seqs, idx = [], {}
    for a, b in pares:
        for k in (a, b):
            if k not in idx:
                s = D['seqs'][k]
                s = s[filtro(s)] if filtro else s
                idx[k] = len(seqs); seqs.append(s)
    off = np.cumsum([0] + [len(s) for s in seqs]).astype(np.int64)
    V = np.concatenate([s.v.values for s in seqs]).astype(np.int64)
    LV = np.concatenate([s.nivel.values for s in seqs]).astype(np.int64)
    ok = np.array([min(len(seqs[idx[a]]), len(seqs[idx[b]])) >= 3 for a, b in pares])
    pi = np.array([idx[a] for a, _ in pares], dtype=np.int64)
    pj = np.array([idx[b] for _, b in pares], dtype=np.int64)
    out = np.ones(len(pares))
    if ok.any():
        o, _, n = evaluar_pares(V, LV, off, pi[ok], pj[ok], N_RT, SEED + 7 + modo, ESCALAS, GAP, TAU, KMAX, modo)
        out[ok] = ((n >= o[:, None]).sum(1) + 1) / (N_RT + 1)
    return out


def main():
    D = preparar()
    r = pd.read_csv(os.path.join(OUT, f'barrido_{FASE}.csv.gz'))
    sel = r[(r.q < .2) | (r.p < 1e-3)].copy().reset_index(drop=True)
    kidx = {float(k): x for x, k in enumerate(ESCALAS)}
    filas, celdas = [], []
    for _, x in sel.iterrows():
        A, B = D['seqs'][x.A], D['seqs'][x.B]
        tot, nb, d = detalle(A.v.values.astype(np.int64), B.v.values.astype(np.int64), kidx[round(x.escala, 6)])
        k = x.escala
        va = A.v.values[d.i]
        vb = B.v.values[d.j]
        vbt = np.where(k >= 1, vb * round(k), np.where(vb % max(1, round(1 / k)) == 0, vb // max(1, round(1 / k)), -1)) if k != 1 else vb
        dif = np.abs(va - vbt)
        tol = np.isin(dif, [1, 10, 100, 1000, 10000])
        ex = dif == 0
        la, lb = A.largo.values[d.i], B.largo.values[d.j]
        m = ~(np.isnan(la) | np.isnan(lb))
        rl = stats.pearsonr(la[m], lb[m])[0] if m.sum() >= 5 and la[m].std() > 0 and lb[m].std() > 0 else np.nan
        dl = np.median(np.abs(la[m] - lb[m])) if m.sum() else np.nan
        # reordenamiento: orden de bloques en A frente a B, o sentidos distintos
        bl = d.groupby('bloque').agg(i=('i', 'mean'), j=('j', 'mean'), inv=('inverso', 'first'), n=('i', 'size'))
        bl = bl[bl.n >= 3]
        reord = len(bl) >= 2 and (stats.kendalltau(bl.i, bl.j)[0] < 1 or bl.inv.nunique() > 1)
        inv = bool(bl.inv.iloc[0]) if len(bl) else bool(d.inverso.iloc[0])
        gaps = (d.groupby('bloque').i.agg(lambda s: s.max() - s.min() + 1).sum() - len(d)) + \
               (d.groupby('bloque').j.agg(lambda s: s.max() - s.min() + 1).sum() - len(d))
        tr = []
        if reord:
            tr.append(f'reordenado({len(bl)} bloques)')
        tr.append('inverso' if inv and not reord else ('directo' if not reord else ''))
        if k != 1:
            tr.append(f'escala x{k:g}')
        if gaps > 0:
            tr.append(f'huecos {gaps}')
        if (tol & ~ex).any():
            tr.append(f'±1 nudo {int((tol & ~ex).sum())}')
        tr = '; '.join(t for t in tr if t)
        exv = va[ex]
        filas.append(dict(A=x.A, B=x.B, alineadas=len(d), exactas=int(ex.sum()), tolerantes=int((tol & ~ex).sum()),
                          discordantes=int((~tol).sum()), bloques=nb, reordenado=reord, inverso=inv, escala=k,
                          transformacion=tr, frac_exacta=ex.mean() if len(d) else 0,
                          cobertura_A=len(d) / len(A), cobertura_B=len(d) / len(B),
                          distintos_exactos=len(set(exv)), exactos_ge10=len(set(exv[exv >= 10])),
                          r_largo=rl, dif_med_largo=dl, mismo_objeto=bool(rl >= .9 and dl <= 2.5) if not np.isnan(rl) else False))
        dd = d.assign(A=x.A, B=x.B, cuerdaA=A.cuerda.values[d.i], cuerdaB=B.cuerda.values[d.j], vA=va, vB=vb,
                      nivelA=A.nivel.values[d.i], nivelB=B.nivel.values[d.j], colA=A.col.values[d.i],
                      colB=B.col.values[d.j], termA=A.terminacion.values[d.i], termB=B.terminacion.values[d.j],
                      largoA=la, largoB=lb)
        celdas.append(dd)
    det = pd.DataFrame(filas)
    sel = sel.merge(det, on=['A', 'B'], suffixes=('', '_d'))
    pares = list(zip(sel.A, sel.B))
    com = comunes(D)
    sel['p_sin_comunes'] = evaluar_sub(D, pares, lambda s: ~s.v.isin(com), 0)
    sel['p_bloques'] = evaluar_sub(D, pares, None, 1)
    sel['rt_diversidad'] = (sel.distintos_exactos >= 4) & (sel.exactos_ge10 >= 3)
    sel['rt_comunes'] = sel.p_sin_comunes < .01
    sel['rt_longitud'] = sel.alineadas >= 8
    sel['rt_bloques'] = sel.p_bloques < .05
    sel['rt_pasa'] = sel.rt_diversidad & sel.rt_comunes & sel.rt_longitud & sel.rt_bloques

    def nivel(x):
        if x.holm < .05 and x.rt_pasa:
            return 'bien apoyado'
        if x.q < .05 and x.rt_pasa:
            return 'apoyado'
        if x.q < .2:
            return 'propuesto'
        return 'especulativo' if x.p < 1e-3 else 'ninguno'
    sel['nivel'] = sel.apply(nivel, axis=1)
    sel.to_csv(os.path.join(OUT, f'pares_detalle_{FASE}.csv'), index=False, float_format='%.4g')
    pd.concat(celdas).to_csv(os.path.join(OUT, f'celdas_alineadas_{FASE}.csv'), index=False)
    cols = ['A', 'B', 'score', 'p', 'q', 'holm', 'alineadas', 'exactas', 'transformacion', 'r_largo', 'mismo_objeto',
            'p_sin_comunes', 'p_bloques', 'rt_pasa', 'nivel']
    txt = sel[cols].to_string()
    open(os.path.join(OUT, f'salida_02_{FASE}.txt'), 'w', encoding='utf-8').write(
        txt + '\n\n' + sel.nivel.value_counts().to_string())
    print(sel[cols].head(80).to_string()); print(sel.nivel.value_counts())


if __name__ == '__main__':
    main()
