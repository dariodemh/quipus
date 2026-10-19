"""Paso 2a: tabla de cuerdas para el analisis de "palabras" (secuencias de vueltas de nudos largos).

- Quipus foco (F): los 9 con series de largos (todos con canutos/atado de cuerdas en el OKR, ver 01).
- Para cada cuerda: k racimos, tipos, vueltas (arriba->abajo), posiciones (cm), direcciones, color, grupo KFG, canuto (OKR).
- Referencia decimal (nulo c): cuerdas "decimales limpias" de los demas quipus (niveles estrictamente decrecientes,
  S en niveles >0, k>=2), palabra = digitos de los racimos presentes.
Salidas: cuerdas_foco.csv, cuerdas_decimal.csv
"""
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
F = ["UR039", "UR050", "UR051", "UR052", "UR054", "UR055", "UR110", "UR112", "UR144"]
ARTEF = {"AS090_N2", "AS019", "AS004", "UR211", "UR1095", "UR193", "KH0001"}  # n = valor (06_nudos)

r = pd.read_csv(RAIZ / "analisis/06_nudos/racimos.csv", low_memory=False)
cu = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
j2s = lambda s: ";".join("?" if x != x else f"{x:g}" for x in s)

def por_cuerda(rr):
    g = rr.sort_values(["i", "j"]).groupby("i")
    t = g.agg(kfg=("kfg", "first"), cuerda=("cuerda", "first"), orden=("orden", "first"), nivel=("nivel", "first"),
              grupo=("grupo", "first"), color=("color", "first"), largo=("largo", "first"), k=("j", "size"),
              tipos=("tipo", lambda s: "".join(s)), vueltas=("n", j2s), pos=("pos", j2s), dirs=("dir", lambda s: "".join(s)),
              niv=("niv", j2s), valor=("valor", "first"))
    return t.reset_index()

T = por_cuerda(r[r.kfg.isin(F)])
T["soloL"] = T.tipos.str.fullmatch("L+") & ~T.vueltas.str.contains(r"\?")
T["serie"] = T.soloL & (T.k >= 2)
T["n_c"] = T.cuerda.str.extract(r"^p(\d+)$")[0].astype(float)

# canuto del OKR (colgantes nivel 1, CORD_ORDINAL = n.o de colgante)
oc = pd.read_csv(AQUI / "okr_cuerdas.csv", low_memory=False)
oc = oc[(oc.CORD_LEVEL == 1) & oc.inv.isin(F)][["inv", "CORD_ORDINAL", "CANUTO_ID", "CANUTO_ORDINAL"]]
T = T.merge(oc.rename(columns={"inv": "kfg", "CORD_ORDINAL": "n_c"}), on=["kfg", "n_c"], how="left")
# UR051: sin canutos en OKR pero las notas dicen "cord wrapped with rest of group": se usa el grupo KFG
m = T.kfg == "UR051"
T.loc[m, "CANUTO_ID"] = 9e6 + T.loc[m, "grupo"]
T.loc[m, "CANUTO_ORDINAL"] = T[m].groupby("grupo").orden.rank().values
T.to_csv(AQUI / "cuerdas_foco.csv", index=False)

# referencia decimal
D = r[~r.kfg.isin(F) & ~r.kfg.isin(ARTEF)]
D = por_cuerda(D)
def limpia(row):
    if row.k < 2 or "?" in row.niv or "?" in row.vueltas: return False
    nv = [float(x) for x in row.niv.split(";")]
    if any(a <= b for a, b in zip(nv, nv[1:])): return False
    return all(t == "S" for t, v in zip(row.tipos, nv) if v > 0) and all(t in "SLE" for t in row.tipos) and len(row.tipos) == row.k
D = D[D.apply(limpia, axis=1)]
D.to_csv(AQUI / "cuerdas_decimal.csv", index=False)
print("foco:", len(T), "cuerdas; series:", int(T.serie.sum()), "| sin canuto:", int(T.CANUTO_ID.isna().sum()))
print("decimal limpias k>=2:", len(D), "en", D.kfg.nunique(), "quipus")
