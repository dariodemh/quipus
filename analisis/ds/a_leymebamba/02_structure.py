# -*- coding: utf-8 -*-
"""02: estructura fina de UR001-UR022.
- ceros reales vs ausentes
- cuerdas superiores (union T) y si son sumas
- firma de grupos: tupla (#cuerdas por grupo)
- patrones de color por grupo
- familias de procedencia (Collection Number OKR)
Salida compacta a consola + estructura.csv / grupos_firma.csv
"""
import pandas as pd, numpy as np, os, re

RUTA = os.path.dirname(os.path.abspath(__file__))
ROOT = r"."
LE = ["UR%03d" % i for i in range(1, 23)]

c = pd.read_csv(os.path.join(ROOT, "analisis/datos/cuerdas.csv"))
q = pd.read_csv(os.path.join(ROOT, "analisis/datos/quipus.csv"))
g = pd.read_csv(os.path.join(ROOT, "analisis/datos/grupos.csv"))
c = c[c.kfg.isin(LE)].copy(); g = g[g.kfg.isin(LE)].copy()

c["sin_nudos"] = c.nudos.isna() | (c.nudos.astype(str).str.strip().isin(["", "nan"]))
c["valor_real"] = np.where(c.sin_nudos, np.nan, c.valor)

# --- ceros reales ---
z = c[(c.valor_real == 0) & (~c.sin_nudos)]
print("Ceros reales (valor 0 CON nudos):", len(z), "en", sorted(z.kfg.unique()))
print("  ejemplo nudos:", z.nudos.head(3).tolist())
print("Ausentes (valor 0 sin nudos):", int(c.sin_nudos.sum()))

# --- cuerdas superiores ---
t = c[c.union == "T"]
print("\nCuerdas superiores (union T):", len(t), "quipu(s):", sorted(t.kfg.unique()))
if len(t):
    print(t[["kfg", "cuerda", "nivel", "valor", "nudos", "largo"]].to_string(index=False))

# --- firma de grupos ---
firmas = {}
for kfg, sub in c.groupby("kfg"):
    sub = sub.sort_values("orden")
    col = sub[sub.nivel == 0]
    sizes = col.groupby("grupo").size().tolist()
    firmas[kfg] = sizes
F = pd.DataFrame({"kfg": list(firmas), "n_grupos": [len(v) for v in firmas.values()],
                  "firma": [",".join(map(str, v)) for v in firmas.values()]})
F.to_csv(os.path.join(RUTA, "grupos_firma.csv"), index=False)
print("\nFirma de grupos (tamano de cada grupo de colgantes):")
for _, r in F.sort_values("kfg").iterrows():
    print(f"  {r.kfg}: {r.firma}")

# --- duplicados de firma entre quipus ---
from collections import Counter
cnt = Counter(F.firma)
dup = {k: v for k, v in cnt.items() if v > 1 and k != "1"}
print("\nFirmas repetidas entre quipus:", dup)
for k in dup:
    print("   ", k, "->", F[F.firma == k].kfg.tolist())

# --- patrones de color de colgantes ---
for kfg, sub in c.groupby("kfg"):
    sub = sub[sub.nivel == 0].sort_values("orden")
    pass
# secuencia de color por quipu -> repetidos
sig_color = {}
for kfg, sub in c.groupby("kfg"):
    sub = sub[sub.nivel == 0].sort_values("orden")
    sig_color[kfg] = "|".join(sub.color.fillna("?").astype(str))
cc = Counter(sig_color.values())
print("\nSecuencias de color identicas:", {k: v for k, v in cc.items() if v > 1})

# --- familias de procedencia (Collection Number) ---
okr = pd.read_csv(os.path.join(ROOT, "data/external/open-khipu-repository/data/okr-kh-numbers.csv"))
okr = okr[okr["OKR Number"].isin(["KH%04d" % i for i in range(237, 259)])]
fam = {}
for _, r in okr.iterrows():
    cn = str(r["Collection Number"]).replace("\\r", " ").replace("\\n", " ").strip()
    cn = re.sub(r"[\s]+", " ", cn)
    fam[str(r["Other Names"]).strip()] = cn
print("\nFamilias (Collection Number OKR):")
for k in sorted(fam):
    print(f"  {k}: {fam[k]}")
