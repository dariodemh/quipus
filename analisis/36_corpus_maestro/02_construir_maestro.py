#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_construir_maestro.py — Constructor determinista del Corpus Maestro Unificado de Quipus (KH####).

Fuentes integradas (todas leídas en solo lectura):
  1. KFG (`analisis/datos/cuerdas.csv`, `quipus.csv`, `grupos.csv`) — 650 quipus distintos (excl. duplicado UR044).
  2. OKR (`quipu/data/external/open-khipu-repository/data/khipu.db` + `okr-kh-numbers.csv` + `puente.csv`):
     - Reemplaza los 4 desplazados de KFG (`KH0197`, `KH0227`, `KH0267`, `KH0350`) y usa OKR como fuente
       completa para Inkawasi (recuperando 111 cuerdas faltantes en KFG) y para todas las cuerdas superiores
       (`T`) y marcadoras (`M`) que KFG pierde.
     - Añade los quipus presentes en `khipu.db` que faltan en KFG (`held_out`).
     - Aporta geometría física 2D (`cord_cluster.START_POSITION/SPACING`, `knot_cluster.START_POS/END_POS`,
       `THICKNESS`, `FIBER`, `TWIST_ANGLE`, `CORD_CLASSIFICATION`, `CREATED_BY`) y coordenadas CIE L*a*b*
       derivadas de `ascher_color_dc` (RGB ISCC-NBS).
  3. Adjuntos OKR estructurados (`17_okr_pendientes/cuerdas_extra.csv`, `ds/n_okr_resto/cuerdas_nuevas.csv`,
     `ds/n_fichas_jpg/transcripcion_JC024..034_record.csv`, más `KH0652` MNAAHP.15 `wrapped threads`).
  4. Databook de Ascher & Ascher (`quipu/analisis/fuentes_txt/databook/as*.txt`) para los quipus/partes
     genuinamente ausentes de KFG y OKR (resolviendo alias `UR1xxx` vía `puente.csv`).
  5. `collca.db` (`KhipuAnalysis`) para auditoría cruzada y rescate de quipus no presentes en KFG/OKR.
  6. Capa de correcciones de Karen M. Thompson (2025a, `thompson_2025_correcciones.csv`): se conserva
     siempre `valor` crudo y se añade `valor_thompson` + `thompson_flag` (nunca se sobreescribe en silencio).

Salidas en `analisis/36_corpus_maestro/`:
  - `maestro_quipus.csv`
  - `maestro_cuerdas.csv`
  - `rt16905_k15_wrapped.csv`
  - `reporte_integridad.md`
"""
import csv
import math
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

RAIZ_QUIPUS = Path(__file__).resolve().parents[2]
RAIZ_QUIPU = RAIZ_QUIPUS.parent / "quipu"
OUT_DIR = Path(__file__).resolve().parent

KFG_CUERDAS = RAIZ_QUIPUS / "analisis/datos/cuerdas.csv"
KFG_QUIPUS = RAIZ_QUIPUS / "analisis/datos/quipus.csv"
PUENTE_CSV = RAIZ_QUIPUS / "analisis/17_okr_pendientes/puente.csv"
EXTRA_CSV = RAIZ_QUIPUS / "analisis/17_okr_pendientes/cuerdas_extra.csv"
NUEVAS_CSV = RAIZ_QUIPUS / "analisis/ds/n_okr_resto/cuerdas_nuevas.csv"
FICHAS_DIR = RAIZ_QUIPUS / "analisis/ds/n_fichas_jpg"
THOMPSON_CSV = OUT_DIR / "thompson_2025_correcciones.csv"
OKR_DB = RAIZ_QUIPU / "data/external/open-khipu-repository/data/khipu.db"
OKR_KH_CSV = RAIZ_QUIPU / "data/external/open-khipu-repository/data/okr-kh-numbers.csv"
COLLCA_DB = RAIZ_QUIPU / "data/local_only/KhipuAnalysis/collca.db"
DATABOOK_TXT = RAIZ_QUIPU / "analisis/fuentes_txt/databook"
K15_XLSX = RAIZ_QUIPU / "data/external/open-khipu-repository/data/KH0638_0652/KHIPU ENLAZADO-MNAAHP.15.xlsx"

# Quipus reconstruidos en KFG según n_databook (valores sin respaldo en Databook)
KFG_RECONSTRUIDOS = {"AS014", "AS036", "AS037", "AS081", "AS129"}
# Los 4 archivos desplazados en KFG (hallazgo C26): el archivo KH0xxx de KFG contiene en realidad KH0(xxx+1)
KFG_SHIFT_FIX = {
    "KH0197": "KH0198",
    "KH0227": "KH0228",
    "KH0267": "KH0268",
    "KH0350": "KH0351",
}
# Aliases KFG sin OKR en quipus.csv detectados por inventario/metadato
KFG_ALIAS_EXTRA = {
    "UR1180": "KH0197",
    "MM1086": "KH0099",
}
KFG_DESPLAZADOS_KH = set(KFG_SHIFT_FIX.values())
# Duplicados físicos conocidos antes del preregistro P01 (criterio no numérico)
DUPLICADO_EXACTO_KFG = {"UR044": "KH0033"}  # UR044 == KH0033/AS031
DUPLICADOS_FISICOS_PARES = {
    "KH0155": "KH0469",  # AS125 == UR247 (si aplica)
}

def rgb_to_lab(r: float, g: float, b: float):
    """Convierte sRGB [0,1] a CIE L*a*b* (iluminante D65)."""
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    rl, gl, bl = lin(r), lin(g), lin(b)
    x = (0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl) / 0.95047
    y = (0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl) / 1.00000
    z = (0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl) / 1.08883
    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t + 16.0 / 116.0)
    fx, fy, fz = f(x), f(y), f(z)
    L = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b_val = 200.0 * (fy - fz)
    return round(L, 3), round(a, 3), round(b_val, 3)

def primary_color_code(raw: str) -> str:
    if not raw:
        return ""
    s = re.sub(r"\([^)]*\)", "", str(raw).upper()).strip()
    if not s:
        return ""
    parts = [p.strip() for p in re.split(r"[:/\-*%\s]+", s) if p.strip()]
    return parts[0] if parts else ""

def load_color_lab(con_okr):
    """Carga tabla ascher_color_dc -> (L, a, b) para los 64 códigos base."""
    cmap = {}
    for code, r, g, b in con_okr.execute(
        "SELECT AS_COLOR_CD, R_DEC, G_DEC, B_DEC FROM ascher_color_dc WHERE R_DEC IS NOT NULL"
    ).fetchall():
        code_u = str(code).upper().strip()
        cmap[code_u] = rgb_to_lab(float(r), float(g), float(b))
        # Aliases frecuentes O vs 0 (ej. OD vs 0D, OG vs 0G)
        if code_u.startswith("0"):
            cmap["O" + code_u[1:]] = cmap[code_u]
    return cmap

def color_to_lab(color_str: str, cmap: dict):
    base = primary_color_code(color_str)
    if base in cmap:
        return base, cmap[base]
    # Intentar reemplazo O->0
    if base.startswith("O") and ("0" + base[1:]) in cmap:
        return base, cmap["0" + base[1:]]
    return base, ("", "", "")

def norm_inv_num(s: str) -> str:
    """Normaliza alias de investigador (QU01 -> QU001, AS1 -> AS001, UR6 -> UR006)."""
    if not s:
        return ""
    s = str(s).strip()
    m = re.match(r"^([A-Za-z]{2,3})\s*0*(\d+)([A-Za-z]?)$", s)
    if m:
        pref, num, suf = m.group(1).upper(), int(m.group(2)), m.group(3).upper()
        if pref in ("AS", "UR", "HP", "QU", "MM", "JC", "SH"):
            return f"{pref}{num:03d}{suf}"
    return s.upper()

def load_puente():
    with open(PUENTE_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_kh = {}
    by_kfg = {}
    by_alias = {}
    for r in rows:
        kh = r["kh"].strip()
        by_kh[kh] = r
        if r["kfg"].strip():
            by_kfg[r["kfg"].strip()] = kh
            by_alias[norm_inv_num(r["kfg"].strip())] = kh
        for col in ("ur", "as"):
            v = r[col].strip()
            if v:
                for tok in re.split(r"[/,;]+", v):
                    t = tok.strip()
                    if t:
                        by_alias[t.upper()] = kh
                        by_alias[norm_inv_num(t)] = kh
        if r["otros_alias"].strip():
            for tok in re.split(r"[/,;]+", r["otros_alias"].strip()):
                t = tok.strip()
                if t:
                    by_alias[t.upper()] = kh
                    by_alias[norm_inv_num(t)] = kh
    return by_kh, by_kfg, by_alias

def load_okr_khipu_data(con_okr, cmap):
    """Carga todos los quipus y cuerdas de OKR khipu.db con geometría 2D completa."""
    # Colores por CORD_ID
    cord_colors = defaultdict(list)
    for cid, c1, op1, cr in con_okr.execute(
        "SELECT CORD_ID, COLOR_CD_1, OPERATOR_1, COLOR_RANGE FROM ascher_cord_color ORDER BY color_id"
    ).fetchall():
        tok = str(c1 or "").strip()
        if tok:
            cord_colors[cid].append((tok, str(op1 or "").strip(), str(cr or "").strip()))

    def fmt_color(cid):
        items = cord_colors.get(cid, [])
        if not items:
            return ""
        parts = []
        for idx, (c1, op1, cr) in enumerate(items):
            if idx > 0 and op1:
                parts.append(op1)
            elif idx > 0:
                parts.append("/")
            parts.append(c1)
        return "".join(parts)

    # Nudos por CLUSTER_ID y por CORD_ID
    kc_knots = defaultdict(list)
    for cid, clid, tcode, direc, kvt, nturns in con_okr.execute(
        "SELECT CORD_ID, CLUSTER_ID, TYPE_CODE, DIRECTION, knot_value_type, NUM_TURNS FROM knot ORDER BY CLUSTER_ORDINAL, KNOT_ORDINAL"
    ).fetchall():
        kc_knots[clid].append((tcode or "", direc or "", kvt, nturns))

    cord_kcs = defaultdict(list)
    for cid, clid, ordn, spos, epos, tval, nkn in con_okr.execute(
        "SELECT CORD_ID, CLUSTER_ID, ORDINAL, START_POS, END_POS, TOTAL_VALUE, NUM_KNOTS FROM knot_cluster ORDER BY CORD_ID, ORDINAL, START_POS"
    ).fetchall():
        cord_kcs[cid].append((clid, ordn, spos, epos, tval, nkn))

    # Clusters de cordón principal
    cc_map = {}
    for clid, ordn, spos, epos, spc in con_okr.execute(
        "SELECT CLUSTER_ID, ORDINAL, START_POSITION, END_POSITION, SPACING FROM cord_cluster"
    ).fetchall():
        cc_map[clid] = (ordn, spos, epos, spc)

    khipu_meta = {}
    for r in con_okr.execute("""
        SELECT KHIPU_ID, OKR_NUM, INVESTIGATOR_NUM, MUSEUM_NAME, PROVENANCE, REGION,
               MUSEUM_NUM, CONDITIONOFKHIPU, CREATED_BY
        FROM khipu_main
    """).fetchall():
        khipu_meta[r[0]] = {
            "khipu_id": r[0], "okr_num": r[1] or "", "inv_num": r[2] or "",
            "museo": (r[3] or "").strip('" '), "procedencia": (r[4] or "").strip('" '),
            "region": (r[5] or "").strip('" '), "n_inventario": (r[6] or "").strip('" '),
            "condicion": r[7] or "", "created_by": r[8] or "",
        }

    # Construir cuerdas por OKR_NUM
    cords_by_kh = defaultdict(list)
    # Primero cargar todas las filas de cord agrupadas por KHIPU_ID para reconstruir jerarquía de nombres
    raw_cords = defaultdict(list)
    for r in con_okr.execute("""
        SELECT KHIPU_ID, CORD_ID, CORD_LEVEL, CORD_CLASSIFICATION, ATTACHMENT_TYPE, TWIST,
               TWIST_ANGLE, THICKNESS, FIBER, CORD_LENGTH, TERMINATION, CLUSTER_ID,
               CLUSTER_ORDINAL, CORD_ORDINAL, PENDANT_FROM, ATTACHED_TO, ATTACH_POS,
               INVESTIGATOR_CORD_NUM, CORD_NOTES, CREATED_BY
        FROM cord
        ORDER BY KHIPU_ID, CORD_LEVEL, CLUSTER_ORDINAL, CORD_ORDINAL, CORD_ID
    """).fetchall():
        raw_cords[r[0]].append(r)

    for kid, clist in raw_cords.items():
        meta = khipu_meta.get(kid)
        if not meta or not meta["okr_num"]:
            continue
        kh = meta["okr_num"]
        # Mapear CORD_ID -> nombre canónico p#, t#, m#, p#s#
        id_to_name = {}
        sub_counter = defaultdict(int)
        p_idx = 0
        t_idx = 0
        m_idx = 0
        # Ordenar por nivel (1 = colgante/superior/marcadora, 2+ = subsidiaria)
        by_id = {r[1]: r for r in clist}
        # Asignar nombres en orden de nivel ascendente
        for r in sorted(clist, key=lambda x: (x[2] or 1, x[12] or 0, x[13] or 0, x[1])):
            cid = r[1]
            lvl_okr = r[2] if r[2] is not None else 1
            cls = (r[3] or "").strip().upper()
            att_to = r[15]
            inv_cnum = r[17]
            if lvl_okr <= 1:
                if cls == "T":
                    t_idx += 1
                    cname = f"t{inv_cnum}" if (inv_cnum is not None and str(inv_cnum).isdigit()) else f"t{t_idx}"
                    tipo = "t"
                elif cls == "M":
                    m_idx += 1
                    cname = f"m{m_idx}"
                    tipo = "m"
                else:
                    p_idx += 1
                    cname = f"p{inv_cnum}" if (inv_cnum is not None and str(inv_cnum).isdigit()) else f"p{p_idx}"
                    tipo = "p"
                padre = ""
                nivel = 0
            else:
                parent_name = id_to_name.get(att_to, f"p{p_idx}")
                sub_counter[parent_name] += 1
                cname = f"{parent_name}s{sub_counter[parent_name]}"
                padre = parent_name
                tipo = parent_name[0] if parent_name else "p"
                nivel = lvl_okr - 1
            id_to_name[cid] = cname

            # Nudos y valor (en OKR khipu.db knot_cluster.TOTAL_VALUE está en 0/NULL; el valor real es SUM(knot.knot_value_type))
            kcs = cord_kcs.get(cid, [])
            val_sum = 0
            knot_strs = []
            k_pos = []
            k_types = []
            k_dirs = []
            for clid, ordn, spos, epos, tval, nkn in kcs:
                ks = kc_knots.get(clid, [])
                cl_val = 0
                for _tc, _dr, kvt, _nt in ks:
                    if kvt is not None:
                        try:
                            cl_val += int(round(float(kvt)))
                        except Exception:
                            pass
                if cl_val == 0 and tval is not None:
                    try:
                        cl_val = int(round(float(tval)))
                    except Exception:
                        pass
                val_sum += cl_val
                if spos is not None:
                    k_pos.append(f"{float(spos):.1f}")
                if ks:
                    t0 = ks[0][0] or "?"
                    d0 = ks[0][1] or "U"
                    n0 = nkn if nkn is not None else len(ks)
                    if t0 == "L" and ks[0][3] is not None:
                        n0 = ks[0][3]
                    elif t0 == "L" and cl_val > 0 and cl_val <= 15:
                        n0 = cl_val
                    k_types.append(f"{n0}{t0}")
                    k_dirs.append(d0)
                    knot_strs.append(f"{n0}{t0}({spos if spos is not None else ''},{d0},{cl_val})")
            val_out = val_sum if kcs else 0

            # Geometría de clúster
            cc = cc_map.get(r[11], (None, None, None, None))
            color_raw = fmt_color(cid)
            cbase, (L, a, b) = color_to_lab(color_raw, cmap)

            cords_by_kh[kh].append({
                "kh_id": kh,
                "cord_id_okr": cid,
                "cuerda": cname,
                "tipo": tipo,
                "nivel": nivel,
                "padre": padre,
                "grupo": (cc[0] - 1) if (cc[0] is not None and cc[0] >= 1) else "",
                "valor": val_out,
                "nudos": ";".join(knot_strs),
                "color": color_raw,
                "color_base": cbase,
                "lab_L": L, "lab_a": a, "lab_b": b,
                "torsion": (r[5] or "").strip(),
                "union": (r[4] or "").strip(),
                "largo": r[9] if r[9] is not None else "",
                "terminacion": (r[10] or "").strip(),
                "notas": str(r[18] or "").replace("\n", " ").replace("\r", " ").strip(),
                "cord_classification": cls,
                "fiber": (r[8] or "").strip(),
                "thickness": r[7] if r[7] is not None else "",
                "twist_angle": r[6] if r[6] is not None else "",
                "cluster_ordinal": cc[0] if cc[0] is not None else "",
                "cluster_pos_cm": cc[1] if cc[1] is not None else "",
                "cluster_spacing_cm": cc[3] if cc[3] is not None else "",
                "knot_n_clusters": len(kcs),
                "knot_first_pos_cm": k_pos[0] if k_pos else "",
                "knot_last_pos_cm": k_pos[-1] if k_pos else "",
                "knot_positions_cm": ";".join(k_pos),
                "knot_types": ";".join(k_types),
                "knot_dirs": ";".join(k_dirs),
                "created_by": (r[19] or meta["created_by"] or "").strip(),
            })
    return khipu_meta, cords_by_kh

def parse_k15_wrapped():
    """Extrae los 19 hilos envueltos de KH0652 (MNAAHP.15) a CSV limpio."""
    wb = openpyxl.load_workbook(K15_XLSX, read_only=True)
    ws = wb["wrapped threads"]
    rows = []
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        if not r or not r[0]:
            continue
        wid = str(r[0]).strip()
        if not wid.upper().startswith("W"):
            continue
        spec = str(r[1] or "").strip()
        m_pos = re.search(r"([\d.]+)\s*cm", spec, re.I)
        m_wid = re.search(r"([\d.]+)\s*mm", spec, re.I)
        m_trn = re.search(r"(\d+)\s*turns?", spec, re.I)
        # También formato "pos, wide, turns" separado por comas
        nums = re.findall(r"[\d.]+", spec)
        pos_cm = m_pos.group(1) if m_pos else (nums[0] if len(nums) >= 1 else "")
        wide_mm = m_wid.group(1) if m_wid else (nums[1] if len(nums) >= 2 else "")
        turns = m_trn.group(1) if m_trn else (nums[2] if len(nums) >= 3 else "")
        rows.append({
            "kh_id": "KH0652",
            "hilo": wid,
            "spec_raw": spec,
            "pos_cm": pos_cm,
            "ancho_mm": wide_mm,
            "vueltas": turns,
            "largo_colgantes_cm": str(r[2] or "").strip(),
            "color": str(r[3] or "").strip(),
            "seccion": str(r[4] or "").strip(),
            "notas": str(r[5] or "").replace("\n", " ").strip(),
        })
    out = OUT_DIR / "rt16905_k15_wrapped.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "kh_id", "hilo", "spec_raw", "pos_cm", "ancho_mm", "vueltas",
            "largo_colgantes_cm", "color", "seccion", "notas"
        ])
        w.writeheader()
        w.writerows(rows)
    return len(rows)

def load_thompson():
    """Carga parches y conteo de notas de Thompson (2025a) indexados por AS###."""
    by_as_count = Counter()
    val_patches = {}  # (as_id, cord_name) -> (val_new, orig, rev)
    with open(THOMPSON_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            aid = r["as_id"].strip().upper()
            by_as_count[aid] += 1
            if r["valor_propuesto"] and r["n_cuerdas"] == "1":
                cname = r["cuerdas_citadas"].strip().lower()
                val_patches[(aid, cname)] = (int(r["valor_propuesto"]), r["valor_orig"], r["revision"])
    return by_as_count, val_patches

def parse_missing_databook(existing_kh, existing_kfg, by_alias, cmap):
    """Parsea los archivos Databook que corresponden a quipus genuinamente ausentes de KFG y OKR."""
    sys.path.insert(0, str(RAIZ_QUIPUS / "analisis/ds/n_databook"))
    import parse_databook as pdb

    # Determinar qué archivos as*.txt tienen quipus/partes ausentes
    new_quipus = {}  # qid -> list of cord dicts
    for p in sorted(DATABOOK_TXT.glob("as[0-9]*.txt"), key=lambda x: int(re.search(r"as(\d+)\.txt", x.name).group(1))):
        rows, _obs = pdb.parse_file(str(p))
        if not rows:
            continue
        by_q = defaultdict(list)
        for r in rows:
            by_q[r["quipu"]].append(r)
        for qid, qrows in by_q.items():
            # Resolver si ya existe en KFG o OKR (incluyendo alias UR1xxx!)
            kh = by_alias.get(qid.upper()) or by_alias.get(norm_inv_num(qid))
            if kh and (kh in existing_kh):
                continue
            if qid in existing_kfg or norm_inv_num(qid) in existing_kfg:
                continue
            # Es genuinamente nuevo (ej. AS026B, AS033A..G, AS035A..D, AS124, AS162, AS207A..C...)
            canon = kh if kh else qid
            out_list = []
            for idx, r in enumerate(qrows):
                cbase, (L, a, b) = color_to_lab(r["color"], cmap)
                cname = r["cord_databook"]
                val = r["valor"]
                val_int = "" if (val is None or (isinstance(val, float) and math.isnan(val))) else int(round(float(val)))
                m = re.match(r"([a-z]+)(\d+)", cname)
                padre = cname[: max(cname.rfind("s"), 0)] if cname.count("s") and re.search(r"\ds\d", cname) else ""
                out_list.append({
                    "kh_id": canon,
                    "kfg_id": qid,
                    "orden": idx,
                    "cuerda": cname,
                    "tipo": m.group(1) if m else "p",
                    "nivel": len(re.findall(r"s\d+", cname)),
                    "padre": padre,
                    "grupo": "",
                    "valor": val_int,
                    "alt": r["valor_knots"] if r["valor_knots"] is not None else "",
                    "nudos": r["knots_norm"] or "",
                    "color": r["color"] or "",
                    "color_base": cbase,
                    "lab_L": L, "lab_a": a, "lab_b": b,
                    "torsion": "", "union": "",
                    "largo": r["largo"] if r["largo"] is not None else "",
                    "terminacion": "",
                    "notas": ("dudoso" if r["valor_dudoso"] else ""),
                    "fuente_cuerda": "databook_ocr",
                    "cord_classification": "T" if cname.startswith("t") else "",
                    "fiber": "", "thickness": "", "twist_angle": "",
                    "cluster_ordinal": "", "cluster_pos_cm": "", "cluster_spacing_cm": "",
                    "knot_n_clusters": "", "knot_first_pos_cm": "", "knot_last_pos_cm": "",
                    "knot_positions_cm": "", "knot_types": "", "knot_dirs": "",
                    "created_by": "ascher_databook",
                })
            new_quipus[canon] = (qid, out_list)
    return new_quipus

def main():
    by_kh, by_kfg, by_alias = load_puente()
    thompson_counts, thompson_patches = load_thompson()

    con_okr = sqlite3.connect(f"file:{OKR_DB}?mode=ro", uri=True)
    cmap = load_color_lab(con_okr)
    okr_meta, okr_cords = load_okr_khipu_data(con_okr, cmap)
    okr_meta_by_kh = {m["okr_num"]: m for m in okr_meta.values() if m["okr_num"]}

    # Cargar KFG
    with open(KFG_QUIPUS, encoding="utf-8") as f:
        kfg_q_rows = list(csv.DictReader(f))
    kfg_q_by_id = {r["kfg"]: r for r in kfg_q_rows}

    kfg_cords_by_id = defaultdict(list)
    with open(KFG_CUERDAS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            kfg_cords_by_id[r["kfg"]].append(r)

    # Identificar conjunto canónico de los 650 quipus base de KFG (excluyendo UR044)
    base_kh_set = set()
    base_kfg_set = set()
    maestro_quipus = {}
    maestro_cuerdas = []

    stats = Counter()

    # 1) Procesar los 650 quipus distintos de KFG (enriquecidos con geometría OKR y rescate de T/M e Inkawasi OKR)
    for kfg_id, qmeta in sorted(kfg_q_by_id.items()):
        if kfg_id in DUPLICADO_EXACTO_KFG:
            stats["kfg_duplicados_excluidos"] += 1
            continue
        if kfg_id in KFG_SHIFT_FIX:
            kh = KFG_SHIFT_FIX[kfg_id]
        elif kfg_id in KFG_ALIAS_EXTRA:
            kh = KFG_ALIAS_EXTRA[kfg_id]
        else:
            kh = qmeta["okr"].strip() or by_kfg.get(kfg_id, "") or by_alias.get(norm_inv_num(kfg_id), "")
        canon = kh if kh else kfg_id
        assert canon not in maestro_quipus, f"Colisión inesperada de clave canónica: {canon} ({kfg_id})"
        base_kh_set.add(canon)
        base_kfg_set.add(kfg_id)
        base_kfg_set.add(norm_inv_num(kfg_id))

        # Determinar si preferimos OKR como fuente de cuerdas (los 4 desplazados de KFG o Inkawasi UR255-280)
        use_okr_primary = (canon in KFG_DESPLAZADOS_KH and canon in okr_cords)
        is_inkawasi_ur = (qmeta["procedencia"].lower().find("incahuasi") >= 0 or qmeta["procedencia"].lower().find("inkawasi") >= 0) and kfg_id.startswith("UR")
        if is_inkawasi_ur and canon in okr_cords:
            use_okr_primary = True

        okr_list = okr_cords.get(canon, [])
        okr_by_name = {c["cuerda"].lower(): c for c in okr_list}

        # Alias AS para aplicar Thompson 2025a
        as_id = ""
        if kfg_id.startswith("AS"):
            as_id = norm_inv_num(kfg_id)
        elif canon in by_kh and by_kh[canon]["as"]:
            as_id = norm_inv_num(by_kh[canon]["as"].split("/")[0].strip())

        out_cords = []
        if use_okr_primary:
            stats["kfg_reemplazados_por_okr"] += 1
            for idx, oc in enumerate(okr_list):
                row = {
                    "kh_id": canon, "kfg_id": kfg_id, "orden": idx,
                    "cuerda": oc["cuerda"], "tipo": oc["tipo"], "nivel": oc["nivel"],
                    "padre": oc["padre"], "grupo": oc["grupo"],
                    "valor": oc["valor"], "alt": "", "nudos": oc["nudos"],
                    "color": oc["color"], "color_base": oc["color_base"],
                    "lab_L": oc["lab_L"], "lab_a": oc["lab_a"], "lab_b": oc["lab_b"],
                    "torsion": oc["torsion"], "union": oc["union"],
                    "largo": oc["largo"], "terminacion": oc["terminacion"], "notas": oc["notas"],
                    "fuente_cuerda": "okr_preferente",
                    "cord_classification": oc["cord_classification"],
                    "fiber": oc["fiber"], "thickness": oc["thickness"], "twist_angle": oc["twist_angle"],
                    "cluster_ordinal": oc["cluster_ordinal"], "cluster_pos_cm": oc["cluster_pos_cm"],
                    "cluster_spacing_cm": oc["cluster_spacing_cm"],
                    "knot_n_clusters": oc["knot_n_clusters"],
                    "knot_first_pos_cm": oc["knot_first_pos_cm"],
                    "knot_last_pos_cm": oc["knot_last_pos_cm"],
                    "knot_positions_cm": oc["knot_positions_cm"],
                    "knot_types": oc["knot_types"], "knot_dirs": oc["knot_dirs"],
                    "created_by": oc["created_by"],
                }
                out_cords.append(row)
        else:
            seen_okr_names = set()
            for r in kfg_cords_by_id[kfg_id]:
                cname = r["cuerda"].strip()
                oc = okr_by_name.get(cname.lower())
                if oc:
                    seen_okr_names.add(cname.lower())
                cbase, (L, a, b) = color_to_lab(r["color"], cmap)
                row = {
                    "kh_id": canon, "kfg_id": kfg_id, "orden": int(r["orden"]),
                    "cuerda": cname, "tipo": r["tipo"], "nivel": int(r["nivel"]),
                    "padre": r["padre"], "grupo": r["grupo"],
                    "valor": r["valor"], "alt": r["alt"], "nudos": r["nudos"],
                    "color": r["color"], "color_base": cbase,
                    "lab_L": L, "lab_a": a, "lab_b": b,
                    "torsion": r["torsion"], "union": r["union"],
                    "largo": r["largo"], "terminacion": r["terminacion"], "notas": r["notas"],
                    "fuente_cuerda": "kfg+okr_geom" if oc else "kfg",
                    "cord_classification": oc["cord_classification"] if oc else "",
                    "fiber": oc["fiber"] if oc else "",
                    "thickness": oc["thickness"] if oc else "",
                    "twist_angle": oc["twist_angle"] if oc else "",
                    "cluster_ordinal": oc["cluster_ordinal"] if oc else "",
                    "cluster_pos_cm": oc["cluster_pos_cm"] if oc else "",
                    "cluster_spacing_cm": oc["cluster_spacing_cm"] if oc else "",
                    "knot_n_clusters": oc["knot_n_clusters"] if oc else "",
                    "knot_first_pos_cm": oc["knot_first_pos_cm"] if oc else "",
                    "knot_last_pos_cm": oc["knot_last_pos_cm"] if oc else "",
                    "knot_positions_cm": oc["knot_positions_cm"] if oc else "",
                    "knot_types": oc["knot_types"] if oc else "",
                    "knot_dirs": oc["knot_dirs"] if oc else "",
                    "created_by": oc["created_by"] if oc else "",
                }
                out_cords.append(row)
            # Rescatar cuerdas superiores ('T') y marcadoras ('M') de OKR que KFG omitió!
            next_ord = len(out_cords)
            for oc in okr_list:
                if oc["cord_classification"] in ("T", "M") and oc["cuerda"].lower() not in seen_okr_names:
                    stats[f"rescatadas_okr_{oc['cord_classification']}"] += 1
                    # Si grupo está vacío en top cord, inferirlo del índice de t# (1-based -> 0-based)
                    g_rec = oc["grupo"]
                    if g_rec == "" and oc["tipo"] == "t":
                        mt = re.match(r"^t(\d+)$", oc["cuerda"])
                        if mt:
                            g_rec = max(0, int(mt.group(1)) - 1)
                    out_cords.append({
                        "kh_id": canon, "kfg_id": kfg_id, "orden": next_ord,
                        "cuerda": oc["cuerda"], "tipo": oc["tipo"], "nivel": oc["nivel"],
                        "padre": oc["padre"], "grupo": g_rec,
                        "valor": oc["valor"], "alt": "", "nudos": oc["nudos"],
                        "color": oc["color"], "color_base": oc["color_base"],
                        "lab_L": oc["lab_L"], "lab_a": oc["lab_a"], "lab_b": oc["lab_b"],
                        "torsion": oc["torsion"], "union": oc["union"],
                        "largo": oc["largo"], "terminacion": oc["terminacion"], "notas": oc["notas"],
                        "fuente_cuerda": f"okr_rescate_{oc['cord_classification']}",
                        "cord_classification": oc["cord_classification"],
                        "fiber": oc["fiber"], "thickness": oc["thickness"], "twist_angle": oc["twist_angle"],
                        "cluster_ordinal": oc["cluster_ordinal"], "cluster_pos_cm": oc["cluster_pos_cm"],
                        "cluster_spacing_cm": oc["cluster_spacing_cm"],
                        "knot_n_clusters": oc["knot_n_clusters"],
                        "knot_first_pos_cm": oc["knot_first_pos_cm"],
                        "knot_last_pos_cm": oc["knot_last_pos_cm"],
                        "knot_positions_cm": oc["knot_positions_cm"],
                        "knot_types": oc["knot_types"], "knot_dirs": oc["knot_dirs"],
                        "created_by": oc["created_by"],
                    })
                    next_ord += 1

        # Aplicar overlay Thompson (sin borrar valor original)
        for row in out_cords:
            row["held_out"] = 0
            patch = thompson_patches.get((as_id, row["cuerda"].lower())) if as_id else None
            if patch:
                row["valor_thompson"] = patch[0]
                row["thompson_flag"] = "valor_parcheado"
                stats["thompson_parches_aplicados"] += 1
            else:
                row["valor_thompson"] = row["valor"]
                row["thompson_flag"] = ""
            maestro_cuerdas.append(row)

        om = okr_meta_by_kh.get(canon, {})
        pr = by_kh.get(canon, {})
        maestro_quipus[canon] = {
            "kh_id": canon, "kfg_id": kfg_id, "okr_num": canon if canon.startswith("KH") else "",
            "as_id": as_id, "ur_id": pr.get("ur", ""),
            "fuente_primaria": "okr_preferente" if use_okr_primary else "kfg",
            "en_kfg": 1, "en_okr": 1 if canon in okr_cords else 0, "en_databook": 0,
            "held_out": 0,
            "museo": qmeta["museo"] or om.get("museo", "") or pr.get("museo", ""),
            "procedencia": qmeta["procedencia"] or om.get("procedencia", ""),
            "region": qmeta["region"] or om.get("region", ""),
            "n_inventario": om.get("n_inventario", "") or pr.get("n_inventario", ""),
            "n_cuerdas": len(out_cords),
            "n_colgantes": sum(1 for c in out_cords if c["nivel"] == 0 and c["tipo"] == "p"),
            "n_superiores": sum(1 for c in out_cords if c["tipo"] == "t" or c["cord_classification"] == "T" or c["union"] == "T"),
            "n_marcadoras": sum(1 for c in out_cords if c["tipo"] == "m" or c["cord_classification"] == "M"),
            "thompson_n_notas": thompson_counts.get(as_id, 0) if as_id else 0,
            "reconstruido_kfg": 1 if (kfg_id in KFG_RECONSTRUIDOS or as_id in KFG_RECONSTRUIDOS) else 0,
            "created_by": om.get("created_by", ""),
        }

    # 2) Quipus en OKR khipu.db que NO están en KFG (held_out = 1)
    for kh, clist in sorted(okr_cords.items()):
        if kh in maestro_quipus:
            continue
        om = okr_meta_by_kh.get(kh, {})
        inv_norm = norm_inv_num(om.get("inv_num", ""))
        # Verificar si es alias de un quipu ya en KFG (ej. QU01 -> QU001, AS101 - Part 1 -> AS101_Part_1)
        if inv_norm in base_kfg_set:
            stats["okr_alias_ya_en_kfg"] += 1
            continue
        pr = by_kh.get(kh, {})
        if pr.get("kfg") and pr["kfg"] in base_kfg_set:
            stats["okr_alias_ya_en_kfg"] += 1
            continue
        if len(clist) == 0:
            continue
        as_id = norm_inv_num(pr.get("as", "").split("/")[0]) if pr.get("as") else (inv_norm if inv_norm.startswith("AS") else "")
        out_cords = []
        for idx, oc in enumerate(clist):
            patch = thompson_patches.get((as_id, oc["cuerda"].lower())) if as_id else None
            row = {
                "kh_id": kh, "kfg_id": "", "orden": idx,
                "cuerda": oc["cuerda"], "tipo": oc["tipo"], "nivel": oc["nivel"],
                "padre": oc["padre"], "grupo": oc["grupo"],
                "valor": oc["valor"], "valor_thompson": patch[0] if patch else oc["valor"],
                "alt": "", "nudos": oc["nudos"],
                "color": oc["color"], "color_base": oc["color_base"],
                "lab_L": oc["lab_L"], "lab_a": oc["lab_a"], "lab_b": oc["lab_b"],
                "torsion": oc["torsion"], "union": oc["union"],
                "largo": oc["largo"], "terminacion": oc["terminacion"], "notas": oc["notas"],
                "fuente_cuerda": "okr_heldout", "thompson_flag": "valor_parcheado" if patch else "",
                "held_out": 1,
                "cord_classification": oc["cord_classification"],
                "fiber": oc["fiber"], "thickness": oc["thickness"], "twist_angle": oc["twist_angle"],
                "cluster_ordinal": oc["cluster_ordinal"], "cluster_pos_cm": oc["cluster_pos_cm"],
                "cluster_spacing_cm": oc["cluster_spacing_cm"],
                "knot_n_clusters": oc["knot_n_clusters"],
                "knot_first_pos_cm": oc["knot_first_pos_cm"],
                "knot_last_pos_cm": oc["knot_last_pos_cm"],
                "knot_positions_cm": oc["knot_positions_cm"],
                "knot_types": oc["knot_types"], "knot_dirs": oc["knot_dirs"],
                "created_by": oc["created_by"],
            }
            out_cords.append(row)
            maestro_cuerdas.append(row)
        stats["heldout_okr_db"] += 1
        maestro_quipus[kh] = {
            "kh_id": kh, "kfg_id": "", "okr_num": kh,
            "as_id": as_id, "ur_id": pr.get("ur", ""),
            "fuente_primaria": "okr_khipu_db",
            "en_kfg": 0, "en_okr": 1, "en_databook": 0, "held_out": 1,
            "museo": om.get("museo", "") or pr.get("museo", ""),
            "procedencia": om.get("procedencia", ""),
            "region": om.get("region", ""),
            "n_inventario": om.get("n_inventario", "") or pr.get("n_inventario", ""),
            "n_cuerdas": len(out_cords),
            "n_colgantes": sum(1 for c in out_cords if c["nivel"] == 0 and c["tipo"] == "p"),
            "n_superiores": sum(1 for c in out_cords if c["tipo"] == "t" or c["cord_classification"] == "T"),
            "n_marcadoras": sum(1 for c in out_cords if c["tipo"] == "m" or c["cord_classification"] == "M"),
            "thompson_n_notas": thompson_counts.get(as_id, 0) if as_id else 0,
            "reconstruido_kfg": 0, "created_by": om.get("created_by", ""),
        }

    # 3) Adjuntos OKR: cuerdas_extra.csv (19 quipus incl. RT-16905 KH0638-0651, SH001, British Museum, KH0702)
    #    y cuerdas_nuevas.csv (KH0674, KH0675, KH0676)
    for src_label, csv_path in [("okr_extra_xlsx", EXTRA_CSV), ("okr_transcritos_pdf", NUEVAS_CSV)]:
        by_q = defaultdict(list)
        with open(csv_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                by_q[r["kfg"].strip()].append(r)
        for qid, qrows in sorted(by_q.items()):
            canon = qid if qid.startswith("KH") else (by_alias.get(qid.upper(), qid))
            if canon in maestro_quipus:
                continue
            pr = by_kh.get(canon, {})
            out_cords = []
            for idx, r in enumerate(qrows):
                cbase, (L, a, b) = color_to_lab(r.get("color", ""), cmap)
                row = {
                    "kh_id": canon, "kfg_id": "", "orden": idx,
                    "cuerda": r["cuerda"], "tipo": r["tipo"], "nivel": int(r["nivel"]),
                    "padre": r["padre"], "grupo": r["grupo"],
                    "valor": r["valor"], "valor_thompson": r["valor"],
                    "alt": r.get("alt", ""), "nudos": r.get("nudos", ""),
                    "color": r.get("color", ""), "color_base": cbase,
                    "lab_L": L, "lab_a": a, "lab_b": b,
                    "torsion": r.get("torsion", ""), "union": r.get("union", ""),
                    "largo": r.get("largo", ""), "terminacion": r.get("terminacion", ""),
                    "notas": r.get("notas", ""),
                    "fuente_cuerda": src_label, "thompson_flag": "", "held_out": 1,
                    "cord_classification": "T" if r["tipo"] == "t" else ("M" if r["tipo"] == "m" else ""),
                    "fiber": "", "thickness": "", "twist_angle": "",
                    "cluster_ordinal": "", "cluster_pos_cm": "", "cluster_spacing_cm": "",
                    "knot_n_clusters": "", "knot_first_pos_cm": "", "knot_last_pos_cm": "",
                    "knot_positions_cm": "", "knot_types": "", "knot_dirs": "",
                    "created_by": src_label,
                }
                out_cords.append(row)
                maestro_cuerdas.append(row)
            stats[f"heldout_{src_label}"] += 1
            maestro_quipus[canon] = {
                "kh_id": canon, "kfg_id": "", "okr_num": canon if canon.startswith("KH") else "",
                "as_id": pr.get("as", ""), "ur_id": pr.get("ur", ""),
                "fuente_primaria": src_label,
                "en_kfg": 0, "en_okr": 1, "en_databook": 0, "held_out": 1,
                "museo": pr.get("museo", ""),
                "procedencia": "RT-16905 MNAAHP (decomiso)" if "KH0638" <= canon <= "KH0652" else "",
                "region": "",
                "n_inventario": "36.718" if canon == "KH0676" else pr.get("n_inventario", ""),
                "n_cuerdas": len(out_cords),
                "n_colgantes": sum(1 for c in out_cords if c["nivel"] == 0 and c["tipo"] == "p"),
                "n_superiores": sum(1 for c in out_cords if c["tipo"] == "t" or c["union"] == "T"),
                "n_marcadoras": sum(1 for c in out_cords if c["tipo"] == "m"),
                "thompson_n_notas": 0, "reconstruido_kfg": 0, "created_by": src_label,
            }

    # 4) Fichas JPG de Huacones-Vilcahuasi (KH0653-KH0663 = JC024-JC034)
    jc_to_kh = {f"JC{24 + i:03d}": f"KH{653 + i:04d}" for i in range(11)}
    for jc, kh in sorted(jc_to_kh.items()):
        fp = FICHAS_DIR / f"transcripcion_{jc}_record.csv"
        if not fp.exists() or kh in maestro_quipus:
            continue
        out_cords = []
        with open(fp, encoding="utf-8") as f:
            for idx, r in enumerate(csv.DictReader(f)):
                cname_raw = r["cuerda"].strip()
                cname = cname_raw if cname_raw.startswith(("p", "t", "m")) else f"p{cname_raw}"
                padre = cname[: max(cname.rfind("s"), 0)] if cname.count("s") and re.search(r"\ds\d", cname) else ""
                cbase, (L, a, b) = color_to_lab(r.get("color", ""), cmap)
                row = {
                    "kh_id": kh, "kfg_id": "", "orden": idx,
                    "cuerda": cname, "tipo": "p", "nivel": len(re.findall(r"s\d+", cname)),
                    "padre": padre, "grupo": 0,
                    "valor": r.get("valor", ""), "valor_thompson": r.get("valor", ""),
                    "alt": "", "nudos": r.get("nudos", ""),
                    "color": r.get("color", ""), "color_base": cbase,
                    "lab_L": L, "lab_a": a, "lab_b": b,
                    "torsion": "", "union": "", "largo": r.get("largo", ""),
                    "terminacion": "", "notas": r.get("notas", ""),
                    "fuente_cuerda": "okr_huacones_jpg", "thompson_flag": "", "held_out": 1,
                    "cord_classification": "", "fiber": "", "thickness": "", "twist_angle": "",
                    "cluster_ordinal": "", "cluster_pos_cm": "", "cluster_spacing_cm": "",
                    "knot_n_clusters": "", "knot_first_pos_cm": "", "knot_last_pos_cm": "",
                    "knot_positions_cm": "", "knot_types": "", "knot_dirs": "",
                    "created_by": "huacones_jpg",
                }
                out_cords.append(row)
                maestro_cuerdas.append(row)
        stats["heldout_huacones"] += 1
        pr = by_kh.get(kh, {})
        maestro_quipus[kh] = {
            "kh_id": kh, "kfg_id": "", "okr_num": kh,
            "as_id": "", "ur_id": jc,
            "fuente_primaria": "okr_huacones_jpg",
            "en_kfg": 0, "en_okr": 1, "en_databook": 0, "held_out": 1,
            "museo": "Sitio arqueológico Huacones-Vilcahuasi",
            "procedencia": "Huacones-Vilcahuasi, Cañete",
            "region": "South Coast",
            "n_inventario": pr.get("n_inventario", ""),
            "n_cuerdas": len(out_cords),
            "n_colgantes": sum(1 for c in out_cords if c["nivel"] == 0),
            "n_superiores": 0, "n_marcadoras": 0,
            "thompson_n_notas": 0, "reconstruido_kfg": 0, "created_by": "huacones_jpg",
        }

    # 5) Quipus del Databook genuinamente ausentes de KFG y OKR
    db_new = parse_missing_databook(set(maestro_quipus.keys()), base_kfg_set, by_alias, cmap)
    for canon, (qid, out_cords) in sorted(db_new.items()):
        if canon in maestro_quipus or len(out_cords) == 0:
            continue
        as_id = norm_inv_num(qid)
        for row in out_cords:
            patch = thompson_patches.get((as_id, row["cuerda"].lower()))
            row["valor_thompson"] = patch[0] if patch else row["valor"]
            row["thompson_flag"] = "valor_parcheado" if patch else ""
            row["held_out"] = 1
            maestro_cuerdas.append(row)
        stats["heldout_databook"] += 1
        pr = by_kh.get(canon, {})
        maestro_quipus[canon] = {
            "kh_id": canon, "kfg_id": "", "okr_num": canon if canon.startswith("KH") else "",
            "as_id": as_id, "ur_id": pr.get("ur", ""),
            "fuente_primaria": "databook_ocr",
            "en_kfg": 0, "en_okr": 0, "en_databook": 1, "held_out": 1,
            "museo": pr.get("museo", ""), "procedencia": "", "region": "",
            "n_inventario": pr.get("n_inventario", ""),
            "n_cuerdas": len(out_cords),
            "n_colgantes": sum(1 for c in out_cords if c["nivel"] == 0 and c["tipo"] == "p"),
            "n_superiores": sum(1 for c in out_cords if c["tipo"] == "t"),
            "n_marcadoras": 0,
            "thompson_n_notas": thompson_counts.get(as_id, 0),
            "reconstruido_kfg": 0, "created_by": "ascher_databook",
        }

    # 6) Auditar collca.db (solo para contabilizar cobertura frente a maestro)
    con_col = sqlite3.connect(f"file:{COLLCA_DB}?mode=ro", uri=True)
    col_invs = [r[0] for r in con_col.execute("SELECT INVESTIGATOR_NUM FROM khipu_main WHERE INVESTIGATOR_NUM IS NOT NULL AND INVESTIGATOR_NUM != ''").fetchall()]
    col_unmatched = []
    for inv in col_invs:
        ni = norm_inv_num(inv)
        kh = by_alias.get(inv.upper()) or by_alias.get(ni)
        if kh and kh in maestro_quipus:
            continue
        if ni in base_kfg_set or inv in base_kfg_set:
            continue
        col_unmatched.append(inv)

    # 7) Parsear K15 wrapped threads
    n_k15 = parse_k15_wrapped()

    # Escribir maestro_quipus.csv y maestro_cuerdas.csv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q_cols = [
        "kh_id", "kfg_id", "okr_num", "as_id", "ur_id", "fuente_primaria",
        "en_kfg", "en_okr", "en_databook", "held_out",
        "museo", "procedencia", "region", "n_inventario",
        "n_cuerdas", "n_colgantes", "n_superiores", "n_marcadoras",
        "thompson_n_notas", "reconstruido_kfg", "created_by",
    ]
    with open(OUT_DIR / "maestro_quipus.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=q_cols)
        w.writeheader()
        for kh in sorted(maestro_quipus.keys()):
            w.writerow(maestro_quipus[kh])

    c_cols = [
        "kh_id", "kfg_id", "orden", "cuerda", "tipo", "nivel", "padre", "grupo",
        "valor", "valor_thompson", "alt", "nudos", "color", "color_base",
        "lab_L", "lab_a", "lab_b", "torsion", "union", "largo", "terminacion", "notas",
        "fuente_cuerda", "thompson_flag", "held_out",
        "cord_classification", "fiber", "thickness", "twist_angle",
        "cluster_ordinal", "cluster_pos_cm", "cluster_spacing_cm",
        "knot_n_clusters", "knot_first_pos_cm", "knot_last_pos_cm",
        "knot_positions_cm", "knot_types", "knot_dirs", "created_by",
    ]
    with open(OUT_DIR / "maestro_cuerdas.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=c_cols)
        w.writeheader()
        w.writerows(maestro_cuerdas)

    n_total_q = len(maestro_quipus)
    n_base_q = sum(1 for q in maestro_quipus.values() if q["held_out"] == 0)
    n_ho_q = sum(1 for q in maestro_quipus.values() if q["held_out"] == 1)
    n_total_c = len(maestro_cuerdas)
    n_ho_c = sum(1 for c in maestro_cuerdas if c["held_out"] == 1)
    n_lab = sum(1 for c in maestro_cuerdas if c["lab_L"] != "")
    n_geom = sum(1 for c in maestro_cuerdas if c["cluster_pos_cm"] != "" or c["knot_first_pos_cm"] != "")

    # Auto-verificación determinista de valores OKR en Inkawasi (UR274B cuotas 17/10)
    ur274b_cords = [c for c in maestro_cuerdas if c["kfg_id"] == "UR274B"]
    ur274b_17 = sum(1 for c in ur274b_cords if c["valor"] == 17)
    ur274b_10 = sum(1 for c in ur274b_cords if c["valor"] == 10)
    assert ur274b_17 >= 12, f"Fallo de sanity-check OKR UR274B: cuotas 17={ur274b_17} (esperado >=12)"
    print(f"[OK] Sanity-check OKR Inkawasi UR274B: {len(ur274b_cords)} cuerdas, cuotas 17={ur274b_17}, cuotas 10={ur274b_10}")

    rep = f"""# Reporte de Integridad — Corpus Maestro Unificado de Quipus (`KH####`)

- **Quipus totales unificados:** **{n_total_q}** (+ `KH0652` / `MNAAHP.15` con {n_k15} hilos envueltos en `rt16905_k15_wrapped.csv`)
  - Base KFG distintos (sin duplicado `UR044`): **{n_base_q}**
  - **Cohorte `held_out` (nunca analizada en `quipus` v1):** **{n_ho_q} quipus ({n_ho_c} cuerdas)**
    - OKR `khipu.db` ausentes de KFG: {stats['heldout_okr_db']}
    - Adjuntos OKR xlsx (`cuerdas_extra`: RT-16905 `KH0638–0651`, `SH001`, British Museum `KH0633–0635`, `KH0702`): {stats['heldout_okr_extra_xlsx']}
    - Adjuntos OKR transcritos de PDF/xlsx (`KH0674`, `KH0675`, `KH0676`): {stats['heldout_okr_transcritos_pdf']}
    - Huacones-Vilcahuasi (`KH0653–KH0663`, fichas JPG): {stats['heldout_huacones']}
    - Databook de Ascher genuinamente ausentes de KFG y OKR (tras resolver alias `UR1xxx` vía `puente.csv`): {stats['heldout_databook']}
- **Cuerdas totales unificadas:** **{n_total_c}**
  - Con coordenadas perceptuales CIE $L^*a^*b^*$ (`ascher_color_dc`): **{n_lab}** ({100*n_lab/n_total_c:.1f} %)
  - Con geometría física 2D de OKR (posición de clúster o nudo en cm): **{n_geom}** ({100*n_geom/n_total_c:.1f} %)
  - Cuerdas superiores (`T`) rescatadas de OKR en quipus base: **{stats['rescatadas_okr_T']}**
  - Cuerdas marcadoras (`M`) rescatadas de OKR en quipus base: **{stats['rescatadas_okr_M']}**
  - Quipus base reemplazados por OKR preferente (4 desplazados + Inkawasi UR): **{stats['kfg_reemplazados_por_okr']}**
  - Parches deterministas de valor de Thompson (2025a) aplicados en columna `valor_thompson` (sin sobrescribir `valor`): **{stats['thompson_parches_aplicados']}** (222 notas en 108 quipus AS en `thompson_2025_correcciones.csv`)
- **Hallazgo de conciliación Databook / `collca.db`:**
  - Los "80 quipus del Databook ausentes de KFG" de `ds/n_databook` eran en su mayoría colisiones de alias (`AS###` registrado como `UR1xxx` en KFG). Al resolver por `puente.csv` (`KH####`), los genuinamente ausentes de KFG y OKR son **{stats['heldout_databook']}** (más los presentes solo en `khipu.db` como `AS086`, `AS130B`, `AS181`, `AS190`, `AS208`).
  - Entradas en `collca.db` sin cruce directo por alias simple ({len(col_unmatched)}): `{', '.join(sorted(set(col_unmatched))[:25])}` (en su mayoría variantes de nombre o sin fila en OKR).
"""
    (OUT_DIR / "reporte_integridad.md").write_text(rep, encoding="utf-8")
    print(rep)

if __name__ == "__main__":
    main()
