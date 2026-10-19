"""Estructura cuantitativa de UR278, UR266 y UR275 y cribado del corpus.

Unidad de analisis = quipu. Filas = grupos de colgantes (registros);
columnas = posicion dentro del grupo. Valores 0 sin nudos = ausentes.
Semilla fija. Salida por stdout (se guarda en salida_01.txt).
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, spearmanr

RAIZ = Path(r"./analisis")
sys.path.insert(0, str(RAIZ / "ds" / "n_que_se_contaba"))
from comun import cargar, tablas  # noqa: E402

SEED = 20261018
rng = np.random.default_rng(SEED)
OUT = RAIZ / "ds" / "n_nueve_partes"


def matriz_grupos(c, k, K=9):
    """Matriz filas=grupos con EXACTAMENTE K cuerdas de nivel 0."""
    q = c[(c.kfg == k) & (c.nivel == 0)].sort_values(["grupo", "orden"])
    gs, rows = [], []
    for g, s in q.groupby("grupo"):
        v = s.v.values
        if len(v) == K:
            gs.append(g)
            rows.append(v)
    return np.array(rows, float), gs


def cv_col(P):
    """CV entre las medias de columna del perfil (la cifra 0,18 del informe previo)."""
    m = np.nanmean(P, axis=0)
    return np.nanstd(m, ddof=1) / np.nanmean(m)


def cv_rows(V, min_pres):
    out = []
    for row in V:
        x = row[np.isfinite(row)]
        if len(x) >= min_pres and x.mean() > 0:
            out.append(x.std(ddof=1) / x.mean())
    return np.array(out)


def boot_ci(x, B=5000):
    x = np.asarray(x, float)
    bs = np.array([rng.choice(x, len(x), replace=True).mean() for _ in range(B)])
    return x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def describe(k, V):
    pres = np.isfinite(V).sum(1)
    ok = pres >= 7
    Vc = V[pres == 9]
    P = Vc / Vc.sum(1, keepdims=True)
    print(f"\n== {k}: {V.shape[0]} grupos; tamanos {pd.Series(pres).value_counts().sort_index().to_dict()}")
    print(f"   filas completas (9): {len(Vc)}; filas >=7: {ok.sum()}; "
          f"total = {np.nansum(V):.0f}; mediana fila = {np.median(np.nansum(V,1)):.0f}")
    cvs = cv_rows(V, 7)
    m, lo, hi = boot_ci(cvs)
    print(f"   CV dentro de fila (>=7): media {m:.3f} IC95 [{lo:.3f};{hi:.3f}]; "
          f"mediana {np.median(cvs):.3f} (n={len(cvs)})")
    cvc = cv_col(P)
    bs = np.array([cv_col(P[rng.choice(len(P), len(P), True)]) for _ in range(5000)])
    print(f"   CV ENTRE MEDIAS DE COLUMNA: {cvc:.3f} IC95 [{np.percentile(bs,2.5):.3f};"
          f"{np.percentile(bs,97.5):.3f}]  <-- cifra comparable a 0,18")
    prof = np.nanmean(P, 0)
    print("   perfil (% del registro): " +
          " ".join(f"c{j+1}={100*prof[j]:.1f}" for j in range(9)))
    print(f"   max/min de las medias de columna: {prof.max()/prof.min():.2f}")
    # split-half de las medias de columna: ?se conservan las identidades?
    if len(P) >= 10:
        h = len(P) // 2
        a, b = np.nanmean(P[:h], 0), np.nanmean(P[h:], 0)
        r, p = spearmanr(a, b)
        print(f"   split-half (primeras {h} vs ultimas {len(P)-h}): rho={r:.2f}, p={p:.4f}")
    # Friedman
    if len(Vc) >= 5:
        stat, p = friedmanchisquare(*[Vc[:, j] for j in range(9)])
        print(f"   Friedman chi2={stat:.1f}, p={p:.3g} (n={len(Vc)})")
    # nulo 1: permutar celdas dentro de fila -> rompe identidad de columna
    obs = cvc
    null = []
    for _ in range(4000):
        Pp = P.copy()
        for i in range(len(Pp)):
            Pp[i] = rng.permutation(Pp[i])
        null.append(cv_col(Pp))
    null = np.array(null)
    print(f"   nulo columnas intercambiables: CVcol {null.mean():.3f} "
          f"[{np.percentile(null,2.5):.3f};{np.percentile(null,97.5):.3f}], "
          f"p={((null>=obs).sum()+1)/(len(null)+1):.4f}")
    # nulo 2: Dirichlet-multinomial con el perfil observado y los totales de fila
    alpha = prof * 40  # concentracion laxa: CV tipico ~0.15
    sims = []
    for _ in range(2000):
        Ps = np.array([rng.dirichlet(alpha) for _ in range(len(P))])
        sims.append(cv_col(Ps))
    sims = np.array(sims)
    print(f"   nulo Dirichlet(perfil, a0=40): CVcol {sims.mean():.3f} "
          f"[{np.percentile(sims,2.5):.3f};{np.percentile(sims,97.5):.3f}]; "
          f"p(observado mas plano)={((sims<=obs).sum()+1)/(len(sims)+1):.4f}")
    return dict(k=k, grupos=V.shape[0], completos=len(Vc), cv_fila=m,
                cv_col=cvc, maxmin=float(prof.max()/prof.min()),
                total=float(np.nansum(V)))


def particiones(prof):
    """R2 de la mejor particion contigua del perfil ORDENADO por tamano."""
    m = np.sort(prof)[::-1]
    tot = ((m - m.mean()) ** 2).sum()
    print("   perfil ordenado: " + " ".join(f"{100*x:.1f}" for x in m))
    for nombre, cortes in [("2 grupos", [2]), ("3 grupos", [3, 6]),
                           ("4+5", [5]), ("3+3+3", [3, 6]), ("2+3+4", [2, 5])]:
        best = None
        import itertools
        for cc in itertools.combinations(range(1, len(m)), len(cortes)):
            idx = (0,) + cc + (len(m),)
            sse = sum(((m[a:b] - m[a:b].mean()) ** 2).sum()
                      for a, b in zip(idx[:-1], idx[1:]))
            if best is None or sse < best[0]:
                best = (sse, cc)
        print(f"   mejor particion en {nombre}: R2={1-best[0]/tot:.3f} cortes={best[1]}")


def main():
    c = cargar()
    print(f"quipus: {c.kfg.nunique()}; cuerdas nivel 0: {(c.nivel==0).sum()}")

    res = []
    V278, g278 = matriz_grupos(c, "UR278", 9)
    res.append(describe("UR278", V278))
    particiones(np.nanmean(V278[np.isfinite(V278).sum(1) == 9] /
                           np.nansum(V278[np.isfinite(V278).sum(1) == 9], 1, keepdims=True), 0))

    # UR266 y UR275: no son tablas de K fijo; describir grupos y cuotas
    for k in ["UR266", "UR275"]:
        q = c[(c.kfg == k) & (c.nivel == 0)]
        tam = q.groupby("grupo").size()
        print(f"\n== {k}: {len(q)} colgantes, {len(tam)} grupos; "
              f"tamanos {tam.value_counts().sort_index().to_dict()}; "
              f"total {np.nansum(q.v):.0f}")
        # cuota por registro: c = x - suma(resto), busqueda exacta con 3-8 cuerdas
        cu = []
        for g, s in q.groupby("grupo"):
            v = s.sort_values("orden").v.dropna().values
            if 3 <= len(v) <= 8:
                for i in range(len(v)):
                    resto = np.delete(v, i)
                    if abs(v[i] - resto.sum()) < 0.5 and resto.min() > 0:
                        cu.append((g, v[i], resto.min()))
        print(f"   grupos que cierran x=suma(resto): {len(cu)}; "
              f"cuotas mas frecuentes: {pd.Series([x[2] for x in cu]).value_counts().head(5).to_dict()}")

    # cribado del corpus: tablas K=9 y todas las tablas
    T = tablas(c, min_filas=3, min_cols=3)
    filas = []
    for k, d in T.items():
        V = d["V"]
        if V.shape[0] < 3:
            continue
        Vc = V[np.isfinite(V).sum(1) == V.shape[1]]
        if len(Vc) < 3:
            continue
        P = Vc / Vc.sum(1, keepdims=True)
        filas.append(dict(kfg=k, K=V.shape[1], filas=len(Vc),
                          cv_col=float(cv_col(P)),
                          cv_fila=float(cv_rows(Vc, V.shape[1]).mean()),
                          total=float(np.nansum(V))))
    F = pd.DataFrame(filas).sort_values("cv_col")
    F.to_csv(OUT / "cribado_tablas.csv", index=False)
    print(f"\n== Cribado: {len(F)} tablas con >=3 filas completas y >=3 columnas")
    print("   tablas K=9:", int((F.K == 9).sum()))
    print(F[F.K == 9].sort_values("cv_col").head(12).to_string(index=False))
    for k in ["UR278"]:
        row = F[F.kfg == k].iloc[0]
        sub = F[F.K == row.K]
        print(f"   {k}: K={row.K}, CVcol={row.cv_col:.3f}, percentil "
              f"{100*(sub.cv_col < row.cv_col).mean():.0f} de {len(sub)} tablas K={row.K}")
    print("   distribucion de K:", F.K.value_counts().sort_index().to_dict())

    # cuotas exactas en todo el corpus (grupos de 3-4 cuerdas)
    cuotas = []
    base = c[c.nivel == 0]
    for k, q in base.groupby("kfg"):
        for g, s in q.groupby("grupo"):
            v = s.sort_values("orden").v.dropna().values
            if 3 <= len(v) <= 4:
                for i in range(len(v)):
                    resto = np.delete(v, i)
                    if len(resto) >= 2 and abs(v[i] - resto.sum()) < 0.5 and resto.min() > 0:
                        cuotas.append((k, g, v[i], resto.min(), resto.max()))
    C = pd.DataFrame(cuotas, columns=["kfg", "grupo", "x", "c", "n"])
    C.to_csv(OUT / "cuotas_trios.csv", index=False)
    print(f"\n== Cuotas: {len(C)} trios exactos x=c+n en {C.kfg.nunique()} quipus")
    print(C.c.value_counts().head(12).to_string())
    for val in [10, 15, 17, 46, 47, 208]:
        print(f"   c={val}: {C[C.c==val].kfg.value_counts().to_dict()}")
        print(f"      valor {val} como cuerda: {int((c.v==val).sum())} cuerdas en "
              f"{c[c.v==val].kfg.nunique()} quipus")


if __name__ == "__main__":
    main()
