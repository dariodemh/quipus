"""04 - Busqueda dirigida de relaciones NUEVAS con las cuerdas que KFG no tiene.

Universo de cuerdas nuevas: las 107 subsidiarias (nivel>0) de los 5 quipus de Incahuasi en los que KFG
no registro NINGUNA subsidiaria: UR256 (+58), UR274B (+32), UR265 (+11), UR255 (+4), UR264 (+2).
Es una definicion conservadora: excluye los quipus donde la diferencia es solo el aplanamiento de la
jerarquia en OKR (UR262, UR270, UR280, UR271...) y no puede contar dos veces la misma cuerda.
En total OKR tiene 111 subsidiarias nuevas; las 4 de UR280 quedan fuera del analisis por esa razon.

Pruebas:
 N1  valores nuevos de UR274B  -> diana del libro consolidado (UR266+UR275+UR269)
 N2  valores nuevos de UR256   -> diana del consolidado
 N3  valores nuevos de UR274B  -> diana de UR270 ; N4 -> diana de UR278 ; N5 -> cuotas {10,15,17,25,30,46,47,208}
 N6  valores nuevos de UR256   -> diana de UR267B (su original) ; N7 -> diana de UR255 (pareja atada)
 N8  UR274B: cabecera + suma de subsidiarias nuevas del registro -> consolidado (nulo: barajar las nuevas
     entre registros de UR274B)
 N9  UR274A + UR274B (con las nuevas) -> consolidado  [ya calculado en 03; se repite aqui para el BH]
 N10 cuota 17 explicita en UR274B [de 03; se repite el p para el BH]

Nulo de N1-N7: cada valor nuevo se sustituye por uno de los 40 valores mas cercanos en escala log del
pool de cuerdas anudadas de Incahuasi que NO son nuevas (conserva magnitud; rompe la identidad concreta).
10 000 replicas, semilla fija. BH-FDR sobre la familia N1-N8 (8 pruebas). N9 y N10 son replicas de 03 y
se informan aparte para no mezclar familias.

Salida: nuevas_pruebas.csv
"""
import numpy as np
import pandas as pd
import lib_okr as L

SEED = 4219
rng = np.random.default_rng(SEED)
NPERM = 10000
NUEVOS = ["UR255", "UR256", "UR264", "UR265", "UR274B"]
c = L.cargar()
nuevas = c[(c.nivel > 0) & c.kfg.isin(NUEVOS)].copy()
pool = c[c.pres & ~c.cord_id.isin(nuevas.cord_id)].valor.to_numpy()
ps = np.sort(pool)
lps = np.log(np.maximum(ps, 1))


def vecinos(vals):
    """Sustituye cada valor por uno de los 40 mas cercanos en log del pool (nulo de magnitud de 13)."""
    idx = np.searchsorted(lps, np.log(np.maximum(np.asarray(vals, float), 1)))
    lo = np.clip(idx - 20, 0, len(ps) - 40)
    return ps[lo + rng.integers(0, 40, size=len(vals))]


FIL = []


def prueba(nombre, vals, S, familia="nuevas"):
    vals = np.asarray(vals)
    S = np.asarray(S)
    obs = int(np.isin(vals, S).sum())
    nul = np.array([np.isin(vecinos(vals), S).sum() for _ in range(NPERM)])
    FIL.append(dict(prueba=nombre, n=len(vals), obs=obs, nulo_media=float(nul.mean()),
                    nulo_max=int(nul.max()), p=float((np.sum(nul >= obs) + 1) / (NPERM + 1)), familia=familia))
    print(f"{nombre}: {obs}/{len(vals)}; nulo {nul.mean():.2f} (max {nul.max()}); p={(np.sum(nul >= obs) + 1) / (NPERM + 1):.4g}")


CONS = L.conjunto(c, ["UR266", "UR275", "UR269"])
CUOTAS = np.array([10, 15, 17, 25, 30, 46, 47, 208])
v274 = nuevas[(nuevas.kfg == "UR274B") & nuevas.pres].valor.to_numpy()
v256 = nuevas[(nuevas.kfg == "UR256") & nuevas.pres].valor.to_numpy()

print(f"cuerdas nuevas: {len(nuevas)} ({nuevas.pres.sum()} anudadas); UR274B {len(v274)}, UR256 {len(v256)}")
prueba("UR274B nuevas -> consolidado", v274, CONS)
prueba("UR256 nuevas -> consolidado", v256, CONS)
prueba("UR274B nuevas -> UR270", v274, L.conjunto(c, ["UR270"]))
prueba("UR274B nuevas -> UR278", v274, L.conjunto(c, ["UR278"]))
prueba("UR274B nuevas -> cuotas", v274, CUOTAS)
prueba("UR256 nuevas -> UR267B", v256, L.conjunto(c, ["UR267B"]))
prueba("UR256 nuevas -> UR255", v256, L.conjunto(c, ["UR255"]))

# N8: cabecera + nuevas subsidiarias del registro -> consolidado
s = c[(c.kfg == "UR274B") & c.pres].copy()
regs = []
for g, x in s.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if not len(x0) or not x0.pres.any():
        continue
    cab = int(x0.valor.iloc[0])
    nn = x[(x.nivel > 0)].valor.sum()
    regs.append((g, cab, int(nn)))
G = pd.DataFrame(regs, columns=["grupo", "cab", "nuevas"])
obs = int(np.isin((G.cab + G.nuevas).to_numpy(), CONS).sum())
nul = np.array([np.isin((G.cab + rng.permutation(G.nuevas.to_numpy())), CONS).sum() for _ in range(NPERM)])
FIL.append(dict(prueba="UR274B cabecera + nuevas del registro -> consolidado", n=len(G), obs=obs,
                nulo_media=float(nul.mean()), nulo_max=int(nul.max()),
                p=float((np.sum(nul >= obs) + 1) / (NPERM + 1)), familia="nuevas"))
print(f"cab+nuevas -> consolidado: {obs}/{len(G)}; nulo {nul.mean():.2f}; p={(np.sum(nul >= obs) + 1) / (NPERM + 1):.4g}")

T = pd.DataFrame(FIL)
T["q_bh"] = L.bh(T.p.to_numpy()) if hasattr(L, "bh") else np.nan
from scipy.stats import false_discovery_control  # noqa: E402
T["q_bh"] = false_discovery_control(T.p.to_numpy())
T.to_csv(L.AQUI / "nuevas_pruebas.csv", index=False, float_format="%.4g")

# N9/N10: replicas de 03 con el mismo codigo (se leen de pruebas_okr.csv / pruebas_kfg.csv)
try:
    a = pd.read_csv(L.AQUI / "pruebas_okr.csv")
    b = pd.read_csv(L.AQUI / "pruebas_kfg.csv")
    print("\nComparacion KFG -> OKR en las pruebas afectadas por las cuerdas nuevas:")
    for pat in ["UR274A+UR274B", "UR274B: registros con 17"]:
        x = a[a.prueba.str.contains(pat, regex=False)][["prueba", "n", "obs", "p"]]
        y = b[b.prueba.str.contains(pat, regex=False)][["prueba", "n", "obs", "p"]]
        print(pd.concat([y.assign(fuente="KFG"), x.assign(fuente="OKR")]).to_string(index=False))
except FileNotFoundError:
    pass
pd.set_option("display.width", 220)
print("\n== TABLA NUEVAS")
print(T[["prueba", "n", "obs", "nulo_media", "nulo_max", "p", "q_bh"]].to_string(index=False))
