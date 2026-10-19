"""01_parse_tabla.py — Extrae la tabla reconstructiva del quipu wanka (Murra 2024, pp. 38-43)
del texto OCR a una lista ordenada de valores por (clúster, evento).

LIMITACIÓN CLAVE: el OCR pierde las coordenadas de columna. Por eso NO asignamos
valor->columna: guardamos la SECUENCIA de valores de cada fila (invariante conocida)
y el número de celdas con dato. Las magnitudes por grupo (suma de la fila) sí son
invariantes a la asignación.
"""
import re, json, csv, unicodedata, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC = r"../../fuentes_txt/Murra2024_EthnoCategories.txt"

# páginas del cuadro en la versión inglesa y clústeres que contiene
PAGINAS = {
    38: [("I", 1, 5), ("II", 1, 5)],          # se resuelve abajo por columnas
}

# columnas por página (números de cuerda impresos en el encabezado)
COLS = {
    38: [1, 2, 3, 4, 5],
    39: list(range(6, 15)),
    40: list(range(15, 25)),
    41: list(range(25, 33)),
    42: list(range(33, 39)),
    43: list(range(39, 44)),
}
# clúster (grupo de cuerdas) al que pertenece cada columna
CLUSTER = {
    1: "I", 2: "I", 3: "II", 4: "II", 5: "II",
    6: "III", 7: "III", 8: "III", 9: "IV", 10: "IV", 11: "IV",
    12: "IV", 13: "IV", 14: "IV",
    15: "V", 16: "V", 17: "V", 18: "V", 19: "V", 20: "V",
    21: "VI", 22: "VI", 23: "VI", 24: "VI",
    25: "VII", 26: "VII", 27: "VII",
    28: "VIII", 29: "VIII", 30: "VIII", 31: "VIII", 32: "VIII",
    33: "IX", 34: "IX", 35: "IX", 36: "IX",
    37: "X", 38: "X",
    39: "XI", 40: "XI", 41: "XII", 42: "XII", 43: "XII",
}

ETIQUETAS = ["a", "b", "c", "ch", "d", "e", "f", "g", "h", "i", "j", "k",
             "l", "ll", "m", "n", "o", "p", "q"]

def limpia(s):
    return unicodedata.normalize("NFKC", s).replace("\u00a0", " ").strip()

def num(tok):
    """convierte '1,2045' (typo OCR) o '12,406' o '188½' a float"""
    t = tok.replace("*", "").replace("†", "").strip()
    t = t.replace("½", ".5")
    t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None

def main():
    txt = open(SRC, encoding="utf-8", errors="replace").read()
    # dividir por páginas
    partes = re.split(r"=== p(\d+) ===", txt)
    paginas = {}
    for i in range(1, len(partes), 2):
        paginas[int(partes[i])] = partes[i + 1]

    filas = []          # (pagina, col_ini, col_fin, evento, texto_celdas, valores)
    for pg in COLS:
        body = paginas[pg]
        lines = [limpia(l) for l in body.split("\n")]
        # recortar el encabezado: hasta la línea del primer evento "a)"
        try:
            i0 = lines.index("a)")
        except ValueError:
            # p38: la etiqueta puede venir con texto
            i0 = next(i for i, l in enumerate(lines) if re.match(r"^a\)", l))
        # recorrer filas
        actual, desc, vals, raws = None, [], [], []
        def cierra():
            if actual is not None:
                filas.append(dict(pagina=pg, evento=actual, desc=" ".join(desc),
                                  valores=vals[:], crudos=raws[:]))
        for l in lines[i0:]:
            m = re.match(r"^(ch|ll|[a-q])\)\s*(.*)$", l)
            if m:
                cierra()
                actual, desc, vals, raws = m.group(1), [m.group(2)] if m.group(2) else [], [], []
                continue
            if actual is None:
                continue
            if not l:
                continue
            # ¿línea con números?
            toks = re.findall(r"(?:\*|†)?\s*[\d][\d,\.]*\s*½?|\d+½", l)
            resto = re.sub(r"(?:\*|†)?\s*[\d][\d,\.]*\s*½?|\d+½", "", l).strip(" .;:")
            if toks and not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]{3,}", resto):
                for t in toks:
                    v = num(t)
                    if v is not None:
                        vals.append(v); raws.append(l)
            elif toks and re.search(r"[A-Za-z]{3,}", resto):
                # celda con número + palabra ("132 rams", "Azua 2,424", "354 measures")
                for t in toks:
                    v = num(t)
                    if v is not None:
                        vals.append(v); raws.append(l)
            else:
                desc.append(l)
        cierra()

    # asignar cada fila de página a su(s) clúster(es) según nº de columnas
    out = []
    for f in filas:
        cols = COLS[f["pagina"]]
        grupos = []
        for c in cols:
            if CLUSTER[c] not in grupos:
                grupos.append(CLUSTER[c])
        # separar años (1533-1548) de las cantidades
        anios = [v for v in f["valores"] if 1500 <= v <= 1600]
        f["valores"] = [v for v in f["valores"] if not (1500 <= v <= 1600)]
        f["anio"] = int(anios[0]) if anios else None
        f["clusters"] = grupos
        f["n_cols"] = len(cols)
        f["n_vals"] = len(f["valores"])
        out.append(f)

    with open("wanka_celdas.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["pagina", "clusteres", "n_columnas", "evento", "anio", "descripcion",
                    "n_valores", "valores", "crudos"])
        for f in out:
            w.writerow([f["pagina"], "+".join(f["clusters"]), f["n_cols"], f["evento"],
                        f["anio"], f["desc"], f["n_vals"],
                        ";".join(f"{v:g}" for v in f["valores"]),
                        " | ".join(f["crudos"])])

    # resumen por página
    print("pág  clusters   cols  eventos  valores  completos")
    import collections
    for pg in COLS:
        ff = [f for f in out if f["pagina"] == pg]
        nv = sum(f["n_vals"] for f in ff)
        comp = sum(1 for f in ff if f["n_vals"] == f["n_cols"])
        print(f"{pg:4d}  {'+'.join(ff[0]['clusters']):9s}  {len(COLS[pg]):4d}  {len(ff):7d}  {nv:7d}  {comp:9d}")
    print("TOTAL valores:", sum(f["n_vals"] for f in out), " celdas máximas:", 19 * 43)

if __name__ == "__main__":
    main()
