"""14_copias · Tarea 2b: UR118 y UR119 (Paracas, Göteborg), fila a fila.
Salidas: ur118_ur119_filas.csv y texto por pantalla (redirigir a ur118_ur119_salida.txt). Semilla 20261017.
"""
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

OUT = Path(__file__).resolve().parent
C = pd.read_csv(OUT.parents[1] / "analisis/datos/cuerdas.csv")
rng = np.random.default_rng(20261017)


def filas(k):
    d = C[C.kfg == k]
    cq = d[(d.nivel == 0) & (d.union != "T")]
    out = []
    for g in sorted(cq.grupo.unique()):
        x = cq[cq.grupo == g]
        out.append({"kfg": k, "grupo": int(g), "orden0": int(x.orden.min()), "n": len(x), "nk": int((x.valor > 0).sum()),
                    "cuerdas": f"{x.cuerda.iloc[0]}-{x.cuerda.iloc[-1]}", "vals": [int(v) for v in x.valor],
                    "S": int(x.valor.sum()), "S_all": int(d[d.grupo == g].valor.sum()), "colores": ",".join(sorted(set(x.color.dropna()))),
                    "ceros": int((x.valor == 0).sum()), "rotas": int((x.terminacion == "B").sum())})
    return out


def con_totales(k):
    """empareja cada fila (>=2 cuerdas con nudos) con la suelta adyacente (grupo ±1) y devuelve la lista de filas."""
    g = pd.DataFrame(filas(k))
    uni = g[g.n == 1].set_index("grupo")
    res = []
    for r in g[g.nk >= 2].itertuples():
        cand = [(gg, uni.loc[gg]) for gg in (r.grupo - 1, r.grupo + 1) if gg in uni.index and uni.loc[gg].S > 0]
        # elegir la suelta cuyo valor esté más cerca de S
        tot = min(cand, key=lambda t: abs(t[1].S - r.S)) if cand else None
        res.append({"kfg": k, "fila": r.cuerdas, "n_cuerdas": r.n, "vals": r.vals, "S": r.S, "S_all": r.S_all, "ceros": r.ceros, "rotas": r.rotas,
                    "marcador": r.vals[0], "total": int(tot[1].S) if tot else np.nan,
                    "total_cuerda": tot[1].cuerdas if tot else None,
                    "lado": ("antes" if tot and tot[1].orden0 < r.orden0 else "despues") if tot else None,
                    "colores": r.colores})
    return pd.DataFrame(res)


A, B = con_totales("UR118"), con_totales("UR119")
for D in (A, B):
    D["diff"] = D.total - D.S
    D["diff_all"] = D.total - D.S_all
pd.concat([A, B]).to_csv(OUT / "ur118_ur119_filas.csv", index=False)

pr = print
for k, D in (("UR118", A), ("UR119", B)):
    t = D[D.total.notna()]
    pr(f"\n=== {k}: {len(D)} filas (>=2 cuerdas con nudos); con cuerda-total adyacente: {len(t)}")
    pr(f"  total == suma de la fila: {(t['diff']==0).sum()} ; |dif|<=1: {(t['diff'].abs()<=1).sum()} ; total == suma con subsidiarias: {(t.diff_all==0).sum()}")
    pr(f"  lado del total: {t.lado.value_counts().to_dict()}")
    sin = t[t["diff"] != 0]
    pr("  filas con total != suma (diff = total - suma; ceros = cuerdas sin nudos en la fila; marcador = valor de la 1.ª cuerda):")
    for r in sin.itertuples():
        pr(f"    {r.fila:10s} S={r.S:4d} total={int(r.total):4d} diff={int(r.diff):+5d}  ceros={r.ceros} marcador={r.marcador}  vals={r.vals}")
    # las filas con ceros: ¿total - suma == marcador (la cuerda sin nudos era el marcador perdido) u otro valor de la columna?
    z = t[t.ceros > 0]
    if len(z):
        pr("  filas con cuerda sin nudos:", [(r.fila, int(r["diff"]), r.vals) for _, r in z.iterrows()])

# --- signo de la diferencia y daño
d_ = pd.concat([A.iloc[:-1], B])  # se excluye el último bloque de UR118 (p160-p167, tabla de 8 cuerdas grandes, no es una fila)
d_ = d_[d_.total.notna() & (d_["diff"] != 0) & (d_.ceros == 0)]
pos, neg = int((d_["diff"] > 0).sum()), int((d_["diff"] < 0).sum())
pr(f"\nFilas con total != suma y sin cuerdas vacías: total > suma en {pos}, total < suma en {neg}; p binomial bilateral = {stats.binomtest(pos, pos+neg, .5).pvalue:.3f}")
t_ = pd.concat([A.iloc[:-1], B]); t_ = t_[t_.total.notna()]
eq, ne = t_[t_["diff"] == 0].rotas, t_[t_["diff"] != 0].rotas
pr(f"cuerdas rotas (terminación B) por fila: total==suma media {eq.mean():.2f} (n={len(eq)}), total!=suma media {ne.mean():.2f} (n={len(ne)}); Mann-Whitney p={stats.mannwhitneyu(ne, eq, alternative='greater').pvalue:.3f}")
# --- ¿totales sin nudos? filas sin cuerda-total
pr("\nFilas sin cuerda-total adyacente (con nudos):", {k: int(D.total.isna().sum()) for k, D in (("UR118", A), ("UR119", B))})

# --- marcador (columna 0) por filas: bloques de valor constante
for k, D in (("UR118", A), ("UR119", B)):
    m = D.marcador.tolist()
    bl, cur, n = [], m[0], 0
    for x in m:
        if x == cur:
            n += 1
        else:
            bl.append((cur, n)); cur, n = x, 1
    bl.append((cur, n))
    pr(f"{k} marcador por filas (valor x nº de filas consecutivas): {bl}")

# --- emparejamiento fila a fila UR118 vs UR119
pr("\n=== Emparejamiento fila a fila")
a = A.vals.tolist(); b = B.vals.tolist()


def n_iguales(x, y):
    """columnas 1..5 con el mismo valor no nulo en la misma posición (se omite la columna 0 = marcador)."""
    return sum(1 for p in range(1, min(len(x), len(y), 6)) if x[p] == y[p] and x[p] > 0)


def pares_con_ge2(a, b):
    return sum(n_iguales(x, y) >= 2 for x in a for y in b)


obs = pares_con_ge2(a, b)
nul = []
for _ in range(2000):
    # nulo: barajar los valores de cada columna entre filas (conserva el perfil de cada columna en cada quipu)
    b2 = [list(r) for r in b]
    for p in range(1, 6):
        col = [r[p] for r in b2 if len(r) > p]
        rng.shuffle(col)
        it = iter(col)
        for r in b2:
            if len(r) > p:
                r[p] = next(it)
    nul.append(pares_con_ge2(a, b2))
pr(f"pares de filas (UR118 x UR119) con >=2 columnas idénticas en la misma posición: {obs}; nulo (columnas barajadas) {np.mean(nul):.2f}, p={(1+sum(n>=obs for n in nul))/2001:.3f}")
for i, x in enumerate(a):
    for j, y in enumerate(b):
        if n_iguales(x, y) >= 2:
            pr(f"   UR118 {A.fila[i]} {x}  ~  UR119 {B.fila[j]} {y}")
sa = np.array([sum(r) for r in a[3:]], float); sb = np.array([sum(r) for r in b], float)  # las filas con total empiezan en la 4.ª de UR118


def mejor(x, y):
    out = []
    for rev in (0, 1):
        yy = y[::-1] if rev else y
        for off in range(-4, 5):
            i0, i1 = max(0, -off), min(len(x), len(yy) - off)
            if i1 - i0 >= 8:
                out.append((stats.spearmanr(x[i0:i1], yy[i0 + off:i1 + off])[0], rev, off, i1 - i0))
    return max(out)


ob = mejor(sa, sb)
nu = [mejor(sa, rng.permutation(sb))[0] for _ in range(2000)]
pr(f"alineamiento monótono de totales de fila (desfases -4..4, ambos sentidos): mejor rho={ob[0]:.2f} (sentido inverso={bool(ob[1])}, desfase {ob[2]}, n={ob[3]}); "
   f"nulo (orden de filas barajado, mismo máximo): p={(1+sum(n>=ob[0] for n in nu))/2001:.3f}")
# comparación de formatos
for k, D in (("UR118", A), ("UR119", B)):
    t = D.dropna(subset=["total"])
    pr(f"{k}: mediana de suma de fila {t.S.median():.0f} (rango {t.S.min()}-{t.S.max()}); columna mayor (4.ª-5.ª) mediana "
       f"{np.median([max(v) for v in t.vals]):.0f}; nº de cuerdas por fila: {t.n_cuerdas.value_counts().to_dict()}")
pr("Mann-Whitney sumas de fila UR118 vs UR119:", stats.mannwhitneyu(A.dropna(subset=['total']).S, B.dropna(subset=['total']).S).pvalue)
