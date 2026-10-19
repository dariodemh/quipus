"""14_copias · Tarea 3: material para verificación en museo.
Salidas: verificacion_objetos.csv (una fila por quipu implicado), verificacion_pares.csv (una fila por par, con la predicción
bajo "mismo objeto" y bajo "copia" y las cuerdas a mirar), verificacion_UR1107_UR237.csv (cuerda a cuerda),
verificacion_HP055_UR1084.csv (discordancias y cuerdas sin pareja).
"""
import re, sqlite3
from pathlib import Path
import numpy as np, pandas as pd

OUT = Path(__file__).resolve().parent
RAIZ = OUT.parents[1]
C = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv")
Q = pd.read_csv(RAIZ / "analisis/datos/quipus.csv").set_index("kfg")
R = pd.read_csv(OUT / "pares_resumen.csv")
F = pd.read_csv(OUT / "filas_alineadas.csv")
kh = pd.read_csv(RAIZ / "data/external/open-khipu-repository/data/okr-kh-numbers.csv").set_index("OKR Number")
con = sqlite3.connect(RAIZ / "data/external/open-khipu-repository/data/khipu.db")
km = pd.read_sql("select * from khipu_main", con)

# pares a verificar: (A, B, categoria, hipotesis)
LISTA = [
    ("UR1107", "UR237", "duplicado de base NO documentado (Berlín, dos números VA)", "mismo objeto"),
    ("KH0033", "UR044", "duplicado de base documentado (control)", "mismo objeto"),
    ("AS125", "UR247", "duplicado de base documentado (control)", "mismo objeto"),
    ("HP055", "UR1084", "copia entre museos (Lima / París)", "copia"),
    ("KH0049", "UR122", "copia/versión entre museos (Lima / Gotemburgo)", "copia"),
    ("MM008", "UR212", "copia fragmentaria entre museos (Basilea / Berlín)", "copia"),
    ("MM015", "UR212", "copia fragmentaria entre museos (Basilea / Berlín)", "copia"),
    ("MM016", "UR212", "copia fragmentaria entre museos (Basilea / Berlín)", "copia"),
    ("MM016", "UR1131", "copia fragmentaria entre museos (Basilea / Berlín)", "copia"),
    ("QU002", "UR137", "copia entre museos (Dallas / Miami)", "copia"),
    ("UR1175", "UR233", "copia/versión dentro de Berlín (misma colección, otro número VA)", "copia"),
    ("UR1175", "UR232", "copia/versión dentro de Berlín", "copia"),
    ("UR232", "UR233", "mismo número de inventario VA63038 asignado a ambos (A/B de Urton)", "verificar"),
    ("UR1118", "UR218", "copia dentro de Berlín", "copia"),
    ("UR1114", "UR1123", "copia dentro de Berlín (réplica de Urton 2005)", "copia"),
    ("AS159", "AS173", "copia dentro de Berlín (réplica de Urton 2005)", "copia"),
    ("UR255", "UR267A", "versión dentro de Incahuasi (nota OKR: 'match')", "versión"),
]


def info(k):
    d = C[C.kfg == k]
    okr = Q.loc[k, "okr"] if k in Q.index else None
    row = km[(km.INVESTIGATOR_NUM == k) | (km.OKR_NUM == okr)]
    r = row.iloc[0] if len(row) else None
    khn = okr if okr in kh.index else None
    if khn is None:
        for n in (k, ):
            for i, x in kh["Other Names"].dropna().items():
                if re.search(rf"\b{n}\b", x):
                    khn = i
    k_ = kh.loc[khn] if khn in kh.index else None
    return {
        "kfg": k, "KH": khn, "otros_nombres": k_["Other Names"] if k_ is not None else None,
        "museo": k_["Collection / Location"] if k_ is not None else Q.loc[k, "museo"],
        "ciudad": k_["City / State"] if k_ is not None else None,
        "n_inventario_okr_kh": k_["Collection Number"] if k_ is not None else None,
        "n_inventario_khipu_main": r.MUSEUM_NUM if r is not None else None,
        "procedencia": Q.loc[k, "procedencia"], "cordon_principal_cm": Q.loc[k, "pc_largo"], "cordon_principal_color": Q.loc[k, "pc_color"],
        "cuerdas_total": len(d), "colgantes": int((d.nivel == 0).sum()), "con_nudos": int(d.nudos.notna().sum()),
        "subsidiarias": int((d.nivel >= 1).sum()), "rotas_B_pct": round(100 * (d.terminacion == "B").mean(), 1),
        "nota_okr": (str(r.NOTES)[:200].replace("\n", " ") if r is not None and r.NOTES not in (None, "None") else None),
        "comentario_kh": (k_["Comments"] if k_ is not None and isinstance(k_["Comments"], str) else None),
    }


ks = sorted({k for a, b, *_ in LISTA for k in (a, b)})
O = pd.DataFrame([info(k) for k in ks])
O["discrepancia_n_inventario"] = O.apply(lambda r: (str(r.n_inventario_okr_kh).replace(" ", "").lower() != str(r.n_inventario_khipu_main).replace(" ", "").lower()) and pd.notna(r.n_inventario_khipu_main), axis=1)
O.to_csv(OUT / "verificacion_objetos.csv", index=False)


def lectura(r, lado):
    return f"{r['cuerda_' + lado]}={int(r['valor_' + lado])} [{r['nudos_' + lado]}] L{r['largo_' + lado]} {r['color_' + lado]} term {r['term_' + lado]}"


filas = []
for a, b, cat, hip in LISTA:
    p = R[((R.A == a) & (R.B == b)) | ((R.A == b) & (R.B == a))]
    g = F[((F.A == a) & (F.B == b))]
    o = {"A": a, "B": b, "categoria": cat, "hipotesis": hip}
    if len(p):
        p = p.iloc[0]
        o.update({"q_04": p.q_04, "cuerdas_alineadas": int(p.n_alineadas), "exactas": int(p.n_exacta), "solo_A": int(p.solo_A), "solo_B": int(p.solo_B),
                  "sentido": g.sentido.iloc[0], "largo_rho": round(p.largo_rho, 2) if p.largo_rho == p.largo_rho else None})
        dis = g[g.valor_A.notna() & g.valor_B.notna() & (g.clase != "exacta") & (g.nivel_A == 0) & (g.nivel_B == 0)]
        o["cuerdas_a_mirar"] = " || ".join(f"{lectura(r, 'A')} <> {lectura(r, 'B')}" for _, r in dis.head(8).iterrows())
        o["n_discordantes_colgantes"] = len(dis)
    else:
        o["cuerdas_a_mirar"] = "sin alineamiento significativo en 04: comprobar solo inventario"
    if hip == "mismo objeto":
        o["si_mismo_objeto_se_espera"] = "largos de cuerda iguales (±2 cm) uno a uno, mismo nº de cuerdas, mismas uniones R/V, mismos colores físicos y numeración invertida si sentido=inverso"
        o["si_copia_se_espera"] = "largos de cuerda no relacionados (rho<0,5), numeraciones/etiquetas históricas distintas"
    elif hip == "copia":
        o["si_mismo_objeto_se_espera"] = "largos coincidentes (r>=0,9, diferencia mediana <=2,5 cm); no se espera en estas parejas (04: r largo bajo)"
        o["si_copia_se_espera"] = "dos objetos distintos con la misma secuencia de valores: nudos físicamente distintos, largos y torsión distintos, y las diferencias de la lista 'cuerdas_a_mirar' son lecturas reales (nudo de más/menos), no errores de transcripción"
    else:
        o["si_mismo_objeto_se_espera"] = "una sola pieza con dos partes (A/B) o un mismo objeto desdoblado"
        o["si_copia_se_espera"] = "dos objetos con el mismo número de inventario"
    filas.append(o)
V = pd.DataFrame(filas)
V.to_csv(OUT / "verificacion_pares.csv", index=False)

# --- UR1107/UR237 cuerda a cuerda
g = F[(F.A == "UR1107") & (F.B == "UR237")][["cuerda_A", "cuerda_B", "clase", "valor_A", "valor_B", "nudos_A", "nudos_B", "largo_A", "largo_B", "color_A", "color_B", "union_A", "union_B", "term_A", "term_B", "torsion_A", "torsion_B"]].copy()
g["dif_largo_cm"] = (g.largo_B - g.largo_A).round(2)
g.to_csv(OUT / "verificacion_UR1107_UR237.csv", index=False)

# --- HP055/UR1084
h = F[(F.A == "HP055") & (F.B == "UR1084") & (F.clase != "exacta")][["cuerda_A", "cuerda_B", "clase", "valor_A", "valor_B", "nudos_A", "nudos_B", "largo_A", "largo_B", "color_A", "color_B", "term_A", "term_B", "vacias_otro_lado"]]
h.to_csv(OUT / "verificacion_HP055_UR1084.csv", index=False)

pd.set_option("display.width", 250, "display.max_colwidth", 70, "display.max_columns", 30)
print(O[["kfg", "KH", "museo", "n_inventario_okr_kh", "n_inventario_khipu_main", "discrepancia_n_inventario", "cuerdas_total", "con_nudos", "cordon_principal_cm", "rotas_B_pct"]].to_string(index=False))
print()
print(V[["A", "B", "categoria", "cuerdas_alineadas", "exactas", "solo_A", "solo_B", "sentido", "largo_rho", "n_discordantes_colgantes"]].to_string(index=False))
print()
print(g.to_string(index=False))
