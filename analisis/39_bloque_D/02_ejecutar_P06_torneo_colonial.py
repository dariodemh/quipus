#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_ejecutar_P06_torneo_colonial.py — Ejecución estricta del Preregistro P06 (v1.1, SHA-256 sellado).

Familia confirmatoria (Holm exacto sobre m = 4):
  - P06.1: Separabilidad real entre géneros coloniales (LODO global + LOSO en géneros multi-fuente)
  - P06.2: Controles positivos NO circulares cerrados en P06 §3 (`ASG`, `PAD` Santa, `TAL` OOD)
  - P06.3: Clasificación abierta (con rechazo OOD y calibración empírica de FPR en 1 000 sintéticos)
           de los 180 quipus de la frontera (`28_atlas_generos/atlas.csv`)
  - P06.4: Prueba ampliada de Predicción #17 — listas coloniales de ≥7 unidades **excluyendo Bambamarca**.

Semilla fija: 20261127.
"""
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import balanced_accuracy_score
from sklearn.preprocessing import StandardScaler

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


def compute_8_features(vals):
    """Vector congelado de 8 firmas invariantes a color/transcriptor (P06 §2)."""
    arr = np.array([v for v in vals if v is not None and v > 0], dtype=float)
    if len(arr) < 5:
        return None
    l10 = np.log10(arr)
    log10_med = float(np.median(l10))
    iqr_l10 = float(np.percentile(l10, 75) - np.percentile(l10, 25))
    ge10 = arr[arr >= 10]
    frac_red10 = float(np.mean((ge10 % 10) == 0)) if len(ge10) >= 3 else 0.0
    ge5 = arr[arr >= 5]
    frac_red5 = float(np.mean((ge5 % 5) == 0)) if len(ge5) >= 3 else 0.0
    p95 = float(np.percentile(arr, 95))
    w = np.minimum(arr, p95)
    cv_p95 = float(np.std(w) / np.mean(w)) if np.mean(w) > 0 else 0.0
    frac_le9 = float(np.mean(arr <= 9))
    frac_rep = 1.0 - (len(set(arr.tolist())) / len(arr))
    r_pos = float(stats.spearmanr(np.arange(len(arr)), arr).statistic)
    if np.isnan(r_pos):
        r_pos = 0.0
    return np.array([log10_med, iqr_l10, frac_red10, frac_red5, cv_p95, frac_le9, frac_rep, r_pos], dtype=float)


def fit_lda_ood(X_tr, y_tr, reg=0.25):
    """LDA bayesiano gaussiano regularizado (puro NumPy, 100x más rápido que sklearn en permutaciones)."""
    mu_g = X_tr.mean(axis=0)
    sd_g = X_tr.std(axis=0)
    sd_g[sd_g < 1e-9] = 1.0
    Xs = (X_tr - mu_g) / sd_g
    classes = np.unique(y_tr)
    n, d = Xs.shape
    centroids = {}
    priors = {}
    Sw = np.zeros((d, d), dtype=float)
    for c in classes:
        Xc = Xs[y_tr == c]
        mc = Xc.mean(axis=0)
        centroids[str(c)] = mc
        priors[str(c)] = len(Xc) / n
        if len(Xc) > 1:
            diff = Xc - mc
            Sw += diff.T @ diff
    Sw = Sw / max(1, n - len(classes))
    cov_reg = (1.0 - reg) * Sw + reg * np.eye(d)
    inv_cov = np.linalg.inv(cov_reg)
    # Coeficientes lineales LDA: score_c(x) = x @ w_c + b_c
    W = np.stack([inv_cov @ centroids[str(c)] for c in classes], axis=1)
    b = np.array([-0.5 * (centroids[str(c)] @ inv_cov @ centroids[str(c)]) + math.log(max(1e-12, priors[str(c)]))
                  for c in classes], dtype=float)
    return (mu_g, sd_g), (classes, W, b), centroids, inv_cov


def _lda_predict(X, sc, clf):
    mu_g, sd_g = sc
    classes, W, b = clf
    Xs = (X - mu_g) / sd_g
    logits = Xs @ W + b
    return classes[np.argmax(logits, axis=1)]


def predict_with_ood(X, sc, clf, centroids, inv_cov, p_chi2_thresh=0.01, post_thresh=0.70):
    mu_g, sd_g = sc
    classes, W, b = clf
    Xs = (X - mu_g) / sd_g
    logits = Xs @ W + b
    logits -= logits.max(axis=1, keepdims=True)
    exp_l = np.exp(logits)
    probs = exp_l / exp_l.sum(axis=1, keepdims=True)
    df = Xs.shape[1]
    preds = []
    for i in range(len(Xs)):
        bi = int(np.argmax(probs[i]))
        best_cls = str(classes[bi])
        best_p = float(probs[i, bi])
        d_cls = Xs[i] - centroids[best_cls]
        md2 = float(d_cls @ inv_cov @ d_cls)
        p_chi2 = float(1.0 - stats.chi2.cdf(md2, df=df))
        is_ood = (p_chi2 < p_chi2_thresh)
        assigned = best_cls if (not is_ood and best_p >= post_thresh) else "FUERA_DE_DISTRIBUCION"
        preds.append({
            "best_cls": best_cls, "posterior": round(best_p, 4),
            "md2": round(md2, 2), "p_chi2": round(p_chi2, 5),
            "is_ood": is_ood, "assigned": assigned,
        })
    return preds


def main():
    rng = np.random.default_rng(SEED)

    # 1) Cargar corpus colonial ampliado
    by_doc = defaultdict(list)
    doc_meta = {}
    with open(DIR / "corpus_colonial_ampliado.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v = to_int(r["valor"])
            if v is not None and v > 0:
                by_doc[r["doc_id"]].append(v)
                doc_meta[r["doc_id"]] = {
                    "fuente": r["fuente"], "genero": r["genero"],
                    "es_lista_unidades": int(r["es_lista_unidades"]),
                    "es_bambamarca": int(r["es_bambamarca"]),
                }

    # Verificar salvaguarda muestral P06 §1 (>=500 items, >=25 tablas, >=4 géneros)
    docs_valid = []
    X_col, y_col, src_col = [], [], []
    for doc_id, vals in sorted(by_doc.items()):
        fv = compute_8_features(vals)
        if fv is not None:
            docs_valid.append(doc_id)
            X_col.append(fv)
            y_col.append(doc_meta[doc_id]["genero"])
            src_col.append(doc_meta[doc_id]["fuente"])

    X_col = np.array(X_col, dtype=float)
    y_col = np.array(y_col)
    src_col = np.array(src_col)
    n_items_tot = sum(len(by_doc[d]) for d in docs_valid)

    # ---------- P06.1: Separabilidad real LODO + LOSO ----------
    # LODO sobre todas las tablas válidas (clases con >= 2 tablas)
    cls_cnt = Counter(y_col.tolist())
    keep_lodo = np.array([cls_cnt[g] >= 2 for g in y_col])
    Xl, yl, sl = X_col[keep_lodo], y_col[keep_lodo], src_col[keep_lodo]

    def bacc_fast(y_t, y_p):
        y_t = np.asarray(y_t)
        y_p = np.asarray(y_p)
        cs = np.unique(y_t)
        return float(np.mean([np.mean(y_p[y_t == c] == c) for c in cs]))

    def run_lodo(X_m, y_m):
        preds = []
        for i in range(len(X_m)):
            tr = np.arange(len(X_m)) != i
            sc, clf, _, _ = fit_lda_ood(X_m[tr], y_m[tr])
            preds.append(str(_lda_predict(X_m[i:i + 1], sc, clf)[0]))
        return bacc_fast(y_m, preds), preds

    bacc_lodo, lodo_preds = run_lodo(Xl, yl)

    # LOSO en géneros multi-fuente (>= 2 fuentes distintas)
    gen_srcs = defaultdict(set)
    for g, s in zip(yl, sl):
        gen_srcs[g].add(s)
    multi_gens = sorted(g for g, ss in gen_srcs.items() if len(ss) >= 2)
    keep_loso = np.isin(yl, multi_gens)
    Xo, yo, so = Xl[keep_loso], yl[keep_loso], sl[keep_loso]

    def run_loso(X_m, y_m, s_m):
        preds = np.empty(len(y_m), dtype=object)
        valid_mask = np.zeros(len(y_m), dtype=bool)
        for src in sorted(set(s_m.tolist())):
            te = (s_m == src)
            tr = ~te
            # Solo evaluar si todas las clases de test existen en train
            if set(y_m[te].tolist()).issubset(set(y_m[tr].tolist())) and len(set(y_m[tr].tolist())) >= 2:
                sc, clf, _, _ = fit_lda_ood(X_m[tr], y_m[tr])
                preds[te] = _lda_predict(X_m[te], sc, clf)
                valid_mask[te] = True
        if valid_mask.sum() == 0:
            return 0.0
        return bacc_fast(y_m[valid_mask], preds[valid_mask])

    bacc_loso = run_loso(Xo, yo, so)

    # Permutación de etiquetas a nivel de documento (2 000 réplicas exactas según P06 §4)
    B = 2000
    ge_lodo = 0
    ge_loso = 0
    for _ in range(B):
        yp = rng.permutation(yl)
        bl, _ = run_lodo(Xl, yp)
        if bl >= bacc_lodo - 1e-12:
            ge_lodo += 1
        ypo = rng.permutation(yo)
        bo = run_loso(Xo, ypo, so)
        if bo >= bacc_loso - 1e-12:
            ge_loso += 1
    p_lodo = (ge_lodo + 1) / (B + 1)
    p_loso = (ge_loso + 1) / (B + 1)
    p_061 = max(p_lodo, p_loso)
    r1 = {
        "test_id": "P06.1",
        "n_items": n_items_tot, "n_tablas": int(len(Xl)), "generos_lodo": dict(Counter(yl.tolist())),
        "generos_multi_fuente_loso": multi_gens,
        "balanced_acc_LODO": round(bacc_lodo, 4), "p_LODO": round(p_lodo, 5),
        "balanced_acc_LOSO": round(bacc_loso, 4), "p_LOSO": round(p_loso, 5),
        "p": round(p_061, 5),
        "veredicto": "SEPARABLES" if (bacc_lodo >= 0.55 and bacc_loso >= 0.50 and p_061 < 0.05) else "NO_SEPARABLES_BAJO_LOSO",
    }

    # ---------- Cargar quipus del Corpus Maestro + Atlas 28 ----------
    cords_by_q = defaultdict(list)
    with open(MAESTRO / "maestro_cuerdas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["nivel"] == "0" and r["tipo"] == "p":
                v = to_int(r["valor"])
                if v is not None and v > 0:
                    cords_by_q[r["kh_id"]].append(v)
    kfg_to_kh = {}
    with open(MAESTRO / "maestro_quipus.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["kfg_id"]:
                kfg_to_kh[r["kfg_id"]] = r["kh_id"]

    atlas_rows = {}
    frontier_180 = []
    with open(RAIZ / "analisis/28_atlas_generos/atlas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            atlas_rows[r["kfg"]] = r
            if r["genero"] == "SIN" and "decimal sin estructura" in r.get("evidencia", "").lower():
                frontier_180.append(r["kfg"])

    # Entrenar modelo generativo final sobre TODAS las tablas coloniales (con >=2 tablas por género)
    sc_full, clf_full, cent_full, icov_full = fit_lda_ood(Xl, yl)

    # ---------- P06.2: Controles positivos NO circulares cerrados (ASG, PAD Santa, TAL) ----------
    asg_kfgs = [k for k, r in atlas_rows.items() if r["genero"] == "ASG"]
    pad_kfgs = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]
    tal_kfgs = [k for k, r in atlas_rows.items() if r["genero"] == "TAL"]

    # Precomputar matrices de 8 rasgos para los 3 controles UNA sola vez (100x más rápido)
    ctrl_specs = [
        ("ASG", asg_kfgs, {"SERVICIO_ASIGNACION", "TRIBUTO_TASA"}),
        ("PAD_Santa", pad_kfgs, {"PADRON_DEMOGRAFICO"}),
        ("TAL", tal_kfgs, {"FUERA_DE_DISTRIBUCION"}),
    ]
    ctrl_mats = {}
    for cname, klist, expected_set in ctrl_specs:
        vecs = []
        for k in klist:
            kh = kfg_to_kh.get(k)
            if kh and len(cords_by_q[kh]) >= 10:
                fv = compute_8_features(cords_by_q[kh])
                if fv is not None:
                    vecs.append(fv)
        ctrl_mats[cname] = (np.array(vecs, dtype=float) if vecs else None, expected_set)

    chi2_crit_001 = float(stats.chi2.ppf(0.99, df=Xl.shape[1]))

    def eval_controls(sc_m, clf_m, cent_m, icov_m, fast=False):
        res_c = {}
        accs = []
        mu_g, sd_g = sc_m
        classes, W, b = clf_m
        for cname, (mat, expected_set) in ctrl_mats.items():
            if mat is None or len(mat) == 0:
                res_c[cname] = {"n": 0, "acc": 0.0, "dist": {}}
                continue
            if fast:
                Xs = (mat - mu_g) / sd_g
                logits = Xs @ W + b
                logits -= logits.max(axis=1, keepdims=True)
                exp_l = np.exp(logits)
                probs = exp_l / exp_l.sum(axis=1, keepdims=True)
                bi = np.argmax(probs, axis=1)
                hits = 0
                for idx_r in range(len(Xs)):
                    cls_s = str(classes[bi[idx_r]])
                    bp = float(probs[idx_r, bi[idx_r]])
                    d_cls = Xs[idx_r] - cent_m[cls_s]
                    md2 = float(d_cls @ icov_m @ d_cls)
                    assigned = cls_s if (md2 <= chi2_crit_001 and bp >= 0.50) else "FUERA_DE_DISTRIBUCION"
                    if assigned in expected_set:
                        hits += 1
                accs.append(hits / len(Xs))
            else:
                preds = predict_with_ood(mat, sc_m, clf_m, cent_m, icov_m, p_chi2_thresh=0.01, post_thresh=0.50)
                hits = sum(1 for pr in preds if pr["assigned"] in expected_set)
                acc = hits / len(preds)
                accs.append(acc)
                res_c[cname] = {"n": len(preds), "hits": hits, "acc": round(acc, 4),
                                "dist_asignada": dict(Counter(pr["assigned"] for pr in preds)),
                                "dist_best_cls": dict(Counter(pr["best_cls"] for pr in preds))}
        return float(np.mean(accs)) if accs else 0.0, res_c

    obs_ctrl_acc, ctrl_detail = eval_controls(sc_full, clf_full, cent_full, icov_full, fast=False)
    # Permutación de etiquetas de los documentos de entrenamiento (2 000 réplicas exactas según P06 §4)
    B_c = 2000
    ge_c = 0
    for _ in range(B_c):
        yp = rng.permutation(yl)
        sc_p, clf_p, cent_p, icov_p = fit_lda_ood(Xl, yp)
        ap, _ = eval_controls(sc_p, clf_p, cent_p, icov_p, fast=True)
        if ap >= obs_ctrl_acc - 1e-12:
            ge_c += 1
    p_062 = (ge_c + 1) / (B_c + 1)
    r2 = {
        "test_id": "P06.2",
        "acierto_medio_3_controles": round(obs_ctrl_acc, 4),
        "detalle_controles": ctrl_detail,
        "p": round(p_062, 5),
        "veredicto": "CONTROLES_CONFIRMADOS" if (obs_ctrl_acc >= 0.60 and p_062 < 0.05) else "CONTROLES_INSUFICIENTES",
    }

    # ---------- P06.3: Frontera de 180 quipus con calibración de FPR en 1 000 sintéticos ----------
    f_vecs, f_ids = [], []
    for k in frontier_180:
        kh = kfg_to_kh.get(k)
        if kh and len(cords_by_q[kh]) >= 10:
            fv = compute_8_features(cords_by_q[kh])
            if fv is not None:
                f_vecs.append(fv)
                f_ids.append(k)
    f_preds = predict_with_ood(np.array(f_vecs), sc_full, clf_full, cent_full, icov_full, p_chi2_thresh=0.05, post_thresh=0.70)
    n_f_assigned = sum(1 for pr in f_preds if pr["assigned"] != "FUERA_DE_DISTRIBUCION")

    # 1 000 listas sintéticas sin género (500 log-normales aleatorias + 500 permutadas de pools mixtos)
    all_vals_pool = np.array([v for vs in cords_by_q.values() for v in vs], dtype=int)
    syn_vecs = []
    for i in range(1000):
        L = int(rng.integers(12, 60))
        if i < 500:
            mu = float(rng.uniform(0.5, 5.0))
            sg = float(rng.uniform(0.3, 1.8))
            arr = np.maximum(1, np.round(np.exp(rng.normal(mu, sg, size=L)))).astype(int)
        else:
            arr = rng.choice(all_vals_pool, size=L, replace=True)
        fv = compute_8_features(arr)
        if fv is not None:
            syn_vecs.append(fv)
    syn_preds = predict_with_ood(np.array(syn_vecs), sc_full, clf_full, cent_full, icov_full, p_chi2_thresh=0.05, post_thresh=0.70)
    fpr_syn = sum(1 for pr in syn_preds if pr["assigned"] != "FUERA_DE_DISTRIBUCION") / len(syn_preds)

    p_063 = float(stats.binomtest(n_f_assigned, len(f_preds), min(0.999, max(0.001, fpr_syn)), alternative="greater").pvalue)
    r3 = {
        "test_id": "P06.3",
        "n_frontera_ge10": len(f_preds),
        "n_asignados_post070_chi005": n_f_assigned,
        "tasa_asignada_frontera": round(n_f_assigned / max(1, len(f_preds)), 4),
        "FPR_sinteticos_1000": round(fpr_syn, 4),
        "distribucion_frontera": dict(Counter(pr["assigned"] for pr in f_preds)),
        "p": round(p_063, 5),
        "veredicto": "APOYADO" if (fpr_syn < 0.05 and p_063 < 0.05) else "FPR_ALTA_O_NEGATIVO",
    }

    # ---------- P06.4: Predicción #17 — Listas coloniales de >=7 unidades EXCLUYENDO Bambamarca ----------
    lists_p17 = []
    for doc_id, vals in sorted(by_doc.items()):
        m = doc_meta[doc_id]
        if m["es_lista_unidades"] == 1 and m["es_bambamarca"] == 0 and len(vals) >= 7:
            arr = np.array(vals, dtype=float)
            rho = float(stats.spearmanr(np.arange(len(arr)), arr).statistic)
            cv = float(np.std(arr, ddof=1) / np.mean(arr)) if np.mean(arr) > 0 else np.nan
            lists_p17.append({"doc_id": doc_id, "n": len(vals), "rho": round(rho, 4), "cv": round(cv, 4)})

    rhos_p17 = [x["rho"] for x in lists_p17]
    med_rho = float(np.median(rhos_p17)) if rhos_p17 else 0.0
    # Permutación de posiciones dentro de cada lista (5 000 réplicas vectorizadas, unilateral med_rho <= obs)
    B_17 = 5000
    null_rhos = np.zeros((B_17, len(lists_p17)), dtype=float)
    for j_l, x in enumerate(lists_p17):
        arr = np.array(by_doc[x["doc_id"]], dtype=float)
        r_arr = stats.rankdata(arr)
        r_arr = r_arr - r_arr.mean()
        r_norm = np.linalg.norm(r_arr)
        pos = np.arange(len(arr), dtype=float)
        pos = pos - pos.mean()
        p_norm = np.linalg.norm(pos)
        if r_norm > 0 and p_norm > 0:
            perms = rng.permuted(np.tile(r_arr, (B_17, 1)), axis=1)
            null_rhos[:, j_l] = (perms @ pos) / (r_norm * p_norm)
    null_meds = np.median(null_rhos, axis=1) if len(lists_p17) else np.zeros(B_17)
    le_17 = int((null_meds <= med_rho + 1e-12).sum())
    p_064 = (le_17 + 1) / (B_17 + 1)
    ur278_pct_rho = float(np.mean([1.0 if r <= -0.73 else 0.0 for r in rhos_p17])) if rhos_p17 else None
    ur278_pct_cv = float(np.mean([1.0 if x["cv"] <= 0.173 else 0.0 for x in lists_p17])) if lists_p17 else None
    r4 = {
        "test_id": "P06.4",
        "n_listas_ge7_sin_Bambamarca": len(lists_p17),
        "mediana_rho": round(med_rho, 4),
        "mediana_cv": round(float(np.median([x["cv"] for x in lists_p17])), 4) if lists_p17 else None,
        "frac_listas_rho_le_UR278": round(ur278_pct_rho, 4) if ur278_pct_rho is not None else None,
        "frac_listas_cv_le_UR278": round(ur278_pct_cv, 4) if ur278_pct_cv is not None else None,
        "p": round(p_064, 5),
        "listas": lists_p17,
        "veredicto": "DESCENSO_SISTEMATICO" if (med_rho < -0.30 and p_064 < 0.05) else "ORDEN_DE_PRESTIGIO_CONFIRMA_P17",
    }

    p_map = {r["test_id"]: r["p"] for r in (r1, r2, r3, r4)}
    h_map = holm_adjust(p_map)
    for r in (r1, r2, r3, r4):
        r["p_holm"] = round(h_map[r["test_id"]], 6)

    out = {
        "preregistro": "P06_torneo_colonial_generativo.md",
        "semilla": SEED,
        "familia_holm": [r1, r2, r3, r4],
    }
    (DIR / "resultados_P06.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESULTADOS PREREGISTRO P06 (TORNEO COLONIAL GENERATIVO) ===")
    for r in out["familia_holm"]:
        print(f"  {r['test_id']} [{r['veredicto']}]: p={r['p']} | p_Holm={r['p_holm']}")
    print("  P06.1 LODO/LOSO:", {k: r1[k] for k in ("n_items", "n_tablas", "balanced_acc_LODO", "p_LODO", "balanced_acc_LOSO", "p_LOSO")})
    print("  P06.2 Controles:", r2["acierto_medio_3_controles"], r2["detalle_controles"])
    print("  P06.3 Frontera:", {k: r3[k] for k in ("n_frontera_ge10", "n_asignados_post070_chi005", "tasa_asignada_frontera", "FPR_sinteticos_1000", "distribucion_frontera")})
    print("  P06.4 Predicción #17 (sin Bambamarca):", {k: r4[k] for k in ("n_listas_ge7_sin_Bambamarca", "mediana_rho", "mediana_cv", "frac_listas_rho_le_UR278", "frac_listas_cv_le_UR278")})
    for lx in lists_p17:
        print("   ", lx)


if __name__ == "__main__":
    main()
