"""Tareas 3 y 4: verificación de pares significativos, artefactos de base de datos y grafos de archivo.

Requiere haber corrido concordancias.py. Uso: python analisis/04_concordancias/archivos.py
Salidas en analisis/04_concordancias/resultados/:
  pares_significativos.csv   pares de la tarea 1 con q<0.05 (FDR global), clasificados
  alineamientos.txt          cuerdas alineadas de cada par significativo (para leerlas)
  archivo_<nombre>_aristas.csv  relaciones dentro de cada archivo (FDR por archivo)
  sumas_cuerda_a_cuerda.csv  tripletes B = A1 + A2 (cuerda a cuerda) por archivo, con p FWER
  totales_globales.csv       total de A presente como cuerda de B, por archivo
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from numba import njit

sys.path.insert(0, os.path.dirname(__file__))
import concordancias as C  # noqa: E402

OUT = C.OUT
ROOT = C.ROOT
SEED = 20261018


# ---------------------------------------------------------------- metadatos y artefactos
def metadatos():
    q = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'quipus.csv'))
    k = pd.read_csv(os.path.join(ROOT, 'data', 'external', 'open-khipu-repository', 'data',
                                 'okr-kh-numbers.csv'), encoding='utf-8-sig').replace(r'\s+', ' ', regex=True)
    nombres = {}
    for _, r in k.iterrows():
        for t in [r['OKR Number']] + re.split(r'[,/]', str(r['Other Names'])):
            t = t.strip().replace(' ', '_')
            if t and t != 'nan':
                nombres.setdefault(t, set()).add(r['OKR Number'])

    def kh(row):
        for t in [row.okr, row.kfg] + re.split(r'[/_]', str(row.okr)):
            t = str(t).replace(' ', '_')
            if t in nombres:
                return sorted(nombres[t])[0]
        return None

    q['kh'] = q.apply(kh, axis=1)
    k = k.set_index('OKR Number')
    q['coleccion'] = q.kh.map(k['Collection / Location'])
    q['n_coleccion'] = q.kh.map(k['Collection Number'])
    q['comentario_okr'] = q.kh.map(k['Comments'])
    # duplicados documentados en comentarios OKR ("duplicate of KHxxxx")
    dup_doc = set()
    for kh_, com in k['Comments'].dropna().items():
        for m in re.findall(r'KH\d{4}', com):
            if 'duplicate' in com.lower():
                dup_doc.add(frozenset((kh_, m)))
    return q.set_index('kfg'), dup_doc


def archivos(q):
    p = q.procedencia.fillna('')
    return {
        'Incahuasi': sorted(q.index[p.str.contains('Incahuasi')]),
        'Puruchuco': [f'UR0{i}' for i in range(60, 83)],  # Mackey: vasija de Puruchuco (OKR: Huaquerones)
        'Santa': [f'UR0{i}' for i in range(87, 93)],
        'Leymebamba': sorted(q.index[p.str.contains('Leymebamba')]),
        'Pachacamac': sorted(q.index[p.str.contains('Pachacamac')]),
    }


# ---------------------------------------------------------------- lectura de cuerdas alineadas
def leer_par(D, a, b, kind='dup'):
    sa, sb = D['seqs'][a], D['seqs'][b]
    if kind == 'dup':
        S = C.matriz_dup(sa.v.values, sb.v.values)
        rows = sa
    else:
        tot, grs = C.totales_grupo(D, a)
        S = C.matriz_sum(tot, sb.v.values)
        rows = pd.DataFrame(dict(cuerda=[f'grupo{g}' for g in grs], v=tot, color='', largo=np.nan,
                                 nudos=''))
    sc, sentido, path = C.traza(S, gap_b=C.GAP_B_SUM if kind == 'sum' else None)
    alin = []
    for i, j in path:
        ra = rows.iloc[i] if i is not None else None
        rb = sb.iloc[j] if j is not None else None
        alin.append((ra, rb))
    return sc, sentido, alin


def resumen_alineamiento(alin):
    ex = tol = mis = gaps = col = lar = nud = 0
    for ra, rb in alin:
        if ra is None or rb is None:
            gaps += 1
            continue
        d = abs(int(ra.v) - int(rb.v))
        if d == 0:
            ex += 1
        elif d in (1, 10, 100, 1000, 10000, 100000):
            tol += 1
        else:
            mis += 1
        col += str(ra.color) == str(rb.color)
        lar += pd.notna(ra.largo) and ra.largo == rb.largo
        nud += str(ra.nudos) == str(rb.nudos)  # incluye posiciones en cm
    n = ex + tol + mis
    # geometría: mismo objeto medido dos veces => largos y posición del 1.er nudo casi iguales
    pares = [(ra, rb) for ra, rb in alin if ra is not None and rb is not None]
    la = np.array([pd.to_numeric(ra.largo, errors='coerce') for ra, _ in pares], float)
    lb = np.array([pd.to_numeric(rb.largo, errors='coerce') for _, rb in pares], float)
    ka = np.array([_pos1(ra.nudos) for ra, _ in pares], float)
    kb = np.array([_pos1(rb.nudos) for _, rb in pares], float)
    ok = ~np.isnan(la) & ~np.isnan(lb)
    okk = ~np.isnan(ka) & ~np.isnan(kb)
    vals = [int(ra.v) for ra, rb in pares]
    return dict(valores_distintos=len(set(vals)), tramo_A=f'{pares[0][0].cuerda}-{pares[-1][0].cuerda}' if pares else '',
                tramo_B=f'{pares[0][1].cuerda}-{pares[-1][1].cuerda}' if pares else '',
                alineadas=n, exactas=ex, tolerantes=tol, discordantes=mis, huecos=gaps,
                frac_color_igual=col / max(n, 1), frac_largo_igual=lar / max(n, 1),
                frac_nudos_identicos=nud / max(n, 1),
                r_largo=np.corrcoef(la[ok], lb[ok])[0, 1] if ok.sum() > 3 else np.nan,
                dif_med_largo_cm=np.median(np.abs(la[ok] - lb[ok])) if ok.any() else np.nan,
                r_pos_nudo=np.corrcoef(ka[okk], kb[okk])[0, 1] if okk.sum() > 3 else np.nan,
                dif_med_pos_nudo_cm=np.median(np.abs(ka[okk] - kb[okk])) if okk.any() else np.nan)


def _pos1(nudos):
    m = re.search(r'\(([\d.]+),', str(nudos))
    return float(m.group(1)) if m else np.nan


def texto_alineamiento(a, b, sc, sentido, alin, fh):
    fh.write(f'\n=== {a} vs {b}  score={sc:.1f} bits  sentido={sentido}\n')
    for ra, rb in alin:
        fa = '-' if ra is None else f'{ra.cuerda:>9} {int(ra.v):>6} {str(ra.color):>8} {ra.largo!s:>5} {ra.nudos}'
        fb = '-' if rb is None else f'{rb.cuerda:>9} {int(rb.v):>6} {str(rb.color):>8} {rb.largo!s:>5} {rb.nudos}'
        fh.write(f'{fa:<70} | {fb}\n')


def clasificar(r, q, dup_doc):
    A, B = q.loc[r.A], q.loc[r.B]
    if A.kh is not None and A.kh == B.kh:
        return 'duplicado de base (mismo número KH)'
    if frozenset((A.kh, B.kh)) in dup_doc:
        return 'duplicado de base (documentado en OKR)'
    mismo_museo = str(A.coleccion) == str(B.coleccion)
    mismo_num = mismo_museo and str(A.n_coleccion) == str(B.n_coleccion) and pd.notna(A.n_coleccion)
    # geometría calibrada con los duplicados documentados (KH0033/UR044: r=1.00, 0 cm; AS125/UR247: r=0.92, 2 cm)
    if r.frac_nudos_identicos >= 0.5 or (r.r_largo >= 0.9 and r.dif_med_largo_cm <= 2.5):
        return 'probable mismo objeto registrado dos veces (no documentado)'
    if r.valores_distintos <= 4:
        return 'débil: baja diversidad (<=4 valores distintos en el tramo; posible artefacto de rachas)'
    if mismo_num:
        return 'copia dentro de un conjunto con el mismo n.º de inventario'
    return 'candidato a copia/versión'


# ---------------------------------------------------------------- sumas cuerda a cuerda (B = A1 + A2)
@njit(cache=True)
def _clave(x, y, z):
    return (x * 1000003 + y) * 1000003 + z


@njit(cache=True)
def tripletes(V, off, min_b):
    """Para cada (A1, B) y cada par de ventanas de 3 cuerdas (x en A1, z en B, z>=min_b, z-x>=1),
    busca una ventana de A2 (A2 != A1, B) igual a z-x y extiende la racha exacta. Devuelve filas
    (A1, A2, B, i1, i2, ib, largo) con largo>=3, sólo la racha máxima por triplete."""
    nq = off.shape[0] - 1
    keys = []
    who = []
    pos = []
    for q in range(nq):
        for s in range(off[q], off[q + 1] - 2):
            keys.append(_clave(V[s], V[s + 1], V[s + 2])); who.append(q); pos.append(s - off[q])
    K = np.array(keys); W = np.array(who); P = np.array(pos)
    o = np.argsort(K)
    K = K[o]; W = W[o]; P = P[o]
    best = {}
    for b in range(nq):
        for a1 in range(nq):
            if a1 == b:
                continue
            for zb in range(off[b], off[b + 1] - 2):
                if V[zb] < min_b or V[zb + 1] < min_b or V[zb + 2] < min_b:
                    continue
                for xa in range(off[a1], off[a1 + 1] - 2):
                    d0 = V[zb] - V[xa]; d1 = V[zb + 1] - V[xa + 1]; d2 = V[zb + 2] - V[xa + 2]
                    if d0 < 1 or d1 < 1 or d2 < 1:
                        continue
                    key = _clave(d0, d1, d2)
                    lo = np.searchsorted(K, key)
                    while lo < K.shape[0] and K[lo] == key:
                        a2 = W[lo]
                        if a2 != a1 and a2 != b and a1 < a2:
                            # extender
                            L = 3
                            p2 = off[a2] + P[lo]
                            while (zb + L < off[b + 1] and xa + L < off[a1 + 1] and p2 + L < off[a2 + 1]
                                   and V[zb + L] == V[xa + L] + V[p2 + L] and V[zb + L] > 0):
                                L += 1
                            t = (a1, a2, b)
                            if t not in best or best[t][3] < L:
                                best[t] = (zb - off[b], xa - off[a1], P[lo], L)
                        lo += 1
    out = np.zeros((len(best), 7), dtype=np.int64)
    k = 0
    for t, v in best.items():
        out[k, 0] = t[0]; out[k, 1] = t[1]; out[k, 2] = t[2]
        out[k, 3] = v[1]; out[k, 4] = v[2]; out[k, 5] = v[0]; out[k, 6] = v[3]
        k += 1
    return out


def sumas_cuerda_a_cuerda(D, miembros, nperm=100, min_b=10):
    ids = [m for m in miembros if m in D['seqs']]
    seqs = [D['seqs'][m].v.values.astype(np.int64) for m in ids]
    off = np.cumsum([0] + [len(s) for s in seqs]).astype(np.int64)
    obs = tripletes(np.concatenate(seqs), off, min_b)
    rng = np.random.default_rng(SEED)
    maxnull = []
    for _ in range(nperm):
        sh = np.concatenate([rng.permutation(s) for s in seqs])
        r = tripletes(sh, off, min_b)
        maxnull.append(r[:, 6].max() if len(r) else 0)
    maxnull = np.array(maxnull)
    df = pd.DataFrame(obs, columns=['A1', 'A2', 'B', 'pos_A1', 'pos_A2', 'pos_B', 'racha'])
    for c in ('A1', 'A2', 'B'):
        df[c] = [ids[i] for i in df[c]]
    df['p_fwer'] = [((maxnull >= L).sum() + 1) / (nperm + 1) for L in df.racha]
    return df.sort_values('racha', ascending=False), maxnull


# ---------------------------------------------------------------- totales globales
def totales_globales(D, miembros, todos, nperm=2000):
    """¿El total de colgantes de A (>=10) aparece como cuerda de B? Nulo: totales de quipus ajenos al
    archivo, sorteados en igual número."""
    tot = {}
    for k in todos:
        s = D['seqs'][k]
        tot[k] = int(s[s.nivel == 0].v.sum())
    ids = [m for m in miembros if m in D['seqs']]
    vals = {m: set(D['seqs'][m].v.values.tolist()) for m in ids}

    def cuenta(asig):
        return sum(1 for a, t in asig.items() for b in ids if b != a and t >= 10 and t in vals[b])

    obs_list = [(a, b, tot[a]) for a in ids for b in ids if a != b and tot[a] >= 10 and tot[a] in vals[b]]
    ajenos = np.array([tot[k] for k in todos if k not in set(ids)])
    rng = np.random.default_rng(SEED)
    null = [cuenta(dict(zip(ids, rng.choice(ajenos, len(ids), replace=False)))) for _ in range(nperm)]
    p = (np.sum(np.array(null) >= len(obs_list)) + 1) / (nperm + 1)
    return obs_list, len(obs_list), float(np.mean(null)), p


# ---------------------------------------------------------------- principal
def main():
    D = C.preparar()
    q, dup_doc = metadatos()
    r1 = pd.read_csv(os.path.join(OUT, 'pares_duplicados_todos.csv.gz'))
    r2 = pd.read_csv(os.path.join(OUT, 'pares_resumen_todos.csv.gz'))
    r3 = pd.read_csv(os.path.join(OUT, 'pares_duplicados_valores100.csv.gz'))

    # ---- tarea 1 + 4: pares significativos (FDR global) verificados
    sig = r1[r1.q < 0.05].sort_values('p').copy()
    filas = []
    with open(os.path.join(OUT, 'alineamientos.txt'), 'w', encoding='utf-8') as fh:
        for _, r in sig.iterrows():
            sc, sentido, alin = leer_par(D, r.A, r.B)
            texto_alineamiento(r.A, r.B, sc, sentido, alin, fh)
            filas.append(dict(sentido=sentido, **resumen_alineamiento(alin)))
    sig = pd.concat([sig.reset_index(drop=True), pd.DataFrame(filas)], axis=1)
    # rango del par entre los compañeros de A y de B (control de "quipus que se parecen a todo")
    for col, other in (('A', 'B'), ('B', 'A')):
        rk = []
        for _, r in sig.iterrows():
            k = r[col]
            fila = r1[(r1.A == k) | (r1.B == k)]
            rk.append(int((fila.p < r.p).sum()) + 1)
        sig[f'rango_en_{col}'] = rk
    for c in ('procedencia', 'museo', 'kh', 'n_coleccion'):
        sig[f'{c}_A'] = sig.A.map(q[c]); sig[f'{c}_B'] = sig.B.map(q[c])
    sig['clase'] = [clasificar(r, q, dup_doc) for _, r in sig.iterrows()]
    sig.to_csv(os.path.join(OUT, 'pares_significativos.csv'), index=False, float_format='%.3g')
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
    print(sig[['A', 'B', 'nA', 'nB', 'score', 'p', 'q', 'p_bloque', 'alineadas', 'exactas', 'tolerantes',
               'discordantes', 'huecos', 'frac_color_igual', 'frac_nudos_identicos', 'rango_en_A', 'rango_en_B',
               'sentido', 'clase']].to_string())
    print(sig[['A', 'B', 'tramo_A', 'tramo_B', 'r_largo', 'dif_med_largo_cm', 'r_pos_nudo', 'dif_med_pos_nudo_cm']].round(2).to_string())
    print(sig[['A', 'B', 'kh_A', 'kh_B', 'procedencia_A', 'procedencia_B', 'museo_A', 'museo_B',
               'n_coleccion_A', 'n_coleccion_B']].to_string())

    # ---- tarea 2: mejores pares de resumen (global)
    print('\nTarea 2, mejores 15 (FDR global):')
    print(r2.sort_values('p').head(15).to_string())

    # ---- tarea 3: archivos
    arch = archivos(q)
    todos = D['ids']
    resumen = []
    with open(os.path.join(OUT, 'alineamientos_archivos.txt'), 'w', encoding='utf-8') as fh:
        for nombre, miembros in arch.items():
            m = set(miembros) & set(D['seqs'])
            a1 = r1[r1.A.isin(m) & r1.B.isin(m)].copy()
            a1['q_archivo'] = C.bh(a1.p.values)
            a2 = r2[r2.A_totales.isin(m) & r2.B_cuerdas.isin(m)].copy()
            a2['q_archivo'] = C.bh(a2.p.values)
            e1 = a1[a1.q_archivo < 0.05].assign(tipo='copia/versión').rename(columns={'A': 'origen', 'B': 'destino'})
            a3 = r3[r3.A.isin(m) & r3.B.isin(m)].copy()
            a3['q_archivo'] = C.bh(a3.p.values) if len(a3) else []
            e3 = a3[a3.q_archivo < 0.05].assign(tipo='copia/versión (sólo valores>=100)').rename(
                columns={'A': 'origen', 'B': 'destino'})
            a2['q_archivo_orden'] = C.bh(a2.p_orden.values)
            e2 = a2[(a2.q_archivo < 0.05) & (a2.q_archivo_orden < 0.05)].assign(tipo='totales de grupo de origen = cuerdas de destino').rename(
                columns={'A_totales': 'origen', 'B_cuerdas': 'destino'})
            for _, r in e1.iterrows():
                sc, sentido, alin = leer_par(D, r.origen, r.destino)
                texto_alineamiento(r.origen, r.destino, sc, sentido, alin, fh)
            for _, r in e2.iterrows():
                sc, sentido, alin = leer_par(D, r.origen, r.destino, kind='sum')
                texto_alineamiento('totales ' + r.origen, r.destino, sc, sentido, alin, fh)
            ar = pd.concat([e1, e3, e2])[['tipo', 'origen', 'destino', 'score', 'p', 'p_emp', 'p_bloque', 'q', 'q_archivo',
                                          'p_orden', 'q_archivo_orden']]
            ar.to_csv(os.path.join(OUT, f'archivo_{nombre}_aristas.csv'), index=False, float_format='%.3g')
            trip, maxnull = sumas_cuerda_a_cuerda(D, miembros)
            trip.assign(archivo=nombre).to_csv(os.path.join(OUT, f'sumas_cuerda_a_cuerda_{nombre}.csv'),
                                               index=False)
            obs_list, n_obs, n_null, p_tot = totales_globales(D, miembros, todos)
            pd.DataFrame(obs_list, columns=['A_total', 'B_contiene', 'total']).to_csv(
                os.path.join(OUT, f'totales_globales_{nombre}.csv'), index=False)
            print(f'\n##### {nombre}: {len(m)} quipus con datos ({len(miembros)} listados); '
                  f'pares {len(a1)}, ordenados tarea 2 {len(a2)}')
            print(ar.to_string() if len(ar) else '  sin aristas q_archivo<0.05')
            print('  mejores 5 tarea 1 dentro del archivo:')
            print(a1.sort_values('p').head(5)[['A', 'B', 'nA', 'nB', 'score', 'p', 'p_bloque', 'q_archivo']].to_string())
            print('  mejores 5 tarea 2 dentro del archivo:')
            print(a2.sort_values('p').head(5)[['A_totales', 'B_cuerdas', 'n_totales', 'score', 'p', 'q_archivo', 'p_orden',
                                               'q_archivo_orden']].to_string())
            print(f'  sumas cuerda a cuerda: racha máx observada {trip.racha.max() if len(trip) else 0}, '
                  f'nulo máx: mediana {np.median(maxnull)}, p95 {np.percentile(maxnull, 95)}')
            print(trip.head(5).to_string())
            print(f'  totales globales en cuerdas de otro quipu: {n_obs} (nulo medio {n_null:.2f}), p={p_tot:.3g}')
            print('  ', obs_list[:10])
            resumen.append(dict(archivo=nombre, quipus=len(m), pares=len(a1), aristas_copia=len(e1),
                                aristas_copia_v100=len(e3),
                                aristas_resumen=len(e2), racha_suma_max=trip.racha.max() if len(trip) else 0,
                                p_racha=trip.p_fwer.min() if len(trip) else 1, totales_obs=n_obs,
                                totales_nulo=n_null, p_totales=p_tot))
    pd.DataFrame(resumen).to_csv(os.path.join(OUT, 'resumen_archivos.csv'), index=False, float_format='%.3g')
    print(pd.DataFrame(resumen).to_string())


if __name__ == '__main__':
    main()
