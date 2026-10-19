"""T4. Clindaniel (2019, cap. 3): direccion de los nudos S/Z.

Afirmaciones:
  A) En Inkawasi dominan los nudos Z: 6209 Z vs 1704 S; los simple son
     1619 Z vs 19 S (p<0.0001); los largos/en ocho 402 S vs 835 Z.
  B) Si un cordel tiene un nudo largo en S, sus nudos simples son todos Z
     (1212 Z vs 0 S).
  C) El patron se replica en Pachacamac, Puruchuco y el resto del KDB,
     salvo Armatambo, donde predomina S.

Se cuenta cada nudo individual (no cada racimo) y se contrasta con el
nulo binomial, pero ademas se evalua la pseudorreplicacion: la unidad
del brief es el quipu. Se dan IC por bootstrap de quipus.
"""
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, contar_nudos, nudos_de, bootstrap_por_quipu, RNG

c, q, _ = cargar()
d = contar_nudos(c).merge(q[["kfg", "region", "museo", "procedencia"]],
                          on="kfg", how="left")
d["simple_n"] = d.simple_S + d.simple_Z
d["largo_n"] = d.largo_S + d.largo_Z


def grupo(nombre, mask):
    x = d[mask]
    s, z = x.simple_S.sum(), x.simple_Z.sum()
    sl, zl = x.largo_S.sum(), x.largo_Z.sum()
    p = stats.binomtest(int(z), int(s + z), 0.5).pvalue if s + z else np.nan
    print(f"{nombre:28s} khipus={len(x):3d} | simples S={s:6.0f} Z={z:6.0f} "
          f"(%Z={z/max(1,s+z):.3f}) bin.p={p:.1e} | largos S={sl:6.0f} Z={zl:6.0f}")


print("=== A/C. Direccion por procedencia (nudos simples) ===")
jc = d.kfg.str.startswith("JC")
# Muestra Inkawasi de Clindaniel: JC001-JC023 + UR255-UR280 (n=52)
ink = d.kfg.str.startswith("JC") | d.kfg.isin(
    ["UR255", "UR256", "UR257", "UR258", "UR259", "UR260", "UR261", "UR262",
     "UR263", "UR264", "UR265", "UR266", "UR267A", "UR267B", "UR268", "UR269",
     "UR270", "UR271", "UR272", "UR273", "UR274", "UR275", "UR276", "UR277",
     "UR278", "UR279", "UR280"])
pac = d.museo.astype(str).str.contains("Pachacamac")
pur = d.region.astype(str).str.contains("Puruchuco")
arm = d.procedencia.astype(str).str.contains("Armatambo")
cha = d.region.astype(str).str.contains("Chachapoyas")
grupo("Inkawasi (JC)", jc)
grupo("Inkawasi Clindaniel (52)", ink)
grupo("Pachacamac (museo)", pac)
grupo("Puruchuco (region)", pur)
grupo("Armatambo (todos)", arm)
grupo("Armatambo UR281-294", d.kfg.isin([f"UR{i}" for i in range(281, 295)]))
grupo("Chachapoyas", cha)
grupo("resto", ~(jc | pac | pur | arm | cha))

print("\nArmatambo, detalle por khipu (simples S/Z):")
print(d[arm][["kfg", "simple_S", "simple_Z"]].to_string(index=False))

print("\n=== Pseudorreplicacion: nudos vs quipus ===")
x = d[d.simple_n > 0]
allz = (x.simple_Z == x.simple_n).sum()
alls = (x.simple_S == x.simple_n).sum()
mix = len(x) - allz - alls
print(f"khipus con >=1 nudo simple: {len(x)} | todos Z: {allz} | todos S: {alls} | mixtos: {mix}")
print("proporcion de khipus puramente S:", round(alls / len(x), 3))

# Chi-cuadrado de homogeneidad entre quipus (¿la direccion depende del quipu?)
# y estadistico de conglomerado: fraccion de varianza explicada por quipu.
p_global = x.simple_Z.sum() / x.simple_n.sum()
print("p global (nudos):", round(p_global, 4))
print("IC binomial 95%:",
      [round(v, 4) for v in stats.binomtest(int(x.simple_Z.sum()),
                                            int(x.simple_n.sum())).proportion_ci(0.95)])

# Bootstrap por quipu de la proporcion agregada
B = 5000
vals = []
n = len(x)
z = x.simple_Z.to_numpy(float)
nn = x.simple_n.to_numpy(float)
for _ in range(B):
    idx = RNG.integers(0, n, n)
    vals.append(z[idx].sum() / nn[idx].sum())
lo, hi = np.percentile(vals, [2.5, 97.5])
print(f"IC 95% bootstrap por quipu: [{lo:.4f}, {hi:.4f}]")
se_bin = np.sqrt(p_global * (1 - p_global) / nn.sum())
se_clu = np.std(vals, ddof=1)
print(f"SE binomial={se_bin:.5f} | SE cluster={se_clu:.5f} | "
      f"deff={(se_clu/se_bin)**2:.1f}")

# Sign test a nivel de quipu entre los puramente S y puramente Z
print("Sign test khipus puros S vs puros Z:",
      stats.binomtest(int(allz), int(allz + alls), 0.5).pvalue)

print("\n=== B. Cordeles con nudo largo en S: direccion de sus nudos simples ===")
tot_s = tot_z = 0
cords = 0
jc_s = jc_z = jc_cords = 0
for k, g in c.groupby("kfg"):
    esjc = k.startswith("JC")
    for st in g.nudos.dropna():
        ns = nudos_de(st)
        if not any(t != "S" and dr == "S" for _, t, _, dr in ns):
            continue
        s = sum(n for n, t, _, dr in ns if t == "S" and dr == "S")
        z = sum(n for n, t, _, dr in ns if t == "S" and dr == "Z")
        cords += 1
        tot_s += s
        tot_z += z
        if esjc:
            jc_cords += 1
            jc_s += s
            jc_z += z
print(f"todos los khipus: cordeles={cords}, simples S={tot_s}, Z={tot_z}")
print(f"solo Inkawasi (JC): cordeles={jc_cords}, simples S={jc_s}, Z={jc_z}")
print("Afirmacion de Clindaniel: 1212 Z vs 0 S (solo Inkawasi).")

print("\nCordeles cuyo UNICO nudo es largo/figure-eight (comparacion con 402 S vs 835 Z):")
ink_kfgs = set(d.loc[ink, "kfg"])
for nombre, kfgs in [("Inkawasi 52", ink_kfgs), ("todos", None)]:
    ss = zz = 0
    sub = c if kfgs is None else c[c.kfg.isin(kfgs)]
    for k, g in sub.groupby("kfg"):
        for st in g.nudos.dropna():
            ns = nudos_de(st)
            if len(ns) == 1 and ns[0][1] != "S":
                if ns[0][3] == "S":
                    ss += ns[0][0]
                elif ns[0][3] == "Z":
                    zz += ns[0][0]
    print(f"  {nombre:12s}: S={ss}, Z={zz} (%Z={zz/max(1,ss+zz):.3f})")

print("\n=== Distribucion de la fraccion Z por quipu (n>=10 simples) ===")
dd = x[x.simple_n >= 10].copy()
dd["fz"] = dd.simple_Z / dd.simple_n
print(dd.fz.describe().round(3).to_string())
print("khipus con fz>0.9:", (dd.fz > 0.9).sum(), "| fz<0.1:", (dd.fz < 0.1).sum(),
      "| 0.4<fz<0.6:", ((dd.fz > 0.4) & (dd.fz < 0.6)).sum(), "de", len(dd))
