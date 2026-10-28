# -*- coding: utf-8 -*-
"""
05_tabla.py
Genera tabla_afirmaciones.csv: contraste de las cifras de Urton & Brezine (2009)
contra KFG (cuerdas.csv) y OKR (khipu.db).
"""
import re
import sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = BASE + r"\analisis\ds\n_urton_brezine_sz"
DB = BASE + r"\data\external\open-khipu-repository\data\khipu.db"

cuerdas = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
quipus = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")
quipus["prov"] = quipus.procedencia.fillna("").str.strip()
quipus.loc[quipus.prov.str.lower().isin(["unknown", ""]), "prov"] = "SIN"
exec(open(OUT + r"\arch12.py", encoding="utf-8").read())
quipus["arch"] = quipus.prov.map(arch12)
quipus.loc[quipus.region.fillna("").str.strip() == "Puruchuco", "arch"] = "Puruchuco"
ARCHS = ["Pachacamac", "Ica", "Laguna de los Condores", "Nazca", "Arica", "Paracas",
         "Chancay", "Santa", "Ocucaje", "Atarco", "Tambo Colorado", "Puruchuco"]

# --- KFG parse
PAT = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([SZUszu]?)\)")
rows = []
for r in cuerdas.itertuples():
    if not isinstance(r.nudos, str):
        continue
    for m in PAT.finditer(r.nudos):
        t = m.group(2)
        d = (m.group(4) or "U").upper()
        n = int(m.group(1)) if t in ("S", "SP") else 1
        if d not in ("S", "Z"):
            d = "U"
        rows.append((r.kfg, t, d, n))
kk = pd.DataFrame(rows, columns=["kfg", "t", "d", "n"])
kk["t3"] = kk.t.where(kk.t.isin(["S", "L", "E"]), "otros")


def pctS(df):
    x = df[df.d.isin(["S", "Z"])]
    return 100 * (x.d == "S").mean() if len(x) else np.nan, len(x)


def one(df, nm):
    x = df.groupby(["t3", "d"]).n.sum().unstack(fill_value=0).reindex(columns=["S", "Z", "U"], fill_value=0)
    out = {}
    for t in ["S", "L", "E"]:
        if t in x.index:
            ss = x.loc[t, "S"]; zz = x.loc[t, "Z"]
            out[t] = (round(100 * ss / (ss + zz), 1), int(ss + zz))
    return out


# --- OKR
con = sqlite3.connect(DB)
knot = pd.read_sql("select k.CORD_ID,k.TYPE_CODE,k.DIRECTION,c.KHIPU_ID from knot k "
                   "join cord c on c.CORD_ID=k.CORD_ID", con)
knot["n"] = 1
knot["t3"] = knot.TYPE_CODE.where(knot.TYPE_CODE.isin(["S", "L", "E"]), "otros")
knot["d"] = knot.DIRECTION.fillna("U")
knot.loc[~knot.d.isin(["S", "Z"]), "d"] = "U"
ot = knot.groupby(["t3", "d"]).size().unstack(fill_value=0).reindex(columns=["S", "Z", "U"], fill_value=0)

cord = pd.read_sql("select KHIPU_ID,CORD_ID,TWIST,FIBER from cord", con)
km = pd.read_sql("select KHIPU_ID,OKR_NUM,PROVENANCE from khipu_main", con)
okr_arch = km.PROVENANCE.fillna("").str.strip().map(arch12)
n_okr12 = int(okr_arch.isin(ARCHS).sum())
n_okr = len(km)

# --- perquipu KFG
o = kk[kk.d.isin(["S", "Z"])]
qk = o.groupby("kfg").d.agg(n_dir="size", pZ=lambda s: (s == "Z").mean())
qk = qk[qk.n_dir > 0]
# all-oriented: no U
u = kk[kk.d == "U"].groupby("kfg").n.sum().reindex(qk.index).fillna(0)
qallo = qk[u == 0]

# --- perquipu OKR
o2 = knot[knot.d.isin(["S", "Z"])]
qo = o2.groupby("KHIPU_ID").d.agg(n_dir="size", pZ=lambda s: (s == "Z").mean())
qo = qo[qo.n_dir > 0]
u2 = knot[knot.d == "U"].groupby("KHIPU_ID").size().reindex(qo.index).fillna(0)
qoallo = qo[u2 == 0]

# --- torsion
kT = cuerdas.torsion.fillna("NA").replace("", "NA").value_counts()
oT = cord.TWIST.fillna("NA").replace("", "NA").value_counts()
tS, tZ = int(kT.get("S", 0)), int(kT.get("Z", 0))
oS, oZ = int(oT.get("S", 0)), int(oT.get("Z", 0))

# --- fibra
fib = cord.FIBER.dropna()
fib = fib[fib != ""]
zfib = cord[(cord.TWIST == "Z") & cord.FIBER.notna() & (cord.FIBER != "")].FIBER

tK = one(kk, "KFG")
tO = one(knot, "OKR")

rows = []
R = rows.append
R(dict(id="U07a", afirmacion="Khipus con procedencia en 12 archivos",
       cifra_UB="222 de 451 (49,2%)",
       KFG=f"{int(quipus.arch.isin(ARCHS).sum())} de {len(quipus)} ({100*quipus.arch.isin(ARCHS).mean():.1f}%)",
       OKR=f"{n_okr12} de {n_okr} ({100*n_okr12/n_okr:.1f}%)",
       comentario="Depende de la definicion de 'archivo' y del tamano del corpus.",
       nivel="apoyado con datos (proporcion), no reproducible en absoluto"))
R(dict(id="U07b", afirmacion="Pachacamac es el archivo mayor",
       cifra_UB="68", KFG=f"{int((quipus.arch=='Pachacamac').sum())} (14,0%)",
       OKR=f"{int((okr_arch=='Pachacamac').sum())} ({100*(okr_arch=='Pachacamac').mean():.1f}%)",
       comentario="La proporcion se mantiene (~15%); el absoluto crece con el corpus.",
       nivel="bien apoyado"))
R(dict(id="U07c", afirmacion="Khipus sin procedencia",
       cifra_UB="229 de 451 (50,8%)",
       KFG=f"{int((~quipus.arch.isin(ARCHS)).sum())} de {len(quipus)} ({100*(~quipus.arch.isin(ARCHS)).mean():.1f}%)",
       OKR=f"{n_okr-n_okr12} de {n_okr} ({100*(1-n_okr12/n_okr):.1f}%)",
       comentario="Misma proporcion; el corpus crecio de 451 a 651.",
       nivel="apoyado con datos"))
R(dict(id="U08", afirmacion="Media de cordeles por khipu: 218 (Nazca) a 10 (Chancay); max 323; min 12",
       cifra_UB="218-10; 323; 12", KFG="media 231 (Nazca) - 26 (Chancay); max 1831 (Arica); min 5",
       OKR="no calculado por archivo",
       comentario="Orden de magnitud similar; los extremos dependen de incluir khipus gigantes (AS069).",
       nivel="apoyado con datos (parcial)"))
R(dict(id="U09", afirmacion="Khipus mayores: Laguna 870, Arica 1585; Pachacamac 338, Puruchuco 114",
       cifra_UB="870; 1585; 338; 114",
       KFG="874 (UR006); 1831 (AS069); 338 exacto; 225 (max Puruchuco)",
       OKR="no calculado",
       comentario="Pachacamac 338 y Laguna 874 casi exactos. Arica crecio (1831). Puruchuco no coincide.",
       nivel="apoyado con datos"))
R(dict(id="U10", afirmacion="Khipus con cordeles subsidiarios",
       cifra_UB="291 de 451 (64,5%)",
       KFG=f"{int((cuerdas[cuerdas.nivel>=1].groupby('kfg').size().reindex(quipus.kfg).fillna(0)>0).sum())} de {len(quipus)} ({100*(cuerdas[cuerdas.nivel>=1].groupby('kfg').size().reindex(quipus.kfg).fillna(0)>0).mean():.1f}%)",
       OKR="no calculado",
       comentario="Casi identico.",
       nivel="bien apoyado"))
R(dict(id="U12", afirmacion="Cordeles con datos de material: 15.616 (40%); 85% algodon, 9% camelido, 6% otros",
       cifra_UB="15.616; 85/9/6",
       KFG="sin campo de fibra",
       OKR=f"{len(fib)} ({100*len(fib)/len(cord):.1f}%); {100*(fib=='CN').mean():.0f}% algodon, {100*(fib=='CL').mean():.1f}% camelido",
       comentario="Mas cords documentados y mas algodon que en 2009; el camelido esta subrepresentado.",
       nivel="apoyado con datos (composicion distinta)"))
R(dict(id="U14a", afirmacion="Cordeles con retorcido final S / Z",
       cifra_UB="96% S / 4% Z (1.012 Z de 26.279)",
       KFG=f"{100*tS/(tS+tZ):.2f}% S / {100*tZ/(tS+tZ):.2f}% Z ({tZ} Z de {tS+tZ})",
       OKR=f"{100*oS/(oS+oZ):.2f}% S / {100*oZ/(oS+oZ):.2f}% Z ({oZ} Z de {oS+oZ})",
       comentario="La proporcion Z se duplica (4% -> 7%); el absoluto Z se triplica. Depende de la fibra (38% Z en camelido vs 9% en algodon).",
       nivel="apoyado con datos (cambio de corpus)"))
R(dict(id="U14b", afirmacion="De los cordeles Z, 54% camelido y 33% algodon",
       cifra_UB="54% camelido; 33% algodon",
       KFG="sin fibra", OKR=f"{100*(zfib=='CL').mean():.0f}% camelido; {100*(zfib=='CN').mean():.0f}% algodon (entre los Z con fibra, n={len(zfib)})",
       comentario="No se reproduce: el numero absoluto de cordeles Z de camelido es parecido (495 vs ~546), pero hay 7x mas cordeles Z de algodon.",
       nivel="refutado en el corpus actual"))
R(dict(id="U16a", afirmacion="Total de nudos registrados",
       cifra_UB="70.660", KFG=f"{int(kk.n.sum())}", OKR=f"{len(knot)}",
       comentario="El corpus actual tiene 1,6-1,7x mas nudos.",
       nivel="cambio de corpus"))
R(dict(id="U16b", afirmacion="Nudos con orientacion conocida",
       cifra_UB="51.178 (72,4%)",
       KFG=f"{int(kk.loc[kk.d.isin(['S','Z']),'n'].sum())} ({100*kk.loc[kk.d.isin(['S','Z']),'n'].sum()/kk.n.sum():.1f}%)",
       OKR=f"{int(knot.d.isin(['S','Z']).sum())} ({100*knot.d.isin(['S','Z']).mean():.1f}%)",
       comentario="La cobertura de orientacion subio de 72% a 88%.",
       nivel="cambio de corpus"))
R(dict(id="U16c", afirmacion="Nudos simples: 35% S / 65% Z",
       cifra_UB="35/65", KFG=f"{tK['S'][0]}/{100-tK['S'][0]:.1f} (n={tK['S'][1]})",
       OKR=f"{tO['S'][0]}/{100-tO['S'][0]:.1f} (n={tO['S'][1]})",
       comentario="NO se reproduce: los simples son 26-27% S, no 35%. El 35/65 coincide con el agregado de TODOS los tipos (34,8% S en khipu_summary).",
       nivel="refutado / probable error de etiqueta"))
R(dict(id="U16d", afirmacion="Nudos largos: 53% S / 47% Z",
       cifra_UB="53/47", KFG=f"{tK['L'][0]}/{100-tK['L'][0]:.1f}", OKR=f"{tO['L'][0]}/{100-tO['L'][0]:.1f}",
       comentario="Reproduccion casi exacta.",
       nivel="bien apoyado"))
R(dict(id="U16e", afirmacion="Figura de ocho: 30% S / 70% Z",
       cifra_UB="30/70", KFG=f"{tK['E'][0]}/{100-tK['E'][0]:.1f}", OKR=f"{tO['E'][0]}/{100-tO['E'][0]:.1f}",
       comentario="Reproduccion cercana (27/73).",
       nivel="bien apoyado"))
R(dict(id="U17a", afirmacion="Patron todo-Z",
       cifra_UB="72 de 272 (26,5%)",
       KFG=f"{int((qallo.pZ==1).sum())} de {len(qallo)} ({100*(qallo.pZ==1).mean():.1f}%)",
       OKR=f"{int((qoallo.pZ==1).sum())} de {len(qoallo)} ({100*(qoallo.pZ==1).mean():.1f}%)",
       comentario="Proporcion casi identica; el denominador se duplica con el corpus.",
       nivel="bien apoyado"))
R(dict(id="U17b", afirmacion="Patron todo-S",
       cifra_UB="27 de 272 (9,9%)",
       KFG=f"{int((qallo.pZ==0).sum())} de {len(qallo)} ({100*(qallo.pZ==0).mean():.1f}%)",
       OKR=f"{int((qoallo.pZ==0).sum())} de {len(qoallo)} ({100*(qoallo.pZ==0).mean():.1f}%)",
       comentario="Casi identico.",
       nivel="bien apoyado"))
R(dict(id="U17c", afirmacion="Pachacamac tiene el mayor % de nudos Z",
       cifra_UB="cualitativo",
       KFG="Pachacamac 76,0% (todos) / 92,4% (simples); Puruchuco 80,6/97,5; Santa 81,3/83,4",
       OKR="Pachacamac 84,8%; Santa 96,2%; Puruchuco n.d.",
       comentario="Pachacamac esta en el grupo alto, pero NO es el maximo: Puruchuco y Santa lo superan, sin diferencia significativa. Si es significativo vs el resto en simples (q=0,007).",
       nivel="parcialmente apoyado"))
R(dict(id="U12b", afirmacion="Cordeles totales (texto vs figura)",
       cifra_UB="38.381 vs 38.831",
       KFG=f"{len(cuerdas)}", OKR=f"{len(cord)}",
       comentario="No se reproduce ninguno de los dos; el corpus actual es 1,42x mayor. La discrepancia de 450 es interna al capitulo (probable errata).",
       nivel="no verificable"))

df = pd.DataFrame(rows)
df.to_csv(OUT + r"\tabla_afirmaciones.csv", index=False, encoding="utf-8-sig")
print(df[["id", "afirmacion", "cifra_UB", "KFG", "OKR"]].to_string(index=False))
print("\nGuardado tabla_afirmaciones.csv")
