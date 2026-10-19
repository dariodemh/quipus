# -*- coding: utf-8 -*-
"""Numeros finales para el informe: prevalencia esperada, aporte de los principales
quipus, repdigitos y consistencia de color (solo colores solidos)."""
import pandas as pd, numpy as np, os, re
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False).set_index("kfg")
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)
qids = sorted(k.kfg.unique()); qmap = {x: i for i, x in enumerate(qids)}
k["qi"] = k.kfg.map(qmap)
nq = len(qids)
n_i = k.groupby("qi").size().reindex(range(nq), fill_value=0).values
f = pd.Series(k.valor.values).value_counts()

print("=== prevalencia observada vs esperada si el valor se repartiera al azar ===")
print("valor  n  quipus_obs  quipus_esp  ratio")
for v in [1, 2, 3, 5, 10, 11, 12, 15, 20, 22, 30, 40, 47, 50, 100, 110, 200]:
    p = f[v] / len(k)
    esp = (1 - (1 - p) ** n_i).sum()
    obs = k.loc[k.valor == v, "kfg"].nunique()
    print(f"{v:>5} {f[v]:>5} {obs:>10} {esp:>10.0f} {obs/esp:>6.2f}")

print("\n=== aporte de los 3 quipus mayores a cada valor ===")
for v in [1, 10, 15, 47, 100, 200, 110, 22, 33]:
    cnt = k[k.valor == v].groupby("qi").size().sort_values(ascending=False)
    top = cnt.head(3).sum(); tot = cnt.sum()
    print(f"v={v:>4}: total={tot:>5} top3={top:>4} ({100*top/tot:.0f}%) | "
          + ", ".join(f"{qids[i]}:{c}" for i, c in cnt.head(3).items()))

print("\n=== repdigitos: frecuencia y razon frente al nulo de digitos (aprox. B2) ===")
T = pd.read_csv(OUT + r"\tabla_heaping_global.csv")
rep = [11, 22, 33, 44, 55, 66, 77, 88, 99, 111, 222, 333, 444, 555, 666, 777, 888, 999]
print(T[T.valor.isin(rep)][["valor", "n", "quipus", "ratio_B2", "qB2"]].sort_values("n", ascending=False)
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))

print("\n=== color: contribucion de los 3 quipus mayores (solo colores solidos) ===")
def color_prim(x):
    if not isinstance(x, str): return None
    return re.split(r"[\(:/,\-]", x.strip())[0].strip()
k["col"] = k.color.map(color_prim)
k["solido"] = k.color.map(lambda x: isinstance(x, str) and not re.search(r"[\(:/,\-]", x))
for v, col in [(1, "B"), (3, "B"), (30, "KB"), (47, "YB")]:
    for solid in [False, True]:
        kk = k[k.solido] if solid else k
        nn = kk.groupby("qi").size().reindex(range(nq), fill_value=0).values.astype(float)
        nv = kk[kk.valor == v].groupby("qi").size().reindex(range(nq), fill_value=0).values.astype(float)
        nc = kk[kk.col == col].groupby("qi").size().reindex(range(nq), fill_value=0).values.astype(float)
        safe = np.where(nn > 0, nn, 1)
        pi = np.where(nn > 0, nv / safe, 0)
        obs = int(((kk.valor == v) & (kk.col == col)).sum())
        exp = float((nc * pi).sum())
        dev = nc * pi - nc * pi  # placeholder
        # desviacion por quipu: obs_i - nc_i*pi_i
        oi = np.array([((kk.qi == i) & (kk.valor == v) & (kk.col == col)).sum() for i in range(nq)])
        di = oi - nc * pi
        share = np.sort(np.abs(di))[::-1][:3].sum() / np.abs(di).sum() if np.abs(di).sum() > 0 else np.nan
        if not solid:
            print(f" v={v} {col}: TODOS obs={obs} esp={exp:.0f} ratio={obs/exp:.2f} | top3 aportan {100*share:.0f}% de |desv|")
        else:
            print(f" v={v} {col}: SOLIDOS obs={obs} esp={exp:.0f} ratio={obs/exp if exp else float('nan'):.2f}")

print("\n=== cuantos quipus son 'especialistas' en al menos un valor ===")
C = pd.read_csv(OUT + r"\tabla_concentracion.csv")
print("(no calculado por quipu; ver HHI medio observado vs nulo en 08_chequeos.py)")
print("\n=== 222: en que quipus ===")
m = k[k.valor == 222]
print("total:", len(m), "quipus:", m.kfg.nunique(), "| top:", m.kfg.value_counts().head(6).to_dict())
