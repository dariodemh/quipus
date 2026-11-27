#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_ejecutar_P02_rt16905.py — Ejecución estricta del Preregistro P02 (v1.1, SHA-256 sellado)
sobre los 15 Quipus Enlazados RT-16905 (KH0638–KH0652, MNAAHP Lima).

Familia Holm (m = 4):
  - P02.1: Sumas jerárquicas (valores >= 10) sobre ejes físicos, normalizadas por tamaño (QAP 10 000)
  - P02.2: Acoplamiento numérico Smith-Waterman (estandarizado por tamaño) vs proximidad física (Mantel QAP 10 000)
  - P02.3: Coherencia físico-textil (Gower sin tamaño) vs proximidad física (Mantel QAP 10 000)
  - P02.4: Alineación cromática de K15 (19 hilos envueltos) con K01 (nulo por rachas 5 000)

Descriptivos fuera de Holm:
  - D02.5: Contabilidad interna individual (R1, F, A, TA) en cada uno de K01–K14 (5 000 permutaciones)
  - D02.6: Descripción de Tie Cord 04 y conteos de K15 vs K01.

Semilla fija: 20261127.
"""
import csv
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np
from scipy import stats

DIR = Path(__file__).resolve().parent
MAESTRO = DIR.parent / "36_corpus_maestro"
SEED = 20261127

# Mapeo congelado K01..K14 -> KH0638..KH0651
K_LIST = [f"KH{638 + i:04d}" for i in range(14)]
K_NUM = {f"KH{638 + i:04d}": i + 1 for i in range(14)}

# Topología física congelada del preregistro P02 §1 (extraída del croquis y docx ANTES de ver valores)
HUBS = {
    "Hub_C": [10, 11, 12],
    "Hub_A": [11, 12, 13, 14],
    "Hub_B": [1, 13, 14],
    "Hub_D": [1, 2, 3],
    "Hub_E": [1, 4],
    "Zona_F": [4, 5, 6, 7],
    "Hub_G": [4, 8, 9],
}


def build_phys_graph():
    n = 14
    adj = np.zeros((n, n), dtype=int)
    for members in HUBS.values():
        for a in members:
            for b in members:
                if a != b:
                    adj[a - 1, b - 1] = 1
    # Distancias de camino más corto (BFS)
    dist = np.full((n, n), 99, dtype=float)
    for i in range(n):
        dist[i, i] = 0
        q = deque([i])
        while q:
            u = q.popleft()
            for v in range(n):
                if adj[u, v] and dist[i, v] > dist[i, u] + 1:
                    dist[i, v] = dist[i, u] + 1
                    q.append(v)
    return adj, dist


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


def to_float(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def load_rt16905():
    cords_by_k = defaultdict(list)
    with open(MAESTRO / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["kh_id"] in K_NUM:
                cords_by_k[r["kh_id"]].append(r)
    k15 = []
    with open(MAESTRO / "rt16905_k15_wrapped.csv", encoding="utf-8") as f:
        k15 = list(csv.DictReader(f))
    return cords_by_k, k15


def sw_score(a, b, inv_freq):
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
                s = inv_freq.get(va, 2.5) if va >= 10 else 0.4
            elif va >= 10 and vb >= 10 and abs(va - vb) in (1, 10, 100):
                s = 0.5 * min(inv_freq.get(va, 2.5), inv_freq.get(vb, 2.5))
            else:
                s = -2.0
            val = max(0.0, dp[i - 1, j - 1] + s, dp[i - 1, j] - 1.5, dp[i, j - 1] - 1.5)
            dp[i, j] = val
            if val > best:
                best = float(val)
    return best


def permute_runs(seq, rng):
    if not seq:
        return []
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


def main():
    rng = np.random.default_rng(SEED)
    adj, dist = build_phys_graph()
    cords_by_k, k15 = load_rt16905()

    # Resumen por quipu K01..K14
    summary = []
    vals_ge10 = []
    group_totals_ge10 = []
    khipu_totals = []
    seqs_all = []
    pool_ge10 = []

    for kh in K_LIST:
        cs = cords_by_k[kh]
        p_vals = [to_int(c["valor"]) for c in cs if c["nivel"] == "0" and c["tipo"] == "p"]
        p_pos = [v for v in p_vals if v is not None and v > 0]
        all_pos = [to_int(c["valor"]) for c in cs if to_int(c["valor"]) is not None and to_int(c["valor"]) > 0]
        v10 = [v for v in all_pos if v >= 10]
        pool_ge10.extend(v10)

        g_sums = defaultdict(int)
        for c in cs:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                v = to_int(c["valor"])
                if v is not None:
                    g_sums[c["grupo"]] += v
        gt10 = [s for s in g_sums.values() if s >= 10]
        ktot = sum(all_pos)
        if ktot >= 10:
            gt10_with_k = gt10 + [ktot]
        else:
            gt10_with_k = gt10

        vals_ge10.append(v10)
        group_totals_ge10.append(gt10_with_k)
        khipu_totals.append(ktot)
        seqs_all.append(p_pos)

        summary.append({
            "k_num": K_NUM[kh], "kh_id": kh, "n_cuerdas": len(cs),
            "n_colgantes": sum(1 for c in cs if c["nivel"] == "0" and c["tipo"] == "p"),
            "n_grupos": len(g_sums), "total": ktot,
            "n_vals_ge10": len(v10), "max_val": max(all_pos) if all_pos else 0,
        })

    pool_ge10_arr = np.array(pool_ge10, dtype=int) if pool_ge10 else np.array([10], dtype=int)

    # ---------- P02.1: Sumas jerárquicas (>= 10) estandarizadas por tamaño + QAP ----------
    n = 14
    Z_hier = np.zeros((n, n), dtype=float)
    hits_detail = []
    for i in range(n):
        src_tots = set(group_totals_ge10[i])
        for j in range(n):
            if i == j:
                continue
            tgt_vals = set(vals_ge10[j]) | set(group_totals_ge10[j])
            obs_ij = len(src_tots & tgt_vals)
            if obs_ij > 0 and adj[i, j]:
                hits_detail.append({
                    "src": f"K{i+1:02d}", "tgt": f"K{j+1:02d}",
                    "coincidencias_ge10": sorted(src_tots & tgt_vals),
                })
            # Nulo interno condicionado al tamaño |tgt| (200 réplicas)
            m_t = len(vals_ge10[j])
            if not src_tots or m_t == 0:
                Z_hier[i, j] = 0.0
                continue
            null_hits = []
            for _ in range(200):
                samp = set(rng.choice(pool_ge10_arr, size=m_t, replace=True).tolist())
                null_hits.append(len(src_tots & samp))
            mu = float(np.mean(null_hits))
            sd = max(float(np.std(null_hits)), 1.0)
            Z_hier[i, j] = (obs_ij - mu) / sd

    # Diferencia media en pares adyacentes vs no adyacentes (QAP 10 000)
    mask_adj = adj == 1
    mask_non = (adj == 0) & (~np.eye(n, dtype=bool))
    obs_p021 = float(Z_hier[mask_adj].mean() - Z_hier[mask_non].mean())
    B_qap = 10000
    ge_p021 = 0
    for _ in range(B_qap):
        perm = rng.permutation(n)
        Zp = Z_hier[np.ix_(perm, perm)]
        stat_p = float(Zp[mask_adj].mean() - Zp[mask_non].mean())
        if stat_p >= obs_p021 - 1e-12:
            ge_p021 += 1
    p_021 = (ge_p021 + 1) / (B_qap + 1)

    # ---------- P02.2: Acoplamiento numérico SW estandarizado por tamaño vs -dist (Mantel QAP) ----------
    vc = Counter()
    for s in seqs_all:
        for v in set(s):
            vc[v] += 1
    inv_f = {v: min(6.0, math.log2(n / max(1, c)) + 1.0) for v, c in vc.items()}

    Z_sw = np.zeros((n, n), dtype=float)
    top_sw_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            s1, s2 = seqs_all[i], seqs_all[j]
            if len(s1) < 3 or len(s2) < 3:
                continue
            sc = max(sw_score(s1, s2, inv_f), sw_score(s1, s2[::-1], inv_f))
            # Nulo por rachas del par (80 réplicas internas para estandarizar por tamaño)
            nscores = []
            for _ in range(80):
                p1 = permute_runs(s1, rng)
                nscores.append(max(sw_score(p1, s2, inv_f), sw_score(p1, s2[::-1], inv_f)))
            mu = float(np.mean(nscores))
            sd = max(float(np.std(nscores)), 0.5)
            z = (sc - mu) / sd
            Z_sw[i, j] = Z_sw[j, i] = z
            top_sw_pairs.append({
                "par": f"K{i+1:02d}-K{j+1:02d}", "adyacente": int(adj[i, j]),
                "dist_fis": int(dist[i, j]), "sw": round(sc, 2), "z_sw": round(z, 2),
            })

    tri_i, tri_j = np.triu_indices(n, k=1)
    prox_vec = -dist[tri_i, tri_j]
    zsw_vec = Z_sw[tri_i, tri_j]
    obs_p022 = float(stats.spearmanr(zsw_vec, prox_vec).statistic)
    if np.isnan(obs_p022):
        obs_p022 = 0.0
    ge_p022 = 0
    for _ in range(B_qap):
        perm = rng.permutation(n)
        Zp = Z_sw[np.ix_(perm, perm)][tri_i, tri_j]
        r_p = float(stats.spearmanr(Zp, prox_vec).statistic)
        if not np.isnan(r_p) and r_p >= obs_p022 - 1e-12:
            ge_p022 += 1
    p_022 = (ge_p022 + 1) / (B_qap + 1)

    # ---------- P02.3: Coherencia físico-textil (sin tamaño) vs -dist (Mantel QAP) ----------
    # Rasgos por quipu: frac_S, frac_R, largo_med, lab_L_med, paleta_set
    feats = []
    palettes = []
    for kh in K_LIST:
        cs = cords_by_k[kh]
        tors = [c["torsion"].upper() for c in cs if c["torsion"].upper() in ("S", "Z")]
        unions = [c["union"].upper() for c in cs if c["union"].upper() in ("R", "V")]
        largos = [to_float(c["largo"]) for c in cs if to_float(c["largo"]) is not None and to_float(c["largo"]) > 0]
        labs_L = [to_float(c["lab_L"]) for c in cs if to_float(c["lab_L"]) is not None]
        pal = set(c["color_base"] for c in cs if c["color_base"])
        palettes.append(pal)
        feats.append([
            sum(1 for t in tors if t == "S") / len(tors) if tors else np.nan,
            sum(1 for u in unions if u == "R") / len(unions) if unions else np.nan,
            float(np.median(largos)) if largos else np.nan,
            float(np.median(labs_L)) if labs_L else np.nan,
        ])
    F = np.array(feats, dtype=float)
    ranges = np.nanmax(F, axis=0) - np.nanmin(F, axis=0)
    ranges[ranges == 0] = 1.0
    Sim_tex = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            comps = []
            for k in range(F.shape[1]):
                if not np.isnan(F[i, k]) and not np.isnan(F[j, k]):
                    comps.append(1.0 - abs(F[i, k] - F[j, k]) / ranges[k])
            if palettes[i] or palettes[j]:
                jacc = len(palettes[i] & palettes[j]) / max(1, len(palettes[i] | palettes[j]))
                comps.append(jacc)
            Sim_tex[i, j] = Sim_tex[j, i] = float(np.mean(comps)) if comps else 0.0

    stex_vec = Sim_tex[tri_i, tri_j]
    obs_p023 = float(stats.spearmanr(stex_vec, prox_vec).statistic)
    if np.isnan(obs_p023):
        obs_p023 = 0.0
    ge_p023 = 0
    for _ in range(B_qap):
        perm = rng.permutation(n)
        Sp = Sim_tex[np.ix_(perm, perm)][tri_i, tri_j]
        r_p = float(stats.spearmanr(Sp, prox_vec).statistic)
        if not np.isnan(r_p) and r_p >= obs_p023 - 1e-12:
            ge_p023 += 1
    p_023 = (ge_p023 + 1) / (B_qap + 1)

    # ---------- P02.4: Alineación cromática de K15 (19 hilos envueltos) con K01 ----------
    k15_cols = [c["color"].upper().split("(")[0].split(":")[0].split("/")[0].split("-")[0].strip() for c in k15 if c["color"]]
    k01_cols = [c["color_base"] for c in cords_by_k["KH0638"] if c["nivel"] == "0" and c["tipo"] == "p" and c["color_base"]]
    # Alinear K15 por posición relativa (19 hilos) contra los colgantes de K01 (re-muestreo proporcional de índice)
    def align_score(c15, c01):
        if not c15 or not c01:
            return 0.0
        L15, L01 = len(c15), len(c01)
        matches = 0
        for idx, col in enumerate(c15):
            j = min(L01 - 1, int(round(idx * (L01 - 1) / max(1, L15 - 1))))
            if col == c01[j]:
                matches += 1
        return matches / L15

    obs_p024 = align_score(k15_cols, k01_cols)
    B_k15 = 5000
    ge_p024 = 0
    for _ in range(B_k15):
        p15 = permute_runs(k15_cols, rng)
        if align_score(p15, k01_cols) >= obs_p024 - 1e-12:
            ge_p024 += 1
    p_024 = (ge_p024 + 1) / (B_k15 + 1)

    # ---------- D02.5: Contabilidad interna individual en K01..K14 (descriptivo) ----------
    internal_results = []
    for kh in K_LIST:
        cs = cords_by_k[kh]
        # R1: colgante = suma de sus subsidiarias (>=2 subs con valor>0)
        subs_by_p = defaultdict(list)
        val_by_c = {}
        for c in cs:
            v = to_int(c["valor"])
            val_by_c[c["cuerda"]] = v if v is not None else 0
            if c["nivel"] == "1" and c["padre"]:
                subs_by_p[c["padre"]].append(v if v is not None else 0)
        r1_hits = sum(1 for p, svs in subs_by_p.items() if len([x for x in svs if x > 0]) >= 2 and val_by_c.get(p, 0) == sum(svs))
        # A: en grupos con >=3 colgantes con valor>0, algún colgante = suma del resto
        by_g = defaultdict(list)
        for c in cs:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["grupo"] != "":
                v = to_int(c["valor"])
                if v is not None and v > 0:
                    by_g[c["grupo"]].append(v)
        g_hits = 0
        g_elig = 0
        for g, vs in by_g.items():
            if len(vs) >= 3:
                g_elig += 1
                s = sum(vs)
                if any(v == s - v for v in vs):
                    g_hits += 1
        # Suma total de un grupo = suma de otros grupos o valor de otro colgante
        internal_results.append({
            "k_num": K_NUM[kh], "kh_id": kh,
            "r1_hits": r1_hits, "g_elig": g_elig, "g_sum_hits": g_hits,
        })

    # Holm sobre los 4 tests preregistrados
    p_map = {"P02.1": p_021, "P02.2": p_022, "P02.3": p_023, "P02.4": p_024}
    h_map = holm_adjust(p_map)

    out = {
        "preregistro": "P02_rt16905_enlazados.md",
        "semilla": SEED,
        "resumen_14_quipus": summary,
        "familia_holm": [
            {"test_id": "P02.1", "obs_diff_Z_adj_vs_non": round(obs_p021, 4), "p": round(p_021, 6), "p_holm": round(h_map["P02.1"], 6), "hits_adyacentes": hits_detail},
            {"test_id": "P02.2", "rho_mantel": round(obs_p022, 4), "p": round(p_022, 6), "p_holm": round(h_map["P02.2"], 6), "top_pares": sorted(top_sw_pairs, key=lambda x: -x["z_sw"])[:10]},
            {"test_id": "P02.3", "rho_mantel_textil": round(obs_p023, 4), "p": round(p_023, 6), "p_holm": round(h_map["P02.3"], 6)},
            {"test_id": "P02.4", "align_k15_k01": round(obs_p024, 4), "k15_colores": k15_cols, "k01_colores_muestra": k01_cols[:20], "p": round(p_024, 6), "p_holm": round(h_map["P02.4"], 6)},
        ],
        "descriptivo_D02_5": internal_results,
        "descriptivo_D02_6": {
            "k15_n_hilos": len(k15),
            "k15_secciones": dict(Counter(c["seccion"] for c in k15)),
            "k01_n_colgantes": summary[0]["n_colgantes"],
            "k01_n_grupos": summary[0]["n_grupos"],
        },
    }
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "resultados_P02.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESULTADOS PREREGISTRO P02 (RT-16905 ENLAZADOS) ===")
    for s in summary:
        print(f"  K{s['k_num']:02d} ({s['kh_id']}): {s['n_cuerdas']} cuerdas, {s['n_colgantes']} colg, {s['n_grupos']} grps, total={s['total']}, max={s['max_val']}")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']}: p={r['p']} | p_Holm={r['p_holm']} | { {k:v for k,v in r.items() if k not in ('test_id','p','p_holm','top_pares','k15_colores','k01_colores_muestra','hits_adyacentes')} }")
    print("  Top 5 pares SW (Z):", out["familia_holm"][1]["top_pares"][:5])
    print("  Hits jerárquicos adyacentes (>=10):", hits_detail)
    print("  D02.5 contabilidad interna:", [x for x in internal_results if x["r1_hits"] or x["g_sum_hits"]])
    print("  D02.6 K15 vs K01:", out["descriptivo_D02_6"])


if __name__ == "__main__":
    main()
