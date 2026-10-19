"""Convierte KH0676 (JS01, exportacion KDB de la tesis de Julia Strauss) a cuerdas_KH0676.csv.

Regla principal (posicional, la de construir_tabla.py / Ascher):
  - los racimos se leen de arriba abajo; el ultimo ocupa las unidades si es L o E;
    si el ultimo es S, los simples ocupan las decenas (nunca unidades);
  - cada racimo anterior sube una decena; valor = nº nudos * 10^lugar.
Regla alternativa que sugiere la propia hoja ("all single knots = 10, long knots = their
value in parentheses, e-knot = 1"): suma aditiva, cada nudo simple = 10, cada largo = sus
vueltas, cada ocho = 1, sin jerarquia de posiciones. Se guarda en `alt` para comparar.
"""
import csv
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, "..", "..", "..", "data", "external", "open-khipu-repository",
                    "data", "KH0676", "JS01_Strauss_Harvard_Senior_Thesis.xlsx")
CAMPOS = ["kfg", "orden", "cuerda", "tipo", "nivel", "padre", "grupo", "valor", "alt", "nudos",
          "color", "torsion", "union", "largo", "terminacion", "notas"]
PAT = re.compile(r"(\d+)\s*([sLeE]|SP)\s*\(\s*([\d.]+)\s*/\s*([zZsS])\s*\)\s*([DU])?")


def clusters(s):
    out = []
    for m in PAT.finditer(str(s)):
        t = m.group(2)
        t = "S" if t in ("s", "SP") else ("L" if t == "L" else "E")
        out.append({"n": int(m.group(1)), "t": t, "pos": float(m.group(3)),
                    "spin": m.group(4).upper(), "dir": m.group(5) or ""})
    return out


def val_posicional(cl):
    if not cl:
        return 0, ""
    lug = [0] * len(cl)
    lug[-1] = 0 if cl[-1]["t"] in ("L", "E") else 1
    for i in range(len(cl) - 2, -1, -1):
        lug[i] = lug[i + 1] + 1
    tot, partes = 0, []
    for c, p in zip(cl, lug):
        ap = c["n"] * 10 ** p
        tot += ap
        partes.append("%d%s(%.1f,U),%d" % (c["n"], c["t"], c["pos"], ap))
    return tot, ";".join(partes)


def val_aditivo(cl):
    tot = 0
    for c in cl:
        if c["t"] == "S":
            tot += 10 * c["n"]
        elif c["t"] == "L":
            tot += c["n"]
        else:
            tot += c["n"]
    return tot


def clave(c):
    m = re.match(r"(\d+)((?:s\d+)*)$", str(c))
    if not m:
        return (999999, ())
    return (int(m.group(1)), tuple(int(x) for x in re.findall(r"s(\d+)", m.group(2))))


def main():
    d = pd.read_excel(XLSX, sheet_name="Pendant Detail", header=None, skiprows=6)
    d = d.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]]
    d.columns = ["cord", "spin", "ply", "attach", "knots", "length", "term", "color", "subs"]
    d = d[d.cord.notna()].copy()
    d["cord"] = d.cord.astype(str).str.strip()
    d = d.sort_values("cord", key=lambda s: s.map(clave))
    out = []
    for orden, (_, r) in enumerate(d.iterrows()):
        cue = r.cord
        nivel = len(re.findall(r"s\d+", cue))
        padre = cue[: cue.rfind("s")] if nivel else ""
        cl = clusters(r.knots)
        vpos, nud_pos = val_posicional(cl)
        # Regla primaria: la que declara la propia hoja (simples=10, largos=vueltas, ochos=1).
        # La variante jerarquica se guarda en `alt`; produce valores de hasta 6 cifras
        # (max 314.120) porque casi todas las cuerdas tienen 3+ racimos.
        v, nud = val_aditivo(cl), nud_pos
        va = vpos
        nota = []
        if "SP" in str(r.knots):
            nota.append("tipo SP tratado como S")
        if len(cl) >= 3:
            nota.append("3+ racimos: regla de la hoja (simples=10); la jerarquica daria %d" % va)
        if len(cl) >= 2 and sum(1 for c in cl if c["t"] == "S") >= 2:
            nota.append("varios racimos S: hoja=%d, jerarquica=%d" % (v, va))
        out.append({"kfg": "KH0676", "orden": orden, "cuerda": cue, "tipo": "p", "nivel": nivel,
                    "padre": padre, "grupo": "", "valor": v, "alt": va, "nudos": nud,
                    "color": r.color if isinstance(r.color, str) else "",
                    "torsion": (str(r.spin) + "/" + str(r.ply)) if isinstance(r.spin, str) else "",
                    "union": str(r.attach) if isinstance(r.attach, str) else "",
                    "largo": r.length if pd.notna(r.length) else "",
                    "terminacion": r.term if isinstance(r.term, str) else "",
                    "notas": "; ".join(nota)})
    dst = os.path.join(HERE, "cuerdas_KH0676.csv")
    with open(dst, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(out)
    print("filas", len(out), "suma posicional", sum(x["valor"] for x in out),
          "suma aditiva", sum(x["alt"] for x in out))
    print("con 3+ racimos", sum(1 for x in out if x["nudos"].count(";") >= 2))
    print(d.head(10)[["cord", "knots"]].to_string(max_colwidth=60))


if __name__ == "__main__":
    main()
