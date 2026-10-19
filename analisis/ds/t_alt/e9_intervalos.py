"""Analisis de sensibilidad por INTERVALOS: para cada racimo, la lectura transcrita
y las lecturas alternativas plausibles que recoge la literatura
(Ascher 'tipo por posicion' vs Urton 'tipo por nudo'; Thompson 2025 documenta
20S que era 20L, 3L->4L, cuerdas rotas no codificadas).

Reglas alternativas (explicitas):
  A1. Un nudo L/E/raro que NO es el ultimo racimo (tiene algo debajo) se lee en
      Ascher por su POSICION: aporte = n * 10^(niveles por debajo).  (Urton: unidades)
  A2. Un nudo S con aporte que no es n*10^k se lee como n en unidades.
  A3. Un racimo sin aporte aporta 0 o, alternativamente, n*10^(lugar).
  A4. Nudo ausente/roto: no genera alternativa (no hay dato) -> se trata aparte.

Se calcula el intervalo [min,max] del valor de cada cuerda y se propaga a sumas.
"""
import re
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
R = re.compile(r"^(\d+)([A-Za-z]+)\(([\d.]+),([A-Z])\)(?:,(-?\d+))?$")

rec = []
for i, s in zip(d.index, d.nudos):
    if not s:
        continue
    for j, k in enumerate(s.split(";")):
        m = R.match(k)
        if not m:
            rec.append(dict(i=i, j=j, n=np.nan, tipo="?", ap=np.nan)); continue
        rec.append(dict(i=i, j=j, n=float(m.group(1)), tipo=m.group(2),
                        ap=float(m.group(5)) if m.group(5) is not None else np.nan))
c = pd.DataFrame(rec)
c["m"] = c.groupby("i").j.transform("max") + 1
c["desde_abajo"] = c.m - 1 - c.j          # 0 = ultimo racimo (unidades)
c["ap0"] = c.ap.fillna(0)

def niveles(r):
    if r.tipo == "S" and r.n > 0 and r.ap > 0:
        x = np.log10(r.ap / r.n)
        if abs(x - round(x)) < 1e-9:
            return int(round(x))
    return None
c["niv"] = c.apply(niveles, axis=1)

# --- aporte alternativo por racimo (maximo de las alternativas plausibles)
alt = c.ap0.copy()
a1 = (~c.tipo.isin(["S"])) & (c.desde_abajo > 0) & (c.ap.notna())
alt[a1] = c.n[a1] * 10 ** c.desde_abajo[a1]
a2 = (c.tipo == "S") & c.ap.notna() & c.niv.isna()
alt[a2] = c.n[a2]
a3 = c.ap.isna() & c.n.notna()
alt[a3] = c.n[a3] * 10 ** c.desde_abajo[a3]
c["alt"] = alt
c["d"] = c.alt - c.ap0

c["lo"] = np.minimum(c.ap0, c.alt)
c["hi"] = np.maximum(c.ap0, c.alt)
V = c.groupby("i").agg(v0=("ap0", "sum"), vmin=("lo", "sum"), vmax=("hi", "sum"),
                       n_amb=("d", lambda s: (s != 0).sum()),
                       dmax=("d", lambda s: s.abs().max()))
V["ancho"] = V.vmax - V.v0
V["rel"] = V.ancho / V.v0.replace(0, np.nan)
V = V.join(d[["kfg", "cuerda", "nivel"]], how="left")
print("cuerdas con nudos:", len(V))
print("cuerdas con >=1 racimo con lectura alternativa:", (V.n_amb > 0).sum(),
      f"({100*(V.n_amb>0).mean():.2f}%)")
print("cuerdas cuyo valor CAMBIA con la alternativa:", (V.ancho != 0).sum(),
      f"({100*(V.ancho!=0).mean():.2f}%)")
print("\nrel = ancho/valor (solo las que cambian):")
print(V.rel[V.ancho != 0].describe(percentiles=[.25,.5,.75,.9,.99]).round(3).to_string())
print("\npor tipo de racimo afectado (conteo de racimos con d!=0):")
print(c[c.d != 0].tipo.value_counts().to_string())
print("\ncuerdas afectadas por quipu:", V[V.ancho != 0].groupby("kfg").size().describe().round(2).to_dict())
V.to_csv(AQUI/"intervalos_cuerdas.csv", index=False)
c.to_csv(AQUI/"racimos_alt.csv", index=False)
