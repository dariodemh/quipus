"""T3. Medrano & Urton (2018) y FitzPatrick (2024): los seis quipus del
valle del Santa (UR087-UR092).

Afirmaciones:
  A) Hay 133 grupos de seis cordeles (M&U 2018).
  B) Los valores de los primeros cordeles de esos grupos suman el tributo
     de la revisita de 1670 (documento externo: NO esta en el repo).
  C) Los nudos de amarre de los primeros cordeles varian de forma binaria
     (verso/recto) y dividen a los tributarios en mitades (M&U 2018;
     FitzPatrick 2024 anade marcado/no marcado).
  D) La alineacion optima de mitades de FitzPatrick (combinatoria).

Pruebas: reconstruir los bloques de 6 colgantes consecutivos, contar,
test binomial V/R, test de conglomerados (permutacion preservando el
numero de bloques por quipu) y comparacion de magnitudes dentro/fuera
de quipu. La alineacion de D no se puede replicar sin los valores del
censo de 1670; se reporta como parcial.
"""
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, bloques_de_6, RNG

c, q, _ = cargar()
SEIS = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]

print("Identificacion de los seis quipus del Santa:")
print(q[q.kfg.isin(SEIS)][["kfg", "okr", "museo", "procedencia"]].to_string(index=False))
print("\nOtros quipus con procedencia 'Santa':")
print(q[q.procedencia.astype(str).str.contains("Santa", case=False, na=False)]["kfg"].tolist())

b = bloques_de_6(c, SEIS)
print("\nA) Bloques de 6 colgantes consecutivos:", len(b))
print("   colgantes cubiertos:", 6 * len(b),
      "| colgantes totales nivel 0:", (c.kfg.isin(SEIS) & (c.nivel == 0)).sum())
print("   bloques por khipu:")
print(b.groupby("kfg").size().to_string())

print("\nDistribucion de union del primer cordel de cada bloque:")
print(b.union1.value_counts().to_string())
vv = (b.union1 == "V").sum()
rr = (b.union1 == "R").sum()
print(f"V={vv} R={rr} U={(b.union1=='U').sum()}")
print("binomial V vs R (p=0.5): p =", round(stats.binomtest(vv, vv + rr, 0.5).pvalue, 4))

print("\nC) Union del primer cordel por quipu (¿la variacion es dentro o entre quipus?):")
tab = pd.crosstab(b.kfg, b.union1)
print(tab.to_string())

# Test de conglomerados: ¿cuantos khipus tienen ambos R y V?
obs = sum((tab.get("R", 0) > 0) & (tab.get("V", 0) > 0))
ns = tab.sum(axis=1).to_numpy()
pV = vv / (vv + rr)
B = 20000
cnt = 0
for _ in range(B):
    ambos = 0
    for n in ns:
        x = RNG.binomial(n, pV)
        if 0 < x < n:
            ambos += 1
    if ambos <= obs:
        cnt += 1
p_clust = (cnt + 1) / (B + 1)
print(f"\nKhipus con ambos R y V: observado={obs}; nulo independiente p={p_clust:.5f} (B={B})")

chi2, pchi, dof, _ = stats.chi2_contingency(tab)
print(f"Chi2 khipu x union: chi2={chi2:.1f}, dof={dof}, p={pchi:.2e}")
print("Cramer's V =", round(np.sqrt(chi2 / (tab.values.sum() * (min(tab.shape) - 1))), 3))

print("\nB) Suma de los primeros cordeles =", b.v1.sum())
print("   por khipu:")
print(b.groupby("kfg").v1.agg(["size", "sum"]).to_string())
print("   suma de todas las posiciones del bloque (offsets 0-5):",
      [int(sum(v[j] for v in b.valores)) for j in range(6)])
print("   (132 tributarios y 133 bloques: ningun offset da 132/133)")

print("\nMagnitud del bloque segun union del primer cordel:")
print(b.groupby("union1").agg(n=("v1", "size"), v1_med=("v1", "median"),
                              total_med=("total", "median")).to_string())
for col in ["v1", "total"]:
    x = b[b.union1 == "V"][col]
    y = b[b.union1 == "R"][col]
    print(f"  Mann-Whitney {col}: p={stats.mannwhitneyu(x, y).pvalue:.2e}"
          f" (V med={x.median():.0f}, R med={y.median():.0f})")

print("\nControl dentro de quipu: solo UR090 tiene bloques R y V.")
u = b[b.kfg == "UR090"]
print(u.groupby("union1").agg(n=("v1", "size"), v1_med=("v1", "median"),
                              total_med=("total", "median")).to_string())
for col in ["v1", "total"]:
    x = u[u.union1 == "V"][col]
    y = u[u.union1 == "R"][col]
    print(f"  UR090 Mann-Whitney {col}: p={stats.mannwhitneyu(x, y).pvalue:.3f}"
          f" (V med={x.median():.0f}, R med={y.median():.0f})")

print("\nNivel de quipu: comparacion de medianas de bloque")
print(b.groupby("kfg").agg(med_total=("total", "median"), med_v1=("v1", "median"),
                           union=("union1", lambda s: "/".join(sorted(set(s))))).to_string())
