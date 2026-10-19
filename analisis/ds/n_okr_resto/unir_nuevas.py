"""Une las cuerdas nuevas (KH0674, KH0675, KH0676) en cuerdas_nuevas.csv y comprueba
que no duplican quipus ya presentes en analisis/datos/cuerdas.csv.
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

partes = []
for kh in ("KH0674", "KH0675", "KH0676"):
    d = pd.read_csv(os.path.join(HERE, "cuerdas_%s.csv" % kh), dtype={"cuerda": str})
    d["notas"] = ("fuente: transcripcion visual %s; " % kh) + d["notas"].fillna("")
    d["notas"] = d["notas"].str.rstrip("; ")
    partes.append(d)
out = pd.concat(partes, ignore_index=True)
out.to_csv(os.path.join(HERE, "cuerdas_nuevas.csv"), index=False, encoding="utf-8")
print("cuerdas_nuevas", out.shape)
print(out.groupby("kfg").agg(cuerdas=("cuerda", "size"), colgantes=("nivel", lambda s: (s == 0).sum()),
                             valor=("valor", "sum")).to_string())
viejo = pd.read_csv(os.path.join(RAIZ, "analisis", "datos", "cuerdas.csv"), usecols=["kfg"])
print("KH ya en cuerdas.csv:", sorted(set(out.kfg) & set(viejo.kfg)))
print(out.groupby("kfg").valor.describe().to_string())
