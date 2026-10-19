"""T7. Calidad del dato de color y trampa de identificadores KFG <-> OKR.

Motivacion: Milillo et al. (2023) advierten que el color registrado a ojo
no es un dato duro y que eso limita su uso estadistico. Aqui se comprueba
si el KFG y el OKR permiten un control independiente del color.

Hallazgo metodologico: CORD_ORDINAL del OKR es el ordinal *dentro del
padre* (las subsidiarias vuelven a 1), no un ordinal global. Un join
naive por (khipu, ordinal) produce solo ~38% de concordancia, un artefacto.
Se compara entonces a nivel de quipu (proporcion de cada color), que no
depende de la alineacion cordel a cordel.
"""
import os
import sqlite3
import numpy as np
import pandas as pd
from comun import cargar, RAIZ

c, q, _ = cargar()
db = os.path.join(RAIZ, "data", "external", "open-khipu-repository",
                  "data", "khipu.db")
con = sqlite3.connect(db)
k = pd.read_sql("SELECT KHIPU_ID, OKR_NUM, orig_inv_num FROM khipu_main", con)
cor = pd.read_sql("SELECT KHIPU_ID, CORD_ID, CORD_ORDINAL, PENDANT_FROM FROM cord", con)
col = pd.read_sql("SELECT CORD_ID, COLOR_CD_1 FROM ascher_cord_color", con)
col = col.drop_duplicates("CORD_ID")
okr = cor.merge(col, on="CORD_ID", how="left").merge(k, on="KHIPU_ID", how="left")

print("=== Trampa de CORD_ORDINAL ===")
dup = cor.duplicated(["KHIPU_ID", "CORD_ORDINAL"]).sum()
print("filas de cord con (KHIPU_ID, CORD_ORDINAL) duplicado:",
      dup, "de", len(cor), f"({dup/len(cor):.1%})")
print("Ejemplo UR090 (KH0326): primeros ordinales =",
      cor[cor.KHIPU_ID == 1000274].CORD_ORDINAL.head(12).tolist())

mapa = {}
for _, r in k.iterrows():
    for clave in [str(r.OKR_NUM), str(r.orig_inv_num)]:
        if clave and clave != "nan":
            mapa.setdefault(clave, int(r.KHIPU_ID))
q["kid"] = q.kfg.map(mapa)
print("\nquipus KFG con equivalente OKR:", q.kid.notna().sum(), "de", len(q))


def base(x):
    if not isinstance(x, str):
        return None
    return x.split("(")[0].split("%")[0].split(":")[0].split("-")[0].split("/")[0].strip()


c["cb"] = c.color.map(base)
qq = q[q.kid.notna()]

filas = []
for _, r in qq.iterrows():
    gk = c[c.kfg == r.kfg]
    go = okr[okr.KHIPU_ID == r.kid]
    if len(gk) < 10 or len(go) < 10:
        continue
    filas.append((r.kfg, len(gk), len(go),
                  gk.cb.value_counts(normalize=True).to_dict(),
                  go.COLOR_CD_1.value_counts(normalize=True).to_dict()))
print("khipus comparables (>=10 cuerdas en ambas bases):", len(filas))

colores = ["W", "AB", "MB", "KB", "YB", "B", "LB", "GG"]
print("\n=== Concordancia a nivel de quipu (proporcion de cada color) ===")
print("color   n   r Pearson   dif. media abs")
for colr in colores:
    x = np.array([f[3].get(colr, 0) for f in filas])
    y = np.array([f[4].get(colr, 0) for f in filas])
    if x.std() > 0 and y.std() > 0:
        r = np.corrcoef(x, y)[0, 1]
        print(f"{colr:6s} {len(x):3d}   {r:+.3f}      {np.abs(x-y).mean():.3f}")

# Diferencia global de composicion por quipu
mad = np.mean([np.abs(f[3].get(x, 0) - f[4].get(x, 0))
               for f in filas for x in colores])
print("\ndiferencia media absoluta global (8 colores):", round(mad, 4))
print("Interpretacion: KFG y OKR son casi la misma observacion (no son")
print("controles independientes). El color sigue sin validacion externa;")
print("Milillo et al. no puede refutarse ni confirmarse con estas bases.")

print("\n=== Join naive por ordinal (para documentar el artefacto) ===")
m = c.merge(q[["kfg", "kid"]], on="kfg").merge(
    okr[["KHIPU_ID", "CORD_ORDINAL", "COLOR_CD_1"]],
    left_on=["kid", "orden"], right_on=["KHIPU_ID", "CORD_ORDINAL"], how="inner")
m = m[m.cb.notna() & m.COLOR_CD_1.notna()]
print("cuerdas comparables:", len(m),
      "| concordancia:", round((m.cb == m.COLOR_CD_1).mean(), 3))
