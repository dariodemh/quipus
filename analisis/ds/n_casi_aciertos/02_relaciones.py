# -*- coding: utf-8 -*-
"""Inventario de casi-aciertos del sistema Incahuasi, como relaciones verificables.

Cada fila es una relacion: suma de k cuerdas (o una sola cuerda) frente a un
objetivo registrado en otro quipu del sistema. Se guarda el residual
objetivo - observado.
"""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")
c = pd.read_csv(os.path.join(OUT, "subset_cuerdas.csv"), dtype={"valor": float})

def val(q, cuerda):
    x = c[(c.kfg == q) & (c.cuerda == cuerda)]
    return float(x.valor.iloc[0]) if len(x) else np.nan

def cabeceras(q):
    """Cabecera (primer colgante anudado, no separador PK) de cada grupo."""
    s = c[(c.kfg == q) & (c.nivel == 0)].sort_values("orden")
    out = []
    for g, x in s.groupby("grupo", sort=True):
        if len(x) and x.color.astype(str).str.startswith("PK").all() and (x.valor.fillna(0) == 0).all():
            continue
        p = x[x.valor.fillna(0) > 0]
        out.append((g, float(p.valor.iloc[0]) if len(p) else np.nan))
    return out

filas = []

# ---------------- R1: total de fila de UR278 = cabecera del libro ----------------
T = pd.read_csv(os.path.join(ROOT, "analisis", "13_sistema_incahuasi", "ur278_tabla.csv"))
objetivo_R1 = {0: 3618, 1: 1506, 2: 1384, 3: 2919, 4: 3317, 5: 2089, 6: 1842, 7: 1876,
               8: 3249, 9: 2229, 11: 4273, 12: 2633, 13: 3096, 14: 2950, 16: 1278,
               17: 2114, 19: 2106, 21: 1653}
u8 = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
for _, r in T.iterrows():
    g = int(r.grupo)
    if g not in objetivo_R1 or r.n < 9:
        continue
    cuerdas = list(u8[u8.grupo == g].cuerda)
    vals = [val("UR278", x) for x in cuerdas]
    if len(vals) != 9 or any(np.isnan(vals)):
        continue
    filas.append(dict(familia="R1_ur278_fila", quipu="UR278", relacion=f"g{g}",
                      objetivo=objetivo_R1[g], objetivo_cuerda="UR266/UR275 cabecera",
                      cuerdas=";".join("UR278:"+x for x in cuerdas), valores=";".join(str(int(v)) for v in vals),
                      observado=sum(vals), k=9))

# ---------------- R2: celda de UR278 = colgante + subsidiaria 1 de UR270 ----------------
u = c[c.kfg == "UR270"].sort_values("orden")
for g, x in u[u.nivel == 0].groupby("grupo", sort=True):
    p = x[x.valor.fillna(0) > 0]
    if len(p) != 9:
        continue
    cuerdas, vals2 = [], []
    ok = True
    for _, r in p.iterrows():
        s1 = u[(u.padre == r.cuerda) & (u.nivel == 1)]
        if len(s1) == 0:
            ok = False
            break
        cuerdas += [r.cuerda, s1.cuerda.iloc[0]]
        vals2 += [float(r.valor), float(s1.valor.iloc[0])]
    if not ok:
        continue
    # fila de UR278: la que mejor coincide (>=6 columnas a +-1)
    best = None
    for _, rr in T.iterrows():
        if rr.n < 9:
            continue
        cols = [rr["c%d" % (i + 1)] for i in range(9)]
        if any(pd.isna(cols)):
            continue
        sumas = [vals2[2 * i] + vals2[2 * i + 1] for i in range(9)]
        ac = sum(abs(a - b) <= 1 for a, b in zip(sumas, cols))
        if best is None or ac > best[0]:
            best = (ac, int(rr.grupo), sumas, cols)
    ac, gg, sumas, cols = best
    if ac < 6:
        continue
    for i in range(9):
        if abs(sumas[i] - cols[i]) < 1:
            continue
        filas.append(dict(familia="R2_ur278_celda", quipu="UR278", relacion=f"g{gg}c{i+1}~UR270g{g}",
                          objetivo=int(cols[i]), objetivo_cuerda=f"UR278 g{gg} col{i+1}",
                          cuerdas=f"UR270:{cuerdas[2*i]};UR270:{cuerdas[2*i+1]}",
                          valores=f"{int(vals2[2*i])};{int(vals2[2*i+1])}",
                          observado=int(sumas[i]), k=2, nota=f"{ac}/9 columnas a +-1"))

# ---------------- R3/R4: A+B = cabecera del libro ----------------
def registros_cab(q):
    s = c[c.kfg == q]
    out = []
    for g, x in s.groupby("grupo", sort=True):
        x0 = x[x.nivel == 0]
        if len(x0) and x0.color.astype(str).str.startswith("PK").all() and (x0.valor.fillna(0) == 0).all():
            continue
        p = x0[x0.valor.fillna(0) > 0]
        out.append((g, p.cuerda.iloc[0] if len(p) else None, float(p.valor.iloc[0]) if len(p) else np.nan))
    return out

CF = pd.read_csv(os.path.join(ROOT, "analisis", "13_sistema_incahuasi", "componentes_filas.csv"))
def destino_de(fuente, registro):
    x = CF[(CF.fuente == fuente) & (CF.registro == registro)]
    if not len(x) or not isinstance(x.en_resumen.iloc[0], str):
        return None
    cands = []
    for tok in x.en_resumen.iloc[0].split():
        q, g, v = tok.rsplit(":", 2)
        cands.append((abs(float(v.rstrip("~")) - x.suma.iloc[0]), tok.rstrip("~"), tok.endswith("~")))
    exactos = [c for c in cands if not c[2]]
    pool = exactos if exactos else cands
    return min(pool)[1]

for qa, qb in [("UR273A", "UR273B"), ("UR274A", "UR273B")]:
    fam = "R3_ur273ab" if qa == "UR273A" else "R4_ur274a_273b"
    A, B = registros_cab(qa), registros_cab(qb)
    n = min(len(A), len(B))
    for i in range(n):
        if np.isnan(A[i][2]) or np.isnan(B[i][2]):
            continue
        s_ = A[i][2] + B[i][2]
        dest = destino_de(f"{qa}+{qb}", float(i))
        if dest is None:
            filas.append(dict(familia=fam, quipu=qa, relacion=f"reg{i}", objetivo=np.nan,
                              objetivo_cuerda="sin destino en el libro",
                              cuerdas=f"{qa}:{A[i][1]};{qb}:{B[i][1]}",
                              valores=f"{int(A[i][2])};{int(B[i][2])}", observado=int(s_), k=2))
            continue
        q, g, v = dest.rsplit(":", 2)
        filas.append(dict(familia=fam, quipu=qa, relacion=f"reg{i}", objetivo=int(v),
                          objetivo_cuerda=f"{q} g{g}",
                          cuerdas=f"{qa}:{A[i][1]};{qb}:{B[i][1]}",
                          valores=f"{int(A[i][2])};{int(B[i][2])}", observado=int(s_), k=2))

# ---------------- R5: cuota / cuerda unica ----------------
singles = [("UR275", "p51", 47, "cuota 47 (24/25 registros)"),
           ("UR274B", "p9", 17, "cuota 17"),
           ("UR274B", "p13", 17, "cuota 17"),
           ("UR274B", "p19", 17, "cuota 17"),
           ("UR274B", "p64", 17, "cuota 17"),
           ("UR275", "p88", 1827, "UR273A+UR273B / copia"),
           ("UR275", "p100", 1765, "UR273A+UR273B"),
           ("UR275", "p94", 1961, "UR274A+UR273B"),
           ("UR266", "p86", 2020, "UR274A+UR273B")]
for q, cu, obj, why in singles:
    v = val(q, cu)
    if np.isnan(v):
        continue
    filas.append(dict(familia="R5_cuota", quipu=q, relacion=cu, objetivo=obj, objetivo_cuerda=why,
                      cuerdas=f"{q}:{cu}", valores=str(int(v)), observado=int(v), k=1))

R = pd.DataFrame(filas)
R["residual"] = R.objetivo - R.observado
R = R[R.residual.isna() | (R.residual.fillna(0) != 0)]
R.to_csv(os.path.join(OUT, "relaciones_casi.csv"), index=False)
print(R.groupby("familia").agg(n=("relacion", "size"), exacto=("residual", lambda s: (s == 0).sum())).to_string())
print()
for f, g in R.groupby("familia"):
    print(f, "| residuales:", " ".join(f"{int(x):+d}" for x in g.residual.dropna()))
print("\ntotal casi-aciertos:", len(R))
print(R[["familia", "quipu", "relacion", "objetivo", "observado", "residual"]].to_string(max_rows=60))
