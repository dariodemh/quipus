"""D1. Constante por registro (cuota), por quipu y por coleccion.

Dos formas de cuota:
 (a) Diferencia constante: en cada registro, x_i - n_i = c, donde x_i es la cabecera y n_i
     otra cuerda anudada del mismo registro (1 <= c <= x/2).
     Estadistico: maximo numero de registros con apoyo para un mismo c. c* = argmax.
 (b) Posicion relativa constante: un valor que se repite en la misma posicion j de los
     colgantes (j>=1; j=0 es la cabecera) en casi todos los registros.
     Estadistico: maximo sobre j del conteo modal.
Ademas, para el c* de (a), cuantas veces aparece explicito en la primera posicion no-cabecera.

Nulos (1000 replicas, semilla fija):
 (a) barajar las cuerdas no-cabecera entre registros del mismo quipu (conserva tamanos de grupo,
     multiconjunto y magnitudes; rompe x-n=c y la posicion).
 (b) dentro de cada registro, barajar los valores no-cabecera entre las posiciones de colgante
     (conserva el multiconjunto del registro; rompe la asociacion posicion-valor).

Unidad = quipu. Se aplica a todos los quipus de colecciones con >=3 quipus (procedencia y,
aparte, museo). BH dentro de cada familia para cada test.

Salida: d1_cuotas.csv
"""
import numpy as np
import pandas as pd
import comun as C

NPERM = 1000
SEED = C.SEMILLA + 1
rng = np.random.default_rng(SEED)


def cuentas_d(X, rest, off):
    ds, rid = [], []
    for i, (x, r) in enumerate(zip(X, rest)):
        if x <= 1 or len(r) == 0:
            continue
        d = x - r
        d = d[(d > 0) & (d <= x // 2)]
        if len(d):
            ds.append(d); rid.append(np.full(len(d), i, dtype=np.int64))
    if not ds:
        return np.zeros(0, dtype=np.int64)
    d = np.concatenate(ds); i = np.concatenate(rid)
    key = np.unique(i * off + d)
    return np.bincount(key % off)


def apoyo_c(X, rest, c):
    n = 0
    for x, r in zip(X, rest):
        if x > c and np.any(r == x - c):
            n += 1
    return n


def expl_c(rest, c):
    return sum(1 for r in rest if len(r) and r[0] == c)


def modal_pos(P):
    """P: lista de listas de valores de colgantes (incluye cabecera en pos 0)."""
    mx = len(max(P, key=len)) if P else 0
    best = 0; bj = None; bv = None
    for j in range(1, mx):
        vals = [p[j] for p in P if len(p) > j]
        if len(vals) < 2:
            continue
        u, c = np.unique(vals, return_counts=True)
        k = int(c.max())
        if k > best:
            best, bj, bv = k, j, int(u[int(np.argmax(c))])
    return best, bj, bv


def main():
    c, q = C.cargar()
    R = C.todos_los_registros(c, min_rec=3)
    fp, fm = C.familias(q)
    fam_de = {}
    for k in R:
        fam_de[k] = ("proc:" + str(fp[k][1])) if k in fp else (("museo:" + str(fm[k][1])) if k in fm else "sin_familia")
    filas = []
    for k, recs in R.items():
        X = [r["x"] for r in recs]
        rest = [np.array(r["rest"], dtype=np.int64) for r in recs]
        P = [r["pend"] for r in recs]
        maxd = max([x for x in X] + [1])
        off = int(maxd) + 2
        cnt = cuentas_d(X, rest, off)
        if len(cnt) == 0:
            continue
        best = int(cnt.max())
        cs = np.where(cnt == best)[0]
        cstar = int(cs.min())
        obs_expl = expl_c(rest, cstar)
        obs_pos, pj, pv = modal_pos(P)

        # tamaños para permutar cuerdas no-cabecera entre registros
        sizes = np.cumsum([len(r) for r in rest])[:-1]
        flat = np.concatenate(rest) if rest else np.array([], dtype=np.int64)
        n_max = np.zeros(NPERM, dtype=np.int64)
        n_c = np.zeros(NPERM, dtype=np.int64)
        n_ex = np.zeros(NPERM, dtype=np.int64)
        n_pos = np.zeros(NPERM, dtype=np.int64)
        for b in range(NPERM):
            perm = rng.permutation(flat)
            rp = np.split(perm, sizes) if len(flat) else []
            if len(rp) != len(X):
                rp = [np.array([], dtype=np.int64)] * len(X)
            cp = cuentas_d(X, rp, off)
            n_max[b] = cp.max() if len(cp) else 0
            if cstar < len(cp):
                n_c[b] = cp[cstar]
                n_ex[b] = expl_c(rp, cstar)
            # nulo de posicion: barajar dentro de cada registro entre posiciones >=1
            Pp = []
            for p in P:
                if len(p) > 2:
                    Pp.append([p[0]] + list(rng.permutation(p[1:])))
                else:
                    Pp.append(p)
            n_pos[b] = modal_pos(Pp)[0]
        p_max = C.p_emp(best, n_max)
        p_c = C.p_emp(best, n_c)
        p_ex = C.p_emp(obs_expl, n_ex)
        p_pos = C.p_emp(obs_pos, n_pos)
        filas.append(dict(kfg=k, familia=fam_de[k], nrec=len(recs), n_reg_con_cabecera=sum(x > 0 for x in X),
                          c_estrella=cstar, apoyo=best, nulo_max_media=n_max.mean(), p_max=p_max,
                          p_c=p_c, cuota_explicita=obs_expl, nulo_expl_media=n_ex.mean(), p_expl=p_ex,
                          pos_j=pj, pos_valor=pv, pos_conteo=obs_pos, nulo_pos_media=n_pos.mean(), p_pos=p_pos))
    D = pd.DataFrame(filas).sort_values("kfg")
    for col, qcol in [("p_max", "q_max"), ("p_c", "q_c"), ("p_expl", "q_expl"), ("p_pos", "q_pos")]:
        D[qcol] = np.nan
        for fam, idx in D.groupby("familia").groups.items():
            D.loc[idx, qcol] = C.bh(D.loc[idx, col])
    D.to_csv(C.AQUI / "d1_cuotas.csv", index=False, float_format="%.4g")
    print(f"quipus analizados: {len(D)}; familias: {D.familia.nunique()}")
    print(f"q_max<0.05: {(D.q_max < 0.05).sum()}; q_expl<0.05: {(D.q_expl < 0.05).sum()}; q_pos<0.05: {(D.q_pos < 0.05).sum()}")
    pd.set_option("display.width", 220)
    print(D[(D.q_max < 0.05) | (D.q_expl < 0.05) | (D.q_pos < 0.05)]
          [["kfg", "familia", "nrec", "c_estrella", "apoyo", "p_max", "q_max", "cuota_explicita", "p_expl", "q_expl",
            "pos_j", "pos_valor", "pos_conteo", "p_pos", "q_pos"]].to_string(index=False))
    print("\nResumen por familia (quipus con q_max<0.05):")
    t = D[D.q_max < 0.05].groupby("familia").agg(n=("kfg", "size"), cuotas=("c_estrella", lambda s: sorted(set(s)))).sort_values("n", ascending=False)
    print(t.to_string())


if __name__ == "__main__":
    main()
