# -*- coding: utf-8 -*-
"""UR262 (Incahuasi / Inkawasi, KH0498): preparacion de datos y estructura.

Lee analisis/datos/cuerdas.csv, limpia UR262 y deja:
  ur262_cuerdas.csv   (una fila por cuerda, lista para analisis)
  ur262_estructura.txt (volcado jerarquico para inspeccion humana)
No modifica nada fuera de analisis/ds/k_UR262/.
"""
import os
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATOS = os.path.join(ROOT, "analisis", "datos")
OUT = os.path.dirname(os.path.abspath(__file__))
KFG = "UR262"

q = pd.read_csv(os.path.join(DATOS, "cuerdas.csv"), dtype=str, keep_default_na=False)
q = q[q["kfg"] == KFG].copy()

for c in ["orden", "nivel", "grupo"]:
    q[c] = pd.to_numeric(q[c], errors="coerce")
for c in ["valor", "largo"]:
    q[c] = pd.to_numeric(q[c].replace("", None), errors="coerce")

q["sin_nudos"] = q["nudos"] == ""
q["tiene_nudos"] = ~q["sin_nudos"]
q = q.sort_values("orden").reset_index(drop=True)

# nudo inferior (L/E con racimo debajo): ultimo racimo es L o E
def ultimo_tipo(nudos):
    if not nudos:
        return ""
    ult = nudos.split(";")[-1]
    return ult.split("(")[0][-1] if "(" in ult else ""

q["ult_tipo"] = q["nudos"].apply(ultimo_tipo)
q.to_csv(os.path.join(OUT, "ur262_cuerdas.csv"), index=False)

# --- volcado jerarquico ---
lines = []
cur_g = None
for _, r in q.iterrows():
    if r["nivel"] == 0:
        if r["grupo"] != cur_g:
            cur_g = r["grupo"]
            lines.append("")
            lines.append(f"== GRUPO {int(cur_g)} ==")
        lines.append(
            f"{r['cuerda']:>7} v={r['valor']:>7.0f} col={r['color']:<7} u={r['union']} "
            f"L={r['largo']:>5.1f} nudos={r['nudos'] if r['nudos'] else '-'}"
        )
    else:
        ind = "  " * int(r["nivel"])
        lines.append(
            f"{ind}{r['cuerda']:>7} v={r['valor']:>7.0f} col={r['color']:<7} u={r['union']} "
            f"L={r['largo']:>5.1f} nudos={r['nudos'] if r['nudos'] else '-'}"
        )
open(os.path.join(OUT, "ur262_estructura.txt"), "w", encoding="utf-8").write("\n".join(lines))

# --- resumen en consola (<=40 lineas) ---
print("cuerdas:", len(q), "| pendientes:", (q.nivel == 0).sum(), "| subsidiarias:", (q.nivel > 0).sum())
print("profundidad maxima:", int(q.nivel.max()), "| grupos:", q.grupo.nunique())
print("sin nudos:", int(q.sin_nudos.sum()), f"({100*q.sin_nudos.mean():.1f}%)")
print("union:", q.union.value_counts().to_dict(), "| torsion:", q.torsion.value_counts().to_dict())
print("colores distintos:", q.color.nunique(), "| top:", q.color.value_counts().head(6).to_dict())
print("largo: min %.1f mediana %.1f max %.1f" % (q.largo.min(), q.largo.median(), q.largo.max()))
print("valor pendientes: suma %.0f mediana %.0f max %.0f" % (
    q.loc[q.nivel == 0, "valor"].sum(), q.loc[q.nivel == 0, "valor"].median(),
    q.loc[q.nivel == 0, "valor"].max()))
print("sin nudos por nivel:", q.groupby("nivel").sin_nudos.sum().to_dict())
print("sin nudos por grupo:", q[q.sin_nudos].grupo.value_counts().sort_index().to_dict())
