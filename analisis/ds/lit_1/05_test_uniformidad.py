# -*- coding: utf-8 -*-
"""V4: uniformidad de torsión y dirección de nudo (Ascher 2005).
Contraste con: spin/ply uniformes salvo 3 quipus; ~81% de quipus con dirección de nudo uniforme.
"""
import pandas as pd, numpy as np, re, os
RNG = np.random.default_rng(20261017)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
D["nivel"] = pd.to_numeric(D["nivel"], errors="coerce")

print("=== V4a. Torsión (spin) por quipu ===")
t = D[D.torsion.isin(["S", "Z"])]
g = t.groupby("kfg").torsion
n = g.size(); nu = g.nunique()
print("quipus con torsión S/Z:", len(n), "| uniformes:", int((nu == 1).sum()),
      f"({100*(nu==1).mean():.1f}%)", "| mixtos:", int((nu > 1).sum()))
print("distribución nº de valores por quipu:", nu.value_counts().sort_index().to_dict())
print("global S/Z:", t.torsion.value_counts().to_dict())
pZ = (t.torsion == "Z").mean()
exp = sum(pZ**k + (1 - pZ)**k for k in n)
print(f"nulo (etiquetas independientes, p(Z)={pZ:.3f}): quipus uniformes esperados={exp:.2f}")
# restringir a quipus con >=5 cuerdas con torsión (evita que n=1 sea trivialmente uniforme)
m5 = n >= 5
exp5 = sum(pZ**k + (1 - pZ)**k for k in n[m5])
print(f"quipus con >=5 cuerdas con torsión: {int(m5.sum())}, uniformes={int((nu[m5]==1).sum())} "
      f"({100*(nu[m5]==1).mean():.1f}%), esperado nulo={exp5:.2f}")
# ¿los mixtos son quipus grandes?
mix = nu[nu > 1].index
print("tamaño medio (cuerdas) uniformes vs mixtos:",
      round(n[nu == 1].mean(), 1), "vs", round(n[nu > 1].mean(), 1))
print("torsión del cordón principal no está en quipus.csv (sólo color/largo/estructura)")

print("\n=== V4b. Dirección de nudo por quipu (S/Z en la cadena de nudos) ===")
def dirs(s):
    if not isinstance(s, str):
        return []
    return [m.group(2) for m in re.finditer(r"\(([-0-9.]+),([SZU])\)", s)]
per = {}
for k, s in zip(D.kfg, D.nudos):
    ds = [x for x in dirs(s) if x in "SZ"]
    if ds:
        per.setdefault(k, []).extend(ds)
per = {k: v for k, v in per.items()}
uni = {k: len(set(v)) == 1 for k, v in per.items()}
print("quipus con >=1 nudo S/Z:", len(per), "| uniformes:", sum(uni.values()),
      f"({100*sum(uni.values())/len(per):.1f}%)", "| mixtos:", len(per) - sum(uni.values()))
print("global S/Z en nudos:", pd.Series([x for v in per.values() for x in v]).value_counts().to_dict())
# fracción mayoritaria
frac = np.array([max(v.count("S"), v.count("Z")) / len(v) for v in per.values()])
for th in [0.8, 0.9, 0.95, 1.0]:
    print(f"quipus con >= {int(th*100)}% de nudos en una sola dirección: {int((frac >= th).sum())} ({100*(frac>=th).mean():.1f}%)")
print("mediana de la fracción mayoritaria:", round(float(np.median(frac)), 3))

# por cuerda
cu = []
for k, s in zip(D.kfg, D.nudos):
    ds = [x for x in dirs(s) if x in "SZ"]
    if ds:
        cu.append(len(set(ds)) == 1)
print("cuerdas con nudos S/Z:", len(cu), "uniformes por cuerda:", sum(cu), f"({100*np.mean(cu):.1f}%)")

print("\n=== V4c. ¿La mixtura depende del tamaño? ===")
sz = D[D.nivel == 0].groupby("kfg").size()
df = pd.DataFrame({"mix": [not uni[k] for k in per], "np": [sz.get(k, 0) for k in per]})
print(df.groupby("mix").np.agg(["size", "mean", "median"]).round(1).to_string())

# nulo: si las direcciones se asignaran al azar con la p global, ¿cuántos quipus uniformes?
pZ2 = 33908 / (33908 + 22015)
print(f"nulo aproximado con p(Z)={pZ2:.3f}: uniformes esperados < 0.01% de los quipus")

print("\nresumen:", dict(tors_quipus=len(n), tors_unif=int((nu==1).sum()),
                         dir_quipus=len(per), dir_unif=int(sum(uni.values())),
                         dir_unif_pct=round(100*sum(uni.values())/len(per), 1)))
