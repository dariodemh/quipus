#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_ejecutar_P04_cielab_geometria.py — Ejecución estricta del Preregistro P04 (v1.1, SHA-256 sellado).

Familia confirmatoria (Holm exacto sobre m = 4):
  - P04.1: Invariancia perceptual CIELAB (Delta E 2000) entre transcriptores distintos en dobles lecturas y copias
  - P04.2: Gradiente continuo de luminancia (L*) vs log1p(valor) intra-grupo, estratificado por transcriptor (y sin W)
  - P04.3: Segmentación física por huecos en cm (k = 2,0 fijado antes del hash) y replicación de T4 (tendencias)
  - P04.4: «Manos de quipucamayoc» (geometría física 2D independiente del valor) en archivos cerrados,
           estratificado por (sitio, CREATED_BY)

Control descriptivo obligatorio fuera de Holm:
  - D04.5: Descomposición de varianza (PERMANOVA parcial) entre CREATED_BY, museo, sitio y vínculo aritmético.

Semilla fija: 20261127.
"""
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[1]
MAESTRO = DIR.parent / "36_corpus_maestro"
SEED = 20261127


def holm_adjust(pvals):
    valid = [(k, v) for k, v in pvals.items() if v is not None]
    m = len(valid)
    order = sorted(valid, key=lambda x: x[1])
    adj = {}
    rmax = 0.0
    for i, (k, p) in enumerate(order):
        val = min(1.0, (m - i) * p)
        rmax = max(rmax, val)
        adj[k] = rmax
    for k, v in pvals.items():
        if v is None:
            adj[k] = None
    return adj


def to_float(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def to_int(x):
    if x is None or x == "":
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


def ciede2000(lab1, lab2):
    """Distancia perceptual exacta CIE Delta E 2000 entre (L1,a1,b1) y (L2,a2,b2)."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    C_bar = 0.5 * (C1 + C2)
    C_bar7 = C_bar ** 7
    G = 0.5 * (1.0 - math.sqrt(C_bar7 / (C_bar7 + 25.0 ** 7)))
    a1p = (1.0 + G) * a1
    a2p = (1.0 + G) * a2
    C1p = math.hypot(a1p, b1)
    C2p = math.hypot(a2p, b2)

    def hp_fn(ap, b):
        if ap == 0 and b == 0:
            return 0.0
        ang = math.degrees(math.atan2(b, ap))
        return ang + 360.0 if ang < 0 else ang

    h1p = hp_fn(a1p, b1)
    h2p = hp_fn(a2p, b2)
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        diff = h2p - h1p
        if abs(diff) <= 180.0:
            dhp = diff
        elif diff > 180.0:
            dhp = diff - 360.0
        else:
            dhp = diff + 360.0
    dHp = 2.0 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2.0))
    Lbp = 0.5 * (L1 + L2)
    Cbp = 0.5 * (C1p + C2p)
    if C1p * C2p == 0:
        hbp = h1p + h2p
    else:
        if abs(h1p - h2p) <= 180.0:
            hbp = 0.5 * (h1p + h2p)
        elif (h1p + h2p) < 360.0:
            hbp = 0.5 * (h1p + h2p + 360.0)
        else:
            hbp = 0.5 * (h1p + h2p - 360.0)
    T = (1.0
         - 0.17 * math.cos(math.radians(hbp - 30.0))
         + 0.24 * math.cos(math.radians(2.0 * hbp))
         + 0.32 * math.cos(math.radians(3.0 * hbp + 6.0))
         - 0.20 * math.cos(math.radians(4.0 * hbp - 63.0)))
    d_theta = 30.0 * math.exp(-(((hbp - 275.0) / 25.0) ** 2))
    Cbp7 = Cbp ** 7
    RC = 2.0 * math.sqrt(Cbp7 / (Cbp7 + 25.0 ** 7))
    SL = 1.0 + (0.015 * ((Lbp - 50.0) ** 2)) / math.sqrt(20.0 + ((Lbp - 50.0) ** 2))
    SC = 1.0 + 0.045 * Cbp
    SH = 1.0 + 0.015 * Cbp * T
    RT = -math.sin(math.radians(2.0 * d_theta)) * RC
    return math.sqrt(
        (dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2 + RT * (dCp / SC) * (dHp / SH)
    )


def load_master():
    quipus = {}
    kfg_to_kh = {}
    with open(MAESTRO / "maestro_quipus.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            quipus[r["kh_id"]] = r
            if r["kfg_id"]:
                kfg_to_kh[r["kfg_id"]] = r["kh_id"]
    cords_by_q = defaultdict(list)
    with open(MAESTRO / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cords_by_q[r["kh_id"]].append(r)
    return quipus, kfg_to_kh, cords_by_q


def series_of_kfg(kfg_id: str) -> str:
    m = re.match(r"^([A-Z]+)", kfg_id or "")
    if not m:
        return "OTHER"
    p = m.group(1)
    if p == "UR" and re.match(r"^UR1\d{3}", kfg_id or ""):
        return "AS"  # En KFG/24_color_formato, UR1xxx proviene de transcripciones de Ascher
    return p


def test_p04_1_cielab_invariance(quipus, kfg_to_kh, cords_by_q, rng):
    """P04.1: Delta E 2000 en pares alineados de 14_copias/filas_alineadas.csv con investigadores distintos."""
    # Construir mapa (kfg_id, cuerda) -> (L,a,b) y color_base
    lab_lookup = {}
    col_lookup = {}
    for kh, cs in cords_by_q.items():
        kfg = quipus[kh]["kfg_id"] or kh
        for c in cs:
            L, a, b = to_float(c["lab_L"]), to_float(c["lab_a"]), to_float(c["lab_b"])
            if L is not None and a is not None and b is not None:
                lab_lookup[(kfg, c["cuerda"])] = (L, a, b)
                lab_lookup[(kh, c["cuerda"])] = (L, a, b)
            col_lookup[(kfg, c["cuerda"])] = c["color_base"]

    filas_path = RAIZ / "analisis/14_copias/filas_alineadas.csv"
    pair_rows = defaultdict(list)
    with open(filas_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q1, q2 = r["A"].strip(), r["B"].strip()
            c1, c2 = r["cuerda_A"].strip(), r["cuerda_B"].strip()
            if (q1, c1) in lab_lookup and (q2, c2) in lab_lookup:
                pair_rows[(q1, q2)].append((
                    lab_lookup[(q1, c1)], lab_lookup[(q2, c2)],
                    col_lookup.get((q1, c1), ""), col_lookup.get((q2, c2), ""),
                ))

    # Añadir explícitamente UR1107 vs UR237 (invertido) si no está con suficientes filas
    if ("UR1107", "UR237") not in pair_rows and ("UR237", "UR1107") not in pair_rows:
        c1 = [c for c in cords_by_q[kfg_to_kh["UR1107"]] if c["nivel"] == "0" and c["tipo"] == "p"]
        c2 = [c for c in cords_by_q[kfg_to_kh["UR237"]] if c["nivel"] == "0" and c["tipo"] == "p"][::-1]
        for a_c, b_c in zip(c1, c2):
            la = (to_float(a_c["lab_L"]), to_float(a_c["lab_a"]), to_float(a_c["lab_b"]))
            lb = (to_float(b_c["lab_L"]), to_float(b_c["lab_a"]), to_float(b_c["lab_b"]))
            if None not in la and None not in lb:
                pair_rows[("UR1107", "UR237")].append((la, lb, a_c["color_base"], b_c["color_base"]))

    cross_pairs = []
    same_pairs = []
    for (q1, q2), items in sorted(pair_rows.items()):
        if len(items) < 8:
            continue
        s1, s2 = series_of_kfg(q1), series_of_kfg(q2)
        labs1 = [x[0] for x in items]
        labs2 = [x[1] for x in items]
        # Verificar que haya al menos 2 colores distintos en ambos
        if len(set(labs1)) < 2 or len(set(labs2)) < 2:
            continue
        obs_de = float(np.median([ciede2000(u, v) for u, v in zip(labs1, labs2)]))
        exact_rate = float(np.mean([1.0 if x[2] == x[3] else 0.0 for x in items]))
        r_L = float(stats.spearmanr([u[0] for u in labs1], [v[0] for v in labs2]).statistic)
        if np.isnan(r_L):
            r_L = 0.0

        # Nulo: permutar labs2 dentro del par (2 000 réplicas internas; 5 000 para el agregado)
        B = 2000
        null_des = np.empty(B, dtype=float)
        idx_arr = np.arange(len(labs2))
        for b_i in range(B):
            perm = rng.permutation(idx_arr)
            null_des[b_i] = np.median([ciede2000(labs1[k], labs2[perm[k]]) for k in range(len(labs1))])
        med_null = float(np.median(null_des))
        ratio = obs_de / med_null if med_null > 0 else 1.0
        p_pair = float((np.sum(null_des <= obs_de + 1e-12) + 1) / (B + 1))

        rec = {
            "par": f"{q1}~{q2}", "series": f"{s1}-{s2}", "n": len(items),
            "exact_label_rate": round(exact_rate, 3),
            "obs_dE2000": round(obs_de, 2), "null_dE2000": round(med_null, 2),
            "ratio_dE": round(ratio, 4), "spearman_L": round(r_L, 3), "p_pair": round(p_pair, 5),
            "_null_vec": null_des,
        }
        if s1 != s2:
            cross_pairs.append(rec)
        else:
            same_pairs.append(rec)

    if not cross_pairs:
        return {"test_id": "P04.1", "status": "SIN_POTENCIA", "p": None}

    # Agregado sobre pares con distintos investigadores (unidad = par)
    obs_ratio_med = float(np.median([x["ratio_dE"] for x in cross_pairs]))
    # Distribución nula del ratio mediano usando las 2000 réplicas independientes de cada par
    B = len(cross_pairs[0]["_null_vec"])
    null_ratios_mat = np.array([x["_null_vec"] / max(x["null_dE2000"], 1e-6) for x in cross_pairs])
    null_meds = np.median(null_ratios_mat, axis=0)
    p_agg = float((np.sum(null_meds <= obs_ratio_med + 1e-12) + 1) / (B + 1))

    clean_cross = [{k: v for k, v in x.items() if k != "_null_vec"} for x in cross_pairs]
    clean_same = [{k: v for k, v in x.items() if k != "_null_vec"} for x in same_pairs]
    return {
        "test_id": "P04.1",
        "n_pares_distinto_investigador": len(clean_cross),
        "n_pares_mismo_investigador": len(clean_same),
        "obs_ratio_dE_mediano": round(obs_ratio_med, 4),
        "mediana_exact_label_cross": round(float(np.median([x["exact_label_rate"] for x in clean_cross])), 3),
        "mediana_spearman_L_cross": round(float(np.median([x["spearman_L"] for x in clean_cross])), 3),
        "p": round(p_agg, 6),
        "pares_cross": clean_cross,
        "status": "EVALUADO",
    }


def test_p04_2_luminancia_magnitud(quipus, cords_by_q, rng):
    """P04.2: Correlación intra-grupo Spearman(L*, log1p(valor)) estratificada por transcriptor (con y sin W)."""
    def run_pass(exclude_W=False):
        by_trans = defaultdict(list)  # trans -> list of (kh, obs_rho, groups_data)
        for kh, q in quipus.items():
            trans = series_of_kfg(q["kfg_id"] or q["ur_id"] or q["as_id"] or kh)
            by_g = defaultdict(list)
            all_L = []
            for c in cords_by_q[kh]:
                if c["nivel"] != "0" or c["tipo"] != "p":
                    continue
                if exclude_W and c["color_base"] == "W":
                    continue
                v = to_int(c["valor"])
                L = to_float(c["lab_L"])
                g = to_int(c["grupo"])
                if v is not None and v > 0 and L is not None and g is not None:
                    by_g[g].append((L, math.log1p(v)))
                    all_L.append(L)
            n_tot = sum(len(x) for x in by_g.values())
            if n_tot < 15 or len(set(all_L)) < 2:
                continue
            # Calcular rho intra-grupo promedio ponderado por tamaño de grupo (en grupos con >=3 y >=2 L)
            g_rhos = []
            valid_gs = []
            for g, pts in by_g.items():
                if len(pts) >= 3 and len(set(p[0] for p in pts)) >= 2 and len(set(p[1] for p in pts)) >= 2:
                    r = float(stats.spearmanr([p[0] for p in pts], [p[1] for p in pts]).statistic)
                    if not np.isnan(r):
                        g_rhos.append(r)
                        valid_gs.append(pts)
            if not g_rhos:
                continue
            by_trans[trans].append((kh, float(np.mean(g_rhos)), valid_gs))

        # Estadístico global y por transcriptor (UR, AS)
        all_items = [it for lst in by_trans.values() for it in lst]
        obs_med = float(np.median([x[1] for x in all_items]))
        by_t_med = {t: {"n": len(lst), "med_rho": round(float(np.median([x[1] for x in lst])), 4)}
                    for t, lst in sorted(by_trans.items()) if len(lst) >= 5}

        # Nulo vectorizado: precomputar rangos estandarizados por grupo (exacto a Spearman, 500x más rápido)
        B = 2000
        q_null_mat = np.empty((len(all_items), B), dtype=np.float32)
        for qi, (_kh, _obs, vgs) in enumerate(all_items):
            g_sum = np.zeros(B, dtype=np.float64)
            for pts in vgs:
                m = len(pts)
                rl = stats.rankdata([p[0] for p in pts])
                rv = stats.rankdata([p[1] for p in pts])
                rl = rl - rl.mean()
                rv = rv - rv.mean()
                denom = math.sqrt(float(np.dot(rl, rl) * np.dot(rv, rv)))
                if denom <= 0:
                    continue
                rl_u = rl / math.sqrt(float(np.dot(rl, rl)))
                rv_u = rv / math.sqrt(float(np.dot(rv, rv)))
                # Generar B permutaciones de rl_u en bloque
                idx = np.argsort(rng.random((B, m)), axis=1)
                g_sum += rl_u[idx] @ rv_u
            q_null_mat[qi, :] = g_sum / len(vgs)
        null_meds = np.median(q_null_mat, axis=0)
        p = float((np.sum(np.abs(null_meds) >= abs(obs_med) - 1e-12) + 1) / (B + 1))
        return {"n_quipus": len(all_items), "med_rho_global": round(obs_med, 4), "por_transcriptor": by_t_med, "p": round(p, 6)}

    con_W = run_pass(exclude_W=False)
    sin_W = run_pass(exclude_W=True)
    ur_s = con_W["por_transcriptor"].get("UR", {}).get("med_rho", 0)
    as_s = con_W["por_transcriptor"].get("AS", {}).get("med_rho", 0)
    same_sign = (ur_s * as_s) > 0
    return {
        "test_id": "P04.2",
        "con_W": con_W,
        "sin_W": sin_W,
        "mismo_signo_UR_AS": same_sign,
        "p": max(con_W["p"], sin_W["p"]),  # Exigimos que sobreviva a ambos
        "status": "EVALUADO",
    }


def test_p04_3_segmentacion_fisica_T4(quipus, cords_by_q, rng):
    """P04.3: Segmentación física por huecos en cm (k=2.0, min 0.5 cm) y replicación de T4."""
    elig_q = 0
    sig_q = 0
    sig_list = []

    for kh, q in quipus.items():
        # Extraer colgantes nivel 0 con cluster_pos_cm y cluster_spacing_cm en OKR
        p_cords = [c for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
        # Agrupar por cluster_ordinal de OKR para obtener posiciones físicas de cada clúster
        by_cl = {}
        cl_vals = defaultdict(list)
        for c in p_cords:
            co = to_int(c["cluster_ordinal"])
            pos = to_float(c["cluster_pos_cm"])
            spc = to_float(c["cluster_spacing_cm"])
            v = to_int(c["valor"])
            if co is not None and pos is not None:
                by_cl[co] = (pos, spc if spc is not None else 0.0)
                if v is not None and v > 0:
                    cl_vals[co].append(v)
        if len(by_cl) < 4:
            continue
        sorted_cls = sorted(by_cl.keys(), key=lambda k: by_cl[k][0])
        gaps = [by_cl[sorted_cls[i + 1]][0] - by_cl[sorted_cls[i]][0] for i in range(len(sorted_cls) - 1)]
        pos_gaps = [g for g in gaps if g > 0]
        if not pos_gaps:
            continue
        thresh = max(0.5, 2.0 * float(np.median(pos_gaps)))
        # Cortar en grupos físicos donde el salto entre clústeres > thresh
        phys_groups = []
        cur = list(cl_vals[sorted_cls[0]])
        for i, gap in enumerate(gaps):
            if gap > thresh:
                phys_groups.append(cur)
                cur = list(cl_vals[sorted_cls[i + 1]])
            else:
                cur.extend(cl_vals[sorted_cls[i + 1]])
        phys_groups.append(cur)
        phys_groups = [g for g in phys_groups if len(g) >= 4 and len(set(g)) >= 3]
        if len(phys_groups) < 3:
            continue

        elig_q += 1
        taus = [abs(float(stats.kendalltau(range(len(g)), g).statistic)) for g in phys_groups]
        obs_t = float(np.mean(taus))
        B = 500
        ge = 0
        for _ in range(B):
            tp = [abs(float(stats.kendalltau(range(len(g)), rng.permutation(g)).statistic)) for g in phys_groups]
            if float(np.mean(tp)) >= obs_t - 1e-12:
                ge += 1
        p_q = (ge + 1) / (B + 1)
        if p_q < 0.05:
            sig_q += 1
            sig_list.append({"kh_id": kh, "kfg": q["kfg_id"], "n_phys_grps": len(phys_groups), "mean_abs_tau": round(obs_t, 3), "p": round(p_q, 4)})

    if elig_q < 10:
        return {"test_id": "P04.3", "status": "SIN_POTENCIA", "n_quipus": elig_q, "p": None}
    p_bin = float(stats.binomtest(sig_q, elig_q, 0.05, alternative="greater").pvalue)
    return {
        "test_id": "P04.3",
        "n_quipus_elegibles": elig_q,
        "n_sig_p005": sig_q,
        "exp_p005": round(elig_q * 0.05, 2),
        "tasa_obs": round(sig_q / elig_q, 4),
        "p": round(p_bin, 6),
        "top_sig": sorted(sig_list, key=lambda x: x["p"])[:8],
        "status": "EVALUADO",
    }


def test_p04_4_y_d04_5_manos(quipus, kfg_to_kh, cords_by_q, rng):
    """P04.4: Manos de quipucamayoc (geometría física 2D independiente del valor) + D04.5 PERMANOVA."""
    # Archivos cerrados congelados: Inkawasi, Puruchuco, Leymebamba, Pachacamac
    def site_bucket(q):
        pr = (q["procedencia"] + " " + q["museo"]).lower()
        if "incahuasi" in pr or "inkawasi" in pr:
            return "Inkawasi"
        if "puruchuco" in pr:
            return "Puruchuco"
        if "leymebamba" in pr or "cóndores" in pr or "condores" in pr or "mallqui" in pr:
            return "Leymebamba"
        if "pachacamac" in pr:
            return "Pachacamac"
        return ""

    # Cargar pares vinculados aritméticamente o copias verificadas (14_copias + 33_estematica + Inkawasi + Puruchuco)
    linked_pairs = set()
    pares_path = RAIZ / "analisis/33_estematica/pares_copia.csv"
    if pares_path.exists():
        with open(pares_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("nivel", "").startswith(("bien", "apoyado")):
                    k1 = kfg_to_kh.get(r["kfg_a"], r["kfg_a"])
                    k2 = kfg_to_kh.get(r["kfg_b"], r["kfg_b"])
                    linked_pairs.add((min(k1, k2), max(k1, k2)))
    # Añadir enlaces aritméticos conocidos de Inkawasi y Puruchuco
    for a, b in [
        ("UR270", "UR278"), ("UR278", "UR266"), ("UR278", "UR275"), ("UR266", "UR275"),
        ("UR273A", "UR273B"), ("UR273A", "UR274A"), ("UR273B", "UR274B"),
        ("UR255", "UR267A"), ("UR256", "UR267B"),
        ("UR068", "UR067"), ("UR068", "UR066"), ("UR063", "UR068"), ("UR064", "UR068"),
    ]:
        if a in kfg_to_kh and b in kfg_to_kh:
            k1, k2 = kfg_to_kh[a], kfg_to_kh[b]
            linked_pairs.add((min(k1, k2), max(k1, k2)))

    # Construir vector geométrico 2D estrictamente independiente del valor por quipu
    q_vecs = {}
    q_meta = {}
    for kh, q in quipus.items():
        sb = site_bucket(q)
        if not sb:
            continue
        cs = [c for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
        if len(cs) < 8:
            continue
        # 1) Largo mediano de colgantes SIN nudos (o de 1 solo racimo si no hay sin nudos)
        len_un = [to_float(c["largo"]) for c in cs if to_int(c["knot_n_clusters"]) == 0 and to_float(c["largo"]) and to_float(c["largo"]) > 0]
        if len(len_un) < 3:
            len_un = [to_float(c["largo"]) for c in cs if to_float(c["largo"]) and to_float(c["largo"]) > 0]
        f1_len = float(np.median(len_un)) if len_un else np.nan

        # 2) Grosor (thickness) mediano
        thks = [to_float(c["thickness"]) for c in cs if to_float(c["thickness"]) and to_float(c["thickness"]) > 0]
        f2_thk = float(np.median(thks)) if thks else np.nan

        # 3) Espaciado físico mediano en el cordón principal
        spcs = [to_float(c["cluster_spacing_cm"]) for c in cs if to_float(c["cluster_spacing_cm"]) and to_float(c["cluster_spacing_cm"]) > 0]
        f3_spc = float(np.median(spcs)) if spcs else np.nan

        # 4) Posición normalizada del nudo de unidades SOLO en cuerdas con exactamente 1 racimo de unidades (L o E)
        u_rel = []
        # 5) Altura física absoluta del único racimo en cuerdas de 1 solo racimo
        s1_pos = []
        for c in cs:
            if to_int(c["knot_n_clusters"]) == 1:
                fp = to_float(c["knot_first_pos_cm"])
                lg = to_float(c["largo"])
                kt = c.get("knot_types", "")
                if fp is not None and fp > 0:
                    s1_pos.append(fp)
                    if lg is not None and lg > fp and ("L" in kt or "E" in kt):
                        u_rel.append(fp / lg)
        f4_urel = float(np.median(u_rel)) if len(u_rel) >= 3 else np.nan
        f5_s1p = float(np.median(s1_pos)) if len(s1_pos) >= 3 else np.nan

        vec = [f1_len, f2_thk, f3_spc, f4_urel, f5_s1p]
        if sum(1 for x in vec if not np.isnan(x)) >= 3:
            q_vecs[kh] = vec
            q_meta[kh] = {"sitio": sb, "created_by": q["created_by"] or "UNKNOWN", "museo": q["museo"]}

    # Imputar faltantes por mediana global de la muestra y estandarizar z-score
    khs = sorted(q_vecs.keys())
    M = np.array([q_vecs[k] for k in khs], dtype=float)
    for j in range(M.shape[1]):
        col = M[:, j]
        med = np.nanmedian(col)
        col[np.isnan(col)] = med if not np.isnan(med) else 0.0
        sd = np.std(col)
        M[:, j] = (col - np.mean(col)) / (sd if sd > 1e-8 else 1.0)
    z_by_kh = {k: M[i] for i, k in enumerate(khs)}

    # Evaluar dentro de estratos (sitio, created_by) que tengan >=1 par enlazado y >=1 par no enlazado
    strata = defaultdict(list)
    for k in khs:
        strata[(q_meta[k]["sitio"], q_meta[k]["created_by"])].append(k)

    valid_strata = []
    obs_diffs = []
    n_linked_tot = 0
    n_unlinked_tot = 0
    for st, members in sorted(strata.items()):
        if len(members) < 4:
            continue
        m_len = len(members)
        D = np.zeros((m_len, m_len), dtype=float)
        Lmat = np.zeros((m_len, m_len), dtype=bool)
        for i in range(m_len):
            for j in range(i + 1, m_len):
                D[i, j] = D[j, i] = float(np.linalg.norm(z_by_kh[members[i]] - z_by_kh[members[j]]))
                pair = (min(members[i], members[j]), max(members[i], members[j]))
                if pair in linked_pairs:
                    Lmat[i, j] = Lmat[j, i] = True
        nl = int(Lmat.sum() // 2)
        nu = (m_len * (m_len - 1) // 2) - nl
        if nl >= 1 and nu >= 2:
            valid_strata.append((st, members, D, Lmat, nl, nu))
            n_linked_tot += nl
            n_unlinked_tot += nu

    if not valid_strata:
        r4 = {"test_id": "P04.4", "status": "SIN_POTENCIA", "p": None, "n_estratos": 0}
    else:
        def calc_stat(strata_list, perm_flag=False):
            d_l, d_u = [], []
            for _st, _m, D, Lmat, _nl, _nu in strata_list:
                if perm_flag:
                    perm = rng.permutation(D.shape[0])
                    Lm = Lmat[np.ix_(perm, perm)]
                else:
                    Lm = Lmat
                iu, ju = np.triu_indices(D.shape[0], k=1)
                mask = Lm[iu, ju]
                d_l.extend(D[iu, ju][mask].tolist())
                d_u.extend(D[iu, ju][~mask].tolist())
            return float(np.mean(d_u) - np.mean(d_l)), float(np.mean(d_l)), float(np.mean(d_u))

        obs_diff, mean_l, mean_u = calc_stat(valid_strata, perm_flag=False)
        B = 5000
        ge = 0
        for _ in range(B):
            dp, _, _ = calc_stat(valid_strata, perm_flag=True)
            if dp >= obs_diff - 1e-12:
                ge += 1
        p_044 = (ge + 1) / (B + 1)
        r4 = {
            "test_id": "P04.4",
            "n_estratos_sitio_capturista": len(valid_strata),
            "estratos": [{"estrato": f"{st[0]}|{st[1]}", "n_quipus": len(m), "n_enlazados": nl} for st, m, _, _, nl, _ in valid_strata],
            "n_pares_enlazados": n_linked_tot,
            "n_pares_no_enlazados": n_unlinked_tot,
            "dist_media_enlazados": round(mean_l, 4),
            "dist_media_no_enlazados": round(mean_u, 4),
            "diff_no_menos_enlazados": round(obs_diff, 4),
            "p": round(p_044, 6),
            "status": "EVALUADO",
        }

    # D04.5: PERMANOVA (R2 de sitio vs CREATED_BY sobre la matriz de distancias euclídeas global)
    N_all = len(khs)
    D_all = np.zeros((N_all, N_all), dtype=float)
    for i in range(N_all):
        for j in range(i + 1, N_all):
            D_all[i, j] = D_all[j, i] = float(np.linalg.norm(M[i] - M[j]))
    SS_tot = float(np.sum(D_all ** 2) / (2.0 * N_all))

    def permanova_r2(labels):
        by_lbl = defaultdict(list)
        for idx, lb in enumerate(labels):
            by_lbl[lb].append(idx)
        ss_w = 0.0
        for idxs in by_lbl.values():
            if len(idxs) > 1:
                sub = D_all[np.ix_(idxs, idxs)]
                ss_w += float(np.sum(sub ** 2) / (2.0 * len(idxs)))
        return max(0.0, (SS_tot - ss_w) / SS_tot) if SS_tot > 0 else 0.0

    r2_sitio = permanova_r2([q_meta[k]["sitio"] for k in khs])
    r2_cb = permanova_r2([q_meta[k]["created_by"] for k in khs])
    r2_museo = permanova_r2([q_meta[k]["museo"] for k in khs])
    # R2 de CREATED_BY dentro de Inkawasi solo (si hay >1 capturista)
    ink_idx = [i for i, k in enumerate(khs) if q_meta[k]["sitio"] == "Inkawasi"]
    ink_cbs = [q_meta[khs[i]]["created_by"] for i in ink_idx]
    d5 = {
        "test_id": "D04.5",
        "n_quipus": N_all,
        "R2_sitio": round(r2_sitio, 4),
        "R2_created_by": round(r2_cb, 4),
        "R2_museo": round(r2_museo, 4),
        "inkawasi_capturistas": dict(Counter(ink_cbs)),
        "alerta_confusion": r2_cb > r2_sitio,
    }
    return r4, d5


def main():
    rng = np.random.default_rng(SEED)
    quipus, kfg_to_kh, cords_by_q = load_master()

    r1 = test_p04_1_cielab_invariance(quipus, kfg_to_kh, cords_by_q, rng)
    r2 = test_p04_2_luminancia_magnitud(quipus, cords_by_q, rng)
    r3 = test_p04_3_segmentacion_fisica_T4(quipus, cords_by_q, rng)
    r4, d5 = test_p04_4_y_d04_5_manos(quipus, kfg_to_kh, cords_by_q, rng)

    p_map = {r["test_id"]: r["p"] for r in (r1, r2, r3, r4)}
    h_map = holm_adjust(p_map)
    for r in (r1, r2, r3, r4):
        r["p_holm"] = round(h_map[r["test_id"]], 6) if h_map[r["test_id"]] is not None else None

    out = {
        "preregistro": "P04_cielab_y_geometria_2d.md",
        "semilla": SEED,
        "familia_holm": [r1, r2, r3, r4],
        "descriptivo_D04_5": d5,
    }
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "resultados_P04.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESULTADOS PREREGISTRO P04 (CIELAB + GEOMETRÍA 2D) ===")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']}: status={r['status']} | p={r['p']} | p_Holm={r['p_holm']}")
    print("  P04.1 CIELAB cross:", {k: r1[k] for k in ("n_pares_distinto_investigador", "obs_ratio_dE_mediano", "mediana_exact_label_cross", "mediana_spearman_L_cross", "p", "p_holm") if k in r1})
    print("  P04.2 Luminancia:", {"con_W": r2["con_W"], "sin_W": r2["sin_W"], "mismo_signo_UR_AS": r2["mismo_signo_UR_AS"]})
    print("  P04.3 Segmentación física T4:", {k: r3[k] for k in ("n_quipus_elegibles", "n_sig_p005", "exp_p005", "tasa_obs", "p", "p_holm") if k in r3})
    print("  P04.4 Manos 2D:", {k: r4[k] for k in ("n_estratos_sitio_capturista", "n_pares_enlazados", "dist_media_enlazados", "dist_media_no_enlazados", "diff_no_menos_enlazados", "p", "p_holm") if k in r4})
    print("  D04.5 PERMANOVA:", d5)


if __name__ == "__main__":
    main()
