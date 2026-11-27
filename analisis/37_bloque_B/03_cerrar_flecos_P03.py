#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_cerrar_flecos_P03.py — Cierra los 3 flecos exploratorios/descriptivos declarados en P03 §3:
  1. E03.6 (ampliación): Barrido de copias de QU005 (Dallas, bloques de 19) contra los 691 quipus del Corpus Maestro.
  2. E03.7: Barrido de estructura interna y copias en los 4 quipus held-out del British Museum (KH0633, KH0634, KH0635, KH0702).
  3. D03.8: Reverificación de las 3 zonas relativas de altura de nudos de UR050 (KH0280) directamente sobre OKR `khipu.db`.

Semilla fija: 20261127.
"""
import csv
import json
import math
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[1]
MAESTRO = DIR.parent / "36_corpus_maestro"
OKR_DB = RAIZ / "data/external/open-khipu-repository/data/khipu.db"
SEED = 20261127


def to_int(x):
    if x is None or x == "":
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


def load_master():
    qmeta = {}
    with open(MAESTRO / "maestro_quipus.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            qmeta[r["kh_id"]] = r
    cords = defaultdict(list)
    with open(MAESTRO / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cords[r["kh_id"]].append(r)
    return qmeta, cords


def sw_logodds(a, b, log_p):
    """Smith-Waterman rápido sobre secuencias de valores positivos >= 10 (mismo esquema que P01.5/P02.2)."""
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return 0.0
    best = 0.0
    prev = [0.0] * (nb + 1)
    for i in range(1, na + 1):
        ai = a[i - 1]
        cur = [0.0] * (nb + 1)
        for j in range(1, nb + 1):
            sc = (-log_p.get(ai, 9.0)) if ai == b[j - 1] else -2.5
            v = max(0.0, prev[j - 1] + sc, prev[j] - 2.0, cur[j - 1] - 2.0)
            cur[j] = v
            if v > best:
                best = v
        prev = cur
    return best


def main():
    rng = np.random.default_rng(SEED)
    qmeta, cords = load_master()

    # Construir secuencias >=10 por quipu y frecuencias log_p
    seq10 = {}
    cnt_val = Counter()
    tot_val = 0
    for kh, cs in cords.items():
        vs = [to_int(c["valor"]) for c in cs if c["nivel"] == "0" and c["tipo"] == "p"]
        s10 = [v for v in vs if v is not None and v >= 10]
        if len(s10) >= 3:
            seq10[kh] = s10
            cnt_val.update(s10)
            tot_val += len(s10)
    log_p = {v: math.log(cnt / tot_val) for v, cnt in cnt_val.items()}

    def sweep_copies(target_id, min_shared=3):
        t_seq = seq10.get(target_id, [])
        if len(t_seq) < 4:
            return {"n_ge10": len(t_seq), "top_5": [], "copia_confirmada": False}
        t_set = set(t_seq)
        t_rev = list(reversed(t_seq))
        cands = []
        for other, o_seq in seq10.items():
            if other == target_id:
                continue
            shared = len(t_set & set(o_seq))
            if shared < min_shared:
                continue
            sc_d = sw_logodds(t_seq, o_seq, log_p)
            sc_r = sw_logodds(t_rev, o_seq, log_p)
            sc = max(sc_d, sc_r)
            if sc >= 8.0:
                cands.append((sc, other, shared, "dir" if sc_d >= sc_r else "rev"))
        cands.sort(reverse=True)
        top5 = []
        for sc, other, shared, orient in cands[:5]:
            o_seq = seq10[other]
            ge = 0
            B = 1000
            for _ in range(B):
                ps = rng.permutation(o_seq).tolist()
                if max(sw_logodds(t_seq, ps, log_p), sw_logodds(t_rev, ps, log_p)) >= sc - 1e-12:
                    ge += 1
            pv = (ge + 1) / (B + 1)
            q_bonf = min(1.0, pv * len(seq10))
            top5.append({
                "other": other, "kfg": qmeta[other].get("kfg_id", ""),
                "museo": qmeta[other].get("museo", ""), "prov": qmeta[other].get("procedencia", ""),
                "sw": round(sc, 2), "shared_ge10": shared, "orient": orient,
                "p": round(pv, 5), "p_bonf_corpus": round(q_bonf, 4),
            })
        return {
            "n_ge10": len(t_seq),
            "n_candidatos_sw_ge8": len(cands),
            "top_5": top5,
            "copia_confirmada": any(x["p_bonf_corpus"] < 0.05 for x in top5),
        }

    # --- 1) E03.6 ampliación: barrido de copias de QU005 ---
    qu005_kh = next((kh for kh, m in qmeta.items() if m.get("kfg_id") == "QU005" or kh == "QU005"), "QU005")
    e36_copies = sweep_copies(qu005_kh, min_shared=4)

    # --- 2) E03.7: 4 quipus held-out del British Museum (KH0633, KH0634, KH0635, KH0702) ---
    bm_ids = ["KH0633", "KH0634", "KH0635", "KH0702"]
    bm_res = {}
    for kh in bm_ids:
        cs = cords.get(kh, [])
        p = [c for c in cs if c["nivel"] == "0" and c["tipo"] == "p"]
        vs = [to_int(c["valor"]) for c in p]
        vpos = [v for v in vs if v is not None and v > 0]
        by_g = defaultdict(list)
        for c in p:
            v = to_int(c["valor"])
            if v is not None and v > 0:
                by_g[to_int(c["grupo"])].append(v)
        g_elig = [g for g, gv in by_g.items() if len(gv) >= 3]
        g_hits = sum(1 for g in g_elig if any(x == sum(by_g[g]) - x for x in by_g[g]))
        # Permutación rápida para sumas de grupo si hay >=2 hits
        p_gsum = None
        if g_hits >= 1 and len(g_elig) >= 2:
            all_gv = [v for g in g_elig for v in by_g[g]]
            lens = [len(by_g[g]) for g in g_elig]
            ge = 0
            B = 2000
            for _ in range(B):
                perm = rng.permutation(all_gv)
                idx = 0
                h = 0
                for L in lens:
                    sl = perm[idx:idx + L]
                    idx += L
                    s_tot = int(sl.sum())
                    if any(int(x) == s_tot - int(x) for x in sl):
                        h += 1
                if h >= g_hits:
                    ge += 1
            p_gsum = round((ge + 1) / (B + 1), 5)
        bm_res[kh] = {
            "n_cuerdas": len(cs), "n_colgantes": len(p), "n_grupos": len(by_g),
            "n_vals_pos": len(vpos), "max_val": max(vpos) if vpos else 0,
            "g_elig": len(g_elig), "g_sum_hits": g_hits, "p_gsum": p_gsum,
            "barrido_copias": sweep_copies(kh, min_shared=3),
        }

    # --- 3) D03.8: UR050 (KH0280) alturas relativas directamente sobre OKR khipu.db ---
    con = sqlite3.connect(f"file:{OKR_DB.as_posix()}?mode=ro", uri=True)
    cur = con.cursor()
    row_id = cur.execute("SELECT KHIPU_ID, OKR_NUM FROM khipu_main WHERE OKR_NUM='KH0280'").fetchone()
    d38 = {"okr_match": row_id}
    if row_id:
        kid = row_id[0]
        rows = cur.execute("""
            SELECT c.CORD_ID, c.CORD_LENGTH, kc.START_POS
            FROM cord c
            JOIN knot_cluster kc ON kc.CORD_ID = c.CORD_ID
            WHERE c.KHIPU_ID = ? AND c.CORD_LEVEL = 1 AND c.CORD_LENGTH > 0 AND kc.START_POS IS NOT NULL
        """, (kid,)).fetchall()
        rel_h = [pos / clen for _, clen, pos in rows if 0.0 <= pos / clen <= 1.05]
        arr = np.array(rel_h, dtype=float)
        if len(arr) >= 10:
            c3 = np.array([0.20, 0.41, 0.75])
            for _ in range(30):
                lab = np.argmin(np.abs(arr[:, None] - c3[None, :]), axis=1)
                for k_i in range(3):
                    if np.any(lab == k_i):
                        c3[k_i] = float(arr[lab == k_i].mean())
            c3 = np.sort(c3)
            lab = np.argmin(np.abs(arr[:, None] - c3[None, :]), axis=1)
            counts = [int((lab == k_i).sum()) for k_i in range(3)]
            var1 = float(np.var(arr)) + 1e-9
            ll1 = -0.5 * len(arr) * (math.log(2 * math.pi * var1) + 1.0)
            bic1 = -2 * ll1 + 2 * math.log(len(arr))
            ll3 = 0.0
            for k_i in range(3):
                sub = arr[lab == k_i]
                if len(sub) > 1:
                    vk = float(np.var(sub)) + 1e-6
                    wk = len(sub) / len(arr)
                    ll3 += len(sub) * (math.log(wk) - 0.5 * (math.log(2 * math.pi * vk) + 1.0))
            bic3 = -2 * ll3 + 8 * math.log(len(arr))
            d38.update({
                "n_racimos_okr": len(arr),
                "n_colgantes_con_altura": len(set(r[0] for r in rows)),
                "centroides_3_zonas_okr": [round(float(x), 3) for x in c3],
                "conteos_por_zona": counts,
                "delta_BIC_1_vs_3": round(bic1 - bic3, 1),
                "reproduce_zonas_020_041_075": bool(abs(c3[0] - 0.20) < 0.06 and abs(c3[1] - 0.41) < 0.08 and abs(c3[2] - 0.75) < 0.08 and (bic1 - bic3) > 100),
            })
        else:
            d38["n_racimos_okr"] = len(arr)
    con.close()

    out = {
        "semilla": SEED,
        "E03_6_QU005_copias": {"kh_id": qu005_kh, **e36_copies},
        "E03_7_British_Museum": bm_res,
        "D03_8_UR050_OKR": d38,
    }
    (DIR / "resultados_flecos_P03.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("=== FLECOS P03 CERRADOS ===")
    print("E03.6 QU005 copias:", e36_copies["copia_confirmada"], "| top:", e36_copies["top_5"][:3])
    print("E03.7 British Museum:")
    for kh, v in bm_res.items():
        print(f"  {kh}: {v['n_colgantes']} colg, {v['n_grupos']} grps, g_sums={v['g_sum_hits']}/{v['g_elig']} (p={v['p_gsum']}), copia={v['barrido_copias']['copia_confirmada']}, top={v['barrido_copias']['top_5'][:2]}")
    print("D03.8 UR050 OKR:", d38)


if __name__ == "__main__":
    main()
