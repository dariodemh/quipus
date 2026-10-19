"""Tarea 3. ¿Las cuotas 10, 15, 17, 30, 47, 208 (y 25, 44, 46 de UR269) se relacionan entre sí?

(a) Coincidencia numérica pura. Con el conjunto K de cuotas constantes por quipu {10, 15, 17, 30, 47, 208} se cuentan
    relaciones a + b = c, a·b = c, 2a = c. Nulo: 6 enteros log-uniformes en [10, 250] (rango de las cuotas), 100 000
    réplicas: P(>= tantas relaciones). Lo mismo añadiendo 25.
(b) Relación estructural (no numerológica): en 04 se demostró que el registro del libro consolidado es la suma de
    los registros de dos componentes. Si la cuota se aplica igual en cada componente, la cuota del consolidado debe
    ser la suma de las de los componentes: 15 + 10 = 25 (UR267A + UR267B -> filas de UR269 con 25) y
    30 + 17 = 47 (UR273A/UR274A + UR273B/UR274B -> UR266/UR275/UR269). Aquí se comprueba registro a registro:
    para cada cabecera del consolidado que es suma A+B (grafo_cuerdas.csv), qué cuota lleva el registro destino.
(c) Curiosidad: 47 + 46 + 46 + 44 + 25 = 208 (cuotas modales de las 5 filas de cada bloque de UR269 frente a la cuota
    de UR268). Probabilidad de que la suma de 5 cuotas tomadas al azar de las cuotas observadas en UR269 dé 208.
"""
import itertools
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13009
rng = np.random.default_rng(SEED)


def relaciones(K):
    K = sorted(K)
    r = []
    for a, b in itertools.combinations_with_replacement(K, 2):
        for cc in K:
            if cc not in (a, b) and a + b == cc:
                r.append(f"{a}+{b}={cc}")
            if cc not in (a, b) and a * b == cc:
                r.append(f"{a}x{b}={cc}")
    return sorted(set(r))


for K in ([10, 15, 17, 30, 47, 208], [10, 15, 17, 25, 30, 47, 208]):
    obs = relaciones(K)
    n = len(K)
    nul = np.array([len(relaciones(np.unique(np.round(np.exp(rng.uniform(np.log(10), np.log(250), n))).astype(int))))
                    for _ in range(100000)])
    print(f"(a) K = {K}: relaciones {obs} ({len(obs)}); nulo medio {nul.mean():.2f}; "
          f"P(>= {len(obs)}) = {(np.sum(nul >= len(obs)) + 1) / 100001:.3f}")

# (b)
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])
E = pd.read_csv(C.AQUI / "grafo_cuerdas.csv")
S = E[(E.tipo == "suma_AB(parte A)") & E.exacto]
P = c[c.pres]
print("\n(b) cuota del registro consolidado cuya cabecera es una suma A+B exacta")
filas = []
for r in S.drop_duplicates(["destino", "cuerda_d"]).itertuples():
    d = P[P.kfg == r.destino]
    g = d[d.cuerda == r.cuerda_d].grupo.iloc[0]
    x = d[d.grupo == g]
    x0 = x[x.cuerda == r.cuerda_d]
    rest = x[x.orden > x0.orden.iloc[0]]
    vals = rest.valor.tolist()
    cuota = [v for v in vals if v < 100]
    netos = [r.valor_d - v for v in vals if 0 < r.valor_d - v < 100]
    filas.append(dict(fuente=r.origen, destino=r.destino, grupo=g, cabecera=r.valor_d, resto=vals,
                      cuota_explicita=cuota, cuota_implicita_x_menos_n=netos))
F = pd.DataFrame(filas)
pd.set_option("display.width", 200)
print(F.to_string(index=False))

# (c)
u = c[(c.kfg == "UR269") & c.pres]
cu = []
for g, x in u.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if len(x0) and x0.valor.iloc[0] >= 100:
        xv = x0.valor.iloc[0]
        cands = [v for v in x.valor.iloc[1:] if 15 <= v <= 50] + [xv - v for v in x.valor.iloc[1:] if 15 <= xv - v <= 50]
        if cands:
            cu.append(cands[0])
cu = np.array(cu)
sims = rng.choice(cu, size=(200000, 5)).sum(1)
print(f"\n(c) cuotas observadas en UR269 (por registro): {sorted(cu.tolist())}")
print(f"    P(suma de 5 cuotas al azar = 208) = {np.mean(sims == 208):.3f}; P(|suma-208| <= 2) = {np.mean(np.abs(sims - 208) <= 2):.3f}")
