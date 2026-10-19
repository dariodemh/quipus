"""01 · Grafo de equivalencias 'misma categoria' y consistencia de atributos.

Nodos = cuerdas. Aristas verificadas por aritmetica o por alineamiento de copias:
  - celda_P / celda_S : la celda k de una fila de UR278 es el colgante k de UR270
                        (y su primera subsidiaria). Verificado en 13/07.
  - copia             : UR255 <-> UR267A, alineamiento de 14 (Smith-Waterman).
  - cabecera          : cabeceras del mismo registro en UR266 / UR275 / UR269
                        (LCS exacta sobre la lista ordenada de cabeceras).
  - componente_A / _B : el mismo componente A (o B) de un registro en las dos copias
                        UR273A/UR274A (o UR273B/UR274B), via componentes_filas.csv.

Controles: se permuta el atributo dentro de cada quipu Y nivel (preserva estilo de
libro y composicion por nivel), 5000 replicas, semilla fija. BH sobre 16 pruebas.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, ".")
from comun_rejilla import (RAIZ, SEMILLA, cargar_cuerdas, color_familia,
                           componentes, bh, COLS9)

rng = np.random.default_rng(SEMILLA)
c, q = cargar_cuerdas()

# ---------------------------------------------------------------- indices
idx = {(r.kfg, r.cuerda): r for r in c.itertuples()}
nodos = set(idx)
por_grupo = {k: g.sort_values("orden") for k, g in c.groupby(["kfg", "grupo"])}


def cord(kfg, grupo, nivel=0, k=None, valor=None):
    """Devuelve la cuerda nivel 'nivel' k-esima (0-based) del grupo, o por valor."""
    g = por_grupo.get((kfg, grupo))
    if g is None:
        return None
    g = g[g.nivel == nivel]
    if valor is not None:
        g2 = g[np.isclose(g.valor.astype(float), float(valor), equal_nan=False)]
        return g2.iloc[0].cuerda if len(g2) == 1 else None
    if k is not None and len(g) > k:
        return g.iloc[k].cuerda
    return None


aristas = []

# 1) celdas UR270 <-> UR278 (solo filas con 9 colgantes y >=6/9 aciertos)
pares_celda = [(0, 21), (4, 25), (5, 26), (8, 27), (9, 28)]
filas_celda = []
for g270, g278 in pares_celda:
    for k in range(9):
        p278 = cord("UR278", g278, 0, k)
        p270 = cord("UR270", g270, 0, k)
        if p278 is None or p270 is None:
            continue
        aristas.append((( "UR278", p278), ("UR270", p270), "celda_P"))
        filas_celda.append((g270, g278, k + 1, p270, p278))
        g = por_grupo[("UR270", g270)]
        subs = g[(g.nivel == 1) & (g.padre == p270)].sort_values("orden")
        if len(subs):
            aristas.append((("UR278", p278), ("UR270", subs.iloc[0].cuerda), "celda_S"))

# 2) copia UR255 <-> UR267A (alineamiento de 14)
f = pd.read_csv(f"{RAIZ}/14_copias/filas_alineadas.csv")
f = f[(f.A == "UR255") & (f.B == "UR267A")]
f = f[f.clase.isin(["exacta", "pm1_nudo", "un_digito_otro", "varias_cifras",
                    "misma_cifra_otra_posicion", "transposicion"])]
for r in f.itertuples():
    if ("UR255", r.cuerda_A) in nodos and ("UR267A", r.cuerda_B) in nodos:
        aristas.append((("UR255", r.cuerda_A), ("UR267A", r.cuerda_B), "copia"))

# 3) cabeceras del mismo registro (LCS exacta entre listas ordenadas)
lib = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/libro_consolidado.csv")


def cabeceras(kfg):
    out = []
    for r in lib[lib.quipu == kfg].itertuples():
        g = por_grupo.get((kfg, r.grupo))
        if g is None:
            continue
        g0 = g[(g.nivel == 0) & np.isclose(g.valor.astype(float), float(r.cabecera))]
        if len(g0) == 0:
            continue
        out.append((int(r.grupo), g0.iloc[0].cuerda, float(r.cabecera)))
    return out


def lcs_pares(a, b):
    """Pares (i,j) de la subsecuencia comun mas larga de valores exactos."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return []
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            dp[i + 1][j + 1] = (dp[i][j] + 1 if a[i][2] == b[j][2]
                                else max(dp[i][j + 1], dp[i + 1][j]))
    out, i, j = [], n, m
    while i and j:
        if a[i - 1][2] == b[j - 1][2] and dp[i][j] == dp[i - 1][j - 1] + 1:
            out.append((a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]


cab = {k: cabeceras(k) for k in ["UR266", "UR275", "UR269"]}
n_cab = 0
for ka, kb in [("UR266", "UR275"), ("UR266", "UR269"), ("UR275", "UR269")]:
    for A, B in lcs_pares(cab[ka], cab[kb]):
        aristas.append(((ka, A[1]), (kb, B[1]), "cabecera"))
        n_cab += 1

# 4) componente A / B del mismo registro: dos cuerdas que, con la MISMA pareja,
#    dan el MISMO total son el mismo componente en dos copias (notas de 13).
import re
gr = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/grafo_cuerdas.csv")
pat = re.compile(r"(UR\w+):(p\d+)=(\d+) \+ (UR\w+):(p\d+)=(\d+) = (\d+)")
por_B, por_A = {}, {}
for nota in gr.nota.dropna().unique():
    m = pat.search(str(nota))
    if not m:
        continue
    qa, ca, va, qb, cb, vb, tot = m.groups()
    por_B.setdefault((qb, cb, tot), []).append((qa, ca))
    por_A.setdefault((qa, ca, tot), []).append((qb, cb))
n_comp = 0
for d, tipo in [(por_B, "componente_A"), (por_A, "componente_B")]:
    for _, ns in d.items():
        ns = sorted(set(ns))
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                aristas.append((ns[i], ns[j], tipo))
                n_comp += 1

G = pd.DataFrame([(u[0], u[1], v[0], v[1], t) for u, v, t in aristas],
                 columns=["q_u", "cuerda_u", "q_v", "cuerda_v", "tipo"])
G.to_csv("grafo_aristas.csv", index=False)
print("aristas por tipo:\n", G.tipo.value_counts().to_string())
print("quipus en el grafo:", sorted(set(G.q_u) | set(G.q_v)))

# ---------------------------------------------------------------- componentes
nodos_txt = [(r.kfg, r.cuerda) for r in c.itertuples() if r.kfg in set(G.q_u) | set(G.q_v)]
comp = componentes(nodos_txt, list(zip(zip(G.q_u, G.cuerda_u), zip(G.q_v, G.cuerda_v))))
tam = pd.Series([len(v) for v in comp.values()])
print("\ncomponentes:", len(comp), "| tam >=2:", (tam >= 2).sum(),
      "| mayor:", tam.max(), "| media tam>=2:", round(tam[tam >= 2].mean(), 2))
mapa = {n: i for i, (_, ns) in enumerate(comp.items()) for n in ns}
G["comp"] = [mapa.get((a, b)) for a, b in zip(G.q_u, G.cuerda_u)]
resumen = (G.groupby("comp").agg(n_aristas=("tipo", "size"),
                                tipo=("tipo", lambda s: s.mode().iat[0]),
                                quipus=("q_u", lambda s: ",".join(sorted(set(s)))))
             .sort_values("n_aristas", ascending=False))
resumen.to_csv("grafo_componentes.csv", encoding="utf-8-sig")
print("\ncomponentes con >=2 aristas:")
print(resumen[resumen.n_aristas >= 2].head(12).to_string())

# ---------------------------------------------------------------- atributos
c["color_fam"] = c.color.map(color_familia)
c["color_base"] = c.color.map(lambda x: x.split(":")[0].split("/")[0][:2])
idx = {(r.kfg, r.cuerda): r for r in c.itertuples()}


def consistencia(tipo, campo, B=5000):
    E = G[G.tipo == tipo]
    if len(E) == 0:
        return None
    pares = [((a, b), (d, e)) for a, b, d, e in
             zip(E.q_u, E.cuerda_u, E.q_v, E.cuerda_v)
             if (a, b) in idx and (d, e) in idx]
    if not pares:
        return None
    vu = np.array([getattr(idx[u], campo) for u, _ in pares], dtype=object)
    # estratos (quipu, nivel) con todos los nodos del quipu, no solo los del grafo
    estratos, pos_de = {}, {}
    for (k, cord), r in idx.items():
        clave = (k, int(r.nivel))
        pos_de[(k, cord)] = (clave, len(estratos.get(clave, [])))
        estratos.setdefault(clave, []).append((k, cord))
    V = {clave: np.array([getattr(idx[x], campo) for x in ns], dtype=object)
         for clave, ns in estratos.items()}
    pv = [pos_de[v] for _, v in pares]
    obs = int(sum(vu[i] == V[pv[i][0]][pv[i][1]] for i in range(len(pares))))
    null = np.empty(B, dtype=int)
    for b in range(B):
        for clave in V:
            rng.shuffle(V[clave])
        null[b] = sum(vu[i] == V[pv[i][0]][pv[i][1]] for i in range(len(pares)))
    p = (1 + int(np.sum(null >= obs))) / (B + 1)
    return dict(tipo=tipo, atributo=campo, n=len(pares), aciertos=obs,
                esperado=float(null.mean()), razon=obs / max(null.mean(), 1e-9), p=p)


pruebas = [consistencia(t, a) for t in sorted(G.tipo.unique())
           for a in ["color", "color_fam", "union", "torsion"]]
T = pd.DataFrame([p for p in pruebas if p])
T["q_BH"] = bh(T.p)
T = T.sort_values("p")
T.to_csv("consistencia_atributos.csv", index=False, encoding="utf-8-sig")
print("\nConsistencia de atributos (permutacion dentro de quipu y nivel):")
print(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# nivel: no es un atributo del mismo tipo (UR270 parte la celda en 0+1)
print("\nNivel de los pares de celda:")
for t in ["celda_P", "celda_S"]:
    E = G[G.tipo == t]
    nu = [idx[(a, b)].nivel for a, b in zip(E.q_u, E.cuerda_u) if (a, b) in idx]
    nv = [idx[(a, b)].nivel for a, b in zip(E.q_v, E.cuerda_v) if (a, b) in idx]
    print(t, "nivel UR278:", pd.Series(nu).value_counts().to_dict(),
          "| nivel UR270:", pd.Series(nv).value_counts().to_dict())
