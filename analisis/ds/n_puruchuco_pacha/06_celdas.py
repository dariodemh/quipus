"""06: regla (c) 'tabla colgante+s1 -> filas', version D4 con todas las cuerdas.

Para cada grupo de A con >=3 celdas completas (colgante + su primera subsidiaria)
se compara el vector de celdas con el vector de colgantes de cada grupo de B,
posicion a posicion (tolerancia +-1 digito). Estadistico del par:
  suma sobre los grupos de A del maximo de columnas coincidentes
  (solo grupos de B con longitud dentro de +-1).
Nulo: barajar los grupos (vectores completos) de B. BH sobre todos los pares.
Control positivo: UR270 -> UR278 (Incahuasi).
"""
import itertools
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
import comun_np as L

rng = np.random.default_rng(L.SEED + 6)
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def grupos_celdas(c, k):
    out = []
    s = c[c.kfg == k]
    for g, x in s.groupby("grupo", sort=True):
        x0 = x[(x.nivel == 0) & x.pres].sort_values("orden")
        if len(x0) < 3:
            continue
        cel, ok = [], True
        for _, p in x0.iterrows():
            sub = x[(x.nivel == 1) & (x.padre == p.cuerda) & x.pres]
            if len(sub) == 0:
                ok = False
                break
            cel.append(int(p.valor) + int(sub.valor.iloc[0]))
        if ok and len(cel) >= 3:
            out.append((int(g), np.array(cel, dtype=np.int64)))
    return out


def grupos_pend(c, k):
    out = []
    s = c[c.kfg == k]
    for g, x in s.groupby("grupo", sort=True):
        p = [int(v) for v in x[(x.nivel == 0) & x.pres].sort_values("orden").valor]
        if len(p) >= 3:
            out.append((int(g), np.array(p, dtype=np.int64)))
    return out


def matriz(GA, GB):
    M = np.full((len(GA), len(GB)), -1, dtype=np.int16)
    for i, (_, va) in enumerate(GA):
        for j, (_, vb) in enumerate(GB):
            n = min(len(va), len(vb))
            if n < 3 or abs(len(va) - len(vb)) > 1:
                continue
            M[i, j] = int(np.isin(np.abs(va[:n] - vb[:n]), list(L.TOL)).sum())
    return M


def reqs(GA):
    return np.array([max(3, int(np.ceil(0.65 * len(v)))) for _, v in GA])


def analizar(proc, sel):
    c, q = L.cargar_kfg()
    ks = sorted(q[sel].kfg)
    GC = {k: grupos_celdas(c, k) for k in ks}
    GP = {k: grupos_pend(c, k) for k in ks}
    ks = [k for k in ks if GC[k]]
    pr(f"\n== {proc}: {len(ks)} quipus con tabla de celdas: {ks}")
    filas = []
    for a, b in itertools.permutations(ks, 2):
        A, B = GC[a], GP[b]
        if len(A) < 2 or len(B) < 2:
            continue
        M = matriz(A, B)
        rq = reqs(A)
        good = M >= rq[:, None]
        obs = int(good.any(1).sum())
        if obs == 0:
            continue
        # nulo: inyeccion aleatoria de los grupos de A en grupos distintos de B
        nA, nB = good.shape
        nl = []
        for _ in range(2000):
            if nA <= nB:
                jj = rng.choice(nB, size=nA, replace=False)
            else:
                jj = rng.integers(0, nB, size=nA)
            nl.append(int(good[np.arange(nA), jj].sum()))
        nl = np.array(nl)
        best = good.sum(0)
        bj = int(np.argmax(best))
        tau = float(kendalltau(np.arange(len(A)), np.argmax(M, axis=1)).statistic)
        filas.append(dict(A=a, B=b, grupos=len(A), cols=int(M[:, bj].max()),
                          obs=obs, nulo=nl.mean(), p=L.p_emp(obs, nl), tau=tau))
    d = pd.DataFrame(filas)
    if len(d):
        d["q"] = L.bh(d.p)
        d = d.sort_values("p")
        pr(f"   {len(d)} pares; min q={d.q.min():.3f}")
        pr("   top: " + ", ".join(
            f"{t.A}->{t.B}(cols={t.cols},obs={t.obs},nulo={t.nulo:.1f},p={t.p:.4f},q={t.q:.2f})"
            for t in d.head(5).itertuples()))
        d.to_csv(L.AQUI / f"celdas_{proc}.csv", index=False)
    return d


if __name__ == "__main__":
    for proc, sel in [("Incahuasi", None), ("Pachacamac", None), ("Puruchuco", None)]:
        c, q = L.cargar_kfg()
        if proc == "Puruchuco":
            s = q.region == "Puruchuco"
        else:
            s = q.procedencia == proc
        analizar(proc, s)
    with open(L.AQUI / "salida_06_celdas.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(OUT) + "\n")
