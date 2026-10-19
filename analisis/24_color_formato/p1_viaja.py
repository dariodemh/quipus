"""P1: ¿el color viaja con el dato? (diseno.md §2)

Construye enlaces fuente -> destino (copias, sumas de Incahuasi, sumas de Puruchuco),
mide coincidencia de color (M), NMI y color de destino, con nulos N1 (emparejamiento)
y N2 (paleta del quipu destino). Salidas: p1_enlaces.csv, p1_resumen.csv, p1_tablas.txt
"""
import re
from collections import Counter

import numpy as np
import pandas as pd

import comun24 as C

rng = np.random.default_rng(C.SEED)
NREP = 9999
c = C.cargar()
c = c.sort_values(["kfg", "orden"])
col_de = {(k, cu): v for k, cu, v in zip(c.kfg, c.cuerda, c.col)}
niv_de = {(k, cu): v for k, cu, v in zip(c.kfg, c.cuerda, c.nivel)}
ENL = []


def add(fam, sub, fq, fcols, dq, dcu, dcol=None, nivel=None):
    if dcol is None:
        dcol = col_de.get((dq, dcu), "")
    if nivel is None:
        nivel = niv_de.get((dq, dcu), 0)
    fcols = [x for x in fcols if x]
    if not dcol or not fcols:
        return
    ENL.append(dict(familia=fam, sub=sub, fuente=fq, fuente_col="|".join(fcols), destino=dq,
                    destino_cuerda=dcu, destino_col=dcol, destino_nivel=nivel))


def modal(xs):
    xs = [x for x in xs if x]
    return Counter(xs).most_common(1)[0][0] if xs else ""


# ---------------------------------------------------------------- F1 copias
fa = pd.read_csv(C.RAIZ / "analisis/14_copias/filas_alineadas.csv", keep_default_na=False)
for r in fa.itertuples():
    ca, cb = C.norm(r.color_A), C.norm(r.color_B)
    same = C.registrador(r.A) == C.registrador(r.B)
    fam = "F1_copia_mismo_reg" if same else "F1_copia_otro_reg"
    if ca and cb:
        ENL.append(dict(familia=fam, sub=f"{r.A}~{r.B}", fuente=r.A, fuente_col=ca, destino=r.B,
                        destino_cuerda=r.cuerda_B, destino_col=cb, destino_nivel=int(float(r.nivel_B or 0))))

# ---------------------------------------------------------------- F2 Incahuasi
g = pd.read_csv(C.RAIZ / "analisis/13_sistema_incahuasi/grafo_cuerdas.csv", keep_default_na=False)
g = g[(g.origen != g.destino) & ~g.tipo.isin(["copia", "cuota", "neto"])]
u270 = c[c.kfg == "UR270"]
u278 = c[(c.kfg == "UR278") & (c.nivel == 0)]


def grupo270(gn, parte):
    x = u270[u270.grupo == gn]
    if parte == "P":
        return modal(x[x.nivel == 0].col)
    return modal(x[x.cuerda.str.endswith("s1") & (x.nivel == 1)].col)


# las sumas A+B: un enlace por destino con las dos fuentes
ab = g[g.tipo.str.startswith("suma_AB")]
for nota, x in ab.groupby("nota"):
    if len(x) != 2:
        continue
    d = x.iloc[0]
    fcols = [col_de.get((r.origen, r.cuerda_o), "") for r in x.itertuples()]
    srcs = "+".join(sorted(x.origen))
    add("F2_incahuasi_suma", "suma_AB", srcs, fcols, d.destino, d.cuerda_d)
for r in g[g.tipo == "total_grupo"].itertuples():
    gn = int(re.match(r"g(\d+)", r.cuerda_o).group(1))
    add("F2_incahuasi_suma", "total_fila_UR278", "UR278", [modal(u278[u278.grupo == gn].col)], r.destino, r.cuerda_d)
for r in g[g.tipo.isin(["suma_PS", "parte_P", "parte_S"])].itertuples():
    gn = int(re.match(r"g(\d+)", r.cuerda_o).group(1))
    if r.tipo == "suma_PS":
        fc = [grupo270(gn, "P"), grupo270(gn, "S")]
    else:
        fc = [grupo270(gn, "P" if r.tipo == "parte_P" else "S")]
    add("F2_incahuasi_suma", r.tipo, "UR270", fc, r.destino, r.cuerda_d)

# UR270 -> celdas de UR278 (colgante + subsidiaria, columna a columna)
t78 = pd.read_csv(C.RAIZ / "analisis/13_sistema_incahuasi/ur270_ur278.csv")
for r in t78[t78.aciertos >= 6].itertuples():
    x = u270[(u270.grupo == r.grupo_UR270)]
    p0 = x[x.nivel == 0]
    y = u278[u278.grupo == r.fila_UR278]
    P = list(map(int, r.P.split()))
    S = list(map(int, r.S1.split()))
    D = [int(v) if v.lstrip("-").isdigit() else -1 for v in r.UR278.split()]
    for j in range(min(len(P), len(D), len(p0), len(y))):
        if P[j] > 0 and D[j] > 0 and abs(P[j] + S[j] - D[j]) <= 1:
            pc = p0.iloc[j]
            sc = x[x.cuerda == pc.cuerda + "s1"]
            add("F2_incahuasi_celda", "UR270->UR278", "UR270",
                [pc.col, sc.col.iloc[0] if len(sc) else ""], "UR278", y.iloc[j].cuerda)

# ---------------------------------------------------------------- F3 Puruchuco
def cuerdas(k):
    return c[c.kfg == k].sort_values("orden").reset_index(drop=True)


def coincide(a, b):
    if a == b:
        return True
    sa, sb = str(a), str(b)
    return len(sa) == len(sb) and sum(x != y for x, y in zip(sa, sb)) == 1


k68, k67, k66 = cuerdas("UR068"), cuerdas("UR067"), cuerdas("UR066")
sec68 = [k68.iloc[13:33], k68.iloc[33:53], k68.iloc[53:73]]
sum68 = [sum(int(s.iloc[j].valor) for s in sec68) for j in range(20)]
d67 = pd.concat([k67.iloc[12:29], k67.iloc[30:33]])
# UR066: mejor desplazamiento contra las sumas
best = max(range(0, len(k66) - 19), key=lambda o: sum(coincide(a, int(b)) for a, b in zip(sum68, k66.iloc[o:o + 20].valor)))
d66 = k66.iloc[best:best + 20]
ok67 = sum(coincide(a, int(b)) for a, b in zip(sum68, d67.valor))
for dest, dd in (("UR067", d67), ("UR066", d66)):
    for j in range(20):
        if coincide(sum68[j], int(dd.iloc[j].valor)) and sum68[j] > 0:
            add("F3_puruchuco", "UR068->" + dest, "UR068", [s.iloc[j].col for s in sec68], dest, dd.iloc[j].cuerda)

# ---------------------------------------------------------------- estadísticos
E = pd.DataFrame(ENL)
E["M"] = [d in f.split("|") for f, d in zip(E.fuente_col, E.destino_col)]
E["M_base"] = [C.base(d) in {C.base(x) for x in f.split("|")} for f, d in zip(E.fuente_col, E.destino_col)]
E.to_csv(C.AQUI / "p1_enlaces.csv", index=False)

# paleta por quipu y nivel para N2
pal = {k: x.col[x.col != ""].values for k, x in c.groupby(["kfg", "nivel"])}


def stats(x):
    m = np.mean([d in f.split("|") for f, d in zip(x.fuente_col, x.destino_col)])
    fs = [f.split("|")[0] for f in x.fuente_col]
    return m, C.nmi(fs, list(x.destino_col))


def nulo_N1(x):
    """permutar color de destino entre enlaces del mismo quipu destino"""
    idx = [np.where(x.destino.values == dq)[0] for dq in x.destino.unique()]
    dcol = x.destino_col.values
    fs = [f.split("|") for f in x.fuente_col]
    f0 = [f[0] for f in fs]
    Ms, Ns = [], []
    for _ in range(NREP):
        d = dcol.copy()
        for ii in idx:
            d[ii] = d[rng.permutation(ii)]
        Ms.append(np.mean([a in b for a, b in zip(d, fs)]))
        Ns.append(C.nmi(f0, d))
    return np.array(Ms), np.array(Ns)


def nulo_N2(x, nrep=2000):
    fs = [f.split("|") for f in x.fuente_col]
    out = []
    pals = [pal.get((dq, nv), np.array([""])) for dq, nv in zip(x.destino, x.destino_nivel)]
    for _ in range(nrep):
        out.append(np.mean([rng.choice(p) in f for p, f in zip(pals, fs)]))
    return np.array(out)


filas = []
T = []
grupos = [("F1_copia_mismo_reg", None), ("F1_copia_otro_reg", None), ("F2_incahuasi_suma", None),
          ("F2_incahuasi_suma", "suma_AB"), ("F2_incahuasi_suma", "total_fila_UR278"),
          ("F2_incahuasi_suma", "suma_PS"), ("F2_incahuasi_celda", None), ("F3_puruchuco", None),
          ("F3_puruchuco", "UR068->UR067"), ("F3_puruchuco", "UR068->UR066")]
for fam, sub in grupos:
    x = E[(E.familia == fam) & ((E["sub"] == sub) if sub else True)].reset_index(drop=True)
    if len(x) < 3:
        continue
    m, n = stats(x)
    M1, N1 = nulo_N1(x)
    M2 = nulo_N2(x)
    dc = Counter(x.destino_col)
    filas.append(dict(familia=fam, sub=sub or "todo", n=len(x), n_destinos=x.destino.nunique(),
                      M=round(m, 3), M_base=round(x.M_base.mean(), 3),
                      M_N1=round(M1.mean(), 3), p_M_N1=C.p_emp(m, M1),
                      NMI=round(n, 3), NMI_N1=round(N1.mean(), 3), p_NMI_N1=C.p_emp(n, N1),
                      M_N2=round(M2.mean(), 3), p_M_N2=C.p_emp(m, M2),
                      W_dest=round(np.mean(x.destino_col == "W"), 3),
                      dest_top=", ".join(f"{k}:{v}" for k, v in dc.most_common(4))))
    T.append(f"\n=== {fam} / {sub or 'todo'} (n={len(x)})\n" +
             pd.crosstab(x.fuente_col, x.destino_col).to_string())

R = pd.DataFrame(filas)
R.to_csv(C.AQUI / "p1_resumen.csv", index=False)
with open(C.AQUI / "p1_tablas.txt", "w", encoding="utf-8") as f:
    f.write(f"Puruchuco: sumas UR068 {sum68}\nUR067 datos {list(d67.valor)} ({ok67}/20 coinciden)\n"
            f"UR066 desplazamiento {best}: {list(d66.valor)}\n")
    f.write("\n".join(T))
pd.set_option("display.width", 250)
print(R.to_string())
