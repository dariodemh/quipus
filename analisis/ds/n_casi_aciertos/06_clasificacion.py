# -*- coding: utf-8 -*-
"""Cierre: clasificacion caso a caso, nulo agregado y tablas del informe.

Salidas:
  reparaciones.csv          (entrega: una fila por candidata, con clase)
  resumen_relaciones.csv    (una fila por casi-acierto)
  resumen_familias.csv
  salida_06.txt
"""
import os
import pandas as pd
import numpy as np
from scipy.stats import binom

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")

D = pd.read_csv(os.path.join(OUT, "reparaciones.csv"))
S = pd.read_csv(os.path.join(OUT, "reparaciones_resumen.csv"))
RC = pd.read_csv(os.path.join(OUT, "relacion_cuerdas.csv"))
Q = pd.read_csv(os.path.join(OUT, "nulo_ediciones.csv"))

# ---------- resolucion conjunta ----------
res_de = (S.familia + ":" + S.quipu + ":" + S.relacion).to_frame("rel")
res_de["residual"] = S.residual.values
res_de = res_de.set_index("rel").residual.to_dict()
RC["residual"] = RC.relacion.map(res_de)
joint = []
for _, c in D.iterrows():
    rels = RC[(RC.quipu == c.quipu_cuerda) & (RC.cuerda == c.cuerda)]
    n = sum(((rr.lado == "detalle") and abs(rr.residual - c.delta_aplicado) < 1e-9) or
            ((rr.lado == "libro") and abs(rr.residual + c.delta_aplicado) < 1e-9)
            for _, rr in rels.iterrows() if not pd.isna(rr.residual))
    joint.append(int(n))
D["relaciones_que_resuelve"] = joint

# ---------- p_nulo por relacion ----------
def q_any(delta, nrac=2):
    x = Q[(Q.delta == delta) & (Q.n_racimos == nrac)]
    return float(x.q_any.iloc[0]) if len(x) else 0.0

pn = []
for _, r in S.iterrows():
    if pd.isna(r.residual):
        pn.append(np.nan); continue
    k = len([x for x in str(r.cuerdas).split(";") if ":" in x])
    pn.append(1 - (1 - q_any(r.residual)) ** max(k, 1))
S["p_nulo_relacion"] = pn

# ---------- clasificacion (reglas + overrides por caso) ----------
OVR = {
    ("R1_ur278_fila", "g4"): "discrepancia_real_o_compuesta",
    ("R1_ur278_fila", "g8"): "error_de_lectura_plausible",
    ("R1_ur278_fila", "g12"): "discrepancia_entre_copias",
    ("R1_ur278_fila", "g13"): "ambiguo",
    ("R1_ur278_fila", "g17"): "ambiguo",
    ("R1_ur278_fila", "g19"): "ambiguo",
    ("R1_ur278_fila", "g21"): "error_de_lectura_plausible",
    ("R2_ur278_celda", "g21c1~UR270g0"): "error_de_lectura_plausible",
    ("R2_ur278_celda", "g25c1~UR270g4"): "sistematico",
    ("R2_ur278_celda", "g27c1~UR270g8"): "error_de_lectura_plausible",
    ("R2_ur278_celda", "g27c2~UR270g8"): "ambiguo",
    ("R2_ur278_celda", "g27c4~UR270g8"): "discrepancia_real_o_compuesta",
    ("R2_ur278_celda", "g28c6~UR270g9"): "discrepancia_real_o_compuesta",
    ("R2_ur278_celda", "g28c7~UR270g9"): "ambiguo",
    ("R2_ur278_celda", "g28c9~UR270g9"): "ambiguo",
    ("R3_ur273ab", "reg0"): "error_de_lectura_plausible",
    ("R3_ur273ab", "reg4"): "ambiguo",
    ("R3_ur273ab", "reg13"): "error_de_lectura_plausible",
    ("R3_ur273ab", "reg18"): "ambiguo",
    ("R3_ur273ab", "reg19"): "ambiguo",
    ("R3_ur273ab", "reg20"): "error_de_lectura_plausible",
    ("R3_ur273ab", "reg21"): "ambiguo",
    ("R4_ur274a_273b", "reg3"): "ambiguo",
    ("R4_ur274a_273b", "reg4"): "ambiguo",
    ("R4_ur274a_273b", "reg14"): "ambiguo",
    ("R4_ur274a_273b", "reg19"): "ambiguo",
    ("R5_cuota", "p51"): "error_de_lectura_plausible",
    ("R5_cuota", "p9"): "sistematico",
    ("R5_cuota", "p13"): "sistematico",
    ("R5_cuota", "p19"): "sistematico",
    ("R5_cuota", "p64"): "sistematico",
    ("R5_cuota", "p88"): "ambiguo",
    ("R5_cuota", "p100"): "ambiguo",
    ("R5_cuota", "p94"): "ambiguo",
    ("R5_cuota", "p86"): "discrepancia_real_o_compuesta",
}
S["clase"] = [OVR.get((f, r), "sin_destino" if pd.isna(res) else "ambiguo")
              for f, r, res in zip(S.familia, S.relacion, S.residual)]

# ---------- nulo agregado ----------
val = S[S.residual.notna()]
obs = int((val.n_ediciones > 0).sum())
exp = float(val.p_nulo_relacion.fillna(0).sum())
pbar = float(val.p_nulo_relacion.fillna(0).mean())
pval = binom.sf(obs - 1, len(val), pbar)

# ---------- mejores candidatas ----------
PESO = {"vueltas": 1.0, "conteo_simple": 1.0, "factor10": 0.9, "ocho_vs_largo": 0.7,
        "S_vs_L": 0.6, "racimo_omitido": 0.5, "racimo_duplicado": 0.3, "insercion": 0.25}
D["peso"] = D.tipo_error.map(PESO)
D["nrac"] = D.nudos_actual.fillna("").str.count(";") + 1
med = D.groupby("relacion").nrac.transform("median")
D["plantilla_corta"] = D.nrac < med
D["score"] = (3 * D.relaciones_que_resuelve + 2 * D.peso + 0.2 * (D.lado == "detalle")
              + 1.0 * D.plantilla_corta)
D = D.sort_values(["score", "probabilidad"], ascending=False)
D["recomendada"] = False
D.loc[D.groupby("relacion").head(1).index, "recomendada"] = True
# en las cuotas, la plantilla de las cuerdas hermanas es un largo de 7 vueltas, no 7 simples
D.loc[D.familia == "R5_cuota", "recomendada"] = False
m = (D.familia == "R5_cuota") & D.descripcion.str.contains("nudo largo", na=False)
D.loc[D[m].groupby("relacion").head(1).index, "recomendada"] = True
faltan = set(D.relacion) - set(D[D.recomendada].relacion)
for rel in faltan:
    D.loc[D[D.relacion == rel].index[0], "recomendada"] = True
best = D[D.recomendada]
S2 = S.copy()
S2["rel_id"] = S2.familia + ":" + S2.quipu + ":" + S2.relacion
S2 = S2.merge(best[["relacion", "cuerda", "lado", "tipo_error", "descripcion",
                    "delta_aplicado", "relaciones_que_resuelve"]],
              left_on="rel_id", right_on="relacion", how="left", suffixes=("", "_b"))
S2.to_csv(os.path.join(OUT, "resumen_relaciones.csv"), index=False)

# entrega final
D["clase"] = D.relacion.map(S2.set_index("rel_id").clase)
cols = ["relacion", "familia", "quipu_cuerda", "cuerda", "lado", "residual", "delta_aplicado",
        "nudos_actual", "nudos_propuesto", "tipo_error", "descripcion", "probabilidad",
        "p_nulo", "n_candidatos_cuerda", "relaciones_que_resuelve", "recomendada", "clase"]
D[cols].to_csv(os.path.join(OUT, "reparaciones.csv"), index=False)

fam = S2.groupby("familia").agg(n=("relacion", "size"), con_destino=("residual", lambda s: s.notna().sum()),
                                reparables=("n_ediciones", lambda s: (s > 0).sum()),
                                candidatas_medianas=("n_ediciones", "median"))
fam.to_csv(os.path.join(OUT, "resumen_familias.csv"))

print("=== NULO AGREGADO ===")
print(f"relaciones con destino: {len(val)} | reparables con 1 edicion: {obs} | esperadas: {exp:.2f} (exceso {obs-exp:+.2f})")
print(f"p binomial aproximado = {pval:.4f} (pbar={pbar:.3f}); no corrige dependencia entre relaciones")
print()
print(fam.to_string())
print()
print("=== CLASES ===")
print(S2.clase.value_counts().to_string())
print()
print("=== TABLA ===")
print(S2[["familia", "relacion", "residual", "n_ediciones", "clase", "cuerda", "lado",
          "tipo_error", "relaciones_que_resuelve"]].to_string(index=False))
