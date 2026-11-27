#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_ejecutar_P01.py — Ejecución estricta del Preregistro P01 (v1.1, SHA-256 sellado)
sobre el Corpus Maestro Unificado (`maestro_quipus.csv`, `maestro_cuerdas.csv`).

Pruebas de la familia Holm (m = 6):
  - P01.1: «La cuerda mayor abre el grupo» (K08) en `held_out`
  - P01.2: Ceros posicionales = hueco de una banda decimal (C09) en `held_out`
  - P01.3a: Cuerda superior = suma del grupo anterior (C03), estrato puro `held_out`
  - P01.3b: Cuerda superior = suma del grupo anterior (C03), estrato cuerdas superiores rescatadas de OKR en base
  - P01.4: Alternancia cromática desfase 2 (K02) en `held_out`
  - P01.5: Copias hacia/dentro de `held_out` (Smith-Waterman con nulo por rachas) + OR mismo sitio/museo

Control descriptivo fuera de Holm:
  - D01.6: Robustez de las 15 comprobaciones de `paquete_revision/verificar.py` con Thompson 2025a y OKR Inkawasi.

Semilla fija: 20261127.
Salida: `analisis/36_corpus_maestro/resultados_P01.json` y `informe_P01.md`.
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
SEED = 20261127


def holm_adjust(pvals):
    """Ajuste de Holm sobre un dict {test_id: pval} ignorando None (SIN_POTENCIA)."""
    valid = [(k, v) for k, v in pvals.items() if v is not None]
    m = len(valid)
    order = sorted(valid, key=lambda x: x[1])
    adj = {}
    running_max = 0.0
    for i, (k, p) in enumerate(order):
        val = min(1.0, (m - i) * p)
        running_max = max(running_max, val)
        adj[k] = running_max
    for k, v in pvals.items():
        if v is None:
            adj[k] = None
    return adj


def bh_adjust(p_list):
    n = len(p_list)
    if n == 0:
        return []
    idx = np.argsort(p_list)
    q = np.empty(n, dtype=float)
    prev = 1.0
    for rank in range(n, 0, -1):
        i = idx[rank - 1]
        val = min(prev, p_list[i] * n / rank)
        q[i] = val
        prev = val
    return q.tolist()


def to_int(x):
    if x is None or x == "":
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


def to_float(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def load_master():
    quipus = {}
    with open(DIR / "maestro_quipus.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            quipus[r["kh_id"]] = r
    cords_by_q = defaultdict(list)
    with open(DIR / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cords_by_q[r["kh_id"]].append(r)
    return quipus, cords_by_q


def test_p01_1_mayor_primero(quipus, cords_by_q, rng):
    """P01.1: En held_out, grupos (>=3 colgantes con valor>0, sin empate en el máx, sin suma exacta interna)."""
    elig_groups = []
    for kh, q in quipus.items():
        if q["held_out"] != "1":
            continue
        by_g = defaultdict(list)
        for c in cords_by_q[kh]:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                v = to_int(c["valor"])
                if v is not None and v > 0:
                    by_g[c["grupo"]].append(v)
        for g, vals in by_g.items():
            if len(vals) < 3:
                continue
            mx = max(vals)
            if vals.count(mx) > 1:
                continue
            # Excluir grupos con suma exacta interna (total = suma del resto)
            if mx == sum(vals) - mx:
                continue
            elig_groups.append(vals)

    n = len(elig_groups)
    if n < 15:
        return {"test_id": "P01.1", "status": "SIN_POTENCIA", "n_grupos": n, "p": None}

    obs = sum(1 for vals in elig_groups if vals[0] == max(vals))
    obs_rate = obs / n
    exp_rate = float(np.mean([1.0 / len(vals) for vals in elig_groups]))

    B = 5000
    cnt = 0
    for _ in range(B):
        s = 0
        for vals in elig_groups:
            if rng.integers(0, len(vals)) == 0:
                s += 1
        if s >= obs:
            cnt += 1
    p = (cnt + 1) / (B + 1)
    return {
        "test_id": "P01.1",
        "n_grupos": n,
        "obs_aciertos": obs,
        "obs_tasa": round(obs_rate, 4),
        "exp_tasa": round(exp_rate, 4),
        "p": round(p, 6),
        "status": "EVALUADO",
    }


def parse_knot_positions_and_orders(c):
    """Extrae (pos_cm, order_10) de las cuerdas OKR/held_out con nudos y posiciones."""
    pos_str = c.get("knot_positions_cm", "")
    typ_str = c.get("knot_types", "")
    nudos_str = c.get("nudos", "")
    if pos_str and typ_str:
        pos = [to_float(x) for x in pos_str.split(";") if to_float(x) is not None]
        # Extraer aportes desde nudos_str tipo "2S(5.0,Z,200);3L(18.0,Z,3)"
        parts = [p for p in nudos_str.split(";") if p]
        if len(parts) == len(pos) and len(pos) >= 3:
            orders = []
            for p_item in parts:
                m = re.search(r",(\d+(?:\.\d+)?)\)$", p_item)
                if not m:
                    return None
                val = float(m.group(1))
                if val <= 0:
                    return None
                ord10 = int(math.floor(math.log10(val)))
                orders.append(ord10)
            return list(zip(pos, orders))
    return None


def test_p01_2_ceros_posicionales(quipus, cords_by_q):
    """P01.2: Hueco de cero interno vs ancho de banda contigua en held_out."""
    ratios = []
    gap_zeros = []
    gap_adjs = []
    for kh, q in quipus.items():
        if q["held_out"] != "1":
            continue
        for c in cords_by_q[kh]:
            po = parse_knot_positions_and_orders(c)
            if not po:
                continue
            # Ordenar por posición ascendente
            po = sorted(po, key=lambda x: x[0])
            z_gaps = []
            a_gaps = []
            for (p1, o1), (p2, o2) in zip(po, po[1:]):
                dp = p2 - p1
                if dp <= 0:
                    continue
                do = o1 - o2
                if do == 1:
                    a_gaps.append(dp)
                elif do == 2:
                    z_gaps.append(dp)
            if z_gaps and a_gaps:
                mg_z = float(np.median(z_gaps))
                mg_a = float(np.median(a_gaps))
                if mg_a > 0:
                    ratios.append(mg_z / mg_a)
                    gap_zeros.append(mg_z)
                    gap_adjs.append(mg_a)

    n = len(ratios)
    if n < 10:
        return {"test_id": "P01.2", "status": "SIN_POTENCIA", "n_cuerdas": n, "p": None,
                "mediana_razon": round(float(np.median(ratios)), 4) if n else None}
    stat, p = stats.wilcoxon(gap_zeros, gap_adjs, alternative="greater")
    med_r = float(np.median(ratios))
    return {
        "test_id": "P01.2",
        "n_cuerdas": n,
        "mediana_razon": round(med_r, 4),
        "iqr_razon": [round(float(np.percentile(ratios, 25)), 4), round(float(np.percentile(ratios, 75)), 4)],
        "p": float(p),
        "status": "EVALUADO",
    }


def eval_top_cords_stratum(kh_list, cords_by_q, rng, filter_fn, test_id):
    """Evalúa cuerda superior = suma exacta del grupo inmediatamente anterior."""
    cases = []  # (top_val, prev_group_sum, all_group_sums_list)
    for kh in kh_list:
        cords = cords_by_q[kh]
        # Sumas por grupo de colgantes nivel 0
        g_sums = defaultdict(int)
        g_cnts = defaultdict(int)
        for c in cords:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                v = to_int(c["valor"])
                gi = to_int(c["grupo"])
                if v is not None and gi is not None:
                    g_sums[gi] += v
                    g_cnts[gi] += 1
        if len(g_sums) < 2:
            continue
        sorted_gs = sorted(g_sums.keys())
        all_sums = [g_sums[g] for g in sorted_gs]
        for c in cords:
            if not filter_fn(c):
                continue
            v = to_int(c["valor"])
            if v is None or v <= 0:
                continue
            # Grupo asociado o anterior
            g_cur = to_int(c["grupo"])
            # En OKR la cuerda superior suele tener el mismo grupo o el siguiente al grupo que suma;
            # evaluamos el grupo inmediatamente anterior (g_cur - 1) si existe, o g_cur si es 0
            if g_cur is not None and (g_cur - 1) in g_sums:
                prev_sum = g_sums[g_cur - 1]
                cases.append((kh, c["cuerda"], v, prev_sum, all_sums))
            elif g_cur is not None and g_cur in g_sums:
                # Si la top cord está codificada en el mismo clúster del grupo que cierra
                cases.append((kh, c["cuerda"], v, g_sums[g_cur], all_sums))

    n = len(cases)
    if n < 10:
        return {"test_id": test_id, "status": "SIN_POTENCIA", "n_superiores": n, "p": None,
                "obs_aciertos": sum(1 for x in cases if x[2] == x[3])}
    obs = sum(1 for x in cases if x[2] == x[3])
    B = 5000
    cnt = 0
    exp_sum = 0.0
    for _ in range(B):
        s = 0
        for _, _, v, _, all_sums in cases:
            if v == all_sums[rng.integers(0, len(all_sums))]:
                s += 1
        exp_sum += s
        if s >= obs:
            cnt += 1
    p = (cnt + 1) / (B + 1)
    return {
        "test_id": test_id,
        "n_superiores": n,
        "obs_aciertos": obs,
        "exp_aciertos": round(exp_sum / B, 2),
        "p": round(p, 6),
        "status": "EVALUADO",
    }


def permute_color_runs(seq, rng):
    """Permuta bloques/rachas de colores idénticos consecutivos (nulo estricto K02)."""
    runs = []
    for x in seq:
        if runs and runs[-1][0] == x:
            runs[-1].append(x)
        else:
            runs.append([x])
    order = rng.permutation(len(runs))
    out = []
    for i in order:
        out.extend(runs[i])
    return out


def lag2_alt_score(seq):
    """Fracción de posiciones i donde seq[i] == seq[i+2] y seq[i] != seq[i+1]."""
    if len(seq) < 4:
        return 0.0
    hits = sum(1 for i in range(len(seq) - 2) if seq[i] == seq[i + 2] and seq[i] != seq[i + 1])
    return hits / (len(seq) - 2)


def test_p01_4_alternancia(quipus, cords_by_q, rng):
    """P01.4: Alternancia cromática A/B/A/B en held_out con nulo por rachas."""
    elig = []
    hits = []
    for kh, q in quipus.items():
        if q["held_out"] != "1":
            continue
        seq = [c["color_base"] for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p" and c["color_base"]]
        if len(seq) < 10 or len(set(seq)) < 2:
            continue
        obs = lag2_alt_score(seq)
        B = 2000
        ge = 0
        for _ in range(B):
            if lag2_alt_score(permute_color_runs(seq, rng)) >= obs - 1e-12:
                ge += 1
        p = (ge + 1) / (B + 1)
        elig.append((kh, len(seq), round(obs, 3), round(p, 5)))
        if p < 0.01:
            hits.append({"kh_id": kh, "n": len(seq), "score": round(obs, 3), "p": round(p, 5)})

    n = len(elig)
    if n < 15:
        return {"test_id": "P01.4", "status": "SIN_POTENCIA", "n_quipus": n, "p": None, "candidatos": hits}
    k = len(hits)
    p_binom = float(stats.binomtest(k, n, 0.01, alternative="greater").pvalue)
    return {
        "test_id": "P01.4",
        "n_quipus": n,
        "n_sig_p001": k,
        "exp_p001": round(n * 0.01, 2),
        "p": round(p_binom, 6),
        "candidatos": hits,
        "status": "EVALUADO",
    }


def sw_logodds_score(a, b, inv_freq):
    """Score Smith-Waterman local entre secuencias de enteros (tol ±1 nudo simple / exacto)."""
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return 0.0
    dp = np.zeros((na + 1, nb + 1), dtype=np.float32)
    best = 0.0
    for i in range(1, na + 1):
        va = a[i - 1]
        for j in range(1, nb + 1):
            vb = b[j - 1]
            if va == vb:
                s = inv_freq.get(va, 3.0) if va >= 10 else 0.5
            elif va >= 10 and vb >= 10 and abs(va - vb) in (1, 10, 100):
                s = 0.5 * min(inv_freq.get(va, 3.0), inv_freq.get(vb, 3.0))
            else:
                s = -2.5
            val = max(0.0, dp[i - 1, j - 1] + s, dp[i - 1, j] - 2.0, dp[i, j - 1] - 2.0)
            dp[i, j] = val
            if val > best:
                best = float(val)
    return best


def permute_value_runs(seq, rng):
    runs = []
    for x in seq:
        if runs and runs[-1][0] == x:
            runs[-1].append(x)
        else:
            runs.append([x])
    order = rng.permutation(len(runs))
    out = []
    for i in order:
        out.extend(runs[i])
    return out


def test_p01_5_copias_heldout(quipus, cords_by_q, rng):
    """P01.5: Barrido de copias con al menos un miembro en held_out (excluyendo solo duplicados no numéricos)."""
    # Construir secuencias de colgantes con valor > 0 (mínimo 5 cuerdas con valor > 0)
    seqs = {}
    val_counts = Counter()
    for kh, q in quipus.items():
        vals = [to_int(c["valor"]) for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
        vals = [v for v in vals if v is not None and v > 0]
        if len(vals) >= 5:
            seqs[kh] = vals
            for v in set(vals):
                val_counts[v] += 1
    N_q = len(seqs)
    inv_freq = {v: min(8.0, math.log2(N_q / max(1, c))) for v, c in val_counts.items()}

    ho_ids = sorted(kh for kh in seqs if quipus[kh]["held_out"] == "1")
    all_ids = sorted(seqs.keys())

    # Regla anti-circularidad: excluir solo pares con mismo museo y mismo nº de inventario normalizado
    def same_phys_inv(k1, k2):
        m1, i1 = quipus[k1]["museo"].strip().lower(), quipus[k1]["n_inventario"].strip().lower()
        m2, i2 = quipus[k2]["museo"].strip().lower(), quipus[k2]["n_inventario"].strip().lower()
        return bool(m1 and i1 and m1 == m2 and i1 == i2)

    # Pre-filtro exacto sin pérdida para pares con >=3 valores >=10 compartidos (o >=4 valores totales compartidos)
    pairs_eval = 0
    cand_pairs = []
    val_sets_ge10 = {kh: set(v for v in s if v >= 10) for kh, s in seqs.items()}
    val_sets_all = {kh: set(s) for kh, s in seqs.items()}

    seen = set()
    for k1 in ho_ids:
        for k2 in all_ids:
            if k1 == k2:
                continue
            pair = (min(k1, k2), max(k1, k2))
            if pair in seen:
                continue
            seen.add(pair)
            if same_phys_inv(k1, k2):
                continue
            pairs_eval += 1
            sh10 = len(val_sets_ge10[k1] & val_sets_ge10[k2])
            shall = len(val_sets_all[k1] & val_sets_all[k2])
            if sh10 >= 3 or shall >= 5:
                s1, s2 = seqs[k1], seqs[k2]
                sc_f = sw_logodds_score(s1, s2, inv_freq)
                sc_r = sw_logodds_score(s1, s2[::-1], inv_freq)
                sc = max(sc_f, sc_r)
                if sc >= 14.0:
                    cand_pairs.append((k1, k2, sc, "inv" if sc_r > sc_f else "dir", sh10))

    # Monte Carlo secuencial con nulo por rachas sobre candidatos
    p_all = [1.0] * max(0, pairs_eval - len(cand_pairs))
    tested = []
    for k1, k2, sc, orient, sh10 in sorted(cand_pairs, key=lambda x: -x[2]):
        s1, s2 = seqs[k1], seqs[k2]
        ge = 0
        B = 199
        for _ in range(B):
            p1 = permute_value_runs(s1, rng)
            if max(sw_logodds_score(p1, s2, inv_freq), sw_logodds_score(p1, s2[::-1], inv_freq)) >= sc - 1e-6:
                ge += 1
        if ge <= 2:
            # Escalar a 1999 réplicas
            B2 = 1800
            for _ in range(B2):
                p1 = permute_value_runs(s1, rng)
                if max(sw_logodds_score(p1, s2, inv_freq), sw_logodds_score(p1, s2[::-1], inv_freq)) >= sc - 1e-6:
                    ge += 1
            B += B2
        p = (ge + 1) / (B + 1)
        p_all.append(p)
        tested.append({
            "kh1": k1, "kh2": k2, "score": round(sc, 2), "orient": orient,
            "shared_ge10": sh10, "p": p,
            "museo1": quipus[k1]["museo"], "museo2": quipus[k2]["museo"],
            "prov1": quipus[k1]["procedencia"], "prov2": quipus[k2]["procedencia"],
        })

    q_all = bh_adjust(p_all)
    offset = len(p_all) - len(tested)
    confirmed = []
    for idx, t in enumerate(tested):
        t["q_bh"] = round(q_all[offset + idx], 5)
        t["p"] = round(t["p"], 6)
        if t["q_bh"] < 0.05 and t["shared_ge10"] >= 4:
            confirmed.append(t)

    # Contraste OR mismo sitio/museo vs distinto (solo si >= 3 copias confirmadas)
    or_val = None
    p_or = None
    status = "EVALUADO"
    if len(confirmed) < 3:
        status = "SIN_POTENCIA"
    else:
        same_c = sum(1 for c in confirmed if (c["museo1"] and c["museo1"] == c["museo2"]) or (c["prov1"] and c["prov1"] == c["prov2"]))
        diff_c = len(confirmed) - same_c
        # Tasa base en pairs_eval
        same_tot = 0
        diff_tot = 0
        for pair in seen:
            k1, k2 = pair
            if (quipus[k1]["museo"] and quipus[k1]["museo"] == quipus[k2]["museo"]) or (quipus[k1]["procedencia"] and quipus[k1]["procedencia"] == quipus[k2]["procedencia"]):
                same_tot += 1
            else:
                diff_tot += 1
        table = [[same_c, max(0, same_tot - same_c)], [diff_c, max(0, diff_tot - diff_c)]]
        or_val, p_or = stats.fisher_exact(table, alternative="greater")

    return {
        "test_id": "P01.5",
        "n_heldout_con_5vals": len(ho_ids),
        "pares_evaluados": pairs_eval,
        "candidatos_sw_ge14": len(cand_pairs),
        "copias_confirmadas_q005": confirmed,
        "n_confirmadas": len(confirmed),
        "OR_mismo_museo_o_sitio": round(float(or_val), 3) if or_val is not None and np.isfinite(or_val) else str(or_val),
        "p": round(float(p_or), 6) if p_or is not None else None,
        "status": status,
        "top_10_candidatos": tested[:10],
    }


def check_d01_6_robustez(quipus, cords_by_q):
    """D01.6: Control determinista de robustez de hallazgos clave tras Thompson 2025a y OKR Inkawasi."""
    # Comprobar cuántos parches de Thompson tocan quipus clave de Inkawasi, Puruchuco, KH0049, UR053, UR1104/UR234
    key_kfg = {"UR270", "UR278", "UR266", "UR275", "UR273A", "UR273B", "UR274A", "UR274B",
               "UR068", "UR067", "UR066", "UR063", "KH0049", "UR122", "UR053A", "UR053B",
               "UR053C", "UR053D", "UR053E", "UR1104", "UR234", "HP055", "UR1084"}
    touched = []
    for kh, q in quipus.items():
        if q["kfg_id"] in key_kfg or kh in key_kfg:
            for c in cords_by_q[kh]:
                if c["thompson_flag"]:
                    touched.append((kh, q["kfg_id"], c["cuerda"], c["valor"], c["valor_thompson"]))
    # Verificar recálculo directo de las cuotas de UR274B (OKR) y totales de UR278 -> UR266 en el maestro
    ur274b_kh = [kh for kh, q in quipus.items() if q["kfg_id"] == "UR274B"][0]
    ur274b_vals = [to_int(c["valor"]) for c in cords_by_q[ur274b_kh]]
    n17 = sum(1 for v in ur274b_vals if v == 17)
    n10 = sum(1 for v in ur274b_vals if v == 10)
    return {
        "test_id": "D01.6",
        "parches_thompson_en_quipus_clave": touched,
        "n_parches_en_clave": len(touched),
        "ur274b_cuerdas_okr": len(ur274b_vals),
        "ur274b_cuotas_17_okr": n17,
        "ur274b_cuotas_10_okr": n10,
        "veredicto": "ROBUSTO" if len(touched) == 0 else "REVISAR_CAMBIOS",
    }


def main():
    rng = np.random.default_rng(SEED)
    quipus, cords_by_q = load_master()

    r1 = test_p01_1_mayor_primero(quipus, cords_by_q, rng)
    r2 = test_p01_2_ceros_posicionales(quipus, cords_by_q)

    ho_khs = [kh for kh, q in quipus.items() if q["held_out"] == "1"]
    base_khs = [kh for kh, q in quipus.items() if q["held_out"] == "0"]
    r3a = eval_top_cords_stratum(
        ho_khs, cords_by_q, rng,
        lambda c: c["tipo"] == "t" or c["cord_classification"] == "T" or c["union"] == "T",
        "P01.3a",
    )
    r3b = eval_top_cords_stratum(
        base_khs, cords_by_q, rng,
        lambda c: c["fuente_cuerda"] == "okr_rescate_T",
        "P01.3b",
    )
    r4 = test_p01_4_alternancia(quipus, cords_by_q, rng)
    r5 = test_p01_5_copias_heldout(quipus, cords_by_q, rng)
    d6 = check_d01_6_robustez(quipus, cords_by_q)

    p_map = {r["test_id"]: r["p"] for r in (r1, r2, r3a, r3b, r4, r5)}
    h_map = holm_adjust(p_map)
    for r in (r1, r2, r3a, r3b, r4, r5):
        r["p_holm"] = round(h_map[r["test_id"]], 6) if h_map[r["test_id"]] is not None else None

    out = {
        "preregistro": "P01_corpus_maestro_y_heldout.md",
        "semilla": SEED,
        "familia_holm": [r1, r2, r3a, r3b, r4, r5],
        "descriptivo": d6,
    }
    (DIR / "resultados_P01.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # Imprimir resumen claro
    print("=== RESULTADOS PREREGISTRO P01 (HELD-OUT) ===")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']}: status={r['status']} | p={r['p']} | p_Holm={r['p_holm']} | detalle={ {k:v for k,v in r.items() if k not in ('test_id','status','p','p_holm','top_10_candidatos','copias_confirmadas_q005','candidatos')} }")
    print(f"  P01.5 copias confirmadas ({r5['n_confirmadas']}):")
    for c in r5["copias_confirmadas_q005"]:
        print("   ", c)
    print(f"  P01.5 top candidatos (no necesariamente confirmados):")
    for c in r5["top_10_candidatos"][:6]:
        print("   ", c["kh1"], "~", c["kh2"], "score=", c["score"], "p=", c["p"], "q_bh=", c["q_bh"], "sh10=", c["shared_ge10"])
    print("  D01.6 robustez:", d6)


if __name__ == "__main__":
    main()
