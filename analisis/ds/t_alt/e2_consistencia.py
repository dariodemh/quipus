"""Consistencia interna: valor declarado vs suma de aportes de los racimos.
Localiza los 'valores dudosos' y clasifica su causa.
"""
import re
from pathlib import Path
import pandas as pd, numpy as np

RAIZ = Path(__file__).resolve().parents[3]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
R = re.compile(r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Z])\)(?:,(-?\d+))?$")

rec = []
for i, s in zip(d.index, d.nudos):
    if not s:
        continue
    tot = 0.0; falta = False; malos = 0
    for k in s.split(";"):
        m = R.match(k)
        if not m or m.group(5) is None:
            falta = True; malos += 1; continue
        tot += float(m.group(5))
    rec.append((i, tot, falta, malos))
S = pd.DataFrame(rec, columns=["i", "sumap", "falta", "malos"]).set_index("i")
d = d.join(S)
d["v"] = pd.to_numeric(d.valor, errors="coerce")
sub = d[d.has_nudos if "has_nudos" in d else d.nudos != ""]
sub = d[d.nudos != ""]
ok = sub.dropna(subset=["v", "sumap"])
ok = ok[ok.falta == False]
dif = ok.v - ok.sumap
print("cuerdas con nudos y valor numerico:", len(ok))
print("coinciden exacto:", (dif == 0).sum(), f"({100*(dif==0).mean():.2f}%)")
print("discrepan:", (dif != 0).sum(), f"({100*(dif!=0).mean():.2f}%)")
print("\n-- magnitud de la discrepancia --")
print(dif[dif != 0].abs().describe().to_string())
print("\n-- ejemplos (20) --")
print(ok[dif != 0][["kfg", "cuerda", "valor", "sumap", "nudos"]].head(20).to_string(max_colwidth=45))
print("\n-- cuerdas con nudos sin valor numerico:", (sub.v.isna()).sum())
print(sub[sub.v.isna()][["kfg", "cuerda", "valor", "nudos"]].head(6).to_string(max_colwidth=40))
print("\n-- racimos no parseables (raw) --")
for i in d.index[d.nudos.str.contains(r"\(\d", regex=True) & (d.malos.fillna(0) > 0)][:6]:
    print(" ", d.loc[i, "kfg"], d.loc[i, "cuerda"], repr(d.loc[i, "nudos"])[:90])
