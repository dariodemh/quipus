#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_ejecutar_P03_huacones_y_abiertos.py — Ejecución estricta del Preregistro P03 (v1.1, SHA-256 sellado).

Familia confirmatoria preregistrada (Holm exacto sobre m = 5):
  - P03.1: Huacones-Vilcahuasi (JC031 = Quipu 9, JC024 = Quipu 8) — Predicción #13
  - P03.2: Chirinos (2026) — Sumas de tramos contiguos en UR053E -> UR053B/C (por color y trío)
  - P03.3: Los 4 quipus sin leer del montón de maní de Inkawasi (UR272, UR276, UR277, UR279) con OKR
  - P03.4: KH0674 (Dumbarton Oaks, 41 grupos) — ¿cuerda resumen por grupo?
  - P03.5: Búsqueda Damerow-Englund de bases/radices mixtas (r1, r2) != (10,10) con nulo optimizado

Auditorías post-hoc y descriptivas fuera de Holm:
  - E03.6: Auditoría post-hoc de QU005 (B2 = B0 + B1) corrigiendo por todas las particiones de 3 bloques
  - E03.7: Exploratorio Inkawasi cuotas 46/44 en UR272/276/277/279 y filas 0-20 de UR278
  - D03.8: Auditoría descriptiva de las 116 notas aritméticas de Ascher (`notas_ascher.csv`)
  - D03.9: Comparación descriptiva Huacones-Vilcahuasi vs Inkawasi sector A (UR) y sector B (JC).

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


def to_int(x):
    if x is None or x == "":
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


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


def test_p03_1_huacones(quipus, cords_by_q, rng):
    """P03.1: Predicción #13 sobre JC031 (KH0660, Quipu 9) y JC024 (KH0653, Quipu 8)."""
    res = {}
    rhos = []
    p_indiv = []
    for label, kh in [("JC031_Quipu9", "KH0660"), ("JC024_Quipu8", "KH0653")]:
        cs = [c for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
        vals_all = [to_int(c["valor"]) for c in cs]
        vals_pos = [(i, v) for i, v in enumerate(vals_all) if v is not None and v > 0]
        n_pos = len(vals_pos)
        if n_pos < 4:
            res[label] = {"kh_id": kh, "n_colgantes": len(cs), "n_pos": n_pos, "vals_all": vals_all, "status": "SIN_POTENCIA"}
            continue
        pos = np.array([x[0] for x in vals_pos], dtype=float)
        v = np.array([x[1] for x in vals_pos], dtype=float)
        rho = float(stats.spearmanr(pos, v).statistic)
        cv = float(np.std(v, ddof=1) / np.mean(v)) if np.mean(v) > 0 else np.nan
        # Permutación unilateral (rho <= obs)
        B = 10000
        le = 0
        for _ in range(B):
            vp = rng.permutation(v)
            rp = float(stats.spearmanr(pos, vp).statistic)
            if rp <= rho + 1e-12:
                le += 1
        p = (le + 1) / (B + 1)
        res[label] = {
            "kh_id": kh, "n_colgantes": len(cs), "n_pos": n_pos,
            "vals_all": vals_all, "vals_pos": [int(x) for x in v],
            "rho": round(rho, 4), "cv": round(cv, 4), "p": round(p, 5),
        }
        rhos.append(rho)
        p_indiv.append(p)

    # Criterio congelado P03.1: JC031 necesita >=6 colgantes positivos para potencia
    jc31 = res["JC031_Quipu9"]
    if jc31.get("n_pos", 0) < 6:
        status = "SIN_POTENCIA"
        p_comb = res["JC024_Quipu8"].get("p")
    else:
        status = "EVALUADO"
        # Combinación Fisher de ambos p-valores si ambos evaluados
        if len(p_indiv) == 2:
            _, p_comb = stats.combine_pvalues(p_indiv, method="fisher")
            p_comb = float(p_comb)
        else:
            p_comb = p_indiv[0] if p_indiv else None

    veredicto = "SIN_POTENCIA"
    if status == "EVALUADO":
        if jc31["rho"] <= -0.50 and jc31["cv"] < 0.35 and (p_comb is not None and p_comb < 0.05):
            veredicto = "CONFIRMA_CANDIDATO"
        else:
            veredicto = "REFUTADA"
    else:
        # Evaluar JC024 por separado como nota
        jc24 = res["JC024_Quipu8"]
        if jc24.get("cv", 9) >= 0.35:
            veredicto = "SIN_POTENCIA_JC031_Y_CV_ALTO_JC024"

    return {
        "test_id": "P03.1",
        "detalle": res,
        "p": round(p_comb, 6) if p_comb is not None else None,
        "status": status,
        "veredicto_preliminar": veredicto,
    }


def extract_ur053_trios(cords):
    """Extrae los tríos sucesivos (W, R/RL/RB, AB) de UR053A-E iniciando un nuevo trío en cada colgante W."""
    trios = []
    cur = None
    for c in cords:
        v = to_int(c["valor"])
        if v is None:
            continue
        col = c["color_base"]
        is_p0 = (c["nivel"] == "0" and c["tipo"] == "p")
        if is_p0 and col == "W":
            if cur is not None:
                trios.append(cur)
            cur = {"W": v, "R": 0, "AB": 0, "ALL": v}
            continue
        if cur is None:
            cur = {"W": 0, "R": 0, "AB": 0, "ALL": 0}
        cur["ALL"] += v
        if col == "W":
            cur["W"] += v
        elif col in ("R", "RL", "RD", "RM", "RB", "RG", "PK"):
            cur["R"] += v
        elif col in ("AB", "MB", "LB", "YB", "B", "DB", "KB"):
            cur["AB"] += v
    if cur is not None:
        trios.append(cur)
    return trios


def test_p03_2_ur053_chirinos(kfg_to_kh, cords_by_q, rng):
    """P03.2: Sumas de tramos contiguos de grupos en UR053E -> UR053B/C (por color W, R, AB y total)."""
    trios = {name: extract_ur053_trios(cords_by_q[kfg_to_kh[name]]) for name in ["UR053A", "UR053B", "UR053C", "UR053D", "UR053E"]}
    E = trios["UR053E"]
    targets = {}
    for ch in ("W", "R", "AB", "ALL"):
        targets[ch] = set()
        for tname in ("UR053B", "UR053C"):
            for g in trios[tname]:
                if g[ch] >= 10:
                    targets[ch].add(g[ch])

    def count_contig_hits(E_list, tol=0):
        # Contar cuántos valores objetivo distintos de B/C se alcanzan como suma de 2..5 grupos contiguos de E
        matched_exact = set()
        matches_detail = []
        nE = len(E_list)
        for ch in ("W", "R", "AB", "ALL"):
            arr = [g[ch] for g in E_list]
            tgts = targets[ch]
            for i in range(nE):
                s = arr[i]
                for L in range(2, min(6, nE - i + 1)):
                    s += arr[i + L - 1]
                    if s < 10:
                        continue
                    if tol == 0:
                        if s in tgts:
                            matched_exact.add((ch, s))
                            matches_detail.append({"canal": ch, "tramo_E": f"{i}..{i+L-1}", "suma": s})
                    else:
                        for t in tgts:
                            if abs(s - t) <= tol:
                                matched_exact.add((ch, t))
        return len(matched_exact), matches_detail

    obs_exact, det_exact = count_contig_hits(E, tol=0)
    obs_tol1, _ = count_contig_hits(E, tol=1)

    B = 5000
    ge = 0
    null_vals = []
    for _ in range(B):
        idx = rng.permutation(len(E))
        Ep = [E[i] for i in idx]
        c_p, _ = count_contig_hits(Ep, tol=0)
        null_vals.append(c_p)
        if c_p >= obs_exact:
            ge += 1
    p = (ge + 1) / (B + 1)
    return {
        "test_id": "P03.2",
        "n_grupos_E": len(E),
        "n_targets_BC_por_canal": {k: len(v) for k, v in targets.items()},
        "obs_exactos": obs_exact,
        "obs_tol1": obs_tol1,
        "nulo_medio": round(float(np.mean(null_vals)), 2),
        "p": round(p, 6),
        "ejemplos_exactos": det_exact[:15],
        "status": "EVALUADO",
    }


def test_p03_3_inkawasi_4_sin_leer(kfg_to_kh, cords_by_q, rng):
    """P03.3: Los 4 quipus sin leer del montón de maní (UR272, UR276, UR277, UR279) con OKR hacia libros."""
    unread = ["UR272", "UR276", "UR277", "UR279"]
    books = ["UR266", "UR275", "UR269", "UR278"]

    # Recolectar cabeceras y totales de grupo >= 10 de los 4 libros
    book_targets = set()
    for b in books:
        kh = kfg_to_kh[b]
        by_g = defaultdict(list)
        for c in cords_by_q[kh]:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                v = to_int(c["valor"])
                gi = to_int(c["grupo"])
                if v is not None and gi is not None:
                    by_g[gi].append(v)
        for g, vs in by_g.items():
            if vs and vs[0] >= 10:
                book_targets.add(vs[0])
            s = sum(vs)
            if s >= 10:
                book_targets.add(s)

    # Extraer valores por grupo de los 4 sin leer
    u_groups = {}
    u_summary = {}
    for u in unread:
        kh = kfg_to_kh[u]
        by_g = defaultdict(list)
        all_v = []
        for c in cords_by_q[kh]:
            v = to_int(c["valor"])
            if v is not None and v > 0:
                all_v.append(v)
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                gi = to_int(c["grupo"])
                if v is not None and gi is not None:
                    by_g[gi].append(v)
        u_groups[u] = [by_g[g] for g in sorted(by_g.keys())]
        u_summary[u] = {
            "kh_id": kh, "n_cuerdas": len(cords_by_q[kh]), "n_grupos": len(by_g),
            "top_valores": Counter(all_v).most_common(6),
            "suma_total": sum(all_v),
        }

    def score_unread(groups_dict):
        hits = 0
        details = []
        # 1) Sumas de grupo de cada quipu hacia book_targets
        g_sums_by_u = {}
        for u, gs in groups_dict.items():
            ss = [sum(g) for g in gs]
            g_sums_by_u[u] = ss
            for gi, s in enumerate(ss):
                if s >= 10 and s in book_targets:
                    hits += 1
                    details.append({"tipo": "suma_grupo", "origen": f"{u} g{gi}", "valor": s})
        # 2) Parejas A+B alineadas por índice de grupo entre los 4 sin leer
        for i in range(len(unread)):
            for j in range(i + 1, len(unread)):
                u1, u2 = unread[i], unread[j]
                s1, s2 = g_sums_by_u[u1], g_sums_by_u[u2]
                for gi in range(min(len(s1), len(s2))):
                    if s1[gi] > 0 and s2[gi] > 0:
                        tot = s1[gi] + s2[gi]
                        if tot >= 10 and tot in book_targets:
                            hits += 1
                            details.append({"tipo": "par_A+B", "origen": f"{u1}+{u2} g{gi}", "valor": tot})
        return hits, details

    obs, det = score_unread(u_groups)
    # Nulo: permutar valores entre grupos dentro de cada uno de los 4 quipus (5 000 réplicas)
    B = 5000
    ge = 0
    nulls = []
    flat_by_u = {u: [v for g in gs for v in g] for u, gs in u_groups.items()}
    lens_by_u = {u: [len(g) for g in gs] for u, gs in u_groups.items()}
    for _ in range(B):
        gp = {}
        for u in unread:
            arr = rng.permutation(flat_by_u[u]).tolist()
            pos = 0
            gs_p = []
            for L in lens_by_u[u]:
                gs_p.append(arr[pos:pos + L])
                pos += L
            gp[u] = gs_p
        h_p, _ = score_unread(gp)
        nulls.append(h_p)
        if h_p >= obs:
            ge += 1
    p = (ge + 1) / (B + 1)
    return {
        "test_id": "P03.3",
        "resumen_4_quipus": u_summary,
        "n_book_targets": len(book_targets),
        "obs_aciertos": obs,
        "nulo_medio": round(float(np.mean(nulls)), 2),
        "p": round(p, 6),
        "ejemplos": det[:15],
        "status": "EVALUADO",
    }


def test_p03_4_kh0674_topcords(cords_by_q, rng):
    """P03.4: KH0674 (Dumbarton Oaks, 41 grupos) — ¿una cuerda del grupo iguala la suma de las demás?"""
    cs = cords_by_q["KH0674"]
    # Variante A: solo colgantes nivel 0; Variante B: colgante + sus subsidiarias
    sub_sum = defaultdict(int)
    for c in cs:
        if c["nivel"] != "0":
            # Raíz p#
            m = re.match(r"^(p\d+)", c["cuerda"])
            v = to_int(c["valor"])
            if m and v is not None:
                sub_sum[m.group(1)] += v

    groups_A = defaultdict(list)
    groups_B = defaultdict(list)
    for c in cs:
        if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
            gi = to_int(c["grupo"])
            if gi is None:
                continue
            v = to_int(c["valor"]) or 0
            groups_A[gi].append(v)
            groups_B[gi].append(v + sub_sum.get(c["cuerda"], 0))

    def eval_variant(gdict):
        gs = [gdict[g] for g in sorted(gdict.keys())]
        def count_hits(glist):
            h = 0
            for vals in glist:
                if len(vals) < 3:
                    continue
                tot = sum(vals)
                if any(v >= 10 and v == tot - v for v in vals):
                    h += 1
            return h
        obs = count_hits(gs)
        flat = [v for g in gs for v in g]
        lens = [len(g) for g in gs]
        B = 5000
        ge = 0
        ns = []
        for _ in range(B):
            arr = rng.permutation(flat).tolist()
            pos = 0
            gp = []
            for L in lens:
                gp.append(arr[pos:pos + L])
                pos += L
            hp = count_hits(gp)
            ns.append(hp)
            if hp >= obs:
                ge += 1
        return obs, round(float(np.mean(ns)), 2), (ge + 1) / (B + 1), len(gs)

    obsA, muA, pA, nG = eval_variant(groups_A)
    obsB, muB, pB, _ = eval_variant(groups_B)
    # Corregir por las 2 variantes (Bonferroni ×2)
    p_corr = min(1.0, 2.0 * min(pA, pB))
    return {
        "test_id": "P03.4",
        "n_grupos": nG,
        "solo_colgantes": {"obs": obsA, "nulo_medio": muA, "p": round(pA, 6)},
        "colgantes_mas_subs": {"obs": obsB, "nulo_medio": muB, "p": round(pB, 6)},
        "p": round(p_corr, 6),
        "status": "EVALUADO",
    }


def parse_knot_digits(nudos_str):
    """Extrae lista de dígitos/cuentas por racimo (de abajo arriba: [unidades, nivel1, nivel2]) para búsqueda de radices."""
    if not nudos_str:
        return None
    toks = re.findall(r"(\d+)\s*([SLEsle])", nudos_str)
    if len(toks) < 2 or len(toks) > 3:
        return None
    # Orden en KFG/OKR es de arriba hacia abajo -> invertimos para [nivel0, nivel1, nivel2]
    counts = [int(n) for n, _t in reversed(toks)]
    if any(c <= 0 or c > 25 for c in counts):
        return None
    return counts


def test_p03_5_radices_mixtas(quipus, kfg_to_kh, cords_by_q, rng):
    """P03.5: Búsqueda Damerow-Englund de bases/radices mixtas (r1, r2) in {2..20}^2 != (10,10)."""
    # Leer géneros TAL y NON del atlas + lista explícita congelada
    atlas_path = RAIZ / "analisis/28_atlas_generos/atlas.csv"
    cand_khs = set()
    for name in ("UR050", "UR054", "UR055", "UR039", "UR178", "UR179", "UR180"):
        if name in kfg_to_kh:
            cand_khs.add(kfg_to_kh[name])
    cand_khs.add("KH0676")
    with open(atlas_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["genero"] in ("TAL", "NON"):
                kh = kfg_to_kh.get(r["kfg"])
                if kh:
                    cand_khs.add(kh)

    # Pre-construir pares (r1, r2) != (10,10)
    r_grid = [(r1, r2) for r1 in range(2, 21) for r2 in range(2, 21) if not (r1 == 10 and r2 == 10)]
    r1_arr = np.array([x[0] for x in r_grid], dtype=np.int32)
    r2_arr = np.array([x[1] for x in r_grid], dtype=np.int32)

    results_q = []
    for kh in sorted(cand_khs):
        cs = cords_by_q[kh]
        # Agrupar colgantes por grupo
        by_g = defaultdict(list)
        n_multi = 0
        for c in cs:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                gi = to_int(c["grupo"])
                if gi is None:
                    continue
                ds = parse_knot_digits(c["nudos"])
                if ds is not None:
                    n_multi += 1
                    d0 = ds[0]
                    d1 = ds[1] if len(ds) >= 2 else 0
                    d2 = ds[2] if len(ds) >= 3 else 0
                    by_g[gi].append((d0, d1, d2))
                else:
                    v = to_int(c["valor"])
                    if v is not None and v > 0:
                        by_g[gi].append((v, 0, 0))
        if n_multi < 15 or len(by_g) < 3:
            continue

        gs = [by_g[g] for g in sorted(by_g.keys()) if len(by_g[g]) >= 3]
        if len(gs) < 3:
            continue

        def eval_all_radices(glist):
            # Vectorizado sobre las 360 combinaciones de (r1, r2) + base (10,10)
            hits_grid = np.zeros(len(r_grid), dtype=np.int32)
            hits_10 = 0
            for g in glist:
                d0 = np.array([x[0] for x in g], dtype=np.int32)
                d1 = np.array([x[1] for x in g], dtype=np.int32)
                d2 = np.array([x[2] for x in g], dtype=np.int32)
                # Base 10
                v10 = d0 + 10 * d1 + 100 * d2
                s10 = v10.sum()
                if np.any((v10 >= 10) & (2 * v10 == s10)):
                    hits_10 += 1
                # Grid (G, M) -> (360, M)
                vg = d0[None, :] + r1_arr[:, None] * d1[None, :] + (r1_arr * r2_arr)[:, None] * d2[None, :]
                sg = vg.sum(axis=1, keepdims=True)
                ok = np.any((vg >= 10) & (2 * vg == sg), axis=1)
                hits_grid += ok.astype(np.int32)
            best_idx = int(np.argmax(hits_grid))
            return int(hits_grid[best_idx]), hits_10, (int(r1_arr[best_idx]), int(r2_arr[best_idx]))

        obs_best, obs_10, best_r = eval_all_radices(gs)
        obs_gain = obs_best - obs_10
        if obs_gain <= 0:
            results_q.append({"kh_id": kh, "kfg": quipus[kh]["kfg_id"], "n_multi": n_multi, "n_grupos": len(gs),
                              "obs_10": obs_10, "obs_best": obs_best, "best_r": list(best_r), "gain": obs_gain, "p": 1.0})
            continue

        # Nulo: 500 permutaciones de cuerdas entre grupos aplicando la MISMA optimización sobre 360 radices
        flat = [x for g in gs for x in g]
        lens = [len(g) for g in gs]
        B = 500
        ge = 0
        for _ in range(B):
            perm = rng.permutation(len(flat))
            pos = 0
            gp = []
            for L in lens:
                gp.append([flat[idx] for idx in perm[pos:pos + L]])
                pos += L
            b_p, b10_p, _ = eval_all_radices(gp)
            if (b_p - b10_p) >= obs_gain:
                ge += 1
        p_q = (ge + 1) / (B + 1)
        results_q.append({"kh_id": kh, "kfg": quipus[kh]["kfg_id"], "n_multi": n_multi, "n_grupos": len(gs),
                          "obs_10": obs_10, "obs_best": obs_best, "best_r": list(best_r), "gain": obs_gain, "p": round(p_q, 5)})

    if not results_q:
        return {"test_id": "P03.5", "status": "SIN_POTENCIA", "n_quipus": 0, "p": None}
    min_p = min(r["p"] for r in results_q)
    # Corrección de Bonferroni sobre todos los quipus evaluados en P03.5
    p_global = min(1.0, min_p * len(results_q))
    return {
        "test_id": "P03.5",
        "n_quipus_evaluados": len(results_q),
        "p": round(p_global, 6),
        "top_5": sorted(results_q, key=lambda x: (x["p"], -x["gain"]))[:5],
        "status": "EVALUADO",
    }


def audit_e03_6_qu005(kfg_to_kh, cords_by_q, rng):
    """E03.6 (post-hoc): Auditoría completa de QU005 (bloques de 19, B2 = B0 + B1)."""
    kh = kfg_to_kh["QU005"]
    cs = [c for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
    by_g = defaultdict(list)
    for c in cs:
        v = to_int(c["valor"])
        by_g[c["grupo"]].append(v if v is not None else 0)
    # Evaluar en bloques por grupo y también por cortes uniformes de tamaño 19 (como en SINTESIS)
    vals = [to_int(c["valor"]) or 0 for c in cs]
    n_p = len(vals)
    # Probar bloques consecutivos de tamaño K=19 (o modal de grupo)
    K = 19
    nB = n_p // K
    blocks = [vals[i * K:(i + 1) * K] for i in range(nB)]
    obs_exact = 0
    obs_tol1 = 0
    best_triple = None
    n_triples = 0
    for a in range(nB):
        for b in range(nB):
            for c in range(b + 1, nB):
                if a in (b, c):
                    continue
                n_triples += 1
                ex = sum(1 for j in range(K) if blocks[a][j] > 0 and blocks[a][j] == blocks[b][j] + blocks[c][j])
                t1 = sum(1 for j in range(K) if blocks[a][j] > 0 and abs(blocks[a][j] - (blocks[b][j] + blocks[c][j])) <= 1)
                if ex > obs_exact:
                    obs_exact = ex
                    obs_tol1 = t1
                    best_triple = (a, b, c)

    # Nulo: permutar posiciones dentro de cada bloque (10 000 réplicas) tomando el máximo sobre TODOS los tríos
    B = 10000
    ge = 0
    nulls = []
    for _ in range(B):
        bp = [rng.permutation(bl).tolist() for bl in blocks]
        mx = 0
        for a in range(nB):
            for b in range(nB):
                for c in range(b + 1, nB):
                    if a in (b, c):
                        continue
                    ex = sum(1 for j in range(K) if bp[a][j] > 0 and bp[a][j] == bp[b][j] + bp[c][j])
                    if ex > mx:
                        mx = ex
        nulls.append(mx)
        if mx >= obs_exact:
            ge += 1
    p_corr = (ge + 1) / (B + 1)
    return {
        "test_id": "E03.6_POST_HOC",
        "kh_id": kh, "n_colgantes": n_p, "n_bloques_19": nB, "n_trios": n_triples,
        "mejor_trio": f"B{best_triple[0]} = B{best_triple[1]} + B{best_triple[2]}" if best_triple else None,
        "obs_exactas": obs_exact, "obs_tol1": obs_tol1,
        "nulo_max_medio": round(float(np.mean(nulls)), 2),
        "p_corregido_trios": round(p_corr, 6),
        "bloques": blocks,
    }


def desc_d03_9_huacones_vs_inkawasi(quipus, cords_by_q):
    """D03.9: Comparación descriptiva Huacones-Vilcahuasi vs Inkawasi A (UR) vs Inkawasi B (JC)."""
    groups = {"Huacones": [], "Inkawasi_A_UR": [], "Inkawasi_B_JC": []}
    for kh, q in quipus.items():
        if "KH0653" <= kh <= "KH0663":
            grp = "Huacones"
        elif "KH0491" <= kh <= "KH0519":
            grp = "Inkawasi_A_UR"
        elif "KH0608" <= kh <= "KH0630":
            grp = "Inkawasi_B_JC"
        else:
            continue
        vals = [to_int(c["valor"]) for c in cords_by_q[kh] if to_int(c["valor"]) is not None and to_int(c["valor"]) > 0]
        groups[grp].append({
            "kh": kh, "n_cuerdas": int(q["n_cuerdas"]),
            "med_val": float(np.median(vals)) if vals else 0.0,
            "max_val": max(vals) if vals else 0,
        })
    out = {}
    for g, lst in groups.items():
        out[g] = {
            "n_quipus": len(lst),
            "mediana_n_cuerdas": round(float(np.median([x["n_cuerdas"] for x in lst])), 1) if lst else None,
            "mediana_de_medianas_val": round(float(np.median([x["med_val"] for x in lst])), 1) if lst else None,
            "mediana_max_val": round(float(np.median([x["max_val"] for x in lst])), 1) if lst else None,
        }
    return out


def main():
    rng = np.random.default_rng(SEED)
    quipus, kfg_to_kh, cords_by_q = load_master()

    r1 = test_p03_1_huacones(quipus, cords_by_q, rng)
    r2 = test_p03_2_ur053_chirinos(kfg_to_kh, cords_by_q, rng)
    r3 = test_p03_3_inkawasi_4_sin_leer(kfg_to_kh, cords_by_q, rng)
    r4 = test_p03_4_kh0674_topcords(cords_by_q, rng)
    r5 = test_p03_5_radices_mixtas(quipus, kfg_to_kh, cords_by_q, rng)

    p_map = {r["test_id"]: r["p"] for r in (r1, r2, r3, r4, r5)}
    h_map = holm_adjust(p_map)
    for r in (r1, r2, r3, r4, r5):
        r["p_holm"] = round(h_map[r["test_id"]], 6) if h_map[r["test_id"]] is not None else None

    e6 = audit_e03_6_qu005(kfg_to_kh, cords_by_q, rng)
    d9 = desc_d03_9_huacones_vs_inkawasi(quipus, cords_by_q)

    out = {
        "preregistro": "P03_huacones_y_casos_abiertos.md",
        "semilla": SEED,
        "familia_holm": [r1, r2, r3, r4, r5],
        "post_hoc_E03_6_QU005": e6,
        "descriptivo_D03_9_canete": d9,
    }
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "resultados_P03.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESULTADOS PREREGISTRO P03 (HUACONES Y CASOS ABIERTOS) ===")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']}: status={r['status']} | p={r['p']} | p_Holm={r['p_holm']}")
    print("  P03.1 Huacones detalle:", r1["detalle"], "| veredicto:", r1["veredicto_preliminar"])
    print("  P03.2 UR053E->BC:", {k: r2[k] for k in ("obs_exactos", "obs_tol1", "nulo_medio", "p", "p_holm")})
    print("  P03.3 Inkawasi 4 sin leer:", {k: r3[k] for k in ("obs_aciertos", "nulo_medio", "p", "p_holm")}, "| ejemplos:", r3["ejemplos"][:5])
    print("  P03.4 KH0674 top cords:", r4)
    print("  P03.5 Radices mixtas:", {k: r5[k] for k in ("n_quipus_evaluados", "p", "p_holm", "top_5") if k in r5})
    print("  E03.6 QU005 (post-hoc):", {k: e6[k] for k in ("mejor_trio", "obs_exactas", "obs_tol1", "nulo_max_medio", "p_corregido_trios")})
    print("  D03.9 Valle de Cañete:", d9)


if __name__ == "__main__":
    main()
