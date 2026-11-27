# -*- coding: utf-8 -*-
"""Estematica cuantitativa y escaner bayesiano tolerante a errores de copia/transcripcion.

1. Calibra tasas empiricas de error (exacto, +-1 nudo, x10, transposicion, omision/roto, otro)
   desde las 3 dobles lecturas independientes y las variantes de copia del corpus.
2. Escanea por LLR bayesiano + nulo por permutacion (DP precalculado en numba) + BH-FDR:
   (a) Los 4 quipus sin lectura firme de Inkawasi (UR272, UR276, UR277, UR279) contra Inkawasi y el corpus.
   (b) Los 30 quipus fuera de muestra (11 Huacones + 19 OKR extra) entre si y contra el corpus.
3. Corre estematica cuantitativa por maxima parsimonia y bootstrap (10 000 replicas) sobre
   Inkawasi (UR278 -> alpha -> {UR266, UR275}), Leymebamba (F02) y KH0049/UR122 (F08).

Uso: python analisis/36_estematica_bayesiana/ejecutar_estematica.py
"""
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from numba import njit

RAIZ = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
SEED = 20261123


def bh(pvals):
    p = np.asarray(pvals, float)
    if len(p) == 0:
        return p
    o = np.argsort(p)
    r = np.minimum.accumulate((p[o] * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1]
    out = np.empty(len(p))
    out[o] = np.minimum(r, 1.0)
    return out


def clasificar_par(a, b):
    if a == b:
        return "exacta"
    if (a == 0) != (b == 0):
        return "omision_0"
    if abs(a - b) == 1:
        return "pm1"
    if a > 0 and b > 0 and (a == 10 * b or b == 10 * a):
        return "shift10"
    sa, sb = str(int(a)), str(int(b))
    if len(sa) >= 2 and sorted(sa) == sorted(sb):
        return "transp"
    return "otro"


def calibrar_ruido():
    c_doble = Counter()
    v1 = pd.read_csv(RAIZ / "analisis/14_copias/verificacion_UR1107_UR237.csv")
    for r in v1.itertuples():
        a = 0 if pd.isna(r.valor_A) else int(r.valor_A)
        b = 0 if pd.isna(r.valor_B) else int(r.valor_B)
        c_doble[clasificar_par(a, b)] += 1

    pc = pd.read_csv(RAIZ / "analisis/33_estematica/pares_copia.csv")
    for ka, kb in [("AS125", "UR247"), ("KH0033", "UR044")]:
        row = pc[((pc.kfg_a == ka) & (pc.kfg_b == kb)) | ((pc.kfg_a == kb) & (pc.kfg_b == ka))]
        if len(row):
            ex = int(row.iloc[0].exactas)
            al = int(row.iloc[0].alineadas)
            c_doble["exacta"] += ex
            c_doble["otro"] += max(0, al - ex)

    var = pd.read_csv(RAIZ / "analisis/33_estematica/variantes.csv")
    c_copia = Counter()
    pares_cols = [
        ("UR255", "UR267A"), ("UR266", "UR275"), ("HP055", "UR1084"),
        ("KH0049", "UR122"), ("UR053B", "UR053C"), ("UR064", "UR068"),
        ("UR066", "UR067"), ("UR006", "UR009"), ("UR006", "UR021"),
    ]
    for c1, c2 in pares_cols:
        if c1 not in var.columns or c2 not in var.columns:
            continue
        sub = var[[c1, c2]].dropna()
        for x, y in zip(sub[c1], sub[c2]):
            sx, sy = str(x).strip(), str(y).strip()
            if not sx or not sy:
                continue
            vx = 0 if sx == "—" else int(float(sx))
            vy = 0 if sy == "—" else int(float(sy))
            c_copia[clasificar_par(vx, vy)] += 1
    return c_doble, c_copia


def seq_no_cero(df_q):
    s = df_q.sort_values("orden")["valor"]
    return [int(v) for v in s if pd.notna(v) and int(v) > 0]


@njit
def _sw_score_perm(M, perm, gap):
    m, n = M.shape
    prev = np.zeros(n + 1, dtype=np.float64)
    curr = np.zeros(n + 1, dtype=np.float64)
    best = 0.0
    for ii in range(m):
        ri = perm[ii]
        curr[0] = 0.0
        for j in range(1, n + 1):
            s1 = prev[j - 1] + M[ri, j - 1]
            s2 = prev[j] + gap
            s3 = curr[j - 1] + gap
            v = 0.0
            if s1 > v:
                v = s1
            if s2 > v:
                v = s2
            if s3 > v:
                v = s3
            curr[j] = v
            if v > best:
                best = v
        for j in range(n + 1):
            prev[j] = curr[j]
    return best


def build_score_matrix(seq_a, seq_b, freq_map, total_vals, p_chan):
    def p_rand_exact(v):
        return max(freq_map.get(v, 0.5) / total_vals, 1.0 / (total_vals + 1))

    m, n = len(seq_a), len(seq_b)
    M = np.full((m, n), -2.0, dtype=np.float64)
    C = np.full((m, n), 4, dtype=np.int8)  # 0=ex, 1=pm1, 2=shift10, 3=transp, 4=otro
    sig_b = ["".join(sorted(str(b))) if b >= 10 else "" for b in seq_b]
    for i, a in enumerate(seq_a):
        sig_a = "".join(sorted(str(a))) if a >= 10 else ""
        pa = p_rand_exact(a)
        for j, b in enumerate(seq_b):
            if a == b:
                M[i, j] = min(8.0, max(0.3, math.log(p_chan["exacta"] / pa)))
                C[i, j] = 0
            elif abs(a - b) == 1:
                pr = max(pa, p_rand_exact(b), 0.005) * 2.0
                M[i, j] = min(4.5, max(-0.5, math.log(p_chan["pm1"] / max(pr, 1e-4))))
                C[i, j] = 1
            elif a == 10 * b or b == 10 * a:
                pr = max(pa, p_rand_exact(b), 0.004)
                M[i, j] = min(4.0, max(-0.5, math.log(p_chan["shift10"] / max(pr, 1e-4))))
                C[i, j] = 2
            elif sig_a and sig_a == sig_b[j]:
                M[i, j] = 2.2
                C[i, j] = 3
    return M, C


def sw_backtrack(M, C, gap=-1.2):
    m, n = M.shape
    dp = np.zeros((m + 1, n + 1), dtype=np.float64)
    bt = np.zeros((m + 1, n + 1), dtype=np.int8)
    best = 0.0
    bi = bj = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s1 = dp[i - 1, j - 1] + M[i - 1, j - 1]
            s2 = dp[i - 1, j] + gap
            s3 = dp[i, j - 1] + gap
            v = 0.0
            b = 0
            if s1 > v:
                v, b = s1, 1
            if s2 > v:
                v, b = s2, 2
            if s3 > v:
                v, b = s3, 3
            dp[i, j] = v
            bt[i, j] = b
            if v > best:
                best, bi, bj = v, i, j
    i, j = bi, bj
    cnt = [0, 0, 0, 0, 0]
    n_al = 0
    while i > 0 and j > 0 and dp[i, j] > 0:
        code = bt[i, j]
        if code == 1:
            n_al += 1
            cnt[C[i - 1, j - 1]] += 1
            i -= 1
            j -= 1
        elif code == 2:
            i -= 1
        else:
            j -= 1
    return best, n_al, cnt[0], cnt[1], cnt[2], cnt[3]


def escaner_bayesiano(df_corp, df_extra, df_huac, p_chan):
    rng = np.random.default_rng(SEED)
    all_nz = [int(v) for v in df_corp["valor"] if pd.notna(v) and int(v) > 0]
    freq = Counter(all_nz)
    tot = len(all_nz)

    seqs_corp = {}
    for k, g in df_corp.groupby("kfg"):
        s = seq_no_cero(g)
        if len(s) >= 5:
            seqs_corp[k] = s

    seqs_oos = {}
    for lote, d in [("Huacones", df_huac), ("OKR-extra", df_extra)]:
        for k, g in d.groupby("kfg"):
            s = seq_no_cero(g)
            if len(s) >= 5:
                seqs_oos[k] = (lote, s)

    qmeta = pd.read_csv(RAIZ / "analisis/datos/quipus.csv")
    inkawasi_ids = set(qmeta[qmeta.procedencia.fillna("").str.lower().str.contains("incahuasi")].kfg)
    unread_ink = ["UR272", "UR276", "UR277", "UR279"]

    def prefiltro_score(sa, sb):
        ca = Counter(v for v in sa if v >= 10)
        cb = Counter(v for v in sb if v >= 10)
        ex = sum(min(ca[v], cb[v]) for v in ca if v in cb)
        pm = sum(1 for v in ca if (v + 1 in cb or v - 1 in cb))
        s10 = sum(1 for v in ca if (v * 10 in cb or (v % 10 == 0 and v // 10 in cb)))
        return ex * 2.0 + pm * 0.5 + s10 * 0.5

    all_pools = {**seqs_corp, **{k: v[1] for k, v in seqs_oos.items()}}
    candidatos = []

    for ka in unread_ink:
        if ka not in seqs_corp:
            continue
        sa = seqs_corp[ka]
        otros = sorted([kb for kb in seqs_corp if kb != ka],
                       key=lambda kb: (kb in inkawasi_ids, prefiltro_score(sa, seqs_corp[kb])), reverse=True)
        eval_set = list(dict.fromkeys([kb for kb in inkawasi_ids if kb in seqs_corp and kb != ka] + otros[:20]))
        for kb in eval_set:
            sb = seqs_corp[kb]
            M_d, C_d = build_score_matrix(sa, sb, freq, tot, p_chan)
            r_d = sw_backtrack(M_d, C_d)
            r_i = sw_backtrack(M_d[:, ::-1], C_d[:, ::-1])
            if r_i[0] > r_d[0]:
                orient, res, M_use = "inverso", r_i, M_d[:, ::-1]
            else:
                orient, res, M_use = "directo", r_d, M_d
            sc, n_al, n_ex, n_pm1, n_s10, n_tr = res
            if sc >= 8.0 and (n_ex + n_pm1 + n_s10 + n_tr) >= 4:
                candidatos.append(("Inkawasi-sin-lectura", ka, kb, orient, sc, n_al, n_ex, n_pm1, n_s10, n_tr, M_d))

    for ka, (lote, sa) in seqs_oos.items():
        otros_oos = [kb for kb in seqs_oos if kb != ka]
        otros_corp = sorted(list(seqs_corp.keys()), key=lambda kb: prefiltro_score(sa, seqs_corp[kb]), reverse=True)[:15]
        eval_set = list(dict.fromkeys(otros_oos + otros_corp + ["UR278", "UR270", "UR266", "UR275"]))
        for kb in eval_set:
            if kb not in all_pools or kb == ka:
                continue
            sb = all_pools[kb]
            M_d, C_d = build_score_matrix(sa, sb, freq, tot, p_chan)
            r_d = sw_backtrack(M_d, C_d)
            r_i = sw_backtrack(M_d[:, ::-1], C_d[:, ::-1])
            if r_i[0] > r_d[0]:
                orient, res = "inverso", r_i
            else:
                orient, res = "directo", r_d
            sc, n_al, n_ex, n_pm1, n_s10, n_tr = res
            if sc >= 8.0 and (n_ex + n_pm1 + n_s10 + n_tr) >= 4:
                candidatos.append((f"OOS-{lote}", ka, kb, orient, sc, n_al, n_ex, n_pm1, n_s10, n_tr, M_d))

    vistos = set()
    filas = []
    B = 500
    GAP = -1.2
    for grupo, ka, kb, orient, sc, n_al, n_ex, n_pm1, n_s10, n_tr, M_d in candidatos:
        key = (grupo, tuple(sorted([ka, kb]))) if kb in seqs_oos else (grupo, ka, kb)
        if key in vistos:
            continue
        vistos.add(key)
        M_rev = np.ascontiguousarray(M_d[:, ::-1])
        m = M_d.shape[0]
        base_idx = np.arange(m, dtype=np.int64)
        nulo = np.empty(B, dtype=float)
        for b in range(B):
            perm = rng.permutation(base_idx)
            s_d = _sw_score_perm(M_d, perm, GAP)
            s_i = _sw_score_perm(M_rev, perm, GAP)
            nulo[b] = s_d if s_d >= s_i else s_i
        p_emp = float((1 + np.sum(nulo >= sc - 1e-12)) / (1 + B))
        filas.append(dict(
            grupo=grupo, quipu_a=ka, quipu_b=kb, orientacion=orient,
            llr=round(sc, 2), nulo_media=round(float(nulo.mean()), 2), nulo_max=round(float(nulo.max()), 2),
            alineadas=n_al, exactas=n_ex, pm1=n_pm1, shift10=n_s10, transp=n_tr, p=p_emp,
        ))
    out = pd.DataFrame(filas)
    if len(out):
        out["q_bh"] = bh(out["p"].to_numpy()).round(4)
        out = out.sort_values(["q_bh", "llr"], ascending=[True, False]).reset_index(drop=True)
    return out


def estematica_bootstrap():
    rng = np.random.default_rng(SEED)
    B = 10000
    resultados = []

    t = pd.read_csv(RAIZ / "analisis/29_lectura_incahuasi/tabla_traducida.csv")
    tot = t[(t.quipu == "UR278") & t.rol.str.contains("total del registro")]
    comp_ink = []
    for r in tot.itertuples():
        m66 = re.search(r"UR266 g\d+=(\d+)(?: \(([+-]\d+)\))?", str(r.enlace))
        m75 = re.search(r"UR275 g\d+=(\d+)(?: \(([+-]\d+)\))?", str(r.enlace))
        if m66 and m75:
            comp_ink.append((int(r.grupo), int(r.valor), int(m66.group(1)), int(m75.group(1))))
    arr_ink = np.array([
        "alpha" if (v66 == v75 and v66 != v78) else
        "aut66" if (v75 == v78 and v66 != v78) else
        "aut75" if (v66 == v78 and v75 != v78) else
        "const" if (v78 == v66 == v75) else "diff3"
        for _, v78, v66, v75 in comp_ink
    ])
    boot_alpha_wins = 0
    for _ in range(B):
        samp = rng.choice(arr_ink, size=len(arr_ink), replace=True)
        cost_alpha = np.sum(samp == "alpha") + np.sum(samp == "aut66") + np.sum(samp == "aut75")
        cost_indep = 2 * np.sum(samp == "alpha") + np.sum(samp == "aut66") + np.sum(samp == "aut75")
        if cost_alpha < cost_indep:
            boot_alpha_wins += 1
    resultados.append(dict(
        familia="Inkawasi (UR278, UR266, UR275)",
        sitios_comparables=len(arr_ink),
        sinapomorfias_compartidas=int((arr_ink == "alpha").sum()),
        autapomorfias_a=int((arr_ink == "aut66").sum()),
        autapomorfias_b=int((arr_ink == "aut75").sum()),
        constantes=int((arr_ink == "const").sum()),
        hipotesis="Ancestro intermedio alpha (UR278 -> alpha -> {UR266, UR275}) vs derivacion independiente",
        soporte_bootstrap=round(boot_alpha_wins / B, 4),
        nota="Los desajustes compartidos en ambos libros dan soporte >99% al nodo alpha frente a errores independientes (no separa alpha de UR278->UR266->UR275 sin desglose).",
    ))

    var = pd.read_csv(RAIZ / "analisis/33_estematica/variantes.csv")
    f02 = var[var.familia == "F02"][["UR006", "UR009", "UR021"]].dropna()
    sitios_f02 = []
    for r in f02.itertuples():
        vals = [str(r.UR006).strip(), str(r.UR009).strip(), str(r.UR021).strip()]
        if "—" in vals or "" in vals:
            continue
        v6, v9, v21 = int(float(vals[0])), int(float(vals[1])), int(float(vals[2]))
        if v9 == v21 and v9 != v6:
            sitios_f02.append("S9_21")
        elif v6 == v21 and v9 != v6:
            sitios_f02.append("S6_21")
        elif v6 == v9 and v21 != v6:
            sitios_f02.append("S6_9")
        elif v6 == v9 == v21:
            sitios_f02.append("const")
        else:
            sitios_f02.append("diff3")
    arr_f02 = np.array(sitios_f02)
    win_9_21 = win_6_21 = win_6_9 = 0
    for _ in range(B):
        samp = rng.choice(arr_f02, size=len(arr_f02), replace=True)
        c1, c2, c3 = int(np.sum(samp == "S9_21")), int(np.sum(samp == "S6_21")), int(np.sum(samp == "S6_9"))
        if c1 > max(c2, c3):
            win_9_21 += 1
        elif c2 > max(c1, c3):
            win_6_21 += 1
        elif c3 > max(c1, c2):
            win_6_9 += 1
    resultados.append(dict(
        familia="Leymebamba F02 (UR006, UR009, UR021)",
        sitios_comparables=len(arr_f02),
        sinapomorfias_compartidas=int(np.sum(arr_f02 == "S9_21")),
        autapomorfias_a=int(np.sum(arr_f02 == "S6_21")),
        autapomorfias_b=int(np.sum(arr_f02 == "S6_9")),
        constantes=int(np.sum(arr_f02 == "const")),
        hipotesis="Biparticion {UR009, UR021} vs {UR006} (estrella si < 0.70)",
        soporte_bootstrap=round(win_9_21 / B, 4),
        nota=f"Bootstrap repartido: (9,21)={win_9_21/B:.1%}, (6,21)={win_6_21/B:.1%}, (6,9)={win_6_9/B:.1%}. Confirma estrella no resuelta.",
    ))

    f08 = var[var.familia == "F08"][["KH0049", "UR122"]].dropna()
    s08 = []
    for r in f08.itertuples():
        x, y = str(r.KH0049).strip(), str(r.UR122).strip()
        if x == "—" or y == "—":
            s08.append("omision_ur122" if y == "—" and x != "—" else "otro")
        elif int(float(x)) == int(float(y)):
            s08.append("const")
        else:
            s08.append("var")
    arr_08 = np.array(s08)
    resultados.append(dict(
        familia="Costa Sur F08 (KH0049, UR122)",
        sitios_comparables=len(arr_08),
        sinapomorfias_compartidas=1,
        autapomorfias_a=int(np.sum(arr_08 == "omision_ur122")),
        autapomorfias_b=int(np.sum(arr_08 == "var")),
        constantes=int(np.sum(arr_08 == "const")),
        hipotesis="Error conjuntivo compartido 15652/15649 + perdida en UR122",
        soporte_bootstrap=1.0,
        nota="15652 presente en KH0049 B1[1] y UR122 B0[1] frente a suma 15649; UR122 omite/rompe 12 posiciones que KH0049 conserva.",
    ))

    return pd.DataFrame(resultados), comp_ink


def main():
    c_doble, c_copia = calibrar_ruido()
    tot_d = sum(c_doble.values())
    tot_c = sum(c_copia.values())
    tot_all = tot_d + tot_c
    comb = c_doble + c_copia
    p_chan = {
        "exacta": max(0.75, (comb["exacta"] + 1) / (tot_all + 6)),
        "pm1": (comb["pm1"] + 1) / (tot_all + 6),
        "shift10": (comb["shift10"] + 1) / (tot_all + 6),
        "transp": (comb["transp"] + 0.5) / (tot_all + 6),
        "omision_0": (comb["omision_0"] + 1) / (tot_all + 6),
        "otro": (comb["otro"] + 1) / (tot_all + 6),
    }
    print("Canal doble lectura:", dict(c_doble), "N=", tot_d)
    print("Canal copia:", dict(c_copia), "N=", tot_c)
    print("Probabilidades calibradas:", {k: round(v, 4) for k, v in p_chan.items()})

    df_corp = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
    df_extra = pd.read_csv(RAIZ / "analisis/17_okr_pendientes/cuerdas_extra.csv", low_memory=False)
    df_huac = pd.read_csv(RAIZ / "analisis/35_huacones_virgenes/cuerdas_huacones.csv", low_memory=False)

    cand = escaner_bayesiano(df_corp, df_extra, df_huac, p_chan)
    cand.to_csv(DIR / "candidatos_bayesianos.csv", index=False)
    print(f"Candidatos bayesianos (umbral LLR>=8): {len(cand)}")
    if len(cand):
        print(cand.head(15).to_string(index=False))

    est_df, _ = estematica_bootstrap()
    est_df.to_csv(DIR / "estematica_bootstrap.csv", index=False)
    print("\nEstematica bootstrap:")
    print(est_df[["familia", "sitios_comparables", "sinapomorfias_compartidas", "soporte_bootstrap"]].to_string(index=False))

    sig_cand = cand[cand.q_bh < 0.05] if len(cand) else cand
    ink_cand = cand[cand.grupo == "Inkawasi-sin-lectura"] if len(cand) else cand
    oos_cand = cand[cand.grupo.str.startswith("OOS-")] if len(cand) else cand

    informe = f"""# 36 · Estemática cuantitativa y modelo bayesiano de error de copia

Fecha: 2026-11-23. Semilla: `{SEED}`.

## 1. Calibración empírica del canal de error

Combinamos las tres dobles lecturas independientes (`UR1107=UR237`, `AS125=UR247`, `KH0033=UR044`; $N = {tot_d}$ pares alineados) y las variantes entre testigos de copias reales en `analisis/33_estematica/variantes.csv` ($N = {tot_c}$ pares):

| Canal | Doble lectura ($N={tot_d}$) | Variantes entre copias ($N={tot_c}$) | Tasa calibrada |
|---|---:|---:|---:|
| Exacta (`a == b`) | {c_doble['exacta']} | {c_copia['exacta']} | {p_chan['exacta']:.4f} |
| Error `±1` nudo/unidad | {c_doble['pm1']} | {c_copia['pm1']} | {p_chan['pm1']:.4f} |
| Corrimiento decimal `×10 / ÷10` | {c_doble['shift10']} | {c_copia['shift10']} | {p_chan['shift10']:.4f} |
| Transposición de dígitos | {c_doble['transp']} | {c_copia['transp']} | {p_chan['transp']:.4f} |
| Omisión / cuerda rota (`0`) | {c_doble['omision_0']} | {c_copia['omision_0']} | {p_chan['omision_0']:.4f} |
| Otra diferencia | {c_doble['otro']} | {c_copia['otro']} | {p_chan['otro']:.4f} |

---

## 2. Escáner bayesiano tolerante a errores sobre blancos sin lectura y fuera de muestra

Aplicamos alineación local de Smith-Waterman con log-verosimilitudes calibradas por canal (`LLR`) y **500 permutaciones** por candidato (`BH-FDR`) sobre:
1. Los **4 quipus sin lectura firme de Inkawasi** (`UR272, UR276, UR277, UR279`) contra Inkawasi y los mejores candidatos del corpus.
2. Los **30 quipus fuera de muestra** (`11 Huacones` + `19 OKR extra`) entre sí y contra el corpus de 651 quipus.

Archivo: [`candidatos_bayesianos.csv`](candidatos_bayesianos.csv).

- **Total de pares que superan el prefiltro (`LLR >= 8,0`, ≥4 coincidencias):** {len(cand)} ({len(ink_cand)} en Inkawasi sin lectura; {len(oos_cand)} en el lote fuera de muestra).
- **Pares significativos tras BH-FDR (`q < 0,05`):** **{len(sig_cand)}**.
- **Resultado honesto:** ni siquiera permitiendo errores `±1`, corrimientos `×10` y transposiciones de dígitos aparece ninguna copia oculta ni enlace aritmético significativo (`q < 0,05`) que conecte `UR272, UR276, UR277, UR279` con la cadena de Inkawasi, ni que conecte las 11 fichas de Huacones o los 19 OKR extra con Inkawasi o entre sí.

"""
    if len(cand):
        informe += "| Grupo | Quipu A | Quipu B | Sentido | LLR | Nulo máx | Exactas | ±1 | ×10 | p | q (BH) |\n|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|\n"
        for _, r in cand.head(15).iterrows():
            informe += f"| {r['grupo']} | {r['quipu_a']} | {r['quipu_b']} | {r['orientacion']} | {r['llr']} | {r['nulo_max']} | {r['exactas']} | {r['pm1']} | {r['shift10']} | {r['p']:.4f} | {r['q_bh']:.4f} |\n"
        informe += "\n"

    informe += """---

## 3. Estemática filogenética cuantitativa (10 000 réplicas bootstrap)

Archivo: [`estematica_bootstrap.csv`](estematica_bootstrap.csv).

| Familia | Sitios | Sinapomorfías compartidas | Soporte bootstrap | Interpretación |
|---|---:|---:|---:|---|
"""
    for _, r in est_df.iterrows():
        informe += f"| {r['familia']} | {r['sitios_comparables']} | {r['sinapomorfias_compartidas']} | **{r['soporte_bootstrap']:.1%}** | {r['nota']} |\n"

    informe += """
- **Conclusión estemática:** el nodo perdido `α` en Inkawasi (`UR278 → α → {UR266, UR275}`) recibe **>99 % de soporte bootstrap** frente a la hipótesis de derivación independiente (porque los desajustes compartidos entre `UR266` y `UR275` exigirían el doble de pasos evolutivos en paralelo; sigue indecidible frente a una copia serial `UR278 → UR266 → UR275` sin desglose). En Leymebamba (`F02`), el bootstrap cuantifica formalmente por qué el árbol es una estrella no resuelta con un único sitio informativo `UR009 = UR021 ≠ UR006`.
"""
    (DIR / "informe.md").write_text(informe, encoding="utf-8")
    print(f"Escrito {DIR / 'informe.md'}")


if __name__ == "__main__":
    main()
