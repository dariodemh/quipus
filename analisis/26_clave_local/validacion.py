"""26_clave_local / validación de la invariancia (diseno.md §2).

Pares del mismo contenido transcritos por dos personas (14_copias/filas_alineadas.csv). ¿Coinciden las particiones,
los patrones R1/R2 y los descriptores R3 aunque las etiquetas no coincidan?
Uso: python analisis/26_clave_local/validacion.py      Salidas: validacion.csv, salida_validacion.txt
"""
import sys, itertools
sys.path.insert(0, 'analisis/26_clave_local')
from comun26 import *  # noqa
from detector import norm
from scipy import stats

L = []
def say(*a):
    s = ' '.join(map(str, a)); print(s); L.append(s)


def ari(x, y):
    t = pd.crosstab(pd.Series(x), pd.Series(y)).to_numpy()
    c2 = lambda v: (v * (v - 1) / 2).sum()
    n = t.sum(); sij, sa, sb = c2(t), c2(t.sum(1)), c2(t.sum(0)); e = sa * sb / (n * (n - 1) / 2)
    return (sij - e) / (0.5 * (sa + sb) - e) if 0.5 * (sa + sb) != e else np.nan


def kappa(x, y):
    x, y = np.asarray(x, bool), np.asarray(y, bool)
    po = (x == y).mean(); pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


Q, _ = cargar()
REP, R3 = cargar_reps()
F = pd.read_csv('analisis/14_copias/filas_alineadas.csv')
F = F[(F.nivel_A == 0) & (F.nivel_B == 0) & F.cuerda_A.notna() & F.cuerda_B.notna()].copy()
F['cA'], F['cB'] = F.color_A.map(norm), F.color_B.map(norm)
F = F[(F.cA != 'nan') & (F.cB != 'nan')]
filas = []
for (a, b), d in F.groupby(['A', 'B'], sort=False):
    n = len(d)
    if n < 6: continue
    xa, xb = d.cA.to_numpy(), d.cB.to_numpy()
    ex = (xa == xb).mean(); ar = ari(xa, xb)
    chA, chB = xa[1:] != xa[:-1], xb[1:] != xb[:-1]; ka = kappa(chA, chB)
    nul_ari = [ari(xa, np.roll(xb, s)) for s in range(1, n)]
    nul_ka = [kappa(chA, np.roll(chB, s)) for s in range(1, n - 1)]
    sentido = d.sentido.iloc[0]
    da, db = Q.get(a), Q.get(b)
    fila = dict(A=a, B=b, invA=inv(a), invB=inv(b), cruzado=inv(a) != inv(b), sentido=sentido, n_alineadas=n,
                n_colores_A=len(set(xa)), n_colores_B=len(set(xb)), etiqueta_exacta=ex,
                ARI=ar, ARI_nulo=np.nanmean(nul_ari), p_ARI=(1 + np.sum(np.array(nul_ari) >= ar)) / n,
                kappa_cambio=ka, kappa_nulo=np.nanmean(nul_ka), p_kappa=(1 + np.sum(np.array(nul_ka) >= ka)) / (n - 1))
    if da is not None and db is not None:
        ra = representar(da); rb = representar(invertir(db) if sentido == 'inverso' else db)
        for R in ('R1', 'R2'):
            sh, co = concord(ra[R], rb[R])
            fila.update({f'{R}_nA': len(ra[R]), f'{R}_nB': len(rb[R]), f'{R}_comparte': sh, f'{R}_concuerda': co,
                         f'{R}_dmin': min([np.linalg.norm(ra[R][t][0] - rb[R][t][0]) for t in ra[R] if t in rb[R]], default=np.nan)})
        for x in ('bandas', 'cabecera'):
            fila[f'{x}_A'], fila[f'{x}_B'] = ra[x], rb[x]
    filas.append(fila)
V = pd.DataFrame(filas)
V.to_csv(A26 + 'validacion.csv', index=False)
pd.set_option('display.width', 250)
say('== pares alineados (≥ 6 colgantes de nivel 0 con color en ambos) ==')
say(V[['A', 'B', 'invA', 'invB', 'sentido', 'n_alineadas', 'n_colores_A', 'n_colores_B', 'etiqueta_exacta', 'ARI', 'ARI_nulo', 'p_ARI',
       'kappa_cambio', 'kappa_nulo', 'p_kappa', 'R1_nA', 'R1_nB', 'R1_comparte', 'R1_concuerda', 'R1_dmin', 'R2_comparte', 'R2_concuerda', 'R2_dmin']].round(3).to_string())

C = V[V.cruzado]
say(f'\n== pares con investigadores distintos: {len(C)} ==')
for m in ('etiqueta_exacta', 'ARI', 'kappa_cambio'):
    nul = {'ARI': 'ARI_nulo', 'kappa_cambio': 'kappa_nulo'}.get(m)
    if nul:
        dd = (C[m] - C[nul]).dropna()
        say(f'  {m}: mediana {C[m].median():.3f} (nulo {C[nul].median():.3f}); > nulo en {(dd > 0).sum()}/{len(dd)}; Wilcoxon p = {stats.wilcoxon(dd, alternative="greater").pvalue:.3g}; pares con p<.05: {(C["p_" + ("ARI" if m == "ARI" else "kappa")] < .05).sum()}')
    else:
        say(f'  {m}: mediana {C[m].median():.3f}')
# concordancia de quipu frente a pares al azar con el mismo par de investigadores
base = {}
for R in ('R1', 'R2'):
    ks = list(REP[R]); tot = {}
    for a, b in itertools.combinations(ks, 2):
        key = frozenset((inv(a), inv(b))); s = tot.setdefault(key, [0, 0])
        s[0] += concord(REP[R][a], REP[R][b])[1]; s[1] += 1
    base[R] = tot
for R in ('R1', 'R2'):
    X = C[C[f'{R}_nA'].fillna(0).gt(0) & C[f'{R}_nB'].fillna(0).gt(0)]
    if X.empty:
        say(f'  {R}: ningún par de validación con formularios en ambos'); continue
    obs = int(X[f'{R}_concuerda'].sum()); n = len(X)
    pb = np.mean([base[R][frozenset((r.invA, r.invB))][0] / base[R][frozenset((r.invA, r.invB))][1] for r in X.itertuples()])
    p = stats.binomtest(obs, n, pb, alternative='greater').pvalue
    say(f'  {R}: concuerdan {obs}/{n} pares de validación frente a {pb:.3f} en pares al azar de los mismos investigadores; binomial p = {p:.3g}')
# R3
R3v = R3.dropna(subset=['bandas', 'cabecera'])
for x in ('bandas', 'cabecera'):
    dv = (C[f'{x}_A'] - C[f'{x}_B']).abs().dropna()
    vals = R3[x].dropna().to_numpy(); dr = np.abs(vals[:, None] - vals[None, :])[np.triu_indices(len(vals), 1)]
    say(f'  R3 {x}: |dif| mediana validación {dv.median():.3f} (n={len(dv)}) frente a pares al azar {np.median(dr):.3f}; Mann-Whitney p = {stats.mannwhitneyu(dv, dr, alternative="less").pvalue:.3g}' if len(dv) else f'  R3 {x}: sin datos')
say('\n== referencia: copias del mismo investigador ==')
S_ = V[~V.cruzado]
say(f'  etiqueta exacta mediana {S_.etiqueta_exacta.median():.3f}; ARI mediana {S_.ARI.median():.3f} (nulo {S_.ARI_nulo.median():.3f}); kappa mediana {S_.kappa_cambio.median():.3f}')
open(A26 + 'salida_validacion.txt', 'w', encoding='utf-8').write('\n'.join(L))
