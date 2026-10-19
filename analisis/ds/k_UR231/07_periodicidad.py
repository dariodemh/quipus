"""UR231: periodicidad de 14 grupos (plantilla de color) y alineacion de sets."""
import pandas as pd, numpy as np, json

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
RNG = np.random.default_rng(0)
g = pd.read_csv(OUT + 'grupos_resumen.csv')
col = g.color.astype(str).to_numpy()

def fam(c):
    c = c.split('(')[0]
    base = c.split(':')[0]
    brown = {'B', 'MB', 'HB', 'KB', 'AB', 'NB', 'LB', 'EB', 'GB', 'DB'}
    return 'BROWN' if base in brown else base

famv = np.array([fam(c) for c in col])

def matches(seq, lag, lo=0, hi=None):
    hi = len(seq) - lag if hi is None else hi
    return int(sum(seq[i] == seq[i + lag] for i in range(lo, min(hi, len(seq) - lag))))

print('=== exacto, todos los grupos ===')
table = {L: matches(col, L) for L in range(1, 79)}
print('top:', sorted(table.items(), key=lambda x: -x[1])[:6])
print('=== exacto, g=27..65 (sets C-F) ===')
tab2 = {L: matches(col, L, 27, 66) for L in range(1, 40)}
print('top:', sorted(tab2.items(), key=lambda x: -x[1])[:6])

def null_test(seq, lag, lo, hi, nperm=2000):
    obs = matches(seq, lag, lo, hi)
    nd = np.array([matches(RNG.permutation(seq), lag, lo, hi) for _ in range(nperm)])
    return obs, float(nd.mean()), float((1 + (nd >= obs).sum()) / (1 + nperm))

for name, seq in [('exacto', col), ('familia', famv)]:
    for lo, hi, lab in [(0, None, 'todos'), (27, 66, 'C-F')]:
        o, m, p = null_test(seq, 14, lo, hi)
        print(f'{name:8s} lag14 {lab:6s}: obs={o} nulo={m:.2f} p={p:.4f}')

# alineacion de sets: separadores en 8,22,36,50,64,78
sep = [8, 22, 36, 50, 64, 78]
print('\nAlineacion (posicion 1-based dentro del set que termina en el separador):')
for k, e in enumerate(sep):
    start = (sep[k - 1] + 1) if k > 0 else 0
    sub = g[(g.grupo >= start) & (g.grupo <= e)]
    d = sub[sub.nval > 0]
    print(f'set {start}-{e} (n={len(sub)}):', [(int(r.grupo), int(r.grupo - start + 1), r.color, int(r.nval)) for _, r in d.iterrows()])

print('\nPares 0D->12 consecutivos:', [(int(a), int(b)) for a, b in zip(g[g.color == '0D'].grupo, g[g.color == '0D'].grupo + 1)])
print('0D seguido de grupo de 12 con datos:', all(
    int(g.loc[g.grupo == gg + 1, 'n'].iloc[0]) == 12 and g.loc[g.grupo == gg + 1, 'nval'].iloc[0] >= 10
    for gg in g[g.color == '0D'].grupo))
