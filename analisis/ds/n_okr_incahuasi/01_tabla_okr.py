"""01 - Construye la tabla de cuerdas OKR equivalente a la de KFG (Incahuasi y resto).

Salida: cuerdas_okr.csv (una fila por cuerda OKR de los quipus con fila en puente.csv).
Columnas equivalentes a analisis/datos/cuerdas.csv:
  kfg, khipu_id, cord_id, orden, cuerda, nivel, padre, grupo, valor, color, union, pres, nudos, sep, clas
- nivel: CORD_LEVEL-1 (0 = colgante, 1 = subsidiaria, ...).
- grupo: indice (0-based) del CLUSTER_ID de la cuerda nivel 1, ordenado por CORD_ORDINAL.
         Las subsidiarias heredan el grupo de su colgante.
- valor: suma de knot.knot_value_type de la cuerda (unidades decimales ya resueltas en OKR).
- pres: la cuerda tiene >=1 nudo (0 sin nudos = ausente, como en KFG).
- sep: True si CORD_CLASSIFICATION == 'M' (marcadora / separador).
- color: FULL_COLOR de ascher_cord_color; las marcadoras se fuerzan a 'PK' para que
         lib18.registros las trate como separadores igual que en KFG.
- union: ATTACHMENT_TYPE.
"""
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
DB = RAIZ / "data/external/open-khipu-repository/data/khipu.db"
PUENTE = RAIZ / "analisis/17_okr_pendientes/puente.csv"


def cargar_okr(db=DB, puente=PUENTE):
    p = pd.read_csv(puente, keep_default_na=False)
    p = p[p.khipu_id.astype(str).str.strip() != ""].copy()
    p["khipu_id"] = p.khipu_id.astype(int)
    con = sqlite3.connect(db)
    cord = pd.read_sql("""select KHIPU_ID,CORD_ID,CORD_LEVEL,CORD_ORDINAL,CLUSTER_ID,CLUSTER_ORDINAL,
                                 PENDANT_FROM,ATTACHMENT_TYPE,CORD_CLASSIFICATION,CORD_LENGTH,TWIST
                          from cord where CORD_LEVEL>=1""", con)
    k = pd.read_sql("select CORD_ID, knot_value_type from knot", con)
    con.close()
    k["v"] = pd.to_numeric(k.knot_value_type, errors="coerce").fillna(0)
    val = k.groupby("CORD_ID").agg(valor=("v", "sum"), nnudos=("v", "size")).reset_index()
    cord = cord.merge(val, on="CORD_ID", how="left")
    cord["nnudos"] = cord.nnudos.fillna(0).astype(int)
    cord["valor"] = cord.valor.fillna(0).round().astype(int)
    cord["pres"] = cord.nnudos > 0
    for col in ["CORD_LEVEL", "CORD_ORDINAL", "CLUSTER_ID", "CLUSTER_ORDINAL"]:
        cord[col] = pd.to_numeric(cord[col], errors="coerce")

    con = sqlite3.connect(db)
    col = pd.read_sql("select CORD_ID,FULL_COLOR,COLOR_CD_1,color_id from ascher_cord_color order by color_id", con)
    con.close()
    col["color"] = col.FULL_COLOR.fillna("").replace("", np.nan)
    col["color"] = col.color.fillna(col.COLOR_CD_1.fillna(""))
    col = col.drop_duplicates("CORD_ID", keep="first")
    cord = cord.merge(col[["CORD_ID", "color"]], on="CORD_ID", how="left")
    cord["color"] = cord.color.fillna("")
    cord["clas"] = cord.CORD_CLASSIFICATION.fillna("")
    cord["sep"] = cord.clas == "M"
    cord.loc[cord.sep, "color"] = "PK"
    cord["union"] = cord.ATTACHMENT_TYPE.fillna("").replace("", "U")

    cord = cord[cord.KHIPU_ID.isin(p.khipu_id)].copy()
    cord = cord.sort_values(["KHIPU_ID", "CORD_LEVEL", "CORD_ORDINAL"]).reset_index(drop=True)

    # grupo = indice de cluster (nivel 1) por primer CORD_ORDINAL
    out = []
    for kid, s in cord.groupby("KHIPU_ID", sort=False):
        s = s.copy()
        l1 = s[s.CORD_LEVEL == 1].sort_values("CORD_ORDINAL")
        clusters = list(dict.fromkeys(l1.CLUSTER_ID.dropna().tolist()))
        gmap = {c: i for i, c in enumerate(clusters)}
        # grupo de cada cordon por su ancestro nivel 1
        parent = dict(zip(s.CORD_ID, s.PENDANT_FROM))
        level = dict(zip(s.CORD_ID, s.CORD_LEVEL))
        cluster = dict(zip(s.CORD_ID, s.CLUSTER_ID))
        gid = {}

        def grupo_de(cid):
            if cid in gid:
                return gid[cid]
            lv = level.get(cid)
            if lv == 1:
                g = gmap.get(cluster.get(cid), -1)
            else:
                par = parent.get(cid)
                g = grupo_de(par) if par in level else -1
            gid[cid] = g
            return g
        s["grupo"] = [grupo_de(c) for c in s.CORD_ID]

        # nombre jerarquico y orden DFS
        children = {}
        for r in s.itertuples():
            par = r.PENDANT_FROM if r.PENDANT_FROM in level else None
            children.setdefault(par, []).append(r.CORD_ID)
        for par in children:
            children[par] = sorted(children[par], key=lambda c: (level[c], _ord(s, c)))

        rows = []
        # nivel 1 en orden
        for cid in sorted([c for c in s.CORD_ID if level[c] == 1], key=lambda c: _ord(s, c)):
            rows.append(cid)

        nombre = {}
        orden = {}

        def dfs(cid, name):
            nombre[cid] = name
            orden[cid] = len(orden)
            for j, ch in enumerate(children.get(cid, []), start=1):
                if level[ch] == level[cid] + 1:
                    dfs(ch, f"{name}s{j}")
        for r in sorted([x for x in s.itertuples() if x.CORD_LEVEL == 1], key=lambda x: x.CORD_ORDINAL):
            dfs(r.CORD_ID, f"p{int(r.CORD_ORDINAL)}")
        s["cuerda"] = s.CORD_ID.map(nombre)
        s["orden"] = s.CORD_ID.map(orden)
        s["padre"] = [nombre.get(par, "") for par in s.PENDANT_FROM]
        s["khipu_id"] = kid
        out.append(s)

    d = pd.concat(out, ignore_index=True)
    d = d.merge(p[["khipu_id", "kfg"]], on="khipu_id", how="left")
    d["kfg"] = d.kfg.fillna("")
    d = d.sort_values(["kfg", "orden"]).reset_index(drop=True)
    return d, p


def _ord(s, cid):
    return float(s.loc[s.CORD_ID == cid, "CORD_ORDINAL"].iloc[0])


COLS = ["kfg", "khipu_id", "cord_id", "orden", "cuerda", "nivel", "padre", "grupo",
        "valor", "color", "union", "pres", "clas", "sep"]


def main():
    d, p = cargar_okr()
    d["nivel"] = (d.CORD_LEVEL - 1).astype(int)
    d["cord_id"] = d.CORD_ID
    d[COLS].to_csv(AQUI / "cuerdas_okr.csv", index=False)
    inc = ([f"JC{i:03d}" for i in range(1, 24)]
           + [f"UR{i}" for i in range(255, 281) if i not in (267, 273, 274)]
           + ["UR267A", "UR267B", "UR273A", "UR273B", "UR274A", "UR274B"])
    x = d[d.kfg.isin(inc)]
    print(f"OKR: {len(d)} cuerdas en {d.kfg.nunique()} quipus con kfg; Incahuasi {len(x)} cuerdas en {x.kfg.nunique()} quipus")
    print(x.groupby("nivel").size().to_string())
    print("Nivel 1 por nivel OKR:", x[x.CORD_LEVEL == 1].shape[0], "| T:", (x.clas == "T").sum(), "| M:", (x.clas == "M").sum())


if __name__ == "__main__":
    main()
