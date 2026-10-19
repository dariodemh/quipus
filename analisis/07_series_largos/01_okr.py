"""Paso 1: verificar las series de nudos largos contra la fuente cruda (OKR).

- Reconstruye, desde `knot` + `knot_cluster` del OKR, la secuencia de racimos de cada cuerda (tipo, vueltas, posicion, direccion).
- Define `serie_L` = cuerda con >=2 racimos y todos los racimos son un unico nudo L (sin S/E).
- Compara por quipu contra KFG (`06_nudos/racimos.csv`): numero de cuerdas serie_L y multiconjunto de "palabras" (tuplas de vueltas).
- Lista notas de campo (khipu_main.NOTES, cord.CORD_NOTES, knot_cluster.NOTES) y canutos de los quipus con series.
Salidas: okr_racimos.csv, okr_cuerdas.csv, 01_quipus.csv, 01_salida.txt
"""
import sqlite3
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
db = sqlite3.connect(RAIZ / "data/external/open-khipu-repository/data/khipu.db")
q = lambda s: pd.read_sql(s, db)

km = q("select KHIPU_ID, INVESTIGATOR_NUM inv, OKR_NUM okr, PROVENANCE, NOTES from khipu_main")
cord = q("select KHIPU_ID, CORD_ID, CORD_LEVEL, CORD_ORDINAL, PENDANT_FROM, ATTACHED_TO, CANUTO_ID, CANUTO_ORDINAL, "
         "CORD_LENGTH, THICKNESS, TWIST, FIBER, TERMINATION, CORD_NOTES from cord")
kc = q("select CORD_ID, CLUSTER_ID, START_POS, ORDINAL, NUM_KNOTS, NOTES from knot_cluster")
kn = q("select CORD_ID, CLUSTER_ID, TYPE_CODE, DIRECTION, NUM_TURNS, KNOT_ORDINAL, AXIS_ORIENTATION from knot")
kn["TYPE_CODE"] = kn.TYPE_CODE.str.replace("'", "").str.strip()

# --- racimo OKR: tipo(s), n.o de nudos, vueltas (L), direccion
g = kn.groupby("CLUSTER_ID")
rac = pd.DataFrame({
    "tipos": g.TYPE_CODE.agg(lambda s: "+".join(sorted(set(s)))),
    "nk": g.size(),
    "turns": g.NUM_TURNS.max(),
    "dir": g.DIRECTION.agg(lambda s: "".join(sorted(set(s)))),
}).reset_index()
rac = kc.merge(rac, on="CLUSTER_ID", how="left").merge(cord[["CORD_ID", "KHIPU_ID"]], on="CORD_ID")
rac = rac.sort_values(["CORD_ID", "START_POS", "ORDINAL"])
rac["j"] = rac.groupby("CORD_ID").cumcount()
rac.to_csv(AQUI / "okr_racimos.csv", index=False)

# --- cuerda OKR
def resumen(s):
    unL = ((s.tipos == "L") & (s.nk == 1)).all()
    return pd.Series({"ncl": len(s), "serie_L": len(s) >= 2 and unL,
                      "palabra": "-".join(str(int(t)) if t == t else "?" for t in s.turns) if unL else "",
                      "pos": ";".join(f"{p:g}" for p in s.START_POS), "dirs": "".join(s.dir.fillna("?"))})
oc = rac.groupby("CORD_ID").apply(resumen, include_groups=False).reset_index()
oc = cord.merge(oc, on="CORD_ID", how="left").merge(km[["KHIPU_ID", "inv", "okr"]], on="KHIPU_ID")
oc["ncl"] = oc.ncl.fillna(0).astype(int); oc["serie_L"] = oc.serie_L.fillna(False).astype(bool)
oc.to_csv(AQUI / "okr_cuerdas.csv", index=False)

# --- KFG
r6 = pd.read_csv(RAIZ / "analisis/06_nudos/racimos.csv", low_memory=False)
qu = pd.read_csv(RAIZ / "analisis/datos/quipus.csv")
kg = r6.groupby("i").agg(kfg=("kfg", "first"), ncl=("j", "size"), allL=("tipo", lambda s: (s == "L").all()),
                         palabra=("n", lambda s: "-".join(str(int(x)) if x == x else "?" for x in s)))
kg["serie_L"] = kg.allL & (kg.ncl >= 2)

out = []
for _, r in qu.iterrows():
    a = kg[kg.kfg == r.kfg]; b = oc[oc.okr == r.okr]
    wa = Counter(a.palabra[a.serie_L]); wb = Counter(b.palabra[b.serie_L])
    inter = sum((wa & wb).values())
    out.append(dict(kfg=r.kfg, okr=r.okr, procedencia=r.procedencia, kfg_cuerdas_nudo=len(a), kfg_serieL=int(a.serie_L.sum()),
                    okr_cuerdas_nudo=int((b.ncl > 0).sum()), okr_serieL=int(b.serie_L.sum()),
                    palabras_comunes=inter, okr_canutos=int(b.CANUTO_ID.fillna(0).gt(0).sum()) if len(b) else 0))
Q = pd.DataFrame(out)
Q["frac_kfg"] = Q.kfg_serieL / Q.kfg_cuerdas_nudo.replace(0, np.nan)
Q["frac_okr"] = Q.okr_serieL / Q.okr_cuerdas_nudo.replace(0, np.nan)
Q.sort_values("kfg_serieL", ascending=False).to_csv(AQUI / "01_quipus.csv", index=False)

f = open(AQUI / "01_salida.txt", "w", encoding="utf-8")
def P(*a):
    print(*a); print(*a, file=f)

P("Cuerdas serie_L: KFG", int(kg.serie_L.sum()), "| OKR", int(oc.serie_L.sum()))
P("Quipus con >=1 serie_L: KFG", int((Q.kfg_serieL > 0).sum()), "| OKR", int((Q.okr_serieL > 0).sum()))
top = Q.sort_values("kfg_serieL", ascending=False).head(25)
P(top[["kfg", "okr", "procedencia", "kfg_cuerdas_nudo", "kfg_serieL", "okr_serieL", "palabras_comunes", "frac_kfg", "okr_canutos"]].round(2).to_string(index=False))
P("\nQuipus con canutos en OKR:", sorted(oc.loc[oc.CANUTO_ID.fillna(0) > 0, "inv"].unique()))

OBJ = ["UR039", "UR050", "UR051", "UR052", "UR054", "UR055", "UR110", "UR112", "UR144"]
ro = rac[rac.KHIPU_ID.isin(km[km.inv.isin(OBJ)].KHIPU_ID)]
P("\nRacimos OKR en los quipus objetivo: tipos", ro.tipos.value_counts().to_dict())
P("n.o de nudos por racimo L:", ro[ro.tipos == "L"].nk.value_counts().to_dict())
P("vueltas L:", ro[ro.tipos == "L"].turns.value_counts().sort_index().to_dict())
P("direccion L:", ro[ro.tipos == "L"].dir.value_counts().to_dict())
ax = kn[kn.CORD_ID.isin(ro.CORD_ID) & (kn.TYPE_CODE == "L")].AXIS_ORIENTATION.replace("", "vacio").value_counts().to_dict()
P("AXIS_ORIENTATION L:", ax)

for inv in OBJ:
    k = km[km.inv == inv]
    if k.empty: continue
    k = k.iloc[0]
    P(f"\n=== {inv} ({k.okr}) procedencia OKR='{k.PROVENANCE}'")
    P("NOTES:", (k.NOTES or "").replace("\n", " | ")[:900])
    cn = oc[(oc.KHIPU_ID == k.KHIPU_ID) & (oc.CORD_NOTES.fillna("").str.strip() != "")].CORD_NOTES.str.strip()
    P(f"CORD_NOTES ({len(cn)}):", " || ".join(cn.unique()[:25])[:1500])
    kn_ = rac[(rac.KHIPU_ID == k.KHIPU_ID) & (rac.NOTES.fillna("").str.strip() != "")].NOTES
    P(f"cluster NOTES ({len(kn_)}):", " || ".join(kn_.unique()[:10])[:600])
    b = oc[oc.KHIPU_ID == k.KHIPU_ID]
    P("cuerdas por canuto:", b[b.CANUTO_ID > 0].groupby("CANUTO_ID").size().value_counts().to_dict(),
      "| cuerdas fuera de canuto:", int((b.CANUTO_ID.fillna(0) == 0).sum()), "| niveles:", b.CORD_LEVEL.value_counts().to_dict())
f.close()

# --- comparacion racimo a racimo en los quipus objetivo (colgante n <-> CORD_ORDINAL n de nivel 1; misma posicion cm)
f = open(AQUI / "01_salida.txt", "a", encoding="utf-8")
P("\n=== Concordancia racimo a racimo KFG vs OKR (colgantes; emparejados por n.o de colgante y posicion)")
filas = []
for inv in OBJ + ["UR193", "UR1087", "UR177", "UR1145"]:
    ok = km[km.inv == inv].KHIPU_ID.iloc[0]
    A = r6[(r6.kfg == inv) & (r6.nivel == 0)].copy()
    A["n_c"] = A.cuerda.str.extract(r"^p(\d+)$")[0].astype(float)
    B = rac[rac.KHIPU_ID == ok].merge(cord[["CORD_ID", "CORD_LEVEL", "CORD_ORDINAL"]], on="CORD_ID")
    B = B[B.CORD_LEVEL == 1].rename(columns={"CORD_ORDINAL": "n_c", "START_POS": "pos"})
    m = A.merge(B, on=["n_c", "pos"], how="outer", indicator=True)
    both = m[m._merge == "both"]
    filas.append(dict(quipu=inv, kfg=len(A), okr=len(B), emparejados=len(both),
                      mismo_tipo=float((both.tipo == both.tipos).mean()),
                      mismas_vueltas=float((both.n == both.turns)[both.tipo == "L"].mean()),
                      misma_dir=float((both["dir_x"] == both["dir_y"]).mean())))
    if inv == "UR144":
        dif = both[(both.tipo == "L") & (both.n != both.turns)]
        P("UR144 diferencias de vueltas (KFG - OKR):", (dif.n - dif.turns).value_counts().to_dict(),
          "| racimo j (0=arriba):", dif.j_x.value_counts().to_dict(), "| KFG n:", dif.n.value_counts().to_dict())
P(pd.DataFrame(filas).round(3).to_string(index=False))
f.close()
