"""Convierte las transcripciones visuales de KH0674 y KH0675 a cuerdas_*.csv
con el mismo esquema que analisis/datos/cuerdas.csv.

Regla decimal (Ascher / nota de la ficha JS01): los racimos se leen de abajo arriba.
El ultimo racimo ocupa las unidades si es largo (L) o figura de ocho (E); si es simple (S)
ocupa las decenas (los nudos simples nunca son unidades). Cada racimo anterior sube una
decena. Valor del racimo = nº de nudos * 10^lugar.
"""
import csv
import math
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPOS = ["kfg", "orden", "cuerda", "tipo", "nivel", "padre", "grupo", "valor", "alt", "nudos",
          "color", "torsion", "union", "largo", "terminacion", "notas"]

# grupos de colgantes: (desde, hasta, grupo, pos_cm, espacio_cm, seccion)
GRUPOS = {
    "KH0674": [
        (1, 11, 0, "0.0", "1.0", "A"), (12, 22, 1, "4.0", "1.0", "A"), (23, 33, 2, "7.0", "1.0", "A"),
        (34, 38, 3, "10.0", "1.0", "A"), (39, 49, 4, "12.0", "1.0", "A"), (50, 60, 5, "15.0", "1.0", "A"),
        (61, 71, 6, "18.0", "1.0", "A"), (72, 82, 7, "20.5", "1.0", "A"), (83, 93, 8, "23.5", "0.0", "A"),
        (94, 104, 9, "28.5", "1.0", "B"), (105, 109, 10, "31.5", "1.0", "B"), (110, 120, 11, "33.0", "1.0", "B"),
        (121, 131, 12, "35.5", "1.0", "B"), (132, 142, 13, "38.5", "1.0", "B"), (143, 153, 14, "41.0", "1.0", "B"),
        (154, 164, 15, "44.0", "1.5", "B"), (165, 175, 16, "47.5", "3.0", "B"), (176, 186, 17, "50.5", "1.0", "B"),
        (187, 197, 18, "55.5", "2.5", "B"), (198, 208, 19, "59.5", "2.0", "B"), (209, 219, 20, "63.0", "0.5", "B"),
        (220, 230, 21, "65.5", "2.5", "B"), (231, 241, 22, "69.0", "0.5", "B"), (242, 252, 23, "73.0", "1.0", "B"),
        (253, 263, 24, "75.5", "1.0", "B"), (264, 274, 25, "78.0", "1.0", "B"), (275, 285, 26, "80.5", "1.0", "B"),
        (286, 296, 27, "83.0", "1.5", "B"), (297, 306, 28, "86.5", "3.5", "B"), (307, 317, 29, "90.5", "1.5", "B"),
        (318, 328, 30, "94.5", "1.0", "B"), (329, 339, 31, "97.5", "1.0", "B"), (340, 350, 32, "101.0", "1.0", "B"),
        (351, 361, 33, "103.5", "1.0", "B"), (362, 372, 34, "107.0", "2.0", "B"), (373, 383, 35, "111.5", "1.0", "B"),
        (384, 394, 36, "114.0", "1.0", "B"), (395, 405, 37, "116.5", "1.0", "B"), (406, 416, 38, "119.0", "1.0", "B"),
        (417, 427, 39, "121.5", "1.0", "B"), (428, 438, 40, "124.0", "0.5", "B"),
    ],
    "KH0675": [
        (1, 6, 0, "7.0", "0.5", ""), (7, 30, 1, "8.0", "0.5", ""), (31, 48, 2, "12.0", "0.5", ""),
        (49, 67, 3, "15.0", "0.5", ""), (68, 93, 4, "18.5", "0.5", ""), (94, 99, 5, "23.0", "0.5", ""),
        (100, 111, 6, "24.5", "0.5", ""), (112, 123, 7, "26.5", "0.5", ""), (124, 180, 8, "28.5", "0.5", ""),
        (181, 203, 9, "41.0", "0.5", ""),
    ],
}

CLUSTER = re.compile(r"(\d+)\s*([A-Za-z]+)\s*\(\s*([\d.]+)\s*/\s*([A-Za-z0-9?]+)\s*\)\s*([dD])?")


def parse_nudos(s):
    s = (s or "").strip()
    if not s or s == "?":
        return [] if not s else None
    out = []
    for m in CLUSTER.finditer(s):
        out.append({"n": int(m.group(1)), "tipo": m.group(2).upper(), "pos": float(m.group(3)),
                    "dir": m.group(4).upper(), "suf": (m.group(5) or "")})
    return out if out else None


def valor_y_nudos(clusters):
    """Devuelve (valor, nudos_kfg, dudoso)."""
    if clusters is None:
        return None, "?", True
    if not clusters:
        return 0, "", False
    # lugar decimal de abajo arriba
    lugares = [0] * len(clusters)
    ult = clusters[-1]["tipo"]
    lugares[-1] = 0 if ult in ("L", "E", "EE", "LL") else 1
    for i in range(len(clusters) - 2, -1, -1):
        lugares[i] = lugares[i + 1] + 1
    partes, tot = [], 0
    for c, lug in zip(clusters, lugares):
        ap = c["n"] * (10 ** lug)
        tot += ap
        d = c["dir"] if c["dir"] in ("S", "Z", "U") else "U"
        partes.append("%d%s(%.1f,%s),%d" % (c["n"], c["tipo"], c["pos"], d, ap))
    return tot, ";".join(partes), False


def leer_transcripcion(kh):
    filas = []
    for suf in ("", "_b", "_c"):
        p = os.path.join(HERE, "transcripcion_%s%s.txt" % (kh, suf))
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8"):
            if ln.startswith("#") or "|" not in ln:
                continue
            partes = ln.rstrip("\n").split("|")
            if len(partes) < 4:
                continue
            pag, cue, spin, nud = partes[:4]
            nota = partes[4] if len(partes) > 4 else ""
            filas.append({"pag": pag, "cuerda": cue.strip(), "spin": spin.strip(),
                          "nudos_raw": nud.strip(), "nota": nota.strip()})
    # dedupe por (pagina, cuerda): la ultima version manda
    vistos = {}
    for f in filas:
        vistos[(f["pag"], f["cuerda"])] = f
    return list(vistos.values())


def orden_clave(cuerda):
    m = re.match(r"(\d+)((?:s\d+)*)$", cuerda)
    if not m:
        return (10 ** 6, ())
    subs = tuple(int(x) for x in re.findall(r"s(\d+)", m.group(2)))
    return (int(m.group(1)), subs)


def grupo_de(kh, n):
    for a, b, g, pos, esp, sec in GRUPOS[kh]:
        if a <= n <= b:
            return g
    return ""


def main():
    for kh in ("KH0674", "KH0675"):
        filas = leer_transcripcion(kh)
        expandidas = []
        for f in filas:
            cue = f["cuerda"]
            mr = re.match(r"(\d+)-(\d+)$", cue)
            if mr:
                for n in range(int(mr.group(1)), int(mr.group(2)) + 1):
                    g = dict(f)
                    g["cuerda"] = str(n)
                    expandidas.append(g)
            else:
                expandidas.append(f)
        # ordinal y filas
        expandidas.sort(key=lambda f: orden_clave(f["cuerda"]))
        out = []
        for orden, f in enumerate(expandidas):
            cue = f["cuerda"]
            m = re.match(r"(\d+)((?:s\d+)*)$", cue)
            base = m.group(1) if m else ""
            nivel = len(re.findall(r"s\d+", cue))
            padre = cue[: cue.rfind("s")] if nivel else ""
            cl = parse_nudos(f["nudos_raw"])
            val, nud, dudoso = valor_y_nudos(cl)
            nota = f["nota"]
            if dudoso:
                nota = (nota + "; NUDOS DUDOSOS").strip("; ")
            out.append({"kfg": kh, "orden": orden, "cuerda": cue, "tipo": "p", "nivel": nivel,
                        "padre": padre, "grupo": grupo_de(kh, int(base)) if base else "",
                        "valor": "" if val is None else val, "alt": "", "nudos": nud,
                        "color": "", "torsion": "", "union": "", "largo": "", "terminacion": "",
                        "notas": nota, "_pag": f["pag"]})
        dst = os.path.join(HERE, "cuerdas_%s.csv" % kh)
        with open(dst, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=CAMPOS)
            w.writeheader()
            for r in out:
                w.writerow({k: r[k] for k in CAMPOS})
        n0 = sum(1 for r in out if r["nivel"] == 0)
        con = sum(1 for r in out if isinstance(r["valor"], int) and r["valor"] > 0)
        print(kh, "filas", len(out), "colgantes", n0, "con valor>0", con,
              "suma", sum(r["valor"] for r in out if isinstance(r["valor"], int)))
        # discrepancias con valores anotados en la ficha
        for r in out:
            if "ficha:" in r["notas"]:
                print("  ficha", r["cuerda"], "calc", r["valor"], "|", r["notas"])


if __name__ == "__main__":
    main()
