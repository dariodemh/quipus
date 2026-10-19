"""Firmas estructurales derivadas de los géneros de transcripción, medidas en el corpus con nulo.

F-A  Asignación redondeada vs recuento (m4 = 9/9 múltiplos de 10; m40 y Santa = 0): por quipu,
     fracción de cuerdas INTACTAS (terminación K) con valor >= 10 que son múltiplo de 10.
     Nulo: binomial p0 = 0,1 (último dígito uniforme de un recuento). + prueba de sobredispersión.
F-B  Total antes / después de la lista (m40: 823 -> 260 -> 11 pueblos que suman 260):
     colgante = suma exacta de los k = 3..12 colgantes siguientes (antes) o anteriores (después).
     Nulo: permutación de valores no vacíos dentro del quipu (posiciones vacías fijas).
F-C  Cantidad x precio = valor (m16, m17: memorias con pesos): terna consecutiva con a*b = c.
F-F  Cuota repetida (m4: 150,150 / 200,200; m5: '100 cada 15 días'): colgantes adyacentes iguales (>= 10).
F-D  Santa: ¿los tamaños de los 6 quipus (grupos de seis) igualan los de las 6 pachacas mejor que el azar?
Unidad = quipu; colgantes de nivel 0 sin cuerdas superiores (unión T) en F-B/C/F. Semilla fija. BH por prueba.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import binomtest, chi2, poisson, false_discovery_control

RAIZ = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SEED = 20261017
B = 2000
ARTEFACTOS = {'UR211', 'AS090_N2', 'AS019', 'AS004'}  # 06_nudos: excluir
rng = np.random.default_rng(SEED)


def bh(p):
    p = np.asarray(p, float)
    q = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    q[ok] = false_discovery_control(p[ok])
    return q


def cargar():
    c = pd.read_csv(RAIZ / "datos" / "cuerdas.csv", low_memory=False).sort_values(["kfg", "orden"])
    c["v"] = np.where(c.nudos.notna(), c.valor, np.nan)
    return c[~c.kfg.isin(ARTEFACTOS)]


# ---------- conteos vectorizados sobre una matriz (filas = permutaciones) ----------
def _win(V, k):
    """sumas de ventanas de k y número de vacíos en ellas; V: (P, n) con NaN."""
    isn = np.isnan(V)
    Z = np.where(isn, 0.0, V)
    P0 = np.zeros((V.shape[0], 1))
    cs = np.concatenate([P0, np.cumsum(Z, 1)], 1)
    cn = np.concatenate([P0, np.cumsum(isn, 1)], 1)
    return cs[:, k:] - cs[:, :-k], cn[:, k:] - cn[:, :-k]


def cuenta_totales(V, kmin=3, kmax=12, hmin=20):
    """(#cabeceras-antes, #totales-después) por fila de V."""
    P, n = V.shape
    antes = np.zeros((P, n), bool)
    despues = np.zeros((P, n), bool)
    ok = ~np.isnan(V) & (V >= hmin)
    for k in range(kmin, kmax + 1):
        if n < k + 1:
            break
        s, nn = _win(V, k)  # s[:, j] = suma de V[j:j+k]
        # antes: V[i] == suma(V[i+1:i+1+k]) -> ventana j=i+1, i = 0..n-k-1
        a = (nn[:, 1:] == 0) & (s[:, 1:] == V[:, :n - k])
        antes[:, :n - k] |= a & ok[:, :n - k]
        # después: V[i] == suma(V[i-k:i]) -> ventana j=i-k, i = k..n-1
        d = (nn[:, :n - k] == 0) & (s[:, :n - k] == V[:, k:])
        despues[:, k:] |= d & ok[:, k:]
    return antes.sum(1), despues.sum(1)


def cuenta_producto(V):
    """ternas consecutivas no vacías (a,b,c) con a*b=c (en cualquier orden), factor menor 2..12, producto >= 20."""
    if V.shape[1] < 3:
        return np.zeros(V.shape[0])
    a, b, c = V[:, :-2], V[:, 1:-1], V[:, 2:]
    hit = np.zeros(a.shape, bool)
    for x, y, z in ((a, b, c), (a, c, b), (b, c, a)):
        lo, hi = np.fmin(x, y), np.fmax(x, y)
        hit |= (x * y == z) & (lo >= 2) & (lo <= 12) & (hi >= 2) & (z >= 20)
    return hit.sum(1)


def cuenta_iguales(V, vmin=10):
    a, b = V[:, :-1], V[:, 1:]
    return ((a == b) & (a >= vmin)).sum(1)


def perm(v, P):
    """P permutaciones de los valores no vacíos, con vacíos fijos."""
    idx = np.flatnonzero(~np.isnan(v))
    M = np.tile(v, (P, 1))
    vals = v[idx]
    for r in range(P):
        M[r, idx] = rng.permutation(vals)
    return M


def firmas_secuencia(c):
    p = c[(c.nivel == 0) & (c.union != "T")]
    rows = []
    for kfg, g in p.groupby("kfg", sort=True):
        v = g.v.to_numpy(float)
        if (~np.isnan(v)).sum() < 6:
            continue
        M = np.vstack([v[None, :], perm(v, B)])
        an, de = cuenta_totales(M)
        pr = cuenta_producto(M)
        ig = cuenta_iguales(M)
        r = dict(kfg=kfg, n=int((~np.isnan(v)).sum()))
        for nom, x in (("antes", an), ("despues", de), ("producto", pr), ("iguales", ig)):
            r[nom] = x[0]
            r[nom + "_esp"] = x[1:].mean()
            r["p_" + nom] = ((x[1:] >= x[0]).sum() + 1) / (B + 1) if x[0] > 0 else 1.0
            # cola de Poisson con la media nula (eventos raros): resuelve p por debajo del piso 1/(B+1)
            r["pp_" + nom] = poisson.sf(x[0] - 1, max(x[1:].mean(), 1 / B)) if x[0] > 0 else 1.0
            r["_null_" + nom] = x[1:]
        rows.append(r)
    return rows


def firma_redondeo(c):
    v = c[c.nudos.notna() & (c.terminacion == "K") & (c.valor >= 10)]
    g = v.groupby("kfg").valor.agg(n="size", r=lambda s: int((s % 10 == 0).sum()))
    g = g[g.n >= 8].copy()
    g["frac"] = g.r / g.n
    g["p"] = [binomtest(int(r), int(n), 0.1, alternative="greater").pvalue for r, n in zip(g.r, g.n)]
    g["q"] = bh(g.p)
    g["p_menor"] = [binomtest(int(r), int(n), 0.1, alternative="less").pvalue for r, n in zip(g.r, g.n)]
    pool = g.r.sum() / g.n.sum()
    x2 = (((g.r - g.n * pool) ** 2) / (g.n * pool * (1 - pool))).sum()
    disp = dict(pool=pool, chi2=x2, gl=len(g) - 1, p=chi2.sf(x2, len(g) - 1))
    # tasa por banda de magnitud (todas las cuerdas intactas)
    banda = pd.cut(v.valor, [9, 99, 999, 1e9], labels=["10-99", "100-999", ">=1000"])
    tb = v.groupby(banda, observed=True).valor.agg(n="size", frac_red=lambda s: (s % 10 == 0).mean())
    return g, disp, tb


def santa_tamanos():
    grupos = np.array([48, 9, 34, 17, 15, 10])  # KFG = publicado (05_etnohistoria 3.1)
    pach = np.array([18, 23, 9, 7, 41, 32])
    obs = np.abs(np.sort(grupos) - np.sort(pach)).sum()
    # nulo 1: composiciones uniformes de 133 en 6 partes >= 1 (tamaños de quipu al azar)
    N = 100000
    cortes = np.sort(np.array([rng.choice(132, 5, replace=False) for _ in range(N)]) + 1, 1)
    parts = np.diff(np.concatenate([np.zeros((N, 1)), cortes, np.full((N, 1), 133)], 1), axis=1)
    d1 = np.abs(np.sort(parts, 1) - np.sort(pach)).sum(1)
    # nulo 2: lo mismo con Dirichlet(2) (tamaños menos dispares)
    w = rng.dirichlet(np.full(6, 2.0), N)
    parts2 = np.maximum(1, np.round(w * 133))
    d2 = np.abs(np.sort(parts2, 1) - np.sort(pach)).sum(1)
    return dict(obs=int(obs), p_unif=((d1 <= obs).sum() + 1) / (N + 1), p_dir2=((d2 <= obs).sum() + 1) / (N + 1),
                med_unif=float(np.median(d1)), med_dir2=float(np.median(d2)),
                pares=list(zip(np.sort(grupos).tolist(), np.sort(pach).tolist())))


if __name__ == "__main__":
    c = cargar()
    q = pd.read_csv(RAIZ / "datos" / "quipus.csv").set_index("kfg")
    tab = set(pd.read_csv(RAIZ / "10_tablas" / "t1_por_quipu.csv").kfg)
    out = []

    # F-A
    g, disp, tb = firma_redondeo(c)
    g["procedencia"] = q.procedencia.reindex(g.index)
    g["tabular"] = g.index.isin(tab)
    g.to_csv(OUT / "fA_redondeo_por_quipu.csv")
    asig = g[(g.q < .05) & (g.frac >= .8)]
    cuenta = g[(g.frac <= .2)]
    out += ["F-A asignación redondeada vs recuento (cuerdas intactas K, valor >= 10, quipus con >= 8):",
            f"  quipus evaluables {len(g)}; tasa conjunta de múltiplos de 10 = {disp['pool']:.3f} (recuento puro: 0,10)",
            f"  sobredispersión entre quipus: chi2 = {disp['chi2']:.0f} con {disp['gl']} gl, p = {disp['p']:.1e}",
            f"  por magnitud: {tb.round(3).to_dict('index')}",
            f"  exceso de redondeo (BH q<0,05 vs p0=0,1): {(g.q < .05).sum()}; de ellos con >= 80 % redondos ('asignación'): {len(asig)}",
            f"  compatibles con recuento (<= 20 % redondos): {len(cuenta)}",
            f"  histograma de la fracción redonda: {np.histogram(g.frac, bins=[0, .1, .2, .4, .6, .8, .95, 1.01])[0].tolist()}"
            " (bins 0-.1-.2-.4-.6-.8-.95-1)",
            "  asignación (frac >= 0,8, q<0,05): " + ", ".join(f"{k}({r.r}/{r.n},{r.procedencia})" for k, r in asig.sort_values('n', ascending=False).iterrows()),
            f"  tabulares de 10_tablas entre los 'asignación': {asig.tabular.sum()}/{len(asig)}; entre los 'recuento': {cuenta.tabular.sum()}/{len(cuenta)};"
            f" base {g.tabular.sum()}/{len(g)}",
            "  por procedencia (mediana frac, n): " + "; ".join(
                f"{k} {v['median']:.2f} ({int(v['count'])})" for k, v in g.groupby('procedencia').frac.agg(['median', 'count']).query('count >= 5').sort_values('median').iterrows()),
            ]
    # cruce con los rasgos de tabla de 10_tablas (¿las tablas son de asignación o de recuento?)
    from scipy.stats import mannwhitneyu
    t1 = pd.read_csv(RAIZ / "10_tablas" / "t1_por_quipu.csv", index_col=0)
    j = g.join(t1, how="inner", rsuffix="_t")
    for col, nom in (("q_constante", "columna casi constante"), ("q_corr", "filas con tamaño (corr. entre columnas)"),
                     ("q_orden", "columna mayor/menor")):
        s_ = j[col] < .05
        out.append(f"  tablas con {nom} (q<0,05): mediana frac redonda {j.frac[s_].median():.2f} (n={s_.sum()}) vs "
                   f"{j.frac[~s_].median():.2f} (n={(~s_).sum()}), Mann-Whitney p = {mannwhitneyu(j.frac[s_], j.frac[~s_]).pvalue:.2f}")
    out.append("")

    # F-B, F-C, F-F
    rows = firmas_secuencia(c)
    res = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]).set_index("kfg")
    for nom in ("antes", "despues", "producto", "iguales"):
        # eventos raros (totales, producto): BH sobre max(p empírico, p Poisson) si el empírico está en el piso;
        # iguales (recuentos grandes, sobredispersos): solo p empírico
        pe = res["p_" + nom].to_numpy()
        pu = np.where(pe <= 1 / (B + 1) + 1e-12, res["pp_" + nom].to_numpy(), pe) if nom != "iguales" else pe
        res["q_" + nom] = bh(pu)
        tot_null = np.sum([r["_null_" + nom] for r in rows], axis=0)
        obs = res[nom].sum()
        p_tot = ((tot_null >= obs).sum() + 1) / (B + 1)
        sig = res[res["q_" + nom] < .05].sort_values(nom, ascending=False)
        out.append(f"F {nom}: corpus obs {obs} vs nulo {tot_null.mean():.1f} (máx {tot_null.max()}), p = {p_tot:.3g}; "
                   f"quipus q<0,05: {len(sig)}: " + ", ".join(f"{k}({int(r[nom])} vs {r[nom + '_esp']:.1f})" for k, r in sig.head(25).iterrows()))
    res["procedencia"] = q.procedencia.reindex(res.index)
    res.to_csv(OUT / "fBCF_por_quipu.csv")
    both = res[(res.q_antes < .05) | (res.q_despues < .05)]
    out.append(f"  dirección en quipus con totales significativos: antes>{'después'} en {(both.antes > both.despues).sum()}, "
               f"después>antes en {(both.despues > both.antes).sum()}, empate {(both.despues == both.antes).sum()}")
    # cruce F-A x F-F: ¿las listas con cuotas repetidas son las redondeadas (tipo m4)?
    rep = g.index.isin(res[res.q_iguales < .05].index)
    out.append(f"  F-A x F-F: fracción redonda en quipus con repeticiones (q<0,05) {g.frac[rep].median():.2f} (n={rep.sum()}) vs "
               f"{g.frac[~rep].median():.2f}; Mann-Whitney p = {mannwhitneyu(g.frac[rep], g.frac[~rep]).pvalue:.1e}; "
               f"en ambas listas: {sorted(set(asig.index) & set(g.index[rep]))}")
    out.append("")

    # F-D
    s = santa_tamanos()
    out.append(f"F-D Santa: L1 entre tamaños ordenados de los 6 quipus y de las 6 pachacas = {s['obs']} (pares {s['pares']});"
               f" nulo composiciones uniformes: mediana {s['med_unif']}, p = {s['p_unif']:.3f}; Dirichlet(2): mediana {s['med_dir2']}, p = {s['p_dir2']:.3f}")
    txt = "\n".join(out)
    (OUT / "r2_resumen.txt").write_text(txt, encoding="utf8")
    print(txt)
