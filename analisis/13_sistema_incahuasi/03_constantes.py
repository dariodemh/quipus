"""Tareas 1 y 3. Constante de deducción c por quipu y verificación de las cuotas en todo el archivo.

Registro = grupo con cabecera x (primer colgante anudado, x>=100) y >=1 cuerda anudada más (cualquier nivel).
Apoyo aritmético de d en un registro: alguna otra cuerda del grupo vale x-d (neto), con 1<=d<=x/2.
(No exige que la cuerda d esté anudada: en UR266, UR268, UR273B... la cuota a veces es una cuerda en blanco.)
(a) Descubrimiento: c* = d con más registros de apoyo; estadístico = ese máximo.
(b) Verificación dirigida: para cada cuota candidata C en {10,15,17,20,25,30,40,44,46,47,208} y cada quipu,
    nº de registros con neto x-C, y nº de registros con la cuerda C explícita en las dos posiciones siguientes a x.
Nulo (ambas): barajar entre registros todas las cuerdas no cabecera del quipu (conserva x, los tamaños de
grupo y el multiconjunto de valores: una cuota repetida sigue estando, pero se rompe x-n=c). 2000 réplicas.
BH-FDR: (a) sobre quipus; (b) sobre la matriz quipu x cuota.
Salidas: constantes_descubrimiento.csv, constantes_verificacion.csv
"""
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13003
NPERM = 2000
CUOTAS = [10, 15, 17, 20, 25, 30, 40, 44, 46, 47, 208]

c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])


def registros(s):
    R = []
    for g, x in s[s.pres].groupby("grupo"):
        p0 = x[x.nivel == 0]
        if len(p0) == 0 or len(x) < 2:
            continue
        cab = p0.index[0]
        xv = int(p0.valor.iloc[0])
        if xv < 100:
            continue
        resto = x.drop(cab)
        R.append((xv, resto.valor.to_numpy(int), resto.cuerda.tolist()))
    return R


def apoyo(X, rest, d=None):
    """Cuenta por d (o para un d dado) cuántos registros tienen una cuerda = x-d."""
    if d is not None:
        return sum(int(np.any(r == x - d)) for x, r in zip(X, rest))
    cnt = {}
    for x, r in zip(X, rest):
        for dd in set((x - r[(r < x) & (x - r <= x // 2)]).tolist()):
            cnt[dd] = cnt.get(dd, 0) + 1
    return cnt


def explicito(X, rest, d):
    return sum(int(np.any(r[:2] == d)) for r in rest)


rng = np.random.default_rng(SEED)
desc, ver = [], []
for k in C.ARCHIVO:
    R = registros(c[c.kfg == k])
    if len(R) < 4:
        continue
    X = [x for x, _, _ in R]
    rest = [r for _, r, _ in R]
    sizes = np.cumsum([len(r) for r in rest])[:-1]
    flat = np.concatenate(rest)
    cnt = apoyo(X, rest)
    best = max(cnt.values()) if cnt else 0
    cstar = sorted([d for d, v in cnt.items() if v == best])[:3] if cnt else []
    obs_v = {C_: (apoyo(X, rest, C_), explicito(X, rest, C_)) for C_ in CUOTAS}
    nul_best, nul_v = [], {C_: [] for C_ in CUOTAS}
    for _ in range(NPERM):
        rp = np.split(rng.permutation(flat), sizes)
        cn = apoyo(X, rp)
        nul_best.append(max(cn.values()) if cn else 0)
        for C_ in CUOTAS:
            nul_v[C_].append((apoyo(X, rp, C_), explicito(X, rp, C_)))
    nb = np.array(nul_best)
    desc.append(dict(quipu=k, registros=len(R), c_estrella=cstar, apoyo=best, nulo_media=nb.mean(), nulo_max=nb.max(),
                     p=(np.sum(nb >= best) + 1) / (NPERM + 1)))
    for C_ in CUOTAS:
        N = np.array(nul_v[C_])
        a, e = obs_v[C_]
        ver.append(dict(quipu=k, cuota=C_, registros=len(R), neto_x_menos_c=a, nulo_neto=N[:, 0].mean(),
                        p_neto=(np.sum(N[:, 0] >= a) + 1) / (NPERM + 1), c_tras_cabecera=e, nulo_expl=N[:, 1].mean(),
                        p_expl=(np.sum(N[:, 1] >= e) + 1) / (NPERM + 1)))

D = pd.DataFrame(desc)
D["q"] = C.bh(D.p)
D = D.sort_values("p")
D.to_csv(C.AQUI / "constantes_descubrimiento.csv", index=False, float_format="%.4g")
V = pd.DataFrame(ver)
V["q_neto"] = C.bh(V.p_neto)
V["q_expl"] = C.bh(V.p_expl)
V.to_csv(C.AQUI / "constantes_verificacion.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 250)
print("== (a) descubrimiento de c por quipu (registros con cabecera >=100)")
print(D.to_string(index=False))
print("\n== (b) verificación: registros con neto = x - C (q_neto<0,05 marcado *) / C explícita tras la cabecera")
t = V.assign(cel=V.apply(lambda r: f"{r.neto_x_menos_c}{'*' if r.q_neto < 0.05 else ''}/{r.c_tras_cabecera}{'*' if r.q_expl < 0.05 else ''}", axis=1))
print(t.pivot(index="quipu", columns="cuota", values="cel").join(D.set_index("quipu")[["registros"]]).to_string())
