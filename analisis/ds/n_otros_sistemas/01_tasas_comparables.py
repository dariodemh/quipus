# -*- coding: utf-8 -*-
"""
01 · ¿Es comparable la tasa 8/18 de Incahuasi con otras contabilidades?
Objetivo: mostrar que una tasa bruta de "sumas exactas" no es comparable entre
sistemas con distinto regimen numerico; la unica magnitud comparable es el
exceso sobre el azar (lift), y ese exceso exige conocer el espacio de busqueda.

No re-deriva la alineacion de Incahuasi (ya auditada en 13, 16 y por el
coordinador): usa componentes_filas.csv y libro_consolidado.csv como datos.
Semilla fija. Salidas: resultados_01.txt, tasas_regimenes.csv
"""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(20261018)
BASE = os.path.dirname(os.path.abspath(__file__))
R13 = os.path.join(BASE, "..", "..", "13_sistema_incahuasi")
DAT = os.path.join(BASE, "..", "..", "datos")

# ---------- A. Incahuasi: reproducir el conteo y medir la densidad del blanco ----
comp = pd.read_csv(os.path.join(R13, "componentes_filas.csv"))
lib = pd.read_csv(os.path.join(R13, "libro_consolidado.csv"))
s = comp[comp.fuente == "UR273A+UR273B"].copy()
targets = set(lib.cabecera.dropna().astype(int))
print("Registros A+B:", len(s), "| cabeceras en UR266/275/269:", len(targets),
      "| rango:", min(targets), max(targets))
exact = s.suma.isin(targets).sum()
pm1 = s.suma.apply(lambda x: any(abs(x - t) <= 1 for t in targets)).sum()
print("Sumas exactas:", exact, "/", len(s), "| +-1:", pm1)

# Nulo 1: barajar B entre registros (rompe el emparejamiento, conserva marginales)
B = s.parte_B.to_numpy(); A = s.parte_A.to_numpy(); obs = exact
cnt = np.zeros(20000, dtype=int)
for i in range(20000):
    cnt[i] = np.isin(A + rng.permutation(B), list(targets)).sum()
p1 = (1 + (cnt >= obs).sum()) / 20001
print(f"Nulo barajando B: media {cnt.mean():.2f} max {cnt.max()} p={p1:.5f}")
chance = cnt.mean() / len(s)
print(f"Tasa de acierto por comparacion al azar: {chance:.3f}; observada {obs/len(s):.3f}; lift {obs/cnt.mean():.1f}x")

# Densidad "efectiva" del blanco: cuantas sumas de pares caen en el blanco
# usando A y B remuestreados con reemplazo (mismo regimen de magnitud).
boot = []
for i in range(4000):
    a = rng.choice(A, len(A)); b = rng.choice(B, len(B))
    boot.append(np.isin(a + b, list(targets)).sum() / len(A))
print(f"Chance bootstrap (A,B con reemplazo): {np.mean(boot):.3f} (DE {np.std(boot):.3f})")

# ---------- B. Regimen de numeros pequenos: quipus reales del corpus -------------
cu = pd.read_csv(os.path.join(DAT, "cuerdas.csv"), usecols=["kfg", "grupo", "nivel", "valor", "nudos"])
cu = cu[(cu.nivel == 0) & (cu.grupo.notna())]
# cabecera de grupo = primer colgante con nudos
rows = []
for (k, g), d in cu.groupby(["kfg", "grupo"], sort=False):
    d = d.sort_index()
    v = d[d.nudos.notna() & (d.valor > 0)]
    if len(v) >= 2:
        rows.append((k, int(g), int(v.valor.iloc[0]), len(d)))
g = pd.DataFrame(rows, columns=["kfg", "grupo", "cabecera", "ancho"])

def chance_regimen(T, pool, n=4000):
    """P(a+b in T) con a,b extraidos del pool (con reemplazo)."""
    T = np.array(sorted(set(T))); pool = np.array(pool)
    a = rng.choice(pool, n); b = rng.choice(pool, n)
    return np.isin(a + b, T).mean()

small = []
for k, d in g.groupby("kfg"):
    if len(d) >= 6:
        h = d.cabecera.to_numpy()
        if 5 <= np.median(h) <= 300 and h.max() <= 2000:
            small.append(chance_regimen(h, h, 2000))
print(f"Quipus de numeros pequenos usados: {len(small)} | chance mediana {np.median(small):.3f} (IQR {np.percentile(small,25):.3f}-{np.percentile(small,75):.3f})")

# ---------- C. Regimenes sexagesimales sinteticos (Uruk-like) -------------------
def grid(step, lo, hi, n):
    vals = np.arange(lo, hi + 1, step)
    return rng.choice(vals, min(n, len(vals)), replace=False)

out = [dict(regimen="Incahuasi (observado)", n_blanco=len(targets), rango=f"{min(targets)}-{max(targets)}",
            chance=obs/len(s), nota="8/18 exactas")]
out.append(dict(regimen="Incahuasi (nulo de emparejamiento)", n_blanco=len(targets),
                rango=f"{min(targets)}-{max(targets)}", chance=chance, nota="barajar B"))
out.append(dict(regimen="quipus reales, valores <=300", n_blanco=np.nan, rango="5-2000",
                chance=float(np.median(small)), nota=f"n={len(small)} quipus"))
for step, hi, name in [(10, 1000, "redondo: 20 valores, multiplos de 10 (1-1000)"),
                       (60, 3600, "sexagesimal: 20 valores, multiplos de 60 (60-3600)"),
                       (1, 1000, "enteros: 20 valores (1-1000)")]:
    T = grid(step, step, hi, 20)
    pool = grid(step, step, hi // 2, 20)
    out.append(dict(regimen=name, n_blanco=len(T), rango=f"{step}-{hi}",
                    chance=chance_regimen(T, pool, 20000), nota="simulacion, 20 blancos"))

res = pd.DataFrame(out)
res["chance"] = res.chance.round(3)
res.to_csv(os.path.join(BASE, "tasas_regimenes.csv"), index=False)
print("\n--- Comparacion de regimenes ---")
print(res.to_string(index=False))
print("\nLectura: 44% de acierto solo es informativo frente al ~5% de su propio nulo.")
print("En un regimen de numeros redondos o sexagesimales el azar solo puede dar 19-35%.")
