"""Tarea 1e. ¿Las correspondencias entre quipus respetan el orden de los registros?

Para cada relación del grafo (06) y de 07, se toman los pares (posición del registro en el quipu origen,
posición de la cuerda en el quipu destino) de las coincidencias exactas o ±1 (una por registro de origen: la primera
cuerda del destino) y se calcula la tau de Kendall. Nulo: permutar las posiciones de destino (5000 réplicas).
BH sobre las relaciones con >=4 pares. Además, posición dentro del bloque de UR269 (bloques separados por cuerdas
rosas) de las cabeceras que son suma A+B: ¿ocupan siempre la misma fila del bloque?
"""
import re
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
import comun13 as C

SEED = 13008
rng = np.random.default_rng(SEED)
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])
orden = {(k, cu): o for k, cu, o in zip(c.kfg, c.cuerda, c.orden)}
E = pd.read_csv(C.AQUI / "grafo_cuerdas.csv")
E = E[(E.origen != E.destino) & (E.valor_d.sub(E.valor_o).abs() <= 1) | E.tipo.str.startswith("suma")]
E = E[E.origen != E.destino]


def pos_origen(r):
    m = re.match(r"g(\d+)", str(r.cuerda_o))
    return int(m.group(1)) * 1000 if m else orden[(r.origen, r.cuerda_o)]


filas = []
E = pd.concat([E.assign(variante="exactas y ±1"), E[E.exacto].assign(variante="solo exactas")])
for (o, d, t, var), x in E.groupby(["origen", "destino", "tipo", "variante"]):
    if t == "suma_AB(parte B)" or (var == "solo exactas" and not t.startswith("suma")):
        continue  # la parte B repite la información de la parte A
    x = x.assign(po=[pos_origen(r) for r in x.itertuples()], pd_=[orden[(r.destino, r.cuerda_d)] for r in x.itertuples()])
    x = x.sort_values(["po", "pd_"]).drop_duplicates("po")
    if len(x) < 4:
        filas.append(dict(origen=o, destino=d, tipo=t, variante=var, pares=len(x), tau=np.nan, p=np.nan))
        continue
    tau = kendalltau(x.po, x.pd_).statistic
    nul = np.array([kendalltau(x.po, rng.permutation(x.pd_.to_numpy())).statistic for _ in range(5000)])
    filas.append(dict(origen=o, destino=d, tipo=t, variante=var, pares=len(x), tau=tau,
                      p=(np.sum(nul >= tau) + 1) / 5001))
D = pd.DataFrame(filas)
m = D.p.notna()
D.loc[m, "q"] = C.bh(D.loc[m, "p"])
pd.set_option("display.width", 200)
print(D.to_string(index=False))

# UR270 -> UR278 (de 07)
U = pd.read_csv(C.AQUI / "ur270_ur278.csv")
U = U[U.aciertos >= 5]
tau = kendalltau(U.grupo_UR270, U.fila_UR278).statistic
print(f"\nUR270 -> UR278 (grupos con >=5 columnas): pares {len(U)}, tau = {tau:.2f}",
      list(zip(U.grupo_UR270, U.fila_UR278)))

# posición en el bloque de UR269
u = c[c.kfg == "UR269"]
pos = {}
b, i = 0, 0
for g, x in u.groupby("grupo"):
    if x.color.str.startswith("PK").all() and not x.pres.any():
        b, i = b + 1, 0
        continue
    if x.pres.any():
        i += 1
        pos[g] = (b, i, None)
tam = {}
for g, (bb, ii, _) in pos.items():
    tam[bb] = max(tam.get(bb, 0), ii)
S = E[(E.destino == "UR269") & (E.tipo == "suma_AB(parte A)")]
gr = dict(zip(u.cuerda, u.grupo))
print("\nUR269: posición en el bloque (fila, tamaño del bloque) de las cabeceras = suma A+B")
for fuente in ["UR267A", "UR273A", "UR274A"]:
    s = S[S.origen == fuente]
    pp = sorted({(gr[cu], pos[gr[cu]][1], tam[pos[gr[cu]][0]]) for cu in s.cuerda_d if gr[cu] in pos})
    primera = sum(p == 1 for _, p, _ in pp)
    ultima = sum(p == t for _, p, t in pp)
    pnul_1 = np.prod([1 / t for _, _, t in pp])
    print(f"  {fuente}: {pp}; en 1.a fila {primera}/{len(pp)}, en la última {ultima}/{len(pp)};"
          f" P(todas en la 1.a por azar) = {pnul_1:.2g}; P(todas en la última) = {pnul_1:.2g}")
