# -*- coding: utf-8 -*-
"""Integra y analiza tres fuentes virgenes dentro de OKR:
  A. JS01 (KH0676, Brooklyn 36.718): parsing de Pendant Detail a esquema cuerdas.csv
  B. RT-16905 (KH0638-KH0652): red fisica de enlaces del croquis vs valores de cuerdas_extra.csv
  C. UR-298 (KH0675, Dumbarton Oaks PC.WBC.2016.071.pdf): prueba fuera de muestra de huecos de cero

Uso: python analisis/37_vision_y_extra/integrar_js01_y_enlazados.py
"""
import csv
import re
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from scipy.stats import mannwhitneyu

RAIZ = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
SEED = 20261123


def parse_js01():
    xlsx = RAIZ / "data/external/open-khipu-repository/data/KH0676/JS01_Strauss_Harvard_Senior_Thesis.xlsx"
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    rows = list(wb["Pendant Detail"].iter_rows(values_only=True))[6:]
    wb.close()

    cols = ["kfg", "orden", "cuerda", "tipo", "nivel", "padre", "grupo", "valor", "alt",
            "nudos", "color", "torsion", "union", "largo", "terminacion", "notas"]
    out_rows = []
    n_non_dec = 0
    n_knotted = 0
    n_sp = 0

    for idx, r in enumerate(rows):
        cnum_raw, spin, ply, att, knots_raw, length, term, color, subs, photo = r[:10]
        if cnum_raw is None:
            continue
        cs = str(cnum_raw).strip()
        parts = cs.split("s")
        cuerda = f"p{cs}"
        nivel = len(parts) - 1
        padre = "" if nivel == 0 else f"p{'s'.join(parts[:-1])}"

        torsion = str(ply).strip().upper() if ply and str(ply).strip() not in ("-", "") else "U"
        union = str(att).strip().upper() if att and str(att).strip() not in ("-", "") else ""
        color_s = "" if color is None else str(color).strip()
        largo = "" if length is None or str(length).strip() in ("", "-") else float(length)
        term_s = "" if term is None else str(term).strip()

        kstr = "" if knots_raw is None else str(knots_raw).strip()
        nudos_norm = []
        val_total = 0
        ordenes = []
        notas = ["fuente: JS01_Strauss_Harvard_Senior_Thesis.xlsx (KH0676)"]

        if kstr and kstr != "--":
            n_knotted += 1
            for m in re.finditer(r"(\d+)(SP|[sLe])\(([\d.]+)/(z|s)\)", kstr, re.I):
                cnt = int(m.group(1))
                kt = m.group(2)
                pos = float(m.group(3))
                dr = m.group(4).upper()
                if kt == "s":
                    v = cnt * 10
                    kt_norm = "S"
                    ordenes.append(1)
                elif kt == "L":
                    v = cnt
                    kt_norm = "L"
                    ordenes.append(0)
                elif kt == "e":
                    v = cnt
                    kt_norm = "E"
                    ordenes.append(0)
                else:  # SP
                    v = cnt
                    kt_norm = "S"
                    n_sp += 1
                    notas.append(f"nudo especial {cnt}SP")
                    ordenes.append(0)
                val_total += v
                nudos_norm.append(f"{cnt}{kt_norm}({pos},{dr}),{v}")

            # Verificar si rompe orden decimal estricto (lugares repetidos o orden invertido de arriba abajo)
            if len(ordenes) != len(set(ordenes)) or ordenes != sorted(ordenes, reverse=True):
                n_non_dec += 1
                notas.append("gramatica no decimal / orden aditivo")

        out_rows.append([
            "JS01", idx, cuerda, "p", nivel, padre, 0, val_total, "",
            ";".join(nudos_norm), color_s, torsion, union, largo, term_s, "; ".join(notas)
        ])

    out_csv = DIR / "cuerdas_js01.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(out_rows)

    resumen = dict(
        cuerdas=len(out_rows),
        colgantes=sum(1 for r in out_rows if r[4] == 0),
        subsidiarias=sum(1 for r in out_rows if r[4] > 0),
        anudadas=n_knotted,
        no_decimales=n_non_dec,
        frac_no_dec=round(n_non_dec / n_knotted, 4) if n_knotted else 0.0,
        suma_total=sum(r[7] for r in out_rows),
        nudos_sp=n_sp,
    )
    print("JS01:", resumen)
    return resumen


def analizar_rt16905():
    # Mapa del croquis Croquis KhipusEnlazadosEnglish.jpg:
    # Hubs: C={10,11,12}, A={11,12,13,14}, B={1,13,14,15}, D={2,3,4}, E={1,4}, Zona_F={5,6,7}, G={4,8,9}
    hubs = {
        "Hub_C": [10, 11, 12],
        "Hub_A": [11, 12, 13, 14],
        "Hub_B": [1, 13, 14, 15],
        "Hub_D": [2, 3, 4],
        "Hub_E": [1, 4],
        "Zona_F": [5, 6, 7],
        "Hub_G": [4, 8, 9],
    }
    num_to_kh = {i: f"KH{637 + i:04d}" for i in range(1, 16)}
    kh_hubs = {num_to_kh[i]: [] for i in range(1, 16)}
    for h, nums in hubs.items():
        for i in nums:
            kh_hubs[num_to_kh[i]].append(h)

    ex = pd.read_csv(RAIZ / "analisis/17_okr_pendientes/cuerdas_extra.csv", low_memory=False)
    nodes = [f"KH{i:04d}" for i in range(638, 652)]  # 1..14 en cuerdas_extra.csv (15=KH0652 es marco de hilos)

    stats = {}
    for k in nodes:
        sub = ex[ex.kfg == k]
        vals = set(int(v) for v in sub.valor.dropna() if int(v) > 0)
        stats[k] = dict(
            n=len(sub),
            suma=int(sub.valor.fillna(0).sum()),
            largo_med=float(sub.largo.dropna().median()) if sub.largo.notna().any() else np.nan,
            vals=vals,
        )

    pares_filas = []
    linked_jacc, unlinked_jacc = [], []
    linked_ldiff, unlinked_ldiff = [], []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            shared = sorted(set(kh_hubs[a]) & set(kh_hubs[b]))
            is_link = len(shared) > 0
            va, vb = stats[a]["vals"], stats[b]["vals"]
            jacc = len(va & vb) / len(va | vb) if (va | vb) else 0.0
            ldiff = abs(stats[a]["largo_med"] - stats[b]["largo_med"])
            pares_filas.append(dict(
                quipu_a=a, quipu_b=b, enlazados=int(is_link), hubs=";".join(shared),
                jaccard_valores=round(jacc, 4), dif_largo_cm=round(ldiff, 2) if not np.isnan(ldiff) else None,
            ))
            if is_link:
                linked_jacc.append(jacc)
                if not np.isnan(ldiff):
                    linked_ldiff.append(ldiff)
            else:
                unlinked_jacc.append(jacc)
                if not np.isnan(ldiff):
                    unlinked_ldiff.append(ldiff)

    # Nulo por permutacion de etiquetas de quipus sobre el grafo (B=2000)
    rng = np.random.default_rng(SEED)
    obs_diff_j = float(np.mean(linked_jacc) - np.mean(unlinked_jacc))
    obs_diff_l = float(np.mean(unlinked_ldiff) - np.mean(linked_ldiff))
    edge_pairs = [(i, j) for i in range(len(nodes)) for j in range(i + 1, len(nodes))
                  if set(kh_hubs[nodes[i]]) & set(kh_hubs[nodes[j]])]
    edge_set = set(edge_pairs)
    n_tot_pairs = len(nodes) * (len(nodes) - 1) // 2
    ge_j = ge_l = 0
    B = 2000
    for _ in range(B):
        perm = rng.permutation(len(nodes))
        lj, uj, ll, ul = [], [], [], []
        for a_i in range(len(nodes)):
            for b_i in range(a_i + 1, len(nodes)):
                ka, kb = nodes[perm[a_i]], nodes[perm[b_i]]
                va, vb = stats[ka]["vals"], stats[kb]["vals"]
                jc = len(va & vb) / len(va | vb) if (va | vb) else 0.0
                ld = abs(stats[ka]["largo_med"] - stats[kb]["largo_med"])
                if (a_i, b_i) in edge_set:
                    lj.append(jc)
                    if not np.isnan(ld):
                        ll.append(ld)
                else:
                    uj.append(jc)
                    if not np.isnan(ld):
                        ul.append(ld)
        if np.mean(lj) - np.mean(uj) >= obs_diff_j - 1e-12:
            ge_j += 1
        if np.mean(ul) - np.mean(ll) >= obs_diff_l - 1e-12:
            ge_l += 1

    pd.DataFrame(pares_filas).to_csv(DIR / "red_rt16905.csv", index=False)
    res = dict(
        n_nodos=len(nodes), n_pares=n_tot_pairs, n_enlazados=len(edge_pairs),
        jacc_enlazados=round(float(np.mean(linked_jacc)), 4),
        jacc_no_enlazados=round(float(np.mean(unlinked_jacc)), 4),
        p_jacc=round((1 + ge_j) / (1 + B), 4),
        ldiff_enlazados=round(float(np.mean(linked_ldiff)), 2),
        ldiff_no_enlazados=round(float(np.mean(unlinked_ldiff)), 2),
        p_largo=round((1 + ge_l) / (1 + B), 4),
    )
    print("RT-16905:", res)
    return res


def analizar_ur298_ceros():
    """Prueba fuera de muestra de huecos de cero sobre UR-298 (KH0675, PC.WBC.2016.071.pdf)."""
    # Intervalos medidos directamente en las hojas manuscritas de PC.WBC.2016.071.pdf (pp. 2, 3, 10, 13, 17, 18)
    # Formato: (cuerda, valor, tipo_intervalo, pos1_cm, pos2_cm, pagina)
    intervalos = [
        # Huecos con cero intermedio (salto de 2 ordenes decimales)
        ("p72", 105, "cero_intermedio", 8.0, 18.5, 10),
        ("p73", 608, "cero_intermedio", 8.0, 18.5, 10),
        ("p80", 609, "cero_intermedio", 9.0, 20.5, 10),
        ("p117", 805, "cero_intermedio", 9.0, 20.5, 13),
        ("p124", 104, "cero_intermedio", 8.0, 18.5, 13),
        ("p125", 102, "cero_intermedio", 8.5, 19.0, 13),
        ("p126", 103, "cero_intermedio", 8.5, 19.0, 13),
        ("p127", 103, "cero_intermedio", 9.0, 19.0, 13),
        ("p129", 102, "cero_intermedio", 9.5, 19.0, 13),
        ("p188", 18067, "cero_intermedio", 6.5, 17.0, 17),
        ("p191", 2084, "cero_intermedio", 4.0, 15.0, 17),
        ("p192", 1083, "cero_intermedio", 4.0, 14.5, 17),
        ("p196", 1040, "cero_intermedio", 3.5, 14.0, 17),
        # Intervalos adyacentes sin cero (en esas mismas cuerdas y controles de pp. 2, 3, 17, 18)
        ("p188", 18067, "adyacente", 1.0, 6.5, 17),
        ("p188", 18067, "adyacente", 17.0, 24.5, 17),
        ("p191", 2084, "adyacente", 15.0, 23.5, 17),
        ("p192", 1083, "adyacente", 14.5, 21.0, 17),
        ("p1", 551, "adyacente", 9.5, 14.0, 2),
        ("p1", 551, "adyacente", 14.0, 19.0, 2),
        ("p2", 270, "adyacente", 9.5, 14.0, 2),
        ("p3", 125, "adyacente", 9.5, 14.0, 2),
        ("p3", 125, "adyacente", 14.0, 19.5, 2),
        ("p4", 295, "adyacente", 9.0, 13.5, 2),
        ("p4", 295, "adyacente", 13.5, 19.0, 2),
        ("p19", 212, "adyacente", 10.0, 14.5, 3),
        ("p19", 212, "adyacente", 14.5, 21.5, 3),
        ("p20", 134, "adyacente", 10.0, 15.0, 3),
        ("p20", 134, "adyacente", 15.0, 21.5, 3),
        ("p21", 226, "adyacente", 10.0, 15.0, 3),
        ("p21", 226, "adyacente", 15.0, 21.5, 3),
        ("p22", 234, "adyacente", 10.0, 15.5, 3),
        ("p22", 234, "adyacente", 15.5, 21.5, 3),
        ("p23", 174, "adyacente", 10.0, 15.5, 3),
        ("p23", 174, "adyacente", 15.5, 21.5, 3),
        ("p24", 116, "adyacente", 10.0, 15.5, 3),
        ("p24", 116, "adyacente", 15.5, 21.0, 3),
        ("p184", 1190, "adyacente", 4.0, 9.0, 17),
        ("p184", 1190, "adyacente", 9.0, 15.0, 17),
        ("p185", 1758, "adyacente", 4.0, 9.0, 17),
        ("p185", 1758, "adyacente", 9.0, 15.0, 17),
        ("p185", 1758, "adyacente", 15.0, 21.0, 17),
        ("p189", 2755, "adyacente", 4.0, 9.5, 17),
        ("p189", 2755, "adyacente", 9.5, 16.0, 17),
        ("p189", 2755, "adyacente", 16.0, 19.0, 17),
        ("p193", 1136, "adyacente", 4.5, 7.5, 17),
        ("p193", 1136, "adyacente", 7.5, 16.5, 17),
        ("p193", 1136, "adyacente", 16.5, 22.5, 17),
        ("p194", 1675, "adyacente", 4.0, 9.0, 17),
        ("p194", 1675, "adyacente", 9.0, 14.5, 17),
        ("p194", 1675, "adyacente", 14.5, 21.5, 17),
        ("p195", 853, "adyacente", 10.0, 15.5, 17),
        ("p195", 853, "adyacente", 15.5, 22.0, 17),
        ("p197", 15980, "adyacente", 1.0, 4.0, 18),
        ("p197", 15980, "adyacente", 4.0, 9.0, 18),
        ("p197", 15980, "adyacente", 9.0, 14.5, 18),
        ("p201", 1486, "adyacente", 4.0, 10.0, 18),
        ("p201", 1486, "adyacente", 10.0, 15.5, 18),
        ("p201", 1486, "adyacente", 15.5, 21.0, 18),
    ]
    rows = []
    for c, v, t, p1, p2, pag in intervalos:
        rows.append(dict(cuerda=c, valor=v, tipo=t, pos1_cm=p1, pos2_cm=p2, distancia_cm=round(p2 - p1, 2), pagina=pag))
    df = pd.DataFrame(rows)
    df.to_csv(DIR / "ur298_ceros_oos.csv", index=False)

    ceros = df[df.tipo == "cero_intermedio"].distancia_cm.to_numpy()
    adjs = df[df.tipo == "adyacente"].distancia_cm.to_numpy()
    u_stat, p_u = mannwhitneyu(ceros, adjs, alternative="greater")

    # Comparacion intracuerda en p188, p191, p192
    intra = [
        round(10.5 / np.mean([5.5, 7.5]), 3),  # p188
        round(11.0 / 8.5, 3),                  # p191
        round(10.5 / 6.5, 3),                  # p192
    ]
    res = dict(
        n_ceros=len(ceros),
        n_adyacentes=len(adjs),
        mediana_cero_cm=round(float(np.median(ceros)), 2),
        mediana_adj_cm=round(float(np.median(adjs)), 2),
        razon_medianas=round(float(np.median(ceros) / np.median(adjs)), 3),
        razones_intracuerda=intra,
        mediana_intracuerda=round(float(np.median(intra)), 3),
        mannwhitney_u=float(u_stat),
        p_u=float(p_u),
    )
    print("UR-298 ceros OOS:", res)
    return res


def main():
    r_js = parse_js01()
    r_rt = analizar_rt16905()
    r_ur = analizar_ur298_ceros()
    # Guardar resumen JSON para el informe conjunto
    import json
    (DIR / "resumen_extra.json").write_text(
        json.dumps(dict(js01=r_js, rt16905=r_rt, ur298=r_ur), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
