"""Verificación de la afirmación de K-CAT:
"padre = suma de hijos se cumple solo en 6,6% de los grupos padre-hijo;
razón mediana 0,35; 39,4% de los grupos son triviales".

Definiciones (transparentes, porque K-CAT no publica la suya):
  D1: grupos padre->hijos directos con >=1 hijo con valor; cuerdas sin nudos
      = ausentes (regla 6 del brief).
  D1b: como haría un pipeline que cuenta los grupos sin hijos con valor como
      "suma 0" (ausencia tratada como cero). Sirve para diagnosticar el 6,6%/0,35.
  D2: solo grupos con >=2 hijos con valor (descarta el caso de 1 hijo).

Control: nulo por permutación de los valores de los hijos DENTRO de cada
quipu (preserva distribución de valores y tamaño de grupo de cada quipu),
2000 permutaciones, p empírico de una cola, Holm para D1/D2.
"""
import json
import os

import numpy as np
import pandas as pd

from comun import cargar_cuerdas, SALIDA, SEMILLA

rng = np.random.default_rng(SEMILLA)
c = cargar_cuerdas()
c["v0"] = np.where(c.con_nudos & c.valor.notna(), c.valor, 0.0)
R = {}

# ---------------------------------------------------------------- construir grupos
# lookup sin duplicados (algunos nombres de cuerda se repiten: nos quedamos con el primero)
cab = c.drop_duplicates(["kfg", "cuerda"]).set_index(["kfg", "cuerda"])["v"].to_dict()
cab0 = c.drop_duplicates(["kfg", "cuerda"]).set_index(["kfg", "cuerda"])["v0"].to_dict()
filas = []
for (k, p), g in c[c.nivel >= 1].groupby(["kfg", "padre"]):
    pv = cab.get((k, p), np.nan)
    if pd.isna(pv):
        continue
    hijos = g.v.dropna()
    filas.append(dict(kfg=k, padre=p, pv=float(pv), suma=float(hijos.sum()),
                      nh=int(len(hijos)), suma0=float(g.v0.sum()),
                      nh0=int(len(g)), pv0=float(cab0.get((k, p), np.nan))))
gr = pd.DataFrame(filas)
print(f"grupos padre-hijo con valor de padre: {len(gr)}; khipus: {gr.kfg.nunique()}")
print(f"  de ellos, sin ningún hijo con valor: {(gr.nh == 0).sum()}")


def resumen(sub, etiqueta):
    exact = (sub.pv == sub.suma)
    ratio = sub.suma / sub.pv.replace(0, np.nan)
    print(f"{etiqueta:32s} n={len(sub):5d}  exacto={100*exact.mean():5.2f}%  "
          f"mediana hijo/padre={ratio.median():.2f}")
    return dict(n=int(len(sub)), pct_exacto=round(100*float(exact.mean()), 2),
                mediana_ratio=round(float(ratio.median()), 3))


print("\n--- reproducción descriptiva ---")
R["D1"] = resumen(gr[gr.nh > 0], "D1 hijos con valor (correcto)")
R["D1b"] = resumen(gr, "D1b todos (ausentes=0)")
R["D2"] = resumen(gr[gr.nh >= 2], "D2 grupos con >=2 hijos")
# ¿qué fracción de las igualdades exactas viene de grupos de 1 hijo?
base1 = gr[gr.nh > 0]
ex = base1[base1.pv == base1.suma]
pct_1h = 100 * (ex.nh == 1).mean()
print(f"de las {len(ex)} igualdades exactas, {int((ex.nh == 1).sum())} son grupos "
      f"de 1 hijo ({pct_1h:.1f}%)")
R["composicion_exactas"] = dict(n_exactas=int(len(ex)),
                                de_1_hijo=int((ex.nh == 1).sum()),
                                pct_1_hijo=round(float(pct_1h), 1))
# D3: ceros donde no hay nudos, como K-CAT
triv = (gr.pv0 == 0) | (gr.suma0 == 0)
nt = gr[~triv]
print(f"D3 (sin nudos=0): triviales={100*triv.mean():.1f}% (K-CAT 39,4%); "
      f"exacto no trivial={100*(nt.pv0 == nt.suma0).mean():.2f}% (K-CAT 6,6%); "
      f"mediana ratio={((nt.suma0/nt.pv0).median()):.2f} (K-CAT 0,35)")
R["D3"] = dict(pct_trivial=round(100*float(triv.mean()), 1),
               pct_exacto_no_trivial=round(100*float((nt.pv0 == nt.suma0).mean()), 2),
               mediana_ratio=round(float((nt.suma0 / nt.pv0).median()), 2))
# variante ampliada: incluir también grupos cuyo padre no tiene valor (padre=0)
filas2 = []
for (k, p), g in c[c.nivel >= 1].groupby(["kfg", "padre"]):
    filas2.append((float(cab0.get((k, p), 0.0)), float(g.v0.sum())))
d2 = pd.DataFrame(filas2, columns=["pv", "cs"])
tr2 = (d2.pv == 0) | (d2.cs == 0)
print(f"D3 ampliado (padres ausentes=0): grupos={len(d2)}; "
      f"triviales={100*tr2.mean():.1f}% (K-CAT 39,4%)")
R["D3_ampliado"] = dict(grupos=int(len(d2)), pct_trivial=round(100*float(tr2.mean()), 1))

# ---------------------------------------------------------------- nulo por permutación
# Solo grupos con >=1 hijo con valor (D1). Tabla de hijos con valor.
base = gr[gr.nh > 0].reset_index(drop=True)
ch = c[(c.nivel >= 1) & c.v.notna()].copy()
ch = ch.merge(base[["kfg", "padre"]].assign(gid=np.arange(len(base))),
              on=["kfg", "padre"], how="inner")
ch = ch.sort_values("gid").reset_index(drop=True)
gid = ch.gid.values
vals = ch.v.values.astype(float)
G = len(base)
pv = base.pv.values.astype(float)
claves = list(ch.groupby("kfg").indices.values())


def tasas(v):
    s = np.bincount(gid, weights=v, minlength=G)
    ex = pv == s
    return ex.mean(), ex[(base.nh >= 2).values].mean()


obs1, obs2 = tasas(vals)
print(f"\nObservado: D1={100*obs1:.2f}%  D2={100*obs2:.2f}%")

n_perm = 2000
n1 = n2 = 0
for _ in range(n_perm):
    v = vals.copy()
    for idx in claves:
        v[idx] = rng.permutation(v[idx])
    e1, e2 = tasas(v)
    n1 += e1 >= obs1
    n2 += e2 >= obs2
p1, p2 = (n1 + 1) / (n_perm + 1), (n2 + 1) / (n_perm + 1)
print(f"p_perm D1={p1:.4f}  p_perm D2={p2:.4f}  (N={n_perm}, una cola)")
pvals = sorted([("D1", p1), ("D2", p2)], key=lambda x: x[1])
holm = {nom: min(1.0, p * (2 - i)) for i, (nom, p) in enumerate(pvals)}
print("Holm:", {k: round(v, 4) for k, v in holm.items()})
R["nulo"] = dict(obs_D1=round(100*float(obs1), 2), obs_D2=round(100*float(obs2), 2),
                 p_D1=float(p1), p_D2=float(p2), holm=holm, n_perm=n_perm)

# Interpretación: la igualdad exacta ocurre MÁS que en el nulo que baraja los
# valores de los hijos dentro del quipu, pero sigue siendo una minoría.

with open(os.path.join(SALIDA, "res_06_sumas.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_06_sumas.json")
