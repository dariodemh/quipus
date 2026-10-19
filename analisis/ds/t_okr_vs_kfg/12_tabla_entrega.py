# -*- coding: utf-8 -*-
"""Genera la tabla de entrega (>5%) con causa y las correcciones de metadatos."""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")

MAL = {"KH0197": "KH0198", "KH0227": "KH0228", "KH0267": "KH0268", "KH0350": "KH0351"}
DUP = {"UR196", "MM007_AN002"}

h = pd.read_csv(os.path.join(SAL, "por_quipu.csv"), index_col=0)
g = pd.read_csv(os.path.join(SAL, "por_quipu_final.csv"), index_col=0)
j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))

mult = {}
for k, x in j[j.dlargo <= 0.51].groupby("kfg"):
    if len(x) >= 5:
        mult[k] = bool(sorted(x.valor.fillna(0)) == sorted(x.valor_okr.fillna(0)))

NOTAS = {
    "UR193": "OKR multi-raiz (PENDANT_FROM colgante); 134 cuerdas con largo distinto. Mezcla/estructura + valor.",
    "AS072": "KFG reordena las cuerdas (mismo n de cuerdas, largos en otro orden).",
    "HP009": "KFG incompleto: 13 cuerdas frente a 20 en OKR; largos 0-2 cm con nudos a 15-20 cm.",
    "UR144": "Valor: vueltas de nudos largos (KFG 7L donde OKR tiene 4L). 56 cuerdas.",
    "UR090": "Valor: lugar decimal (OKR asigna 100 donde KFG asigna 10). 67 cuerdas.",
    "HP024": "Solo orden: multiset de valores identico.",
    "UR190": "OKR multi-raiz; 253 cuerdas con largo distinto. Estructura + 14 valores.",
    "HP004": "Solo orden de subsidiarias: multiset de valores identico.",
    "HP045": "Solo orden: multiset de valores identico.",
    "HP006": "Solo orden: multiset de valores identico.",
    "HP023": "Orden + 1 discrepancia de valor.",
    "UR096": "Solo orden: multiset de valores identico.",
    "HP047": "Solo orden: multiset de valores identico.",
    "KH0058": "Registro KH de AS047/HP035; mezcla de orden y valor. Revisar antes de usar.",
    "UR235": "Valor: lugar decimal (OKR 100 donde KFG 10). 36 cuerdas.",
    "HP054": "Valor: 3 cuerdas con nudos en KFG y otra lectura en OKR.",
    "UR003": "OKR multi-raiz (8 cuerdas huerfanas); 52 largos distintos; 3 valores.",
    "UR044": "Duplicado con KH0033; 13 largos distintos y 1 valor. 33 cuerdas solo en OKR.",
    "KH0033": "Duplicado de UR044; codifica largos ausentes como 0 (infla el desajuste).",
    "UR255": "1 discrepancia de valor.",
    "HP038": "Valor: KFG registra nudos que OKR no tiene (4 cuerdas).",
    "UR253": "Solo orden: multiset de valores identico.",
    "UR280": "1 discrepancia de valor.",
}

lista = h[(h.tasa > 0.05) & (~h.index.isin(MAL) & ~h.index.isin(DUP))].copy()
lista["disc_valor"] = g.disc_valor.reindex(lista.index).fillna(0).astype(int)
lista["n_valor"] = g.n_valor.reindex(lista.index).fillna(0).astype(int)
lista["tasa_valor"] = (lista.disc_valor / lista.n_valor.replace(0, np.nan)).round(3)
lista["n_estruct"] = g.n_estruct.reindex(lista.index).fillna(0).astype(int)
lista["multiset_igual"] = lista.index.map(mult)
lista["frac_est"] = lista.n_estruct / lista.n_con_nudos.replace(0, np.nan)
def causa(r):
    if r.tasa_valor >= 0.05:
        return "mixto" if r.frac_est >= 0.2 else "valor"
    if r.multiset_igual is True:
        return "orden/mapeo"
    return "estructura"
lista["causa"] = [causa(r) for r in lista.itertuples()]
lista["nota"] = [NOTAS.get(k, "") for k in lista.index]
lista = lista.sort_values("tasa", ascending=False)
cols = ["prefijo", "n_con_nudos", "disc", "tasa", "disc_valor", "n_valor", "tasa_valor",
        "n_estruct", "multiset_igual", "causa", "nota"]
lista[cols].to_csv(os.path.join(SAL, "quipus_mas_5pct.csv"))
print(lista[cols].to_string())

print("\n=== metadatos KFG erroneos (off-by-one) ===")
corr = pd.DataFrame([(k, v, 1.0, 1.0) for k, v in MAL.items()],
                    columns=["kfg", "okr_correcto", "match_largos", "match_valores"])
print(corr.to_string(index=False))
corr.to_csv(os.path.join(SAL, "correcciones_kfg.csv"), index=False)

print("\nfilas:", len(lista), "| de ellas causa=valor:", (lista.causa == "valor").sum())
