"""Controles estadisticos de la transcripcion.

(a) Coherencia valor <-> nudos: n.o de cuerdas cuyo valor escrito coincide con la suma
    posicional de los racimos transcritos. Nulo: permutar los valores DENTRO de cada
    ficha (10 000 permutaciones, semilla 20261017). p empirico por ficha y global.
(b) Relaciones jerarquicas: n.o de cuerdas madre cuyo valor = suma de los valores de
    todas sus descendientes. Nulo: permutar valores dentro del quipu.
(c) Fiabilidad de lectura: proporcion de celdas marcadas con '?'.
"""
import csv, glob, os, re, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r'(\d+)\s*([SLEB]{1,2})\s*\(')
RNG = np.random.default_rng(20261017)
NPERM = 10000


def clusters(s):
    return [int(m.group(1)) for m in PAT.finditer(s or '')]


def fits(cs, v):
    n = len(cs)
    if n == 0:
        return False
    if n == 1:
        return v in (cs[0], 10 * cs[0], 100 * cs[0])
    dec = sum(c * 10 ** (n - 1 - i) for i, c in enumerate(cs))
    rev = sum(c * 10 ** i for i, c in enumerate(cs))
    tu = cs[0] * 10 + sum(cs[1:])
    u = sum(cs)
    return v in (dec, rev, tu, u)


def load():
    fichas = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'transcripcion_*.csv'))):
        name = os.path.basename(f).replace('transcripcion_', '').replace('_record.csv', '')
        rows = list(csv.DictReader(open(f, encoding='utf-8')))
        fichas[name] = rows
    return fichas


def numeric(v):
    m = re.sub(r'[^0-9]', '', v or '')
    return int(m) if m else None


def holm(ps):
    items = sorted(ps.items(), key=lambda kv: kv[1])
    m = len(items)
    adj, prev = {}, 0.0
    for k, (name, p) in enumerate(items):
        a = min(1.0, (m - k) * p)
        a = max(a, prev)
        adj[name] = a
        prev = a
    return adj


def test_a(fichas):
    print('=== (a) valor escrito vs suma de nudos (nulo: permutar valores dentro de la ficha)')
    tot_obs = tot_exp = 0
    ps = {}
    for name, rows in fichas.items():
        cs = [clusters(r['nudos']) for r in rows]
        vs = [numeric(r['valor']) for r in rows]
        idx = [i for i in range(len(rows)) if len(cs[i]) >= 2 and vs[i] is not None]
        if not idx:
            continue
        obs = sum(fits(cs[i], vs[i]) for i in idx)
        pool = [vs[i] for i in idx]
        null = np.empty(NPERM, dtype=int)
        for k in range(NPERM):
            perm = RNG.permutation(pool)
            null[k] = sum(fits(cs[i], perm[j]) for j, i in enumerate(idx))
        p = (1 + (null >= obs).sum()) / (NPERM + 1)
        ps[name] = p
        tot_obs += obs
        tot_exp += null.mean()
        print(f'  {name}: observado {obs}/{len(idx)} = {100*obs/len(idx):.0f}%, '
              f'esperado por azar {null.mean():.2f} ({100*null.mean()/len(idx):.1f}%), p={p:.4f}')
    adj = holm(ps)
    print('  Holm (9 fichas con cuerdas de >=2 racimos):',
          ', '.join(f'{k}={v:.3f}' for k, v in adj.items()))
    print(f'  GLOBAL: {tot_obs} aciertos observados vs {tot_exp:.2f} esperados por azar')
    return ps


def subtree(rows, name):
    """nombres de todas las descendientes de `name` (prefijo jerarquico)."""
    return [r['cuerda'] for r in rows if r['cuerda'] != name and r['cuerda'].startswith(name + 's')]


def test_b(fichas):
    print('\n=== (b) madre = suma de sus descendientes (nulo: permutar valores dentro del quipu)')
    total_obs = 0
    total_tests = 0
    detalles = []
    pb = {}
    for name, rows in fichas.items():
        val = {r['cuerda']: numeric(r['valor']) for r in rows}
        pairs = []
        for r in rows:
            d = subtree(rows, r['cuerda'])
            if d and val[r['cuerda']] is not None and all(val[x] is not None for x in d):
                pairs.append((r['cuerda'], sum(val[x] for x in d)))
        if not pairs:
            continue
        obs = sum(val[m] == s for m, s in pairs)
        arr = np.array([val[r['cuerda']] for r in rows], dtype=float)
        names = [r['cuerda'] for r in rows]
        pos = {n: i for i, n in enumerate(names)}
        null = np.empty(NPERM, dtype=int)
        sub = [[pos[d] for d in subtree(rows, m)] for m, _ in pairs]
        mp = [pos[m] for m, _ in pairs]
        for k in range(NPERM):
            perm = RNG.permutation(arr)
            null[k] = sum(perm[mp[j]] == perm[sub[j]].sum() for j in range(len(pairs)))
        p = (1 + (null >= obs).sum()) / (NPERM + 1)
        total_obs += obs
        total_tests += len(pairs)
        for m, s in pairs:
            if val[m] == s:
                detalles.append((name, m, val[m], s))
        pb[name] = p
        print(f'  {name}: {obs}/{len(pairs)} madres cumplen (esperado {null.mean():.2f}), p={p:.3f}')
    adj = holm(pb)
    print('  Holm (7 quipus con madres):', ', '.join(f'{k}={v:.3f}' for k, v in adj.items()))
    print(f'  GLOBAL: {total_obs}/{total_tests} relaciones exactas; '
          f'prob. de coincidencia exacta por azar ~1/100 por prueba -> '
          f'p aproximada de tener >=1 = {1-(0.99**total_tests):.2f}')
    for d in detalles:
        print('   coincidencia:', d)


def test_a_sin_guiadas(fichas):
    print('\n=== (a-bis) sensibilidad: excluyendo lecturas guiadas por el valor escrito')
    obs = tot = 0
    for name, rows in fichas.items():
        for r in rows:
            if 'GUIADA POR EL VALOR' in (r['notas'] or ''):
                continue
            cs = clusters(r['nudos']); v = numeric(r['valor'])
            if len(cs) >= 2 and v is not None:
                tot += 1
                obs += fits(cs, v)
    print(f'  {obs}/{tot} = {100*obs/max(tot,1):.1f}% de coherencia sin las lecturas guiadas')


def test_c(fichas):
    print('\n=== (c) celdas dudosas marcadas con ?')
    cells = q = 0
    for name, rows in fichas.items():
        for r in rows:
            for k in ('nudos', 'color', 'largo', 'notas'):
                cells += 1
                if '?' in (r[k] or ''):
                    q += 1
            if (r['notas'] or '').startswith('SIN NUDOS'):
                pass
    print(f'  {q}/{cells} celdas con ? = {100*q/cells:.1f}%')


if __name__ == '__main__':
    fichas = load()
    test_a(fichas)
    test_a_sin_guiadas(fichas)
    test_b(fichas)
    test_c(fichas)
