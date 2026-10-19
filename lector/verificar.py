# -*- coding: utf-8 -*-
"""Verificación del lector: reproduce resultados conocidos del proyecto y falla (assert) si algo se rompe.
Uso:  python lector/verificar.py      (~1–2 min)"""
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import detectores as D  # noqa: E402
import lector as LT  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
t0 = time.time()
ctx = D.Contexto()
q = ctx.por_quipu
ok = []


def check(nombre, cond, detalle=""):
    print(f"[{'OK' if cond else 'FALLA'}] {nombre}" + (f"\n       {detalle}" if detalle else ""))
    ok.append(bool(cond))


def det(r, tipo, o, d):
    return [h for h in r["datos"]["detectadas"] if h["tipo"] == tipo and h["origen"] == o and h["destino"] == d
            and h["q"] < .05]


# 1. Incahuasi: UR270 -> UR278 (celda) y UR278 -> UR266 / UR275 (totales), recalculados desde cero
r278 = D.relaciones(q["UR278"], ctx)
c = det(r278, "celda = P + S1", "UR270", "UR278")
check("UR270 -> UR278: celda = P + S1 (>=5 grupos, BH q<0,05; con solo P menos grupos)",
      c and c[0]["detalle"].startswith("5 grupos") and c[0]["detalle"].endswith("solo P: 0"), c)
t1, t2 = det(r278, "totales en orden", "UR278", "UR266"), det(r278, "totales en orden", "UR278", "UR275")
check("UR278 -> UR266 y UR278 -> UR275: totales de grupo en orden (BH q<0,05)", t1 and t2,
      [h["detalle"] + f" q={h['q']:.1e}" for h in t1 + t2])
r275 = D.relaciones(q["UR275"], ctx)
t3 = det(r275, "totales en orden", "UR278", "UR275")
doc = [a for a in r275["afirmaciones"] if a["texto"].startswith("UR266 → UR275") and a["nivel"] == "demostrado"]
# La copia UR275 ~ UR266 está demostrada a nivel de registro (13: 44/46 aristas), no por el alineamiento cuerda a
# cuerda: en 04 tampoco pasa (q=0,20, q_bloque=1). El lector reproduce ese negativo y muestra la documentada.
cp = [h for h in r275["datos"]["detectadas"] if h["tipo"].startswith("copia") and h["con"] == "UR266"]
check("Cadena UR278 -> UR275 -> UR266: totales de UR278 en UR275 (recalculado) + copia UR266/UR275 (documentada, 13); "
      "el SW cuerda a cuerda no la da, como en 04", t3 and doc and not cp, [a["texto"] for a in doc])

# 2. Celda de UR278 = P + S1 de UR270, cifra a cifra (13; 29_lectura_incahuasi/coherencia.py)
P, S = D._celdas(q["UR270"])[9]
filas = D._celdas(q["UR278"])[9][0]
g0 = P[0] + S[0]
best = filas[np.argmax([(g0 == f).sum() for f in filas])]
check("UR270 g0 (P+S1) = una fila de UR278 con 8/9 exactas y la 1.ª a +1 (= UR278 g21)",
      (g0 == best).sum() == 8 and best[0] - g0[0] == 1, f"P+S1 {g0.tolist()} | fila {best.tolist()}")

# 3. Formato Nazca/Berlín
for k, size, n, m in (("UR1140", 9, 19, 19), ("UR1131", 10, 12, 11)):
    f = [x for x in D.ficha_nazca(q[k], ctx)["datos"]["barrido"] if x["size"] == size]
    check(f"{k}: ficha de {size} cuerdas, campo 1 máximo en {m} de {n} registros",
          f and f[0]["completos"] == n and f[0]["campo1_max"] == m and f[0]["p_bonf"] < .05, f)

# 4. Género del atlas
g = D.genero(q["UR053A"], ctx, [])["datos"]
check("UR053A: Formulario con clave de reparto (FOR), confianza alta", g["genero"] == "FOR" and g["confianza"] == "alta", g)
RG = ctx._RG
A = RG.clasificar(ctx.matriz)
igual = (A.genero == ctx.atlas.genero.reindex(A.index)).mean()
check("Las reglas del atlas reproducen atlas.csv en los 651 quipus", igual == 1, f"coincidencia {igual:.3f}")

# 5. Nudos de >=10 vueltas reales (OKR): UR1095 = 32 cuerdas (n_nudos_imposibles)
gr = D.gramatica(q["UR1095"], ctx)["datos"]
check("UR1095: 32 cuerdas con nudos largos de >=10 vueltas en OKR", gr["L_10_o_mas_OKR"] == 32, gr)

# 6. Controles negativos: un quipu sin relaciones y UR278 con los valores barajados
for k in ("AS010", "UR001"):
    r = D.relaciones(q[k], ctx)
    check(f"Control negativo {k}: sin relaciones detectadas", not r["datos"]["detectadas"], r["datos"]["detectadas"])
bar = q["UR278"].copy()
bar["valor"] = np.random.default_rng(1).permutation(bar.valor.values)
bar["kfg"] = "UR278_barajado"
r = D.relaciones(bar, ctx)
check("Control negativo: UR278 con valores barajados no da relaciones", not r["datos"]["detectadas"],
      r["datos"]["detectadas"])

# 7. Entrada CSV: UR278 con otro nombre debe dar copia de UR278 y sus totales en UR266
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "X278.csv"
    x = D.preparar(D.pd.read_csv(D.AN / "datos/cuerdas.csv", low_memory=False, keep_default_na=False))
    x = x[x.kfg == "UR278"].drop(columns=["anudada", "pres", "colorn", "kfg"])
    x.to_csv(p, index=False)
    (d,) = LT.resolver(str(p), ctx)
    L = LT.leer(d, ctx)
    rel = next(s for s in L["secciones"] if s["titulo"].startswith("Relaciones"))["datos"]["detectadas"]
    gen = L["secciones"][-1]["datos"]
    check("CSV X278: copia de UR278 y totales en orden en UR266; género recalculado sin error",
          any(h["con"] == "UR278" and h["tipo"] == "copia" for h in rel)
          and any(h["tipo"] == "totales en orden" and h["destino"] == "UR266" for h in rel)
          and not any(s.get("error") for s in L["secciones"]),
          f"{[(h['tipo'], h['con']) for h in rel]}; género {gen['genero']} ({gen['confianza']})")

# 8. Rondas 17–18: detectores de 30_frontera_estructura, desde cero
r = D.alternancia(q["UR040"], ctx)
x = r["datos"]
check("UR040: alternancia W/AB de desfase 2 (26/33 posiciones; p perm<=1e-3) y apoyada por la q del corpus (06)",
      x["desfase"] == 2 and x["posiciones_alternas"] == 26 and x["p"] <= 1e-3
      and any(a["nivel"] == "apoyado" for a in r["afirmaciones"]), {k: x[k] for k in ("desfase", "posiciones_alternas", "p")})
r = D.alternancia(q["AS006"], ctx)
check("Control negativo AS006: sin alternancia de desfase 2", not r["afirmaciones"], r["datos"])
r = D.totales_columna(q["KH0049"], ctx)["datos"]["significativos"]
b0 = [s for s in r if s["total"] == "B0" and s["partes"] == "B1+B2"]
check("KH0049: tabla jerárquica, B0 = B1+B2 en >=12/18 (q<0,05) y B1 = B3+B4+B5 también significativo (07)",
      b0 and b0[0]["exactas"] >= 12 and any(s["total"] == "B1" and s["partes"] == "B3+B4+B5" for s in r), r)
bar = q["KH0049"].copy()
bar["valor"] = np.random.default_rng(1).permutation(bar.valor.values)
bar["kfg"] = "KH0049_barajado"
r = D.totales_columna(bar, ctx)
check("Control negativo: KH0049 con los valores barajados no da totales por columna", not r["afirmaciones"],
      r["datos"]["significativos"])

# 9. UR1104 extrae las cabeceras (campo 1 de los registros de 8 cuerdas) de UR234 (33_estematica), desde cero
cab = q["UR234"][q["UR234"].nivel == 0].valor.to_numpy()[::8]
x = q["UR1104"]
pos = [int(np.where(cab == v)[0][0]) for v in x.valor[x.nivel == 0] if v >= 100 and v in cab]
lis = []  # subsecuencia creciente más larga de las posiciones de cabecera (en orden en los dos quipus)
for p_ in pos:
    i = np.searchsorted(lis, p_)
    lis[i:i + 1] = [p_]
doc = [a for a in D.relaciones(x, ctx)["afirmaciones"] if a["texto"].startswith("UR234 → UR1104")]
check("UR1104 -> UR234: >=8 cabeceras de UR234 en orden en UR1104; la 6.ª, rota en UR234, es 2016 en UR1104; documentada",
      len(lis) >= 8 and cab[5] == 0 and 2016 in x.valor.values and doc and doc[0]["nivel"] == "apoyado",
      f"cabeceras en orden: {len(lis)}; UR234 {cab.tolist()}")

# 10. Enmiendas del atlas (atlas.csv queda congelado) y cobertura alta + media antes/después
g = D.genero(q["KH0049"], ctx, [])["datos"]
E = ctx.enmiendas
check("Enmiendas: KH0049 sigue FOR en el atlas y el lector muestra la enmienda SUM; todas las enmiendas son del atlas",
      g["genero"] == "FOR" and g.get("enmienda", {}).get("genero") == "SUM" and E.index.isin(ctx.atlas.index).all()
      and E.genero_nuevo.isin(RG.NOMBRE).all(), g.get("enmienda"))
conf = ctx.atlas.confianza.copy()
w = ctx.matriz.n_cuerdas.reindex(conf.index)
for nombre, cf in (("antes", conf), ("después", conf.where(~conf.index.isin(E.index), E.confianza.reindex(conf.index)))):
    m = cf.isin(["alta", "media"])
    print(f"       cobertura {nombre}: {m.sum()} quipus ({m.mean():.1%}), {w[m].sum() / w.sum():.1%} de las cuerdas")

print(f"\n{sum(ok)}/{len(ok)} comprobaciones correctas en {time.time() - t0:.0f} s")
assert all(ok), "verificación FALLIDA"
