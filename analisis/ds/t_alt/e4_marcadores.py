"""Marcadores internos de ambiguedad en `nudos`: direccion U, aportes ausentes,
tipos raros, niveles decimales inconsistentes y 'racimos rotos' (notas / cadenas mal formadas).
"""
import re
from pathlib import Path
import pandas as pd, numpy as np

RAIZ = Path(__file__).resolve().parents[3]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
R = re.compile(r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Z])\)(?:,(-?\d+))?$")
EST = {"S", "L", "E"}

rec = []
for i, s in zip(d.index, d.nudos):
    if not s:
        continue
    for j, k in enumerate(s.split(";")):
        m = R.match(k)
        if not m:
            rec.append((i, j, k, np.nan, "?", "?", np.nan))
        else:
            rec.append((i, j, k, int(m.group(1)), m.group(2), m.group(4),
                        float(m.group(5)) if m.group(5) is not None else np.nan))
c = pd.DataFrame(rec, columns=["i", "j", "raw", "n", "tipo", "dir", "ap"])
c = c.join(d[["kfg", "cuerda", "valor"]], on="i")
c["v"] = pd.to_numeric(c.valor, errors="coerce").fillna(0)
c["fuente"] = c.kfg.str.extract(r"^([A-Z]+)")[0]

print("racimos:", len(c), " cuerdas con nudos:", c.i.nunique(), " quipus:", c.kfg.nunique())
print("\n== 1. direccion U ==")
print("racimos U:", (c.dir == "U").sum(), f"({100*(c.dir=='U').mean():.2f}%)")
por = c.groupby("fuente")["dir"].apply(lambda s: (s == "U").mean()).sort_values(ascending=False)
print((100*por).round(1).head(12).to_string())
u_c = c.groupby("i")["dir"].apply(lambda s: (s == "U").mean())
print("\ncuerdas con >=1 racimo U:", (u_c > 0).sum(), f"({100*(u_c>0).mean():.2f}%)")
print("cuerdas 100% U:", (u_c == 1).sum(), f"({100*(u_c==1).mean():.2f}%)")
print("de las 100% U, cuerdas con valor>0:", (u_c[u_c == 1].index.isin(c[c.v > 0].i)).sum())

print("\n== 2. aportes / parseo ==")
print("racimos sin aporte:", c.ap.isna().sum(), " no parseables:", (c.tipo == "?").sum())

print("\n== 3. tipos raros ==")
raros = ~c.tipo.isin(EST)
print("racimos:", raros.sum(), f"({100*raros.mean():.2f}%)  cuerdas afectadas:", c[raros].i.nunique(),
      f"quipus: {c[raros].kfg.nunique()}")
print(c[raros].tipo.value_counts().to_string())

print("\n== 4. niveles decimales ==")
def nivel(r):
    if r.tipo == "S" and r.n > 0 and r.ap > 0:
        x = np.log10(r.ap / r.n)
        if abs(x - round(x)) < 1e-9:
            return int(round(x))
        return 99          # S con aporte no decimal
    if r.tipo in EST or r.tipo in ("EE", "LL", "BL", "SP", "TF", "U"):
        return 0
    return np.nan
c["niv"] = c.apply(nivel, axis=1)
print("S con aporte no decimal (nivel 99):", (c.niv == 99).sum())
print("S con n>9:", ((c.tipo == "S") & (c.n > 9)).sum())
print("L con n==1 (indistinguible de S1):", ((c.tipo == "L") & (c.n == 1)).sum())
print("L con n>=10:", ((c.tipo == "L") & (c.n >= 10)).sum())

# orden de niveles arriba->abajo debe ser estrictamente decreciente
bad_ord = 0; dup = 0; cuerdas_bad = set()
for i, g in c[c.niv.notna()].groupby("i"):
    l = g.sort_values("j").niv.values
    for a in range(1, len(l)):
        if l[a] >= l[a-1]:
            bad_ord += 1; cuerdas_bad.add(i); break
    if len(set(l)) < len(l):
        dup += 1
print("\ncuerdas con niveles no decrecientes:", len(cuerdas_bad), f"({100*len(cuerdas_bad)/c.i.nunique():.2f}%)")
print("cuerdas con nivel decimal duplicado:", dup, f"({100*dup/c.i.nunique():.2f}%)")

print("\n== 5. notas con rotura ==")
pat = re.compile(r"brok|rot|falt|miss|fragm|incomplet|cut|desprend", re.I)
m = d.notas.fillna("") + " " + d.terminacion.fillna("")
sel = d[m.str.contains(pat)]
print("cuerdas con nota de rotura:", len(sel), f"({100*len(sel)/len(d):.2f}%)  quipus:", sel.kfg.nunique())
print(sel[["kfg", "cuerda", "notas"]].head(6).to_string(max_colwidth=60))
