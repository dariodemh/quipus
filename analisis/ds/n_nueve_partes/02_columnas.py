"""UR278 por dentro: identidad y estabilidad de las 9 columnas.

- ?Las 9 columnas tienen proporciones fijas (cuotas) o variables (rendimientos)?
- ?Se agrupan en pares, 4+5 o 3+3+3?
- ?El perfil se conserva entre mitades del registro y entre UR278 y UR270?
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau

RAIZ = Path(r"./analisis")
sys.path.insert(0, str(RAIZ / "ds" / "n_que_se_contaba"))
from comun import cargar  # noqa: E402

rng = np.random.default_rng(20261018)
OUT = RAIZ / "ds" / "n_nueve_partes"


def mat(c, k, K=9):
    q = c[(c.kfg == k) & (c.nivel == 0)].sort_values(["grupo", "orden"])
    gs, rows = [], []
    for g, s in q.groupby("grupo"):
        v = s.v.values
        if len(v) == K and np.isfinite(v).all():
            gs.append(g)
            rows.append(v)
    return np.array(rows, float), gs


def main():
    c = cargar()
    V, gs = mat(c, "UR278")
    V = V[np.isfinite(V).sum(1) == 9]
    P = V / V.sum(1, keepdims=True)
    R, K = P.shape

    print(f"UR278: {R} filas completas x {K} columnas")
    print("\n== 1. Estabilidad de la cuota de cada columna")
    print("   col  media%  sd%   CV%   min%  max%   (CV = sd/media entre filas)")
    for j in range(K):
        m, s = P[:, j].mean(), P[:, j].std(ddof=1)
        print(f"   c{j+1:<2} {100*m:6.2f} {100*s:5.2f} {100*s/m:5.1f} "
              f"{100*P[:,j].min():5.1f} {100*P[:,j].max():5.1f}")
    # CV medio de las cuotas (dentro de columna) frente a ruido multinomial
    cv_intra = np.mean(P.std(0, ddof=1) / P.mean(0))
    # ruido esperado si cada fila fuese multinomial con las cuotas medias
    sim = np.array([rng.multinomial(int(V[i].sum()), P.mean(0)) / V[i].sum()
                    for i in range(R) for _ in range(40)])
    cv_mult = np.mean(sim.std(0, ddof=1) / sim.mean(0))
    print(f"   CV medio intra-columna: observado {cv_intra:.3f}; "
          f"ruido multinomial {cv_mult:.3f}; razon {cv_intra/cv_mult:.2f}")

    print("\n== 2. ?La cuota depende del tamano del registro?")
    tot = V.sum(1)
    for j in range(K):
        r, p = spearmanr(tot, P[:, j])
        print(f"   c{j+1}: rho={r:+.2f} p={p:.3f}", end="")
        if (j + 1) % 3 == 0:
            print()
    print()

    print("\n== 3. Correlacion entre columnas tras quitar el tamano de la fila")
    C = np.corrcoef(P.T)
    print("   matriz (solo |r|>=0.3):")
    for a in range(K):
        for b in range(a + 1, K):
            if abs(C[a, b]) >= 0.3:
                print(f"     c{a+1}-c{b+1}: r={C[a,b]:+.2f}")
    # pares mas correlacionados
    pares = sorted([(C[a, b], a + 1, b + 1) for a in range(K) for b in range(a + 1, K)],
                   reverse=True)
    print("   top 6 pares:", [(f"c{a}-c{b}", round(r, 2)) for r, a, b in pares[:6]])
    print("   peores 4 pares:", [(f"c{a}-c{b}", round(r, 2)) for r, a, b in pares[-4:]])

    print("\n== 4. ?Las columnas se ordenan como 4+5 o 3+3+3?")
    m = P.mean(0)
    orden = np.argsort(-m)
    print("   orden por tamano:", [f"c{j+1}" for j in orden])
    # prueba: suma de cuadrados entre grupos / total, para la particion CONTIGUA
    # en el orden fisico c1..c9 (no en el orden de tamano)
    def r2_fisica(cortes):
        idx = (0,) + tuple(cortes) + (9,)
        sse = sum(((m[a:b] - m[a:b].mean()) ** 2).sum() for a, b in zip(idx[:-1], idx[1:]))
        return 1 - sse / ((m - m.mean()) ** 2).sum()
    for nombre, cortes in [("2+3+4", [2, 5]), ("3+3+3", [3, 6]),
                           ("4+5", [4]), ("5+4", [5])]:
        obs = r2_fisica(cortes)
        # nulo: mismas medias, asignadas al azar a las 9 posiciones
        null = []
        for _ in range(20000):
            mm = rng.permutation(m)
            idx = (0,) + tuple(cortes) + (9,)
            sse = sum(((mm[a:b] - mm[a:b].mean()) ** 2).sum()
                      for a, b in zip(idx[:-1], idx[1:]))
            null.append(1 - sse / ((mm - mm.mean()) ** 2).sum())
        print(f"   particion fisica {nombre}: R2={obs:.3f}; nulo {np.mean(null):.3f} "
              f"[{np.percentile(null,95):.3f} p95]; p={((np.array(null)>=obs).sum()+1)/20001:.3f}")

    print("\n== 5. Concordancia de rango entre filas (Kendall W)")
    ranks = np.apply_along_axis(lambda x: pd.Series(x).rank().values, 1, P)
    Rk = ranks.sum(0)          # suma de rangos por columna
    S = ((Rk - Rk.mean()) ** 2).sum()
    W = 12 * S / (R ** 2 * (K ** 3 - K))
    chi2 = 12 * S / (R * K * (K + 1))
    print(f"   rango medio por columna: " +
          " ".join(f"c{j+1}={Rk[j]/R:.1f}" for j in range(K)))
    print(f"   Kendall W = {W:.3f} (0 = ninguna concordancia; 1 = orden identico); "
          f"chi2 Friedman = {chi2:.1f}")

    print("\n== 5b. Correlacion de log-razones (evita la suma constante)")
    # log(x_i/x_j) es invariante a la escala de la fila; no esta constrenido a sumar 1
    pares_lr = []
    for a in range(K):
        for b in range(a + 1, K):
            lr = np.log((P[:, a] + 1e-9) / (P[:, b] + 1e-9))
            r, p = spearmanr(tot, lr)
            pares_lr.append((abs(r), r, p, a + 1, b + 1))
    pares_lr.sort(reverse=True)
    print("   log-razon vs tamano del registro, |rho| mayores:")
    for _, r, p, a, b in pares_lr[:6]:
        print(f"     log(c{a}/c{b}) vs total: rho={r:+.2f} p={p:.3f}")

    print("\n== 6. UR278 vs UR270: ?mismo perfil de 9 columnas?")
    # emparejamientos ya establecidos en 13_sistema (UR270 g -> fila UR278)
    f = pd.read_csv(RAIZ / "13_sistema_incahuasi" / "ur270_ur278.csv")
    rhos = []
    for _, row in f.iterrows():
        a = np.array([float(x) for x in str(row["P_mas_S1"]).replace("·", "nan").split()])
        b = np.array([float(x) for x in str(row["UR278"]).replace("·", "nan").split()])
        a, b = a[:9], b[:9]
        if len(a) < 9:
            a = np.pad(a, (0, 9 - len(a)), constant_values=np.nan)
        if len(b) < 9:
            b = np.pad(b, (0, 9 - len(b)), constant_values=np.nan)
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() >= 7:
            r, p = spearmanr(a[ok], b[ok])
            rhos.append(r)
            print(f"   UR270 g{int(row['grupo_UR270'])} -> UR278 g{int(row['fila_UR278'])}: "
                  f"{int(row['aciertos'])}/9 celdas +-1, rho de perfil={r:+.2f}")
    print(f"   rho medio de los {len(rhos)} pares: {np.mean(rhos):+.2f}; "
          f"positivos: {sum(1 for x in rhos if x>0)}/{len(rhos)}")

    # guardar
    pd.DataFrame(P, columns=[f"c{j+1}" for j in range(K)]).to_csv(
        OUT / "ur278_proporciones.csv", index=False)


if __name__ == "__main__":
    main()
