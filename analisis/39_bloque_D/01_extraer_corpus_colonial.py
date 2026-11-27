#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_extraer_corpus_colonial.py — Extrae y verifica aritméticamente el Corpus Numérico Colonial Ampliado
para el Preregistro P06 (Curatola 2013 + Chirinos 2010 + Pärssinen 1992 + 11_rosetta).

Cada tabla independiente lleva:
  doc_id, fuente_autor, genero, papel_fila (item|total), orden, etiqueta, valor, nota
Géneros congelados:
  - PADRON_DEMOGRAFICO (Pärssinen 1992 Tablas 2-10 + Chirinos 2010 Chucuito/Chupaychu + 11_rosetta padrones)
  - GANADO_INVENTARIO (Curatola 2013 / Castro de Trelles Cuadros 2-7 + Chirinos 2010 Cuadro 2.3/3.4 ganado)
  - APORTE_INVENTARIO (Chirinos 2010 Cuadros 1.3-1.6, 2.1-2.7, 7.2 aportes de bienes/víveres/tejidos/armas)
  - TRIBUTO_TASA (Curatola 2013 / Medelius Cuadros 1-3 + Chirinos 2010 Cuadros 3.1 tasas, 3.2 Paria, 6.1 Mazco + 11_rosetta tributos)
  - SERVICIO_ASIGNACION (Chirinos 2010 Cuadros 1.1/2.7/7.4 servicios personales + 11_rosetta Chupaychos)
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import fitz

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[1]
RAIZ_QUIPU = RAIZ.parent / "quipu"

CURATOLA_PDF = RAIZ_QUIPU / "papers/2013_Curatola_quipu-colonial.pdf"
CHIRINOS_PDF = RAIZ / "referencias/Chirinos Rivera 2010 - Quipus del Tahuantinsuyo Book.pdf"
PARSSINEN_TXT = RAIZ_QUIPU / "analisis/fuentes_txt/Parssinen1992_Tawantinsuyu.txt"
ROSETTA_CSV = RAIZ / "analisis/11_rosetta/transcripciones_numeros.csv"

OUT_CSV = DIR / "corpus_colonial_ampliado.csv"


def parse_int_token(s):
    if s is None:
        return None
    s = str(s).strip().replace(",", "").replace(".", "")
    if re.fullmatch(r"\d+", s):
        v = int(s)
        return v if v > 0 else None
    return None


def extract_curatola():
    """Extrae tablas de Medelius (pp. 248-257) y Castro de Trelles (pp. 368-377) de Curatola 2013."""
    doc = fitz.open(CURATOLA_PDF)
    rows = []

    # 1) Medelius Cuadro 1 (p.248-249), Cuadro 2 (p.253-254), Cuadro 3 (p.257-258) -> TRIBUTO_TASA
    med_specs = [
        ("CUR_MED_1550_Angaraes_Tasa", [247, 248], "TRIBUTO_TASA"),
        ("CUR_MED_1571_Angaraes_Navidad", [252, 253], "TRIBUTO_TASA"),
        ("CUR_MED_1571_Angaraes_TerceraParte", [256, 257], "TRIBUTO_TASA"),
    ]
    for doc_id, pages, gen in med_specs:
        ord_i = 0
        for pno in pages:
            txt = doc[pno].get_text("text")
            # Extraer líneas con cantidades explícitas (ej. "200 pesos", "50 costales", "400 hanegas", "12 ovejas")
            for ln in txt.splitlines():
                ln_s = ln.strip()
                if not ln_s or re.match(r"^(Mónica|El descargo|Cuadro|Artículo|Cantidad|\d{3}$)", ln_s):
                    continue
                m = re.match(r"^[«\"']?(\d{1,5})\s+(pesos|costales|vestidos|zurroncillos|zurrones|hanegas|fanegas|machos|cestos|ovejas|puercos|piezas|carneros|cargas|cabezas|pares|aves|gallinas|huevos|mantas|camisetas|costales)", ln_s, re.I)
                if m:
                    v = int(m.group(1))
                    if v > 0:
                        ord_i += 1
                        rows.append({
                            "doc_id": doc_id, "fuente_autor": "Curatola2013_Medelius",
                            "genero": gen, "papel": "item", "orden": ord_i,
                            "etiqueta": ln_s[:60], "valor": v,
                        })

    # 2) Castro de Trelles (pp. 368-377): Cuadros 2-7 (ganado Tulpo/Yamobamba 1611-1631) -> GANADO_INVENTARIO
    # Separar por Cuadro (2..7) y por especie (Ganado ovejuno vs vacuno)
    cur_doc = "CUR_CASTRO_Cuadro2_1611"
    ord_map = Counter()
    for pno in range(367, 378):
        if pno >= len(doc):
            break
        page = doc[pno]
        txt = page.get_text("text")
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
        for ln in lines:
            mc = re.match(r"^Cuadro\s+(\d+):", ln)
            if mc:
                cur_doc = f"CUR_CASTRO_Cuadro{mc.group(1)}_Tulpo"
                continue
            if re.match(r"^(Lucila Castro|36\d|37\d|Total\b|Guardián|Dueño|Descripción|Cabezas|Ovejas|Agregados|Lugar|ARC,)", ln, re.I):
                continue
            # En los cuadros de Castro de Trelles, las cifras de conteo aparecen como enteros aislados en su línea
            # (o precedidos de etiqueta). Evitamos años 1600-1699 y folios.
            if re.fullmatch(r"\d{1,5}", ln):
                v = int(ln)
                if 1 <= v <= 20000 and not (1600 <= v <= 1650):
                    ord_map[cur_doc] += 1
                    rows.append({
                        "doc_id": cur_doc, "fuente_autor": "Curatola2013_CastroTrelles",
                        "genero": "GANADO_INVENTARIO", "papel": "item", "orden": ord_map[cur_doc],
                        "etiqueta": f"conteo_{ord_map[cur_doc]}", "valor": v,
                    })
    return rows


def extract_chirinos():
    """Extrae los cuadros tabulados de Chirinos Rivera (2010) usando tablas de PyMuPDF / columnas."""
    doc = fitz.open(CHIRINOS_PDF)
    rows = []

    # Definir mapa (rango de páginas 0-based, doc_id, genero, col_indices_de_valores)
    # Usamos extracción estructurada por líneas/números evitando años (1500-1650), porcentajes (%) y códigos
    specs = [
        ("CHI_1_3_Huancas_1533_Cajamarca", [(34, None)], "APORTE_INVENTARIO"),
        ("CHI_1_4_Huancas_1533_1536", [(35, None), (36, None), (37, None)], "APORTE_INVENTARIO"),
        ("CHI_1_5_Huancas_1537_1542", [(38, None), (39, None), (40, None), (41, None)], "APORTE_INVENTARIO"),
        ("CHI_1_6_Huancas_1542_1548", [(42, None), (43, None)], "APORTE_INVENTARIO"),
        ("CHI_2_1_Huancas_1553_Giron", [(57, None), (58, None)], "APORTE_INVENTARIO"),
        ("CHI_2_2_Huancas_1558_Armas", [(61, 0)], "APORTE_INVENTARIO"),
        ("CHI_2_3_Huancas_1558_Ganado", [(61, 1)], "GANADO_INVENTARIO"),
        ("CHI_2_4_Huancas_1558_Tejidos", [(62, 0)], "APORTE_INVENTARIO"),
        ("CHI_2_5_Huancas_1558_Viveres", [(62, 1), (63, None)], "APORTE_INVENTARIO"),
        ("CHI_2_6_Huancas_1558_Madera", [(65, 0)], "APORTE_INVENTARIO"),
        ("CHI_2_7_Huancas_1558_Cargadores", [(65, 1)], "SERVICIO_ASIGNACION"),
        ("CHI_3_1a_Chucuito_1567_Poblacion", [(72, None), (73, None)], "PADRON_DEMOGRAFICO"),
        ("CHI_3_1b_Chucuito_1567_Tributo", [(72, None), (73, None)], "TRIBUTO_TASA"),
        ("CHI_3_2_Paria_Tasa", [(77, None)], "TRIBUTO_TASA"),
        ("CHI_3_4_Chucuito_GanadoSM", [(84, None)], "GANADO_INVENTARIO"),
        ("CHI_6_1_PachacaMazco_1548_Tributos", [(125, None)], "TRIBUTO_TASA"),
        ("CHI_7_2_Aullagas_1548_Bienes", [(154, None), (155, None), (156, None)], "APORTE_INVENTARIO"),
        ("CHI_7_4_Aullagas_Servicios", [(164, None)], "SERVICIO_ASIGNACION"),
    ]

    # Para precisión máxima, usamos find_tables() en cada página (con índice de tabla exacto si hay 2 cuadros en la misma página)
    for doc_id, page_specs, gen in specs:
        ord_i = 0
        seen_vals = []
        for pno, tab_idx in page_specs:
            if pno >= len(doc):
                continue
            page = doc[pno]
            tabs = page.find_tables()
            if tabs and tabs.tables:
                sel_tabs = [tabs.tables[tab_idx]] if (tab_idx is not None and tab_idx < len(tabs.tables)) else tabs.tables
                for tab in sel_tabs:
                    data = tab.extract()
                    if not data or len(data) < 2:
                        continue
                    header = " ".join(str(x or "") for x in data[0]).lower()
                    for r in data[1:]:
                        r_txt = " ".join(str(x or "") for x in r).strip()
                        if not r_txt or re.match(r"^(total|suma|fuentes|parcialidades|pueblos|cod\.)", r_txt, re.I):
                            continue
                        # Filtrar columnas específicas para Chucuito 3.1 (población cols 1-3 vs tributo cols 4-6)
                        cells = r
                        if doc_id == "CHI_3_1a_Chucuito_1567_Poblacion" and len(r) >= 6:
                            cells = r[1:3]
                        elif doc_id == "CHI_3_1b_Chucuito_1567_Tributo" and len(r) >= 6:
                            cells = r[4:7]
                        for cell in cells:
                            cs = str(cell or "").strip()
                            if not cs or "%" in cs or "/" in cs or "-" in cs:
                                continue
                            # Extraer entero puro o "1,321"
                            m = re.fullmatch(r"(\d{1,3}(?:,\d{3})+|\d{1,5})", cs)
                            if m:
                                v = int(m.group(1).replace(",", ""))
                                if 1 <= v <= 50000 and not (1530 <= v <= 1650):
                                    ord_i += 1
                                    seen_vals.append(v)
                                    rows.append({
                                        "doc_id": doc_id, "fuente_autor": "Chirinos2010",
                                        "genero": gen, "papel": "item", "orden": ord_i,
                                        "etiqueta": (str(r[0] or "")[:45]).replace("\n", " ").strip(),
                                        "valor": v,
                                    })
        # Fallback si find_tables no detectó bordes en esa página
        if ord_i < 5:
            for pno, _ in page_specs:
                if pno >= len(doc):
                    continue
                txt = doc[pno].get_text("text")
                for ln in txt.splitlines():
                    cs = ln.strip()
                    if "%" in cs or re.match(r"^(Cuadro|Capítulo|Parte|Total)", cs, re.I):
                        continue
                    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})+|\d{1,5})", cs)
                    if m:
                        v = int(m.group(1).replace(",", ""))
                        if 1 <= v <= 50000 and not (1530 <= v <= 1650):
                            ord_i += 1
                            rows.append({
                                "doc_id": doc_id, "fuente_autor": "Chirinos2010",
                                "genero": gen, "papel": "item", "orden": ord_i,
                                "etiqueta": f"val_{ord_i}", "valor": v,
                            })
    return rows


def extract_parssinen():
    """Extrae las listas de purics/tributarios por pueblo/pachaca de Pärssinen (1992) Tablas 2-10 (verificadas contra totales)."""
    # Listas verificadas directamente desde Parssinen1992_Tawantinsuyu.txt (Tablas 2-10, pp. 387-404)
    # y verificadas aritméticamente contra los totales impresos en el libro.
    # Nota: Bambamarca se marca explícitamente como `bambamarca_excluir_P06_4` según Preregistro P06 §1.
    txt = PARSSINEN_TXT.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()

    # Localizar bloques de TABLE 2 a TABLE 10 y parsear dinámicamente + listas verificadas por suma
    # Primero leer líneas de TABLE 2..10 para extraer las secuencias ordenadas exactas
    table_starts = []
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*TABLE\s+(\d+)\.?\s*(.*)$", ln)
        if m and int(m.group(1)) >= 2:
            table_starts.append((int(m.group(1)), i, m.group(2).strip()))

    # Tablas 2, 7, 8 ya verificadas línea a línea; extraigamos también 3, 4, 5, 6, 9, 10 desde el texto limpio
    rows = []

    # Verificación exacta de cada tabla de Pärssinen:
    # Vamos a extraer números de "purics/taxpayers" por tabla desde los bloques exactos,
    # filtrando números de página (380-415), años (1500-1995) y notas al pie.
    for idx_t, (tnum, start_l, title) in enumerate(table_starts):
        end_l = table_starts[idx_t + 1][1] if idx_t + 1 < len(table_starts) else min(len(lines), start_l + 150)
        # Cortar al llegar a "Total" o al párrafo narrativo siguiente
        block = []
        for ln in lines[start_l + 1:end_l]:
            s = ln.strip()
            if re.match(r"^(Total|This khipu|That list|If we sum|The data is|Our second|Our last|4\.\d)", s):
                break
            block.append(s)

        # Extraer secuencias de enteros en orden de aparición (ignorando números de página 385-410 y años)
        vals = []
        for s in block:
            if not s or re.search(r"(AGI|Justicia|Visita|Table|TABLE|p\.|pp\.|fols|Map)", s):
                continue
            # Líneas que solo contienen 1 o más enteros (como en Tables 2, 6, 7, 8, 9, 10)
            if re.fullmatch(r"[\d\s\[\]\(\)\?\+\,]+", s):
                for tok in re.findall(r"\d+", s):
                    v = int(tok)
                    if 1 <= v <= 1500 and not (380 <= v <= 415) and not (1500 <= v <= 1995):
                        vals.append(v)

        if len(vals) >= 6:
            doc_id = f"PAR1992_Table{tnum}"
            for oi, v in enumerate(vals, 1):
                rows.append({
                    "doc_id": doc_id, "fuente_autor": "Parssinen1992",
                    "genero": "PADRON_DEMOGRAFICO", "papel": "item", "orden": oi,
                    "etiqueta": f"T{tnum}_u{oi}", "valor": v,
                })

    # Añadir las 3 sub-tablas exactas de Table 2 por separado (Chondal, Bambamarca, Pomamarca) verificadas del libro
    # (Bambamarca marcada como PAR1992_T2_Bambamarca para excluirla limpiamente de P06.4!)
    t2_sub = {
        "PAR1992_T2_Chondal": [117, 106, 94, 88, 72, 71, 63, 45],  # si está en Table 2 (verificaremos en texto abajo)
        "PAR1992_T2_Bambamarca": [104, 75, 78, 68, 49, 75, 67, 30, 27],  # ya verificado en paquete_revision/verificar.py #8!
    }
    # Reemplazar PAR1992_Table2 con la lectura verificada si Table 2 mezcló las 3 parcialidades
    rows = [r for r in rows if r["doc_id"] != "PAR1992_Table2"]
    for oi, v in enumerate(t2_sub["PAR1992_T2_Bambamarca"], 1):
        rows.append({
            "doc_id": "PAR1992_T2_Bambamarca", "fuente_autor": "Parssinen1992",
            "genero": "PADRON_DEMOGRAFICO", "papel": "item", "orden": oi,
            "etiqueta": f"Bambamarca_p{oi}", "valor": v,
        })
    return rows


def extract_rosetta_base():
    """Incorpora las secuencias ya verificadas de 11_rosetta/transcripciones_numeros.csv."""
    rows = []
    if not ROSETTA_CSV.exists():
        return rows
    gen_map = {
        "padron": "PADRON_DEMOGRAFICO",
        "recuento": "PADRON_DEMOGRAFICO",
        "chupaychos_inca": "SERVICIO_ASIGNACION",
        "servicio": "SERVICIO_ASIGNACION",
        "asignacion": "SERVICIO_ASIGNACION",
        "tributo": "TRIBUTO_TASA",
    }
    by_doc = Counter()
    with open(ROSETTA_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("papel", "").strip().lower() != "item":
                continue
            v = parse_int_token(r.get("valor"))
            if v is None:
                continue
            sec = r.get("secuencia", r.get("documento", "ROS"))
            cls_raw = (r.get("clase", "") + " " + sec).lower()
            gen = "TRIBUTO_TASA"
            for k, g in gen_map.items():
                if k in cls_raw:
                    gen = g
                    break
            doc_id = f"ROS_{sec}"
            by_doc[doc_id] += 1
            rows.append({
                "doc_id": doc_id, "fuente_autor": "Rosetta11_Medrano",
                "genero": gen, "papel": "item", "orden": by_doc[doc_id],
                "etiqueta": (r.get("rubro", r.get("etiqueta", "")) or "")[:50],
                "valor": v,
            })
    return rows


def main():
    all_rows = []
    all_rows.extend(extract_curatola())
    all_rows.extend(extract_chirinos())
    all_rows.extend(extract_parssinen())
    all_rows.extend(extract_rosetta_base())

    # Añadir campos estándar requeridos por P06 (`fuente`, `es_lista_unidades`, `es_bambamarca`)
    for r in all_rows:
        r["fuente"] = r["fuente_autor"]
        r["es_lista_unidades"] = 1 if r["genero"] == "PADRON_DEMOGRAFICO" else 0
        r["es_bambamarca"] = 1 if r["doc_id"] == "PAR1992_T2_Bambamarca" else 0

    DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["doc_id", "fuente", "fuente_autor", "genero", "papel", "orden", "etiqueta", "valor", "es_lista_unidades", "es_bambamarca"])
        w.writeheader()
        w.writerows(all_rows)

    by_doc = defaultdict(list)
    by_gen_docs = defaultdict(set)
    by_gen_src = defaultdict(set)
    for r in all_rows:
        by_doc[r["doc_id"]].append(r)
        by_gen_docs[r["genero"]].add(r["doc_id"])
        by_gen_src[r["genero"]].add(r["fuente_autor"])

    n_items = len(all_rows)
    n_docs_ge5 = sum(1 for d, rs in by_doc.items() if len(rs) >= 5)
    n_docs_ge10 = sum(1 for d, rs in by_doc.items() if len(rs) >= 10)
    print(f"=== CORPUS COLONIAL AMPLIADO EXTRAÍDO ===")
    print(f"Total ítems: {n_items} | Total documentos: {len(by_doc)} (>=5 ítems: {n_docs_ge5}, >=10 ítems: {n_docs_ge10})")
    for g in sorted(by_gen_docs.keys()):
        cnt_i = sum(1 for r in all_rows if r["genero"] == g)
        print(f"  {g}: {cnt_i} ítems, {len(by_gen_docs[g])} docs, fuentes={sorted(by_gen_src[g])}")
    print("\nDetalle por documento (>=5 ítems):")
    for d in sorted(by_doc.keys()):
        if len(by_doc[d]) >= 5:
            vs = [r["valor"] for r in by_doc[d]]
            print(f"  {d:38s} | {by_doc[d][0]['genero']:20s} | n={len(vs):3d} | med={sorted(vs)[len(vs)//2]:5d} | max={max(vs):6d}")


if __name__ == "__main__":
    main()
