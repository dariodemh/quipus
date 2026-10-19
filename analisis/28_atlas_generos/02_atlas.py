# -*- coding: utf-8 -*-
"""Paso 2-4. Aplica las reglas, redacta evidencia y una prediccion comprobable por quipu,
y calcula la cobertura. Salidas: atlas.csv, cobertura.csv, resumen_generos.csv."""
import re
import numpy as np, pandas as pd
import reglas as RG

A_ = r"./analisis"
OUT = A_ + r"\28_atlas_generos"
M = pd.read_csv(OUT + r"\matriz.csv", index_col=0)
C = pd.read_csv(A_ + r"\datos\cuerdas.csv")
FD = pd.read_csv(A_ + r"\22_formularios\quipus_detector.csv").set_index("kfg")
NZ = pd.read_csv(A_ + r"\ds\n_ficha_nazca\barrido_corpus.csv").set_index("khipu")
A = RG.clasificar(M)

# ---- datos concretos por quipu para las predicciones ----
def ejemplo_suma(d):
    """Primer grupo donde un colgante extremo = suma de los demas colgantes anudados (>=2, total>=10)."""
    d = d[(d.nivel == 0)]
    for gr, x in d.groupby("grupo"):
        v = x.sort_values("orden")
        vals = v.valor.fillna(0).values
        pos = vals[vals > 0]
        if len(pos) < 3:
            continue
        for i in (0, len(vals) - 1):
            resto = np.delete(vals, i)
            if vals[i] >= 10 and vals[i] == resto[resto > 0].sum() and (resto > 0).sum() >= 2:
                return f"grupo {gr}: {v.cuerda.iloc[i]} = {int(vals[i])} = suma de {(resto > 0).sum()} colgantes"
    return None

def modal(d):
    v = d[(d.valor >= 10)].valor
    if v.empty:
        return None
    m = v.value_counts()
    return int(m.index[0]), int(m.iloc[0])

ext = {}
for k, d in C.groupby("kfg"):
    ext[k] = dict(suma=ejemplo_suma(d), modal=modal(d),
                  ng=d[d.nivel == 0].grupo.nunique(),
                  tam=int(d[d.nivel == 0].groupby("grupo").size().mode().iloc[0]) if (d.nivel == 0).any() else 0)

def pred(k, g):
    r, e = M.loc[k], ext.get(k, {})
    if g == "CAL":
        return ("En el objeto: conjuntos pareados de [20-22 colgantes] + [8-10 de lazo] (~30) cuyo total ronda 730 (2x365); "
                "UR009/UR021 repiten la secuencia. Refuta: si el total de cuerdas por par no se agrupa en ~30.")
    if g == "NAZ":
        s = int(NZ.loc[k, "size"]) if k in NZ.index else 9
        return (f"Registros de {s} cuerdas = {s-2} campos + 2 marcadoras; el campo 1 es el maximo en >=90 % de los registros "
                "y las 2 marcadoras tienen color distinto de sus vecinas en el objeto (verificable en foto). Ningun campo suma a otros.")
    if g == "ARC":
        if k.startswith("UR06") or k in ("UR073", "UR078"):
            return ("Sus secciones suman, columna a columna, las del quipu de nivel superior (UR068->UR067; UR063->UR068), "
                    "con discrepancias de lectura de +-4 como 2904/2908. Una nueva lectura del objeto debe conservarlas.")
        return ("Sus totales reaparecen, en orden, como cabeceras de UR266/UR275/UR269; cuota fija restada c (47, 25, 15, 10). "
                "Prediccion abierta (13): en los 5 quipus de Inkawasi no estudiados por Urton habra parejas con cuotas que sumen 46 o 44.")
    if g == "PAD":
        if r.procedencia == "Santa":
            return (f"{e.get('ng', '?')} grupos de ~{e.get('tam', '?')} cuerdas monocromos y de color alterno. Los 6 quipus del Santa "
                    "suman 133 grupos frente a 130-132 tributarios del padron de 1670 (Medrano y Urton 2018): con el folio original, "
                    "cada grupo debe corresponder a un tributario con la misma cuota (hoy el orden no se demuestra, p=0,18).")
        return (f"{e.get('ng', '?')} grupos de ~{e.get('tam', '?')} cuerdas monocromos y de color alterno, valores pequenos (1-7); "
                "si es padron, un documento del mismo pueblo tendra tantos tributarios como grupos. Debil: P4r no pasa Holm fuera del Santa.")
    if g == "FOR":
        f = FD.loc[k] if k in FD.index else None
        clave = f.claveC if f is not None and isinstance(f.claveC, str) else (f.claveP if f is not None else "")
        cuo = f.cuotas if f is not None and isinstance(f.cuotas, str) else ""
        return (f"Los bloques repiten la clave {clave} (etiquetas del transcriptor; lo comprobable es la particion) con reparto ~{cuo}; otro quipu del mismo archivo (museo consecutivo, "
                "mismo transcriptor) repetira esas proporciones (+-0,05) aunque su escala cambie; la parte mayor va primero o en blanco.")
    if g == "TAL":
        fib = ("fibra de camelido" if pd.isna(r.okr_frac_camelido) else
               f"fibra camelida {r.okr_frac_camelido:.0%} registrada")
        return (f"En el objeto: cuerdas de torsion Z ({'' if pd.isna(r.frac_Z) else f'{r.frac_Z:.0%} en KFG; '}"
                f"{fib} si se analiza) y nudos largos de muchas vueltas en racimos que no siguen lugares decimales; "
                "ninguna cuerda es suma de otras. Lectura esperada: cuentas aditivas por categoria/animal (pastores, Mackey).")
    if g == "NON":
        return ("En foto: cuerdas sin nudos o con nudos no axiales/hilos atados, color o enrollados como unica informacion; "
                "una retranscripcion no hallara valores decimales. Si es de Cajamarquilla, los 3 quipus comparten la morfologia.")
    if g == "SUM":
        ej = e.get("suma")
        return ((f"Comprobable ya en el objeto: {ej}. " if ej else "Totales de grupo adyacentes a sus partes. ") +
                "Un documento equivalente declarara totales (antes o despues de la lista, como la encomienda de Aldana) "
                "que deben salir exactos al sumar las partidas.")
    if g == "ASG":
        m = e.get("modal")
        return ((f"Cifra modal {m[0]} repetida {m[1]} veces; " if m else "") +
                f"{r.red_frac:.0%} de las cifras intactas >=10 son multiplos de 10 (esperado 10 % en un recuento). "
                "Un documento de tasa del mismo valle daria cuotas redondas iguales por pueblo y sin filas co-crecientes.")
    if g == "TAB":
        return (f"Tabla de {int(r.tabla_R)} filas x {int(r.tabla_K)} columnas: la 1.a columna sera la mayor y una fila grande lo sera "
                "en todas las columnas; el total de fila NO estara en el quipu (se calculaba fuera). Analogo: visita con pueblos x rubros.")
    if g == "SEG":
        return (f"{e.get('ng', '?')} grupos; los cambios de color y las marcadoras caen en fronteras de grupo (verificable en foto) "
                "y los bloques repiten el mismo orden de rubros; no se espera aritmetica entre bloques.")
    if A.loc[k, "ev"] == "datos insuficientes":
        return (f"Sin genero por calidad: {r.frac_rota:.0%} cuerdas rotas, {r.n_cuerdas*r.frac_anudada:.0f} anudadas. "
                "Prediccion: una retranscripcion o foto no cambiara su clase hasta recuperar >=30 cuerdas anudadas.")
    return ("Decimal sin estructura detectada: sumas al nivel del azar, cifras no redondas, color sin particion por grupo. "
            "Refuta: un detector congelado que encienda en una retranscripcion independiente.")

A["prediccion"] = [pred(k, g) for k, g in A.genero.items()]
A["evidencia"] = A.ev + np.where(A.secundarios != "", " | tambien: " + A.secundarios, "") + \
    " | calidad: " + M.n_cuerdas.astype(int).astype(str) + " cuerdas, " + (M.frac_rota * 100).round(0).astype(int).astype(str) + \
    "% rotas, transcriptor " + M.transcriptor.astype(str)
atlas = M[["okr", "procedencia", "museo"]].join(A[["genero", "confianza", "evidencia", "prediccion", "lineas", "secundarios"]])
atlas.insert(4, "genero_nombre", atlas.genero.map(RG.NOMBRE))
try:  # estabilidad de 03_controles.py (orden de ejecucion: 01, 03, 02)
    atlas["estabilidad"] = pd.read_csv(OUT + r"\estabilidad.csv", index_col=0)["ambos"].round(2)
except FileNotFoundError:
    pass
atlas.reset_index().to_csv(OUT + r"\atlas.csv", index=False)

# ---- cobertura ----
cob = A.confianza.value_counts().reindex(["alta", "media", "baja", "sin genero"]).fillna(0).astype(int)
cobt = pd.DataFrame({"n": cob, "frac": (cob / len(A)).round(3)})
# cobertura ponderada por cuerdas (cuanto del material entendemos)
w = M.n_cuerdas
cobt["frac_cuerdas"] = [round(w[A.confianza == c].sum() / w.sum(), 3) for c in cobt.index]
cobt.to_csv(OUT + r"\cobertura.csv")
print("COBERTURA\n", cobt.to_string())
print("sin genero por motivo:", A[A.genero == "SIN"].ev.value_counts().to_dict())

# ---- resumen por genero ----
res = []
for g in RG.ORDEN + ["SIN"]:
    s = A[A.genero == g]
    if s.empty:
        continue
    pr = M.loc[s.index, "procedencia"].value_counts()
    mu = M.loc[s.index, "museo"].str.slice(0, 30).value_counts()
    tr = M.loc[s.index, "transcriptor"].value_counts()
    res.append(dict(genero=g, nombre=RG.NOMBRE[g], n=len(s), alta=(s.nivel == 3).sum(), media=(s.nivel == 2).sum(),
                    baja=(s.nivel == 1).sum(), lineas_med=s.lineas.median(),
                    procedencias="; ".join(f"{a} {b}" for a, b in pr.head(6).items()),
                    museos="; ".join(f"{a} {b}" for a, b in mu.head(3).items()),
                    transcriptores="; ".join(f"{a} {b}" for a, b in tr.items()),
                    quipus=" ".join(s.sort_values("nivel", ascending=False).index[:40])))
R = pd.DataFrame(res)
R.to_csv(OUT + r"\resumen_generos.csv", index=False)
print(R[["genero", "n", "alta", "media", "baja", "lineas_med", "procedencias"]].to_string())

# solapes: cuantos quipus tienen >1 genero candidato
nsec = (A.secundarios != "").sum()
print(f"quipus con generos secundarios: {nsec} de {(A.genero != 'SIN').sum()} asignados")
