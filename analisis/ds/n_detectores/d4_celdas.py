"""D4. Celda = colgante + subsidiaria: la suma columna a columna de un grupo de A reproduce
un grupo de B.

Para cada grupo/registro de A se construye el vector de celdas = valor del colgante + valor de su
primera subsidiaria (s1), columna a columna. Se compara con el vector de colgantes de cada grupo de B
(alineado por posicion, longitudes que difieren como maximo en 1). Una celda coincide si la diferencia
es exacta o +-1 digito.

Estadistico: numero de grupos de A que tienen algun grupo de B con >= max(3, ceil(0.65*L))
columnas coincidentes (L = longitud del vector de celdas de A). Se guarda el mejor grupo de B,
las columnas del mejor match y tau entre el orden de los grupos de A y el grupo de B emparejado.
Se prueban todos los pares ordenados (A,B) con >=3 registros y >=1 grupo con >=3 celdas.

Nulo: barajar los grupos de B (permutacion de sus vectores), 1000 replicas. Preserva los vectores
y sus magnitudes; rompe el emparejamiento grupo a grupo.
BH por detector sobre todos los pares y BH dentro de la familia (procedencia / museo).

Control positivo obligatorio: UR270 -> UR278 (5 grupos con 6-9 de 9 columnas).
Salida: d4_celdas.csv
"""
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
import comun as C

NPERM = 1000
SEED = C.SEMILLA + 4
rng = np.random.default_rng(SEED)


def grupos_celdas(c, k):
    s = c[c.kfg == k]
    out = []
    for g, x in s.groupby("grupo", sort=True):
        if C.es_separador(x):
            continue
        x0 = x[(x.nivel == 0) & x.pres].sort_values("orden")
        if len(x0) < 3:
            continue
        celdas, ok = [], True
        for _, p in x0.iterrows():
            sub = x[(x.nivel == 1) & (x.padre == p.cuerda) & x.pres]
            if len(sub) == 0:
                ok = False
                break
            celdas.append(int(p.valor) + int(sub.valor.iloc[0]))
        if ok and len(celdas) >= 3:
            out.append((int(g), np.array(celdas, dtype=np.int64)))
    return out


def grupos_pend(c, k):
    s = c[c.kfg == k]
    out = []
    for g, x in s.groupby("grupo", sort=True):
        if C.es_separador(x):
            continue
        p = [int(v) for v in x[(x.nivel == 0) & x.pres].sort_values("orden").valor.tolist()]
        if len(p) >= 3:
            out.append((int(g), np.array(p, dtype=np.int64)))
    return out


def matriz_match(GA, GB):
    M = np.full((len(GA), len(GB)), -1, dtype=np.int16)
    for i, (_, va) in enumerate(GA):
        for j, (_, vb) in enumerate(GB):
            L = min(len(va), len(vb))
            if L < 3 or abs(len(va) - len(vb)) > 1:
                continue
            M[i, j] = int(np.isin(np.abs(va[:L] - vb[:L]), C.TOL).sum())
    return M


def reqs_de(GA):
    return np.array([max(3, int(np.ceil(0.65 * len(va)))) for _, va in GA], dtype=np.int16)


def main():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    cel = {k: grupos_celdas(c, k) for k in R if len(R[k]) >= 3}
    pen = {k: grupos_pend(c, k) for k in R if len(R[k]) >= 3}
    cel = {k: v for k, v in cel.items() if v}
    pen = {k: v for k, v in pen.items() if v}
    ks = sorted(cel)
    fp, fm = C.familias(q)

    def familia(a, b):
        if a in fp and b in fp and fp[a] == fp[b]:
            return "proc:" + str(fp[a][1])
        if a in fm and b in fm and fm[a] == fm[b]:
            return "museo:" + str(fm[a][1])
        return "global"

    print(f"quipus con grupos-celda: {len(ks)}")
    pares = [(a, b) for a in ks for b in ks if a != b and not C.excluido(a, b)]
    print(f"pares ordenados: {len(pares)}")
    filas = []
    for n, (a, b) in enumerate(pares):
        M = matriz_match(cel[a], pen[b])
        req = reqs_de(cel[a])
        good = M >= req[:, None]
        obs = int(good.any(1).sum())
        bg, cols, tau = -1, 0, np.nan
        if obs:
            cnt = good.sum(0)
            bj = int(np.argmax(cnt))
            bg, cols = pen[b][bj][0], int(M[:, bj].max())
            jj = np.argmax(M, axis=1)
            ia = np.where(good.any(1))[0]
            if len(ia) >= 4:
                try:
                    tau = float(kendalltau(ia, jj[ia]).statistic)
                except Exception:
                    tau = np.nan
        filas.append(dict(A=a, B=b, nA=len(cel[a]), nB=len(pen[b]), obs=obs, B_grupo=bg,
                          columnas=cols, tau=tau, familia=familia(a, b)))
        if (n + 1) % 20000 == 0:
            print(" ", n + 1)
    D = pd.DataFrame(filas)
    D.to_csv(C.AQUI / "d4_observado.csv", index=False, float_format="%.4g")
    print(D.obs.value_counts().sort_index().to_string())
    print(f"pares obs>=2: {(D.obs >= 2).sum()}; obs>=3: {(D.obs >= 3).sum()}")

    cand = D[D.obs >= 2].copy()
    print(f"candidatos a nulo: {len(cand)}")
    pv = np.ones(len(cand)); nm = np.zeros(len(cand)); nx = np.zeros(len(cand))
    for pos, (ix, r) in enumerate(cand.iterrows()):
        M = matriz_match(cel[r.A], pen[r.B])
        good = M >= reqs_de(cel[r.A])[:, None]
        nA, nB = good.shape
        if nA <= nB:
            perms = np.argsort(rng.random((NPERM, nB)), axis=1)[:, :nA].T
        else:
            perms = rng.integers(0, nB, size=(nA, NPERM))
        vals = good[np.arange(nA)[:, None], perms]
        nul = vals.sum(0)
        nm[pos], nx[pos] = nul.mean(), nul.max()
        pv[pos] = C.p_emp(r.obs, nul)
        if (pos + 1) % 5000 == 0:
            print("  nulo", pos + 1)
    cand["nulo_media"] = nm; cand["nulo_max"] = nx; cand["p"] = pv
    D["p"] = 1.0
    D.loc[cand.index, "p"] = cand.p
    D["q"] = C.bh(D.p)
    D["q_familia"] = np.nan
    for fam, idx in D.groupby("familia").groups.items():
        D.loc[idx, "q_familia"] = C.bh(D.loc[idx, "p"])
    D.to_csv(C.AQUI / "d4_celdas.csv", index=False, float_format="%.4g")
    cand["q"] = D.loc[cand.index, "q"]
    cand["q_familia"] = D.loc[cand.index, "q_familia"]
    cand = cand.sort_values(["p", "obs"], ascending=[True, False])
    cand.to_csv(C.AQUI / "d4_candidatos.csv", index=False, float_format="%.4g")
    print(cand.head(25).to_string(index=False))
    print("\nCONTROL UR270->UR278:")
    print(cand[(cand.A == "UR270") & (cand.B == "UR278")].to_string(index=False))


if __name__ == "__main__":
    main()
