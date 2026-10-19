"""01. Construcción de las matrices de 9 columnas y metadatos.

Salidas (todas dentro de esta carpeta):
  ur278_24.csv   24 filas x 9 columnas de UR278 (grupos con exactamente 9 colgantes, todos anudados)
  ur278_26.csv   control: 26 filas con c1..c9 no vacías (incluye grupos de 10 y 12 cuerdas)
  ur270_9.csv    6 filas x 9 columnas reconstruidas de UR270 (colgante P + primera subsidiaria S1)
  ur270_parts.csv  A = S1, B = P por grupo y columna (para el cociente A/(A+B))
  meta.csv       fase, color, n, total, largo medio por columna
  fondo_9.csv    los 136 grupos de 9 cuerdas del KFG (fondo comparativo)
Imprime un resumen compacto. No lee ningún archivo grande completo.
"""
import numpy as np
import pandas as pd
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
D = RAIZ / "analisis" / "datos"
INC = RAIZ / "analisis" / "13_sistema_incahuasi"

COLS = [f"c{i}" for i in range(1, 10)]


def cargar():
    c = pd.read_csv(D / "cuerdas.csv", low_memory=False, keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    c["pos"] = c.groupby(["kfg", "grupo"]).cumcount()
    return c


def main():
    c = cargar()
    # ---------- UR278 ----------
    T = pd.read_csv(INC / "ur278_tabla.csv")
    u = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
    M = T[COLS].to_numpy(float)
    # 24 filas: grupo con exactamente 9 colgantes de nivel 0 (todas anudadas)
    n9 = T.n.to_numpy() == 9
    assert n9.sum() == 24 and np.isfinite(M[n9]).all()
    T24 = T.loc[n9].copy().reset_index(drop=True)
    T24["fase"] = np.where(T24.grupo < 15, "antes15", "despues15")
    T24.to_csv(AQUI / "ur278_24.csv", index=False)
    # 26 filas: c1..c9 no vacías (incluye grupos 18 y 32, que tienen 10 y 12 cuerdas)
    n26 = np.isfinite(M).all(1)
    T.loc[n26].to_csv(AQUI / "ur278_26.csv", index=False)

    # largo medio por columna y color por posición (para el control "explicación aburrida")
    filas = []
    for g, x in u.groupby("grupo"):
        if len(x) != 9:
            continue
        filas.append([g] + x.largo.to_numpy(float).tolist())
    L = pd.DataFrame(filas, columns=["grupo"] + COLS)
    print(f"UR278: {n9.sum()} filas de 9 cuerdas; {n26.sum()} filas con c1-c9 llenas.")
    print("  largo medio por columna:", np.round(L[COLS].mean(), 1).tolist())
    print("  total por fila: min %d max %d" % (T24.total.min(), T24.total.max()))

    # ---------- UR270 ----------
    w = c[c.kfg == "UR270"].sort_values("orden")
    rows, parts = [], []
    for g, x in w.groupby("grupo"):
        x0 = x[x.nivel == 0]
        if len(x0) != 9:
            continue
        P, S = [], []
        for _, r in x0.iterrows():
            s1 = x[x.cuerda == r.cuerda + "s1"]
            P.append(r.valor if r.pres else np.nan)
            S.append(s1.valor.iloc[0] if len(s1) and s1.pres.iloc[0] else np.nan)
        P, S = np.array(P, float), np.array(S, float)
        if np.isfinite(P).all() and np.isfinite(S).all():
            rows.append([g] + (P + S).tolist())
            parts.append([g] + S.tolist() + P.tolist())
    U = pd.DataFrame(rows, columns=["grupo"] + COLS)
    U.to_csv(AQUI / "ur270_9.csv", index=False)
    A = pd.DataFrame(parts, columns=["grupo"] + ["A" + s for s in COLS] + ["B" + s for s in COLS])
    A["ratio_c1"] = A["Ac1"] / (A["Ac1"] + A["Bc1"])
    for j in range(1, 10):
        A[f"ratio_c{j}"] = A[f"Ac{j}"] / (A[f"Ac{j}"] + A[f"Bc{j}"])
    A.to_csv(AQUI / "ur270_parts.csv", index=False)
    print(f"UR270: {len(U)} grupos de 9 con P y S1 completos.")
    print("  cociente A/(A+B) medio por columna:",
          np.round(A[[f"ratio_c{j}" for j in range(1, 10)]].mean(), 3).tolist())

    # ---------- fondo: grupos de 9 del KFG ----------
    d = c[(c.nivel == 0) & c.pres]
    size = d.groupby(["kfg", "grupo"]).size()
    d9 = d.set_index(["kfg", "grupo"]).loc[size[size == 9].index].reset_index()
    d9["pos"] = d9.groupby(["kfg", "grupo"]).cumcount()
    B = d9.pivot_table(index=["kfg", "grupo"], columns="pos", values="valor")
    B = B.dropna()
    B.columns = COLS
    B = B.reset_index()
    B.to_csv(AQUI / "fondo_9.csv", index=False)
    print(f"Fondo KFG: {len(B)} grupos de 9 cuerdas completos en {B.kfg.nunique()} quipus.")
    print("  pos0 es el máximo del grupo: %.2f ; ratio pos0/media(resto) mediana %.2f"
          % ((B[COLS].idxmax(axis=1) == "c1").mean(),
             (B.c1 / B[["c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"]].mean(axis=1)).median()))
    cv = (B[COLS].std(axis=1) / B[COLS].mean(axis=1))
    print("  CV dentro de grupo: mediana fondo %.3f vs UR278 %.3f (media de filas)"
          % (cv.median(), (T24[COLS].std(axis=1) / T24[COLS].mean(axis=1)).mean()))


if __name__ == "__main__":
    main()
