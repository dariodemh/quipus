"""Utilidades comunes de la verificacion (equipo 16). Solo usa analisis/datos/cuerdas.csv."""
import pandas as pd
import numpy as np

CSV = r"./analisis/datos/cuerdas.csv"
SEED = 16


def load():
    c = pd.read_csv(CSV, dtype=str, keep_default_na=False)
    c["orden"] = c["orden"].astype(int)
    c["nivel"] = c["nivel"].astype(int)
    c["valor_n"] = pd.to_numeric(c["valor"], errors="coerce")
    c["tiene_nudos"] = c["nudos"].str.len() > 0
    c["pk"] = c["color"].str.startswith("PK")
    return c


def registros(c, kfg, sep="A"):
    """Devuelve lista de registros (dicts) de un quipu.
    sep: 'A' separador = todas las cuerdas del grupo PK;
         'B' separador = primera cuerda del grupo (orden) empieza por PK;
         'C' separador = alguna cuerda del grupo empieza por PK.
    Registro = grupo de colgantes no separador, ordenado por 'orden'.
    cabecera = valor del primer colgante del grupo con nudos (NaN si ninguno).
    """
    q = c[(c.kfg == kfg) & (c.nivel == 0)].sort_values("orden")
    out = []
    for g, gg in q.groupby("grupo", sort=False):
        gg = gg.sort_values("orden")
        if sep == "A":
            is_sep = gg.pk.all()
        elif sep == "B":
            is_sep = bool(gg.pk.iloc[0])
        else:
            is_sep = gg.pk.any()
        if is_sep:
            continue
        con = gg[gg.tiene_nudos]
        cab = con.valor_n.iloc[0] if len(con) else np.nan
        out.append({"grupo": g, "n": len(gg), "cab": cab,
                    "orden0": gg.orden.iloc[0], "valores": gg.valor_n.tolist(),
                    "colores": gg.color.tolist(), "nombres": gg.cuerda.tolist()})
    return out


def cabeceras(c, kfg, sep="A"):
    return [r["cab"] for r in registros(c, kfg, sep)]
