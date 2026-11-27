#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae a CSV estructurado las notas y correcciones de Karen M. Thompson (Nov 2025,
DOI: 10.26188/30526775) usando coordenadas X/Y exactas de las 3 columnas del PDF:
  Col 0 (KHIPU): x0 < 120
  Col 1 (Information): 120 <= x0 < 295
  Col 2 (Comment / Revision): x0 >= 295
Salida: analisis/36_corpus_maestro/thompson_2025_correcciones.csv
"""
import csv
import re
from collections import Counter
from pathlib import Path
import fitz

RAIZ_QUIPUS = Path(__file__).resolve().parents[2]
PDF_PATH = RAIZ_QUIPUS.parent / "quipu" / "papers" / "2025_Thompson_ascher-corrections.pdf"
OUT_CSV = Path(__file__).resolve().parent / "thompson_2025_correcciones.csv"

CORD_RE = re.compile(r"\b([pt]\d+(?:s\d+)*)\b", re.I)
AS_RE = re.compile(r"^(AS\d{3}[A-Z]?)\b")
PROPOSE_VAL_RE = re.compile(
    r"(?:Propose\s+(?:this\s+could\s+be[^=]{0,30})?value\s*=\s*|should\s+be\s+value\s*=\s*|value\s+should\s+be\s+)(\d+(?:\s*\+\s*\d+)*)",
    re.I,
)
ORIG_VAL_RE = re.compile(r"value\s*=\s*(\d+(?:\s*\+\s*\d+)*|\?)", re.I)

def fix_pdf_ligatures(s: str) -> str:
    # El PDF de Thompson usa una fuente donde ciertas ligaduras se extraen como símbolos
    # Solo limpiamos espacios múltiples y caracteres de control para no alterar códigos.
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def classify_revision(info: str, rev: str) -> str:
    lo = (info + " " + rev).lower()
    if "turn around" in lo or "ordering of the cords" in lo or "reverse order" in lo:
        return "orientacion_orden"
    if "inconsistent with knot" in lo or "propose value" in lo or "propose this could be" in lo or "value=" in lo or "value =" in lo:
        return "valor_o_nudo"
    if "museum" in lo or "inventory" in lo or "va" in lo or "number" in lo:
        return "identificador_museo"
    if "group of" in lo or "cluster" in lo or "cm:" in lo or "count to" in lo:
        return "agrupacion_o_posicion"
    if "color" in lo or "colour" in lo or "thread" in lo:
        return "color_o_hilo"
    if "note " in lo or "total value" in lo or "sum" in lo:
        return "nota_o_suma"
    if "subsidiary" in lo or "attachment" in lo or "termina" in lo or "broken" in lo:
        return "estructura_cuerda"
    return "otra"

def main():
    assert PDF_PATH.exists(), f"No se encontró {PDF_PATH}"
    doc = fitz.open(PDF_PATH)

    # Extraer líneas horizontales (bordes de fila de tabla) o agrupar por líneas de texto (y)
    all_entries = []
    cur_khipu = ""

    for pno in range(1, len(doc)):
        page = doc[pno]
        # Obtener líneas dibujadas horizontales que separan filas de tabla
        drawings = page.get_drawings()
        hlines = sorted(set(
            round(d["rect"].y0, 1)
            for d in drawings
            if abs(d["rect"].y1 - d["rect"].y0) < 2.0 and (d["rect"].x1 - d["rect"].x0) > 200 and 60 < d["rect"].y0 < 785
        ))

        words = page.get_text("words")
        # Filtrar encabezados y pies de página
        words = [w for w in words if 65 < w[1] < 785]
        if not words:
            continue

        # Si hay líneas horizontales de tabla, usar bandas entre ellas; si no, agrupar por salto vertical
        if len(hlines) >= 2:
            bands = [(hlines[i], hlines[i + 1]) for i in range(len(hlines) - 1)]
        else:
            # Fallback: agrupar por y con salto > 16 pt en col 0 o col 1
            bands = [(65.0, 785.0)]

        for y_top, y_bot in bands:
            bw = [w for w in words if (y_top - 1.5) <= w[1] < (y_bot - 1.0)]
            if not bw:
                continue
            col0 = sorted([w for w in bw if w[0] < 120], key=lambda w: (round(w[1], 1), w[0]))
            col1 = sorted([w for w in bw if 120 <= w[0] < 298], key=lambda w: (round(w[1], 1), w[0]))
            col2 = sorted([w for w in bw if w[0] >= 298], key=lambda w: (round(w[1], 1), w[0]))

            t0 = fix_pdf_ligatures(" ".join(w[4] for w in col0))
            t1 = fix_pdf_ligatures(" ".join(w[4] for w in col1))
            t2 = fix_pdf_ligatures(" ".join(w[4] for w in col2))

            if t0.upper().startswith("KHIPU") and ("INFORMA" in t1.upper() or "COMMENT" in t2.upper()):
                continue
            if not t0 and not t1 and not t2:
                continue

            m_as = AS_RE.match(t0)
            if m_as:
                cur_khipu = m_as.group(1)
            elif not cur_khipu:
                continue

            # Si t0 está vacío y t1 está vacío pero t2 tiene texto, es continuación de fila previa
            if not t0 and not t1 and t2 and all_entries and all_entries[-1]["as_id"] == cur_khipu:
                all_entries[-1]["revision"] = (all_entries[-1]["revision"] + " " + t2).strip()
                continue

            all_entries.append({
                "pagina": pno + 1,
                "as_id": cur_khipu,
                "info": t1,
                "revision": t2,
            })

    rows = []
    for e in all_entries:
        c1, c2 = e["info"], e["revision"]
        cords = sorted(set(m.lower() for m in CORD_RE.findall(c1)))
        m_orig = ORIG_VAL_RE.search(c1)
        m_prop = PROPOSE_VAL_RE.search(c2)
        orig_val = m_orig.group(1) if m_orig else ""
        prop_val = m_prop.group(1).replace(" ", "") if m_prop else ""
        prop_num = ""
        if prop_val:
            if "+" in prop_val:
                prop_num = str(sum(int(x) for x in prop_val.split("+")))
            elif prop_val.isdigit():
                prop_num = prop_val
        rows.append({
            "pagina": e["pagina"],
            "as_id": e["as_id"],
            "cuerdas_citadas": ";".join(cords),
            "n_cuerdas": len(cords),
            "tipo": classify_revision(c1, c2),
            "valor_orig": orig_val,
            "valor_propuesto_raw": prop_val,
            "valor_propuesto": prop_num,
            "info": c1,
            "revision": c2,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "pagina", "as_id", "cuerdas_citadas", "n_cuerdas", "tipo",
            "valor_orig", "valor_propuesto_raw", "valor_propuesto", "info", "revision"
        ])
        w.writeheader()
        w.writerows(rows)

    as_set = sorted(set(r["as_id"] for r in rows))
    n_val_patch = sum(1 for r in rows if r["valor_propuesto"] and r["n_cuerdas"] == 1)
    print(f"Extraídas {len(rows)} filas de Thompson (2025a) en {len(as_set)} quipus AS.")
    print(f"Parches deterministas de valor en 1 cuerda: {n_val_patch}")
    print("Por tipo:", dict(Counter(r["tipo"] for r in rows)))
    print("Muestra 5 parches de valor:")
    for r in [x for x in rows if x["valor_propuesto"] and x["n_cuerdas"] == 1][:5]:
        print(" ", r["as_id"], r["cuerdas_citadas"], f"{r['valor_orig']} -> {r['valor_propuesto']}", "|", r["revision"][:80])

if __name__ == "__main__":
    main()
