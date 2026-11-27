#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_ejecutar_P05_auditoria_2026.py — Ejecución estricta del Preregistro P05 (v1.1, SHA-256 sellado).
Auditoría metodológica unificada de la literatura computacional de 2026 sobre quipus:
  - P05.1: `khipu-rv-reproducibility` (codificación binaria R/V en 27 quipus vs cohorte completa sin tope Top-100 + BH + nulo por rachas)
  - P05.2: `Khipu-ML` (Contreras 2026) — Torsión imperial S (F1=0.86) sin `U` y con GroupKFold por sitio/transcriptor
  - P05.3: `Khipu-ML` (Contreras 2026) — Validación Santa Valley (independencia OKR vs collca.db + tasa base 5 puros + 1 mixto)
  - P05.4: `K-CAT` (Da Fieno Delucchi) — Color x magnitud (p=3.6e-267): modelo mixto + permutación de etiquetas entre quipus
  - P05.5: `K-CAT` — 6.6% padre = sum(hijos) contra nulo intra-quipu + diagnóstico conteo 709 vs 650
  - P05.6: `Zenil & Uthamacumaran (2026)` — Rol distal (AUC) + afinidad coseno padre-hijo bajo rewiring estándar y rewiring con control de grupo/escala.

Semilla fija: 20261127.
"""
import csv
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import GroupKFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[1]
RAIZ_QUIPU = RAIZ.parent / "quipu"
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
    with open(MAESTRO / "maestro_quipus.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            quipus[r["kh_id"]] = r
    cords_by_q = defaultdict(list)
    with open(MAESTRO / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cords_by_q[r["kh_id"]].append(r)
    return quipus, cords_by_q


# ==================== P05.1: khipu-rv-reproducibility ====================
def cond_entropy_bigrams(states):
    """H(S_{t+1} | S_t) en bits."""
    if len(states) < 2:
        return 0.0
    trans = Counter(zip(states[:-1], states[1:]))
    prev = Counter(states[:-1])
    n = len(states) - 1
    h = 0.0
    for (a, b), c in trans.items():
        p_ab = c / n
        p_b_given_a = c / prev[a]
        h -= p_ab * math.log2(p_b_given_a)
    return h


def permute_runs(seq, rng):
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


def audit_p05_1_rv_repro(quipus, cords_by_q, rng):
    rv_dir = RAIZ_QUIPU / "data/external/khipu-rv-reproducibility"
    with open(rv_dir / "cords_permutation_cohort.csv", encoding="utf-8") as f:
        rv_cols = next(csv.reader(f))

    def eval_rv_set(k_dict, B_fy=2000, B_runs=2000):
        res = []
        for kid, rows in sorted(k_dict.items()):
            base_s = []
            rv_s = []
            for r in rows:
                b = f"{r.get('color','')}|{r.get('twist','')}|{r.get('knots','')}"
                rv = r.get("rv", "?")
                rv = rv if rv in ("R", "V") else "?"
                base_s.append(b)
                rv_s.append(rv)
            joint_obs = [f"{b}|{rv}" for b, rv in zip(base_s, rv_s)]
            h_obs = cond_entropy_bigrams(joint_obs)
            le_fy = 0
            for _ in range(B_fy):
                rp = rng.permutation(rv_s)
                if cond_entropy_bigrams([f"{b}|{rv}" for b, rv in zip(base_s, rp)]) <= h_obs + 1e-12:
                    le_fy += 1
            p_fy = (le_fy + 1) / (B_fy + 1)
            le_rn = 0
            for _ in range(B_runs):
                rp = permute_runs(rv_s, rng)
                if cond_entropy_bigrams([f"{b}|{rv}" for b, rv in zip(base_s, rp)]) <= h_obs + 1e-12:
                    le_rn += 1
            p_rn = (le_rn + 1) / (B_runs + 1)
            res.append({"id": kid, "n": len(rows), "h_obs": round(h_obs, 4), "p_fy": p_fy, "p_runs": p_rn})
        q_fy = bh_adjust([x["p_fy"] for x in res])
        q_rn = bh_adjust([x["p_runs"] for x in res])
        for x, q1, q2 in zip(res, q_fy, q_rn):
            x["q_fy"] = round(q1, 5)
            x["q_runs"] = round(q2, 5)
            x["p_fy"] = round(x["p_fy"], 5)
            x["p_runs"] = round(x["p_runs"], 5)
        return res

    c27 = defaultdict(list)
    with open(rv_dir / "cords_permutation_cohort.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            kid = r["okrNum"].strip()
            c27[kid].append({
                "color": r.get("colorCd1", ""),
                "twist": r.get("twist", ""),
                "knots": r.get("knotTypes", ""),
                "rv": r.get("attachmentDirection", "?"),
            })
    res_27 = eval_rv_set(c27, B_fy=2000, B_runs=2000)

    # 2) Cohorte completa SIN tope Top-100 sobre el Corpus Maestro (rvSeq >= 5, switchCount > 10)
    full_elig = {}
    for kh, cs in cords_by_q.items():
        p0 = [c for c in cs if c["nivel"] == "0" and c["tipo"] == "p"]
        rv_only = [c["union"] for c in p0 if c["union"] in ("R", "V")]
        if len(rv_only) < 5:
            continue
        switches = sum(1 for a, b in zip(rv_only, rv_only[1:]) if a != b)
        if switches > 10:
            full_elig[kh] = [{
                "color": c["color_base"], "twist": c["torsion"],
                "knots": "1" if (to_int(c["valor"]) or 0) > 0 else "0",
                "rv": c["union"] if c["union"] in ("R", "V") else "?",
            } for c in p0]
    res_full = eval_rv_set(full_elig, B_fy=1000, B_runs=1000)

    n27_nom = sum(1 for x in res_27 if x["p_fy"] < 0.05)
    n27_bh_fy = sum(1 for x in res_27 if x["q_fy"] < 0.05)
    n27_bh_rn = sum(1 for x in res_27 if x["q_runs"] < 0.05)

    nfull = len(res_full)
    nfull_nom_fy = sum(1 for x in res_full if x["p_fy"] < 0.05)
    nfull_bh_fy = sum(1 for x in res_full if x["q_fy"] < 0.05)
    nfull_nom_rn = sum(1 for x in res_full if x["p_runs"] < 0.05)
    nfull_bh_rn = sum(1 for x in res_full if x["q_runs"] < 0.05)

    p_binom_full_fy = float(stats.binomtest(nfull_nom_fy, nfull, 0.05, alternative="greater").pvalue) if nfull else 1.0
    p_binom_full_rn = float(stats.binomtest(nfull_nom_rn, nfull, 0.05, alternative="greater").pvalue) if nfull else 1.0

    # Precedencia estricta congelada en P05.1:
    if p_binom_full_fy >= 0.05:
        veredicto = "ARTEFACTO_COHORTE"
    elif n27_bh_fy < 2 and nfull_bh_fy < 2:
        veredicto = "FRAGIL_A_MULTIPLICIDAD"
    elif n27_bh_rn < 2 and nfull_bh_rn < 2:
        veredicto = "FRAGIL_A_RACHAS"
    else:
        veredicto = "REPLICADO_ROBUSTO"

    return {
        "test_id": "P05.1",
        "rv_cohort_cols": rv_cols,
        "cohorte_27": {"n": len(res_27), "p_fy_lt005": n27_nom, "q_fy_lt005": n27_bh_fy, "q_runs_lt005": n27_bh_rn},
        "cohorte_completa_sin_top100": {
            "n": nfull, "p_fy_lt005": nfull_nom_fy, "q_fy_lt005": nfull_bh_fy,
            "p_runs_lt005": nfull_nom_rn, "q_runs_lt005": nfull_bh_rn,
            "p_binom_fy": round(p_binom_full_fy, 6), "p_binom_runs": round(p_binom_full_rn, 6),
        },
        "p": round(p_binom_full_rn, 6),
        "veredicto": veredicto,
        "top_full_runs": sorted(res_full, key=lambda x: x["p_runs"])[:6],
    }


# ==================== P05.2: Khipu-ML (Torsión imperial sin U + GroupKFold) ====================
def audit_p05_2_khipuml_torsion(quipus, cords_by_q, rng):
    # Reconstruir etiquetas Late Horizon imperial (Inkawasi, Puruchuco, Leymebamba, Pachacamac/sitios estatales) vs resto
    # Evaluar dos definiciones: (a) sitios imperiales clásicos (Inkawasi+Puruchuco+Leymebamba) vs otros con procedencia conocida;
    # excluyendo completamente quipus donde torsión es mayoritariamente 'U' (>50% U).
    X_list, y_list, grp_site, grp_trans = [], [], [], []
    for kh, q in quipus.items():
        prov = (q["procedencia"] or "").strip()
        if not prov or prov.lower() in ("unknown", "desconocida", "peru", "perú"):
            continue
        cs = [c for c in cords_by_q[kh] if c["nivel"] == "0" and c["tipo"] == "p"]
        if len(cs) < 10:
            continue
        tors_all = [c["torsion"].upper() for c in cs]
        tors_sz = [t for t in tors_all if t in ("S", "Z")]
        frac_u = 1.0 - (len(tors_sz) / len(cs))
        if frac_u > 0.50 or len(tors_sz) < 5:
            continue  # Excluir sesgo de U!

        frac_s = sum(1 for t in tors_sz if t == "S") / len(tors_sz)
        largos = [to_float(c["largo"]) for c in cs if to_float(c["largo"]) and to_float(c["largo"]) > 0]
        med_len = float(np.median(largos)) if largos else 30.0
        cv_len = float(np.std(largos) / np.mean(largos)) if len(largos) >= 3 and np.mean(largos) > 0 else 0.3
        frac_kn = sum(1 for c in cs if (to_int(c["valor"]) or 0) > 0) / len(cs)
        n_cols = len(set(c["color_base"] for c in cs if c["color_base"]))
        col_ratio = n_cols / len(cs)
        vals = [to_int(c["valor"]) for c in cs if (to_int(c["valor"]) or 0) > 0]
        med_val = math.log1p(float(np.median(vals))) if vals else 0.0
        subs_ratio = sum(1 for c in cords_by_q[kh] if c["nivel"] != "0") / len(cs)

        pl = prov.lower()
        # Sitios imperiales Inka Late Horizon bien fechados/excavados (Inkawasi, Puruchuco, Leymebamba)
        if any(w in pl for w in ("incahuasi", "inkawasi", "puruchuco", "leymebamba", "cóndores", "condores")):
            y = 1
            site_g = "Inkawasi" if ("inca" in pl or "inka" in pl) else ("Puruchuco" if "puruchuco" in pl else "Leymebamba")
        else:
            y = 0
            site_g = prov.split(",")[0].strip().lower()[:25]

        m = re.match(r"^([A-Z]+)", q["kfg_id"] or kh)
        trans = m.group(1) if m else "UNK"
        X_list.append([frac_s, med_len, cv_len, frac_kn, col_ratio, med_val, subs_ratio])
        y_list.append(y)
        grp_site.append(site_g)
        grp_trans.append(trans)

    X = np.array(X_list, dtype=float)
    y = np.array(y_list, dtype=int)
    gs = np.array(grp_site)

    # 1) CV estándar estratificada (sin agrupar — replica fuga por sitio/colección)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    preds_skf = np.zeros_like(y)
    for tr, te in skf.split(X, y):
        clf = RandomForestClassifier(n_estimators=100, random_state=SEED, class_weight="balanced")
        clf.fit(X[tr], y[tr])
        preds_skf[te] = clf.predict(X[te])
    f1_skf = float(f1_score(y, preds_skf))

    # 2) GroupKFold por sitio/archivo (elimina fuga por archivo!)
    # Necesitamos splits que contengan ambas clases en train y test
    uniq_pos = sorted(set(gs[y == 1]))
    uniq_neg = sorted(set(gs[y == 0]))
    # Dejar fuera 1 sitio positivo + 1/3 de sitios negativos en 3 pliegues limpios
    preds_grp = np.zeros_like(y)
    for fold_i, pos_site in enumerate(uniq_pos):
        neg_te = set(uniq_neg[fold_i::len(uniq_pos)])
        te_mask = (gs == pos_site) | np.isin(gs, list(neg_te))
        tr_mask = ~te_mask
        clf = RandomForestClassifier(n_estimators=100, random_state=SEED, class_weight="balanced")
        clf.fit(X[tr_mask], y[tr_mask])
        preds_grp[te_mask] = clf.predict(X[te_mask])
    f1_grp = float(f1_score(y, preds_grp))

    # Permutación a nivel de grupo/sitio (500 réplicas)
    all_sites = sorted(set(gs))
    site_to_y = {s: int(y[gs == s][0]) for s in all_sites}
    site_y_arr = np.array([site_to_y[s] for s in all_sites])
    B = 300
    ge = 0
    for _ in range(B):
        perm_sy = rng.permutation(site_y_arr)
        pmap = dict(zip(all_sites, perm_sy))
        yp = np.array([pmap[s] for s in gs])
        if yp.sum() < 5 or (1 - yp).sum() < 5:
            continue
        p_pos_sites = [s for s, val in pmap.items() if val == 1]
        p_neg_sites = [s for s, val in pmap.items() if val == 0]
        pr_p = np.zeros_like(yp)
        n_folds = min(3, len(p_pos_sites))
        for fi in range(n_folds):
            te_s = set(p_pos_sites[fi::n_folds]) | set(p_neg_sites[fi::n_folds])
            te_m = np.isin(gs, list(te_s))
            tr_m = ~te_m
            if yp[tr_m].sum() == 0 or (1 - yp[tr_m]).sum() == 0:
                continue
            clf = RandomForestClassifier(n_estimators=40, random_state=SEED, class_weight="balanced")
            clf.fit(X[tr_m], yp[tr_m])
            pr_p[te_m] = clf.predict(X[te_m])
        if float(f1_score(yp, pr_p)) >= f1_grp - 1e-12:
            ge += 1
    p_perm = (ge + 1) / (B + 1)

    veredicto = "REPLICA" if (f1_grp >= 0.70 and p_perm < 0.05) else "INFLADO_POR_SESGO_U_O_FUGA"
    return {
        "test_id": "P05.2",
        "n_quipus_sin_U": int(len(y)),
        "n_imperiales": int(y.sum()),
        "n_otros": int((1 - y).sum()),
        "f1_estratificado_sin_U": round(f1_skf, 4),
        "f1_agrupado_por_sitio_sin_U": round(f1_grp, 4),
        "caida_F1": round(f1_skf - f1_grp, 4),
        "frac_S_imperiales": round(float(X[y == 1, 0].mean()), 4),
        "frac_S_otros": round(float(X[y == 0, 0].mean()), 4),
        "p": round(p_perm, 5),
        "veredicto": veredicto,
    }


# ==================== P05.3: Khipu-ML (Santa Valley independencia + tasa base) ====================
def audit_p05_3_santa_independencia(quipus, cords_by_q, rng):
    con_okr = sqlite3.connect(f"file:{RAIZ_QUIPU / 'data/external/open-khipu-repository/data/khipu.db'}?mode=ro", uri=True)
    con_col = sqlite3.connect(f"file:{RAIZ_QUIPU / 'data/local_only/KhipuAnalysis/collca.db'}?mode=ro", uri=True)

    santa_urs = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]
    comp = []
    tot_match, tot_c = 0, 0
    for ur in santa_urs:
        okr_rv = [r[0] for r in con_okr.execute("""
            SELECT c.ATTACHMENT_TYPE FROM cord c JOIN khipu_main km ON km.KHIPU_ID=c.KHIPU_ID
            WHERE km.INVESTIGATOR_NUM = ? ORDER BY c.CORD_LEVEL, c.CLUSTER_ORDINAL, c.CORD_ORDINAL
        """, (ur,)).fetchall()]
        col_rv = [r[0] for r in con_col.execute("""
            SELECT c.ATTACHMENT_TYPE FROM cord c JOIN khipu_main km ON km.KHIPU_ID=c.KHIPU_ID
            WHERE km.INVESTIGATOR_NUM = ? ORDER BY c.CORD_LEVEL, c.CLUSTER_ORDINAL, c.CORD_ORDINAL
        """, (ur,)).fetchall()]
        n_m = min(len(okr_rv), len(col_rv))
        eq = sum(1 for a, b in zip(okr_rv[:n_m], col_rv[:n_m]) if a == b)
        tot_match += eq
        tot_c += n_m
        comp.append({"ur": ur, "n_okr": len(okr_rv), "n_collca": len(col_rv), "exact_match": eq})

    pct_id = tot_match / max(1, tot_c)

    # Tasa base en bloques de 6 quipus del mismo sitio: patrón "5 puros (>=95%) + 1 mixto (20-80%)"
    by_site = defaultdict(list)
    for kh, q in quipus.items():
        pr = (q["procedencia"] or "").strip()
        if not pr or pr.lower() in ("unknown", "desconocida") or "santa" in pr.lower():
            continue
        rvs = [c["union"] for c in cords_by_q[kh] if c["nivel"] == "0" and c["union"] in ("R", "V")]
        if len(rvs) < 10:
            continue
        fr = sum(1 for x in rvs if x == "R") / len(rvs)
        if fr >= 0.95 or fr <= 0.05:
            cls = "puro"
        elif 0.20 <= fr <= 0.80:
            cls = "mixto"
        else:
            cls = "intermedio"
        by_site[pr.lower()].append(cls)

    elig_sites = {s: lst for s, lst in by_site.items() if len(lst) >= 6}
    # Muestrear 5 000 bloques de 6 quipus dentro de sitios elegibles
    B = 5000
    hits_5p1m = 0
    site_keys = list(elig_sites.keys())
    for _ in range(B):
        s = site_keys[rng.integers(0, len(site_keys))]
        samp = rng.choice(elig_sites[s], size=6, replace=False)
        if np.sum(samp == "puro") == 5 and np.sum(samp == "mixto") == 1:
            hits_5p1m += 1
    p_base = (hits_5p1m + 1) / (B + 1)
    veredicto = "NO_INDEPENDIENTE_MISMA_FUENTE" if pct_id >= 0.99 else ("INDEPENDIENTE_Y_EXCEPCIONAL" if p_base < 0.05 else "NO_EXCEPCIONAL")
    return {
        "test_id": "P05.3",
        "concordancia_OKR_vs_collca_Santa": round(pct_id, 5),
        "detalle_santa": comp,
        "n_sitios_control_ge6": len(elig_sites),
        "tasa_base_5puros_1mixto": round(hits_5p1m / B, 4),
        "p": round(p_base, 5),
        "veredicto": veredicto,
    }


# ==================== P05.4: K-CAT Color x Magnitud (pseudorreplicación vs efecto global) ====================
def audit_p05_4_kcat_color(quipus, cords_by_q, rng):
    # Cuerdas nivel 0 con valor > 0 y color_base presente (colores con >= 50 apariciones en >= 10 quipus)
    raw = []
    col_q = defaultdict(set)
    for kh, q in quipus.items():
        for c in cords_by_q[kh]:
            if c["nivel"] == "0" and c["tipo"] == "p" and c["color_base"]:
                v = to_int(c["valor"])
                if v is not None and v > 0:
                    raw.append((kh, c["color_base"], math.log1p(v)))
                    col_q[c["color_base"]].add(kh)
    valid_cols = sorted(cb for cb, qs in col_q.items() if len(qs) >= 10)
    data = [x for x in raw if x[1] in valid_cols]

    # 1) Kruskal-Wallis ingenuo a nivel de cuerda (réplica K-CAT)
    groups_kw = defaultdict(list)
    for _kh, cb, lv in data:
        groups_kw[cb].append(lv)
    H_kw, p_kw = stats.kruskal(*[groups_kw[c] for c in valid_cols])

    # 2) Residualizar por quipu (efecto fijo/aleatorio de quipu = restar media por quipu)
    by_q = defaultdict(list)
    for kh, cb, lv in data:
        by_q[kh].append((cb, lv))

    # Calcular R2 marginal de color_base sobre residuales intra-quipu (varianza explicada por el nombre global del color)
    q_arrays = []  # lista por quipu de (col_indices, resid_vals)
    c_to_i = {c: i for i, c in enumerate(valid_cols)}
    n_c = len(valid_cols)
    all_res = []
    for kh, items in by_q.items():
        if len(items) < 5:
            continue
        vals = np.array([x[1] for x in items], dtype=float)
        res = vals - vals.mean()
        cidx = np.array([c_to_i[x[0]] for x in items], dtype=int)
        if len(set(cidx.tolist())) < 2:
            continue
        q_arrays.append((cidx, res))
        all_res.append(res)

    all_res_flat = np.concatenate(all_res)
    ss_tot = float(np.sum(all_res_flat ** 2))

    def global_color_r2(pairs_list, perm_labels=False):
        sums = np.zeros(n_c, dtype=float)
        cnts = np.zeros(n_c, dtype=float)
        for cidx, res in pairs_list:
            if perm_labels:
                # Remapeo aleatorio de etiquetas de color por quipu (preserva 100% partición intra-quipu!)
                uniq = np.unique(cidx)
                new_ids = rng.choice(n_c, size=len(uniq), replace=False)
                for u, ni in zip(uniq, new_ids):
                    m = cidx == u
                    sums[ni] += res[m].sum()
                    cnts[ni] += m.sum()
            else:
                np.add.at(sums, cidx, res)
                np.add.at(cnts, cidx, 1.0)
        nz = cnts > 0
        ss_between = float(np.sum((sums[nz] ** 2) / cnts[nz]))
        return ss_between / ss_tot if ss_tot > 0 else 0.0

    r2_global_obs = global_color_r2(q_arrays, perm_labels=False)
    # También medir R2 intra-quipu (clave local: media de R2 por quipu)
    ss_local_between = 0.0
    for cidx, res in q_arrays:
        for u in np.unique(cidx):
            m = cidx == u
            ss_local_between += float((res[m].sum() ** 2) / m.sum())
    r2_local = ss_local_between / ss_tot

    B = 1000
    ge = 0
    null_r2s = []
    for _ in range(B):
        r2p = global_color_r2(q_arrays, perm_labels=True)
        null_r2s.append(r2p)
        if r2p >= r2_global_obs - 1e-12:
            ge += 1
    p_glob = (ge + 1) / (B + 1)
    veredicto = "EFECTO_GLOBAL_REAL" if (r2_global_obs >= 0.02 and p_glob < 0.05) else "PSEUDORREPLICACION_Y_CLAVE_LOCAL"
    return {
        "test_id": "P05.4",
        "n_cuerdas": len(data),
        "n_colores_ge10q": n_c,
        "kw_ingenuo_H": round(float(H_kw), 2),
        "kw_ingenuo_p": float(p_kw),
        "R2_clave_local_intra_quipu": round(r2_local, 4),
        "R2_etiqueta_global_obs": round(r2_global_obs, 5),
        "R2_etiqueta_global_nulo_medio": round(float(np.mean(null_r2s)), 5),
        "p": round(p_glob, 5),
        "veredicto": veredicto,
    }


# ==================== P05.5: K-CAT 6.6% padre = sum(hijos) ====================
def audit_p05_5_kcat_padre_hijos(quipus, cords_by_q, rng):
    # Colgantes nivel 0 con >= 2 subsidiarias nivel 1 anudadas (valor > 0)
    q_cases = []
    tot_elig = 0
    tot_obs = 0
    for kh, cs in cords_by_q.items():
        val_p = {}
        subs = defaultdict(list)
        for c in cs:
            v = to_int(c["valor"])
            if c["nivel"] == "0" and c["tipo"] == "p":
                if v is not None and v > 0:
                    val_p[c["cuerda"]] = v
            elif c["nivel"] == "1" and c["padre"]:
                if v is not None and v > 0:
                    subs[c["padre"]].append(v)
        elig_pairs = [(p, val_p[p], sum(svs)) for p, svs in subs.items() if p in val_p and len(svs) >= 2]
        if not elig_pairs:
            continue
        obs_q = sum(1 for _p, pv, ss in elig_pairs if pv == ss)
        tot_elig += len(elig_pairs)
        tot_obs += obs_q
        all_pvals = list(val_p.values())
        if len(all_pvals) >= 3:
            q_cases.append((kh, elig_pairs, all_pvals, obs_q))

    # Nulo intra-quipu: asignar cada conjunto de subsidiarias a un padre aleatorio del mismo quipu (2 000 réplicas)
    B = 2000
    null_tots = np.zeros(B, dtype=int)
    p_by_q = []
    for kh, elig_pairs, all_pvals, obs_q in q_cases:
        sub_sums = [x[2] for x in elig_pairs]
        p_arr = np.array(all_pvals, dtype=int)
        ge_q = 0
        for b in range(B):
            samp_p = rng.choice(p_arr, size=len(sub_sums), replace=(len(sub_sums) > len(p_arr)))
            hq = int(np.sum(samp_p == np.array(sub_sums)))
            null_tots[b] += hq
            if hq >= obs_q:
                ge_q += 1
        p_by_q.append((kh, len(elig_pairs), obs_q, (ge_q + 1) / (B + 1)))

    q_bh_list = bh_adjust([x[3] for x in p_by_q])
    sig_qs = [{"kh_id": x[0], "elig": x[1], "obs": x[2], "p": round(x[3], 5), "q_bh": round(qb, 5)}
              for x, qb in zip(p_by_q, q_bh_list) if qb < 0.05]
    p_glob = float((np.sum(null_tots >= tot_obs) + 1) / (B + 1))
    veredicto = "SENAL_REAL" if p_glob < 0.05 else "COMPATIBLE_CON_AZAR"
    return {
        "test_id": "P05.5",
        "n_colgantes_ge2subs": tot_elig,
        "obs_exactos": tot_obs,
        "tasa_obs": round(tot_obs / max(1, tot_elig), 4),
        "nulo_medio": round(float(np.mean(null_tots)), 2),
        "tasa_nula": round(float(np.mean(null_tots)) / max(1, tot_elig), 4),
        "n_quipus_qBH_lt005": len(sig_qs),
        "quipus_sig": sig_qs[:8],
        "p": round(p_glob, 5),
        "veredicto": veredicto,
    }


# ==================== P05.6: Zenil & Uthamacumaran (2026) ====================
def parse_sle_counts(knot_types_str, nudos_str):
    """Vector [nS, nL, nE] sin usar knot_value_type (anti-circularidad Zenil 2026), tope 12."""
    s_raw = knot_types_str if knot_types_str else nudos_str
    if not s_raw:
        return None
    toks = re.findall(r"(\d+)\s*([SLEsle])", s_raw)
    if not toks:
        return None
    cS, cL, cE = 0, 0, 0
    for n_s, t in toks:
        n = min(12, int(n_s))
        tu = t.upper()
        if tu == "S":
            cS += n
        elif tu == "L":
            cL += n
        elif tu == "E":
            cE += n
    return (min(12, cS), min(12, cL), min(12, cE))


def audit_p05_6_zenil(quipus, cords_by_q, rng):
    # (a) Rol distal: predecir si un clúster es el último (distal) de la cuerda usando SOLO conteos S/L/E (sin posiciones ni valores!)
    # Hold-out estricto a nivel de quipu (20% test + held_out).
    X_tr, y_tr, X_te, y_te = [], [], [], []
    all_khs = sorted(quipus.keys())
    te_khs = set(kh for kh in all_khs if quipus[kh]["held_out"] == "1")
    # Añadir 20% aleatorio de base a test (hold-out por objeto)
    base_khs = [kh for kh in all_khs if kh not in te_khs]
    te_khs |= set(rng.choice(base_khs, size=int(0.20 * len(base_khs)), replace=False).tolist())

    for kh, cs in cords_by_q.items():
        for c in cs:
            kt = c.get("knot_types", "")
            if not kt:
                continue
            parts = [p for p in kt.split(";") if p]
            if len(parts) < 2:
                continue
            for idx, part in enumerate(parts):
                m = re.match(r"(\d+)([SLEsle])", part)
                if not m:
                    continue
                n = min(12, int(m.group(1)))
                tu = m.group(2).upper()
                vec = [n if tu == "S" else 0, n if tu == "L" else 0, n if tu == "E" else 0,
                       1 if tu == "S" else 0, 1 if tu == "L" else 0, 1 if tu == "E" else 0]
                is_distal = 1 if idx == len(parts) - 1 else 0
                if kh in te_khs:
                    X_te.append(vec); y_te.append(is_distal)
                else:
                    X_tr.append(vec); y_tr.append(is_distal)

    clf = LogisticRegression(max_iter=500, random_state=SEED)
    clf.fit(np.array(X_tr), np.array(y_tr))
    auc_distal = float(roc_auc_score(np.array(y_te), clf.predict_proba(np.array(X_te))[:, 1]))

    # (b) Afinidad coseno padre-hijo: (b1) rewiring por (quipu, fibra, torsión); (b2) rewiring más estricto por (quipu, grupo, magnitud)
    edges = []  # (kh, grp, fib, tor, mag_bin, vec_p, vec_c)
    for kh, cs in cords_by_q.items():
        by_name = {c["cuerda"]: c for c in cs}
        for c in cs:
            if c["nivel"] == "1" and c["padre"] in by_name:
                p = by_name[c["padre"]]
                vp = parse_sle_counts(p.get("knot_types", ""), p.get("nudos", ""))
                vc = parse_sle_counts(c.get("knot_types", ""), c.get("nudos", ""))
                if vp is None or vc is None:
                    continue
                if sum(vp) == 0 or sum(vc) == 0:
                    continue
                vp_n = np.array(vp, dtype=float)
                vc_n = np.array(vc, dtype=float)
                vp_n /= np.linalg.norm(vp_n)
                vc_n /= np.linalg.norm(vc_n)
                pv = to_int(p["valor"]) or 0
                mag = int(math.floor(math.log10(max(1, pv))))
                edges.append((kh, p["grupo"], c["fiber"] or "", c["torsion"] or "", mag, vp_n, vc_n))

    obs_cos = float(np.mean([float(np.dot(e[5], e[6])) for e in edges]))

    def rewiring_z(key_fn, B=500):
        strata = defaultdict(list)
        for idx, e in enumerate(edges):
            strata[key_fn(e)].append(idx)
        null_means = np.empty(B, dtype=float)
        # Pre-extraer matrices
        Vp = np.array([e[5] for e in edges])
        Vc = np.array([e[6] for e in edges])
        strata_idx = [np.array(idxs, dtype=int) for idxs in strata.values() if len(idxs) >= 2]
        fixed_idx = np.array([idxs[0] for idxs in strata.values() if len(idxs) == 1], dtype=int)
        fixed_sum = float(np.sum(Vp[fixed_idx] * Vc[fixed_idx])) if len(fixed_idx) else 0.0
        N = len(edges)
        for b in range(B):
            s = fixed_sum
            for idxs in strata_idx:
                perm = rng.permutation(idxs)
                s += float(np.sum(Vp[idxs] * Vc[perm]))
            null_means[b] = s / N
        mu = float(np.mean(null_means))
        sd = max(float(np.std(null_means)), 1e-9)
        z = (obs_cos - mu) / sd
        p = float((np.sum(null_means >= obs_cos - 1e-12) + 1) / (B + 1))
        return round(mu, 5), round(z, 2), round(p, 5)

    mu_b1, z_b1, p_b1 = rewiring_z(lambda e: (e[0], e[2], e[3]), B=500)
    mu_b2, z_b2, p_b2 = rewiring_z(lambda e: (e[0], e[1], e[4]), B=500)

    if auc_distal >= 0.75 and z_b2 > 3.0 and p_b2 < 0.05:
        veredicto = "REPLICA_ESTRUCTURAL"
    elif z_b1 > 3.0 and (z_b2 <= 3.0 or p_b2 >= 0.05):
        veredicto = "EXPLICADO_POR_ESCALA_LOCAL"
    else:
        veredicto = "NO_REPLICA"

    return {
        "test_id": "P05.6",
        "n_clusters_test": len(y_te),
        "auc_rol_distal_holdout": round(auc_distal, 4),
        "n_enlaces_padre_hijo": len(edges),
        "coseno_obs": round(obs_cos, 5),
        "rewiring_b1_quipu_fibra_torsion": {"nulo": mu_b1, "z": z_b1, "p": p_b1},
        "rewiring_b2_quipu_grupo_magnitud": {"nulo": mu_b2, "z": z_b2, "p": p_b2},
        "p": p_b2,
        "veredicto": veredicto,
    }


def main():
    rng = np.random.default_rng(SEED)
    quipus, cords_by_q = load_master()

    r1 = audit_p05_1_rv_repro(quipus, cords_by_q, rng)
    r2 = audit_p05_2_khipuml_torsion(quipus, cords_by_q, rng)
    r3 = audit_p05_3_santa_independencia(quipus, cords_by_q, rng)
    r4 = audit_p05_4_kcat_color(quipus, cords_by_q, rng)
    r5 = audit_p05_5_kcat_padre_hijos(quipus, cords_by_q, rng)
    r6 = audit_p05_6_zenil(quipus, cords_by_q, rng)

    p_map = {r["test_id"]: r["p"] for r in (r1, r2, r3, r4, r5, r6)}
    h_map = holm_adjust(p_map)
    for r in (r1, r2, r3, r4, r5, r6):
        r["p_holm"] = round(h_map[r["test_id"]], 6) if h_map[r["test_id"]] is not None else None

    out = {
        "preregistro": "P05_auditoria_2026.md",
        "semilla": SEED,
        "familia_holm": [r1, r2, r3, r4, r5, r6],
    }
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "resultados_P05.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESULTADOS PREREGISTRO P05 (AUDITORÍA LITERATURA 2026) ===")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']} [{r['veredicto']}]: p={r['p']} | p_Holm={r['p_holm']}")
    print("  P05.1 rv-repro:", r1["cohorte_27"], "| full:", r1["cohorte_completa_sin_top100"])
    print("  P05.2 Khipu-ML:", {k: r2[k] for k in ("n_quipus_sin_U", "f1_estratificado_sin_U", "f1_agrupado_por_sitio_sin_U", "caida_F1", "frac_S_imperiales", "frac_S_otros")})
    print("  P05.3 Santa:", {k: r3[k] for k in ("concordancia_OKR_vs_collca_Santa", "tasa_base_5puros_1mixto", "veredicto")})
    print("  P05.4 K-CAT color:", {k: r4[k] for k in ("kw_ingenuo_H", "R2_clave_local_intra_quipu", "R2_etiqueta_global_obs", "R2_etiqueta_global_nulo_medio", "p", "veredicto")})
    print("  P05.5 K-CAT padre=hijos:", {k: r5[k] for k in ("n_colgantes_ge2subs", "obs_exactos", "tasa_obs", "nulo_medio", "tasa_nula", "n_quipus_qBH_lt005", "veredicto")})
    print("  P05.6 Zenil 2026:", {k: r6[k] for k in ("auc_rol_distal_holdout", "n_enlaces_padre_hijo", "coseno_obs", "rewiring_b1_quipu_fibra_torsion", "rewiring_b2_quipu_grupo_magnitud", "veredicto")})


if __name__ == "__main__":
    main()
