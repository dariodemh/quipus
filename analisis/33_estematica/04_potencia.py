"""33 · Potencia: copias sembradas en quipus reales (diseño §10).
Se copia un tramo de L cuerdas de un quipu donante dentro de un receptor de otro sitio, con 10 % de
errores ±1 nudo y 10 % de omisiones, partido en dos bloques intercambiados; variantes: tal cual,
invertido, escala ×10. p con 199 permutaciones por nivel + cola de Gumbel; umbral Holm del barrido.
Salida: potencia.csv, salida_04.txt"""
import os

import numpy as np
import pandas as pd

from comun import ESCALAS, GAP, KMAX, OUT, SEED, TAU, evaluar_pares, p_valor, preparar

NPARES = 201930  # se sobrescribe con el del barrido si existe
REPS, NP = 30, 199


def main():
    D = preparar()
    q = pd.read_csv(os.path.join(os.path.dirname(OUT), 'datos/quipus.csv')).set_index('kfg')
    rng = np.random.default_rng(SEED + 4)
    ids = [k for k in D['ids'] if len(D['seqs'][k]) >= 30]
    seqs, filas = [], []
    for L in (5, 8, 12, 20):
        for var in ('reordenado', 'inverso', 'escala10'):
            for r in range(REPS):
                while True:
                    a, b = rng.choice(ids, 2, replace=False)
                    pa, pb = q.procedencia.get(a, 'Unknown'), q.procedencia.get(b, 'Unknown')
                    if pa != pb or pa == 'Unknown':
                        break
                A, B = D['seqs'][a], D['seqs'][b]
                s = rng.integers(0, len(A) - L + 1)
                tramo = A.v.values[s:s + L].copy()
                err = rng.random(L) < .10
                tramo[err] = np.maximum(1, tramo[err] + rng.choice([-1, 1], err.sum()) * 10 ** rng.integers(0, 2, err.sum()))
                tramo = tramo[rng.random(L) >= .10]
                h = len(tramo) // 2
                if var == 'reordenado':
                    tramo = np.concatenate((tramo[h:], tramo[:h]))
                elif var == 'inverso':
                    tramo = tramo[::-1]
                else:
                    tramo = tramo * 10
                vb = B.v.values.copy()
                t = rng.integers(0, len(vb) - len(tramo) + 1)
                vb[t:t + len(tramo)] = tramo
                seqs += [(A.v.values, A.nivel.values), (vb, B.nivel.values)]
                filas.append(dict(L=L, variante=var, A=a, B=b))
    off = np.cumsum([0] + [len(s[0]) for s in seqs]).astype(np.int64)
    V = np.concatenate([s[0] for s in seqs]).astype(np.int64)
    LV = np.concatenate([s[1] for s in seqs]).astype(np.int64)
    pi = np.arange(0, len(seqs), 2, dtype=np.int64)
    o, kb, n = evaluar_pares(V, LV, off, pi, pi + 1, NP, SEED + 5, ESCALAS, GAP, TAU, KMAX, 0)
    p, _ = p_valor(o, n)
    f = pd.DataFrame(filas).assign(score=o, escala=ESCALAS[kb], p=p)
    try:
        npares = len(pd.read_csv(os.path.join(OUT, 'division.csv')))
        npares = npares * (npares - 1) // 2
    except FileNotFoundError:
        npares = NPARES
    f['holm_ok'] = f.p < .05 / npares
    f['p_1e4'] = f.p < 1e-4
    f.to_csv(os.path.join(OUT, 'potencia.csv'), index=False, float_format='%.4g')
    t = f.groupby(['variante', 'L'])[['holm_ok', 'p_1e4']].mean().unstack(0)
    open(os.path.join(OUT, 'salida_04.txt'), 'w', encoding='utf-8').write(
        f'umbral Holm 0,05/{npares}\n' + t.to_string())
    print(t)


if __name__ == '__main__':
    main()
