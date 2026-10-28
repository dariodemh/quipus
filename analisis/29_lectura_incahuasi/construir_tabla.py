# Construye tabla_traducida.csv: cada cifra del archivo del maní de Incahuasi con su lectura propuesta,
# su papel, su enlace aritmético con otros quipus, el nivel de evidencia y la fuente.
# Base: KFG (analisis/datos/cuerdas.csv); OKR coincide en todos los colgantes de estos quipus (ver coherencia.py).
# Uso, desde la raíz del repo:  python analisis/29_lectura_incahuasi/construir_tabla.py
import pandas as pd

c = pd.read_csv("analisis/datos/cuerdas.csv", low_memory=False, keep_default_na=False)
c["valor"] = pd.to_numeric(c.valor, errors="coerce").fillna(0).round().astype(int)
c["grupo"] = c.grupo.astype(int)
c["orden"] = c.orden.astype(int)
c = c.sort_values(["kfg", "orden"])
q = lambda k: c[c.kfg == k]
F13, F16, FCE = ("analisis/13_sistema_incahuasi/informe.md", "analisis/16_verificacion_incahuasi/informe.md",
                 "analisis/ds/n_cuota_entrega/informe.md")
FTA, FNU, FCA = ("analisis/ds/n_tanteo/informe.md", "analisis/ds/n_nueve_unidades/informe.md",
                 "analisis/ds/n_casi_aciertos/informe.md")
filas = []


def fila(k, g, cuerda, nivel, col, valor, color, rol, lectura, enlace, ev, fuente):
    filas.append(dict(quipu=k, grupo=g, cuerda=cuerda, nivel=nivel, columna=col, valor=valor, color=color, rol=rol,
                      lectura=lectura, enlace=enlace, evidencia=ev, fuente=fuente))


def cab(k, g):
    x = q(k)[(q(k).grupo == g) & (q(k).nivel == 0) & (q(k).valor > 0)]
    return int(x.valor.max()) if len(x) else None


def heads(k):
    return {g: cab(k, g) for g in sorted(q(k).grupo.unique()) if cab(k, g)}


H266, H275, H269 = heads("UR266"), heads("UR275"), heads("UR269")


def donde(v, tol=1):
    out = []
    for k, H in [("UR266", H266), ("UR275", H275), ("UR269", H269)]:
        out += [f"{k} g{g}={h}" + ("" if h == v else f" ({h - v:+d})") for g, h in H.items() if abs(h - v) <= tol]
    return "; ".join(out)


# ------------------------------------------------------------------ UR270 (detalle por unidad: P y S1)
MAPA = {0: 21, 4: 25, 5: 26, 8: 27, 9: 28, 10: 29}  # grupo UR270 -> fila UR278 (13 §2.3; 16; coherencia.py)
u270 = q("UR270")
ps = {}
for g, x in u270.groupby("grupo"):
    col = x[x.nivel == 0]
    nueve = len(col) >= 9 and not col.color.str.startswith("PK").all()
    if g in MAPA or (len(col) == 9 and g == 6):
        for j, r in enumerate(col.itertuples(), 1):
            s1 = x[x.cuerda == r.cuerda + "s1"]
            s1v = int(s1.valor.sum()) if len(s1) else 0
            if j <= 9:
                ps.setdefault(g, []).append((r.valor, s1v))
            extra = " Grupo 6: todos los P en {100, 200}, estructura única en Incahuasi (1/142); sentido desconocido." if g == 6 else ""
            if j > 9:
                fila("UR270", g, r.cuerda, 0, j, r.valor, r.color, "cuerda 10 (fuera de la tabla)",
                     "Sin lectura: no pasa a UR278.", "", "especulativo", F13)
                continue
            fila("UR270", g, r.cuerda, 0, j, r.valor, r.color, "P: componente B de la unidad j",
                 f"Parte B (la mayor) que aportó la unidad {j} en este registro." + extra,
                 f"Σ P del grupo -> cabecera de UR273B g{g + 9}", "bien apoyado (P+S1 -> UR278; Σ P = UR273B en 4/9)", FCE)
            if len(s1):
                fila("UR270", g, r.cuerda + "s1", 1, j, s1v, s1.color.iloc[0], "S1: componente A de la unidad j",
                     f"Parte A (la menor, ~1/3 de P) que aportó la unidad {j} en este registro.",
                     f"P+S1 = {r.valor + s1v}" + (f" -> UR278 g{MAPA[g]} col {j}" if g in MAPA else ""),
                     "bien apoyado (celda = P+S1); S1 = UR273A solo apoyado (1/9 exacta, 3/9 ±1)", FCE)
    else:
        for r in x.itertuples():
            fila("UR270", g, r.cuerda, r.nivel, None, r.valor, r.color,
                 "separador" if r.color.startswith("PK") else "registro sin enlace",
                 "Separador rosado entre tramos." if r.color.startswith("PK") else
                 "Registro de otro formato (subsidiarias múltiples); no se enlaza con UR278 ni UR273.",
                 "", "bien apoyado (separador)" if r.color.startswith("PK") else "sin lectura", F13)

# ------------------------------------------------------------------ UR278 (tabla de 9 columnas)
u278 = q("UR278")
for g, x in u278.groupby("grupo"):
    col = x[x.nivel == 0]
    org = {v: k for k, v in MAPA.items()}.get(g)
    if len(col) == 9:
        tot = int(col.valor.sum())
        for j, r in enumerate(col.itertuples(), 1):
            enl, ev = "", "apoyado (9 columnas = 9 unidades fijas; perfil estable)"
            if org is not None:
                p, s1 = ps[org][j - 1]
                d = r.valor - (p + s1)
                enl = f"= UR270 g{org} col {j}: P {p} + S1 {s1} = {p + s1}" + ("" if d == 0 else f" (diferencia {d:+d})")
                ev = "bien apoyado (celda = P+S1)" if abs(d) <= 1 else "apoyado (fila enlazada; esta celda discrepa)"
            fila("UR278", g, r.cuerda, 0, j, r.valor, r.color, f"celda: unidad {j}",
                 f"Bultos de maní que la unidad {j} (¿pachaca {j}?) aportó en el registro {g}.", enl, ev,
                 f"{F13}; {FNU}")
        for r in x[x.nivel > 0].itertuples():
            fila("UR278", g, r.cuerda, r.nivel, None, r.valor, r.color, "subsidiaria pequeña",
                 "Valor de 3 a 10 colgado de una celda; sin regla conocida.", "", "sin lectura", F13)
        d, ev = donde(tot, 0), "bien apoyado (11 totales exactos en orden en UR266, 7 en UR275)"
        if not d and donde(tot, 1):
            d, ev = donde(tot, 1), "apoyado (destino a ±1)"
        if not d:
            casi = [x for x in donde(tot, 1000).split("; ") if x and any(f"({s}{n})" in x for s in "+-"
                                                                         for n in (6, 100, 1000))]
            d = ("casi: " + "; ".join(casi) + " (diferencia de un racimo o un nudo: discrepancia de copia)") if casi                 else "sin destino conservado"
            ev = "propuesto (casi-acierto; n_casi_aciertos)" if casi else "sin enlace"
        fila("UR278", g, "Σ fila", None, None, tot, "", "total del registro (calculado, no anudado)",
             f"Total de bultos de maní del registro {g}, suma de las 9 unidades.", d, ev,
             f"{F16}; {FCA}; paquete_revision/tabla_hallazgos.csv I02")
    else:
        for r in x.itertuples():
            pk = r.color.startswith("PK")
            fila("UR278", g, r.cuerda, r.nivel, None, r.valor, r.color, "separador" if pk else "registro irregular",
                 "Separador." if pk else f"Grupo de {len(col)} colgantes: fuera del formato de 9; sin lectura.",
                 "", "sin lectura", F13)

# ------------------------------------------------------------------ componentes UR273A/B y UR274A/B
CUOTA = {"UR273A": None, "UR273B": 17, "UR274A": 30, "UR274B": 17}
LECT = {"UR273A": "componente A (la parte menor, en centenas) del registro",
        "UR273B": "componente B (la parte mayor, en miles) del registro",
        "UR274A": "copia y complemento del componente A (cuota explícita 30)",
        "UR274B": "copia del componente B (cuota explícita 17)"}
H273A, H273B = heads("UR273A"), heads("UR273B")
for k in CUOTA:
    for g, x in q(k).groupby("grupo"):
        h = cab(k, g)
        for r in x.itertuples():
            if r.color.startswith("PK") and r.valor == 0:
                rol, lec, enl, ev = "separador", "Separador rosado (mismas posiciones en UR273A y UR273B).", "", "bien apoyado"
            elif r.valor == 0:
                continue
            elif k == "UR273A" and r.valor == 30:
                rol, lec, enl, ev = ("cuota fija del componente", "Cuota 30 del componente A con la cabecera en blanco; "
                                     "el registro lo completa UR274A (891 + 1129 = 2020).", "30 + 17 = 47",
                                     "apoyado (cuota); suma propuesta")
            elif r.valor == h and r.nivel == 0:
                rol, lec, ev = "cabecera del componente", f"Bultos del {LECT[k]} {g}.", "apoyado (UR273A+B -> libros, 8/18)"
                enl = ""
                if k in ("UR273A", "UR273B") and g in H273A and g in H273B:
                    s = H273A[g] + H273B[g]
                    enl = f"A+B = {H273A[g]}+{H273B[g]} = {s}" + (f" -> {donde(s, 0)}" if donde(s, 0) else " (sin destino exacto)")
                if k == "UR273B":
                    enl += f"; = Σ P de UR270 g{g - 9}" if (g - 9) in ps and sum(p for p, _ in ps[g - 9]) == h else ""
            elif r.valor in (CUOTA[k], 30, 17, 10) and r.valor < 50:
                rol = "cuota fija del componente"
                lec = f"Cantidad fija apartada por registro ({r.valor})."
                if k == "UR274B" and r.valor == 10:
                    lec += " Probable 17 con el 7L terminal perdido (n_casi_aciertos; mirar la punta)."
                enl, ev = "30 + 17 = 47 (cuota del libro)", "apoyado (cuota fija); suma 30+17=47 propuesta"
            else:
                rol, lec, enl, ev = "partida", "Partida del registro; regla no establecida.", "", "sin lectura"
            fila(k, g, r.cuerda, r.nivel, None, r.valor, r.color, rol, lec, enl, ev, f"{F13}; {FTA}")

# ------------------------------------------------------------------ libros UR266, UR275, UR268, UR269
LIB = {"UR275": (47, "libro del flujo con reparto (bruto, cuota 47, destinos)"),
       "UR266": (47, "copia resumida de UR275 (bruto y cuota 47)"),
       "UR268": (208, "libro de magnitud mayor (cuota 208)"),
       "UR269": (None, "libro de otro formato (cuotas 47/46/44/40/25)")}
tot278 = {g: int(x.valor.sum()) for g, x in u278[u278.nivel == 0].groupby("grupo") if len(x) == 9}
sumAB = {H273A[g] + H273B[g]: g for g in H273A if g in H273B}
for k, (cuota, desc) in LIB.items():
    niveles = [0] if k == "UR269" else [0, 1]
    for g, x in q(k).groupby("grupo"):
        h = cab(k, g)
        for r in x[x.nivel.isin(niveles)].itertuples():
            if r.valor == 0:
                continue
            if r.valor == h and r.nivel == 0:
                rol = "bruto (cabecera)"
                lec = f"Total de bultos que entró en el registro {g} ({desc})."
                e = [f"= fila UR278 g{f}" + ("" if t == h else f" ({t - h:+d})") for f, t in tot278.items() if abs(t - h) <= 1]
                e += [f"= UR273A+B g{gg}" for s, gg in sumAB.items() if s == h]
                otros = donde(h, 0).split("; ")
                e += [o for o in otros if o and not o.startswith(f"{k} ") and h % 100]  # redondos: coincidencia trivial
                enl = "; ".join(e)
                ev = ("bien apoyado (destino de UR278)" if any("UR278" in s for s in e) else
                      "apoyado (destino de A+B)" if any("A+B" in s for s in e) else "apoyado (formato bruto-cuota-resto)")
                if k == "UR269":
                    ev = "apoyado (recibe sumas A+B)" if any("A+B" in s for s in e) else "propuesto"
            elif r.valor in (47, 46, 44, 40, 25, 208) and r.nivel == 0 and (cuota is None or r.valor in (cuota, 40, 44)):
                rol = "cuota fija"
                lec = f"Cantidad fija apartada del registro ({r.valor}; {100 * r.valor / h:.1f} % del bruto)." if h else \
                    f"Cantidad fija ({r.valor})."
                if k == "UR275" and r.valor == 40:
                    lec += " Probable 47 con el 7L terminal perdido (n_casi_aciertos)."
                enl, ev = "", "bien apoyado (valor fijo; publicado por Urton y Chu); absoluta, no %: apoyado"
            else:
                rol = "partida / destino" if r.nivel == 0 else "subsidiaria"
                lec = ("Parte del bruto repartida a un destino (¿colca, procedencia o salida?)." if k in ("UR275", "UR268")
                       else "Partida del registro; regla no establecida." if r.nivel == 0
                       else "Subsidiaria (en UR266, valores grandes 0G/0B sin regla conocida).")
                enl = ""
                ev = "apoyado (UR275: bruto = cuota + destinos en 15/16)" if k == "UR275" and r.nivel == 0 else \
                    "propuesto" if r.nivel == 0 else "sin lectura"
            fila(k, g, r.cuerda, r.nivel, None, r.valor, r.color, rol, lec, enl, ev, f"{F13}; {FTA}")

t = pd.DataFrame(filas)
orden = ["UR270", "UR278", "UR273A", "UR273B", "UR274A", "UR274B", "UR275", "UR266", "UR269", "UR268"]
t["k"] = t.quipu.map(orden.index)
t = t.sort_values(["k", "grupo"], kind="stable").drop(columns="k")
for k in ("nivel", "columna"):
    t[k] = t[k].astype("Int64")
t.to_csv("analisis/29_lectura_incahuasi/tabla_traducida.csv", index=False, encoding="utf-8")
print(len(t), "filas"); print(t.groupby(["quipu", "evidencia"]).size().to_string())
