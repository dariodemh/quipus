"""Tarea 4: verificación dirigida de las relaciones de resumen halladas (lectura directa de cuerdas).

Uso: python analisis/04_concordancias/verificacion.py
Para cada relación A(totales de grupo) -> B: lista los totales de A y las cuerdas de B que coinciden,
cuenta coincidencias exactas/±1 dígito en orden (subsecuencia común más larga) y compara con un nulo
que baraja los colgantes de A entre posiciones conservando el tamaño de los grupos (10 000 veces).
Además, para Puruchuco: cabeceras (valores >=100) de UR063 frente a UR073 y UR078.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import concordancias as C  # noqa: E402

SEED = 20261019
TOL = {0, 1, 10, 100, 1000, 10000}


def lcs_tol(x, y):
    """Longitud de la subsecuencia común más larga con coincidencia exacta o ±1 en un dígito."""
    n, m = len(x), len(y)
    H = np.zeros((n + 1, m + 1), dtype=np.int32)
    for i in range(n):
        for j in range(m):
            H[i + 1, j + 1] = H[i, j] + 1 if abs(int(x[i]) - int(y[j])) in TOL else max(H[i, j + 1], H[i + 1, j])
    return int(H[n, m])


def relacion(D, a, b, nperm=10000, umbral=100):
    seq_b = D['seqs'][b]
    vb = seq_b.v.values
    tot, grs = C.totales_grupo(D, a)
    sel = tot >= umbral  # totales informativos (los pequeños coinciden por azar)
    obs = lcs_tol(tot[sel], vb)
    i = D['ids'].index(a)
    sl = slice(D['poff'][i], D['poff'][i + 1])
    pv, gid = D['PV'][sl], D['GID'][sl]
    rng = np.random.default_rng(SEED)
    null = np.empty(nperm, dtype=int)
    for r in range(nperm):
        t = C._totales(rng.permutation(pv), gid, D['NG'][i])
        null[r] = lcs_tol(t[t >= umbral], rng.permutation(vb))
    p = (np.sum(null >= obs) + 1) / (nperm + 1)
    detalle = []
    for g, t in zip(grs, tot):
        hit = seq_b[np.isin(np.abs(seq_b.v.values - t), list(TOL))]
        detalle.append(f'g{g}={t}->' + (','.join(f'{c}:{v}' for c, v in zip(hit.cuerda, hit.v)) or '·'))
    return dict(A=a, B=b, n_totales=int(sel.sum()), lcs=obs, null_media=null.mean(), null_max=null.max(),
                p=p), detalle


def cabeceras(D, a, b, pool_ids, nperm=10000, umbral=100):
    """LCS tolerante entre los valores >=umbral de a y b; nulo: valores de b sustituidos por
    valores >=umbral sorteados del resto del archivo (misma cantidad)."""
    xa = D['seqs'][a].v.values; xa = xa[xa >= umbral]
    xb = D['seqs'][b].v.values; xb = xb[xb >= umbral]
    pool = np.concatenate([D['seqs'][k].v.values for k in pool_ids if k not in (a, b) and k in D['seqs']])
    pool = pool[pool >= umbral]
    obs = lcs_tol(xa, xb)
    rng = np.random.default_rng(SEED)
    null = np.array([lcs_tol(xa, rng.choice(pool, len(xb), replace=False)) for _ in range(nperm)])
    return dict(A=a, B=b, cab_A=list(map(int, xa)), cab_B=list(map(int, xb)), lcs=obs,
                null_media=null.mean(), p=(np.sum(null >= obs) + 1) / (nperm + 1))


def main():
    D = C.preparar()
    filas = []
    for a, b in [('UR278', 'UR266'), ('UR278', 'UR275'), ('UR270', 'UR274B'), ('UR1034', 'UR1145'),
                 ('UR004', 'UR011'), ('UR004', 'UR006'), ('UR004', 'UR021')]:
            for umbral in (1, 100):
                r, det = relacion(D, a, b, nperm=2000, umbral=umbral)
                r['umbral'] = umbral
                filas.append(r)
                if umbral == 1:
                    print(f'\n{a} -> {b}:', ' '.join(det))
    df = pd.DataFrame(filas)
    print(df.to_string())
    df.to_csv(os.path.join(C.OUT, 'verificacion_resumen.csv'), index=False, float_format='%.4g')

    # UR266: ¿la cuerda cabecera de cada grupo = suma del resto del grupo? (estructura interna)
    s = D['seqs']['UR266']
    s0 = s[s.nivel == 0]
    ok = tot = 0
    for g, x in s0.groupby('grupo'):
        if len(x) >= 3:
            tot += 1
            ok += int(x.v.iloc[0] == x.v.iloc[1:].sum())
    print(f'\nUR266: grupos (>=3 colgantes anudados) cuya 1.a cuerda = suma del resto: {ok}/{tot}')
    s = D['seqs']['UR274B']
    v = s[s.nivel == 0].v.values
    trip = [(v[i], v[i + 1], v[i + 2]) for i in range(len(v) - 2) if v[i] >= 100 and v[i] == v[i + 1] + v[i + 2]]
    print('UR274B: tríos consecutivos con x = y + z (x>=100):', trip)

    puru = [f'UR0{i}' for i in range(60, 83)]
    for a, b in [('UR063', 'UR073'), ('UR063', 'UR078'), ('UR064', 'UR068'), ('UR066', 'UR067')]:
        print(cabeceras(D, a, b, puru))


if __name__ == '__main__':
    main()
