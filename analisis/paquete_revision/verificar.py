# Recálculo independiente de cifras clave del paquete de revisión (no usa scripts de 13/16/19).
# Uso, desde la raíz del repo:  python analisis/paquete_revision/verificar.py
import re
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

c = pd.read_csv("analisis/datos/cuerdas.csv", low_memory=False)
q = lambda k: c[c.kfg == k]
ok = []


def check(nombre, cond, detalle):
    ok.append(cond)
    print(f"[{'OK' if cond else 'FALLA'}] {nombre}: {detalle}")


# 1. Unión R/V de las parejas atadas (SINTESIS, ronda 13)
u = {k: q(k)[q(k).nivel == 0].union.value_counts().to_dict() for k in ["UR273A", "UR273B", "UR267A", "UR267B"]}
check("unión R/V opuesta en UR273A/B y UR267A/B",
      u["UR273A"].get("V") == 83 and u["UR273A"].get("R", 0) == 0 and u["UR273B"].get("R") == 113
      and u["UR273B"].get("V") == 1 and u["UR267A"].get("V") == 82 and u["UR267B"].get("R") == 103, u)

# 2. H1: UR273A + UR273B por número de grupo -> cabeceras de UR266/UR275/UR269: 8/18 exactas
cab = lambda k: q(k)[(q(k).nivel == 0) & (q(k).valor > 0)].groupby("grupo").valor.max()
A, B = cab("UR273A"), cab("UR273B")
comunes = sorted(set(A.index) & set(B.index))
pool = set(pd.concat([q(k)[q(k).nivel == 0].valor for k in ["UR266", "UR275", "UR269"]]).astype(int))
sumas = [int(A[g] + B[g]) for g in comunes]
ex = [s for s in sumas if s in pool]
check("H1 A+B exactas", len(comunes) == 18 and len(ex) == 8, f"{len(ex)}/{len(comunes)} -> {ex}")

# 3. H2: UR270 g0 (P+S1) = UR278 g21 celda a celda
u270 = q("UR270")
g0 = u270[u270.grupo == 0]
ps = [int(r.valor + g0[g0.padre == r.cuerda].valor.iloc[0]) for r in g0[g0.nivel == 0].itertuples()]
f21 = q("UR278")[(q("UR278").grupo == 21) & (q("UR278").nivel == 0)].valor.astype(int).tolist()
dif = [a - b for a, b in zip(f21, ps)]
check("H2 UR270 g0 -> UR278 g21", sum(d == 0 for d in dif) == 8 and dif[0] == 1,
      f"P+S1={ps}; UR278={f21}; difs={dif}")

# 4. H3: totales de fila de UR278 que aparecen, en orden, como colgantes de UR266
u278 = q("UR278")[q("UR278").nivel == 0]
filas = u278.groupby("grupo").valor.agg(["sum", "size"])
tot = filas[filas["size"] == 9]["sum"].astype(int).tolist()
dest = q("UR266")[q("UR266").nivel == 0].sort_values("orden").valor.astype(int).tolist()


def lcs(a, b):
    D = np.zeros((len(a) + 1, len(b) + 1), int)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            D[i + 1, j + 1] = D[i, j] + 1 if x == y else max(D[i, j + 1], D[i + 1, j])
    return D[-1, -1]


n_ord = lcs(tot, dest)
check("H3 filas UR278 -> UR266 en orden", n_ord == 11, f"{n_ord} totales exactos en orden; g0 = {tot[0]}")

# 5. Cuotas de UR274B: 17 frente a 10. n_casi_aciertos dice «las 4 de 10 son exactamente las 4 más cortas»;
#    en KFG una de ellas (25,0 cm) es más larga que la 17 más corta (24,5 cm): están entre las 5 más cortas.
b = q("UR274B")
v17, v10 = b[b.valor == 17], b[b.valor == 10]
rango = pd.concat([v17.largo, v10.largo]).rank(method="first")
max_rango_10 = int(rango.loc[v10.index].max())
check("UR274B cuotas 10 entre las 5 más cortas (no las 4)", len(v17) == 12 and len(v10) == 4 and max_rango_10 == 5,
      f"17: {len(v17)} (largo mín {v17.largo.min()}); 10: {len(v10)} (largos {sorted(v10.largo)}); "
      f"P(4 de 10 entre las 5 más cortas)=5/1820={5/1820:.4f}")

# 6. UR275 p51 = 40 frente a 24 cuotas de 47
r = q("UR275")
check("UR275 p51", int(r[r.cuerda == "p51"].valor.iloc[0]) == 40 and (r.valor == 47).sum() == 24,
      f"p51={int(r[r.cuerda == 'p51'].valor.iloc[0])}; cuerdas = 47: {(r.valor == 47).sum()}")

# 7. Planitud de las 9 columnas de UR278 (CV de las medias de columna)
M = np.array([g.valor.to_numpy() for _, g in u278.groupby("grupo") if len(g) == 9 and (g.valor > 0).all()])
med = M.mean(0)
cv = med.std(ddof=1) / med.mean()
check("UR278 CV entre medias de columna (informes: 0,17-0,19)", 0.17 <= cv <= 0.20, f"{len(M)} filas completas; CV={cv:.3f}; max/min={med.max()/med.min():.2f}")

# 8. Bambamarca (Pärssinen 1992, tabla 2): rho con la posición
bam = [104, 75, 78, 68, 49, 75, 67, 30, 27]
rho, p = spearmanr(range(9), bam)
check("Bambamarca rho", abs(rho + 0.87) < 0.01, f"rho={rho:.3f}, p={p:.4f}; CV={np.std(bam, ddof=1)/np.mean(bam):.3f}")


# 9. UR053A-E: reparto W / R / AB en tríos (misma extracción que 21_ur053/alinear.py)
def norm(s):
    s = re.sub(r"\([^)]*\)", "", str(s))
    return "R" if s.startswith("R") else s


def trios(k):
    g = q(k).copy()
    g["col"] = g.color.map(norm)
    sub = {x.padre: x.valor for x in g[g.nivel == 1].itertuples() if x.col == "AB"}
    L = list(zip(*[g[g.nivel == 0][k2] for k2 in ("cuerda", "col", "valor")]))
    out = []
    for i in range(len(L) - 1):
        if L[i][1] == "W" and L[i + 1][1] == "R":
            ab = sub.get(L[i + 1][0])
            if ab is None and i + 2 < len(L) and L[i + 2][1] == "AB":
                ab = L[i + 2][2]
            if ab is not None:
                out.append((L[i][2], L[i + 1][2], ab))
    return np.array(out, float)


rep = {}
for k in ["UR053A", "UR053B", "UR053C", "UR053D", "UR053E"]:
    t = trios(k)
    rep[k] = np.round(t.sum(0) / t.sum(), 2).tolist()
check("UR053 parte W entre 0,55 y 0,72 en los 5", all(0.55 <= v[0] <= 0.72 for v in rep.values()), rep)

# 10. KH0049: tabla jerarquica en bloques de 18 colgantes (mismo recuento que 30_frontera_estructura/07_ur122_kh0049.py)
vals = lambda k: q(k)[q(k).nivel == 0].sort_values("orden").valor.to_numpy(np.int64)
v49 = vals("KH0049"); B = [v49[i * 18:(i + 1) * 18] for i in range(6)]
ex = lambda a, b: int(((a == b) & (a > 0)).sum())
e01, e1 = ex(B[0], B[1] + B[2]), ex(B[1], B[3] + B[4] + B[5])
check("KH0049 B0=B1+B2 14/18 y B1=B3+B4+B5 7/18", len(v49) >= 108 and e01 == 14 and e1 == 7, f"{e01}/18 y {e1}/18")
u122 = vals("UR122")
check("15652/15649 en KH0049 y UR122",
      B[1][0] == 15652 and u122[0] == 15652 and B[3][0] + B[4][0] + B[5][0] == 15649 and B[0][0] - B[2][0] == 15649,
      f"KH0049 B1[1]={B[1][0]}, UR122 B0[1]={u122[0]}, B3+B4+B5={B[3][0]+B[4][0]+B[5][0]}, B0-B2={B[0][0]-B[2][0]}")
U1, K3 = u122[18:36], B[3]  # el bloque 2 de UR122 (p19-p36) corresponde al B3 de KH0049
cero = [i for i in range(18) if U1[i] == 0 and K3[i] > 0]
check("UR122 p21-p23 en 0 donde KH0049 B3 tiene 487, 281, 661", cero[:3] == [2, 3, 4] and [int(K3[i]) for i in cero[:3]] == [487, 281, 661],
      f"{len(cero)} posiciones en 0 en UR122 con valor en KH0049: {[(18 + i + 1, int(K3[i])) for i in cero]}")

# 11. UR1104 -> cabeceras de UR234 (copia «extracto de un campo»)
a = vals("UR1104")[7:16].tolist()  # 9 cabeceras tras los 7 totales
cab = q("UR234")[q("UR234").nivel == 0].sort_values("orden").groupby("grupo", sort=True).valor.apply(lambda s: int(s.iloc[0]))
b = cab.loc[0:8].tolist()
iguales = [x for x, y in zip(a, b) if x == y]
check("UR1104 frente a cabeceras g0-g8 de UR234: 7 exactas, 1 variante (3102/3012), 1 rota (2016 frente a 0)",
      len(iguales) == 7 and a[2] == 3102 and b[2] == 3012 and a[5] == 2016 and b[5] == 0, f"UR1104={a}; UR234={b}")

# 12. Desajustes UR278 -> libro (usa 29_lectura_incahuasi/tabla_traducida.csv): 18 con destino, 11 exactas, 7 desajustes
import csv
from math import comb
filas = [r for r in csv.DictReader(open("analisis/29_lectura_incahuasi/tabla_traducida.csv", encoding="utf-8"))
         if r["quipu"] == "UR278" and r["cuerda"] == "Σ fila" and "sin destino" not in r["enlace"]]
dif = {r["grupo"]: int(re.search(r"UR266 g\d+=(\d+)", r["enlace"]).group(1)) - int(r["valor"]) for r in filas}
des = {g: d for g, d in dif.items() if d}
uni = sum(abs(d) < 10 for d in des.values()); n = len(des)
p_uni = sum(comb(n, k) * (1 / 3) ** k * (2 / 3) ** (n - k) for k in range(uni, n + 1))
check("Desajustes UR278 -> libro: 18 con destino, 7 desajustes, 6/7 en unidades (p nulo 1/3 ~ 0,007)",
      len(dif) == 18 and n == 7 and uni == 6 and abs(p_uni - 0.007) < 0.001, f"libro - detalle = {des}; p={p_uni:.4f}")
check("UR278 g29: desajuste de -1 (1507 frente a 1506)", des.get("29") == -1, f"g29 = {des.get('29')}")

print(f"\n{sum(ok)}/{len(ok)} comprobaciones correctas")
