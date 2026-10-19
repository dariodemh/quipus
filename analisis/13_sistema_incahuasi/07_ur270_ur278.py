"""Tarea 1d/2. ¿Las celdas de UR278 son colgante + subsidiaria de UR270, columna a columna?

UR270: grupos de colgantes blancos (parte B) con una primera subsidiaria NB (parte A) cada uno.
Para cada grupo g de UR270 con >=7 colgantes y cada fila h de UR278 con >=7 colgantes, se cuenta en cuántas
columnas j (misma posición en el grupo) se cumple |UR278[h,j] - (P[g,j] + S1[g,j])| <= 1, sobre las columnas con
ambas celdas anudadas. Para cada g se toma la mejor fila h.
Estadístico: nº de grupos de UR270 cuya mejor fila acierta >= 6 columnas, y suma de aciertos de las mejores filas.
Nulo 1 (rompe solo la alineación de columna): permutar las 9 sumas P+S1 dentro de cada grupo de UR270.
Nulo 2 (rompe el emparejamiento colgante-subsidiaria): permutar las subsidiarias entre colgantes del mismo grupo.
5000 réplicas. Se repite con solo P (sin subsidiaria) como control: si las celdas fueran solo colgantes, P bastaría.
Salida: ur270_ur278.csv (mejor fila por grupo y detalle de columnas)
"""
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13007
NPERM = 5000
rng = np.random.default_rng(SEED)
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])

u = c[c.kfg == "UR270"].copy()
u["pend"] = u.cuerda.str.extract(r"^(p\d+)")[0]
G = {}
for g, x in u.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if x0.pres.sum() < 7:
        continue
    filas = []
    for _, p in x0.iterrows():
        s1 = x[x.cuerda == p.cuerda + "s1"]
        sv = int(s1.valor.iloc[0]) if len(s1) and s1.pres.iloc[0] else 0
        filas.append((int(p.valor) if p.pres else -10**6, sv))
    G[g] = np.array(filas)

t = c[(c.kfg == "UR278") & (c.nivel == 0)]
H = {}
for h, x in t.groupby("grupo"):
    if x.pres.sum() >= 7:
        H[h] = np.where(x.pres, x.valor, -10**6).astype(int)


def aciertos(v, w):
    n = min(len(v), len(w))
    ok = (v[:n] > 0) & (w[:n] > 0)
    return int(np.sum(ok & (np.abs(v[:n] - w[:n]) <= 1)))


def mejor(cols):
    out = {}
    for g, v in cols.items():
        sc = [(aciertos(v, w), h) for h, w in H.items()]
        out[g] = max(sc)
    return out


def estad(cols):
    m = mejor(cols)
    return sum(a >= 6 for a, _ in m.values()), sum(a for a, _ in m.values())


PS = {g: np.where(a[:, 0] > 0, a[:, 0] + a[:, 1], -10**6) for g, a in G.items()}
P_ = {g: a[:, 0] for g, a in G.items()}
res = []
for nombre, cols in [("P+S1", PS), ("solo P (control)", P_)]:
    o6, osum = estad(cols)
    n1 = np.array([estad({g: rng.permutation(v) for g, v in cols.items()}) for _ in range(NPERM)])
    linea = dict(variable=nombre, grupos_UR270=len(cols), grupos_con_6mas=o6, aciertos_total=osum,
                 nulo1_6mas=n1[:, 0].mean(), p1_6mas=(np.sum(n1[:, 0] >= o6) + 1) / (NPERM + 1),
                 nulo1_total=n1[:, 1].mean(), p1_total=(np.sum(n1[:, 1] >= osum) + 1) / (NPERM + 1))
    if nombre == "P+S1":
        n2 = []
        for _ in range(NPERM):
            cc = {}
            for g, a in G.items():
                s = rng.permutation(a[:, 1])
                cc[g] = np.where(a[:, 0] > 0, a[:, 0] + s, -10**6)
            n2.append(estad(cc))
        n2 = np.array(n2)
        linea.update(nulo2_6mas=n2[:, 0].mean(), p2_6mas=(np.sum(n2[:, 0] >= o6) + 1) / (NPERM + 1),
                     nulo2_total=n2[:, 1].mean(), p2_total=(np.sum(n2[:, 1] >= osum) + 1) / (NPERM + 1))
    res.append(linea)
R = pd.DataFrame(res)
pd.set_option("display.width", 250)
print(R.to_string(index=False))

det = []
for g, (a, h) in sorted(mejor(PS).items()):
    v, w = PS[g], H[h]
    det.append(dict(grupo_UR270=g, fila_UR278=h, aciertos=a, n_col=min(len(v), len(w)),
                    P=" ".join(map(str, G[g][:, 0])), S1=" ".join(map(str, G[g][:, 1])),
                    P_mas_S1=" ".join(str(x) if x > 0 else "·" for x in v),
                    UR278=" ".join(str(x) if x > 0 else "·" for x in w)))
D = pd.DataFrame(det)
D.to_csv(C.AQUI / "ur270_ur278.csv", index=False)
print(D.drop(columns=["P", "S1"]).to_string(index=False))
