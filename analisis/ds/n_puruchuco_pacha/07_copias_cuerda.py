"""07: prueba de copias a nivel de CUERDA (no de grupo).

T1 de 02 compara sumas de grupo y por eso no ve copias cuyo troquelado de
grupos cambia (p. ej. AS125=UR247, el mismo objeto en dos museos). Aqui se
alinean las cuerdas por orden y se cuenta cuantas coinciden (exacto y +-1
digito). Nulo: barajar las cuerdas de B. BH sobre todos los pares.
"""
import itertools
import numpy as np
import pandas as pd
import comun_np as L

rng = np.random.default_rng(L.SEED + 7)
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def analizar(nombre, sel):
    c, q = L.cargar_kfg()
    ks = sorted(q[sel].kfg)
    V = {k: np.array([int(v) for v in c[c.kfg == k].sort_values("orden").valor])
         for k in ks}
    filas = []
    for a, b in itertools.combinations(ks, 2):
        va, vb = V[a], V[b]
        n = min(len(va), len(vb))
        if n < 5:
            continue
        x, y = va[:n], vb[:n]
        M = x[:, None] == y[None, :]
        Mt = np.isin(np.abs(x[:, None] - y[None, :]), list(L.TOL))
        h, ht = int(np.trace(M)), int(np.trace(Mt))
        nl = np.array([Mt[np.arange(n), rng.permutation(n)].sum() for _ in range(1000)])
        filas.append(dict(A=a, B=b, n=n, exactas=h, toler=ht,
                          nulo=nl.mean(), p=L.p_emp(ht, nl)))
    d = pd.DataFrame(filas)
    if len(d):
        d["q"] = L.bh(d.p)
        d = d.sort_values("p")
        pr(f"\n== {nombre}: {len(d)} pares con >=5 cuerdas; min q={d.q.min():.3f}")
        pr("   top: " + ", ".join(
            f"{t.A}={t.B}(ex={t.exactas},tol={t.toler}/{t.n},nulo={t.nulo:.1f},p={t.p:.4f},q={t.q:.2f})"
            for t in d.head(6).itertuples()))
        d.to_csv(L.AQUI / f"copias_cuerda_{nombre}.csv", index=False)
    return d


if __name__ == "__main__":
    c, q = L.cargar_kfg()
    for nombre, sel in [("Incahuasi", q.procedencia == "Incahuasi"),
                        ("Pachacamac", q.procedencia == "Pachacamac"),
                        ("Puruchuco", q.region == "Puruchuco"),
                        ("Ica", q.procedencia == "Ica")]:
        analizar(nombre, sel)
    with open(L.AQUI / "salida_07_copias_cuerda.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(OUT) + "\n")
