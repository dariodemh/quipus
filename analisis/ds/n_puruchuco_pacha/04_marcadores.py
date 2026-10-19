"""04: regla (d) y uso de OKR. Marcadoras (M) y cuerdas superiores (T) en los
tres archivos; bloques de UR073 delimitados por sus 5 marcadoras frente a las
6 secciones de UR063 (copia rota)."""
import pandas as pd
import numpy as np
import comun_np as L

c, q = L.cargar_kfg()
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


ks = sorted(set(q[q.procedencia.isin(["Pachacamac", "Incahuasi"])].kfg) |
            set(q[q.region == "Puruchuco"].kfg))
okr, mapa = L.cargar_okr(ks)
okr["M"] = okr.CORD_CLASSIFICATION.fillna("") == "M"
okr["T"] = okr.CORD_CLASSIFICATION.fillna("") == "T"

pr("Inventario OKR (cuerdas nivel 0 = colgantes; nivel<0 = superiores):")
for name, sel in [("Pachacamac", q.procedencia == "Pachacamac"),
                  ("Puruchuco", q.region == "Puruchuco"),
                  ("Incahuasi", q.procedencia == "Incahuasi")]:
    kk = set(q[sel].kfg)
    d = okr[okr.kfg.isin(kk)]
    pr(f"  {name}: {len(kk)} quipus, {len(d)} cuerdas; "
       f"superiores (nivel<0)={int((d.nivel_okr<0).sum())} en "
       f"{d[d.nivel_okr<0].kfg.nunique()} quipus; marcadoras M={int(d.M.sum())} en "
       f"{d[d.M].kfg.nunique()} quipus; clase T={int(d["T"].sum())}")

pr("\nQuipus de Pachacamac con marcadoras:")
d = okr[okr.kfg.isin(set(q[q.procedencia == "Pachacamac"].kfg)) & okr.M]
pr(d.groupby("kfg").size().to_string())

# UR073: 5 marcadoras -> 6 bloques; comparar con las 6 secciones de UR063
r73 = L.registros_okr(okr, "UR073")
sec73 = [(x["n"], x["p"], x["x"]) for x in r73]
pr("\nUR073: bloques delimitados por las 5 marcadoras M (n, suma P, cabecera):")
pr("  ", sec73)
regs63 = L.registros_kfg(c, "UR063")
# seis secciones = grupos KFG 0 | 1+2+3 | 4 | 5 | 6 | 7
grupos = [x["p"] for x in regs63]
g = regs63
sec63 = [g[0]["p"], g[1]["p"] + g[2]["p"] + g[3]["p"], g[4]["p"], g[5]["p"], g[6]["p"], g[7]["p"]]
pr("UR063: seis secciones (sumas P):", sec63)
pr("Diferencias bloque UR073 - seccion UR063 (primeros 5):",
    [a[1] - b for a, b in zip(sec73[:5], sec63[:5])])
pr("La 6.a seccion de UR063 (233) no tiene bloques en UR073: quipu roto (69 cuerdas).")

# top cords de UR1096
t = okr[okr["T"]]
if len(t):
    pr("\nCuerdas superiores T en la muestra:",
       t[["kfg", "CORD_ORDINAL", "valor"]].to_string(index=False))

with open(L.AQUI / "salida_04_marcadores.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
