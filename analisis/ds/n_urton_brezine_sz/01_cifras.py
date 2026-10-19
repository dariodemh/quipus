# -*- coding: utf-8 -*-
"""
01_cifras.py
Reproduce (o intenta reproducir) las cifras de Urton & Brezine (2009) sobre
nudos (direccion S/Z) y torsion de cordeles, en dos fuentes nuestras:
  - KFG: analisis/datos/cuerdas.csv (campo `nudos` y `torsion`)
  - OKR: data/external/open-khipu-repository/data/khipu.db (tablas knot, cord)
Escribe tablas en salida_01.txt y CSVs auxiliares. No imprime nada grande.
"""
import re
import sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = BASE + r"\analisis\ds\n_urton_brezine_sz"
DB = BASE + r"\data\external\open-khipu-repository\data\khipu.db"

# ---------------------------------------------------------------- KFG
cuerdas = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
quipus = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")

# Parseo de `nudos`: nTIPO(pos,dir),valor  separados por ';'
PAT = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([SZUszu]?)\)")
# Tipos que representan una corrida de n kudos simples; el resto = 1 nudo
RUN_TYPES = {"S", "SP"}          # SP = "simple pendiente"? se cuenta como corrida
COUNT_AS_ONE = {"L", "E", "EE", "LL", "TF", "BL", "U", "M"}


def parse_nudos(s):
    """Devuelve lista de (tipo, direccion, numero_de_nudos)."""
    out = []
    for m in PAT.finditer(str(s)):
        n = int(m.group(1))
        t = m.group(2)
        d = (m.group(4) or "U").upper()
        if d not in ("S", "Z"):
            d = "U"
        k = n if t in RUN_TYPES else 1
        out.append((t, d, k))
    return out


rows = []
per_quipu = {}
for r in cuerdas.itertuples():
    if isinstance(r.nudos, str) and r.nudos.strip() not in ("", ";"):
        for t, d, k in parse_nudos(r.nudos):
            rows.append((r.kfg, t, d, k))
kn = pd.DataFrame(rows, columns=["kfg", "tipo", "dir", "n"])

# Tipos principales y "otros"
kn["tipo2"] = kn.tipo.where(kn.tipo.isin(["S", "L", "E"]), "otros")
tot_knots = int(kn.n.sum())
tab_tipo = (kn.groupby(["tipo2", "dir"]).n.sum().unstack(fill_value=0)
              .reindex(columns=["S", "Z", "U"], fill_value=0))
tab_tipo["total"] = tab_tipo.sum(axis=1)
tab_tipo["n_orient"] = tab_tipo.S + tab_tipo.Z
tab_tipo["pct_S"] = 100 * tab_tipo.S / tab_tipo.n_orient.replace(0, np.nan)
tab_tipo["pct_Z"] = 100 * tab_tipo.Z / tab_tipo.n_orient.replace(0, np.nan)

# Torsion de cordel (KFG)
tors = cuerdas.torsion.fillna("NA").replace("", "NA").value_counts()

# ---------------------------------------------------------------- OKR
con = sqlite3.connect(DB)
knot = pd.read_sql("select k.CORD_ID, k.TYPE_CODE, k.DIRECTION, c.KHIPU_ID "
                   "from knot k join cord c on c.CORD_ID=k.CORD_ID", con)
cord = pd.read_sql("select KHIPU_ID, CORD_ID, TWIST, FIBER from cord", con)
kmain = pd.read_sql("select KHIPU_ID, OKR_NUM, PROVENANCE, REGION from khipu_main", con)

knot["tipo2"] = knot.TYPE_CODE.where(knot.TYPE_CODE.isin(["S", "L", "E"]), "otros")
knot["dir"] = knot.DIRECTION.fillna("U").replace("", "U")
knot.loc[~knot.dir.isin(["S", "Z"]), "dir"] = "U"
ot_tab = (knot.groupby(["tipo2", "dir"]).size().unstack(fill_value=0)
              .reindex(columns=["S", "Z", "U"], fill_value=0))
ot_tab["total"] = ot_tab.sum(axis=1)
ot_tab["n_orient"] = ot_tab.S + ot_tab.Z
ot_tab["pct_S"] = 100 * ot_tab.S / ot_tab.n_orient.replace(0, np.nan)
ot_tab["pct_Z"] = 100 * ot_tab.Z / ot_tab.n_orient.replace(0, np.nan)
ot_tors = cord.TWIST.fillna("NA").replace("", "NA").value_counts()

# ---------------------------------------------------------------- por quipu
# KFG: proporcion Z por quipu (todos los tipos y solo S)
def prop_z(g):
    o = g[g.dir.isin(["S", "Z"])]
    return pd.Series({"n_dir": len(o), "pZ": (o.dir == "Z").mean() if len(o) else np.nan})


qk = kn.groupby("kfg").apply(prop_z, include_groups=False)
qkS = kn[kn.tipo == "S"].groupby("kfg").apply(prop_z, include_groups=False)
qkS.columns = ["n_dir_S", "pZ_S"]

# OKR idem
ok = knot.groupby("KHIPU_ID").apply(prop_z, include_groups=False)
okS = knot[knot.tipo2 == "S"].groupby("KHIPU_ID").apply(prop_z, include_groups=False)
okS.columns = ["n_dir_S", "pZ_S"]

# Patrones todo-Z / todo-S (solo quipus con TODOS los nudos orientados y >=1)
def patrones(q):
    o = q[q.n_dir > 0]
    return pd.Series({"quipus_con_nudos": len(q), "quipus_orientados": len(o),
                      "todo_Z": int((o.pZ == 1).sum()), "todo_S": int((o.pZ == 0).sum()),
                      "mixtos": int(((o.pZ > 0) & (o.pZ < 1)).sum())})

pat_kfg = patrones(qk)
pat_okr = patrones(ok)
# version con >= 10 nudos orientados
pat_kfg10 = patrones(qk[qk.n_dir >= 10])
pat_okr10 = patrones(ok[ok.n_dir >= 10])

# ---------------------------------------------------------------- procedencia
quipus["prov"] = quipus.procedencia.fillna("").str.strip()
quipus.loc[quipus.prov.str.lower().isin(["unknown", ""]), "prov"] = "SIN"
prov_vc = quipus.prov.value_counts()
non_sin = quipus[quipus.prov != "SIN"]
# top 12 etiquetas exactas
top12 = prov_vc.drop("SIN", errors="ignore").head(12)

# Agrupacion amplia por "archivo" (aproximacion a las 12 de U&B)
def archivo(p):
    p0 = p.lower()
    if p in ("SIN",):
        return "SIN"
    if "pachac" in p0:
        return "Pachacamac"
    if "incahuasi" in p0 or "inkawasi" in p0:
        return "Incahuasi"
    if "leymebamba" in p0:
        return "Leymebamba"
    if "ica" in p0 or "ocucaje" in p0 or "callango" in p0 or "ulluj" in p0 or "pisco" in p0 or "paracas" in p0:
        return "Ica-Pisco-Paracas"
    if "nazca" in p0 or "nasca" in p0:
        return "Nazca"
    if "armatambo" in p0 or "huaca san pedro" in p0:
        return "Armatambo"
    if "chancay" in p0 or "huando" in p0:
        return "Chancay"
    if "huacho" in p0 or "huaura" in p0:
        return "Huacho"
    if "arica" in p0 or "lluta" in p0 or "miller" in p0:
        return "Arica"
    if "santa" in p0:
        return "Santa"
    if "tambo colorado" in p0:
        return "Tambo Colorado"
    if "huaquerones" in p0:
        return "Huaquerones"
    if "lima" in p0 or "lurin" in p0 or "rimac" in p0 or "molina" in p0 or "maranga" in p0 or "cajamarquilla" in p0 or "chuquitanta" in p0:
        return "Lima"
    return "Otra/vaga"


quipus["archivo"] = quipus.prov.map(archivo)
arch_vc = quipus.archivo.value_counts()

# Merge KFG per-quipu con metadatos
meta = quipus.set_index("kfg")
qk_all = qk.join(meta[["prov", "archivo", "region"]], how="left")
qkS_all = qkS.join(meta[["prov", "archivo", "region"]], how="left")
qk_all.to_csv(OUT + r"\perquipu_kfg.csv")
qkS_all.to_csv(OUT + r"\perquipu_kfg_S.csv")

# OKR per-quipu con provenance
okm = ok.join(kmain.set_index("KHIPU_ID")[["OKR_NUM", "PROVENANCE", "REGION"]], how="left")
okm["prov"] = okm.PROVENANCE.fillna("").str.strip()
okm.loc[okm.prov.str.lower().isin(["unknown", ""]), "prov"] = "SIN"
okm["archivo"] = okm.prov.map(archivo)
okm.to_csv(OUT + r"\perquipu_okr.csv")

# ---------------------------------------------------------------- salida
lines = []
A = lines.append
A("=== CORPUS ===")
A(f"KFG cuerdas.csv: {len(cuerdas)} cuerdas, {cuerdas.kfg.nunique()} quipus")
A(f"KFG quipus.csv: {len(quipus)} quipus; con procedencia no-Unknown: {len(non_sin)}; etiquetas distintas: {non_sin.prov.nunique()}")
A(f"OKR: {len(kmain)} quipus, {len(cord)} cuerdas, {len(knot)} nudos")
A("")
A("=== NUDOS POR TIPO Y DIRECCION ===")
A("KFG (parseado de cuerdas.csv):")
A(tab_tipo.round(1).to_string())
A(f"KFG total nudos (corridas S contadas como n): {tot_knots}; orientados: {int(tab_tipo.n_orient.sum())}")
A("")
A("OKR (tabla knot):")
A(ot_tab.round(1).to_string())
A(f"OKR total nudos: {len(knot)}; orientados: {int(ot_tab.n_orient.sum())}")
A("")
A("=== TORSION DE CORDEL ===")
A("KFG torsion: " + tors.to_dict().__str__())
A("OKR TWIST: " + ot_tors.to_dict().__str__())
A("")
A("=== PATRONES POR QUIPU (todos los nudos orientados) ===")
A("KFG: " + pat_kfg.to_dict().__str__())
A("KFG >=10 nudos orientados: " + pat_kfg10.to_dict().__str__())
A("OKR: " + pat_okr.to_dict().__str__())
A("OKR >=10 nudos orientados: " + pat_okr10.to_dict().__str__())
A("")
A("=== PROCEDENCIA ===")
A(f"Top 12 etiquetas exactas (suman {int(top12.sum())}):")
A(top12.to_string())
A("")
A("Agrupacion amplia (archivo):")
A(arch_vc.to_string())
A("")
A("=== QUIPUS CON / SIN PROCEDENCIA ===")
A(f"KFG con etiqueta != SIN: {len(non_sin)} de {len(quipus)} ({100*len(non_sin)/len(quipus):.1f}%)")

with open(OUT + r"\salida_01.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines[:8]))
print("... escrito salida_01.txt")
